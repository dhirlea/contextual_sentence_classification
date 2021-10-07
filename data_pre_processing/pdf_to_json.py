import sys
import subprocess
import pathlib
import os
import json
import unicodedata
import hashlib
import collections
import tqdm
import time

import spacy
from spacy_langdetect import LanguageDetector
import subprocess
import pathlib


def convert_pdf_to_text(input_path):
    """
    Convert pdf to text
    """
    result = subprocess.run(["pdftotext", "-q", input_path, "-"], stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8")


nlp = None

def get_nlp():
    """
    Get the spacy object
    """
    global nlp
    if nlp is None:
        nlp = spacy.load("en_core_web_sm", disable=['parser', 'tagger', 'ner'])
        nlp.add_pipe(nlp.create_pipe('sentencizer'))
        nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)
    return nlp


def process_text_lines(text_lines):
    """
    Takes a list of lines, cleans it up a bit, returns a list of tokenised sentences
    """

    processed_text = []
    text_buffer = []
    nlp = get_nlp()
    for i in range(len(text_lines)+1):
        if i == len(text_lines) or len(text_lines[i].strip()) == 0:
            if len(text_buffer) > 0:
                temp_input = " ".join((" ".join(text_buffer).strip()).split()).strip()

                if temp_input.count(".") > 20 and temp_input.count(".") / len(temp_input) > 0.2:
                    temp_input = " ".join(temp_input.replace(".", " ").strip().split()).strip()
                if len(temp_input) == 0:
                    continue

                pdf_text_doc = nlp(temp_input)
                for sentence in pdf_text_doc.sents:
                    tokenised_sentence = " ".join(sentence.text.strip().split())
                    # tokenised_sentence = " ".join([t.text for t in sentence]).strip()
                    if len(tokenised_sentence) == 0:
                        continue
                    processed_text.append(tokenised_sentence)
                text_buffer = []
        else:
            cleaned_line = ''.join(filter(lambda x: not unicodedata.category(x).startswith('C'), text_lines[i]))
            text_buffer.append(cleaned_line)

    processed_text2 = []
    for s in processed_text:
        if s in ["”", "“", "\""] and len(processed_text2) > 0:
            processed_text2[-1] += " " + s
        else:
            processed_text2.append(s)
    processed_text = processed_text2

    return processed_text


def get_text_language(txt):
    """
    Use spacy to try and detect the language
    """
    nlp = get_nlp()
    doc = nlp(txt)
    return doc._.language["language"]


def calculate_file_md5(file_path):
    """
    Calculate an md5 fingerprint
    """
    with open(file_path, 'rb') as f:
        data = f.read()    
        md5_returned = hashlib.md5(data).hexdigest()
    return md5_returned


def get_pdf_metadata(pdf_file_path):
    extractable_keys = ["Title", "Author", "Subject", "CreationDate"]
    metadata = collections.OrderedDict()
    for key in extractable_keys:
        metadata["pdf_" + key.replace("CreationDate", "creation_time").lower()] = None

    with open(pdf_file_path, 'rb') as fp:
        try:
            parser = PDFParser(fp)
            doc = PDFDocument(parser)
            if len(doc.info) > 0:
                for key in extractable_keys:
                    if key in doc.info[0]:
                        value = doc.info[0][key]
                        try:
                            value = value.decode()
                        except:
                            value = str(value)
                    else:
                        value = None
                    metadata["pdf_" + key.replace("CreationDate", "creation_time").lower()] = value
        except:
            pass

    return metadata


