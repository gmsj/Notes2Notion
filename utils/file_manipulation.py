import os
import json
import codecs

### FUNCTIONS SUPPORTS ONLY LINUX USERS

def get_current_user():
    username = os.popen('echo $USER').read()
    username = username.strip()
    return username

def save_result(filename, content):
    filepath = os.path.join(f'./{filename}.json')
    file = codecs.open(filepath, "w", "utf-8")
    content = json.dumps(content, indent = 4, ensure_ascii=False)
    file.write(content)

def get_clippings_file():
    username = get_current_user()

    status_command = os.popen(f'cd /media/{username}/Kindle').read()
    if status_command:
        raise Exception('Unable to find your kindle mount point')
    
    status_command = os.popen(f'cp "/media/{username}/Kindle/documents/My Clippings.txt" current_clippings.txt').read()
    if status_command:
        raise Exception('Could not copy the file containing your notes')

    return True

def load_clippings_file():
    try:
        file = open('current_clippings.txt', mode='r', encoding='utf-8-sig')
        lines = file.readlines()
        file.close()
    except Exception as error:
        raise Exception(error)

    clean_lines = []
    for i in range(0, len(lines)):
        tmp = lines[i].replace('\n', '').strip()
        tmp = ''.join(char for char in tmp if char.isprintable())
        if tmp != '':
            clean_lines.append(tmp)


    initial_split = []
    index_control = 0
    for i in range(0, len(clean_lines)):
        if clean_lines[i] == '==========':
            initial_split.append(clean_lines[index_control:i])
            index_control = i + 1

    notes_dict = {}
    count = 0
    for item in initial_split:
        if item[0] not in notes_dict:
            count = count + 1
            notes_dict[item[0]] = []
        notes_dict[item[0]].append(item[1:])
    
    return notes_dict

def raw_clippings_to_json(notes_dict, debug = False):
    json_notes = []
    dict_keys = notes_dict.keys()
    for item in dict_keys:
        book = {
            'Titulo': item,
            'Registros': len(notes_dict[item]),
            'Marcadores': [],
            'Destaques': [],
            'Notas': []
        }
        for register in notes_dict[item]:
            try:
                if register[0].startswith('- Sua nota'):
                    tmp = register[0].replace('- Sua nota na', '')
                    tmp = tmp[0: tmp.find('| Ad')]
                    tmp = tmp.strip()
                    book['Notas'].append({
                            'Local': tmp,
                            'Registro': register[1]
                        })
                elif register[0].startswith('- Seu destaque'):
                    tmp = register[0].replace('- Seu destaque na', '')
                    tmp = tmp.replace('- Seu destaque ou', '')
                    tmp = tmp[0: tmp.find('| Ad')]
                    tmp = tmp.strip()
                    if len(register) > 1:
                        book['Destaques'].append({
                            'Local': tmp,
                            'Registro': register[1]
                        })
                    else:
                        book['Destaques'].append({
                            'Local': tmp,
                            'Registro': 'Imagem'
                        })
                elif register[0].startswith('- Seu marcador'):
                    tmp = register[0].replace('- Seu marcador na ', '')
                    tmp = tmp[0: tmp.find(' |')]
                    book['Marcadores'].append(tmp)
                else:
                    print(f'Algum problema ao ler a entrada: [{register[0]}]')
            except Exception as error:
                print(f'Registro com problema: [{register[0]}]')
                raise
        json_notes.append(book)
    
    if debug:
        save_result('database', json_notes)
    
    return json_notes