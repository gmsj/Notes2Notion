import markdownNotion

print()
print('Put the memes file in the same directory as the script!')
input('Press enter when done... ')

try:
    file = open('My Clippings.txt', mode='r', encoding='utf-8-sig')
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

print('Select the number of the book you want to export the annotations:', '\n')
count = 0
for item in json_notes:
    print(f'[{count}]:', item.get('Titulo'))
    count = count + 1

print()
number = int(input('Number: '))
if number < 0 or number > len(json_notes):
    raise Exception('Number of book is out of range')

markdown_txt = markdownNotion.generateMarkdown(json_notes[number])
file = open(json_notes[number].get('Titulo') + '_markdown.md', 'w')
file.write(markdown_txt)
file.close()

print('Done, Markdown file was exported')