#!/usr/bin/env python
# coding: utf-8

# In[1]:


import import_ipynb
from extractText import extract_text

import spacy
from spacy import displacy
import json


# In[2]:


#!python -m spacy download de_core_news_lg
nlp = spacy.load('de_core_news_lg')


# In[3]:


#JSONL format : {"text": "President Obama", "labels": [ [10, 15, "PERSON"] ]}

def ner(text):
    '''text = paragraphs list'''
    ner_init = [] #save inital NER
   
    for i in text:
        doc=nlp(i)
        labels_list=[] #save labels
        
        for word in doc.ents:
            if word.label_ == "ORG": #only organisations
                labels_list.append([word.start_char, word.end_char, word.label_])
        
        if len(labels_list) > 0:
            ner_init.append({"text":i, "label":labels_list})
    
    return ner_init   


# def export_jsonl(file_name,ner_init):

#     with open('{}.jsonl'.format(file_name), 'w') as fp:
#         for i in ner_init:
#             json.dump(i, fp)
#             fp.write('\n')
#     fp.close()


def export_jsonl(save_path,file_name,ner_init):
    file = save_path + '\\' + file_name + '.jsonl'
    with open(file, 'w') as fp:
        for i in ner_init:
            json.dump(i, fp)
            fp.write('\n')
    fp.close()


# In[4]:


if __name__ == '__main__':
    file = extract_text('02-08-StRH-I-3-18.pdf')
    file.split_paragraphs()
    text = file.paragraphs
    ner_init = ner(text)
    export_jsonl('C:\\Users\\sooje\\jsonl','test1',ner_init)

