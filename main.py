__author__ = "Anderesu44"
__version__ = 1.0

from sys import argv,exit
from typing import NoReturn
from os import mkdir, listdir, path, system, getcwd
from model.dbm import ConfigManager
from model._class_ import Anime, Reseption, Cleaner
#{
ID_ERROR = "\nthe id given not is valid\n"
DIR_ERROR = "path specified not found"
NAME_ERROR = "not's valid name\na valid name cannot contain ['[', '<', '\\', '*', '\"', '|', ':', '?', '/', '>', ']',]"
COMMAND_UNKNOWN = "\ncommand unknown\ntry -h or --help\n"
ACCESS_DENIED = "Access denied"
VERSION = "1.0.0"
CONFIG_DIR = "C:\\ProgramData\\Anderesu44\\animes"
CFG = ConfigManager(CONFIG_DIR)

ANIMES_DIR:str = CFG["ANIMES_DIR"]
RESEPTION_DIR:str = CFG["RESEPTION_DIR"]
#}
def main(argv:list[str]):
    HELP = """
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
    if len(argv) == 1:
        print(HELP)
        exit()
    match argv[1]:
        case "-n"|"--new":
            _new(argv[1:])
        case "-s"|"--sort":
            _sort(argv[1:])
        case "--config":
            _config(argv[1:])
        case "-v"|"--view":
            _view(argv[1:])
        case "-h"|"--help":
            print(HELP)
            if "--wait" in argv:
                input()
            exit()
        case "--version":
            print(f"animes manager version:{VERSION}")
        case _:
            exit(COMMAND_UNKNOWN)
def _new(args:list)->NoReturn:
    HELP = f"""
animes {args[0]} <id:int> <name:str>

all the arguments after the 3rd will be taken as a name
"""
    if len(args) == 1:
        print(HELP)
        exit()
    if args[1] == "-h":
        print(HELP)
        exit()
    try:
        num = int(args[1])
    except ValueError:
        print(ID_ERROR)
        if "--wait" in argv:
                input()
        exit()
    if len(str(num)) != 4:
        num = f"{int(num):04}"
        if len(str(num)) != 4:

            print(ID_ERROR)
            if "--wait" in argv:
                input()
                exit()
    nam = ""
    c = 1
    for a in args[2:]:
        if c:
            nam += a
            c = 0
        else:
            nam += " " + a 
    if not _valid_name(nam):
        print(NAME_ERROR)
        if "--wait" in argv:
                input()
        exit()
    
    _path =f"{ANIMES_DIR}\\{num}_{nam}"
    try:
        mkdir(_path)
    except FileExistsError:
        pconten = listdir(_path)
        try:
            pconten.remove('desktop.ini')
        except ValueError:
            pass
        conten = []
        for o in pconten:
            try:
                num_ ,nam_ = o.split("_")
            except ValueError:
                num_ = o
            try:
                int(num_)
                if len(num_) != 4:
                    num_ = f"{int(num_):04}"
                    if len(str(num_)) != 4:
                        raise ValueError
                conten.append(o)
            except ValueError:
                pass
                
        conten = str(conten).replace("'","")
        raise FileExistsError(f"Cannot create a folder that already exists\n{num}_{nam}:\n\tContains:{conten}")
    exit()
def _sort(args:list)->NoReturn:
    HELP = f"""
animes <{args[0]}>
animes <{args[0]}> [path]
animes <{args[0]}> [command]
commands
    -h     => show help
special commands
    --wait => the program waits before ending
