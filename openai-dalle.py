# imports
import openai  # OpenAI Python library to make API calls
import requests  # used to download images
import os  # used to access filepaths
from PIL import Image  # used to print and edit images
from IPython.display import display  # used to print images
import streamlit as st
from dt_sms_sdk.message import Message
from dt_sms_sdk.sms_api import Client
import streamlit as st
sidebar_text = f"# Introduction\n\nSend personalized emoji: \n\n\n- [**Github**](https://github.com/masapasa) -  Generate Image using Openai DallE \n- [**Streamlit**](https://streamlit.io/) - frontend\n## Useful links\n\n- )"
st.set_page_config(
    page_title="Send an AI-Generated Image to your friend",
    page_icon="🖱️",
    layout="wide",
)

st.header("🖱️ Send an AI- generated image to your friend")
st.markdown(
    "#### Making your friend happy`*`"
)

st.sidebar.markdown(sidebar_text)
# set API key
openai.api_key = ""
# set a directory to save DALL-E images to
image_dir_name = "images"
image_dir = os.path.join(os.curdir, image_dir_name)

# create the directory if it doesn't yet exist
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

# print the directory to save to
print(f"{image_dir=}")
# create an image

# set the prompt
prompt = "Cute and adorable cartoon, it clown, baby, fantasy, dreamlike, surrealism, super cute, trending on artstation"
st.text_input("What would you like to generate an image of?", value=prompt)
generate_button = st.button("Generate!")
if generate_button:
# call the OpenAI API
    generation_response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024",
        response_format="url",
    )

    # print response
    print(generation_response)
    # save the image
    generated_image_name = "bunny.png"  # any name you like; the filetype should be .png
    generated_image_filepath = os.path.join(image_dir, generated_image_name)
    generated_image_url = generation_response["data"][0]["url"]  # extract image URL from response
    generated_image = requests.get(generated_image_url).content  # download the image

    with open(generated_image_filepath, "wb") as image_file:
        image_file.write(generated_image)  # write the image to the file
        # print the image
    print(generated_image_filepath)
    display(Image.open(generated_image_filepath))
    st.image(generated_image)

from dt_sms_sdk.message import Message
from dt_sms_sdk.sms_api import Client
import streamlit as st

c = Client(api_key="")
body = st.text_area("Enter your message", value="My message to be sent", height=100)
m = Message(_body=body)
button = st.button("Send message")
print(m.number_of_segments()) # will return 1 for this string
if button:
    response = c.send(message=m)
    if response:
        print("Message sent successfully!")