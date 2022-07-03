import tkinter as tk
import pygame as py
import os
from tkinter import ttk

class MP3: # Speciální knihovna pro pouštění hudby
    def __init__(self,prikazy):
        self.prikazy = prikazy
        self.poradi_songy = 0
        self.hudba_nastaveni = "nehraje"
        self.index = 0
        py.mixer.init()
    
    def playlist(self): # Vypíše playlist, aby mohl uživatel si zvolit vlastní song
        self.root = tk.Tk()
        self.root.resizable(width=False, height=False) # Zamezí zvětšování/zmenšování aplikace
        self.root.iconbitmap("data/ikona/ikona.ico")        
        self.root.title("MP3 Playlist")
        
        self.listbox_playlist = tk.Listbox(self.root,bg="white",width=35) 
        self.listbox_playlist.bind("<<ListboxSelect>>",self.vyber_polozku)
        
        try:
            nazev, cesta_k_songu = self.nacti_pisnicky()
            delka = len((max(nazev, key = len)))
            if delka > 35:    
                self.listbox_playlist.configure(width=delka)
        except:
            nazev = []
            cesta_k_songu = []
            
        for song in nazev:
            self.listbox_playlist.insert(tk.END,song)
        
        self.tlacitko_spusti = tk.Button(self.root,text="Spusti",fg="white",bg="#ff6600",borderwidth=2,relief="solid",width=13,command=self.tlacitko_hrej)
        self.tlacitko_odejdi = tk.Button(self.root,text="Odejdi",fg="white",bg="#ff6600",borderwidth=2,relief="solid",width=13,command=self.vypni_playlist)
        
        self.scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.listbox_playlist.yview)
        self.listbox_playlist.configure(yscroll=self.scrollbar.set)
        
        self.listbox_playlist.grid(column=1,row=1,sticky="nswe",pady=(0,10),columnspan=2)
        self.scrollbar.grid(column=3,row=1,sticky="ns",pady=(0,10))
        
        self.tlacitko_spusti.grid(column=1, row=2,padx=3,pady=6)
        self.tlacitko_odejdi.grid(column=2, row=2,padx=3,pady=6)
        
        self.root.mainloop()
    
    def vypni_playlist(self): # Vypne playlist
        self.root.destroy()
        
    def tlacitko_hrej(self): # Spustí song, který si zvolíme v playlistu
        self.poradi_songy = self.index
        self.hrej_song()
    
    def vyber_polozku(self,event):
        self.index = self.listbox_playlist.curselection()[0]
            
    def nacti_pisnicky(self): # Načte naše songy
        self.nazev_songy = []
        self.cesta_k_songu = []
        try:
            for song in os.listdir(self.prikazy.asistent.gui.odkaz_na_hudbu.get()):
                if ".mp3" in song:
                    self.cesta_k_songu.append(self.prikazy.asistent.gui.odkaz_na_hudbu.get()+"/"+song)
                    self.nazev_songy.append(os.path.basename(song).replace(".mp3",""))
            return self.nazev_songy, self.cesta_k_songu        
        except:
            pass
    
    def hrej_song(self):
        try:
            nazev_songy, cesta_k_songu = self.nacti_pisnicky()
            if len(nazev_songy) == 0:
                self.prikazy.asistent.mluv("V playlistu jsem nenašla žádnou písničku")
            else:
                self.prikazy.asistent.mluv("Hraji "+nazev_songy[self.poradi_songy])
                py.mixer.music.load(cesta_k_songu[self.poradi_songy])
                self.hudba_nastaveni = "hraje"
                py.mixer.music.play(loops=0)
        except:
            self.prikazy.asistent.mluv("Nastal problém s otevřením playlistu") 
            self.prikazy.asistent.mluv("Zkontrolujte, zda máte nastavenou složku playlistu") 
            
    def pauza_song(self):
        if self.hudba_nastaveni == "hraje":
            py.mixer.music.pause()
            self.hudba_nastaveni = "pozastavena"
            self.prikazy.asistent.mluv("Zastavuji hudbu")     
        else:
            self.prikazy.asistent.mluv("Jelikož hudba nehraje, nemůžu ji zastavit")  
    
    def pokracovat_song(self):
        if self.hudba_nastaveni == "pozastavena":
            py.mixer.music.unpause()
            self.hudba_nastaveni = "hraje"
            self.prikazy.asistent.mluv("Pokračuji v přehráváná")     
        else:
            self.prikazy.asistent.mluv("Jelikož hudba není zastavená, nemůžu pokračovat v poslechu")                
               
    def preskocit_dopredu_song(self):
        try:
            nazev_songy, cesta_k_songu = self.nacti_pisnicky()
            if self.poradi_songy == len(nazev_songy)-1:
                self.poradi_songy = 0
            else:
                self.poradi_songy += 1
            
            self.prikazy.asistent.mluv("Přeskakuji na další písničku")
            self.hrej_song()
        except:
            self.prikazy.asistent.mluv("Nastal problém s otevřením playlistu") 
            self.prikazy.asistent.mluv("Zkontrolujte, zda máte nastavenou složku playlistu") 
    
    def preskocit_dozadu_song(self):
        try:
            nazev_songy, cesta_k_songu = self.nacti_pisnicky()
            if self.poradi_songy == 0:
                self.poradi_songy = len(nazev_songy)-1
            else:
                self.poradi_songy -= 1
            
            self.prikazy.asistent.mluv("Přeskakuji na předchozí písničku")
            self.hrej_song()
        except:
            self.prikazy.asistent.mluv("Nastal problém s otevřením playlistu") 
            self.prikazy.asistent.mluv("Zkontrolujte, zda máte nastavenou složku playlistu") 