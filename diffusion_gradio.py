import gradio as gr

gradio_ui = gr.Interface(
    title="Stable Diffusion Demo",
    description="Enter a description of an image you'd like to generate!",
    inputs=[
        gr.Textbox(lines=2, label="Paste some text here"),
        
    ],
    outputs=["image"],
    examples=[["a photograph of an astronaut riding a horse"]])

gradio_ui.launch(debug=True)
