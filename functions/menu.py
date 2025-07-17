from datetime import datetime
import locale
import time
from fpdf import FPDF
import os
from functions.manipe import (
    afficher_clients,
    afficher_produits,
    afficher_cartes_reduction,
   
)


#Menu principal
def menu():
    print("1-Consulter un fichier")
    print("2-Générer une facture")
    print("3-Ajouter un produit")
    print("4-Quitter l'application")

def choice(choix):
    if choix == 1:
        print("a.Afficher les clients")
        print("b.Afficher les produits")
        print("c.Afficher les cartes de réduction")
    elif choix == 2:
        CreateFacture()
    elif choix == 3:
        print("Permet d’ajouter un nouveau produit au fichier Produits.")
    elif choix == 4:
        print("Quitter APK")
    else: 
        print("Entrée invalide")

def rechoice(choix):
    if choix =="a":
        # print("afficher les clients")
        afficher_clients()
    elif choix == "b":
        # print("afficher les produits")
        afficher_produits()
    elif choix == "c":
        # print("Afficher les cartes de reduction")
        afficher_cartes_reduction()
    else:
        print("Entrée invalide")


def factureId():
    timestamp = int(time.time())
    return f"{timestamp}"


def CreateFacture():
    locale.setlocale(locale.LC_TIME, 'French_France.1252')
    date = datetime.now()
    format = "%A %d %B %Y à %H:%M:%S"
    Nom = "FacturaPy"
    DeliveryDate = date.strftime(format)
    IdFacture = factureId()
    
    if not os.path.exists("Factures"):
        os.makedirs("Factures")
    
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", "I", size=13)
    pdf.cell(90, 10, txt=Nom, ln=0, align='L')
    
    pdf.set_font("Arial", "I", size=12)
    pdf.cell(100, 10, txt=f"Délivré le : {DeliveryDate}", ln=1, align='R')
    
    pdf.ln(10)
    
    pdf.set_font("Arial", "I", size=12)
    pdf.cell(170, 10, txt=f"Facture n° : {IdFacture}", ln=1, align='C')
    
    pdf.ln(15)
    
    pdf.set_font("Arial", "B", size=10)
    pdf.cell(20, 10, txt="N°", border=1, ln=0, align='C')
    pdf.cell(30, 10, txt="Code Produit", border=1, ln=0, align='C')
    pdf.cell(60, 10, txt="Libellé", border=1, ln=0, align='C')
    pdf.cell(25, 10, txt="P.U.", border=1, ln=0, align='C')
    pdf.cell(25, 10, txt="Qté", border=1, ln=0, align='C')
    pdf.cell(30, 10, txt="Total HT", border=1, ln=1, align='C')
    
    pdf.set_font("Arial", size=10)
    for i in range(4):
        pdf.cell(20, 10, txt="", border=1, ln=0, align='C')
        pdf.cell(30, 10, txt="", border=1, ln=0, align='C')
        pdf.cell(60, 10, txt="", border=1, ln=0, align='C')
        pdf.cell(25, 10, txt="", border=1, ln=0, align='C')
        pdf.cell(25, 10, txt="", border=1, ln=0, align='C')
        pdf.cell(30, 10, txt="", border=1, ln=1, align='C')
    
    pdf.set_font("Arial", "B", size=10)
    
    pdf.cell(135, 10, txt="", border=0, ln=0)  
    pdf.cell(25, 10, txt="Total HT", border=1, ln=0, align='C')
    pdf.cell(30, 10, txt="", border=1, ln=1, align='C')
    
    pdf.cell(135, 10, txt="", border=0, ln=0)
    pdf.cell(25, 10, txt="Remise", border=1, ln=0, align='C')
    pdf.cell(30, 10, txt="", border=1, ln=1, align='C')
    
    pdf.cell(135, 10, txt="", border=0, ln=0)
    pdf.cell(25, 10, txt="THT remise", border=1, ln=0, align='C')
    pdf.cell(30, 10, txt="", border=1, ln=1, align='C')
    
    pdf.cell(135, 10, txt="", border=0, ln=0)
    pdf.cell(25, 10, txt="TVA(18%)", border=1, ln=0, align='C')
    pdf.cell(30, 10, txt="", border=1, ln=1, align='C')
    
    pdf.cell(135, 10, txt="", border=0, ln=0)
    pdf.cell(25, 10, txt="Total TTC", border=1, ln=0, align='C')
    pdf.cell(30, 10, txt="", border=1, ln=1, align='C')
    
    pdf.ln(10)
    
    pdf.set_font("Arial", "I", size=10)
    pdf.cell(190, 10, txt="Arrêtée, la présente facture à la somme de : [Total TTC en lettres]", ln=1, align='L')
    
    filename = f"Factures/Facture_{IdFacture}.pdf"
    pdf.output(filename)
    
    print(f"Facture sauvegardée dans : {filename}")
    return filename