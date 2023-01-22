import streamlit as st
from docarray import Document
SERVER = "grpc://dalle-flow.jina.ai:51005"
NUM_IMAGES = 0
ADD_WATERMARK = True
ADD_INDEX = False

SAMPLE_PHRASES = [
    "Theatrical design inspired by Wes Anderson",
    "A retro dress inspired by Mondrian",
    "Giant inflatable Beyonce",
    "Curving wing of modern hospital building in Californian redwood forest, architecture by Frank Gehry, wide-angle architectural photography from magazine",
]

prompt = st.text_input("What would you like to generate an image of?")

generate_button = st.button("Generate!")

if generate_button:
    doc = Document(text=prompt)
    results = doc.post(SERVER, parameters={"num_images": NUM_IMAGES})

    # for match in results.matches:
        # print(match.content)
        # st.image(match.uri)

    st.image(results.matches[0].uri)