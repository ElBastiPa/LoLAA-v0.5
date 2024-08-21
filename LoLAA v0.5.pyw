import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO

def getChamps():
    url = 'https://ddragon.leagueoflegends.com/cdn/14.16.1/data/es_AR/champion.json'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        campeones = {}
        for key, value in data['data'].items():
            nombre = value['name']
            splash_url = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{key}_0.jpg"
            campeones[nombre] = splash_url
        return campeones
    else:
        print("Error")
        return None

def showImg(event):
    seleccion = campeones_listbox.get(campeones_listbox.curselection())
    imagen_url = campeones[seleccion]

    response = requests.get(imagen_url)
    imagen_data = response.content
    imagen = Image.open(BytesIO(imagen_data))
    imagen = imagen.resize((1000, 550), Image.ANTIALIAS)
    imagen_tk = ImageTk.PhotoImage(imagen)

    imagen_label.config(image=imagen_tk)
    imagen_label.image = imagen_tk

def searchChamp(event):
    texto_busqueda = search_var.get().lower()
    campeones_listbox.delete(0, tk.END)
    
    for campeon in campeones.keys():
        if texto_busqueda in campeon.lower():
            campeones_listbox.insert(tk.END, campeon)

root = tk.Tk()
root.title("Lista de Campeones de LoL")

campeones = getChamps()

search_var = tk.StringVar()
search_entry = tk.Entry(root, textvariable=search_var)
search_entry.pack(pady=5)
search_entry.bind('<KeyRelease>', searchChamp)

campeones_listbox = tk.Listbox(root, height=20, width=40)
for campeon in campeones.keys():
    campeones_listbox.insert(tk.END, campeon)
campeones_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

imagen_label = tk.Label(root)
imagen_label.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

campeones_listbox.bind('<<ListboxSelect>>', showImg)

root.mainloop()