#!/bin/env python3

from base_livre import base_livre
import fonctions_bibli as f

import os
import os.path as osp 
  

try : 
    import ebooklib
except ModuleNotFoundError : 
    os.system("pip install ebooklib")
    import ebooklib
    
from ebooklib import epub  

import requests


class livre_epub(base_livre) : 
    
    def __init__(self,ressource) : 
        ressource=ressource.replace('\\','/')
        if ressource[-5:]!='.epub' : raise NameError("N'est pas un fichier EPUB")
        
        self.nomfichier=osp.basename(ressource)
        
        try : 
            livre_ouvert=epub.read_epub(ressource) #Si le livre est sur la machine.
        except FileNotFoundError : #Si le livre est en ligne
            Chemincache=osp.join(os.getcwd(),"cache") #On créer un fichier de cache dans lequel sera placé le livre.
            if not osp.exists(Chemincache) : os.mkdir(Chemincache)
            reqs = requests.get(ressource,stream=True,verify=f.VerificationSSL)
            if reqs.status_code == 200 : 
                f.Download(ressource,Chemincache)
                ressource=osp.join(Chemincache,osp.basename(ressource))
                livre_ouvert=epub.read_epub(ressource)
            else : return #Créer une instance "vide" au lieu de renvoyer un message d'erreur. 
            #Cela permet d'éviter l'interruption de programmes.
        
        self.ressource=ressource
        
        
        CP=['title','creator','language','subject','date'] #Caracteristiques possibles
        CPfr=['titre','auteur','langue','sujet','date']
        caracteristiques={}
        for i in range(5) : 
            if livre_ouvert.get_metadata('DC', CP[i])==[] : #Si la metadonnée correspondante n'est pas disponible
                caracteristiques[CPfr[i]]=CPfr[i]+" inconnu"
                if CP[i] in ['language','date'] : caracteristiques[CPfr[i]]+='e' #accord au féminin
            else : caracteristiques[CPfr[i]]=livre_ouvert.get_metadata('DC', CP[i])[0][0] #on associe la métadonnée à la clé correspondante
        self.caracteristiques=caracteristiques
        
    def type(self): return 'EPUB'

    def titre(self): return self.caracteristiques['titre']

    def auteur(self): return self.caracteristiques['auteur']

    def langue(self): return self.caracteristiques['langue']

    def sujet(self): return self.caracteristiques['sujet']

    def date(self): return self.caracteristiques['date'] 
