Project Overview
========

This repository contains code underlying the ["Contextual Sentence Classification:Detecting Sustainability Initiatives in Company Reports"](https://arxiv.org/abs/2110.03727) paper written by Dan Hirlea, Dr Marek Rei and Dr Christopher Bryant. The aim of this project is to detect the precise text span of sustainability initiatives in company reports as defined by the Leonardo Centre for Sustainable Business. A company sustainability initiative is defined as a practical activity or set of related activities that a firm performs to tackle a societal issue.

The code provided in this repository is divided in two parts: *data_pre_processing* and *models*. *data_pre_processing* contains 2 python scripts for downloading a set of 45 company reports, converting these into the required json format and assigning initiatives and SDGs to individual sentences. The code under *models* can be run as jupyter notebooks on a local machine after the project dependencies have been installed or using Google Colab (https://colab.research.google.com). We recommend creating separate virtual environments for *data_pre_processing*  and *models* as they require different versions of python to be installed.

Data Pre-processing (Requires Linux Distribution such as Ubuntu 20.04 or WSL2 with Linux distribution installed)
------------

The main components of the system are as follows:

1) Download data folders into root project directory from https://drive.google.com/drive/folders/1cknXPeJ_-NLqMGBAj6EXZG5WR3pSHgYN?usp=sharing. These contain information required to assign sentence labels from company PDF reports.
2) Install poppler-utils library via command line. Use poppler-utils 0.62.0 on Ubuntu 18.04 or poppler-utils 0.86.1 on Ubuntu 20.04.

    ```
    sudo apt-get install poppler-utils 
    ```

3) Install prerequisites from *data_pre_processing_requirements.txt* in a designated virtual environment and activate the environment. It is important to install the correct version of spacy 2.0.12 in order to parse the PDFs in the correct order.
    ```
    conda  create --name pdf_processing python=3.7 
    conda activate pdf_processing
    conda install --file data_pre_processing/data_pre_processing_requirements.txt
    pip install spacy-langdetect==0.1.2
    ```
4) Download the spacy English language package.
    ```
    python -m spacy download en_core_web_sm
    ```
5) Download pdfs for each dataset by running "python download_pdf.py <data_dir> <pdf_dir>". If certain PDF links are not accessible from python, the user can manually click on them and download the PDFs into the corresponding folder manually. 
    ```
    python data_pre_processing/download_pdf.py data_train pdf_train
    python data_pre_processing/download_pdf.py data_develop pdf_develop
    python data_pre_processing/download_pdf.py data_test pdf_test
    ```
6) Convert PDFs to json format and assign sentence labels. 
    ```
    python data_pre_processing/pdf_to_json.py pdf_train json_train data_train
    python data_pre_processing/pdf_to_json.py pdf_develop json_develop data_develop
    python data_pre_processing/pdf_to_json.py pdf_test json_test data_test
    ```
Models (Can be used with Colab or on any OS)
------------
If used with Google Colab, notebooks can be run directly as they are. The only requirement is to have the *json_train*, *json_develop* and *json_test* folders in the user's Google Drive.

If run on a local machine, please use the following steps:

1) Create a new virtual environment and install dependencies from *model_training_requirements.txt*. 
    ```
    conda  create --name sustainability python=3.8
    conda activate sustainability
    conda install pytorch==1.7.0 torchvision==0.8.0 torchaudio==0.7.0 cudatoolkit=11.0 -c pytorch
    pip install transformers==4.0.0
    pip install pytorch-crf==0.7.2
    pip install datasets==1.6.0
    conda install --file models/model_training_requirements.txt
    ```
2) Make sure that *json_train*, *json_develop* and *json_test* are located in the root project directory alongside the notebooks. 
3) Activate the virtual environment and run the desired notebook to replicate the experiment results. All base models and their corresponding tokenizers are imported from the open-source HuggingFace library (https://huggingface.co/transformers/index.html) directly into the jupyter notebooks.
    ```
    conda activate sustainability
    jupyter lab
    ```
4) Random seed can be adjusted at the beginning of the notebook to ensure replicability of results.

The chart below illustrates the machine learning pipeline used for all experiments and follows the structure of the notebooks.
![alt text](https://github.com/dhirlea/contextual_sentence_classification/blob/main/system_pipeline.png)



License
------------

The Dataset used in the project is released for non-commercial research and educational purposes under the following licence agreement:

1. By downloading this dataset and licence, this licence agreement is entered into, effective this date, between you, the Licensee, and the Leonardo Centre on Business for Society, the Licensor.
2. Copyright of the entire licensed dataset is held by the Licensor. No ownership or interest in the dataset is transferred to the Licensee.
3. The Licensor hereby grants the Licensee a non-exclusive non-transferable right to use the licensed dataset for non-commercial research and educational purposes.
Non-commercial purposes exclude without limitation any use of the licensed dataset or information derived from the dataset for or as part of a product or service which is sold, offered for sale, licensed, leased or rented.
4. The Licensor grants the Licensee this right to use the licensed dataset ‘as is’. Licensor does not make, and expressly disclaims, any express or implied warranties, representations or endorsements of any kind whatsoever.
5. This Agreement shall be governed by and construed in accordance with the laws of England and the English courts shall have exclusive jurisdiction.