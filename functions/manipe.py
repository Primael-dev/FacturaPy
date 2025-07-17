import pandas as pd

# ----------- AFFICHAGE -----------

def afficher_clients():
    try:
        df = pd.read_excel("ExcelFiles/Clients.xlsx")
        print("\nListe des clients :")
        print(df)
    except Exception as e:
        print("Erreur lors de la lecture de Clients.xlsx :", e)

def afficher_produits():
    try:
        df = pd.read_excel("ExcelFiles/Produits.xlsx")
        print("\nListe des produits :")
        print(df)
    except Exception as e:
        print("Erreur lors de la lecture de Produits.xlsx :", e)

def afficher_cartes_reduction():
    try:
        df = pd.read_excel("ExcelFiles/CartesReduction.xlsx")
        print("\nListe des cartes de réduction :")
        print(df)
    except Exception as e:
        print("Erreur lors de la lecture de CartesReduction.xlsx :", e)

# ----------- AJOUT -----------

# tsss c'est tout ??? 
# rien d'interessant 