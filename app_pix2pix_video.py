import gradio as gr
from model import Model
from modules import scripts
import os

def create_demo(model: Model):
    examples = [
        [os.path.join(scripts.basedir(),'extensions/Text2Video-Zero', '__assets__/pix2pix video/camel.mp4'), 'make it Van Gogh Starry Night style'],
        [os.path.join(scripts.basedir(),'extensions/Text2Video-Zero','__assets__/pix2pix video/mini-cooper.mp4'), 'make it Picasso style'],
        [os.path.join(scripts.basedir(),'extensions/Text2Video-Zero','__assets__/pix2pix video/snowboard.mp4'), 'replace man with robot'],
        [os.path.join(scripts.basedir(),'extensions/Text2Video-Zero','__assets__/pix2pix video/white-swan.mp4'), 'replace swan with mallard'],
    ]
    with gr.Blocks() as demo:
        with gr.Row():
            gr.Markdown('## Video Instruct Pix2Pix')
        with gr.Row():
            gr.HTML(
                """
                <div style="text-align: left; auto;">
                <h2 style="font-weight: 450; font-size: 1rem; margin: 0rem">
                    Description: For performance purposes, our current preview release supports any input videos but caps output videos to no longer than 15 seconds and the input videos are scaled down before processing. For faster inference you can choose lower output frames per seconds from Advanced Options.
                </h3>
                </div>
                """)

        with gr.Row():
            with gr.Column():
                input_image = gr.Video(label="Input Video",source='upload', type='numpy', format="mp4", visible=True).style(height="auto")
            with gr.Column():
                prompt = gr.Textbox(label='Prompt')
                run_button = gr.Button(label='Run')
                with gr.Accordion('Advanced options', open=False):
                    image_resolution = gr.Slider(label='Image Resolution',
                                                 minimum=256,
                                                 maximum=1024,
                                                 value=512,
                                                 step=64)
                    seed = gr.Slider(label='Seed',
                                     minimum=0,
                                     maximum=65536,
                                     value=0,
                                     step=1)
                    start_t = gr.Slider(label='Starting time in seconds',
                                        minimum=0,
                                        maximum=10,
                                        value=0,
                                        step=1)
                    end_t = gr.Slider(label='End time in seconds',
                                      minimum=0,
                                      maximum=15,
                                      step=1)
                    out_fps = gr.Slider(label='Output video fps',
                                        minimum=1,
                                        maximum=30,
                                        value=-1,
                                        step=1)
            with gr.Column():
                result = gr.Video(label='Output',
                                    show_label=True)
        inputs = [
            input_image,
            prompt,
            image_resolution,
            seed,
            start_t,
            end_t,
            out_fps
        ]

        gr.Examples(examples=examples,
                    inputs=inputs,
                    outputs=result,
                    fn=model.process_pix2pix,
                    cache_examples=True,
                    run_on_click=False,
                    )

        run_button.click(fn=model.process_pix2pix,
                         inputs=inputs,
                         outputs=result)
    return demo
