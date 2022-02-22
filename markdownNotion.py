### TODO: Pesquisar como posso adicionar/herdar métodos da str ###

def generateMarkdown(json_object):
    page = []
    page.append(title('Resumo e Anotações', 2))

    page.append(title('Marcadores', 3))
    for item in json_object.get('Marcadores'):
        page.append(quote(item))
    
    page.append(title('Destaques', 3))
    for item in json_object.get('Destaques'):
        page.append(quote(item.get('Registro')))

    page.append(title('Notas', 3))
    for item in json_object.get('Notas'):
        page.append(quote(item.get('Registro')))
    
    return ''.join(page)

def title(txt, size = 1):
    if size < 1 or size > 3:
        raise Exception('Size of title is not valid')
    return '#' * size + ' ' + txt + '\n\n'

def simpleTxt(txt):
    return txt + '\n\n'

def bulletList(items):
    if not isinstance(items, list):
        raise Exception('Bulleted list must be a list type')
    
    txt_list = []
    for item in items:
        txt_list.append('- ' + item)
    return '\n'.join(txt_list) + '\n'

def numberList(items):
    if not isinstance(items, list):
        raise Exception('Numbered list must be a list type')
    
    txt_list = []
    count = 1
    for item in items:
        txt_list.append(str(count) + '. ' + item)
        count = count + 1
    return '\n'.join(txt_list) + '\n'

def quote(txt):
    return '> ' + txt + '\n' + '> ' + '\n\n'

def callout(txt):
    txt_list = []
    txt_list.append('<aside>')
    txt_list.append(txt + '\n')
    txt_list.append('</aside>')
    return '\n'.join(txt_list) + '\n'

def divider():
    return '---'
