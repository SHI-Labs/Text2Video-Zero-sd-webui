import gradio as gr
import os

from model import Model

from modules import scripts

examples = [
    ['Motion 1', "A Robot is dancing in Sahara desert"],
    ['Motion 2', "A Robot is dancing in Sahara desert"],
    ['Motion 3', "A Robot is dancing in Sahara desert"],
    ['Motion 4', "A Robot is dancing in Sahara desert"],
    ['Motion 5', "A Robot is dancing in Sahara desert"],
]

def create_demo(model: Model):
    with gr.Blocks() as demo:
        with gr.Row():
            gr.Markdown('## Text and Pose Conditional Video Generation')
        # with gr.Row():
        #     gr.HTML(
        #         """
        #         <div style="text-align: left; auto;">
        #         <h2 style="font-weight: 450; font-size: 1rem; margin: 0rem">
        #             Description: 
        #         </h3>
        #         </div>
        #         """)

        with gr.Row():
            gr.Markdown('### You must select one pose sequence shown on the right, or use the examples')
            with gr.Column():
                gallery_pose_sequence = gr.Gallery(label="Pose Sequence", value=[(os.path.join(scripts.basedir(), 'extensions/Text2Video-Zero-sd-webui', '__assets__/poses_skeleton_gifs/dance1.gif'), "Motion 1"), (os.path.join(scripts.basedir(), 'extensions/Text2Video-Zero-sd-webui','__assets__/poses_skeleton_gifs/dance2.gif'), "Motion 2"), (os.path.join(scripts.basedir(), 'extensions/Text2Video-Zero-sd-webui', '__assets__/poses_skeleton_gifs/dance3.gif'), "Motion 3"), (os.path.join(scripts.basedir(), 'extensions/Text2Video-Zero-sd-webui', '__assets__/poses_skeleton_gifs/dance4.gif'), "Motion 4"), (os.path.join(scripts.basedir(), 'extensions/Text2Video-Zero-sd-webui', '__assets__/poses_skeleton_gifs/dance5.gif'), "Motion 5")]).style(grid=[2], height="auto")
                input_video_path = gr.Textbox(label="Pose Sequence",visible=False,value="Motion 1")
                gr.Markdown("## Selection")
                pose_sequence_selector = gr.Markdown('Pose Sequence: **Motion 1**')
            with gr.Column():
                prompt = gr.Textbox(label='Prompt')
                run_button = gr.Button(label='Run')
            with gr.Column():
                result = gr.Image(label="Generated Video")

        input_video_path.change(on_video_path_update, None, pose_sequence_selector)
        gallery_pose_sequence.select(pose_gallery_callback, None, input_video_path)
        inputs = [
            input_video_path,
            prompt,
        ]

        gr.Examples(examples=examples,
                    inputs=inputs,
                    outputs=result,
                    fn=model.process_controlnet_pose,
                    cache_examples = True,
                    run_on_click=False,
                    )

        run_button.click(fn=model.process_controlnet_pose,
                         inputs=inputs,
                         outputs=result,)

    return demo


def on_video_path_update(evt: gr.EventData):
    return f'Pose Sequence: **{evt._data}**'

def pose_gallery_callback(evt: gr.SelectData):
    return f"Motion {evt.index+1}"
