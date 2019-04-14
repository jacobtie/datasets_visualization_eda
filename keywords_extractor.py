import os
import json
import re
from utility import reduceByKey

if __name__ == '__main__':
    keywords = []

    file_path = 'MetaData_Json_DataVerse/MetaData_Json'

    json_files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]
    with open('badwords.txt', 'r') as bw:
        bad_words = bw.read().split('\n')

    # print (bad_words)

    errors = 0
    for f in json_files:
        try:
            with open(file_path+'/'+f, encoding='utf8') as json_file:
                data = json.load(json_file)
                data_fields = list(filter(lambda f: f['typeName'] == 'keyword', data['data']['latestVersion']['metadataBlocks']['citation']['fields']))
                for r in data_fields:
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
        except Exception as ex:
            print(f'Error with file: {f}')
            print(ex)
            os.system(f'cp {file_path}/{f} {file_path}/Error')
            errors += 1
            continue
    print(f'\n{len(json_files)-errors} files were read correctly. {errors} files were bad')
    
    reducedKeywords = reduceByKey(keywords)
    print(sorted(reducedKeywords, key=lambda x: x[1]))
