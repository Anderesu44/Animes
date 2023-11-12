__author__ = "Anderesu44"

from os import listdir

class Anime():
    def __init__(self,path):
        self.__ani_dir = path
        self.__animes_path :dict[tuple, str] = {}
        self.__animes_keys_int:dict[int, str] = {}
        self.__animes_keys_str:dict[str, int] = {}
        objs = listdir(path)
        for o in objs:
            try:
                num,nam = o.split("_")
            except ValueError:
                try:
                    num = int(o.split("_")[0])
                except ValueError:
                    continue
                nam = "unnamed"
            
            self.__animes_path[(int(num),nam)] = o
            self.__animes_keys_int[int(num)] = nam
            self.__animes_keys_str[nam] = int(num)
        
    def __str__(self,*args,**kwargs)->str:
        str_ = "\ns"
        for a in self.__animes_path:
            str_ += f"{a[0]:04}: \"{a[1].title()}\"\n"
        return str_
    get = __str__
    def get_paths(*args,**kwargs)->list:
        pass
    def get_path(*args,num:int =None,nam:str=None,**kwargs)->str:
        if num:
            try:
                int(num)
            except ValueError:
                raise TypeError("The \"num\" argument must be of type \"int\"")
            return
        if nam:
            return
        raise TypeError("Anime.get_path() missing 1 required keyword argument: num or name")
    
    
    
    