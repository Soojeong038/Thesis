# Thesis
Extract initial Named entity recognition results(Only ORG) from PDF files

1.JSONL

	- export result as jsonl files

	- file extension : .jsonl

	- contents : {"text": "Peter Blackburn", "label": [[0, 15, "PERSON"]]}


2.IOB_CoNLL

	- export result as text files
	
	- file extension : .txt
	
	- contents : Peter B-PER / Blackburn I-PER

Subfiles:

	1) walkThru.py

		input: directory path

		output: file names

	2) extractText.py

		input : PDF file

		output : list of paragraphs extracted from input

	3) initialNER.py

		  input : list of paragraphs

		  output : initaial ner result by using spacy ('de_core_news_lg')

	4) pdfToJsonl.py / pdfToCoLL.py

		 input : directory path

		 output : jsonl(txt) files from pdffiles in directory path
