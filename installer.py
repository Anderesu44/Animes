__author__ = "Anderesu44"
__version__ = 0.8

PROJECT_NANE = "animes"
INSTAL_PATH = "C:\\Program Files\\Anderesu44\\"

from os import listdir,mkdir,getcwd,system
from tkinter.messagebox import askquestion,showinfo

def main():
    files = [("model","_class_.py"),("res","Anderesu44.ico"),("pwd","icon.ico")]
    new = []
    is_new = False
    while True:    
        try:
            listdir(INSTAL_PATH)
            break
        except FileNotFoundError:
            mkdir(INSTAL_PATH)
    while True:
        try:
            listdir(INSTAL_PATH + PROJECT_NANE)
            break
        except FileNotFoundError:
            mkdir(INSTAL_PATH+PROJECT_NANE)
            is_new = True
    if is_new:
        _set(files)
        showinfo("Operacion completada","el programa se instalo corectamente")
    else:
        if askquestion("¿Desea Actualizar?","EL programa ya se encuentra instalado,\n¿Desea Actualizar?") == "yes":
            _set(new)
            showinfo("Operacion completada","el programa se actualizo corectamente")
        else:
            showinfo("Operacion canselada","el programa no se acutalizo")
    

def _set(files:list[tuple[str,str]]=[("_file","_path")]):
    pwd = getcwd()
    inst = INSTAL_PATH + PROJECT_NANE
    sub_dirs = set()
    paths = [(f"{pwd}\\main.exe",f"{inst}\\{PROJECT_NANE}.exe")]
    for file_ in files:
        if file_[0] == "pwd":
            dir_ = pwd
            new_dir = inst
        else:
            dir_ = f"{pwd}\\{file_[0]}"
            new_dir = f"{inst}\\{file_[0]}"
            sub_dirs.add(new_dir)
        if file_[1].count(".") != 1 :
            _file = file_[1]
            exte = ""
            new_exte = "dll"
        else:
            _file,exte=file_[1].split(".")
            if exte == "py":
                new_exte = "dll"
            else:
                new_exte = exte
            exte = "." + exte
        paths.append((
            f"{dir_}\\{_file}{exte}",
            f"{new_dir}\\{_file}.{new_exte}"
            ))
    for sub_dir in sub_dirs:
        system(f'mkdir "{sub_dir}"')
    for path_ in paths:
        system(f'remove "{path_[1]}"')
        system(f'copy "{path_[0]}" "{path_[1]}"')

if __name__ == '__main__':
    main()