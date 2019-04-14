import os
import json
import re

if __name__ == '__main__':
    file_path = 'MetaData_Json_DataVerse/MetaData_Json'

    datasets = []

    json_files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]

    with open('badwords.txt', 'r') as bw:
        bad_words = bw.read().split('\n')

    errors = 0

    for f in json_files:
        try:
            with (open('template.json', 'r')) as template:
                data_dict = json.load(template)
            with open(file_path+'/'+f, encoding='utf8') as json_file:
                data = json.load(json_file)
                data_fields = data['data']['latestVersion']['metadataBlocks']['citation']['fields']
                data_dict['title'] = list(filter(lambda f: f['typeName'] == 'title', data_fields))[0]['value']
                data_dict['url'] = data['data']['persistentUrl']
                data_dict['publisher'] = data['data']['publisher']
                data_dict['lastUpdateTime'] = data['data']['latestVersion']['lastUpdateTime']
                data_dict['subject'] = list(filter(lambda f: f['typeName'] == 'subject', data_fields))[0]['value']
                data_dict['description'] = list(filter(lambda f: f['typeName'] == 'dsDescription', data_fields))[0]['value'][0]['dsDescriptionValue']['value']
                # Filesize
                fileSize = 0
                for data_file in data['data']['latestVersion']['files']:
                    fileSize += data_file['dataFile']['filesize']
                data_dict['filesize'] = fileSize
                # Keywords
                keywords = []

                for r in list(filter(lambda f: f['typeName'] == 'keyword', data_fields)):
                    for k in r['value']:
                        try:
                            val = k['keywordValue']['value']
                            if val not in bad_words and re.match('[0-9]+', val) is None:
                                keywords.append(val)
                        except:
                            pass
                        try:
                            val = k['keywordVocabulary']['value']
                            if val not in bad_words and re.match('[0-9]+', val) is None:
                                keywords.append(val)
                        except:
                            pass
                if keywords == []: continue
                data_dict['keywords'] = keywords
                datasets.append(data_dict)
        except Exception as ex:
            print(f'Error with file: {f}')
            print(ex)
            os.system(f'cp {file_path}/{f} {file_path}/Error')
            errors += 1
            continue

    with open('datasets.json', 'w') as o:
        json.dump(datasets, o)

    print('datasets.json has been dumped')