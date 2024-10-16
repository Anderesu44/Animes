__author__ = "A44"
__version__ = 2.5


from os import getcwd, listdir, mkdir, path, system
from sys import argv,exit
from typing import NoReturn

from modules import ID_ERR as ID_ERROR
from A44M import ConfigManager, format_text
from modules.Entities import Animes, Reception


DIR_ERROR = "Not Found or not a folder"
NAME_ERROR = "not's valid name\na valid name cannot contain ['[', '<', '\\', '*', '\"', '|', ':', '?', '/', '>', ']',]"
SINTAX_ERROR ="the command syntax's not correct try --help"
COMMAND_UNKNOWN = "\ncommand unknown\ntry -h or --help\n"
ACCESS_DENIED = "Access denied"

VERSION = "2.5.0"
CONFIG_DIR = path.expanduser("~\\animes")
INST_DIR = "C:\\Program Files\\Anderesu44\\animes"
INIT_CONFIG = {"DEFAULT_ANIMES_DIR": "~/Videos/Animes","DEFAULT_RECEPTION_DIR": "~/Videos/Animes/0000","DEFAULT_ICONS_FOLDER":None,"ANIMES_DIR": "~/Videos/Animes","RECEPTION_DIR": "~/Videos/Animes/0000","ICONS_FOLDER":None,"ANIMES_OLD_DIR": "~/Videos/Animes","RECEPTION_OLD_DIR": "~/Videos/Animes/0000","ICONS_OLD_FOLDER":None}
CFG = ConfigManager(CONFIG_DIR,init=INIT_CONFIG)
ANIMES_DIR = path.realpath(path.expanduser(CFG["ANIMES_DIR"]))
RECEPTION_DIR = path.realpath(path.expanduser(CFG["RECEPTION_DIR"]))
int
def main(*args:tuple[str]): 
    HELP="""
animes <command> [option]
    -n or --new      => make new animme folder
    -s or --sort     => sort the animes in reception folder
    -u or --update   => update the database or the app if needed
    --config         => changes the program configuration

    -d or --download => show the downloads links and copy them on the clipboard
    -v or --view     => show all animes folders
    -h or --help     => show help
    --version        => show vesion

special commands
    --wait          => the program waits before ending
"""
    if len(args) == 1:
        exit(HELP)
    match args[1].lower():
        case "-n"|"--new":
            _new(*args[1:])
        case "-s"|"--sort":
            _sort(*args[1:])
        case "-u"|"--update":
            exit("in development")
        case "--config":
            _config(*args[1:])
        case "-d"|"--download":
            exit("in development")
            _download(*args[1:])
        case "-v"|"--view":
            _view(args[1:])
        case "-h"|"--help":
            print(HELP)
            if "--wait" in args:
                input()
            exit()
        case "--version":
            print(f"animes manager version:{VERSION}")
            if "--wait" in args:
                input()
            exit()
        case "--show-ins_dir":
            exit(INST_DIR)
        case _:
            exit(COMMAND_UNKNOWN)

