import os
import json
import re

if __name__ == '__main__':
    file_path = 'MetaData_Json_DataVerse/MetaData_Json'

    datasets = []

    json_files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]

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
                # Keywords
                datasets.append(data_dict)
                break
        except Exception as ex:
            print(f"I dunno an error or something\n{ex}")
            break


    with open('datasets.json', 'w') as o:
        json.dump(datasets, o)
