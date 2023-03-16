import pandas as pd
from openpyxl.workbook import Workbook
# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

class Entreprise:
    links = ['https://www.goafricaonline.com/annuaire'] 
    driver.get(links[0])
    ld,s=[],[]
    def __init__(self,domaine,service, entreprise, zone, phone):
        self.domaine = domaine
        self.service=service
        self.entreprise=entreprise
        self.zone=zone
        self.phone=phone
        print("="*150)
        print("+"*10,"INITIATION D'UN SCRAPEUR","+"*10)
        print("."*5,"LISTE DES INFORMATIONS A EXTRAIRE","-"*5)
        print("-"*5,self.domaine,"--",self.service,"--",self.entreprise,"--",self.zone,"--",self.phone,"."*5)
   
    def pageMax(self,x):
        import re
        numbers = re.findall(r'\d+', x)  
        max_number = max(map(int, numbers)) 
        print("="*150)
    
        print("+"*10,"NOMBRE DE PAGE DETECTES","+"*10)
        print(max_number)

        return max_number



    def ListeDomaine(self):
        domaine = driver.find_elements("xpath","//a[@class='stretched-link text-center']") #ENV SECRETE_1
        L=[]
        for i in domaine:
            L.append(i.text)
            self.ld=L
        print("="*150)
        print("+"*10,"ENSEMBLE DE DOMAINES DISPONIBLES POUR CETTE PAGE","+"*10)
     
        return self.ld
    
    def getDomaine(self,d):
        if d in self.ld:
            self.domaine=d
        else:
            self.domaine=None
        print("="*150)
        print("+"*10,"DOMAINE SELECTIONNE","+"*10)
        return self.domaine
    
    
    def getService(self,d):
        temp = driver.find_element(By.LINK_TEXT, self.getDomaine(d))
        temp.click()
        self.service=driver.current_url
        print("="*150)
        print("+"*10,"SERVICE CHOISI DANS CE DOMAINE","+"*10)
        return self.service
    
    def ListeService(self,d):
        lk = self.getService(d)
        driver.get(lk)
        L=[]
        services = driver.find_elements("xpath","//div[@class='flex gap-x-4 items-center']") #ENV SECRETE_3
        for i in services:
            L.append(i.text)
        print("="*150)
        print("+"*10,"LISTE D'OFFRES DISPONIBLE DANS CE SERVICE","+"*10)
        print(L)
        return L
      
        
    def choixService(self,s):
        s=self.ListeService(s)
        l=[i.get_attribute("href") for i in driver.find_elements("xpath","//a[@class='stretched-link text-center']")] #ENV SECRETE_4
        dic = {}
        for i,j in zip(s,l):
            dic[i]=j
        print("="*150)
        print("+"*10,"OFFRE CHOISI","+"*10)
        print("."*5,"CORRESPONDANCE (OFFRE, ADRESSE)","-"*5)
        print(dic)
        return dic

    def getInfos(self,choix, demande):
        tmp=self.choixService(choix)[demande]
        urls = [tmp]
        driver.get(urls[0])
        p = driver.find_elements("xpath","//div[@class='mt-20 ls:mt-16 pagerfanta']") #ENV SECRETE_5
        l,entp,zone,phone=[],[],[],[]
        
        for i in p:
            l.append(i.text)
            
        n=self.pageMax(l[0])
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
            
        self.entreprise=entp
        self.zone=zone
        self.phone=phone
        driver.quit()
        data_dict = {"ENTREPRISES":self.entreprise,"ZONES":self.zone,"PHONES":self.phone}
        df=pd.DataFrame()
       
        long=min(len(data_dict["ENTREPRISES"]),len(data_dict["ZONES"]),len(data_dict["PHONES"]))
        df["ENTREPRISES"]=data_dict["ENTREPRISES"][:long]
        df["ZONES"]=data_dict["ZONES"][:long]
        df["PHONES"]=data_dict["PHONES"][:long]
        df['PHONES'] = df['PHONES'].apply(lambda x:x.replace('tel:',''))
        df['PHONES'] = df['PHONES'].apply(lambda x:x.replace('Tel:',''))
        df['PHONES'] = df['PHONES'].apply(lambda x:x.replace('Gsm:',''))
        
        formats = input("Choisissez un format d'enregistrement? (1.csv / 2.xlsx) :\n")
        if formats == "1":
            df.to_csv(f'data/{choix} - {demande}.csv')
        elif formats == "2":
            df.to_excel(f'data/{choix} - {demande}.xlsx')

        print("="*150)
        print("+"*10,"EXTRACTION DES CARACTERISTIQUES CI-DESSOUS MENTIONNEES","+"*10)
        return df.head(15)
    
    



