from model import Entreprise
import streamlit as st
import time
 
I=Entreprise("domaine","service", "entreprise", "zone", "phone")

st.sidebar.header("DOMAINE D'ACTIVITE")
choix_domaine = st.sidebar.selectbox("Choisissez",I.ListeDomaine())


st.header("SECTEURS D'ACTIVITE")
choix_secteur = st.selectbox("Choix",I.ListeService(choix_domaine))


st.subheader("_______DONNEES COLLECTEES_______")
H=I.getInfos(choix_domaine,choix_secteur)
with st.spinner("Scraping data now ..."):
    time.sleep(10)
    st.table(H.tail(5))    

st.subheader("_______SAUVEGARDE DES DONNEES_______")
choix_format = st.radio("Choix d'option",["CSV","EXCEL"])
#data = I.getInfos(choix_domaine,choix_secteur)
if choix_format == "CSV":
    if st.button("Télécharger"):
        H.to_csv(f"data/{choix_domaine} - {choix_secteur}.csv")
elif choix_format == "EXCEL":
    if st.button("Télécharger"):
        H.to_excel(f"data/{choix_domaine} - {choix_secteur}.xlsx")
    