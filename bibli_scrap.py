#!/bin/env python3

import fonctions_bibli as f
from Cbibli import bibli

import os.path as osp  
import requests


class bibli_scrap(bibli) :
    
    def alimenter2(self,url,nbmax,ntel) : #Cette deuxième version de la méthode alimenter considère cette fois-ci un nombre maximale de livre à télécharger. 
            #Comme elle est prédestinée à être utiliser dans la méthode .scrap(), on ne vérifie pas ici le status_code car il est déjà vérifié dans la méthode .scrap(). 
            if type(nbmax)!=list : nbmax=[nbmax] #Juste pour rendre nbmax mutable.
            
            Livres_presents=f.LFichiers(self.path)
            ListeUrls=f.Alllinks(url)
            i=0
            while i<len(ListeUrls) and nbmax[0]>0 :
                #Pour vérifier que c'est bien le lien d'un fichier pdf ou epub qui n'est pas déjà présent dans la bibliothèque.
                if (ListeUrls[i][-5:]==".epub" or ListeUrls[i][-4:]==".pdf") and osp.basename(ListeUrls[i]) not in Livres_presents : 
                    if self.ajouter(ListeUrls[i]) : 
                        ntel[0]+=1
                    nbmax[0]-=1
                                 
                    if ntel[0]%50==0 : print(f'{ntel[0]} livres téléchargés.')
                    
                i+=1  
       
    def scrap(self,url,profondeur,nbmax,Lurl=set([]),premiereappel=True,ntel=[0],arret=[False]) : #Lurl : liste des sites visités
        if premiereappel : 
            profondeur=int(profondeur)
            if profondeur <= 0 : raise ValueError("Profondeur entrée incohérente. Veuillez entrer un entier supérieur ou égal à 1")
        
        reqs = requests.get(url,stream=True,verify=f.VerificationSSL)      
        if reqs.status_code == 200 :

            if type(profondeur)!=list : profondeur=[profondeur]
            if type(nbmax)!=list : nbmax=[nbmax] #Juste pour rendre les deux arguments mutables.
            Lurl.add(url) #On rajoute l'url qui va être scrappé.
            
            self.alimenter2(url,nbmax,ntel)
            profondeur[0]-=1 #Pour noter qu'on a visité un site en plus. 
            
            if len(Lurl)%10==0 : print(f'{len(Lurl)} sites visités.')
            
            if nbmax[0]>0 and profondeur[0]>0  :
                Liste_autres_sites=f.AlllinksURL(url)
                for site in Liste_autres_sites : 
                    if (site not in Lurl) and profondeur[0]>0 and nbmax[0]>0 : #On vérifie que le site n'a pas déjà été visité.
                        self.scrap(site,profondeur,nbmax,Lurl,False,ntel,arret) #On rajoutera le nouveau site visité à Lurl
            elif ntel[0]==0 : 
                print(f"Aucun nouveau livre n'a été trouvé sur {len(Lurl)} page{'s'*(len(Lurl)>1)}.")
                arret[0]=True
            elif len(Lurl)==1 : 
                print(f"Scraping de {ntel[0]} livres sur une page effectué avec succés.")
                arret[0]=True
            else : 
                print(f"Scraping de {ntel[0]} livres sur {len(Lurl)} pages effectué avec succés.")
                arret[0]=True
        
        if not(arret[0]) and premiereappel : #Pour le cas où le programme a visité tous les sites et récupéré tous les livres possibles mais que nbmax[0]>0 et profondeur[0]>0.
            if ntel[0]==0 : 
                print(f"Aucun nouveau livre n'a été trouvé sur {len(Lurl)} page{'s'*(len(Lurl)>1)}.")
            elif len(Lurl)==1 : 
                print(f"Scraping de {ntel[0]} livres sur une page effectué avec succés.")
            else : 
                print(f"Scraping de {ntel[0]} livres sur {len(Lurl)} pages effectué avec succés.")
        
                
                

                
                
                

