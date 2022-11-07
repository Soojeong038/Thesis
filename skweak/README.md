# Weak Supervision with skweak

Reference : https://github.com/NorskRegnesentral/skweak

`skweak` (pronounced /skwi:k/) is a Python-based software toolkit that provides a concrete solution to this problem using weak supervision. skweak is built around a very simple idea: Instead of annotating texts by hand, we define a set of labelling functions to automatically label our documents, and then aggregate their results to obtain a labelled version of our corpus.
<p align="center">
  <img width="460" height="300" src="https://raw.githubusercontent.com/NorskRegnesentral/skweak/main/data/skweak_procedure.png">
</p>

# Steps

<b> 1. Load data </b>

   -  Load unlabelled data - text

   -  Convert to `Doc` object using SpaCy

   - SpaCy pipeline :

   ```
   pipeline = spacy.load("de_core_news_lg", disable=["ner","lemmatizer"])
   ```

   - Add special case to tokenizer - Recognized as a token :

   ```
   "Gesellschaft m.b.H."
   "Gesellschaft mbH"
   "Ges.m.b.H."
   "Gesellschaft mit beschränkter Haftung"
   "Betriebsgesellschaft m.b.H."
   ```


<b> 2. Define labelling function  </b>

   -  0)ORG detected by SpaCy pipelines : ```lf0 = heuristics.FunctionAnnotator("from_spacy_ner", from_spacy_ner)```
   
      - model - "de_core_news_lg",
   
      - except : ['KURZFASSUNG', 'INHALTSVERZEICHNIS','ABKÜRZUNGSVERZEICHNIS', 'Einschau']

   -  1)ma_detector : ```lf1 = heuristics.FunctionAnnotator("ma_detect", ma_detector)```
   
      - token [i] in ["MA","ma","Magistratsabteilung","magistratsabteilung", 'Magistratsabteilungen','magistratsabteilungen']
      
      - token [i+1] == num (r'\d*)
      
   -  2)gov_detector : ```lf2 = gazetteers.GazetteerAnnotator("gov_detect", {"ORG":trie})```
   
      - find tokens in the list of orgs (extracted from document reports titles in https://www.stadtrechnungshof.wien.at/)

   -  3)company_detector : ```lf3 = heuristics.FunctionAnnotator("company_detect", company_detector)```
   
      - find tokens in the list of orgs (extracted from document reports titles in https://www.stadtrechnungshof.wien.at/)
      
      - token [i+1] == num (r'\d*)
# Step 2.
a
