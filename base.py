from functions.menu import menu, choice, rechoice

def main():
    """Programme principal de l'application de facturation"""
    print("🚀 Bienvenue dans l'application de facturation !")
    
    while True:
        try:
            # Affichage du menu principal
            menu()
            choix = input("\nVeuillez faire un choix (1-5) : ").strip()
            
            # Validation de l'entrée
            try:
                choix = int(choix)
            except ValueError:
                print("❌ Veuillez entrer un nombre valide.")
                continue
            
            # Traitement du choix principal
            result = choice(choix)
            
            # Si choix = 5 (Quitter), arrêter le programme
            if result is False:
                break
            
            # Si choix = 1 (Consulter fichier), demander le sous-choix
            if result is True:
                souschoix = input("\nVeuillez faire un choix (a/b/c) : ").strip()
                rechoice(souschoix)
            
            # Attendre avant de continuer (optionnel)
            input("\nAppuyez sur Entrée pour continuer...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Programme interrompu par l'utilisateur. Au revoir !")
            break
        except Exception as e:
            print(f"❌ Une erreur inattendue s'est produite : {e}")
            print("Le programme continue...")

if __name__ == "__main__":
    main()