#!/usr/bin/env python
# coding: utf-8

# In[3]:


import import_ipynb

from initialNer_addRules import *
from walkThru import *

import pandas as pd


# In[2]:


def pdfTojsonl(import_path,export_path):
    
    #get file list
    files_list = files(import_path,'pdf')    
    
    #initial set of dataframe
    ind = 0
    cols = ['year_month','file_name','title']
    info = pd.DataFrame(columns = cols)
    
    for i in files_list:
        year = os.path.basename(i)
        print(year)
        
        for j in files_list[i]:
            file_path = i+'\\'+j

            #extract text
            document = extract_text(file_path)
            extracted_paragraphs = document.clensing()

            #inital ner
            ner_init = ner(nlp, extracted_paragraphs)

            #inital ner
            ner_init = ner(nlp, document.title, document.paragraphs)

            #export as a jsonl file
            export_jsonl(export_path, j, ner_init)

            #store meta data
            info.loc[ind] = [year, j, document.title]
            
            ind += 1   
            
    return info


# # Test

# In[4]:


import_path = "C:\\Users\\sooje\\daten\\2021\\2021_01"
export_path = 'C:\\Users\\sooje\\jsonl'
df_info = pdfTojsonl(import_path, export_path)


# In[5]:


df_info[:5]

