import os
import json
from utility import reduceByKey

if __name__ == '__main__':
    file_path = 'MetaData_Json_DataVerse/MetaData_Json'

    subjects = []

    json_files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]

    errors = 0
    for f in json_files:
        try:
            with open(f'{file_path}/{f}', encoding='utf8') as json_file:
                data = json.load(json_file)
                data_fields = list(filter(lambda f: f['typeName'] == 'subject', data['data']['latestVersion']['metadataBlocks']['citation']['fields']))
                for i in data_fields:
                    for subject in i['value']:
                        subjects.append(subject)
        except Exception as ex:
            print(f'Error with file: {f}')
            print(ex)
            os.system(f'cp {file_path}/{f} {file_path}/Error')
            errors += 1
            continue
        
    print(f'\n{len(json_files)-errors} files were read correctly. {errors} files were bad')
    
    reducedSubjects = reduceByKey(subjects)
    print(sorted(reducedSubjects, key=lambda x: x[1]))