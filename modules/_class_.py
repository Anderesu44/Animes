__author__ = "Anderesu44"
__version__ = 1.0

from os import listdir,system

NONE_STR = ""
BACKSLSAH = "\\"

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
                    num = f"{int(num):04}"
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
        self._prv_ap = self.__animes_path
        self._prv_api= self.__animes_keys_int
        self._prv_aps= self.__animes_keys_str

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
            _path = f"{self.__ani_dir}\\{self.__animes_path[(num,self.__animes_keys_int[num])]}"
            return _path
        if nam:
            return
        raise TypeError("Anime.get_path() missing 1 required keyword argument: num or name")
    
class Reseption(Anime):
    def __init__(self,path:str):    
        super().__init__(path)    
        self.__ani_dir = self.dir
        self.__animes_path = self._prv_ap 
        self.__animes_keys_int=self._prv_api
        self.__animes_keys_str=self._prv_aps
        self.__caps_path = {}
        self.__caps_keys_int = {}
        self.__caps_keys_str = {}

    def search_in_tree(self,*args,**kwargs)->None:
        self.__search_in_tree(self.__ani_dir)

    def __search_in_tree(self,root:str,path:str="Simple",*args,branch:str|None=None,**kwargs)->None:
        actual_path = (lambda x,y: f"{y}\\{x}" if x else y)(branch,root)
        Branches = listdir(actual_path)
        for obj in Branches:
            try:
                listdir(f"{actual_path}\\{obj}")
                obj_type = "Branch"
                match path:
                    case "Simple":
                        pass
                    case "Complete":   
                        obj = f"{branch}\\{obj}"
                    case _:
                        exit("TypeError: ????????????")
            except NotADirectoryError:
                obj_type = "Fruit"
                match path:
                    case "Simple":
                        pass
                    case "Complete":   
                        obj = f"{branch}\\{obj}"
                    case _:
                        exit("TypeError: ????????????")

            if obj_type == "Branch":
                self.__search_in_tree(root,"Complete",branch=obj)
            elif obj_type == "Fruit":
                try:
                    match(obj.split(".")[-1]):
                        case "mp4" | "avi" | "flv" | "mpeg" | "qt" | "rm" | "webm" | "mkv":
                            pass
                        case _:
                            continue
                    temp = (lambda x: x[-1] if x[-1] != "" else x[0])(obj.split("\\"))
                    try:
                        a_num = temp.split("_")[0]
                        c_num = temp.split("_")[1]
                    except IndexError:
                        continue
                    try:
                        int(a_num)
                    except ValueError:
                        continue
                    if len(a_num) > 4:
                        continue
                except ValueError:    
                    continue
                self.__caps_path[(int(a_num),c_num)] = obj
                self.__caps_keys_int[int(a_num)] = c_num
                self.__caps_keys_str[c_num] = int(a_num)
    def get_items(self,*args,**kwargs)->list[str]:
        items = []
        for k in self.__caps_path:
            items.append(self.__caps_path[k])
        return items

class Cleaner():
    def __init__(self,path:str):
        listdir(path)
        self.deleted = 0
        self.clear_in_tree(path)

    def clear_in_tree(self,path,*args,**kwargs)->None:    
        self.__clear_in_tree(path)
        while True:
            if self.deleted >= 1:
                self.deleted = 0
                self.__clear_in_tree(path)
            else:
                break
    def __clear_in_tree(self,root:str,branch:str|None=None)->None:
        actual_path = (lambda x,y: f"{y}\\{x}" if x else y)(branch,root)
        branches = listdir(actual_path)
        if branches == []:
            self.deleted += 1
            system(f'rmdir "{actual_path}"')
        for obj in branches:
            try:
                listdir(f"{actual_path}\\{obj}")
                self.__clear_in_tree(actual_path,branch=obj)
            except NotADirectoryError:
                pass
            