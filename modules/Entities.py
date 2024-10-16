from operator import truediv
from os import listdir, mkdir, path, system
from modules import ID_ERROR,FormatError,ID_ERR
from A44M import A44Map,ConfigManager ,format_text
from modules.hocks import format_name_to_dir
CONFIG_DIR = path.expanduser("~\\animes")#!".\\database"
ANIMES = ConfigManager(CONFIG_DIR,"animes.json")

class Ico():
    def __init__(self,_path:str):
        if not path.isfile(_path):
            raise FileNotFoundError(f'"{_path}" Not Found or not a file')
        _path = path.realpath(_path)
        
        localitation = path.dirname(_path)
        file = path.basename(_path)
        extension = file.split(".")[-1]
        if not extension in ["jpeg", "jpg", "png", "gif","webp", "ico", "bmp"]:
            raise FormatError(f'"{_path}" Not is a image')
        id = self.__get_id(file)

        if extension == "ico":
            status = True
        else:
            status = False

        self.id:int = id 
        self.path:str = _path
        self.location:str = localitation
        self.extension:str = extension
        self.formatted:bool = status
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
    def get_staus(self)->str:
        if self.formatted:
            return "formatted"
        else:
            return "uncformatted"
    def converting(self)-> bool:
        #?script convertidor
        #?script eliminador
        pass
        
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
        self.name:str = format_text(*file.split("_")[1:])
        self.path:str = _path
        self.location:str = localitation
        self.length:int = 0
        self.caps:list[Cap] = self.__find_caps()
        
    def __find_caps(self)-> list[Cap]:
        children_files = listdir(self.path)
        caps:list[Cap] = []
        for child_file in children_files:
            try:
                temp = Cap(path.join(self.path,child_file))
            except FileNotFoundError:
                temp = None
            except ID_ERROR:
                temp = None
            except FormatError:
                temp = None
            if type(temp) == Cap:
                caps.append(temp)
                self.length += 1
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
        return f"{format_text(self.name,max=35)}: {self.length}"
    def set_icon(self,icons_path: str|None=None):
        
        init_file_path = path.join(self.path,"desktop.ini")
        if icons_path:
            icon_path = path.join(path.expanduser(icons_path),f"{self.id}.ico")
        else:
            icon_path = f"{self.id}.ico"
        iter = 0
        while True:
            iter+=1
            try:
                with open(init_file_path,"w") as f:
                    f.write(f'[.ShellClassInfo]\nIconResource="{icon_path}",0')
                    system(f'attrib +h "{init_file_path}"')
                    system(f'attrib +r "{self.path}"')
                    break
            except PermissionError as error:
                system(f'attrib -h "{init_file_path}"')
                system(f'attrib -r "{self.path}"')
                if iter>2:
                    print(error)
                    break
        
    def __len__(self)->int:
        return self.length
class Animes():
    def __init__(self,_path):
        if not path.isdir(_path):
            raise FileNotFoundError(f'"{_path}" Not Found or not a folder')
        animes = []
        self.length:int = 0
        objs = listdir(_path)
        for obj in objs:
            try:
                temp = Anime(path.join(_path,obj))            
            except ID_ERROR:
                temp = None
            except FileNotFoundError:
                temp = None
            if type(temp) == Anime:
                animes.append(temp)
                self.length+=1
        self.path = _path
        self.animes:tuple[Anime]=tuple(animes)
    def get_animes(self):
        return list(self.animes)
    def get_anime_by_id(self,id:int)->Anime:
        for anime in self.animes:
            if anime.id == id:
                return anime
        raise KeyError(id)
    def add_anime(self,anime_id:str,icons_path:str|None=None):
        try:
            anime_name = format_name_to_dir(ANIMES[anime_id]["title"])
        except KeyError as Error:
            raise KeyError(f'El id: "{str(Error).strip("'")}" no se encuentra en la base de datos')
        anime_path = f"{anime_id}_{anime_name}"
        try:
            mkdir(path.join(self.path,anime_path))
        except FileExistsError:
            pass    
        try:
            anime = Anime(path.join(self.path,anime_path))
            anime.set_icon(icons_path)
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
        str_ = (lambda a:f"{a} Animes:\n" if a > 0 else f"No Hay animes en el directorio especificado")(self.length)
        animes = list(self.animes)
        animes.reverse()
        for anime in animes:
            str_ += f"{anime}\n"
        return str_
class Reception():
    def __init__(self,_path):
        _path = path.realpath(_path)
        if not path.exists(_path):
            raise FileNotFoundError(f'"{_path}" Not Found')
        self.map = A44Map(path_=_path)
        caps:list = []
        icos:list = []
        def temp(_path):
            try:
                caps.append(Cap(_path))
                return
            except ID_ERROR:
                pass
            except FormatError:
                pass
            try:
                icos.append(Ico(_path))
                return
            except ID_ERROR:
                pass
            except FormatError:
                pass
                
        self.map._map(files_function=(temp))
        self.caps:tuple[Cap] = tuple(caps)
        self.icos:tuple[Ico] = tuple(icos)
    def get_caps_path(self)-> list[str]:
        caps_p = []
        for cap in self.caps:
            caps_p.append(cap.path)
        return caps_p
        
    def get_caps(self)->list[Cap]:
        return list(self.caps)
    def get_icos(self)->list[Ico]:
        return list(self.icos)