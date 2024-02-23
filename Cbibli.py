#!/bin/env python3

import fonctions_bibli as f
from simple_bibli import simple_bibli

import os.path as osp  
import requests


class bibli(simple_bibli) : 
    
    def alimenter(self,url) : 
        reqs = requests.get(url,stream=True,verify=f.VerificationSSL)
        if reqs.status_code == 200 :
            ListeUrls=f.Alllinks(url)
            Livres_presents=f.LFichiers(self.path)
            for sousurl in ListeUrls :
                #Pour vérifier que c'est bien le lien d'un fichier pdf ou epub qui n'est pas déjà présent dans la bibliothèque.
                if (sousurl[-5:]==".epub" or sousurl[-4:]==".pdf") and osp.basename(sousurl) not in Livres_presents :
                    self.ajouter(sousurl)

