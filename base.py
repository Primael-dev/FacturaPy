from functions.menu import menu,choice,rechoice

menu()
choix=input("Veillez faire un choix : ")
choix=int(choix)
choice(choix)
if choix==1:
    souschoix=input("Veillez faire un choix : ")
    rechoice(souschoix)
