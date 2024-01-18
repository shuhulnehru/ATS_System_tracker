from dotenv import load_dotenv

load_dotenv()

import base64
import io
import os

import google.generativeai as genai
import pdf2image
import streamlit as st
from PIL import Image

# Initialize API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini API
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Function to setup PDF input
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }]
        return pdf_parts
    else:
        return None

# Streamlit App
st.set_page_config(page_title="ATS Resume Checker")
st.header("ATS Tracking System")

input_text = st.text_area("JOB Description: ", key="input")
uploaded_file = st.file_uploader("Upload your Resume (PDF)...", type=['pdf'])

submit1 = st.button("Tell me About the Resume")
submit2 = st.button("How can I improve my skills")
submit3 = st.button("Percentage Match")

# Prompts for Gemini API
input_prompt1 = """
    As an experienced HR professional with a background in Tech, particularly in Data Science, AI, Business Analytics, Data Engineering, and Data Analytics, your task is to conduct a thorough
    review of the provided resume in relation to the specific job description for a role in this field. Please give a detailed professional evaluation of whether the candidate's profile aligns
    well with the job requirements. In your analysis, highlight the strengths and weaknesses of the applicant, focusing on their skills, qualifications, and experiences, and how these
    specifically relate to the expectations and demands of the job description in question.
"""

input_prompt2 = """
    As a career coach specializing in tech roles such as Data Science, AI, Business Analytics, Data Engineering, and Data Analytics, review the provided resume against the job description.
    Identify key skills, qualifications, or experiences missing from the resume that are crucial for the job. Offer specific recommendations for courses, certifications, or projects that
    the candidate can pursue to fill these gaps and strengthen their application for this particular role. Focus on aligning the candidate's profile more closely with the job's requirements
    and enhancing their marketability in the tech industry.
"""

input_prompt3 = """
    You are an experienced ATS Tracking system scanner with a deep understanding of Data Science, AI, Data Engineering, Business Analytics, Data Analytics and deep ATS functionality,
    your task is to evaluate the resume against the provided job description, give me the percentage match of the job description. First the output should come as percentage and then keywords missing and last
    final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
