from dt_sms_sdk.message import Message
from dt_sms_sdk.sms_api import Client
import streamlit as st

# prompt_text = "Cute and adorable cartoon, it clown, baby, fantasy, dreamlike, surrealism, super cute, trending on artstation"
# st.text_input("What would you like to generate an image of?", value=prompt_text)
c = Client()
body = st.text_area("Enter your message", value="My message to be sent", height=100)
m = Message( _body=body)
button = st.button("Send message")
print(m.number_of_segments()) # will return 1 for this string
if button:
    response = c.send(message=m)
    if response:
        print("Message sent successfully!")