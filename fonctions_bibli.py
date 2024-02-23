#!/bin/env python3

VerificationSSL=False

import os
import warnings

try : 
    import ebooklib
except ModuleNotFoundError : 
    os.system("pip install ebooklib")
    import ebooklib
    
from ebooklib import epub  

warnings.filterwarnings("ignore",'In the future version we will turn default option ignore_ncx to True.')
    
    
try : 
    from xhtml2pdf import pisa  
except ModuleNotFoundError : 
    os.system("pip install xhtml2pdf")
    from xhtml2pdf import pisa   
    

try : 
    from bs4 import BeautifulSoup
except ModuleNotFoundError : 
    os.system("pip install beautifulsoup4")
    from bs4 import BeautifulSoup
    

import os.path as osp 
  
import sys
import shutil

import urllib
import urllib.request
import urllib3
import ssl
from urllib.parse import urljoin

import requests

import urllib.error

if not(VerificationSSL) : #Désactivation des verifications du SSL et des alertes.
    urllib3.disable_warnings()
    ssl._create_default_https_context = ssl._create_unverified_context


################################Fonctions Prérequises###################################


def LFichiers(dossier) : 
    """
    dossier : (str) Chemin d'accès du dossier.
    
    Renvoie la liste des fichiers du dossier.
    """
    return [f for f in os.listdir(dossier) if osp.isfile(osp.join(dossier, f))]


def str_to_html(Lstr) :
    """
    Lstr : Liste de str symbolisant un fichier texte. Chaque ligne correspond à un élèment de la liste.
    
    Renvoie le str correspondant au code html censé renvoyer le texte. On a besoin de cette fonction 
    car on peut créer des fichiers epub uniquement à partir de script en html (du moins avec le package ebooklib).
    """         
    html_text = '<html>\n<body>\n'
    for line in Lstr:
        if line == '' : html_text += '<p> <br /> </p>\n'
        html_text += f'<p>{line}</p>\n'
    html_text += '</body>\n</html>'
    return html_text


def html_to_pdf(html_string, pdf_path, titre):
    """
    html_string est le html à transformer
    pdf_path le chemin/nom_du_fichier.pdf
    title est le titre pour la première page 
    
    Cette methode servira dans les rapports aux formats pdf
    """
    # HTML du titre
    ligne_titre = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>{titre}</title>
    </head>
    <body>
        <h1>{titre}</h1>
    </body>
    </html>
    '''

    # html_str et titre concatanés
    html_combine = f"{ligne_titre}\n{html_string}"

    with open(pdf_path, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(html_combine, dest=pdf_file)

    return not pisa_status.err


def html_to_epub(hstr,titre,nomfichier,patharrive,pathcwd=os.getcwd(),) : 
    """
    hstr : str correspondant au code html du texte à rentrer le fichier epub
    titre : (str) Titre affiché à la première page du fichier epub.
    nomfichier : (str) nom du fichier epub
    patharrive : (str) chemin du dossier où sera le fichier epub
    pathcwd : (str) chemin courant de ce script python. Utile à rentre uniquement si la commande 
    "os.getcwd()" ne fonctionne pas
    
    Créer le fichier epub à partir du code html hstr.
    """
    book = epub.EpubBook()
    
    book.set_identifier('sample123456')
    book.set_title(titre)
    book.set_language('en')
    
    book.add_author('user')
    
    
    c1 = epub.EpubHtml(title='Introduction',
                       file_name='text.xhtml',
                       lang='fr')
    c1.set_content(hstr)
    
    book.add_item(c1)
    
    style = 'body { font-family: Times, Times New Roman, serif; }'
    
    nav_css = epub.EpubItem(uid="style_nav",
                            file_name="style/nav.css",
                            media_type="text/css",
                            content=style)
    book.add_item(nav_css)
    
    book.spine = ['nav', c1]
    
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    epub.write_epub(nomfichier,book)

    shutil.move(osp.join(pathcwd,nomfichier),osp.join(patharrive,nomfichier))
    
""" Version vérifiée sur Linux
def Download(url,dossier) :
    
    lien : (str) lien du fichier que l'on veut télécharger.
    dossier : (str) chemin du dossier dans lequel on veut placer le fichier téléchargé.
    
    Télécharge le fichier dans le dossier voulu. 
    
    
    reqs = requests.get(url,stream=True,verify=VerificationSSL)
    
    if reqs.status_code == 200 : 
        nom=osp.basename(url)
        urllib.request.urlretrieve(url,osp.join(dossier,nom))
"""

def Download(url, dossier): #Version non vérifiée sur Linux mais sur Windows
    """
    lien : (str) lien du fichier que l'on veut télécharger.
    dossier : (str) chemin du dossier dans lequel on veut placer le fichier téléchargé.
    
    Télécharge le fichier dans le dossier voulu. 
    Renvoie True si le téléchargement est un succés et False sinon.
    """
    try:
        reqs = requests.get(url, stream=True, verify=VerificationSSL)
        
        if reqs.status_code == 200:
            nom = osp.basename(url)
            urllib.request.urlretrieve(url, osp.join(dossier, nom))
            return True
        else:
            print(f"Échec du téléchargement : {reqs.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Erreur lors du téléchargement : {e}")
        return False
    except urllib.error.URLError as e:
        print(f"Erreur lors du téléchargement : {e}")
        return False

def Alllinks(url) : 
    """
    lien : (str) lien de la page internet.
    
    Renvoie la liste contenant tous les liens présents à cette page. 
    """
    reqs = requests.get(url,stream=True,verify=VerificationSSL)
    
    if reqs.status_code == 200 : 
        soup = BeautifulSoup(reqs.text, 'html.parser')
        urls = []
        for link in soup.find_all('a'):
            sous_url=link.get('href')
            if type(sous_url)==str : #Pour éviter certains cas pathologiques.
                if sous_url[:4]!="http" : #Si c'est juste une "branche" et pas un lien complet (ex sousurl=nom_du_livre.epub ou /lien_d_une_autre_page/)
                    sous_url=urljoin(url,sous_url) #Permet donc de remplacer par le vrai lien (ex https://www.siteinternet.com/blabla/blablabla/.../nom_du_livre.epub)
                urls.append(sous_url)
        
    return urls    

def A_une_extension(lien) : 
    return ("." in osp.basename(lien))

def AlllinksURL(url) : 
    """
    lien : (str) lien de la page internet.
    
    Renvoie la liste contenant tous les liens vers d'autres pages présentes à cette page. 
    """
    reqs = requests.get(url,stream=True,verify=VerificationSSL)

    if reqs.status_code == 200 :
        soup = BeautifulSoup(reqs.text, 'html.parser')
        urls = []
        for link in soup.find_all('a'):
            sous_url=link.get('href')
            if sous_url and isinstance(sous_url, str):  # Vérification de la validité des liens
                ext=A_une_extension(sous_url)
                if type(sous_url)==str and(not(ext) or sous_url[-5:]==".html") : #On enlève les cas pathologiques et les liens de fichiers.
                    if sous_url[:4]!="http" : #Si c'est juste une "branche" et pas un lien complet (ex sousurl=nom_du_livre.epub ou /lien_d_une_autre_page/)
                        sous_url=urljoin(url,sous_url) #Permet donc de remplacer par le vrai lien (ex https://www.siteinternet.com/blabla/blablabla/.../nom_du_livre.epub)
                    urls.append(sous_url)
        
    return urls  
    
