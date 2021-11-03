import gdown

url = 'https://drive.google.com/drive/folders/1YikY903h-jZsuoXyPTLKprK6KmJrhJIS'
dataDevelop = 'data_develop'
gdown.download_folder(url,output=dataDevelop)

url = 'https://drive.google.com/drive/folders/107IYRfgc_IBWHsdLhUGwdYndUUUTpAIc'
dataTest = 'data_test'
gdown.download_folder(url,output=dataTest)

url = 'https://drive.google.com/drive/folders/1mswXCYM9F7k1FjAQMjjidWXi6b5hOv-u'
dataTrain = 'data_train'
gdown.download_folder(url,output=dataTrain)