"""
    for arg in args[1:]:
        if arg == "-h":
            print(HELP)
            exit()
        elif arg == ".":
            try:
                listdir(getcwd())
                _DIR = getcwd()
            except FileNotFoundError:
                exit(DIR_ERROR)
        elif arg == "..":
            try:
                listdir(_back_dir())
                _DIR = _back_dir()
            except FileNotFoundError:
                exit(DIR_ERROR)
        elif arg == "--wait":
            _DIR = RESEPTION_DIR
        
        elif "-" in arg:
            exit(COMMAND_UNKNOWN)

    if len(args) == 1:
        _DIR = RESEPTION_DIR
        
    while True:
        try:
            reseption = Reseption(path.join(_DIR))
            reseption.search_in_tree()
            break
        except FileNotFoundError:
            mkdir(path.join(_DIR))
    
    animes = Anime(ANIMES_DIR)
    caps= reseption.get_items()
    files = {}
    for cap in caps:
        temp = (lambda x: x[-1] if x[-1] != "" else x[0])(cap.split("\\"))
        temp = temp.replace("LAT_","")
        a_num = temp.split("_")[0]# anime_number
        c_num = temp.split("_")[1]
        if len(a_num) != 4:
            a_num = f"{int(a_num):04}"
        
        temp = c_num.split(".")[0]
        c_num = ""#capter_number
        for c in temp:
            try:
                int(c)
                c_num += c
            except ValueError:
                pass
        while True:
            try:
                new_path = f"{animes.get_path(num=int(a_num))}\\{a_num}_{c_num}.mp4"
                break
            except KeyError:
                _new(["-n",a_num,"unnamed"])
        files[f"{_DIR}\\{cap}"] = new_path
    if len(args) == 1:
        Cleaner(_DIR)
    _move(files)
    for arg in args:
        if arg == "--wait":
            input()
    exit()

def _view(args:list)->NoReturn:
    a = Anime(ANIMES_DIR)
    print(a,end="",)
    for arg in args:
        if arg == "--wait":
            input()
    exit()

def _config(args:list)->NoReturn:
    HELP = f"""
animes {args[0]} <commands> [options]

commands
    --a_dir      => changes the animes directory \t\t({ANIMES_DIR})
    --r_dir      => changes the default resection directory \t({RESEPTION_DIR})
    --dir        => changes the animes directory and the default resection directory

    --cfg or -o  => open confing.cfg
    -h           => show help
""" 
    if len(args) == 1:
        exit(HELP)
    HELP_1 = f"""
animes {args[0]} {args[1]} <path>
animes {args[0]} {args[1]} <option>

options
    --back or -b    => back to the previous configuration
    --default or -d => set the default configuration
commands
    -h              => show help
""" 
    match args[1]:
        case "-h":
            exit(HELP)
        case "--cfg"|"-o":
            system(f"{CONFIG_DIR}\\a44.cfg")

        case "--a_dir"| "--r_dir" |"--dir":
            if len(args) == 2:
                exit(HELP_1)
            match args[2]:
                case "-h":
                    exit(HELP_1)
                case "--back" | "-b":
                    path_0 = CFG["ANIMES_DIR_OLD"]
                    path_1 = CFG["RESEPTION_DIR_OLD"]
                case "--default" | "-d":
                    path_0 = CFG["DEFAULT_ANIMES_DIR"]
                    path_1 = CFG["DEFAULT_RESEPTION_DIR"]
                case _:
                    if args[2][0] == "-":
                        exit(COMMAND_UNKNOWN)
                    path_0 = args[2]
                    path_1 = args[2] + "\\0000"
        case _:
            exit(COMMAND_UNKNOWN)

    match args[1]:
        case "--a_dir":
            try:
                mkdir(path_0)
            except FileNotFoundError:
                exit(DIR_ERROR)
            except PermissionError:
                exit(ACCESS_DENIED)
            except FileExistsError:
                pass
            CFG["ANIMES_DIR"] = path_0
            CFG["ANIMES_DIR_OLD"] = ANIMES_DIR
            CFG.save_config()
        case "--r_dir":
            try:
                mkdir(path_1)
            except FileNotFoundError:
                exit(DIR_ERROR)
            except PermissionError:
                exit(ACCESS_DENIED)
            except FileExistsError:
                pass
            CFG["RESEPTION_DIR"] = path_1
            CFG["RESEPTION_DIR_OLD"] = RESEPTION_DIR
            CFG.save_config()

        case "--dir":
            try:
                mkdir(path_0)
                mkdir(path_1)
            except FileNotFoundError:
                exit(DIR_ERROR)
            except PermissionError:
                exit(ACCESS_DENIED)
            except FileExistsError:
                pass
            CFG["ANIMES_DIR"] = path_0 
            CFG["ANIMES_DIR_OLD"] = ANIMES_DIR
            CFG["RESEPTION_DIR_OLD"] = path_1
            CFG["RESEPTION_DIR"] =  RESEPTION_DIR
            CFG.save_config()
            
        case _:
            exit(COMMAND_UNKNOWN)

def _valid_name(name:str)->bool:
    x = name
    if "\\" in x or "/" in x or ":" in x or "*" in x or "?" in x or '"' in x or "<" in x or ">" in x or "|" in x:
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
    main(argv)
    # main(["anime","-s",])#?only debug