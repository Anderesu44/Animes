__author__ = "Anderesu44"

from os import listdir

class Anime():
    def __init__(self,path:str):
        self.dir = self.__ani_dir = path
        self.__animes_path:dict[tuple[int, str], str] = {}
        self.__animes_keys_int:dict[int, str] = {}
        self.__animes_keys_str:dict[str, int] = {}
        objs = listdir(path)
        for o in objs:
            p = o
            try:
                num,nam = o.split("_")
                try:
                    int(num)
                except ValueError:
                    continue
                if len(num) != 4:
                    continue
            except ValueError:
                try:
                    pnum = o.split("_")[0]
                    if len(pnum) != 4:
                        raise ValueError
                    num = int(pnum)
                except ValueError:
                    continue
                nam = "unnamed"
            
            self.__animes_path[(int(num),nam)] = p
            self.__animes_keys_int[int(num)] = nam
            self.__animes_keys_str[nam] = int(num)
        
    def __str__(self,*args,**kwargs)->str:
        str_ = "\ns"
        for a in self.__animes_path:
            str_ += f"{a[0]:04}: \"{a[1].title()}\"\n"
        return str_
    get = __str__
    def get_paths(self,*args,**kwargs)->list[str]:
        _paths = []
        for a in self.__animes_path:
            _paths.append(f"{self.__ani_dir}\\{self.__animes_path[a]}")
        return _paths
    def get_path(self,*args,num:int =None,nam:str=None,**kwargs)->str:
        if num:
            try:
                num = int(num)
            except ValueError:
                raise TypeError("The \"num\" argument must be of type \"int\"")
            #
            _path = f"{self.__ani_dir}{self.__animes_path[(num,self.__animes_keys_int[num])]}"
            return _path
        if nam:
            return
        raise TypeError("Anime.get_path() missing 1 required keyword argument: num or name")
    
class Reseption(Anime):
    def __init__(self,path):
        super().__init__(path)
    

    
    
    