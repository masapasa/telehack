from diffusers import StableDiffusionPipeline
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe = pipe.to("mps")
# Recommended if your computer has < 64 GB of RAM
pipe.enable_attention_slicing()
prompt = "Star wars scene artificial intelligence a yellow golden retriever dog wearing black sith knight cape holding a red lightsaber in it's paw, showing r2d2 and 3po in background, artstation trends, concept art, highly detailed, intricate, sharp focus, digital art, 8 k"
# First-time "warmup" pass (see explanation above)
_ = pipe(prompt, num_inference_steps=1)
# Results match those from the CPU device after the warmup pass.
image = pipe(prompt).images[0]
image.save("star.png")