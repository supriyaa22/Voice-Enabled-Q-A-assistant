import streamlit as st
import os

from helper import read_pdf, doc_uploader

st.sidebar.title('NLP tasks')

option = st.sidebar.selectbox(

    'upload',['Upload Document','Copy paste document']
)
document = doc_uploader(option)
task = None
if document is not None:
    if len(document)> 2:
        task  = st.sidebar.selectbox(
            'Task',[
                        'None',
                        'Question Answering', 
                        'Text Summarization'
                    ]
                )
if document is not None:
    if task == 'Question Answering':
        import transformers
        import torch
        from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
        model = AutoModelForQuestionAnswering.from_pretrained(r'static\qna-model', local_files_only  = True)
        tokenizer = AutoTokenizer.from_pretrained(r'static\tokenizer', local_files_only = True)
        nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)
        question = st.text_area(label = 'Write your Question')
        if question is not None:
            QA_input = {
            'question': question,
            'context': document}

        
            
            res = nlp(QA_input)
            st.write(f"Answer: {res['answer']}")
