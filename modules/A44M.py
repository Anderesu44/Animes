__author__ = "Anderesu44"
__version__ = .9

from json import load,dump
from os import listdir, mkdir, path, getcwd
from types import FunctionType as function

class Algorithms():
    def __init__(self) -> None:
        pass
    def bubbleSort(_list:list)->list:
        n = len(_list)
        for i  in range(1, n):
            for j in range(n-1):
                if _list[j] > _list[j+1]:
                    temp = _list[j]
                    _list[j] = _list[j+1]
                    _list[j+1] = temp
        return _list
    def __merge(self,list_1,list_2)->list:
        list_3 = []
        while len(list_1) > 0 and len(list_2) > 0:
            if  list_1[0] < list_2[0]:
                list_3.append(list_1[0])
                list_1 = list_1[1:]
            else:
                list_3.append(list_2[0])
                list_2 = list_2[1:]
        if len(list_1) > 0:
            list_3 = list_3 + list_1
        if len(list_2) > 0:
           list_3 = list_3 + list_2 
        return list_3
    def mergeSort(self,_list)-> list:
        if len(_list) == 1:
            return _list
        lList = _list[:len(_list)//2]
        rList = _list[len(_list)//2:]
        lList = self.mergeSort(lList)
        rList = self.mergeSort(rList)

        return self.__merge(lList,rList)
        
    def __str__():
        return 'conten : bubbleSort(list)\nmergeSort(list)'
def reducing_characters(text:str,character:str = " ")->str:
    #?reducing characters
    switch = 0
    new_text = ""
    for i in text:
        if switch:
            if i == character:
                switch = 1
                continue
            else:
                switch = 0
                new_text += i
        else:
            if i == character:
                switch = 1
                new_text += i
            else:
                new_text += i
    return new_text

class DataBaseJsonManger():
    def __init__(self,db_path:str=".\\db",name:str="db.json"):
        self.plain_file = path.join(path.realpath(db_path),name)
        if not path.exists(db_path):
            mkdir(db_path)
        try:
            with open(self.plain_file,"r+") as f:
                a = f.read()
                if a == "":
                    f.write("{\n\n}")
        except FileNotFoundError:
            with open(self.plain_file,"w") as f:
                f.write("{\n\n}")
    def create(self,id,registro):
        with open(self.plain_file,"r") as f:
            db_dict = load(f)
        try:
            if db_dict[id]:
                return False
        except KeyError:
            pass
        db_dict[id]=registro
        with open(self.plain_file,"w") as f:
            dump(db_dict,f,indent=2)
        return True
    def update(self,id,registro):
        with open(self.plain_file,"r") as f:
            db_dict = load(f)
        try:
            if not db_dict[id]:
                return False
        except KeyError:
            return False
        db_dict[id]=registro
        with open(self.plain_file,"w") as f:
            dump(db_dict,f,indent=2)
        return True
    def read(self,id=None):
        with open(self.plain_file,"r") as f:
            db_dict:dict = load(f)
        if id:
            return db_dict[id]
        else:
         return db_dict
    def delete(self,id):
        with open(self.plain_file,"r") as f:
            db_dict:dict = load(f)
        try:
            if not db_dict[id]:
                return False
        except KeyError:
            return False
        db_dict.pop(id)
        with open(self.plain_file,"w") as f:
            dump(db_dict,f,indent=2)
        return True
    def _set(self,data):
        with open(self.plain_file,"w") as f:
            dump(data,f,indent=2)
        return True

class ConfigManager(dict):
    def __init__(self,db_path: str = ".\\db",name: str = "cfg.json",init:dict|None=None):
        super().__init__()
        self.db = DataBaseJsonManger(db_path,name)
        self.load_config()
        if len(self)==0:
            if init:
                self.set_config(init)

    def save_config(self,*args,**kwargs):
        self.db._set(self)
    def load_config(self):
        data = self.db.read()
        for key in data:
            value = data[key]
            self.__setitem__(key,value)
    def set_config(self,data):
        for key in data:
            value = data[key]
            self.__setitem__(key,value)
        self.save_config()


class A44Map():
    def __init__(self,path_:str|None=None,folders_function:function|None=None,files_function:function|None=None) -> None:

        self.root:str = path_
        self.folders_function:function = folders_function
        self.files_function:function = files_function
        self.folders:list[str] = []
        self.files:list[str] = []
    
    def _map(self,folders_function:function=None,files_function:function=None):
        if folders_function:
            self.folders_function= folders_function
        if files_function:
            self.files_function= files_function
        self.__map(self.root)
        
    def __map(self,branch):
        childrens = listdir(branch)
        
        for child in childrens:
            child_path = path.join(branch,child)
            if path.isdir(child_path):
                #?child_type = "Branch"
                if self.folders_function == function:
                    self.folders_function(child_path)
                self.folders.append(child_path)
                self.__map(child_path)
            else:
                #*child_type = "Fruit"
                if self.files_function == function:
                    self.files_function(child_path)
                self.files.append(child_path)
    def __str__():
        pass
    
    def get_tree():...


if __name__ == "__main__":
    input()
