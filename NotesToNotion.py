from utils import markdown_builder
from utils import file_manipulation

print()
print('Connect your kindle device to the computer and wait for your storage to be recognized')
print()
input('Press enter when done... ')
print()

# Copy clippings file to current directory
file_manipulation.get_clippings_file()

notes_dict = file_manipulation.load_clippings_file()
json_notes = file_manipulation.raw_clippings_to_json(notes_dict, debug=True)

print('Select the number of the book you want to export the annotations:', '\n')
count = 0
for item in json_notes:
    print(f'[{count}]:', item.get('Titulo'))
    count = count + 1

print()
number = int(input('Number: '))
if number < 0 or number > len(json_notes):
    raise Exception('Number of book is out of range')

markdown_txt = markdown_builder.generateMarkdown(json_notes[number])
file = open('Exported/' + json_notes[number].get('Titulo') + '_markdown.md', 'w')
file.write(markdown_txt)
file.close()

print('Done, Markdown file was exported')