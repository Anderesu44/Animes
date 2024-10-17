from json import dump
from os import path
from bs4 import BeautifulSoup
import requests,threading,time
from A44M import format_text

from modules import CHARACTERS_ALLOWED, LOADING, NON_ALLOWED_CHARACTERS

def format_name_to_dir(name:str)->str:
    for c in NON_ALLOWED_CHARACTERS:
        name = name.replace(c,"")
    return name

def get_id_by_name(cursesWindow,curses,animes,name:str)->str:
    i = 0
    iters = 0
    curses.curs_set(0)
    for id in animes:
        if id == "0000":
            continue
        if name == animes[id]["title"]:
            return id
        cursesWindow.clear()
        i += 1
        if i % 70 == 0:
            iters+=1
        cursesWindow.addstr(0, 0,f"Buscado anime esto puede tardar un rato{LOADING[iters%len(LOADING)]}")
        cursesWindow.refresh()
    raise KeyError
def get_anime_by_name(cursesWindow,curses,animes:dict[dict],name:str)->dict:
    return animes[str(get_id_by_name(cursesWindow,curses,animes,name))]
def get_links_by_anime(cursesWindow,curses,anime:dict,start:int=1,end:int=-1)->dict[str,str]:
    curses.curs_set(0)
    name = __format_name(anime["title"])
    if end == -1:
        global stop_loading
        stop_loading = threading.Event()
        
        loading_thread = threading.Thread(target=loading_screen, args=(cursesWindow," caps"))
        loading_thread.start()

        end = get_chap_number_by_name(cursesWindow,curses,name)

        stop_loading.set()
        loading_thread.join()
    if 0 >= start > end:
        raise IndexError(f"Chapter index out of range: \n'{start}' to '{end}'")
    mega_links=""
    onefichier_links=""
    streamtape_links=""
    other_links=""
    progress = 0
    porsent = 0
    total = end-(start-1)
    for cap in range(start,end+1):
        current_progress = 0
        current_porsent = 0
        cursesWindow.clear()
        cursesWindow.addstr(0, 0,f'\r{("▬"*int(int(current_porsent)//2)).ljust(50,"-")} {format_text((lambda a: str(int(float(a))) if a.split(".")[-1] == "0" else a)(format_text(current_porsent,three_dot="",max=5)),"%",sep="",min_fill=(2," "))}/100% | {current_progress}/??')#?esta amalgama de codigo compactado es demaciado simple para separarlo pero leerlo es un infierno bueno simplemente: formatea el porsientop paraque no de resultados con mas de 2 dijitos despues de la coma osea que diga 33.33 en ves de 33.33333333334 y que cuando diga 33.0 digo 33 y le agrega espacios alfinal dependiendo de la cantidad de dijitos para que no mueva los de atras
        cursesWindow.addstr(1, 0,f'\r{("▬"*int(int(porsent)//2)) .ljust(50,"-")} {format_text((lambda a: str(int(float(a))) if a.split(".")[-1] == "0" else a)((format_text(porsent,three_dot="",max=5))),"%",sep="",min_fill=(2," "))}/100% | {progress}/{total}')#? lo mismo que la de arriva lo que muestra la barra total de progreso mientras la de arriva la del loop actual
        cursesWindow.refresh()
        url = f'https://www3.animeflv.net/ver/{name}-{cap}'
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.content
        else:
            with open(path.expanduser("~\\animes\\links.txt"),"w") as f:
                dump({"mega":mega_links,"1fichier":onefichier_links,"streamtape":streamtape_links,"others":other_links},f)
            raise IndexError(f"Chapter index out of range:[{cap}]\n'{start}' to '{end}'")
        soup = BeautifulSoup(html_content, 'html.parser')
        links = soup.find_all("a", class_="Button Sm fa-download")
        current_total = len(links)
        for link in links:
            link_txt:str = link["href"] + "\n"
            if "https://mega.nz" in link_txt:
                mega_links += link_txt.strip("\n") + "\n"
            elif "https://1fichier.com" in link_txt:
                onefichier_links += link_txt.strip("\n") + "\n"
            elif "https://streamtape.com" in link_txt:
                streamtape_links += link_txt.strip("\n") + "\n"
            else:
                other_links += link_txt + "\n"
            current_progress+=1
            current_porsent = current_progress/current_total*100
            porsent = ((progress+(current_porsent/100))/total)*100
            cursesWindow.clear()
            cursesWindow.addstr(0, 0,f'\r{("▬"*int(int(current_porsent)//2)).ljust(50,"-")} {format_text((lambda a: str(int(float(a))) if a.split(".")[-1] == "0" else a)(format_text(current_porsent,three_dot="",max=5)),"%",sep="",min_fill=(2," "))}/100% | {current_progress}/{current_total}')#?esta amalgama de codigo compactado es demaciado simple para separarlo pero leerlo es un infierno bueno simplemente: formatea el porsientop paraque no de resultados con mas de 2 dijitos despues de la coma osea que diga 33.33 en ves de 33.33333333334 y que cuando diga 33.0 digo 33 y le agrega espacios alfinal dependiendo de la cantidad de dijitos para que no mueva los de atras
            cursesWindow.addstr(1, 0,f'\r{("▬"*int(int(porsent)//2)) .ljust(50,"-")} {format_text((lambda a: str(int(float(a))) if a.split(".")[-1] == "0" else a)((format_text(porsent,three_dot="",max=5))),"%",sep="",min_fill=(2," "))}/100% | {progress}/{total}')#? lo mismo que la de arriva lo que muestra la barra total de progreso mientras la de arriva la del loop actual
            cursesWindow.refresh()
        progress+=1
    return{
        "mega":mega_links,
        "1fichier":onefichier_links,
        "streamtape":streamtape_links,
        "others":other_links
    }
def get_chap_number_by_name(cursesWindow,curses,name)->int:
    caps:int = 0
    for cap in range(1,2000):
        url = f'https://www3.animeflv.net/ver/{name}-{cap}'
        response = requests.get(url)
        status_code = response.status_code
        if status_code == 404:
            break
        elif status_code == 200:
            caps+=1
        else: 
            #!mandame el error a mi api
            # wath
            break
    return caps

def loading_screen(cursesWindow,objective:str=""):
    iters = 0
    while not stop_loading.is_set():
        iters += 1
        cursesWindow.clear()
        cursesWindow.addstr(0, 0, f"Buscando{objective}, esto puede tardar un rato {LOADING[iters % len(LOADING)]}")
        cursesWindow.refresh()
        time.sleep(0.5)
def __format_name(name:str)->str:
    name = name.strip().lower()
    new_name = ""
    for c in name:
        if c in CHARACTERS_ALLOWED:
            new_name += c
    return new_name.replace(" ","-")

