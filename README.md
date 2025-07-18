Le projet FactureApk comporte les dossiers : ExcelFiles, extensions, functions et le fichier base.py.

Roles des différents composants:

*ExcelFiles : contient les fichiers Excels intervenant dans le projet.

*extensions : contient les extensions si on arrive à finir la base du tp d'abord.

*functions : contient toutes les fonctions que l'on créera pour avoir un code bien propre.

*base.py : le coeur de notre projet.

## Génération des statistiques PDF

Le script `functions/statistiques.py` permet de générer automatiquement un rapport PDF de statistiques sur les ventes et les cartes de réduction.

Chaque PDF généré porte un nom unique basé sur la date et l'heure (exemple : `statistiques_20250718_153000.pdf`) et se trouve dans le dossier `Statistiques`. Les anciens fichiers ne sont pas écrasés.

### Dépendances nécessaires

Avant d'utiliser la génération de statistiques, installez les dépendances Python suivantes :

```bash
pip install pandas matplotlib seaborn fpdf
```

### Utilisation

Lancez la fonction `generer_statistiques()` depuis votre menu ou directement dans un script Python pour générer le PDF.

