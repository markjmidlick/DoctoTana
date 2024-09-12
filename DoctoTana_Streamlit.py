import streamlit as st
from io import BytesIO
from PyPDF2 import PdfReader
from docx import Document
import zipfile

def extract_text_from_txt(file):
    return file.read().decode('utf-8')

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text

def convert_to_tana_paste(files):
    tana_paste = "%%tana%%\n\n"
    for file in files:
        file_name = file.name.split('.')[0]
        file_extension = file.name.split('.')[-1].lower()

        if file_extension == 'txt':
            content = extract_text_from_txt(file)
        elif file_extension == 'pdf':
            content = extract_text_from_pdf(file)
        elif file_extension == 'docx':
            content = extract_text_from_docx(file)
        else:
            st.error(f"Unsupported file type: {file_extension}")
            continue
        
        # Format content into Tana Paste format
        tana_paste += f"- {file_name}\n"
        tana_paste += f"  - content::\n"
        for line in content.splitlines():
            tana_paste += f"    - {line}\n"
        tana_paste += "\n"

    return tana_paste

st.title("Document to Tana Paste Converter")
st.write("Upload multiple document files (TXT, PDF, DOCX) to convert them into Tana Paste format.")

uploaded_files = st.file_uploader("Choose files", type=['txt', 'pdf', 'docx'], accept_multiple_files=True)

if uploaded_files:
    if st.button("Convert"):
        tana_paste = convert_to_tana_paste(uploaded_files)

        st.download_button(
            label="Download Tana Paste",
            data=tana_paste,
            file_name="converted_tana_paste.txt",
            mime="text/plain"
        )
