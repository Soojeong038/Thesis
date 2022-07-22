#!/usr/bin/env python
# coding: utf-8

# In[7]:


import import_ipynb

from initialNer import *
from walkThru import *

import pandas as pd


# In[2]:


def pdfTojsonl(import_path,export_path):
    
    #get file list
    files_list = files(import_path,'pdf')    
    
    #initial set of dataframe
    ind = 0
    cols = ['year','file_name','title']
    info = pd.DataFrame(columns = cols)
    
    for i in files_list:
        year = os.path.basename(i)
        print(year)
        
        for j in files_list[i]:
            file_path = i+'\\'+j

            #extract text
            document = extract_text(file_path)
            document.split_paragraphs()

            #inital ner
            ner_init = ner(document.paragraphs)

            #export as a jsonl file
            export_jsonl(export_path, j, ner_init)

            #store meta data
            info.loc[ind] = [year, j, document.title]
            
            ind += 1   
            
    return info


# # Test

# In[4]:


import_path = "C:\\Users\\sooje\\daten"
export_path = 'C:\\Users\\sooje\\jsonl'
df_info = pdfTojsonl(import_path, export_path)


# In[6]:


df_info[:5]

