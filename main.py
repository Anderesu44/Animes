from os import getcwd, listdir, mkdir, path, system
from sys import argv
from typing import NoReturn

from modules.A44M import ConfigManager


ID_ERROR = "\nthe id given not is valid\n"
DIR_ERROR = "path specified not found"
NAME_ERROR = "not's valid name\na valid name cannot contain ['[', '<', '\\', '*', '\"', '|', ':', '?', '/', '>', ']',]"
COMMAND_UNKNOWN = "\ncommand unknown\ntry -h or --help\n"
ACCESS_DENIED = "Access denied"
VERSION = "1.0.2"
CONFIG_DIR = "./db"#!"C:\\ProgramData\\Anderesu44\\animes"
INIT_CONFIG = { "DEFAULT_RESEPTION_DIR": "~/Videos/Animes/0000", "DEFAULT_ANIMES_DIR": "~/Videos/Animes", "RESEPTION_DIR": "~/Videos/Animes/0000;", "ANIMES_DIR": "~/Videos/Animes","RESEPTION_OLD_DIR": "~/Videos/Animes/0000", "ANIMES_OLD_DIR": "~/Videos/Animes"}

CFG = ConfigManager(CONFIG_DIR,init=INIT_CONFIG)
ANIMES_DIR = path.realpath(path.expanduser(CFG["ANIMES_DIR"]))

def main(*args: str,**kwargs):
    HELP="""
animes <command> [option]
    -n or --new     => make new animme folder
    -s or --sort    => sort the animes in reseption folder
    --config        => changes the program configuration

    -v or --view    => show all animes folders
    -h or --help    => show help
    --version       => show vesion

special commands
    --wait          => the program waits before ending
"""
    if len(args) == 1:
        exit(HELP)
    match argv[1]:
        case "-n"|"--new":
            _new(*argv[1:])
        case "-s"|"--sort":
            # _sort(argv[1:])
            pass
        case "--config":
            # _config(argv[1:])
            pass
        case "-v"|"--view":
            # _view(argv[1:])
            pass
        case "-h"|"--help":
            print(HELP)
            if "--wait" in argv:
                input()
            exit()
        case "--version":
            print(f"animes manager version:{VERSION}")
            if "--wait" in argv:
                input()
            exit()
        case _:
            exit(COMMAND_UNKNOWN)


def _new(*args)->NoReturn:
    HELP = f"""
animes {args[0]} <id:int> <name:str>

all the arguments after the 3rd will be taken as a name
"""
    if len(args) == 1 or args[1] == "-h":
        exit(HELP)
    try:
        num = int(args[1])
    except ValueError:
        exit(ID_ERROR)
    if len(str(num)) != 4:
        num = f"{int(num):04}"
        if len(str(num)) != 4:
            exit(ID_ERROR)
    nam = ""
    for a in args[2:]:
            nam += a+" " 
    nam = nam.strip(" ")
    
    if not _valid_name(nam):
        exit(NAME_ERROR)
    
    folder_path =path.join(ANIMES_DIR,f"{num}_{nam}")
    try:
        mkdir(folder_path)
    except FileExistsError:
        pass
    init_file_path = path.join(folder_path,"desktop.ini")
    if CFG["ICONS_FOLDER"]:
        icon_path = path.join(path.realpath(path.expanduser(CFG["ICONS_FOLDER"])),f"{num}.ico")
    else:
        icon_path = f"{num}.ico"
    with open(init_file_path,"w") as f:
        f.write(f'[.ShellClassInfo]\nIconResource="{icon_path}",0')
        system(f'attrib +h "{init_file_path}"')
        system(f'attrib +r "{folder_path}"')
    #?un scrip que encuentre y convierta las imagenes .png y .jpeg en .ico
    #~download = "~/Downloads"
    #~for file in listdir(download):
    #~    file = file.strip("/")[0]
    #~    if file == "":...  
    exit("All right")

def _sort(*args)->NoReturn:
    pass

def _valid_name(name:str)->bool:
    if "\\" in name or "/" in name or ":" in name or "*" in name or "?" in name or '"' in name or "<" in name or ">" in name or "|" in name:
        return False
    else:
        return True
def _back_dir()->str:
    _dir = getcwd()
    temp = _dir.split("\\")
    temp.pop()
    _dir = ""
    for folder in temp:
        _dir += folder + "\\"
    return _dir
def _move(files:dict[str,str])->None:
    iter = -1
    for cap in files:
        iter += 1
        new_path = files[cap]
        system(f'move "{cap}" "{new_path}"')
        if iter == 0:
            print(f"relocated files:")
        print(f"\t{cap} to {new_path}\n")
    print("All Sorted")
if __name__ == '__main__':
    main(*argv)