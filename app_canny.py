import gradio as gr
from model import Model
from modules import scripts

def create_demo(model: Model):

    examples = [
        ["extensions/Text2Video-Zero-sd-webui/__assets__/canny_videos_edge/butterfly.mp4", "white butterfly, a high-quality, detailed, and professional photo"],
        ["extensions/Text2Video-Zero-sd-webui/__assets__/canny_videos_edge/deer.mp4", "oil painting of a deer, a high-quality, detailed, and professional photo"],
        ["extensions/Text2Video-Zero-sd-webui/__assets__/canny_videos_edge/fox.mp4", "wild red fox is walking on the grass, a high-quality, detailed, and professional photo"],
        ["extensions/Text2Video-Zero-sd-webui/__assets__/canny_videos_edge/girl_dancing.mp4", "oil painting of a girl dancing close-up, masterpiece, a high-quality, detailed, and professional photo"],
        ["extensions/Text2Video-Zero-sd-webui/__assets__/canny_videos_edge/girl_turning.mp4", "oil painting of a beautiful girl, a high-quality, detailed, and professional photo"],
        ["extensions/Text2Video-Zero-sd-webui/__assets__/canny_videos_edge/halloween.mp4", "beautiful girl halloween style, a high-quality, detailed, and professional photo"],
        ["extensions/Text2Video-Zero-sd-webui/__assets__/canny_videos_edge/santa.mp4", "a santa claus, a high-quality, detailed, and professional photo"],
    ]

    with gr.Blocks() as demo:
        with gr.Row():
            gr.Markdown('## Text and Canny-Edge Conditional Video Generation')
        with gr.Row():
            gr.HTML(
                """
                <div style="text-align: left; auto;">
                <h2 style="font-weight: 450; font-size: 1rem; margin: 0rem">
                    Description: For performance purposes, our current preview release supports any input videos but caps output videos to no longer than 15 seconds and the input videos are scaled down before processing.
                </h3>
                </div>
                """)

        with gr.Row():
            with gr.Column():
                input_video = gr.Video(label="Input Video",source='upload', format="mp4", visible=True).style(height="auto")
            with gr.Column():
                prompt = gr.Textbox(label='Prompt')
                run_button = gr.Button(label='Run')
            with gr.Column():
                result = gr.Video(label="Generated Video").style(height="auto")

        inputs = [
            input_video,
            prompt, 
        ]

        gr.Examples(examples=examples,
                    inputs=inputs,
                    outputs=result,
                    fn=model.process_controlnet_canny,
                    cache_examples = True,
                    run_on_click=False,
                    )

        run_button.click(fn=model.process_controlnet_canny,
                         inputs=inputs,
                         outputs=result,)
    return demo
