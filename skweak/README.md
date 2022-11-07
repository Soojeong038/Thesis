# Weak Supervision with skweak

Reference : https://github.com/NorskRegnesentral/skweak

`skweak` (pronounced /skwi:k/) is a Python-based software toolkit that provides a concrete solution to this problem using weak supervision. skweak is built around a very simple idea: Instead of annotating texts by hand, we define a set of labelling functions to automatically label our documents, and then aggregate their results to obtain a labelled version of our corpus.
<p align="center">
  <img width="460" height="300" src="https://raw.githubusercontent.com/NorskRegnesentral/skweak/main/data/skweak_procedure.png">
</p>

# Step 1. Load data 

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


# Step 2. Define labelling functions


   -  0)ORG detected by SpaCy pipelines : ```lf0 = heuristics.FunctionAnnotator("from_spacy_ner", from_spacy_ner)```
   
      - model - "de_core_news_lg", only 'ORG' entities
   
      - except : ['KURZFASSUNG', 'INHALTSVERZEICHNIS','ABKÜRZUNGSVERZEICHNIS', 'Einschau']


   -  1)ma_detector : ```lf1 = heuristics.FunctionAnnotator("ma_detect", ma_detector)```
   
      - token [i] in ["MA","ma","Magistratsabteilung","magistratsabteilung", 'Magistratsabteilungen','magistratsabteilungen']
      
      - token [i+1] == num (r'\d*)
      
      
   -  2)gov_detector : ```lf2 = gazetteers.GazetteerAnnotator("gov_detect", {"ORG":trie})```
   
      - find tokens in the list of orgs (extracted from document reports titles in https://www.stadtrechnungshof.wien.at/)


   -  3)company_detector : ```lf3 = heuristics.FunctionAnnotator("company_detect", company_detector)```
   
      - token [i] in ["Gesellschaft m.b.H.","Gesellschaft mbH", "Ges.m.b.H.", "Gesellschaft mit beschränkter Haftung", "Betriebsgesellschaft m.b.H.", "GmbH"]
      
      - if token [i-1] == noun_chunk, then "ORG" = token [i-1] + token [i]
      
        : Example : token [i] = Projekt GmbH, token [i-1] = WIP Wiener Infrastruktur 

          ⇒ "ORG" = "WIP Wiener Infrastruktur Projekt GmbH"
          

   -  4)verein_detector : ```lf4 = heuristics.FunctionAnnotator("verein_detect", verein_detector)```
   
      - 'Verein' in token [i]
      
      - token [i+1].pos_ == 'NOUN' or 'PROPN'
      
      
   -  5)band_detector : ```lf5 = heuristics.FunctionAnnotator("band_detect", band_detector)```
   
      - 'Wiener' in token [i]
      
      - token [i+1] ends with 'band'   
      


# Step3. Aggregate labelling functions


```
doc_lf = lf5(lf4(lf3(lf2(lf1(lf0(docs[0]))))))

# create and fit the HMM aggregation model
hmm = skweak.aggregation.HMM("hmm", ["ORG"])
hmm.fit_and_aggregate([doc_lf]*10)

# once fitted, we simply apply the model to aggregate all functions
doc_hmm = hmm(doc_lf)
```

# Result : compare to hand-labelled data

1. The number of tokens

| Methods  | Total Tokens | B-ORG  | I-ORG | O |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| Hand-labelled  | 42,312  | 814  | 1,046  | 40,425  |
| skweak result | 42,312  | 809  | 1,114 | 40,389  |


2. Classification report

- True = Hand labelled

- Predicted = skweak


|   | precision | recall  | f1-score | support |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| O  | 0.99  | 0.99  | 0.99  | 40,425  |
| B-ORG | 0.91  | 0.87  | 0.89 | 841  |
| I-ORG | 0.85  | 0.90  | 0.87 | 1,046  |
| accuracy | -  | -  | 0.99 | 42312  |
| macro avg | 0.92  | 0.92 | 0.92 | 42312  |
