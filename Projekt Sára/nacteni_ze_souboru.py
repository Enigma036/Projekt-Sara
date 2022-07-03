import os

class Nacitani: # Knihovna pro načítání a zadávání příkazů
    def __init__(self,prikazy):
        self.prikazy = prikazy
        self.pocatecni_hodnoty = []
        # Příkazy, které nechceme, aby uživatel přepsal - Dvojitá pojistka
        self.puvodni_prikazy = ["zapni","vyhledej","najdi","vypočítej","nastavení","řekni","informace","hudba","vypni se","vypni program","čas","kolik je hodin","jaký je čas","jak se máš","jak se daří","jak je"]
        
    def nacti_ze_zapni(self):
        nazev_prikazu =  []
        samotny_prikaz = []
        with open("data/konfiguracni_data/zapni.txt","r",encoding="utf-8") as soubor:
            for radek in soubor.readlines():
                try:
                    rozdeleny_prikaz = radek.strip().split("#")
                    nazev_prikazu.append(rozdeleny_prikaz[1])
                    samotny_prikaz.append(rozdeleny_prikaz[0])
                except:
                    pass
        self.uloz_do_zapni(nazev_prikazu,samotny_prikaz)  
        return nazev_prikazu,samotny_prikaz
          
    def uloz_do_zapni(self,nazev,cesta):            
        with open("data/konfiguracni_data/zapni.txt","w",encoding="utf-8") as soubor:
            for cislo in range(len(nazev)):
                soubor.write(f"{cesta[cislo]}#{nazev[cislo]}\n")
                
    def uloz_do_vlastni_prikaz(self,nazev,cesta):
        with open("data/konfiguracni_data/vlastni_prikaz.txt","w",encoding="utf-8") as soubor:
            for cislo in range(len(nazev)):
                soubor.write(f"{cesta[cislo]}#{nazev[cislo]}\n")            
                        
    def nacti_ze_vlastni_prikazy(self):
        nazev_prikazu =  []
        samotny_prikaz = []
        with open("data/konfiguracni_data/vlastni_prikaz.txt","r",encoding="utf-8") as soubor:
            for radek in soubor.readlines():
                try:
                    rozdeleny_prikaz = radek.strip().split("#")
                    nazev_prikazu.append(rozdeleny_prikaz[1])
                    samotny_prikaz.append(rozdeleny_prikaz[0])
                except:
                    pass
        self.uloz_do_vlastni_prikaz(nazev_prikazu,samotny_prikaz)  
        return nazev_prikazu,samotny_prikaz   
    
    def uloz(self,misto,hodnota): # Načtení konfiguračních souboru
        with open(misto,"w",encoding="utf-8") as soubor:
            soubor.write(hodnota)
            
    def nejdriv_nacti(self): # Nejdřív načte základní konfigurační soubory a "pojistí se", aby uživatel do textového souboru nepsal nesmysly - Pokud napíše, obnoví se tovární nastavení
        opakovac = True
        
        while opakovac:
            opakovac = False
            
            try:
                with open("data/konfiguracni_data/ukladani_ke_spanku.txt","r",encoding="utf-8") as soubor_1:
                    for radek in soubor_1.readlines():
                        rozdeleny_prikaz = radek.strip().split("=")
                    if rozdeleny_prikaz[0] == "ukladani_ke_spanku":
                        self.prikazy.asistent.gui.promenna_ukladani_do_spanku.set(int(rozdeleny_prikaz[1]))
                    else:
                        with open("data/konfiguracni_data/ukladani_ke_spanku.txt","w",encoding="utf-8") as soubor_2:
                            soubor_2.write("ukladani_ke_spanku=1")
                            opakovac = True                   
            except:
                with open("data/konfiguracni_data/ukladani_ke_spanku.txt","w",encoding="utf-8") as soubor_3:
                    soubor_3.write("ukladani_ke_spanku=1")
                    opakovac = True  
            
            try:
                with open("data/konfiguracni_data/cesta_k_hudbe.txt","r",encoding="utf-8") as soubor_4:
                    for radek in soubor_4.readlines():
                        rozdeleny_prikaz = radek.strip().split("=")
                    if rozdeleny_prikaz[0] == "cesta_k_hudbe":
                        self.prikazy.asistent.gui.odkaz_na_hudbu.set(str(rozdeleny_prikaz[1]))
                    else:
                        with open("data/konfiguracni_data/cesta_k_hudbe.txt","w",encoding="utf-8") as soubor_5:
                            soubor_5.write("cesta_k_hudbe="+os.getcwd().replace("\\","/")+"/hudba")
                            opakovac = True                              
            except:
                with open("data/konfiguracni_data/cesta_k_hudbe.txt","w",encoding="utf-8") as soubor_6:
                    soubor_6.write("cesta_k_hudbe="+os.getcwd().replace("\\","/")+"/hudba")
                    opakovac = True                      
            
            try:
                with open("data/konfiguracni_data/zachovani_cmd.txt","r",encoding="utf-8") as soubor_7:
                    for radek in soubor_7.readlines():
                        rozdeleny_prikaz = radek.strip().split("=")
                    if rozdeleny_prikaz[0] == "zachovani_cmd":
                        self.prikazy.asistent.gui.promenna_zachovani_cmd_vlastni_prikaz.set(int(rozdeleny_prikaz[1]))
                    else:
                        with open("data/konfiguracni_data/zachovani_cmd.txt","w",encoding="utf-8") as soubor_8:
                            soubor_8.write("zachovani_cmd=1")
                            opakovac = True                              
            except:
                with open("data/konfiguracni_data/zachovani_cmd.txt","w",encoding="utf-8") as soubor_9:
                    soubor_9.write("zachovani_cmd=1")
                    opakovac = True  