import tkinter as tk
from tkinter import CENTER, ttk
from PIL import ImageFont


class SeznamZapni: # Nedělám to přes tkinter.Toplevel, protože aktuální způsob mi přijde lepší
    def __init__(self,prikazy):
        self.prikazy = prikazy
        
        self.cislo_polozky = -1

        self.root = tk.Tk()
        self.root.resizable(width=False, height=False) # Zamezí zvětšování/zmenšování aplikace
        self.root.iconbitmap("data/ikona/ikona.ico")        
        self.root.title("Projekt Sára")
        
        
        radky = ("nazev","cesta")
        self.menu = ttk.Treeview(self.root,columns=radky,show="headings")
        self.menu.heading("nazev",text="Název souboru")
        self.menu.heading("cesta",text="Cesta k aplikaci")
        self.nacti_ze_prikazu_zapni()

        self.menu.column("nazev",width=self.nejdelsi_znak_nazev+15)
        self.menu.column("cesta",width=self.nejdelsi_znak_cesta+15)
        
        self.tlacitko_odebrat = tk.Button(self.root,text="Odeber příkaz",fg="white",bg="#ff6600",borderwidth=2,relief="solid",width=13,command=self.odeber_aplikaci)
        self.tlacitko_odejdi = tk.Button(self.root,text="Odejdi",fg="white",bg="#ff6600",borderwidth=2,relief="solid",width=13,command=self.odejdi)
        
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.menu.yview)
        self.menu.configure(yscroll=scrollbar.set)
        self.menu.bind('<<TreeviewSelect>>', self.vyber_polozku)
        
        self.menu.grid(column=1,row=1,columnspan=2,sticky="nswe")
        self.tlacitko_odebrat.grid(column=1,row=2,pady=6)
        self.tlacitko_odejdi.grid(column=2,row=2,pady=6)
        scrollbar.grid(row=1, column=3, sticky='ns')
        
        self.root.mainloop()
    
    def vyber_polozku(self,event):
        self.cislo_polozky = self.menu.index(self.menu.selection())
        
    def odeber_aplikaci(self):
        if self.cislo_polozky == -1:
            pass
        else:
            self.nazev.pop(self.cislo_polozky)       
            self.cesta.pop(self.cislo_polozky) 
            self.prikazy.nacitani.uloz_do_zapni(self.nazev,self.cesta)
            for item in self.menu.get_children():
                self.menu.delete(item)
            self.nacti_ze_prikazu_zapni()
            self.cislo_polozky = -1
            

    
    def odejdi(self):
        self.root.destroy()    
        
    def nacti_ze_prikazu_zapni(self): 
        font = ImageFont.load_default() # Pro nalezení správné velikosti
        max_nazev = ""
        max_cesta = ""
        try:
            self.nazev, self.cesta = self.prikazy.nacitani.nacti_ze_zapni()
            # Jelikož má ImageFont problém, že neumí defaultně UTF-8, musel jsem šáhnout pro trochu jiné řešení
            max_nazev = "A"*len(max(self.nazev, key = len)) 
            max_cesta = "A"*len(max(self.cesta, key = len))
            
            self.nejdelsi_znak_nazev = font.getsize(max_nazev)[0]
            self.nejdelsi_znak_cesta = font.getsize(max_cesta)[0]
            
            if self.nejdelsi_znak_nazev < font.getsize("Název souboru")[0]:
                self.nejdelsi_znak_nazev = font.getsize("Název souboru")[0]
            if self.nejdelsi_znak_cesta < font.getsize("Cesta k aplikaci")[0]:
                self.nejdelsi_znak_cesta = font.getsize("Cesta k aplikaci")[0]
            
            for i in range(len(self.nazev)):
               self.menu.insert("",tk.END,values=(self.nazev[i],self.cesta[i]))  
        except:
            self.nejdelsi_znak_nazev = font.getsize("Název souboru")[0]
            self.nejdelsi_znak_cesta = font.getsize("Cesta k aplikaci")[0]
        
     
        