from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input,image,prompt):
    model=genai.GenerativeModel("gemini-pro-vision")
    response=model.generate_content([input,image[0],prompt])
    return response.text


#def input_image seutup
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        #Read file into bytes
        bytes_data=uploaded_file.getvalue()

        image_parts=[
            {
                "mime_type":uploaded_file.type, #get mime type of uploaded file
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File uploaded")
    
    # initialize streamlit

st.set_page_config(page_title="Gemini Health App Demo")
st.header("Health App")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file=st.file_uploader("Choose an image of Invoice...",type=["jpg","jpeg","png"])
image=""

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image.",use_column_width=True)

submit=st.button("Tell me the total calories")

input_prompt="""
you are an expert in nutritionist where yo need to see the food items from the image and claculate the 
total calories, also provide the details of every food item iwith calories intake
in below format

1.item 1 - no of calories
2.item 22 - no of calories
"""

# if submit is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is ")
    st.write(response)