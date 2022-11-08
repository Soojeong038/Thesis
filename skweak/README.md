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


   -  1)ma_detector : ```lf1 = heuristics.FunctionAnnotator("ma_detect", ma_detector)```
   
      - token [i] in ["MA","ma","Magistratsabteilung","magistratsabteilung", 'Magistratsabteilungen','magistratsabteilungen']
      
      - token [i+1] == num ('\d*')
      
      
   -  2)gov_detector : ```lf2 = gazetteers.GazetteerAnnotator("gov_detect", {"ORG":trie})```
   
      - find tokens in the list of orgs
      
      - ORGs extracted from Tätigkeitsberichte 2013 - 2021 : https://www.stadtrechnungshof.wien.at/berichte/archiv/index.html)
      
      - Total 282



   -  3)company_detector : ```lf3 = heuristics.FunctionAnnotator("company_detect", company_detector)```
   
      - token [i] in ["Gesellschaft m.b.H.","Gesellschaft mbH", "Ges.m.b.H.", "Gesellschaft mit beschränkter Haftung", "Betriebsgesellschaft m.b.H.", "GmbH"]
      
      - if token [i-1] == noun_chunk, then "ORG" = token [i-1] + token [i]
      
        : Example : token [i] = Projekt GmbH, token [i-1] = WIP Wiener Infrastruktur 

          ⇒ "ORG" = "WIP Wiener Infrastruktur Projekt GmbH"
          

   -  4)pre_org_detector : ```lf4 = heuristics.FunctionAnnotator("pre_org_detect", pre_org_detector)```
  
      - token [i] in ["Wiener", "Österreichische", "Österreichischen", "Verein", "Vereiner", "Vereinen"]
      
      - if token [i+1] == noun_chunk, then "ORG" = token [i] + noun_chunk  


# Step3. Aggregate labelling functions

1. Fit HMM aggregation model : https://arxiv.org/pdf/2104.09683.pdf

  - implemented classes (MajorityVoter, NaiveBayes, HMM, etc.) instead
  - Fits the parameters of the aggregator model based on a collection of documents.
  
    The method extracts a dataframe of observations for each document and calls the _fit method
   
```
doc_lf = lf4(lf3(lf2(lf1(docs[0]))))

# create and fit the HMM aggregation model
hmm = skweak.aggregation.HMM("hmm", ["ORG"])
hmm.fit_and_aggregate([doc_lf]*10)

# once fitted, we simply apply the model to aggregate all functions
doc_hmm = hmm(doc_lf)
```

OR

2. Combine Annotators

```
combined = skweak.base.CombinedAnnotator()

combined.add_annotator(lf1)
combined.add_annotator(lf2)
combined.add_annotator(lf3)
combined.add_annotator(lf4)

test_with_combined = list(combined.pipe(docs))
```

⇒ Get the same results


# Result : compare to hand-labelled data

1. The number of tokens

| Methods  | Total Tokens | B-ORG  | I-ORG | O |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| Hand-labelled  | 42,312  | 814  | 1,046  | 40,425  |
| skweak result | 42,312  | 866  | 1,241 | 40,205  |


2. Classification report

- True = Hand labelled

- Predicted = skweak


|   | precision | recall  | f1-score | support |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| O  | 0.99  | 0.99  | 0.99  | 40,425  |
| B-ORG | 0.91  | 0.87  | 0.86 | 841  |
| I-ORG | 0.85  | 0.90  | 0.85 | 1,046  |
| accuracy | -  | -  | 0.99 | 42312  |
| macro avg | 0.88 | 0.93 | 0.90 | 42312  |




# Appendix


1. heuristics.FunctionAnnotator :

  - "heuristics" : Labelling sources based on heuristics / handcrafted rules
  - define fuction (If the function to apply is relatively simple and stateless)


```
#https://github.com/NorskRegnesentral/skweak/blob/main/skweak/heuristics.py
class FunctionAnnotator(SpanAnnotator):
    """Annotation based on a heuristic function that generates (start,end,label)
    given a spacy document"""

    def __init__(self, name: str, 
                 function: Callable[[Doc], Iterable[Tuple[int, int, str]]],
                 to_exclude: Sequence[str] = ()):
        """Create an annotator based on a function generating labelled spans given 
        a Spacy Doc object. Spans that overlap with existing spans from sources 
        listed in 'to_exclude' are ignored. """

        super(FunctionAnnotator, self).__init__(name)
        self.find_spans = function
        self.add_incompatible_sources(to_exclude)
```

2. gazetteers.GazetteerAnnotator :

 - create labelling functions is by compiling lists of entities to detect
 - Trie data structure (used for gazetteers) : made of nodes expressed as (dict, bool) pairs, where the
    dictionary expressed possible edges (tokens) going out from the node, and the boolean
    indicates whether the node is terminal or not.
 - Find longest match and add to entity


```
#https://github.com/NorskRegnesentral/skweak/blob/main/skweak/gazetteers.py
class GazetteerAnnotator(base.SpanAnnotator):
    """Annotation using a gazetteer, i.e. a large list of entity terms. The annotation can
    look at either case-sensitive and case-insensitive occurrences.  The annotator relies 
    on a token-level trie for efficient search. """
```
