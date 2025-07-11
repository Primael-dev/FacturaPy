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
        print("Partie générer facture")
    elif choix == 3:
        print("Permet d’ajouter un nouveau produit au fichier Produits.")
    elif choix == 4:
        print("Quitter APK")
    else: 
        print("Entrée invalide")

def rechoice(choix):
    if choix =="a":
        print("afficher les clients")
    elif choix == "b":
        print("afficher les produits")
    elif choix == "c":
        print("Afficher les cartes de reduction")
    else:
        print("Entrée invalide")
    