#!/bin/env python3

from livre_epub import livre_epub
from livre_pdf import livre_pdf
from base_bibli import base_bibli
from base_livre import base_livre
import fonctions_bibli as f


import os
import os.path as osp 


import sys
import shutil


##################On extrait la variable globale cheminrapport de bibli.conf#####################

if sys.argv[1]=="-c" : 
    with open(sys.argv[2],"r") as file : 
        Lconf=[string for string in file]

    cheminrapport=Lconf[1][6:-1]
    if not osp.exists(cheminrapport) : os.mkdir(cheminrapport)

else : 
    with open("bibli.conf","r") as file : 
        Lconf=[string for string in file]
    
    cheminrapport=Lconf[1][6:-1]
    if cheminrapport=='' : cheminrapport=osp.join(os.getcwd(), "Rapports")
    
    if not osp.exists(cheminrapport) : os.mkdir(cheminrapport)

#################################################################################################


class simple_bibli(base_bibli):
    def __init__(self,path): 
        path=path.replace('\\','/')
        self.path=path
        
    def ajouter(self,livre): #livre peut être une instance de classe base_livre, le chemin URL ou local du livre ou le chemin d'un dossier
        if isinstance(livre, base_livre) : #Si "livre" est une instance de classe base_livre
            shutil.copyfile(livre.ressource,self.path+"/"+livre.nomfichier)
        else : 
            livre=livre.replace('\\','/')
            
            if livre[-5:]==".epub" or livre[-4:]==".pdf" : #Si "livre" est le chemin du livre
            
                """ Version verifiée sur Linux
                try : 
                    shutil.copyfile(livre,self.path+"/"+osp.basename(livre))
                except FileNotFoundError : #Si le livre est en ligne
                    f.Download(livre,self.path)
                """
                
                #Version non vérifiée sur Linux mais sur Windows
                if osp.exists(livre) :                                      #Si le livre est sur la machine
                    shutil.copyfile(livre,self.path+"/"+osp.basename(livre))
                else :                                                      #Si le livre est en ligne
                    return f.Download(livre,self.path)
                ###
                
                    
                
            else : #Si "livre" est le chemin d'un dossier duquel on veut récupérer tous les livres aux formats epub et pdf.
                   #En particulier, cela permettra de copier le contenu d'une bibliothèque vers celui de self
                for file in f.LFichiers(livre) : 
                    if file[-5:]==".epub" or file[-4:]==".pdf" :
                        file=livre+"/"+file
                        self.ajouter(file)
                    
    def rapport_livres(self,format,fichier):
        Listenomsfichiers=f.LFichiers(self.path)
        Listelivres = []
        TexteRapport = []
        for nom in Listenomsfichiers : #On créer la liste des instances de classe livre_epub ou livre_pdf
            if nom[-5:]==".epub" : 
                Listelivres.append(livre_epub(self.path+"/"+nom)) 
            if nom[-4:]==".pdf" : 
                Listelivres.append(livre_pdf(self.path+"/"+nom))
        if Listelivres==[] : raise FileNotFoundError("Pas de livre dans la bibliothèque !")
        for livre in Listelivres :
            TexteRapport.append(", ".join([livre.titre(),livre.auteur(),livre.type(),livre.nomfichier])) #Correspond à la ligne ou se trouveront toutes les informations sur le livre           
        TexteRapport=f.str_to_html(TexteRapport)
        if format == "PDF":
            f.html_to_pdf(TexteRapport,cheminrapport+'/'+fichier,"Rapport des livres de la bibliothèque") #! var global
        elif format == "EPUB":
            f.html_to_epub(TexteRapport,"Rapport des livres de la bibliothèque",fichier,cheminrapport)
        

        
    def rapport_auteurs(self,format,fichier):
        Listenomsfichiers=f.LFichiers(self.path)  
        Listeauteurs = []
        Listelivres = []
        TexteRapport = []
        for nom in Listenomsfichiers :
            if nom[-5:]==".epub" : 
                Listeauteurs.append(livre_epub(self.path+"/"+nom).auteur()) #On créer la liste de tous les auteurs présents.
                Listelivres.append(livre_epub(self.path+"/"+nom))
            if nom[-4:]==".pdf" : 
                Listeauteurs.append(livre_pdf(self.path+"/"+nom).auteur())
                Listelivres.append(livre_pdf(self.path+"/"+nom))      
        if Listelivres==[] : raise FileNotFoundError("Pas de livre dans la bibliothèque !")
        Listeauteurs = sorted(list(set(Listeauteurs))) #On enlève les doublons et on range par ordre alphabétique.        
        for auteur in Listeauteurs :
            TexteRapport.append(auteur+' :')      
            Listelivresauteur=[livre for livre in Listelivres if livre.auteur()==auteur] #Liste des livres de l'auteur.
            for livre in Listelivresauteur : 
                TexteRapport.append(", ".join([livre.titre(),livre.type(),livre.nomfichier])) #Ligne de chaque livre de l'auteur.
            TexteRapport.append('') #Saut de ligne
        TexteRapport=f.str_to_html(TexteRapport)
        if format == "PDF":
            f.html_to_pdf(TexteRapport, cheminrapport+'/'+fichier, "Rapport des auteurs de la bibliothèque") #! var global
        elif format=="EPUB":
            f.html_to_epub(TexteRapport,"Rapport des auteurs de la bibliothèque",fichier,cheminrapport)



