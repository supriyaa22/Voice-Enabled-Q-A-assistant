
from PyPDF2 import PdfFileReader
import streamlit as st
def read_pdf(file):
    pdfReader = PdfFileReader(file)
    count = pdfReader.numPages
    all_page_text = ""
    for i in range(count):
        page = pdfReader.getPage(i)
        all_page_text += page.extractText()
    return all_page_text    


def doc_uploader(option):
    document = None
    if option == 'Upload Document':
        uploaded_file = st.sidebar.file_uploader('Choose file',type = ['txt','pdf','docx'])
        if uploaded_file is not None:
            if uploaded_file.type == 'text/plain':
                document = str(uploaded_file.read(),"utf-8")
                st.text_area("document",document,height=60, max_chars=None, key=None)

            elif uploaded_file.type == 'application/pdf':
                try:
                    document = read_pdf(uploaded_file)
                    st.text_area("document",document,height=60, max_chars=None, key=None)
                    
                except:
                    pass

    if option == 'Copy paste document':
        document = st.text_area(label = 'paste your text')

    return document    