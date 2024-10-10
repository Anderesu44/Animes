from os import listdir, mkdir, path

from modules import ID_ERROR,FormatError,ID_ERR
from modules.A44M import A44Map, format_text

class Cap():
    def __init__(self,_path:str):
        if not path.isfile(_path):
            raise FileNotFoundError(f'"{_path}" Not Found or not a file')
        _path = path.realpath(_path)
        
        localitation = path.dirname(_path)
        file = path.basename(_path)
        extension = file.split(".")[-1]
        if not extension in ["mp4", "avi", "flv", "mpeg","mpg", "qt", "rm", "webm", "mkv"]:
            raise FormatError(f'"{_path}" Not is a video')

        
        self.id:int = self.__get_id(file)
        self.name:str = file.split("_")[-1].split(".")[0]
        self.path:str = _path
        self.location:str = localitation
        self.extension:str = extension
        
    def __str__(self)->str:
        return f"{self.id}_{self.name}.mp4"
    
    def __get_id(self,file:str)->int:
        _id = file.split("_")[0]
        if len(_id) > 4 or len(_id) < 3 or _id == "0000":
            raise ID_ERROR(ID_ERR+f'"{_id}"')
        try:
            _id = int(_id)
        except ValueError:
            raise  ID_ERROR(ID_ERR+f'"{_id}"')
        return _id
class Anime():
    def __init__(self,_path:str):
        _path = path.realpath(_path)
        if not path.isdir(_path):
            raise FileNotFoundError(f'"{_path}" Not Found or not a Folder')
        
        _path = path.realpath(_path)
        localitation = _path.replace(_path.split("\\")[-1],"")
        file= _path.split("\\")[-1]
        
        
        self.id:int = self.__get_id(file)
        self.name:str = format_text(*file.split("_")[1:],end="")
        self.path:str = _path
        self.location:str = localitation
        self.caps:list[Cap] = self.__find_caps()
        
    def __find_caps(self)-> list[Cap]:
        children_files = listdir(self.path)
        caps:list[Cap] = []
        for child_file in children_files:
            try:
                temp = Cap(child_file)
            except FileNotFoundError:
                temp = None
            except ID_ERROR:
                temp = None
            if temp:
                caps.append(temp)
        return caps
    
    def __get_id(self,file:str)->int:
        _id = file.split("_")[0]
        if len(_id) > 4 or len(_id) < 3 or _id == "0000":
            raise ID_ERROR(ID_ERR+f'"{_id}"')
        try:
            _id = int(_id)
        except ValueError:
            raise  ID_ERROR(ID_ERR+f'"{_id}"')
        return _id
    def __str__(self):
        return f"{self.name}: {len(self.caps)}"
    
class Animes():
    def __init__(self,_path):
        if not path.isdir(_path):
            raise FileNotFoundError(f'"{_path}" Not Found or not a folder')
        animes = []
        objs = listdir(_path)
        for obj in objs:
            try:
                temp = Anime(path.join(_path,obj))            
            except ID_ERROR:
                temp = None
            except FileNotFoundError:
                temp = None
            if temp:
                animes.append(temp)
        self.path = _path
        self.animes:tuple[Anime]=tuple(animes)
    def get_animes(self):
        pass
    def get_anime_by_id(self,id:int)->Anime:
        for anime in self.animes:
            if anime.id == id:
                return anime
        raise KeyError(id)
    def add_anime(self,anime:str):
        try:
            mkdir(path.join(self.path,anime))
        except FileExistsError:
            pass    
        try:
            anime = Anime(path.join(self.path,anime))            
        except ID_ERROR:
            anime = None
        except FileNotFoundError:
            anime = None
        if anime:
            animes = list(self.animes)
            animes.append(anime)
            self.animes = tuple(animes)
        return anime
    def __str__(self)->str:
        str_ = (lambda a:f"{a} Animes:\n" if a > 0 else "No Hay animes en el directorio especificado")(len(self.animes))
        for animes in self.animes:
            str_ += f"{animes}\n"
        return str_
class Reception():
    def __init__(self,_path):
        _path = path.realpath(_path)
        if not path.exists(_path):
            raise FileNotFoundError(f'"{_path}" Not Found')
        self.map = A44Map(path_=_path)
        caps:list = []
        def temp(_path):
            try:
                caps.append(Cap(_path))
            except ID_ERROR:
                pass
            except FormatError:
                pass
        self.map._map(files_function=(temp))
        self.caps:tuple[Cap] = tuple(caps)
    def get_caps_path(self)-> list[str]:
        caps_p = []
        for cap in self.caps:
            caps_p.append(cap.path)
        return caps_p
        
    def get_caps(self)->list[Cap]:
        return tuple(self.caps)