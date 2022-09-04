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
        
#         self.paragraphs = []
        self.paragraphs = []
        cleansed =[]
        for i in splitted :           
            #remove linebreaking
            temp = i.replace(' -\n','')
            temp = i.replace('-\n','')
            #remove redundant white spaces
            temp = re.sub('\s+',' ',temp)
            if len(temp)>10:
                cleansed.append(temp)
        
        
        #merge paragraghs of Empfehlung and related Stellungnahme
        count = 0
        new = ''
        
        while count < len(cleansed):

            if count < (len(cleansed)-1):
                if "Empfehlung Nr." in cleansed[count] :
                    if cleansed[count+1].startswith("Stellungnahme"):
                        new = cleansed[count]+'\n'+cleansed[count+1]
                        self.paragraphs.append(new)
                        count += 2
                    else:
                        self.paragraphs.append(cleansed[count])
                        count += 1                       
                else:
                    self.paragraphs.append(cleansed[count])
                    count += 1
            else:
                self.paragraphs.append(cleansed[count])
                count += 1

        return self.paragraphs
    
#     def main(self):
#         self.extraction()
#         self.split_paragraphs()
#         print(self.title)


# In[3]:


if __name__ == '__main__':
    path = "daten\\2021\\2021_01\\StRH-I-20-18-MA_51.docx.rtf.pdf"
    
    file = extract_text(path)
    extracted_paragraphs = file.clensing()
    print(extracted_paragraphs)
