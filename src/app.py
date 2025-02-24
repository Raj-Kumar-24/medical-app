import streamlit as st 
import PyPDF2
from fpdf import FPDF
import anthropic 
import openai 
from openai import OpenAI
from googletrans import Translator

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
    response = openai_client.chat.completions.create(
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

def save_to_pdf(summary, patient_friendly, recommendation, suffix, language="en"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt=f"AI-Generated MRI Report ({suffix})", ln=True, align='C')
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
    
    file_name = f"AI_Generated_MRI_Report_{suffix}_{language}.pdf"
    pdf.output(file_name)
    return file_name

def translate_text(text, dest_language):
    translator = Translator()
    translated = translator.translate(text, dest=dest_language)
    return translated.text

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
                st.session_state["openai_summary"] = generate_report_openai(summary_prompt)
            with st.spinner("Generating Patient-Friendly Report with OpenAI..."):
                st.session_state["openai_patient_friendly"] = generate_report_openai(patient_friendly_prompt)
            with st.spinner("Generating Recommendations with OpenAI..."):
                st.session_state["openai_recommendation"] = generate_report_openai(recommendation_prompt)
            st.session_state["openai_pdf_path"] = save_to_pdf(st.session_state["openai_summary"], st.session_state["openai_patient_friendly"], st.session_state["openai_recommendation"], "OpenAI")

        if llm_choice in ["Anthropic", "Both"]:
            with st.spinner("Generating Summary with Anthropic..."):
                st.session_state["anthropic_summary"] = generate_report_anthropic(summary_prompt)
            with st.spinner("Generating Patient-Friendly Report with Anthropic..."):
                st.session_state["anthropic_patient_friendly"] = generate_report_anthropic(patient_friendly_prompt)
            with st.spinner("Generating Recommendations with Anthropic..."):
                st.session_state["anthropic_recommendation"] = generate_report_anthropic(recommendation_prompt)
            st.session_state["anthropic_pdf_path"] = save_to_pdf(st.session_state["anthropic_summary"], st.session_state["anthropic_patient_friendly"], st.session_state["anthropic_recommendation"], "Anthropic")

if "openai_summary" in st.session_state or "anthropic_summary" in st.session_state:
    st.subheader("AI-Generated Reports")
    if "openai_summary" in st.session_state:
        st.write("### OpenAI Summary:")
        st.write(st.session_state["openai_summary"])
        st.write("### OpenAI Patient-Friendly Report:")
        st.write(st.session_state["openai_patient_friendly"])
        st.write("### OpenAI Recommendations:")
        st.write(st.session_state["openai_recommendation"])
    if "anthropic_summary" in st.session_state:
        st.write("### Anthropic Summary:")
        st.write(st.session_state["anthropic_summary"])
        st.write("### Anthropic Patient-Friendly Report:")
        st.write(st.session_state["anthropic_patient_friendly"])
        st.write("### Anthropic Recommendations:")
        st.write(st.session_state["anthropic_recommendation"])

    # Language selection for translation
    language_choice = st.radio("Select language for the report:", ("English", "Spanish"))
    dest_language = "es" if language_choice == "Spanish" else "en"

    if language_choice == "Spanish":
        if "openai_summary" in st.session_state:
            st.session_state["openai_summary_translated"] = translate_text(st.session_state["openai_summary"], dest_language)
            st.session_state["openai_patient_friendly_translated"] = translate_text(st.session_state["openai_patient_friendly"], dest_language)
            st.session_state["openai_recommendation_translated"] = translate_text(st.session_state["openai_recommendation"], dest_language)
            st.session_state["openai_pdf_path_translated"] = save_to_pdf(st.session_state["openai_summary_translated"], st.session_state["openai_patient_friendly_translated"], st.session_state["openai_recommendation_translated"], "OpenAI", dest_language)
        if "anthropic_summary" in st.session_state:
            st.session_state["anthropic_summary_translated"] = translate_text(st.session_state["anthropic_summary"], dest_language)
            st.session_state["anthropic_patient_friendly_translated"] = translate_text(st.session_state["anthropic_patient_friendly"], dest_language)
            st.session_state["anthropic_recommendation_translated"] = translate_text(st.session_state["anthropic_recommendation"], dest_language)
            st.session_state["anthropic_pdf_path_translated"] = save_to_pdf(st.session_state["anthropic_summary_translated"], st.session_state["anthropic_patient_friendly_translated"], st.session_state["anthropic_recommendation_translated"], "Anthropic", dest_language)
    else:
        st.session_state["openai_pdf_path_translated"] = st.session_state["openai_pdf_path"]
        st.session_state["anthropic_pdf_path_translated"] = st.session_state["anthropic_pdf_path"]

    if llm_choice == "Both":
        with open(st.session_state["openai_pdf_path_translated"], "rb") as openai_pdf_file:
            st.download_button(label=f"Download OpenAI Report ({language_choice})", data=openai_pdf_file, file_name=f"AI_Generated_MRI_Report_OpenAI_{dest_language}.pdf", mime="application/pdf")
        with open(st.session_state["anthropic_pdf_path_translated"], "rb") as anthropic_pdf_file:
            st.download_button(label=f"Download Anthropic Report ({language_choice})", data=anthropic_pdf_file, file_name=f"AI_Generated_MRI_Report_Anthropic_{dest_language}.pdf", mime="application/pdf")
    elif llm_choice == "OpenAI":
        with open(st.session_state["openai_pdf_path_translated"], "rb") as openai_pdf_file:
            st.download_button(label=f"Download OpenAI Report ({language_choice})", data=openai_pdf_file, file_name=f"AI_Generated_MRI_Report_OpenAI_{dest_language}.pdf", mime="application/pdf")
    elif llm_choice == "Anthropic":
        with open(st.session_state["anthropic_pdf_path_translated"], "rb") as anthropic_pdf_file:
            st.download_button(label=f"Download Anthropic Report ({language_choice})", data=anthropic_pdf_file, file_name=f"AI_Generated_MRI_Report_Anthropic_{dest_language}.pdf", mime="application/pdf")
