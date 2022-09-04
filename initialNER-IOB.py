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


# In[4]:


def ner(nlp, text):
    '''text = paragraphs list'''
    labels_list=[] #save labels
   
    for i in text:
        doc=nlp(i)
      
        for token in doc:
            if str(token) != " ": #remove redundent white spaces
                if token.ent_type_ == 'ORG': #save only "ORG" entities
                    label = str(token)+"\t"+"{}-{}".format(token.ent_iob_,token.ent_type_)

                    labels_list.append(label)
                else:
                    label = str(token)+"\t"+"O"
                    labels_list.append(label)
        
        labels_list.append("\n") #mark the end of paragraph


    return labels_list   


def export_txt(save_path,file_name,labels_list):
    file = save_path + '\\' + file_name + '.txt'
    with open(file, 'w') as f:
        for line in labels_list:
            if line != "\n":
                f.write(f"{line}\n")
            else:
                f.write("\n")


# In[5]:


if __name__ == '__main__':
    path = "daten\\2021\\2021_01\\StRH-I-20-18-MA_51.docx.rtf.pdf"

    file = extract_text(path)
    extracted_paragraphs = file.clensing()
    data = ner(nlp, extracted_paragraphs)
    print(data)
    export_txt('./','new2',data)

