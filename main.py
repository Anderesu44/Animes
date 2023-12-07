__author__ = "Anderesu44"

from sys import argv,exit
from typing import NoReturn
from os import mkdir,listdir,path,system
from model._class_ import Anime , Reseption
#{
COMMAND_UNKNOWN = "\ncommand unknown\ntry -h or --help\n"
ID_ERROR = "\nthe id given not is valid\n"
NAME_ERROR = "not's valid name\na valid name cannot contain ['[', '<', '\\', '*', '\"', '|', ':', '?', '/', '>', ']',]"
VERSION = "0.2.5"
ANIMES_DIR = "D:\\"
#}
def main(argv):
    HELP = """
animes <command> [option]
    -n or --new     => make new animme folder
    -s or --sort    => sort the animes in reseption folder

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
        case "-v"|"--view":
            _view(argv[1:])
        case "-h"|"--help":
            print(HELP)
        case "--version":
            print(f"animes version:{VERSION}")
        case _:
            print(COMMAND_UNKNOWN)
            exit()
def _new(args:list)->NoReturn:
    HELP = f"""
animes {argv[0]} <id:int> <name:str>

all the arguments after the 3rd will be taken as a name
"""
    if args == 1:
        print(HELP)
        exit()
    if args[1] == "-h":
        print(HELP)
        exit()
    try:
        num = int(args[1])
    except ValueError:
        print(ID_ERROR)
        exit()
    if len(str(num)) != 4:
        print(ID_ERROR)
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
        exit()
    
    _path = path.join(ANIMES_DIR,f"{num}_{nam}")
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
                    raise ValueError
                conten.append(o)
            except ValueError:
                pass
                
        conten = str(conten).replace("'","")
        raise FileExistsError(f"Cannot create a folder that already exists\n{num}_{nam}:\n\tContains:{conten}")
    exit()
def _sort(args)->NoReturn:
    HELP = f"""
animes <{args[0]}> [command]
commands
    -h     => show help
special commands
    --wait => the program waits before ending
"""
    for arg in args[1:]:
        if arg == "-h":
            print(HELP)
        elif "-" in arg and arg != "--wait":
            print(COMMAND_UNKNOWN)
            exit()
    while True:
        try:
            reseption = Reseption(path.join(ANIMES_DIR,"0000"))
            break
        except FileNotFoundError:
            mkdir(path.join(ANIMES_DIR,"0000"))
    animes = Anime(ANIMES_DIR)
    caps = reseption.get_paths()
    for cap in caps:
        temp = cap.split("_")[0]
        temp = temp.replace(ANIMES_DIR + "0000\\","")
        a_num = int(temp)# anime_number

        temp = cap.split("_")[1]
        c_num = "" #capter_number
        for c in temp:
            try:
                int(c)
                c_num += c
            except ValueError:
                break
        while True:
            try:
                new_path = f"{animes.get_path(num=a_num)}\\{a_num}_{c_num}.mp4"
                break
            except KeyError:
                _new(["-n",a_num,"unnamed"])
        system(f'move "{cap}" "{new_path}"')
        print(f"relocated file:\n\t{cap} to {new_path}\n")
    print("All Sorted")
    for arg in args:
        if arg == "--wait":
            input()
    exit()
def _view(*args)->NoReturn:
    a = Anime(ANIMES_DIR)
    print(a,end="",)
    for arg in args:
        if arg == "--wait":
            input()
    exit()

def _valid_name(name)->bool:
    x = name
    if "\\" in x or "/" in x or ":" in x or "*" in x or "?" in x or '"' in x or "<" in x or ">" in x or "|" in x:
        return False
    else:
        return True
if __name__ == '__main__':
    main(argv)