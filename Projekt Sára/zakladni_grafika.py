from asistent import Asistent
import tkinter as tk
from PIL import ImageTk, Image
from threading import Thread, Event
import os
import tkinter as tk
import playsound
import speech_recognition as sr
from gtts import gTTS
from tkinter import filedialog
from tkinter import ttk




class ZakladniOkno:
    def __init__(self):

        # Základní okno, pro načtení základní grafiky
        self.root = tk.Tk()
        self.jmeno=tk.StringVar() # Jméno uživatele  
        self.root.resizable(width=False, height=False) # Zamezí zvětšování/zmenšování aplikace
        self.root.title("Projekt Sára")
        self.root.iconbitmap("data/ikona/ikona.ico")
        self.root.configure(bg="white")
        self.root.geometry("468x332")
        
        self.zakladni_obrazovka = tk.Frame(self.root,bg="white",width=468,height=332)
        self.logo_sary = Image.open("data/obrazky/logo.png")
        self.logo_sary = self.logo_sary.resize((150,150))
        self.logo_sary = ImageTk.PhotoImage(self.logo_sary)
        self.tlacitko_zakladni = tk.Button(self.zakladni_obrazovka, image=self.logo_sary,borderwidth=0,bg="white",anchor="center",command=lambda:self.zmena_hodnoty(1))
               
        self.jmeno_sary = tk.Label(self.zakladni_obrazovka,text="Sára",bg="white",fg = "#ff6600",font=("Arial",15,"italic"),anchor="w")
        self.jmeno_uzivatele = tk.Label(self.zakladni_obrazovka,textvariable=self.jmeno,bg="white",fg = "black",font=("Arial",15,"italic"),anchor="e")
        
        self.text_sary = tk.Label(self.zakladni_obrazovka,text="Řekni \"poslouchej\", nebo zmáčkni tlačítko, a aktivuj mě",bg="#ff6600",fg="white",height=3,width=56,font=("Arial",10),borderwidth=2,relief="solid")
        self.text_uzivatele = tk.Label(self.zakladni_obrazovka,text="",bg="white",fg="black",height=3,width=50,font=("Arial",10),borderwidth=2,relief="solid")
        
        self.jmeno_sary.grid(column=1,row=1,sticky="we",padx=6)
        self.text_sary.grid(column=1,row=2,sticky="we",columnspan=3,padx=6)
        self.jmeno_uzivatele.grid(column=3,row=3,sticky="we",padx=6)
        self.text_uzivatele.grid(column=1,row=4,sticky="we",columnspan=3,padx=6)
        self.tlacitko_zakladni.grid(column=1,row=5,columnspan=3)
        
        self.uvodni_obrazovka()
        self.zakladni_obrazovka.grid(column=1,row=1,sticky="nswe")
        self.prechod_obrazovky(self.zakladni_obrazovka)
        self.nastaveni_okno()
        
        self.asistent = Asistent(self) # Inicializuje asistenta - Předám self aby probíhala komunikace mezi vlákny
        self.vlakno = Thread(target=self.asistent.hlavni_kod,daemon=True) # Zapne vlákno pro asistenta s tím, aby po ukončení hlavního okna se i asistent vypnul
        self.vlakno.start() # Aktivuje vlákno. Následné GUI bude ovládat asistent pro lepší komunikaci
        self.root.mainloop()
        
    def prechod_obrazovky(self,obrazovka): # Umožní nám měnit snímky
        obrazovka.tkraise()
        
    def zmena_hodnoty(self,hodnota): # Změní hodnoty, pro kontrolni bod
        self.asistent.kontrolni_bool=hodnota    
        
    def zmena_hodnoty_pro_nastaveni(self,promenna,hodnota): # Změníme hodnoty nastavení asistenta
        if promenna == "zavri":
            self.asistent.prikazy.nastaveni_prechod_oken = hodnota
        elif promenna == "okno 1":
            self.asistent.prikazy.nastaveni_prechod_oken = hodnota
            self.prechod_obrazovky(self.pravy_frame_hlavni_nastaveni)
        elif promenna == "okno 2":
            self.asistent.prikazy.nastaveni_prechod_oken = hodnota
            self.prechod_obrazovky(self.pravy_frame_prikaz_zapni)    
        elif promenna == "okno 3":
            self.asistent.prikazy.nastaveni_prechod_oken = hodnota
            self.prechod_obrazovky(self.pravy_frame_prikaz_vlastni)
        elif promenna == "pomocna":  
            self.asistent.prikazy.pomocna_hodnota_1 = hodnota               
            
    def nacteni_slozky_pro_hudbu(self): # Umožní nám vybrat složku pro uložení hudby
        try:
            nazev_slozky = filedialog.askdirectory()
            self.odkaz_na_hudbu.set(str(nazev_slozky))
        except:
            self.odkaz_na_hudbu.set("")
        if self.odkaz_na_hudbu.get().isspace():
            self.odkaz_na_hudbu.set("")
    
    def nacteni_cesty_k_aplikaci(self): # Umožní nám vybrat aplikaci
        try:
            cesta_k_aplikaci = filedialog.askopenfilename(filetypes=(("Spustitelné soubory","*.exe"),("Všechny soubory","*.*")))
            self.zapni_cesta_k_aplikaci.set(str(cesta_k_aplikaci))    
        except:
            self.zapni_cesta_k_aplikaci.set("")            
            
    def uvodni_obrazovka(self): # Obrazovka, která se objeví při prvním kontaktu s uživatelem
        self.uvodni_okno = tk.Frame(self.root,bg="white")
        self.zadavani_jmena = tk.Entry(self.uvodni_okno,textvariable=self.jmeno,justify="center",bg="#ff6600",fg="white",width=25,font=("Arial",20),borderwidth=2,relief="solid")
        self.jmeno.set("Zde zadej své jméno")
        self.logo_reproduktoru = Image.open("data/obrazky/reproduktor.png")
        self.logo_reproduktoru = ImageTk.PhotoImage(self.logo_reproduktoru)
        
        self.tlacitko_reproduktoru = tk.Button(self.uvodni_okno,borderwidth=0,bg="white",image=self.logo_reproduktoru,command=lambda:self.zmena_hodnoty(2))
        
        self.logo_potvrdit = Image.open("data/obrazky/tlacitko_potrvd.png")
        self.logo_potvrdit= self.logo_potvrdit.resize((175,75))
        self.logo_potvrdit= ImageTk.PhotoImage(self.logo_potvrdit)
        self.tlacitko_potvrdit = tk.Button(self.uvodni_okno,image=self.logo_potvrdit,bg="white",borderwidth=0,command=lambda:self.zmena_hodnoty(1))
        
        # Pro správné fungování jsem zde musel dát .place(), aby vše fungovalo, jak má, protože při pack nefungovaly určité funkce
        self.zadavani_jmena.place(x=234,y=100,anchor="center")
        self.tlacitko_reproduktoru.place(x=234,y=160,anchor="center")
        self.tlacitko_potvrdit.place(x=234,y=270,anchor="center")
        self.uvodni_okno.grid(column=1,row=1,sticky="nswe")
    
    def nastaveni_okno(self): # GUI pro nastavení
        self.hlacni_nastavovaci_frame = tk.Frame(self.root,bg="white")
        self.levy_frame = tk.Frame(self.hlacni_nastavovaci_frame,bg="white")
        self.pravy_frame_hlavni_nastaveni = tk.Frame(self.hlacni_nastavovaci_frame,bg="white")
        self.pravy_frame_prikaz_zapni = tk.Frame(self.hlacni_nastavovaci_frame,bg="white")
        self.pravy_frame_prikaz_vlastni = tk.Frame(self.hlacni_nastavovaci_frame,bg="white")
        
        
        # Leve tlacitko
        self.tlacitko_hlavni_nastaveni = tk.Button(self.levy_frame,text="Hlavní",bg="#ff6600",font=("Arial",12),borderwidth=2,relief="solid",command=lambda: self.zmena_hodnoty_pro_nastaveni("okno 1",2))
        self.tlacitko_prikaz_zapni = tk.Button(self.levy_frame,text="Příkaz zapni",bg="#ff6600",font=("Arial",12),borderwidth=2,relief="solid",command=lambda: self.zmena_hodnoty_pro_nastaveni("okno 2",3))
        self.tlacitko_prikaz_vlastni = tk.Button(self.levy_frame,text="Vlastní příkaz",bg="#ff6600",font=("Arial",12),borderwidth=2,relief="solid",command=lambda: self.zmena_hodnoty_pro_nastaveni("okno 3",4))
        self.tlacitko_zpet = tk.Button(self.levy_frame,text="Zpět",bg="#ff6600",font=("Arial",12),borderwidth=2,relief="solid",command=lambda: self.zmena_hodnoty_pro_nastaveni("zavri",1))
        
        self.tlacitko_hlavni_nastaveni.grid(column=1,row=1,sticky="nswe",padx=1,pady=1)
        self.tlacitko_prikaz_zapni.grid(column=1,row=2,sticky="nswe",padx=1,pady=1)
        self.tlacitko_prikaz_vlastni.grid(column=1,row=3,sticky="nswe",padx=1,pady=1)
        self.tlacitko_zpet.grid(column=1,row=4,sticky="nswe",padx=1,pady=(195,0))
        
        # Prave - Hlavni nastaveni
        self.text_hlavni_nastaveni = tk.Label(self.pravy_frame_hlavni_nastaveni,text="Hlavní nastavení",bg="white",font=("Arial",15))
        self.text_odchod_do_spanku = tk.Label(self.pravy_frame_hlavni_nastaveni,text="Chcete, aby Sára oznamovala ukladání do spánku?",bg="white",font=("Arial",10))
        self.promenna_ukladani_do_spanku = tk.IntVar()
        self.promenna_ukladani_do_spanku.set(1)
        self.checkbutton_ukladani_ke_spanku = tk.Checkbutton(self.pravy_frame_hlavni_nastaveni,variable=self.promenna_ukladani_do_spanku,onvalue=1,offvalue=0,bg="white",command=lambda: self.zmena_hodnoty_pro_nastaveni("pomocna",1))
        self.text_nazev_pro_zmenu_jmena = tk.Label(self.pravy_frame_hlavni_nastaveni,text="Změna jména",bg="white",font=("Arial",13),justify="left")
        
        self.logo_reproduktoru_2 = Image.open("data/obrazky/reproduktor.png")
        self.logo_reproduktoru_2 = self.logo_reproduktoru_2.resize((30,30))
        self.logo_reproduktoru_2 = ImageTk.PhotoImage(self.logo_reproduktoru_2)
        self.tlacitko_reproduktoru_2 = tk.Button(self.pravy_frame_hlavni_nastaveni,borderwidth=0,bg="white",image=self.logo_reproduktoru_2,command=lambda: self.zmena_hodnoty_pro_nastaveni("pomocna",2))
        
        self.jmeno_nove = tk.StringVar()
        self.jmeno_nove.set("Zadej nové jméno")
        self.zadavani_jmena_2 = tk.Entry(self.pravy_frame_hlavni_nastaveni,textvariable=self.jmeno_nove,justify="center",bg="#ff6600",fg="white",font=("Arial",10),borderwidth=2,relief="solid")
        self.tlacitko_potvrdit_2 = tk.Button(self.pravy_frame_hlavni_nastaveni,text="Potvrď",fg="white",bg="#ff6600",borderwidth=2,relief="solid",command=lambda: self.zmena_hodnoty_pro_nastaveni("pomocna",3))
        
        self.text_pro_změnu_slozky_na_hudbu = tk.Label(self.pravy_frame_hlavni_nastaveni,text="Umístění složky na hudbu",bg="white",font=("Arial",13),justify="left")
        self.odkaz_na_hudbu = tk.StringVar()
        self.odkaz_na_hudbu.set(os.getcwd().replace("\\","/")+"/hudba")
        self.zadavani_umisteni_hudby = tk.Entry(self.pravy_frame_hlavni_nastaveni,textvariable=self.odkaz_na_hudbu,justify="center",bg="#ff6600",fg="white",font=("Arial",10),borderwidth=2,relief="solid")
        self.tlacitko_vybrat_umisteni_hudby = tk.Button(self.pravy_frame_hlavni_nastaveni,text="Vyber umístění",fg="white",bg="#ff6600",borderwidth=2,relief="solid",command= self.nacteni_slozky_pro_hudbu)
        self.tlacitko_potvrdit_3 = tk.Button(self.pravy_frame_hlavni_nastaveni,text="Potvrď",fg="white",bg="#ff6600",borderwidth=2,relief="solid",command=lambda: self.zmena_hodnoty_pro_nastaveni("pomocna",4))
        
        self.text_hlavni_nastaveni.grid(column=1,row=1,sticky="we",pady=6,columnspan=2) 
        self.text_odchod_do_spanku.grid(column=1,row=2,pady=6)
        self.checkbutton_ukladani_ke_spanku.grid(column=2,row=2)
        self.text_nazev_pro_zmenu_jmena.grid(column=1,row=3,pady=(10,0),sticky="w")
        self.zadavani_jmena_2.grid(column=1,row=4,sticky="w")
        self.tlacitko_reproduktoru_2.grid(column=2,row=4,sticky="w")
        self.tlacitko_potvrdit_2.grid(column=1,row=5,sticky="w")
        self.text_pro_změnu_slozky_na_hudbu.grid(column=1,row=6,pady=(10,0),sticky="w")
        self.zadavani_umisteni_hudby.grid(column=1,row=7,columnspan=2,sticky="we")
        self.tlacitko_vybrat_umisteni_hudby.grid(column=1,row=8,sticky="w",pady=5)
        self.tlacitko_potvrdit_3.grid(column=1,row=8,sticky="w",pady=5,padx=95)
        
        # Prave - Příkaz zapni
        self.text_hlavni_prikaz_zapni = tk.Label(self.pravy_frame_prikaz_zapni,text="Příkaz zapni - přídávání a odebírání",bg="white",font=("Arial",15),width=30)
        self.text_nazev_noveho_prikazu = tk.Label(self.pravy_frame_prikaz_zapni,text="Název aplikace/souboru",bg="white",font=("Arial",12))
        
        self.nazev_noveho_prikazu = tk.StringVar()
        self.zadavani_nazvu_noveho_prikazu = tk.Entry(self.pravy_frame_prikaz_zapni,textvariable=self.nazev_noveho_prikazu,justify="center",bg="#ff6600",fg="white",font=("Arial",10),borderwidth=2,relief="solid")
        
        self.text_cesta_k_souboru = tk.Label(self.pravy_frame_prikaz_zapni,text="Cesta k aplikaci/souboru",bg="white",font=("Arial",12))
        
        self.zapni_cesta_k_aplikaci = tk.StringVar()
        self.zadavani_cesty_prikazu_zapni = tk.Entry(self.pravy_frame_prikaz_zapni,textvariable=self.zapni_cesta_k_aplikaci,justify="center",bg="#ff6600",fg="white",font=("Arial",10),borderwidth=2,relief="solid")
        
        self.tlacitko_najdi_cestu_zapni = tk.Button(self.pravy_frame_prikaz_zapni,text="Vyber aplikaci",fg="white",bg="#ff6600",borderwidth=2,relief="solid",command=lambda: self.nacteni_cesty_k_aplikaci())
        
        self.tlacitko_vsechny_aplikace_zapni = tk.Button(self.pravy_frame_prikaz_zapni,text="Všechny aplikace/soubory k příkazu zapni",fg="white",bg="#ff6600",borderwidth=2,relief="solid",command=lambda: self.zmena_hodnoty_pro_nastaveni("pomocna",1))
        self.tlacitko_potvrdit_zapni = tk.Button(self.pravy_frame_prikaz_zapni,text="Potvrď",fg="white",bg="#ff6600",borderwidth=2,relief="solid",command=lambda: self.zmena_hodnoty_pro_nastaveni("pomocna",2))
        
    
        self.text_hlavni_prikaz_zapni.grid(column=1,row=1,columnspan=2,sticky="we",pady=(6,50))
        self.text_nazev_noveho_prikazu.grid(column=1,row=2,columnspan=2,sticky="we",pady=3)  
        self.zadavani_nazvu_noveho_prikazu.grid(column=1,row=3,columnspan=2,sticky="we",pady=6)  
        self.text_cesta_k_souboru.grid(column=1,row=4,columnspan=2,sticky="we",pady=6) 
        self.zadavani_cesty_prikazu_zapni.grid(column=1,row=5,columnspan=2,sticky="we",pady=6) 
        self.tlacitko_najdi_cestu_zapni.grid(column=1,row=6,columnspan=2,pady=(6,20)) 
        self.tlacitko_vsechny_aplikace_zapni.grid(column=1,row=7,sticky="we",pady=6,padx=6) 
        self.tlacitko_potvrdit_zapni.grid(column=2,row=7,sticky="we",pady=6)
        
        # Prave - Vlastní příkaz
        self.text_hlavni_vlastni_prikaz = tk.Label(self.pravy_frame_prikaz_vlastni,text="Vlastní příkaz - přídávání a odebírání",bg="white",font=("Arial",15),width=30)
        self.text_zachovani_cmd_vlastni_prikaz = tk.Label(self.pravy_frame_prikaz_vlastni,text="Chcete, aby shell běžel i po vykonání příkazu?",bg="white",font=("Arial",10))
        
        self.promenna_zachovani_cmd_vlastni_prikaz = tk.IntVar()
        self.promenna_zachovani_cmd_vlastni_prikaz.set(1)
        self.checkbutton_zachovani_cmd_vlastni_prikaz = tk.Checkbutton(self.pravy_frame_prikaz_vlastni,variable=self.promenna_zachovani_cmd_vlastni_prikaz,onvalue=1,offvalue=0,bg="white",command=lambda: self.zmena_hodnoty_pro_nastaveni("pomocna",1))
        
        self.text_nazev_vlastni_prikaz = tk.Label(self.pravy_frame_prikaz_vlastni,text="Název příkazu",bg="white",font=("Arial",12))
        
        self.nazev_noveho_prikazu_vlastni_prikaz = tk.StringVar()
        self.entry_nazev_vlastni_prikaz = tk.Entry(self.pravy_frame_prikaz_vlastni,textvariable=self.nazev_noveho_prikazu_vlastni_prikaz,justify="center",bg="#ff6600",fg="white",font=("Arial",10),borderwidth=2,relief="solid")
        
        self.text_samotny_prikaz_vlastni_prikaz = tk.Label(self.pravy_frame_prikaz_vlastni,text="Samotný příkaz v CMD",bg="white",font=("Arial",12))
        
        self.samotny_prikaz_vlastni_prikaz = tk.StringVar()
        self.entry_samotny_prikaz_vlastni_prikaz = tk.Entry(self.pravy_frame_prikaz_vlastni,textvariable=self.samotny_prikaz_vlastni_prikaz,justify="center",bg="#ff6600",fg="white",font=("Arial",10),borderwidth=2,relief="solid")
        
        self.tlacitko_vsechny_prikazy_vlastni_prikaz = tk.Button(self.pravy_frame_prikaz_vlastni,text="Všechny příkazy",fg="white",bg="#ff6600",borderwidth=2,relief="solid",command=lambda: self.zmena_hodnoty_pro_nastaveni("pomocna",2))
        self.tlacitko_potvrdit_vlastni_prikaz = tk.Button(self.pravy_frame_prikaz_vlastni,text="Potvrď",fg="white",bg="#ff6600",borderwidth=2,relief="solid",command=lambda: self.zmena_hodnoty_pro_nastaveni("pomocna",3))
        
        self.text_hlavni_vlastni_prikaz.grid(column=1,row=1,sticky="we",columnspan=2,pady=(6,10))
        self.text_zachovani_cmd_vlastni_prikaz.grid(column=1,row=2,columnspan=2,pady=(0,35),sticky="w")
        self.checkbutton_zachovani_cmd_vlastni_prikaz.grid(column=2,row=2,columnspan=2,pady=(0,35),sticky="e")
        self.text_nazev_vlastni_prikaz.grid(column=1,row=3,sticky="we",columnspan=2,pady=6)
        self.entry_nazev_vlastni_prikaz.grid(column=1,row=4,sticky="we",columnspan=2,pady=6)
        self.text_samotny_prikaz_vlastni_prikaz.grid(column=1,row=5,columnspan=2,sticky="we",pady=6)
        self.entry_samotny_prikaz_vlastni_prikaz.grid(column=1,row=6,columnspan=2,sticky="we",pady=(6,20))
        self.tlacitko_vsechny_prikazy_vlastni_prikaz.grid(column=1,row=7,sticky="we",pady=6,padx=6) 
        self.tlacitko_potvrdit_vlastni_prikaz.grid(column=2,row=7,pady=6,sticky="we")
        
        
        
        # Grid hlavnich Framu
        self.hlacni_nastavovaci_frame.grid(column=1,row=1,sticky="nswe",columnspan=3)
        
        self.levy_frame.grid(column=1,row=1,sticky="nswe",padx=(0,15))
        self.pravy_frame_hlavni_nastaveni.grid(column=2,row=1,columnspan=2,sticky="nswe")
        self.pravy_frame_prikaz_zapni.grid(column=2,row=1,columnspan=2,sticky="nswe")
        self.pravy_frame_prikaz_vlastni.grid(column=2,row=1,columnspan=2,sticky="nswe")
  
        self.prechod_obrazovky(self.pravy_frame_hlavni_nastaveni)
        self.prechod_obrazovky(self.hlacni_nastavovaci_frame)
    
    def vypni_se(self): # Vypnutí aplikace
        self.root.destroy()    




