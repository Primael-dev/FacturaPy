import pandas as pd

def ajouter_produit():
    try:
        produits = pd.read_excel("ExcelFiles/Produits.xlsx")
    except FileNotFoundError:
        produits = pd.DataFrame(columns=["code_produit", "libelle", "prix_unitaire"])

    print("\n=== AJOUT D’UN NOUVEAU PRODUIT ===")
    code = input("Code produit (ex: P001) : ").strip().upper()

    # Vérifie si le code existe déjà
    if code in produits['code_produit'].values:
        print("Ce code produit existe déjà. Veuillez en choisir un autre.")
        return

    libelle = input("Libellé du produit : ").strip()
    try:
        prix = float(input("Prix unitaire : "))
    except ValueError:
        print("Prix invalide. Entrez un nombre.")
        return

    nouveau_produit = pd.DataFrame([[code, libelle, prix]], columns=produits.columns)
    produits = pd.concat([produits, nouveau_produit], ignore_index=True)
    produits.to_excel("ExcelFiles/Produits.xlsx", index=False)
    print("Produit ajouté avec succès !")


# def ajouter_client():
#     try:
#         clients = pd.read_excel("ExcelFiles/Clients.xlsx")
#     except FileNotFoundError:
#         clients = pd.DataFrame(columns=["code_client", "nom", "contact", "IFU"])

#     print("\n=== AJOUT D’UN NOUVEAU CLIENT ===")
#     code_client = input("Code client (ex: C001) : ").strip().upper()
#     nom = input("Nom : ").strip()
#     contact = input("Contact : ").strip()
#     ifu = input("IFU (13 caractères) : ").strip()

#     # Vérifier si le client existe déjà
#     existe = clients[(clients['code_client'] == code_client)]
#     if not existe.empty:
#         print("Ce client existe déjà !")
#         print(existe)
#         return

#     nouveau_client = pd.DataFrame([[code_client, nom, contact, ifu]], columns=clients.columns)
#     clients = pd.concat([clients, nouveau_client], ignore_index=True)
#     clients.to_excel("ExcelFiles/Clients.xlsx", index=False)
#     print("Client ajouté avec succès !")