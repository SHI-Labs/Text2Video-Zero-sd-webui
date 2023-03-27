from text_to_video.tuneavideo.pipelines.pipeline_text_to_video import TuneAVideoPipeline
from text_to_video.tuneavideo.models.unet import UNet3DConditionModel
import torch
from diffusers import AutoencoderKL, DDIMScheduler
from transformers import CLIPTextModel, CLIPTokenizer


class TextToVideo():

    
    def __init__(self,sd_path = None,motion_field_strength = 12, video_length = 8,t0 = 881, t1=941,use_cf_attn=True,use_motion_field=True) -> None:
        g = torch.Generator(device='cuda')
        g.manual_seed(22)
        self.g = g

        assert sd_path is not None
        
        print(f"Loading model SD-Net model file from {sd_path}")

        self.dtype = torch.float16
        noise_scheduler = DDIMScheduler.from_pretrained(
            sd_path, subfolder="scheduler")
        tokenizer = CLIPTokenizer.from_pretrained(
            sd_path, subfolder="tokenizer")
        text_encoder = CLIPTextModel.from_pretrained(
            sd_path, subfolder="text_encoder")
        vae = AutoencoderKL.from_pretrained(sd_path, subfolder="vae")


        unet = UNet3DConditionModel.from_pretrained_2d(
            sd_path, subfolder="unet", use_cf_attn=use_cf_attn)
        self.pipe = TuneAVideoPipeline(
            vae=vae, text_encoder=text_encoder, tokenizer=tokenizer, unet=unet,
            scheduler=DDIMScheduler.from_pretrained(
                sd_path, subfolder="scheduler")
        ).to('cuda').to(self.dtype)

        noise_scheduler.set_timesteps(50, device='cuda')

        # t0 parameter (DDIM backward from noise until t0)
        self.t0 = t0
        

        # from t0 apply DDPM forward until t1
        self.t1 = t1

        self.use_foreground_motion_field = False  # apply motion field on forground object (not used)

        # strength of motion field (delta_x = delta_y in Sect 3.3.1)
        self.motion_field_strength = motion_field_strength
        self.use_motion_field = use_motion_field  # apply general motion field
        self.smooth_bg = False  # temporally smooth background
        self.smooth_bg_strength = 0.4  # alpha = (1-self.smooth_bg_strength) in Eq (9)


        self.video_length = video_length
        
    def inference(self, prompt):

        prompt_compute = [prompt]
        xT = torch.randn((1, 4, 1, 64, 64), dtype=self.dtype, device="cuda")
        result = self.pipe(prompt_compute,
                           video_length=self.video_length,
                           height=512,
                           width=512,
                           num_inference_steps=50,
                           guidance_scale=7.5,
                           guidance_stop_step=1.0,
                           t0=self.t0,
                           t1=self.t1,
                           xT=xT,
                           use_foreground_motion_field=self.use_foreground_motion_field,
                           motion_field_strength=self.motion_field_strength,
                           use_motion_field=self.use_motion_field,
                           smooth_bg=self.smooth_bg,
                           smooth_bg_strength=self.smooth_bg_strength,
                           generator=self.g)

        return result.videos[0]
