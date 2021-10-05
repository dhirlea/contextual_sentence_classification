Project Overview
========

This repository contains code underlying the "Contextual Sentence Classification:Detecting Sustainability Initiatives in Company Reports" paper written by Dan Hirlea, Dr Marek Rei and Dr Christopher Bryant. The aim of this project is to detect the precise text span of sustainability initiatives in company reports as defined by the Leonardo Centre for Sustainable Business. A company sustainability initiative is defined as a practical activity or set of related activities that a firm performs to tackle a societal issue.

The code provided in this repository is divided in two parts: *data_pre_processing* and *models*. *data_pre_processing* contains 2 python scripts for downloading a set of 45 company reports, converting these into the required json format and assigning initiatives and SDGs to individual sentences. The code under *models* can be run as jupyter notebooks on a local machine after the project dependencies have been installed or using Google Colab (https://colab.research.google.com). We recommend creating separate virtual environments for *data_pre_processing*  and *models* as they require different versions of python to be installed.

Data Pre-processing
------------

The main components of the system are as follows:

1) Download data folders into root project directory from https://drive.google.com/drive/folders/1cknXPeJ_-NLqMGBAj6EXZG5WR3pSHgYN?usp=sharing. These contain information required to assign sentence labels from company PDF reports.
2) Install prerequisites from *data_pre_processing_requirements.txt* in a designated virtual environment and activate the environment. It is important to install the correct version of spacy 2.0.12 in order to parse the PDFs in the correct order. 
3) Download pdfs for each dataset by running "python download_pdf.py <data_dir> <pdf_dir>". For example "python download_pdf.py data_train pdf_train" can be used to download the 25 PDFs in the training set. Similar commands must be run for the development and test sets.
4) Convert PDFs to json format and assign sentence labels by running "python pdf_to_json.py <input_pdf_dir> <output_json_dir> <data_dir>". For example "python pdf_to_json.py pdf_train json_train data_train" converts the training dataset into the required file format. Similar commands must be run for the development and test sets.

Models
------------
1) Create a new virtual environment and install dependencies from *model_training_requirements.txt*.
2) Activate the virtual environment and run the desired notebook to replicate the experiment results. All base models and their corresponding tokenizers are imported from the open-source HuggingFace library (https://huggingface.co/transformers/index.html) directly into the jupyter notebooks.
3) Random seed can be adjusted at the beginning of the notebook to ensure replicability of results.

The chart below illustrates the machine learning pipeline used for all experiments and follows the structure of the notebooks.
![alt text](https://github.com/dhirlea/contextual_sentence_classification/blob/main/Sustainability%20Transformer%20Pipeline.png)


License
------------

The Dataset used in the project is released for non-commercial research and educational purposes under the following licence agreement:

1. By downloading this dataset and licence, this licence agreement is entered into, effective this date, between you, the Licensee, and the Leonardo Centre on Business for Society, the Licensor.
2. Copyright of the entire licensed dataset is held by the Licensor. No ownership or interest in the dataset is transferred to the Licensee.
3. The Licensor hereby grants the Licensee a non-exclusive non-transferable right to use the licensed dataset for non-commercial research and educational purposes.
Non-commercial purposes exclude without limitation any use of the licensed dataset or information derived from the dataset for or as part of a product or service which is sold, offered for sale, licensed, leased or rented.
4. The Licensor grants the Licensee this right to use the licensed dataset ‘as is’. Licensor does not make, and expressly disclaims, any express or implied warranties, representations or endorsements of any kind whatsoever.
5. This Agreement shall be governed by and construed in accordance with the laws of England and the English courts shall have exclusive jurisdiction.