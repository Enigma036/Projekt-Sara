import os
from sys import stderr, stdin, stdout
from nacteni_ze_souboru import Nacitani
import webbrowser as wb
import subprocess
from datetime import datetime
from subprocess import PIPE
from seznam_prikazu_zapni import SeznamZapni
from seznam_prikazu_vlastni_prikaz import SeznamVlastniPrikaz
from mp3 import MP3
import wikipedia

class Prikazy:
    def __init__(self,asistent):
        self.nacitani = Nacitani(self)
        self.hudba = MP3(self)
        self.asistent = asistent
        self.nastaveni_prechod_oken = 0
        self.pomocna_hodnota_1 = 0
        
        self.kontrolka = 1
        
    def vlastni_prikazy(self, puvodni_zvuk): # Načte vlastní příkazy
        nazev, prikaz = self.nacitani.nacti_ze_vlastni_prikazy()
        for cislo in range(len(nazev)):
            if puvodni_zvuk == nazev[cislo]:
                self.kontrolka = 0
                if self.asistent.gui.promenna_zachovani_cmd_vlastni_prikaz.get():
                    os.system(f"start cmd /k {prikaz[cislo]}")
                else:
                    os.system(f"start cmd /c {prikaz[cislo]}")
                break
        
    def jedno_prikazy(self,puvodni_zvuk):
        try:
            zvuk_zdroj = puvodni_zvuk.split(" ",1)
        except:
            pass
        self.kontrolka = 1
        
        # Příkaz zapni
        if len(zvuk_zdroj) == 2 and zvuk_zdroj[0] == "zapni": 
            self.kontrolka = 0
            spravny_prikaz = 0
            nazev, cesta = self.nacitani.nacti_ze_zapni()
            for cislo in range(len(nazev)):
                try:
                    if zvuk_zdroj[1] == nazev[cislo]:
                        spravny_prikaz = 1
                        try:
                            if "\\" not in cesta[cislo] and "/" not in cesta[cislo]:
                                os.startfile(cesta[cislo])
                            else:
                                subprocess.Popen([cesta[cislo]], stdout=PIPE, stderr=PIPE)
                        except:
                            os.startfile(cesta[cislo])                
                        self.asistent.mluv("Zapínám "+nazev[cislo])    
                except:
                    self.asistent.mluv("Omlouvám se, ale nemohla jsem otevřít Vaši aplikaci")   
            if not spravny_prikaz:
                self.asistent.mluv("Omlouvám se, ale nenašla jsem Tvoji aplikaci")
                
        # Vyhledej na internetu 
        elif len(zvuk_zdroj) == 2 and zvuk_zdroj[0] == "vyhledej":
            self.kontrolka = 0
            if zvuk_zdroj[1] not in " " and "www." in zvuk_zdroj[1] and len(zvuk_zdroj[1])>4: # Kdyby to byla nějaké stránka, ať se snaží vyhledat přímo
                url = zvuk_zdroj[1]
            else:    
                url = "https://www.google.com/search?q=" + zvuk_zdroj[1]
            wb.get().open(url) # Otevře nové okno s výsledkem hledání
            self.asistent.mluv("Tohle jsem vyhledala")
        
        # Najdi lokalitu
        elif len(zvuk_zdroj) == 2 and zvuk_zdroj[0] == "najdi":
            self.kontrolka = 0
            url = "https://www.google.com/maps/place/" + zvuk_zdroj[1] + "/&amp;" 
            wb.get().open(url) # Otevře nové okno s výsledkem hledání
            self.asistent.mluv("Našla jsem tohle místo")    
        
        # Vypočítá příklad
        elif len(zvuk_zdroj) == 2 and zvuk_zdroj[0] == "vypočítej":
            self.kontrolka = 0
            seznam_cisel = ["nula","jedna","dva","tři","čtyři","pět","šest","sedm","osm","devět"]
            priklad = str(zvuk_zdroj[1]).lower()
            for cislo in seznam_cisel:
                if cislo in seznam_cisel:
                    priklad = priklad.replace(cislo,str(seznam_cisel.index(cislo)))
            if "děleno" in priklad:
                priklad = priklad.replace("děleno","/")
            if "krát" in priklad:
                priklad = priklad.replace("krát","*")
            if "x" in priklad:
                priklad = priklad.replace("x","*")                
            if "plus" in priklad:
                priklad = priklad.replace("plus","+")
            if "mínus" in priklad:
                priklad = priklad.replace("mínus","-")  
            try:
                vysledek = eval(priklad)
                self.asistent.mluv(f"Výsledek příkladu je {vysledek}") 
            except:           
                self.asistent.mluv("Byly zadány špatné argumenty") 
                
        # Příkaz nastavení        
        elif zvuk_zdroj[0] == "nastavení":
            self.nastaveni_prechod_oken = 2
            self.kontrolka = 0
            self.asistent.gui.prechod_obrazovky(self.asistent.gui.hlacni_nastavovaci_frame)
            self.asistent.gui.prechod_obrazovky(self.asistent.gui.pravy_frame_hlavni_nastaveni)
            self.asistent.mluv("Otevírám nastavení") 
            self.pomocna_hodnota_1 = 0
            while True: # Dokud neklikne na "zpět". Jakmile klikne, použije break
                if self.nastaveni_prechod_oken == 1:
                    self.nastaveni_prechod_oken = 0
                    self.asistent.gui.prechod_obrazovky(self.asistent.gui.zakladni_obrazovka)
                    break
                elif self.nastaveni_prechod_oken == 2:
                    if self.pomocna_hodnota_1 == 1:
                        self.pomocna_hodnota_1 = 0 
                        self.nacitani.uloz("data/konfiguracni_data/ukladani_ke_spanku.txt","ukladani_ke_spanku="+str(self.asistent.gui.promenna_ukladani_do_spanku.get()))
                    elif self.pomocna_hodnota_1 == 2:
                        self.pomocna_hodnota_1 = 0 
                        self.asistent.mluv(self.asistent.gui.jmeno_nove.get()) 
                    elif self.pomocna_hodnota_1 == 3:
                        self.pomocna_hodnota_1 = 0 
                        if len(self.asistent.gui.jmeno_nove.get()) >= 1 and len(self.asistent.gui.jmeno_nove.get()) <= 15 and "#" not in self.asistent.gui.jmeno_nove.get() and "=" not in self.asistent.gui.jmeno_nove.get():
                            self.asistent.gui.jmeno.set(self.asistent.gui.jmeno_nove.get())
                            with open("data/konfiguracni_data/jmeno.txt","w",encoding="utf-8") as soubor:
                                soubor.write("jmeno="+self.asistent.gui.jmeno_nove.get())  
                                self.asistent.mluv("Jméno je změněno")
                        else:
                            self.asistent.mluv("Omlouvám se, ale délka tvého jména musí být větší než 0 a menší než 16. Zároveň nesmí obsahovat znak #, nebo =",False)
                    elif self.pomocna_hodnota_1 == 4:  
                        self.pomocna_hodnota_1 = 0 
                        if "=" in self.asistent.gui.odkaz_na_hudbu.get():
                            self.asistent.mluv("Ve jméně nesmí být znak rovná se")
                        else:
                            self.nacitani.uloz("data/konfiguracni_data/cesta_k_hudbe.txt","cesta_k_hudbe="+str(self.asistent.gui.odkaz_na_hudbu.get()))
                            self.asistent.mluv("Cesta byla úspěšně změněna")   
                    
                elif self.nastaveni_prechod_oken == 3:
                    if self.pomocna_hodnota_1 == 1:
                        self.pomocna_hodnota_1 = 0 
                        try:
                            self.zapni_okno = SeznamZapni(self)
                        except:
                            pass
                    elif self.pomocna_hodnota_1 == 2:
                        self.pomocna_hodnota_1 = 0 
                        nazev, cesta = self.nacitani.nacti_ze_zapni()
                        if self.asistent.gui.nazev_noveho_prikazu.get().lower() in nazev:
                            self.asistent.mluv("Název aplikace je již zabrán. Můžete aplikaci pod stejným názvem nejprve odebrat a znovu vložit s jinou cestou",False)
                        elif "#" in self.asistent.gui.nazev_noveho_prikazu.get().lower()  or "#" in self.asistent.gui.zapni_cesta_k_aplikaci.get().lower():
                            self.asistent.mluv("V názvu aplikace nebo v cestě k aplikaci nesmí být znak #",False)
                        elif (self.asistent.gui.nazev_noveho_prikazu.get().isspace() or self.asistent.gui.zapni_cesta_k_aplikaci.get().isspace()) or (self.asistent.gui.nazev_noveho_prikazu.get() == "" or self.asistent.gui.zapni_cesta_k_aplikaci.get() == ""):
                            self.asistent.mluv("Nesmíte vložit prázdný název nebo cestu",False)
                        else:
                            nazev.append(self.asistent.gui.nazev_noveho_prikazu.get().lower())
                            cesta.append(self.asistent.gui.zapni_cesta_k_aplikaci.get().lower())
                            self.asistent.gui.nazev_noveho_prikazu.set("")
                            self.asistent.gui.zapni_cesta_k_aplikaci.set("")
                            self.nacitani.uloz_do_zapni(nazev,cesta)
                            self.asistent.mluv("Aplikace byla úspěšně vložena",False)           
                elif self.nastaveni_prechod_oken == 4:
                    if self.pomocna_hodnota_1 == 1:
                        self.pomocna_hodnota_1 = 0
                        self.nacitani.uloz("data/konfiguracni_data/zachovani_cmd.txt","zachovani_cmd="+str(self.asistent.gui.promenna_zachovani_cmd_vlastni_prikaz.get()))
                    elif self.pomocna_hodnota_1 == 2:
                        self.pomocna_hodnota_1 = 0
                        try:
                            self.zapni_okno = SeznamVlastniPrikaz(self)
                        except:
                            pass    
                    elif self.pomocna_hodnota_1 == 3:
                        self.pomocna_hodnota_1 = 0
                        nazev, prikaz = self.nacitani.nacti_ze_vlastni_prikazy()
                        if self.asistent.gui.nazev_noveho_prikazu_vlastni_prikaz.get().lower() in nazev:
                            self.asistent.mluv("Název příkazu je již zabrán. Můžete příkaz pod stejným názvem nejprve odebrat a znovu jej vložit")
                        elif "#" in self.asistent.gui.nazev_noveho_prikazu_vlastni_prikaz.get().lower()  or "#" in self.asistent.gui.samotny_prikaz_vlastni_prikaz.get().lower():
                            self.asistent.mluv("V názvu příkazu nebo v samotném příkazu nesmí být znak #")    
                        elif (self.asistent.gui.nazev_noveho_prikazu_vlastni_prikaz.get().isspace() or self.asistent.gui.samotny_prikaz_vlastni_prikaz.get().isspace()) or (self.asistent.gui.nazev_noveho_prikazu_vlastni_prikaz.get() == "" or self.asistent.gui.samotny_prikaz_vlastni_prikaz.get() == ""):
                            self.asistent.mluv("Nesmíte vložit prázdný název nebo příkaz")           
                        elif self.asistent.gui.nazev_noveho_prikazu_vlastni_prikaz.get().lower() in self.nacitani.puvodni_prikazy:
                            self.asistent.mluv("Nemůžete vkládat systémové příkazy jako je zapni, vyhledej a další")
                        else:
                            nazev.append(self.asistent.gui.nazev_noveho_prikazu_vlastni_prikaz.get().lower())
                            prikaz.append(self.asistent.gui.samotny_prikaz_vlastni_prikaz.get().lower())
                            self.asistent.gui.nazev_noveho_prikazu_vlastni_prikaz.set("")
                            self.asistent.gui.samotny_prikaz_vlastni_prikaz.set("")
                            self.nacitani.uloz_do_vlastni_prikaz(nazev,prikaz)
                            self.asistent.mluv("Příkaz byl úspěšně vložen")
            self.nastaveni_prechod_oken = 0  
             
        # Příkaz řekni
        elif len(zvuk_zdroj) == 2 and zvuk_zdroj[0] == "řekni":
            self.kontrolka = 0
            self.asistent.mluv(zvuk_zdroj[1])
            
        # Příkaz informace
        elif len(zvuk_zdroj) == 2 and zvuk_zdroj[0] == "informace": 
            self.kontrolka = 0
            try:
                wikipedia.set_lang("cs")
                url = wikipedia.page(wikipedia.search(zvuk_zdroj[1])[0], auto_suggest=False).url # Zjistí url wikipedia stránky
            except:
                url = zvuk_zdroj[1]
            wb.get().open(url)
            self.asistent.mluv("Tady jsou nějaké informace")       
        
        # Příkaz hudba
        elif len(zvuk_zdroj) == 2 and zvuk_zdroj[0] == "hudba":
            self.kontrolka = 0
            self.novy_nazev = []
            
            try:
                nazev, cesta = self.hudba.nacti_pisnicky()
                for song in nazev:
                    self.novy_nazev.append(str(song).lower())
            except:
                self.novy_nazev = []
                
            if zvuk_zdroj[1] == "spustit" or zvuk_zdroj[1] == "spusti":
                self.hudba.hrej_song()
            elif zvuk_zdroj[1] == "zastav" or zvuk_zdroj[1] == "zastavit":    
                self.hudba.pauza_song()
            elif zvuk_zdroj[1] == "pokračuj" or zvuk_zdroj[1] == "pokračuj v poslechu" or  zvuk_zdroj[1] == "pokračovat":  
                self.hudba.pokracovat_song()
            elif zvuk_zdroj[1] == "přeskočit dopředu" or zvuk_zdroj[1] == "přeskoč dopředu" or zvuk_zdroj[1] == "přeskočí dopředu" or zvuk_zdroj[1] == "přeskočili dopředu":  
                self.hudba.preskocit_dopredu_song()    
            elif zvuk_zdroj[1] == "přeskočit dozadu" or zvuk_zdroj[1] == "přeskoč dozadu" or zvuk_zdroj[1] == "přeskočí dozadu" or zvuk_zdroj[1] == "přeskočili dozadu":  
                self.hudba.preskocit_dozadu_song()  
            elif zvuk_zdroj[1] == "playlist":  
                self.hudba.playlist()
            elif zvuk_zdroj[1] in self.novy_nazev and len(zvuk_zdroj[1]) > 0:
                self.hudba.poradi_songy = self.novy_nazev.index(zvuk_zdroj[1]) 
                self.hudba.hrej_song()
            else:
                self.asistent.mluv("V příkazu hudba jsem nenašla zadaný argument")             
        
        else:
            self.dalsi_prikazy(puvodni_zvuk)
                         
                         
    # Příkazy, které již nepotřebují argument
    def dalsi_prikazy(self,puvodni_zvuk):
        if puvodni_zvuk == "vypni se" or puvodni_zvuk == "vypni program":
            self.kontrolka=0
            self.asistent.mluv("Na viděnou")
            self.asistent.gui.vypni_se()
        elif puvodni_zvuk == "čas" or puvodni_zvuk == "kolik je hodin" or puvodni_zvuk == "jaký je čas":
            self.kontrolka=0
            text = ""
            aktualni_cas = (datetime.now()).strftime("%H:%M")
            hodiny,minuty = map(int,aktualni_cas.split(":"))
            if hodiny == 1:
                text += "1 hodina a "
            elif hodiny == 2 or hodiny == 3 or hodiny == 4:
                text += f"{hodiny} hodiny a "
            else:
                text += f"{hodiny} hodin a "
            if minuty == 1:
                text += "1 minuta"
            elif minuty == 2 or minuty == 3 or minuty == 4:
                text += f"{minuty} minuty"
            else:
                text += f"{minuty} minut"
            self.asistent.mluv("Je "+text)
            text=""    
        elif puvodni_zvuk == "jak se máš" or puvodni_zvuk == "jak se daří" or puvodni_zvuk == "jak je":
            self.kontrolka = 0
            self.asistent.mluv("Moje nálada je vždy neutrální")    
        elif puvodni_zvuk == "kdo tě vytvořil":
            self.kontrolka = 0
            self.asistent.mluv("Naprogramoval mě Tomáš Hanák")   
        
        else:
            self.vlastni_prikazy(puvodni_zvuk)           
            
            
                      
                
                         
            
            
            