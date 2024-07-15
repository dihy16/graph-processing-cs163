import json

def outputListDictsAsJSON(filename, dict_list):
        with open(filename, 'w', encoding='utf8') as fout:
            for d in dict_list:
                json.dump(d, fout, ensure_ascii=False)
                fout.write('\n')