def _new(*args)->NoReturn:
    HELP = f"""
animes {args[0]} <id:int> <name:str>
all the arguments after the 3rd will be taken as a name
animes {args[0]} <id:int> <--auto>
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
    if args[2] == "--auto":
        animes = Animes(ANIMES_DIR)
        try:
            animes.add_anime(str(num),CFG["ICONS_FOLDER"])
        except KeyError as Error:
            exit(f'{str(Error).strip("'")}\npuede solusionar el problema de las siguientes maneras:\ncompruebe que el id, debe dar una id valida no un nombre\ncompruebe la version de la vase de datos si es necesario actualice\nEn caso de que el error persista comuniquese con A44')
        exit("All right")
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
    from shutil import move,Error as MoveError
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
        temp = list(args)
        temp.remove("--wait")
        args = tuple(temp)
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
                    animes_path = path.realpath(path.expanduser(args[3]))
            else:
                exit(COMMAND_UNKNOWN)
    
    animes = Animes(animes_path)
    reception = Reception(reception_path)
    dessorted_caps = reception.get_caps()
    
    progres = 0
    end = len(dessorted_caps)
    for cap in dessorted_caps:
        porsent = 0
        print(f'\r{("▬"*int(int(porsent)//2)) .ljust(50,"-")}',end=f" {format_text((lambda a: str(int(float(a))) if a.split(".")[-1] == "0" else a)((format_text(porsent,three_dot="",max=5))),"%",sep="",min_fill=(6," "))}/100% | {progres}/{end}")
        try:
            anime = animes.get_anime_by_id(cap.id)
        except KeyError:
            anime = animes.add_anime(f"{cap.id}",CFG["ICONS_FOLDER"])
        try:
            move(cap.path,anime.path)
        except MoveError as Error:
            Error = str(Error)
            print(f'\nDestination "{cap}" already exists')
        except OSError as Error:
            Error = str(Error)
            exit("\n"+Error.replace(format_text(*Error[Error.find("["):Error.find("]")+1],sep=""),""))
        # except FileExistsError:
            # pass
        progres+=1
        porsent = progres/end*100
        print(f'\r{("▬"*int(int(porsent)//2)) .ljust(50,"-")}',end=f" {format_text((lambda a: str(int(float(a))) if a.split(".")[-1] == "0" else a)((format_text(porsent,three_dot="",max=5))),"%",sep="",min_fill=(6," "))}/100% |{progres}/{end}")
    if len(dessorted_caps)>0:
        print(f"\r{"▬"*50} 100%                \nCaps sorted",end="\n")
    
    dessorted_icos = reception.get_caps()
    progres = 0
    end = len(dessorted_icos)
    for ico in dessorted_icos:
        try:
            anime = animes.get_anime_by_id(ico.id)
        except KeyError:
            anime = animes.add_anime(f"{ico.id}",CFG["ICONS_FOLDER"])
        try:
            move(ico.path,anime.path)
        except MoveError:
            pass
        progres+=1
        porsent = progres/end*100
        print(f'\r{("▬"*int(int(porsent)//2)) .ljust(50,"-")}',end=f" {format_text((lambda a: str(int(float(a))) if a.split(".")[-1] == "0" else a)((format_text(porsent,three_dot="",max=5))),"%",sep="",min_fill=(6," "))}/100%")
    if len(dessorted_icos) > 1:
        print(f"\r{"▬"*50} 100%                \nIcons sorted",end="\n")
    print("All Sorted",end="")
    if wait:
        input()
    exit()

def _view(*args)->NoReturn:
    animes = Animes(ANIMES_DIR)
    print(animes)
    
    if "--wait" in args:
        input()    
    exit()

def _config(*args)->NoReturn:
    from time import sleep
    from keyboard import KEY_DOWN, read_event
    HELP = f"""
animes {args[0]} <commands> [options]

