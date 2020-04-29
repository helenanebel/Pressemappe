import tesseract_pressemappe
import os

tesseract_pressemappe.get_text_files()

file_list = os.listdir('pressemappe_text_files')

def get_entities_from_text(file_list):
    entities_list = []
    ...

    return entities_list

if __name__ == '__main__':
    get_entities_from_text(file_list)