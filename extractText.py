#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import PyPDF2


# In[2]:


class extract_text:
    '''
    path = pdf file path
    '''
    def __init__(self,path):
        self.path = path 
        
    # extract full text
    def extraction(self):
        text = []
        
        with open(self.path, mode='rb') as f:
            reader = PyPDF2.PdfFileReader(f)
            
            #extract title
            info = reader.getDocumentInfo()
            if info.title != None:
                title = re.sub('\s+',' ', info.title)
            else:
                title = ''
                
            #extract text
            for page in reader.pages:
                text.append(page.extractText())
        
        #join texts into a full text
        full_text = (' ').join(text)
        
        #remove header
        full_text = re.sub(r'StRH\s\s*.*Seite*.*von\s\s*\d+','',full_text)
        
        return title, full_text
    
    def split_paragraphs(self):
        self.title, self.full_text = self.extraction()
        
        #splitting
        splitted = re.split(" \n \n",self.full_text)       
        
        return splitted
    
    def clensing(self):
        splitted = self.split_paragraphs() 
        
        self.paragraphs = []
        
        for i in splitted :           
            #remove linebreaking
            temp = i.replace(' -\n','')
            temp = i.replace('-\n','')
            #remove redundant white spaces
            temp = re.sub('\s+',' ',temp)
            if len(temp)>10:
                self.paragraphs.append(temp)
        
        return self.paragraphs
    
#     def main(self):
#         self.extraction()
#         self.split_paragraphs()
#         print(self.title)


# In[4]:


if __name__ == '__main__':
    path = "02-08-StRH-I-3-18.pdf"
    
    file = extract_text(path)
    extracted_paragraphs = file.clensing()
    print(extracted_paragraphs)

