from os import getcwd, listdir, mkdir, path, system
from shutil import move
from sys import argv
from typing import NoReturn

from modules import ID_ERR as ID_ERROR
from modules.A44M import ConfigManager, format_text
from modules.Entities import Animes, Reception



DIR_ERROR = "path specified not found"
NAME_ERROR = "not's valid name\na valid name cannot contain ['[', '<', '\\', '*', '\"', '|', ':', '?', '/', '>', ']',]"
SINTAX_ERROR ="the command syntax's not correct try --help"
COMMAND_UNKNOWN = "\ncommand unknown\ntry -h or --help\n"
ACCESS_DENIED = "Access denied"
VERSION = "1.0.2"
CONFIG_DIR = "./db"#!"C:\\ProgramData\\Anderesu44\\animes"
INIT_CONFIG = {"DEFAULT_ANIMES_DIR": "~/Videos/Animes","DEFAULT_RECEPTION_DIR": "~/Videos/Animes/0000","ANIMES_DIR": "~/Videos/Animes","RECEPTION_DIR": "~/Videos/Animes/0000","ANIMES_OLD_DIR": "~/Videos/Animes","RECEPTION_OLD_DIR": "~/Videos/Animes/0000","ICONS_FOLDER":None}
CFG = ConfigManager(CONFIG_DIR,init=INIT_CONFIG)
ANIMES_DIR = path.realpath(path.expanduser(CFG["ANIMES_DIR"]))
RECEPTION_DIR = path.realpath(path.expanduser(CFG["RECEPTION_DIR"]))

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
            _sort(*argv[1:])
        case "--config":
            # _config(argv[1:])
            pass
        case "-v"|"--view":
            _view(argv[1:])
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
    HELP = f"""
animes <{args[0]}>
animes <{args[0]}> [path]
animes <{args[0]}> [command]
commands
    -h        => show help
    in        => sort the animes in the specified path instead of the {format_text("...",*(ANIMES_DIR.split("\\")[-3:]),sep="\\")}
special commands
    --wait    => the program waits before ending
    --default => use the path saved default
"""
    wait = False
    reception_path = ""
    animes_path = ANIMES_DIR
    if "--wait" in args:
        wait = True
    if len(args) == 1:
        reception_path = RECEPTION_DIR
    else:
        if args[1] == "-h":
            exit(HELP)
        if args[1] == "--default":
            reception_path = RECEPTION_DIR
        elif "-" in args[1]:
            exit(COMMAND_UNKNOWN)
        else:
            if not path.isdir(path.realpath(path.expanduser(args[1]))):
                if not path.exists(args[1]):
                    exit(f'"{args[1]}" Not Found or not a folder')
            else:
                reception_path = path.realpath(path.expanduser(args[1]))
        if len(args) == 3:
            exit(SINTAX_ERROR)
        if len(args) == 4:
            if args[2] == "in":
                if not path.isdir(path.realpath(path.expanduser(args[3]))):
                    exit(f'"{args[3]}" Not Found or not a folder')
                else:
                    if not path.exists(args[3]):
                        exit(f'"{args[3]}" Not Found or not a folder')
                    animes_path = path.realpath(path. expanduser(args[3]))
            else:
                exit(COMMAND_UNKNOWN)
    
    animes = Animes(animes_path)
    reception = Reception(reception_path)
    dessorted_caps = reception.get_caps()
    iter = -1
    for cap in dessorted_caps:
        try:
            anime = animes.get_anime_by_id(cap.id)
        except KeyError:
            anime = animes.add_anime(f"{cap.id}_unamed")
        move(cap.path,anime.path)
        if iter == 0:
            print(f"relocated files:")
        print(f"\t{cap} to {anime.name}")
    print("All Sorted")
    if wait:
        input()
    exit()

def _view(*args)->NoReturn:
    animes = Animes(ANIMES_DIR)
    print(animes)
    
    if "--wait" in args:
        input()    
    exit()

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
if __name__ == '__main__':
    main(*argv)