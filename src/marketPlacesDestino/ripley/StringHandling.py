import re
from playwright.sync_api import sync_playwright,expect

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

