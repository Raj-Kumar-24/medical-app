def extract_text_from_pdf(uploaded_file): 
    import PyPDF2
    reader = PyPDF2.PdfReader(uploaded_file) 
    text = "".join([page.extract_text() for page in reader.pages if page.extract_text()]) 
    return text

def generate_report(prompt, client): 
    response = client.messages.create(            
            model="claude-3-5-sonnet-20241022",            
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500   
        )  
    return response.content[0].text.strip()