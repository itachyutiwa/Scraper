import streamlit as st
import time
from model import Entreprise
I=Entreprise("Domaine","service", "entreprise", "zone", "phone")
#Service
ListeDomaine = I.ListeDomaine()


st.sidebar.header("DOMAINE DE RECHERCHE")
with st.sidebar:
    with st.spinner("Loading..."):
        time.sleep(5)
domaine = st.sidebar.selectbox(
        "Choisissez le domaine",
        (ListeDomaine)
    )
    
st.header("SERVICES DE RECHERCHE")
with st.spinner("Loading..."):
    time.sleep(3)
I.getDomaine(domaine)
I.getService(domaine)
I.ListeService(domaine)

secteur=st.selectbox("Choisissez votre secteur",I.choixService(domaine))
formats = st.radio(
    "Choisissez un format de telechargement fichier",
    ("CSV", "PDF", "EXCEL","WORD","PPT"))
st.button("Télécharger")
#


#Sidebar de domaine (choix multiple)
#Liste deroulante secteur
#lListe deroulante pays
#Bouton chercher
#Apperçu de la table de données
#Liste deroulante format de fichier(.csv, .xlsx)