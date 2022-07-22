#!/usr/bin/env python
# coding: utf-8

# In[7]:


import os
import glob


# In[4]:


#get leaf directories
def leaf_folders(file_path):
    return [dirpaths for dirpaths, dirnames, filenames in os.walk(file_path) if not dirnames]


#get files
def files(file_path,extension):
    folder_list = leaf_folders(file_path)
    files_list = {}
    
    for i in folder_list:
#         time = os.path.basename(i)
        os.chdir(i)
        files = []
        for file in glob.glob("*.{}".format(extension)):
            files.append(file)
        
        files_list.update({i:files})
        
    return files_list


# In[5]:


if __name__ == '__main__':
    path = "C:\\Users\\sooje\\daten"
    files_list = files(path,'pdf')
    print(files_list)

