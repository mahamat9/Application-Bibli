#!/bin/env python3

from base_livre import base_livre
import fonctions_bibli as f

import os
import os.path as osp 

try : 
    import PyPDF2
except ModuleNotFoundError : 
    os.system("pip install PyPDF2")
    import PyPDF2

import requests


class livre_pdf(base_livre):
    def __init__(self, ressource):
        ressource = ressource.replace('\\', '/')
        if ressource[-4:].lower() != '.pdf':  #lower met en minuscule les caracteres
            raise NameError("N'est pas un fichier PDF")
        self.nomfichier = osp.basename(ressource)
        
        
        try : 
            pdf_file = open(ressource, 'rb') #Si le livre est sur la machine.
        except FileNotFoundError : #Si le livre est en ligne
            Chemincache=osp.join(os.getcwd(),"cache") #On créer un fichier de cache dans lequel sera placé le livre.
            if not osp.exists(Chemincache) : os.mkdir(Chemincache)
            reqs = requests.get(ressource,stream=True,verify=f.VerificationSSL)
            if reqs.status_code == 200 :
                f.Download(ressource,Chemincache)
                ressource=osp.join(Chemincache,osp.basename(ressource))
                pdf_file = open(ressource, 'rb')
            else : return #Créer une instance "vide" au lieu de renvoyer un message d'erreur. 
            #Cela permet d'éviter l'interruption de programmes.
        
        self.ressource=ressource
        
        """
        # Extraire les métadonnées du PDF
        with open(ressource, 'rb') as pdf_file:
            lire_pdf = PyPDF2.PdfReader(pdf_file)
            self.metadonne = pdf_reader.getDocumentInfo()
            
        """   
        # Initialiser un objet PdfReader avec le fichier PDF
        lire_pdf = PyPDF2.PdfReader(pdf_file)

        # Accéder aux métadonnées du PDF via l'attribut info
        metadonnees = lire_pdf.trailer["/Info"]

        # Récupérer les métadonnées spécifiques
        author = str(metadonnees.get('/Author', 'Auteur inconnu'))
        title = str(metadonnees.get('/Title', 'Titre inconnu'))
        language = str(metadonnees.get('/Language', 'Langue inconnue'))
        date = str(metadonnees.get('/ModDate', 'Date inconnue'))
        subject = str(metadonnees.get('/Subject', 'Sujet inconnu'))
        
        if author in ['',' ','1'] : author="Auteur inconnu"

        #Recherche de la langue par un autre moyen
        if language == 'Langue inconnue':
            if '/Language' in metadonnees:
                language = metadonnees['/Language']
            elif '/Lang' in metadonnees:
                language = metadonnees['/Language']
            else:
                language = language
        caracteristique = [author,title, str(language),date,subject]
        self.caracteristique = caracteristique
        

    def type(self):
        return 'PDF'

    def titre(self):
        return self.caracteristique[1]

    def auteur(self):
        return self.caracteristique[0]

    def langue(self):
        return self.caracteristique[2]

    def sujet(self):
        return self.caracteristique[-1]

    def date(self):
        return self.caracteristique[3]