commands
    --a_dir      => changes the animes directory \t\t({format_text("...",*(ANIMES_DIR.split("\\")[-3:]),sep="\\")}))
    --r_dir      => changes the default resection directory \t({format_text("...",*(RECEPTION_DIR.split("\\")[-3:]),sep="\\")})
    --i_dir      => changes the icons directory  (set to None | null | False to save them in the same anime folder) 
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
            editor = "notepad"
            print("abrir con:\n>Notepad  VSCode",end="")
            screen = ">Notepad  VSCode"
            while True:
                event = read_event()    
                if event.name == "esc":
                    exit("cancel")
                if event.event_type == KEY_DOWN:
                    if event.name == "left":
                        screen = "\r>Notepad  VSCode"
                        editor = "notepad"
                    if event.name == "right":
                        screen = "\r Notepad >VSCode"
                        editor = "code"
                    if event.name == "enter":
                        print("\nopen config file.",end="")
                        sleep(1)
                        print("\ropen config file..",end="")
                        sleep(1)
                        system(f'{editor} "{path.join(CONFIG_DIR,"cfg.json")}"')
                        exit("\ropen config file...")
                print(screen,end="")

        case "--a_dir"| "--r_dir"|"--dir":
            if len(args) == 2:
                exit(HELP_1)
            match args[2]:
                case "-h":
                    exit(HELP_1)
                case "--back" | "-b":
                    path_0 = path.realpath(path.expanduser(CFG["ANIMES_OLD_DIR"]))
                    path_1 = path.realpath(path.expanduser(CFG["RECEPTION_OLD_DIR"]))
                case "--default" | "-d":
                    path_0 = path.realpath(path.expanduser(CFG["DEFAULT_ANIMES_DIR"]))
                    path_1 = path.realpath(path.expanduser(CFG["DEFAULT_RECEPTION_DIR"]))
                case _:
                    if args[2][0] == "-":
                        exit(COMMAND_UNKNOWN)
                    if not path.isdir(path.realpath(path.expanduser(args[2]))):
                        exit(f'"{args[2]}" Not Found or not a folder')
                    path_1 = path_0 = path.realpath(path.expanduser(args[2]))
        case  "--i_dir":
            if len(args) == 2:
                exit(HELP_1)
            match args[2].lower():
                case "-h":
                    exit(HELP_1)
                case "--back" | "-b":
                    path_2:str|None = (lambda a:path.realpath(path.expanduser(a)) if a else None)(CFG["ICONS_OLD_FOLDER"])
                case "--default" | "-d":
                    path_2:str|None = (lambda a:path.realpath(path.expanduser(a)) if a else None)(CFG["DEFAULT_ICONS_FOLDER"])
                case "none"|"null"|"false":
                    path_2 = None
                case _:
                    if args[2][0] == "-":
                        exit(COMMAND_UNKNOWN)
                    if not path.isdir(path.realpath(path.expanduser(args[2]))):
                        exit(f'"{args[2]}" Not Found or not a folder')
                        path_2 = path.realpath(path.expanduser(args[2]))
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
            CFG["ANIMES_OLD_DIR"] = ANIMES_DIR
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
            CFG["RECEPTION_DIR"] = path_1
            CFG["RECEPTION_OLD_DIR"] = RECEPTION_DIR
            CFG.save_config()
        case "--i_dir":
            try:            
                if path_2:
                    mkdir(path_2)
                    path_2 = path_2.replace(path.expanduser("~"),"~")
            except FileNotFoundError:
                exit(DIR_ERROR)
            except PermissionError:
                exit(ACCESS_DENIED)
            except FileExistsError:
                pass
            
            CFG["ICONS_OLD_FOLDER"] = CFG["ICONS_FOLDER"]
            CFG["ICONS_FOLDER"] = path_2
            CFG.save_config()
            print("you want to link all the Animes icons to this new directory?")
            decision = input("  y/n?: ")
            if decision.lower() != "y":
                exit('Successful')
            else:
                animes = Animes(ANIMES_DIR)
                for anime in animes.animes:
                    anime.set_icon(path_2)
                exit('Successful')
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
            CFG["ANIMES_OLD_DIR"] = ANIMES_DIR
            CFG["RECEPTION_DIR"] = path.join(path_1,"0000")
            CFG["RECEPTION_OLD_DIR"] =  RECEPTION_DIR
            CFG.save_config()
        case _:
            exit(COMMAND_UNKNOWN)
    exit("Successful")
   
def _download(*agrs)->NoReturn:
    HELP = """
    """
    exit()
    
def _valid_name(name:str)->bool:
    if "\\" in name or "/" in name or ":" in name or "*" in name or "?" in name or '"' in name or "<" in name or ">" in name or "|" in name:
        return False
    else:
        return True

if __name__ == '__main__':
    try:
        main(*argv)
    except Exception as Error:
        #!pide permiso
        from json import dumps
        from datetime import datetime
        from sys import platform
        file = path.join(INST_DIR,"feed.txt")
        txt = f"""{datetime.now()}:\n{format_text(*argv)}\r	  {type(Error).__name__}: {str(Error)}:
            version:{VERSION}
            cfg:{"{"}
{dumps(CFG,indent=18).rstrip("\n}}").lstrip("\n{{")}
            {"}"}
            sys: {platform}
            cfgdir: {CONFIG_DIR}
            anidir: {ANIMES_DIR}
            recdir: {RECEPTION_DIR}
            insdir: {INST_DIR}
            Conten: {format_text(*listdir(INST_DIR),sep="\n                    ")} 
            \n"""
        with open(file,"a") as f:
            f.write(txt)
        exit("\nups a ocurrido un error inesperado\nPorfavor contacte con a44 en:\nhttps://anderesu44.github.io/descktop/#/msg")