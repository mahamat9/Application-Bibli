#!/bin/env python3

import os
import os.path as osp 
import sys

from bibli_scrap import bibli_scrap

##################Extraction des arguments rentrees et des donnees des fichiers .conf#####################

if sys.argv[1]=="-c" : 
    with open(sys.argv[2],"r") as file : 
        Lconf=[string for string in file]

    bibliotheque=Lconf[0][13:-1]
    if not osp.exists(bibliotheque) : os.mkdir(bibliotheque)

    nbmax=int(Lconf[2][6:-1])

    URL_ou_rapports=sys.argv[3] 

    if len(sys.argv)>=5 : profondeur=sys.argv[4]
else : 
    with open("bibli.conf","r") as file : 
        Lconf=[string for string in file]

    bibliotheque=Lconf[0][13:-1]
    if bibliotheque=='' : bibliotheque=osp.join(os.getcwd(), "Bibliotheque")
        
    if not osp.exists(bibliotheque) : os.mkdir(bibliotheque)

    nbmax=int(Lconf[2][6:-1])

    URL_ou_rapports=sys.argv[1] 

    if len(sys.argv)>=3 : profondeur=sys.argv[2]


#############Execution du code################

if __name__=="__main__" : 
    
    bib=bibli_scrap(bibliotheque)
    
    if URL_ou_rapports=='Rapports' : 
        try : 
            bib.rapport_auteurs("EPUB","Rapport_des_auteurs.epub")
            print("Rapport_des_auteurs.epub créé.")
            bib.rapport_livres("EPUB","Rapport_des_livres.epub")
            print("Rapport_des_livres.epub crée.")
            bib.rapport_auteurs("PDF","Rapport_des_auteurs.pdf")
            print("Rapport_des_auteurs.pdf créé.")
            bib.rapport_livres("PDF","Rapport_des_livres.pdf")
            print("Rapport_des_livres.pdf créé.")
            print("Génération des 2x2 rapports effectuée avec succés.")
        except FileNotFoundError as e : 
            print(e)
    else : 
        try :
            bib.scrap(URL_ou_rapports,profondeur,nbmax)
        except ValueError :
            print("Profondeur entrée incohérente. Veuillez entrer un entier supérieur ou égal à 1")
        
