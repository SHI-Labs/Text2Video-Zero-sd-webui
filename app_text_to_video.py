import gradio as gr
from model import Model
from functools import partial

examples = [
    ["an astronaut waving the arm on the moon"],
    ["a sloth surfing on a wakeboard"],
    ["an astronaut walking on a street"],
    ["a cute cat walking on grass"],
    ["a horse is galloping on a street"],
    ["an astronaut is skiing down the hill"],
    ["a gorilla walking alone down the street"],
    ["a gorilla dancing on times square"],
    ["A panda dancing dancing like crazy on Times Square"],
    ]


def create_demo(model: Model):

    with gr.Blocks() as demo:
        with gr.Row():
            gr.Markdown('## Text2Video-Zero: Video Generation')
        with gr.Row():
            gr.HTML(
                """
                <div style="text-align: left; auto;">
                <h2 style="font-weight: 450; font-size: 1rem; margin: 0rem">
                    Description: Simply input <b>any textual prompt</b> to generate videos right away and unleash your creativity and imagination! You can also select from the examples below. For performance purposes, our current preview release generates only 8 output frames and output 4s videos.
                </h3>
                </div>
                """)

        with gr.Row():
            with gr.Column():
                prompt = gr.Textbox(label='Prompt')
                run_button = gr.Button(label='Run')
                with gr.Accordion('Advanced options', open=False):
                    motion_field_strength_x = gr.Slider(label='Global Translation $\delta_{x}$',
                                     minimum=-20,
                                     maximum=20,
                                     value=12,
                                     step=1)
                
                    motion_field_strength_y = gr.Slider(label='Global Translation $\delta_{y}$',
                                     minimum=-20,
                                     maximum=20,
                                     value=12,
                                     step=1)
                #     a_prompt = gr.Textbox(label="Added Prompt", value='best quality, extremely detailed')
                    n_prompt = gr.Textbox(label="Optional Negative Prompt",
                                           value='')
            with gr.Column():
                result = gr.Video(label="Generated Video")
        inputs = [
            prompt,
            motion_field_strength_x,
            motion_field_strength_y,
            n_prompt
        ]

        gr.Examples(examples=examples,
                inputs=inputs,
                outputs=result,
                fn=model.process_text2video,
                cache_examples=True,
                run_on_click=False,
        )

        run_button.click(fn=model.process_text2video,
                         inputs=inputs,
                         outputs=result,)
    return demo
