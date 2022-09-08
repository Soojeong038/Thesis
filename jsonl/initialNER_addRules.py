#!/usr/bin/env python
# coding: utf-8

# In[1]:


import import_ipynb
from extractText_paragraphs import extract_text


import spacy
from spacy import displacy
from spacy.pipeline import EntityRuler 
import json


# In[2]:


#!python -m spacy download de_core_news_lg
nlp = spacy.load('de_core_news_lg')

#add hand-craft rules : MA ##, Stadt~ Wien

ruler = nlp.add_pipe("entity_ruler", before = 'ner')

patterns = [
                {
                    "label": "ORG", "pattern": [
                        {"TEXT": {"REGEX": r"MA"}},
                        {"TEXT": {"REGEX": r"\w\d+"}}
                    ]
                },
                {
                    "label": "ORG", "pattern": [
                        {"TEXT": {"REGEX": r"Magistratsabteilung"}},
                        {"TEXT": {"REGEX": r"\w\d+"}}
                    ]
                },
                {
                    "label": "ORG", "pattern": [
                        {"TEXT": {"REGEX": r"Stadt*"}},
                        {"TEXT": {"REGEX": r"\w"}},
#                         {"TEXT": {"REGEX": r"Wien"}},
                    ]
                }  
            ]

ruler.add_patterns(patterns)

# #create the doc
# doc = nlp(text)

# #extract entities
# for ent in doc.ents:
#     print (ent.text, ent.label_)


# In[3]:


#JSONL format : {"text": "President Obama", "labels": [ [10, 15, "PERSON"] ]}

def ner(nlp, text):
    '''text = paragraphs list'''
    ner_init = [] #save inital NER
    ner_init.append({"text":'title: {}'.format(title), "label":''})
    
    for i in text:
        doc=nlp(i)
        labels_list=[] #save labels
        
        for word in doc.ents:
            if word.label_ == "ORG": #only organisations
                labels_list.append([word.start_char, word.end_char, word.label_])
        
        if len(labels_list) > 0:
            ner_init.append({"text":i, "label":labels_list})
    
    ner_init.append({"text":'End of document', "label":''})
    
    return ner_init   


def export_jsonl(save_path,file_name,ner_init):
    file = save_path + '\\' + file_name + '.jsonl'
    with open(file, 'w') as fp:
        for i in ner_init:
            json.dump(i, fp)
            fp.write('\n')
    fp.close()
    print('Successfully exported : ', file)


# In[7]:


if __name__ == '__main__':
    
    print('Extracting text from PDF...')
    file = extract_text('02-08-StRH-I-3-18.pdf')
    extracted_paragraphs = file.clensing()
    
    print('Finding named entities...')
    ner_init = ner(nlp, file.title, extracted_paragraphs)
    
    export_jsonl('C:\\Users\\sooje\\jsonl','test1',ner_init)

