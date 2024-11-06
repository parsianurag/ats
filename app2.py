import base64
import streamlit as st
import io
import fitz  # PyMuPDF
import google.generativeai as genai

# Configure Google Generative AI with the API key from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Function to get response from Gemini model
def get_gemini_response(input, pdf_content, prompt):
    # Update the model to gemini-1.5-flash
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Function to set up input from PDF using PyMuPDF (fitz)
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Open the uploaded PDF with PyMuPDF
        doc = fitz.open(uploaded_file)
        first_page = doc.load_page(0)  # Get the first page
        
        # Convert the page to an image (pixmap)
        pix = first_page.get_pixmap()
        
        # Save the image to a byte stream (PNG)
        img_byte_arr = io.BytesIO()
        pix.save(img_byte_arr, format="PNG")  # Save as PNG to avoid quality loss
        img_byte_arr = img_byte_arr.getvalue()

        # Encode the image to base64 for later use
        pdf_parts = [
            {
                "mime_type": "image/png",  # Change MIME type to PNG
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")

input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role. Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. Your task is to evaluate the resume against the provided job description. Provide the percentage match if the resume aligns with the job description, list missing keywords, and offer final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")