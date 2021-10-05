import requests
import json
import os
import sys
import tqdm

def get_links_from_dataset(location):
    """ Utility function to retrieve pdf hyperlinks from dataset
    """
    links = []
    for filename in os.listdir(location):
        with open(location+filename, 'r', encoding='utf-8') as file:
            report_json = json.load(file)
            links.append(report_json['url'])
    return links

def download_pdfs(links, save_location, data_location):
    """ Utility function to download pdfs from a list of hyperlinks to a defined location. 
    """

    # Remove all files in the save destination before downloading new pdfs
    for file in os.listdir(save_location):
        os.remove(os.path.join(save_location, file))
    for link, filename in tqdm.tqdm(zip(links, os.listdir(data_location))):
        try:
            response = requests.get(link)
            name = filename.split('.')[0] + '.pdf'
            if response.status_code  == 200: 
                with open(save_location + name, 'wb') as f:
                    f.write(response.content)
            else:
                print(f'Report at link {link} could not be downloaded due to error code {response.status_code}. Please try redownloading the dataset and if the issue persists, check and update the link as necessary.\n')
        except requests.exceptions.ConnectionError:
            print(f'{link} is not a valid URL \n')



if __name__ == '__main__':
    dataset_dir = sys.argv[1]
    pdf_dir = sys.argv[2]
    if pdf_dir not in os.listdir():
        os.mkdir(pdf_dir)
    links_list = get_links_from_dataset(os.path.join(os.getcwd(), dataset_dir + '/'))
    download_pdfs(links_list, save_location=os.path.join(os.getcwd(), pdf_dir + '/'), data_location=os.path.join(os.getcwd(), dataset_dir + '/'))
