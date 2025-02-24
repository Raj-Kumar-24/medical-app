import openai

def generate_report_openai(api_key, prompt):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.6
    )
    return response.choices[0].message.content.strip()

def extract_text_from_pdf(uploaded_file):
    import PyPDF2
    reader = PyPDF2.PdfReader(uploaded_file)
    text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text