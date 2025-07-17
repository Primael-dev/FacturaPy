from functions.menu import menu,choice,rechoice,CreateFacture

from functions.manipe import (
    afficher_clients,
    afficher_produits,
    afficher_cartes_reduction,
   
)

menu()
choix=input("Veillez faire un choix : ")
choix=int(choix)
choice(choix)
if choix==1:
    souschoix=input("Veillez faire un choix : ")
    rechoice(souschoix)


