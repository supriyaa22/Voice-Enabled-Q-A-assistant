import os
import transformers
import torch
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
from text_to_speech import text_to_speech

def q_and_a(context,question):
    model = AutoModelForQuestionAnswering.from_pretrained(r'static\qna-model', local_files_only  = True)
    tokenizer = AutoTokenizer.from_pretrained(r'static\tokenizer', local_files_only = True)
    nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)
    if question.split(" ")[2] not in context:
        print(question.split(" ")[2]
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        )
        return "no match found"
    if question is not None:
        QA_input = {
        'question': question,
        'context': context}
        res = nlp(QA_input)
        # text_to_speech(res['answer'])
        return res['answer']

# print(q_and_a(context="My name is Kashish",question="What is my name?"))