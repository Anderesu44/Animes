from modules import NON_ALLOWED_CHARACTERS

def format_name_to_dir(name:str)->str:
    for c in NON_ALLOWED_CHARACTERS:
        name = name.replace(c,"")
    return name