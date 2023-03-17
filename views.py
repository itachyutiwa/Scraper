import streamlit as st
import time
import pandas as pd
from openpyxl.workbook import Workbook
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver = webdriver.Chrome(options=options)

class Entreprise:
    links = ['https://www.goafricaonline.com/annuaire'] 
    driver.get(links[0])
    ld,s=[],[]

    @st.cache_data
    def __init__(_self,domaine,service, entreprise, zone, phone):
        _self.domaine = domaine
        _self.service=service
        _self.entreprise=entreprise
        _self.zone=zone
        _self.phone=phone
 
    @st.cache_data
    def pageMax(_self,x):
        import re
        numbers = re.findall(r'\d+', x)  
        max_number = max(map(int, numbers)) 
        return max_number


    @st.cache_data
    def ListeDomaine(_self):
        domaine = driver.find_elements("xpath","//a[@class='stretched-link text-center']") #ENV SECRETE_1
        L=[]
        for i in domaine:
            L.append(i.text)
            _self.ld=L
        return _self.ld
    
    @st.cache_data
    def getDomaine(_self,d):
        if d in _self.ld:
            _self.domaine=d
        else:
            _self.domaine=None
        return _self.domaine
    
    @st.cache_data
    def getService(_self,d):
        temp = driver.find_element(By.LINK_TEXT, _self.getDomaine(d))
        temp.click()
        _self.service=driver.current_url
        return _self.service
    
    @st.cache_data
    def ListeService(_self,d):
        lk = _self.getService(d)
        driver.get(lk)
        L=[]
        services = driver.find_elements("xpath","//div[@class='flex gap-x-4 items-center']") #ENV SECRETE_3
        for i in services:
            L.append(i.text)
        return L
      
    @st.cache_data
    def choixService(_self,s):
        s=_self.ListeService(s)
        l=[i.get_attribute("href") for i in driver.find_elements("xpath","//a[@class='stretched-link text-center']")] #ENV SECRETE_4
        dic = {}
        for i,j in zip(s,l):
            dic[i]=j
        print("="*150)
        print("+"*10,"OFFRE CHOISI","+"*10)
        print("."*5,"CORRESPONDANCE (OFFRE, ADRESSE)","-"*5)
        print(dic)
        return dic
    
    @st.cache_data
    def getInfos(_self,choix, demande):
        tmp=_self.choixService(choix)[demande]
        urls = [tmp]
        driver.get(urls[0])
        p = driver.find_elements("xpath","//div[@class='mt-20 ls:mt-16 pagerfanta']") #ENV SECRETE_5
        l,entp,zone,phone=[],[],[],[]
        
        for i in p:
            l.append(i.text)

        
 # ou une valeur par défaut que vous souhaitez
    
        driver.get(tmp)
        list_entreprises = driver.find_elements("xpath","//a[@class='block stretched-link font-bold text-16 t:text-20 text-black hover:text-black no-underline hover:no-underline']") #ENV SECRETE_6
        list_zone = driver.find_elements("xpath","//div[@class='flex']") #ENV SECRETE_7
        list_phone = driver.find_elements("xpath","//a[@class='z-10 text-13 t:text-14 text-gray-700 underline hover:no-underline']") #ENV SECRETE_8
        
        for j in list_entreprises:
            entp.append(j.text)
        for j in list_zone:
            zone.append(j.text)
        for j in list_phone:
            phone.append(j.text)
        if len(l) > 0: 
            for t in range(int(_self.pageMax(l[0])) +1):
                driver.get(tmp+'?p='+str(t))
                list_entreprises = driver.find_elements("xpath","//a[@class='block stretched-link font-bold text-16 t:text-20 text-black hover:text-black no-underline hover:no-underline']") #ENV SECRETE_9
                list_zones= driver.find_elements("xpath","//div[@class='flex']") #ENV SECRETE_10
                list_phones = driver.find_elements("xpath","//a[@class='z-10 text-13 t:text-14 text-gray-700 underline hover:no-underline']") #ENV SECRETE_12
                
                for j in list_entreprises:
                    entp.append(j.text)
                for j in list_zones:
                    zone.append(j.text)
                for j in list_phones:
                    phone.append(j.text)
        else:
            n = 2
            for t in range(n+1):
                driver.get(tmp+'?p='+str(t))
                list_entreprises = driver.find_elements("xpath","//a[@class='block stretched-link font-bold text-16 t:text-20 text-black hover:text-black no-underline hover:no-underline']") #ENV SECRETE_9
                list_zones= driver.find_elements("xpath","//div[@class='flex']") #ENV SECRETE_10
                list_phones = driver.find_elements("xpath","//a[@class='z-10 text-13 t:text-14 text-gray-700 underline hover:no-underline']") #ENV SECRETE_12
                
                for j in list_entreprises:
                    entp.append(j.text)
                for j in list_zones:
                    zone.append(j.text)
                for j in list_phones:
                    phone.append(j.text)
            
        _self.entreprise=entp
        _self.zone=zone
        _self.phone=phone
        driver.quit()
        data_dict = {"ENTREPRISES":_self.entreprise,"ZONES":_self.zone,"PHONES":_self.phone}
        df=pd.DataFrame()
       
        long=min(len(data_dict["ENTREPRISES"]),len(data_dict["ZONES"]),len(data_dict["PHONES"]))
        df["ENTREPRISES"]=data_dict["ENTREPRISES"][:long]
        df["ZONES"]=data_dict["ZONES"][:long]
        df["PHONES"]=data_dict["PHONES"][:long]
        df['PHONES'] = df['PHONES'].apply(lambda x:x.replace('tel:',''))
        df['PHONES'] = df['PHONES'].apply(lambda x:x.replace('Tel:',''))
        df['PHONES'] = df['PHONES'].apply(lambda x:x.replace('Gsm:',''))
        return df
    
 
I=Entreprise("domaine","service", "entreprise", "zone", "phone")

st.sidebar.header("DOMAINE D'ACTIVITE")
choix_domaine = st.sidebar.selectbox("Choisissez",I.ListeDomaine())


st.header("SECTEURS D'ACTIVITE")
choix_secteur = st.selectbox("Choix",I.ListeService(choix_domaine))


st.subheader("_______DONNEES COLLECTEES_______")
H=I.getInfos(choix_domaine,choix_secteur)
with st.spinner("Scraping data now ..."):
    time.sleep(10)
    st.table(H)    

st.subheader("_______SAUVEGARDE DES DONNEES_______")
csv = H.to_csv(f"{choix_domaine} - {choix_secteur}.xlsx",index=False)
xlsx = H.to_excel(f"{choix_domaine} - {choix_secteur}.xlsx",index=False)
choix_format = st.radio("Choix d'option",["CSV","EXCEL"])
if choix_format == "CSV":
    #st.download_button("Télécharger",data=csv,file_name=f"{choix_domaine} - {choix_secteur}.csv",mime='text/csv')
    st.button("Télécharger")
    #st.table(csv)
elif choix_format == "EXCEL":
    #st.download_button("Télécharger",data=xlsx,file_name=f"{choix_domaine} - {choix_secteur}.xlsx",mime='text/xlsx')
    st.button("Télécharger")
    #st.table(xlsx)