from datetime import datetime
import locale
import time
from fpdf import FPDF
import os
import pandas as pd
from functions.manipe import (
    afficher_clients,
    afficher_produits,
    afficher_cartes_reduction,
)

from functions.ajout import (
   ajouter_client,
   ajouter_produit 
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
        # print("Permet d'ajouter un nouveau produit au fichier Produits.")
        ajouter_produit()
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


def nombre_en_lettres(nombre):
    """Convertit un nombre en lettres (version simplifiée)"""
    unites = ["", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf"]
    dizaines = ["", "", "vingt", "trente", "quarante", "cinquante", "soixante", "soixante-dix", "quatre-vingt", "quatre-vingt-dix"]
    
    if nombre == 0:
        return "zéro"
    
    if nombre < 10:
        return unites[nombre]
    elif nombre < 20:
        teens = ["dix", "onze", "douze", "treize", "quatorze", "quinze", "seize", "dix-sept", "dix-huit", "dix-neuf"]
        return teens[nombre - 10]
    elif nombre < 100:
        dizaine = nombre // 10
        unite = nombre % 10
        if unite == 0:
            return dizaines[dizaine]
        else:
            return dizaines[dizaine] + "-" + unites[unite]
    elif nombre < 1000:
        centaine = nombre // 100
        reste = nombre % 100
        result = unites[centaine] + " cent"
        if reste > 0:
            result += " " + nombre_en_lettres(reste)
        return result
    else:
        # Pour les nombres plus grands, version simplifiée
        return f"{nombre} "


def verifier_carte_reduction(code_client):
    """Vérifie si un client a une carte de réduction"""
    try:
        cartes = pd.read_excel("ExcelFiles/CartesReduction.xlsx")
        carte_client = cartes[cartes['code_client'] == code_client]
        if not carte_client.empty:
            return carte_client.iloc[0]['taux_reduction']
        return 0
    except:
        return 0


def creer_carte_reduction(code_client, montant_facture):
    """Crée une carte de réduction si le montant le justifie"""
    try:
        cartes = pd.read_excel("ExcelFiles/CartesReduction.xlsx")
    except:
        cartes = pd.DataFrame(columns=["numero_carte", "code_client", "taux_reduction"])
    
    # Vérifier si le client a déjà une carte
    if code_client in cartes['code_client'].values:
        return
    
    # Définir les plages de remise
    taux_reduction = 0
    if montant_facture >= 100000:  # 100 000 FCFA
        taux_reduction = 10
    elif montant_facture >= 50000:   # 50 000 FCFA
        taux_reduction = 5
    elif montant_facture >= 25000:   # 25 000 FCFA
        taux_reduction = 3
    
    if taux_reduction > 0:
        # Générer un numéro de carte unique
        numero_carte = f"CARD{int(time.time())}"
        
        nouvelle_carte = pd.DataFrame([[numero_carte, code_client, taux_reduction]], 
                                    columns=cartes.columns)
        cartes = pd.concat([cartes, nouvelle_carte], ignore_index=True)
        cartes.to_excel("ExcelFiles/CartesReduction.xlsx", index=False)
        print(f"Carte de réduction créée ! Taux : {taux_reduction}%")


def CreateFacture():
    try:
        locale.setlocale(locale.LC_TIME, 'French_France.1252')
    except:
        pass  # Si la locale française n'est pas disponible
    
    date = datetime.now()
    format = "%A %d %B %Y à %H:%M:%S"
    Nom = "FacturaPy"
    DeliveryDate = date.strftime(format)
    IdFacture = factureId()
    
    # Charger les données
    try:
        clients = pd.read_excel("ExcelFiles/Clients.xlsx")
        produits = pd.read_excel("ExcelFiles/Produits.xlsx")
    except FileNotFoundError as e:
        print(f"Erreur : fichier manquant {e}")
        return
    
    # Gestion du client
    print("\n=== GÉNÉRATION DE FACTURE ===")
    type_client = input("Client existant (E) ou nouveau client (N) ? ").strip().upper()
    
    if type_client == "N":
        ajouter_client()
        # Recharger les clients après ajout
        clients = pd.read_excel("ExcelFiles/Clients.xlsx")
    
    # Sélection du client
    print("\nClients disponibles :")
    print(clients[['code_client', 'nom']])
    
    code_client = input("Code du client : ").strip().upper()
    client = clients[clients['code_client'] == code_client]
    
    if client.empty:
        print("Client non trouvé !")
        return
    
    client_info = client.iloc[0]
    
    # Saisie des produits
    print("\nProduits disponibles :")
    print(produits[['code_produit', 'libelle', 'prix_unitaire']])
    
    produits_facture = []
    total_ht = 0
    
    print("\nSaisie des produits (tapez 'fin' pour terminer) :")
    while True:
        code_produit = input("Code produit : ").strip().upper()
        if code_produit.lower() == 'fin':
            break
        
        produit = produits[produits['code_produit'] == code_produit]
        if produit.empty:
            print("Produit non trouvé !")
            continue
        
        try:
            quantite = int(input("Quantité : "))
        except ValueError:
            print("Quantité invalide !")
            continue
        
        produit_info = produit.iloc[0]
        prix_unitaire = produit_info['prix_unitaire']
        total_produit = prix_unitaire * quantite
        
        produits_facture.append({
            'code_produit': code_produit,
            'libelle': produit_info['libelle'],
            'prix_unitaire': prix_unitaire,
            'quantite': quantite,
            'total': total_produit
        })
        
        total_ht += total_produit
        print(f"Produit ajouté : {produit_info['libelle']} x {quantite} = {total_produit} FCFA")
    
    if not produits_facture:
        print("Aucun produit sélectionné !")
        return
    
    # Vérifier la carte de réduction (seulement pour les clients existants)
    taux_reduction = 0
    if type_client == "E":
        taux_reduction = verifier_carte_reduction(code_client)
    
    # Calculs
    montant_remise = total_ht * taux_reduction / 100
    total_ht_remise = total_ht - montant_remise
    montant_tva = total_ht_remise * 0.18
    total_ttc = total_ht_remise + montant_tva
    
    # Créer une carte de réduction si nécessaire (pas pour la première facture)
    if type_client == "E":
        creer_carte_reduction(code_client, total_ttc)
    
    # Génération du PDF
    if not os.path.exists("Factures"):
        os.makedirs("Factures")
    
    pdf = FPDF()
    pdf.add_page()
    
    # En-tête
    pdf.set_font("Arial", "B", size=14)
    pdf.cell(90, 10, txt=Nom, ln=0, align='L')
    
    pdf.set_font("Arial", "I", size=12)
    pdf.cell(100, 10, txt=f"Délivré le : {DeliveryDate}", ln=1, align='R')
    
    pdf.ln(5)
    
    # Informations client
    pdf.set_font("Arial", size=10)
    pdf.cell(190, 8, txt=f"Client : {client_info['nom']}", ln=1, align='L')
    pdf.cell(190, 8, txt=f"Contact : {client_info['contact']}", ln=1, align='L')
    pdf.cell(190, 8, txt=f"IFU : {client_info['IFU']}", ln=1, align='L')
    
    pdf.ln(10)
    
    # Titre facture
    pdf.set_font("Arial", "B", size=14)
    pdf.cell(190, 10, txt=f"FACTURE N° {IdFacture}", ln=1, align='C')
    
    pdf.ln(10)
    
    # Tableau des produits - En-tête (SANS la colonne vide)
    pdf.set_font("Arial", "B", size=9)
    pdf.cell(15, 8, txt="N°", border=1, ln=0, align='C')
    pdf.cell(35, 8, txt="Code", border=1, ln=0, align='C')
    pdf.cell(70, 8, txt="Libellé", border=1, ln=0, align='C')
    pdf.cell(30, 8, txt="P.U.", border=1, ln=0, align='C')
    pdf.cell(20, 8, txt="Qté", border=1, ln=0, align='C')
    pdf.cell(30, 8, txt="Total HT", border=1, ln=1, align='C')
    
    # Tableau des produits - Contenu
    pdf.set_font("Arial", size=9)
    
    # Fonction pour créer l'en-tête du tableau (pour les nouvelles pages)
    def creer_entete_tableau():
        pdf.set_font("Arial", "B", size=9)
        pdf.cell(15, 8, txt="N°", border=1, ln=0, align='C')
        pdf.cell(35, 8, txt="Code", border=1, ln=0, align='C')
        pdf.cell(70, 8, txt="Libellé", border=1, ln=0, align='C')
        pdf.cell(30, 8, txt="P.U.", border=1, ln=0, align='C')
        pdf.cell(20, 8, txt="Qté", border=1, ln=0, align='C')
        pdf.cell(30, 8, txt="Total HT", border=1, ln=1, align='C')
        pdf.set_font("Arial", size=9)
    
    # Afficher tous les produits
    for i, produit in enumerate(produits_facture, 1):
        # Vérifier si on doit créer une nouvelle page
        if pdf.get_y() > 250:  # Si on approche du bas de page
            pdf.add_page()
            creer_entete_tableau()
        
        # Afficher le produit
        pdf.cell(15, 8, txt=str(i), border=1, ln=0, align='C')
        pdf.cell(35, 8, txt=produit['code_produit'], border=1, ln=0, align='C')
        
        # Gérer les libellés longs
        libelle = produit['libelle']
        if len(libelle) > 25:
            libelle = libelle[:25] + "..."
        
        pdf.cell(70, 8, txt=libelle, border=1, ln=0, align='C')
        pdf.cell(30, 8, txt=f"{produit['prix_unitaire']:,.0f}", border=1, ln=0, align='C')
        pdf.cell(20, 8, txt=str(produit['quantite']), border=1, ln=0, align='C')
        pdf.cell(30, 8, txt=f"{produit['total']:,.0f}", border=1, ln=1, align='C')
    
    # Calculer le nombre de lignes vides nécessaires
    nb_produits = len(produits_facture)
    nb_lignes_min = 4  # Minimum 4 lignes pour un tableau propre
    
    # Ajouter des lignes vides SEULEMENT s'il y a moins de 4 produits
    if nb_produits < nb_lignes_min:
        lignes_vides = nb_lignes_min - nb_produits
        for i in range(lignes_vides):
            pdf.cell(15, 8, txt="", border=1, ln=0, align='C')
            pdf.cell(35, 8, txt="", border=1, ln=0, align='C')
            pdf.cell(70, 8, txt="", border=1, ln=0, align='C')
            pdf.cell(30, 8, txt="", border=1, ln=0, align='C')
            pdf.cell(20, 8, txt="", border=1, ln=0, align='C')
            pdf.cell(30, 8, txt="", border=1, ln=1, align='C')
    
    # Vérifier si on a assez de place pour les totaux
    if pdf.get_y() > 230:  # Si pas assez de place pour les totaux
        pdf.add_page()
    
    # Totaux (ajustés aux nouvelles largeurs)
    pdf.set_font("Arial", "B", size=10)
    
    pdf.cell(170, 8, txt="Total HT", border=1, ln=0, align='C')
    pdf.cell(30, 8, txt=f"{total_ht:,.0f}", border=1, ln=1, align='C')
    
    pdf.cell(170, 8, txt=f"Remise ({taux_reduction}%)", border=1, ln=0, align='C')
    pdf.cell(30, 8, txt=f"{montant_remise:,.0f}", border=1, ln=1, align='C')
    
    pdf.cell(170, 8, txt="Total HT après remise", border=1, ln=0, align='C')
    pdf.cell(30, 8, txt=f"{total_ht_remise:,.0f}", border=1, ln=1, align='C')
    
    pdf.cell(170, 8, txt="TVA (18%)", border=1, ln=0, align='C')
    pdf.cell(30, 8, txt=f"{montant_tva:,.0f}", border=1, ln=1, align='C')
    
    pdf.cell(170, 8, txt="Total TTC", border=1, ln=0, align='C')
    pdf.cell(30, 8, txt=f"{total_ttc:,.0f}", border=1, ln=1, align='C')
    
    pdf.ln(10)
    
    # Bas de page
    pdf.set_font("Arial", "I", size=10)
    total_lettres = nombre_en_lettres(int(total_ttc))
    pdf.cell(200, 10, txt=f"Arrêtée, la présente facture à la somme de : {total_lettres} francs CFA", ln=1, align='L')
    
    filename = f"Factures/Facture_{IdFacture}.pdf"
    pdf.output(filename)
    
    print(f"\nFacture générée avec succès !")
    print(f"Fichier : {filename}")
    print(f"Montant TTC : {total_ttc:,.0f} FCFA")
    print(f"Nombre de produits : {nb_produits}")
    
    if taux_reduction > 0:
        print(f"Remise appliquée : {taux_reduction}%")
    
    return filename