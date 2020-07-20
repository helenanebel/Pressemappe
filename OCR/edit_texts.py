import os

for filename in os.listdir('pressemappe_text_files'):
    with open('pressemappe_text_files/' + filename, 'r', encoding='utf-8') as text_file:
        text = text_file.read()
        text = text.replace('-\n', '')
        text = text.replace('\n', ' ')
        text = text.replace('»', '')
        text = text.replace('«', '')
        last_character = ''
        for character in text:
            if character.isupper():
                if last_character != ' ':
                    text = text.replace(last_character + character, last_character + ' ' + character)
            last_character = character
    with open('pressemappe_text_files/' + filename, 'w', encoding='utf-8') as new_file:
        new_file.write(text)
