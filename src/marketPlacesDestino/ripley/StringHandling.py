import re
from playwright.sync_api import sync_playwright,expect
import unicodedata
import urllib.parse

def extract_number_of_for(for_id:str)->str:
    pattern = r'autogen(\d+)'
    # Search for the pattern in the phrase
    match = re.search(pattern, for_id)
    
    if match:
        # Extract the number from the match
        number = match.group(1)
        return number
    else:
        return None  # No match found
    
def get_id_ul(for_id:str):
    ul_number=extract_number_of_for(for_id)
    ul_id='select2-results-'+ul_number
    return ul_id

def get_first_enabled_locator(locators_list:list):
    for loc in locators_list:
        try:
            expect(loc).to_be_enabled()
        except:
            print("Locator no habilitado,se pasará al siguiente...")
            continue
        else:
            print("Locator habilitado")
            found_loc=loc
            return found_loc

def keyboard_delete_text(page,word_to_erase:str):
    page.keyboard.down("Shift")
    for i in range(len(word_to_erase)):
        page.keyboard.press("ArrowLeft")
    page.keyboard.up("Shift")
    page.keyboard.press("Backspace")


def extract_words_regex(text:str):
    # Define the string to search
    pattern = r'\b\w+\s*\b'
    # Search for the pattern in the phrase
    match = re.findall(pattern, text)
    # Print the matches
    #print(match)
    return match

def atomize_classification_wo_prepositions(classification_list:list)->list:
    
    if type(classification_list)==str:
        print("Es un str,creando lista de 1 solo elemento")
        classification_list=[classification_list]
    print("Lista original")
    print(classification_list)
    print("Atomizando y quitando preposiciones")
    class_string=" ".join(classification_list)
    class_string=re.sub(r',',"",class_string)
    print(class_string)
    prepositions=['de','y','en','para','con','sin','sobre','tras','durante','mediante','hacia','según','versus','vía']
    splitted_list=class_string.split(" ")
    new_classification_list=[i for i in splitted_list if i not in prepositions]
    print(new_classification_list)
    return new_classification_list

def remove_duplicates_preserve_order(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def remove_accents_and_uppercase(lst):
    new_list = []
    for item in lst:
        # Normalizar y filtrar para quitar tildes
        no_accents = ''.join(
            c for c in unicodedata.normalize('NFD', item)
            if unicodedata.category(c) != 'Mn'
        )
        # Convertir a mayúsculas
        upper_case_item = no_accents.upper()
        new_list.append(upper_case_item)
    return new_list


def format_url_with_encoded_values(category_value:str):
    encoded_category_value = urllib.parse.quote(category_value)
    return encoded_category_value

def test_format_url_with_encoded_values():
    category_value = 'Niño y Bebé'
    print(format_url_with_encoded_values(category_value))
    


def test_remove_accents_and_uppercase():
    example_list = ['café', 'jalApeño', 'niño', 'año']

    # Llamada a la función
    result_list = remove_accents_and_uppercase(example_list)
    print(result_list)



def test_remove_duplicates_preserve_order()->list:
    print("Lista original")
    original_list = ['apple', 'banana', 'apple', 'pear', 'banana', 'orange',"dog","cat",2,3]
    print(original_list)
    cleaned_list = remove_duplicates_preserve_order(original_list)
    print("Lista ordenada")
    print(cleaned_list)

def test_atomize_classification()->list:
    classification_list=['Electrodomésticos', 'y', 'Línea Blanca', 'Cocina y Lavandería', 'Cafeteras y Hervidores', 'Cafetera de goteo Oster BVSTDCDW12B013']
    print(atomize_classification_wo_prepositions(classification_list))



if __name__ == "__main__":
    #extract_words_regex("taza de cafe")
    test_atomize_classification()
    #test_remove_duplicates_preserve_order()
    #test_remove_accents_and_uppercase()
    test_format_url_with_encoded_values()
 





