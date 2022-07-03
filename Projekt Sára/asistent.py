import os
import tkinter as tk
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
from hlavni_prikazy import Prikazy



class Asistent:
    def __init__(self,gui):
        self.gui = gui
        self.kontrolni_bool = 0
        self.prikazy = Prikazy(self)
        self.prikazy.nacitani.nejdriv_nacti() # Načte základní konfigurační data, jako je ukládání ke spánku 
    
    def mluv(self,text,vypsani_textu = True): # Slouží pro zvukový výstup sáry
        try:
            if vypsani_textu:
                self.gui.text_sary.configure(text=text)
            tts = gTTS(text=text,lang="cs") # Převede text na zvuk
            nazev = "zvuk.mp3" 
            tts.save(nazev) # Uloží zvuk jako .mp3
            playsound.playsound(nazev) # Přehraje zvuk
            os.remove(nazev) # Vymaže zvukový soubor
        except:
            print("Nastal neočekávaný problém. Jedna z možností je odpojení od sítě.")
    
    def aktivator_sary(self): # Slouží k aktivaci Sáry ze spánkového režimu
        r = sr.Recognizer() # inicializace rozpoznávače
        try:
            with sr.Microphone() as zdroj: # Zapnutí mikrofonu
                zvukovy_soubor = r.listen(zdroj)
                prevedeny_text = ""
                try:
                    prevedeny_text = r.recognize_google(zvukovy_soubor,language="cs") # Rozpozná zvuk a převede na text
                    self.gui.text_uzivatele.configure(text=prevedeny_text) # Zapíše text do LABELU uživatele
                    prevedeny_text = str(prevedeny_text).lower()
                except sr.UnknownValueError: # Když nerozpozná zvuk, neudělá nic
                    pass   
                except sr.RequestError: # Pokud náhodou vypadnou servery googlu
                    prevedeny_text = "Omlouvám se, ale systém není momentálně funkční.".lower()
                    self.gui.text_uzivatele.configure(text="")
                    self.gui.text_sary.configure(text=prevedeny_text)  
                if prevedeny_text == "poslouchej":
                    return 1
                else:
                    return 0       
        except:
            prevedeny_text = "Omlouvám se, ale mikrofon nebyl nalezen"
            self.gui.text_uzivatele.configure(text="")
            self.gui.text_sary.configure(text=prevedeny_text)
            self.mluv(prevedeny_text)
            return 0
            
        
    def zvuk_na_text(self): # Stejné je jako u aktivatoru sary, ale upravené pro moje účely
        r = sr.Recognizer()
        try:
            with sr.Microphone() as zdroj: # Zapnutí mikrofonu
                zvukovy_soubor = r.listen(zdroj)
                prevedeny_text = ""
                try:
                    prevedeny_text = r.recognize_google(zvukovy_soubor,language="cs")
                    self.gui.text_uzivatele.configure(text=prevedeny_text)
                except sr.UnknownValueError:
                    self.gui.text_uzivatele.configure(text="")
                    prevedeny_text = "Omlouvám se, ale nerozuměla jsem Tvému příkazu."
                except sr.RequestError:
                    self.gui.text_uzivatele.configure(text="")
                    prevedeny_text = "Omlouvám se, ale systém není momentálně funkční."
                return prevedeny_text     
        except:
            prevedeny_text = "Omlouvám se, ale mikrofon nebyl nalezen"
            self.gui.text_uzivatele.configure(text="")
            self.gui.text_sary.configure(text=prevedeny_text)
            self.mluv(prevedeny_text)
            return ""
                
    
    def hlavni_kod(self): # Smyčka, která se opakuje do nekonečna a tvoří hlavní kostru kódu
        self.prvni_kontakt_2()
        self.gui.prechod_obrazovky(self.gui.zakladni_obrazovka)
        self.mluv("Vítám tě "+self.gui.jmeno.get(),False)  
        while True:
            aktivator = self.aktivator_sary()
            if aktivator or self.kontrolni_bool: # Pokud uživatel řekne poslouchej, Sára začne poslouchat
                self.kontrolni_bool = 0
                self.mluv("Jsem připravena poslouchat")
                for i in range(3): # Uživatel má 3 pokusy na zadání příkazu
                    prikaz_uzivatele = self.zvuk_na_text()
                    if prikaz_uzivatele == "Omlouvám se, ale nerozuměla jsem Tvému příkazu.":
                        self.mluv(prikaz_uzivatele + " Zkus zadat příkaz znova")
                    elif prikaz_uzivatele == "Omlouvám se, ale systém není momentálně funkční.":  
                        self.mluv(prikaz_uzivatele + " Zkus mě použít později")
                    else:
                        self.gui.text_uzivatele.configure(text=prikaz_uzivatele)   
                        self.prikazy.jedno_prikazy(str(prikaz_uzivatele).lower())
                        if self.prikazy.kontrolka:
                            self.mluv("Omlouvám se, ale daný příkaz jsem nenašla. Zkus příkaz zadat znova")
                        else:
                            break
                if self.gui.promenna_ukladani_do_spanku.get(): # Sára oznámí, že přichází do spánku a je třeba ji aktivovat pomocí hlasového příkazu "poslouchej"
                    self.mluv("Ukládám se ke spánku")  

    
    def prvni_kontakt_2(self): # Slouží pro prvotní kontakt s uživatelem
        t = self.prvni_kontakt_1()
        if t:
            self.gui.prechod_obrazovky(self.gui.uvodni_okno)
            self.mluv("Ahoj, my se ještě neznáme, já jsem Sára, Tvůj nový virtuální asistent. Prosím sděl mi, jak se jmenuješ",False)
            while True:
                if self.kontrolni_bool == 1:
                    self.kontrolni_bool = 0
                    jmeno = self.gui.jmeno.get()
                    if len(jmeno) >= 1 and len(jmeno) <= 15 and "#" not in jmeno and "=" not in jmeno:
                        self.gui.jmeno.set(jmeno)
                        with open("data/konfiguracni_data/jmeno.txt","w",encoding="utf-8") as soubor:
                            soubor.write("jmeno="+jmeno) 
                        break
                        
                    else:
                        self.mluv("Omlouvám se, ale délka tvého jména musí být větší než 0 a menší než 16. Zároveň nesmí obsahovat znak #, nebo =", False)
                if self.kontrolni_bool == 2:
                    self.kontrolni_bool = 0
                    self.mluv(self.gui.jmeno.get(),False)
        else:
            pass                 
    def prvni_kontakt_1(self): # Slouží pro prvotní kontakt s uživatelem
        try:
            with open("data/konfiguracni_data/jmeno.txt","r",encoding="utf-8") as soubor:
                for radek in soubor.readlines(): 
                    if "jmeno=" in radek.strip():
                        schranka = radek.strip().split("=")
                if schranka[0]=="jmeno" and schranka[1] == "#":
                    return 1
                else:
                    self.gui.jmeno.set(schranka[1])
                    return 0
                                        
        except:
            with open("data/konfiguracni_data/jmeno.txt","w",encoding="utf-8") as soubor:   
                soubor.write("jmeno=#")  
                return 1
    
                
              
            
        