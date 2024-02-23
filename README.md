# Application-Bibli
 Une application de création, d'alimentation... d'une bibliothèque électronique




# Guide d'utilisation de l'application "Bibli"
# Introduction : 
L'application "Bibli" a été conçue pour gérer une bibliothèque de livres au format EPUB 
et PDF, permettant l'ajout de livres depuis des URL par scrapping et la génération de rapports basés 
sur les données de la bibliothèque.
# Installation :
1. Assurez-vous d'avoir Python installé sur votre système, de préférence avec le pack Anaconda 
pour être sûr d’avoir tous les modules usuels nécessaires à l’application.
2. Installez les modules non présents dans Anaconda nécessaires avec la commande 
pip install ebooklib PyPDF2 xhtml2pdf beautifulsoup4 sur le terminal.
Configuration :
1. Ouvrez le fichier de configuration bibli.conf.
2. Définissez le répertoire pour les livres (bibliotheque=\....\) et celui pour les rapports 
(etats=\....\).
3. Spécifiez le nombre maximal de livres à rapatrier à chaque collecte (nbmax=100 si on veut un 
maximum de 100 livres par exemple).
4. Attention : Vous ne devez pas laisser d’espace !
# Utilisation :
1. Collecter des livres :
• Pour ajouter des livres depuis une URL avec une profondeur spécifique, utilisez 
./bibli.py <URL> <profondeur> dans le terminal, où <profondeur> est un nombre 
entier correspondant au nombre maximal de sites à visiter pour télécharger les livres.
2. Générer des rapports :
• Pour générer les rapports au format EPUB et PDF, utilisez ./bibli.py rapports .
# Options :
• -c <fichier_conf> : Permet de spécifier un fichier de configuration alternatif.
# Exemples :
1. ./bibli -c bibli2.conf https://math.univ-angers.fr/~jaclin/biblio/livres 1
2. ./bibli -c bibli2.conf rapports
# Remarques :
• Une connexion Internet est requise pour l'opération d'alimentation depuis une URL.
• Veillez à spécifier le fichier de configuration avec l'option -c.
• ATTENTION : Si vous avez un doute sur la sûreté de l’URL que vous souhaitez scrapper, ouvrez
