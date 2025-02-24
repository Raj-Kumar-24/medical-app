import streamlit as st 
import PyPDF2
from fpdf import FPDF
import anthropic 
import openai 
from openai import OpenAI

# User input for OpenAI API Key
if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = ""

st.session_state["openai_api_key"] = st.text_input("Enter your OpenAI API Key", type="password", value=st.session_state["openai_api_key"])

if st.session_state["openai_api_key"]:
    openai_client = OpenAI(api_key=st.session_state["openai_api_key"])

# User input for Anthropic API Key
if "anthropic_api_key" not in st.session_state:
    st.session_state["anthropic_api_key"] = ""

st.session_state["anthropic_api_key"] = st.text_input("Enter your Anthropic API Key", type="password", value=st.session_state["anthropic_api_key"])

if st.session_state["anthropic_api_key"]:
    anthropic_client = anthropic.Anthropic(api_key=st.session_state["anthropic_api_key"])
# Select between OpenAI and Anthropic
llm_choice = st.radio("Select LLM for report generation:", ("OpenAI", "Anthropic", "Both"))

def generate_report_openai(prompt):
    response = openai_client.chat.completion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.6
    )
    return response.choices[0].message.content.strip()

def generate_report_anthropic(prompt): 
    response = anthropic_client.messages.create(            
            model="claude-3-5-sonnet-20241022",            
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500   
        )  
    return response.content[0].text.strip()

def extract_text_from_pdf(uploaded_file): 
    reader = PyPDF2.PdfReader(uploaded_file) 
    text = "".join([page.extract_text() for page in reader.pages if page.extract_text()]) 
    return text

def save_to_pdf(summary, patient_friendly, recommendation, suffix):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="AI-Generated MRI Report", ln=True, align='C')
    pdf.ln(10)
    
    pdf.cell(200, 10, txt="Summary:", ln=True)
    pdf.multi_cell(0, 10, txt=summary)
    pdf.ln(5)
    
    pdf.cell(200, 10, txt="Patient-Friendly Report:", ln=True)
    pdf.multi_cell(0, 10, txt=patient_friendly)
    pdf.ln(5)
    
    pdf.cell(200, 10, txt="Recommendations:", ln=True)
    pdf.multi_cell(0, 10, txt=recommendation)
    pdf.ln(10)
    
    pdf.output(f"AI_Generated_MRI_Report_{suffix}.pdf")
    return f"AI_Generated_MRI_Report_{suffix}.pdf"

st.title("MRI Report AI Assistant")
# File uploader
uploaded_file = st.file_uploader("Upload MRI Report (PDF)", type="pdf")
if uploaded_file: 
    with st.spinner("Extracting text from PDF..."): 
        report_text = extract_text_from_pdf(uploaded_file) 
        st.text_area("Extracted MRI Report:", report_text, height=250)
        st.session_state["report_text"] = report_text

if "report_text" in st.session_state and st.session_state["report_text"].strip():
    if st.button("Generate Reports"):
        st.subheader("AI-Generated Reports")
        
        summary_prompt = f"Please make a summary: {st.session_state['report_text']}"
        patient_friendly_prompt = f"Please make it easy for patients: {st.session_state['report_text']}"
        recommendation_prompt = f"Please make a recommendation for the next step: {st.session_state['report_text']}"
        
        if llm_choice in ["OpenAI", "Both"]:
            with st.spinner("Generating Summary with OpenAI..."):
                openai_summary = generate_report_openai(summary_prompt)
            with st.spinner("Generating Patient-Friendly Report with OpenAI..."):
                openai_patient_friendly = generate_report_openai(patient_friendly_prompt)
            with st.spinner("Generating Recommendations with OpenAI..."):
                openai_recommendation = generate_report_openai(recommendation_prompt)
            openai_pdf_path = save_to_pdf(openai_summary, openai_patient_friendly, openai_recommendation, "OpenAI")

        if llm_choice in ["Anthropic", "Both"]:
            with st.spinner("Generating Summary with Anthropic..."):
                anthropic_summary = generate_report_anthropic(summary_prompt)
            with st.spinner("Generating Patient-Friendly Report with Anthropic..."):
                anthropic_patient_friendly = generate_report_anthropic(patient_friendly_prompt)
            with st.spinner("Generating Recommendations with Anthropic..."):
                anthropic_recommendation = generate_report_anthropic(recommendation_prompt)
            anthropic_pdf_path = save_to_pdf(anthropic_summary, anthropic_patient_friendly, anthropic_recommendation, "Anthropic")

        if llm_choice == "Both":
            with open(openai_pdf_path, "rb") as openai_pdf_file:
                st.download_button(label="Download OpenAI Report", data=openai_pdf_file, file_name="AI_Generated_MRI_Report_OpenAI.pdf", mime="application/pdf")
            with open(anthropic_pdf_path, "rb") as anthropic_pdf_file:
                st.download_button(label="Download Anthropic Report", data=anthropic_pdf_file, file_name="AI_Generated_MRI_Report_Anthropic.pdf", mime="application/pdf")
        elif llm_choice == "OpenAI":
            with open(openai_pdf_path, "rb") as openai_pdf_file:
                st.download_button(label="Download OpenAI Report", data=openai_pdf_file, file_name="AI_Generated_MRI_Report_OpenAI.pdf", mime="application/pdf")
        elif llm_choice == "Anthropic":
            with open(anthropic_pdf_path, "rb") as anthropic_pdf_file:
                st.download_button(label="Download Anthropic Report", data=anthropic_pdf_file, file_name="AI_Generated_MRI_Report_Anthropic.pdf", mime="application/pdf")