def run_convert_reports(input_pdf_dir, output_json_dir, dataset_dir, pdf_metadata=None, resume=True, verbose=True):
    """ 
    Convert pdfs in the input dir into json files in the output dir, using the same filenames 
    """
    
    pathlib.Path(output_json_dir).mkdir(exist_ok=True)

    # clear save location folder
    for file in os.listdir(output_json_dir):
            os.remove(os.path.join(output_json_dir, file))
    
    dataset_names= [name.split('.')[0]  for name in os.listdir(dataset_dir)]
    pdf_names = [name.split('.')[0]  for name in os.listdir(input_pdf_dir)]
    report_paths = list(pathlib.Path(input_pdf_dir).rglob("*.[pP][dD][fF]"))
    report_paths_names = [path.name.split('.')[0] for path in report_paths]

    if  dataset_names != pdf_names:
        different_names = set(dataset_names) - set(pdf_names)
        if len(different_names)>0:
            print(f'Not all pdfs could be downloaded. {different_names} were not found in the pdf directory. Only converting available pdfs. \n')
        dataset_names = list(set(dataset_names).intersection(set(pdf_names)))
        report_paths_names = list(set(report_paths_names).intersection(set(pdf_names)))
        dataset_names.sort()
        report_paths_names.sort()

    valid_report_paths =[report_path for report_path in report_paths if report_path.name.split('.')[0] in report_paths_names]
    valid_report_paths.sort()
    
    dataset_names = [name +'.json' for name in dataset_names]
    dataset_names.sort()
    used_file_names = set()

    for report_pdf_path, report_name in tqdm.tqdm(zip(valid_report_paths, dataset_names)):
        file_name = os.path.splitext(report_pdf_path.name)[0]

        assert(file_name not in used_file_names)
        used_file_names.add(file_name)

        output_json_path = os.path.join(output_json_dir, file_name + ".json")

        if resume == True and pathlib.Path(output_json_path).exists():
            if verbose is True:
                print("Skipping " + str(report_pdf_path))
            continue
        
        if verbose is True:
            print("Processing " + str(report_pdf_path) + " " + output_json_path)

        pdf_txt = ""
        try:
            pdf_txt = convert_pdf_to_text(report_pdf_path)
        except Exception as e:
            if verbose is True:
                print(e)
                print("Failed pdf conversion. Skipping.")
            continue

        report_raw_txt_lines = [x.strip() for x in pdf_txt.split("\n")]
        processed_txt_lines = process_text_lines(report_raw_txt_lines)
        report_language = get_text_language("\n".join(processed_txt_lines)[:999999])
        md5_fingerprint = calculate_file_md5(report_pdf_path)
        predicted_pdf_metadata = get_pdf_metadata(report_pdf_path)

        output_object = collections.OrderedDict()
        output_object["pdf_local_path"] = str(report_pdf_path.absolute())
        report_pdf_path_relative = os.path.relpath(report_pdf_path, start = input_pdf_dir)
        output_object["pdf_local_path_relative"] = str(report_pdf_path_relative)

        if pdf_metadata is not None:
            assert(str(report_pdf_path.absolute()) in pdf_metadata), str(pdf_metadata) + "\n" + report_pdf_path.absolute()
            assert("pdfurl" in pdf_metadata[str(report_pdf_path)]) # metadata_classifier needs pdfurl
            for key in pdf_metadata[str(report_pdf_path)]:
                output_object[key] = pdf_metadata[str(report_pdf_path)][key]
        else:
            output_object["pdfurl"] = None

        output_object["md5_fingerprint"] = md5_fingerprint
        output_object["time_downloaded"] = str(time.time())
        output_object.update(predicted_pdf_metadata)
        output_object["predicted_language"] = report_language
        with open(dataset_dir +'/'+ report_name, 'r', encoding='utf-8') as public_file:
            report_json = json.load(public_file)
            mapped_sentences = [report_json["sentence_to_initiative_mapping"][str(i)] if str(i) in report_json["sentence_to_initiative_mapping"].keys() else [] for i in range(report_json["num_sentences"])]
            sdg1_list = [report_json["intiatives"][initiative_id[0]][0] if len(initiative_id) > 0 else None for initiative_id in mapped_sentences]
            sdg2_list = [report_json["intiatives"][initiative_id[0]][1] if len(initiative_id) > 0 else None for initiative_id in mapped_sentences]
            output_object["tokenised_sentences"] = [{"text" : x, "initiative_ids" : y, "sdg1" : z, "sdg2" : v} for x,y,z,v in zip(processed_txt_lines, mapped_sentences, sdg1_list, sdg2_list)]
            if (len(output_object["tokenised_sentences"]) == report_json["num_sentences"]) and (output_object["md5_fingerprint"] == report_json["md5_fingerprint"]):
                mapping_flag = True
            else:
                mapping_flag = False

        if mapping_flag:
            print(f'Report {report_pdf_path.name} has been mapped successfully \n')
            with open(output_json_path, 'w') as f:
                f.write(json.dumps(output_object, indent=4, ensure_ascii=False))
        else:
            print(f'Report {report_pdf_path.name} was not parsed correctly and cannot be mapped against oficial data. This will be skipped from the mapping process \n')
            print(f'Tokenized sentences {len(output_object["tokenised_sentences"])} and num_sentences {report_json["num_sentences"]} \n ')
            print(f'PDF md5 hash is {output_object["md5_fingerprint"] } and intended mapping hash is {report_json["md5_fingerprint"]} \n ')



if __name__ == "__main__":
    input_pdf_dir = sys.argv[1]
    output_json_dir = sys.argv[2]
    dataset_dir = sys.argv[3]
    run_convert_reports(input_pdf_dir, output_json_dir, dataset_dir, resume=False, verbose=True)

