import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from fpdf import FPDF
import os


def generer_statistiques():
    if not os.path.exists("Graphes"):
        os.makedirs("Graphes")
    if not os.path.exists("Statistiques"):
        os.makedirs("Statistiques")

    # Lecture des données (Produits et Cartes Réduction)
    try:
        produits = pd.read_excel("ExcelFiles/Produits.xlsx")
        cartes = pd.read_excel("ExcelFiles/CartesReduction.xlsx")
    except Exception as e:
        print(f"Erreur de lecture des fichiers Excel : {e}")
        return


    # Statistiques réelles à partir de stats-ventes.xlsx
    ventes_path = "ExcelFiles/stats-ventes.xlsx"
    try:
        ventes_brutes = pd.read_excel(ventes_path)
    except Exception as e:
        print(f"Erreur de lecture du fichier des ventes : {e}")
        return

    # Grouper par produit
    ventes = ventes_brutes.groupby('libelle').agg({
        'quantite': 'sum',
        'total': 'sum'
    }).reset_index().rename(columns={
        'libelle': 'Produit',
        'quantite': 'Quantité vendue',
        'total': "Chiffre d'affaires"
    })
    if ventes.empty:
        print("Aucune vente enregistrée dans stats-ventes.xlsx.")
        return

    # ---- 3️⃣ Graphiques
    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 4))
    sns.barplot(x='Produit', y='Quantité vendue', data=ventes, palette='muted', hue='Produit', legend=False)
    plt.title('Produits les plus vendus')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("Graphes/produits_vendus.png")
    plt.close()

    plt.figure(figsize=(6, 4))
    ventes["Chiffre d'affaires"].plot.pie(autopct='%1.1f%%', labels=ventes['Produit'], startangle=140)
    plt.title("Repartition du chiffre d'affaires par produit")
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig("Graphes/repartition.png")
    plt.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "STATISTIQUES DES VENTES", ln=1, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Tableau des Ventes", ln=1)
    pdf.set_font("Arial", size=10)
    for i, row in ventes.iterrows():
        texte = f"{row['Produit']} : {row['Quantité vendue']} unites - {row["Chiffre d'affaires"]:.0f} FCFA"
        texte = texte.replace("’", "'")
        pdf.cell(0, 8, texte, ln=1)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Graphique : Produits les plus vendus", ln=1)
    pdf.image("Graphes/produits_vendus.png", x=10, y=pdf.get_y(), w=180)
    pdf.ln(90)

    titre_repartition = "Diagramme : Repartition du chiffre d'affaires"
    pdf.cell(0, 10, titre_repartition, ln=1)

    # Vérifier la position Y avant d'insérer l'image
    y_pos = pdf.get_y()

    if y_pos + 100 > 297 - 20:  
        pdf.add_page()
        y_pos = pdf.get_y()
    pdf.image("Graphes/repartition.png", x=10, y=y_pos, w=180)

    pdf.ln(80)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, "Cartes de Reduction Actives :", ln=1)
    for i, row in cartes.iterrows():
        texte = f"Client : {row['code_client']} | Remise : {row['taux_reduction']}%"
        texte = texte.replace("’", "'")
        pdf.cell(0, 8, texte, ln=1)

    from datetime import datetime
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"Statistiques/statistiques_{now}.pdf"
    pdf.output(pdf_filename)
    print(f"PDF de statistiques genere avec succes -> {pdf_filename}")
