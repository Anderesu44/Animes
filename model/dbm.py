__author__ = "Anderesu44"
__version__ = 0.9

from os import system
from builtins import dict

def main(*args,**kwargs):
    pass
    
    

class DataBaseManger():
    def __init__(self,db_path):
        self.db_path = db_path
        self.db_id = "#737825"
        if not self.check_db():
            self.make_db()

    def check_db(self,*args,**kwargs)->bool:
        try:
            file = open(f"{self.db_path}\\a44.cfg","r")
            #? añadir verificasion de sinaxis
            conten = (file.readlines())
            if not(conten[0].replace("\n","") == self.db_id):
                file.close()
                return False
            if not conten[2].replace("\n","") == f"__version__: {__version__};":
                file.close()
                return False
            file.close()
            return True
        except IndexError:
            return False
        except FileNotFoundError:
            return False
    
    def make_db(self,*args,**Kwargs):
        while True:
            try:
                file = open(f"{self.db_path}\\a44.cfg","w")
                break
            except FileNotFoundError:
                system(f"mkdir {self.db_path}")
                continue
        file.write(f"""{self.db_id}
file_type: a44_config;
__version__: {__version__};
""")
        file.close()
    
    def del_db(self,*args,**Kwargs):
        file = open(f"{self.db_path}\\a44.cfg","w")
        file.write("")
        file.close()

    def get_data(self,*args,**kwargs)->dict[str:str]:
        file = open(f"{self.db_path}\\a44.cfg","r")
        data = file.read()
        odata = {}
        selc = 0
        level = 0
        safe = 0
        key= ""
        value = ""
        for c in data:
            if safe:
                if level:
                        if selc:
                            value += c
                        else:
                            key += c
                        safe = 0
            match c:
                case "{":
                    level = 1
                    selc = 0
                case "}":
                    level = 0
                case ":":
                    selc = 1
                case ";":
                    if level:
                        odata[key.strip()] = value.strip()
                        key =""
                        value = ""
                        selc = 0
                case "?":
                    safe = 1
                case "\n"|"\t":
                    continue
                case _:
                    if level:
                        if selc:
                            value += c
                        else:
                            key += c
        return(odata)    
    
    def set_data(self,cfg:dict):
        fdata = """{{
{}
}}"""
        data = ""

        for _ in range(len(cfg)):
            a = cfg.popitem()
            a = str(a)
            a = a.replace("(","")
            a = a.replace(")","")
            a = a.replace("'","")
            a = a.replace(":","?:")
            a = a.replace(",",":")
            a = a.replace("{{}","?{{")
            a = a.replace("}}","?}}")
            a = a.replace("\\\\","\\")
            a = self.remove_spaces(a)
            a+=";\n"
            data+=a

        file = open(f"{self.db_path}\\a44.cfg","w")
        file.write(f"""{self.db_id}
file_type: a44_config;
__version__: {__version__};
{fdata.format(data)}""")
        file.close()

    def remove_spaces(self,text:str)->str:
        switch = 0
        new_text = ""
        for i in text:
            if switch:
                if i == " ":
                    switch = 1
                    continue
                else:
                    switch = 0
                    new_text += i
            else:
                if i == " ":
                    switch = 1
                    new_text += i
                else:
                    new_text += i
        return new_text


    
    def delte_config(self,*args,**kwargs)->str:
        self.db.set_data({})

class ConfigManager(dict):
    def __init__(self,db_path):
        super().__init__()
        self.db = DataBaseManger(db_path)
        self.load_config()

    def save_config(self,*args,**kwargs):
        self.db.set_data(self)
    def load_config(self):
        data = self.db.get_data()
        for key in data:
            value = data[key]
            self.__setitem__(key,value)
    # def __setitem__(self,key,value):
    #     super().__setitem__(key,value)
    
if __name__ == '__main__':
    main()


# class ConfigManager():
#     def __init__(self,db_path:str):
#         # self.db_path = db_path
#         self.db = DataBaseManger(db_path)
#         self.__def_value()
        
#     def __def_value(self):
#         self.file_path = self.db.get_data()["ANIMES_DIR"]
#         self.res_path = self.db.get_data()["RESEPTION_DIR"]
#         self.lang = self.db.get_data()["lang"]
    # def get_config(self,*args,**kwargs)->str:
    #     configs = [self.file_path_old,self.res_path_old,self.file_path,self.res_path, self.lang]
    #     cfgs = {}
    #     direct = 0
    #     if len(kwargs) ==0:
    #         if len(args) > 0:
    #             for i in args:
    #                 cfgs[i] = "X"
    #         else: 
    #             return configs
    #     else:
    #         cfgs = kwargs
    #     for k in cfgs:        
    #         match k:
    #             case "ANIMES_DIR":
    #                 if cfgs[k] == "!" or (not(cfgs[k])):
    #                     configs.remove(self.file_path)
    #                     direct = 1
    #                 if direct == 0:
    #                     return self.file_path
    #             case "RESEPTION_DIR":
    #                 if cfgs[k] == "!" or (not(cfgs[k])):
    #                     configs.remove(self.res_path)
    #                     direct = 1
    #                 if direct == 0:
    #                     return self.res_path
    #             case "OLD_ANIMES_DIR":
    #                 if cfgs[k] == "!" or (not(cfgs[k])):
    #                     configs.remove(self.file_path_old)
    #                     direct = 1
    #                 if direct == 0:
    #                     return self.file_path_old
    #             case "OLD_RESEPTION_DIR":
    #                 if cfgs[k] == "!" or (not(cfgs[k])):
    #                     configs.remove(self.res_path_old)
    #                     direct = 1
    #                 if direct == 0:
    #                     return self.res_path_old
    #             case "lang":
    #                 if cfgs[k] == "!" or (not(cfgs[k])):
    #                     configs.remove(self.lang)
    #                     direct = 1
    #                 if direct == 0:
    #                     return self.lang
    #     if direct:
    #         return configs
    # def set_config(self,*args,**kwargs):
    #     for k in kwargs:
    #         match k:
    #             case "ANIMES_DIR":
    #                 self.file_path=kwargs[k]
    #             case "RESEPTION_DIR":
    #                 self.res_path=kwargs[k]
    #             case "OLD_ANIMES_DIR":
    #                 self.res_path=kwargs[k]
    #             case "OLD_RESEPTION_DIR":
    #                 self.res_path=kwargs[k]
    #             case "lang":
    #                 self.lang=kwargs[k]
    #     self.save_config()

    #? def save_config(self,*args,**kwargs):
    #?     cfg = {"ANIMES_DIR": self.file_path,"RESEPTION_DIR": self.res_path, "lang" : self.lang,
    #?           "OLD_ANIMES_DIR": self.file_path_old,"OLD_RESEPTION_DIR": self.res_path_old,}
    #?    self.db.set_data(cfg)