import pandas as pd
# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

class Entreprise:
    links = ['https://www.goafricaonline.com/annuaire']
    driver.get(links[0])
    def __init__(self,domaine,service, entreprise, zone, phone, description):
        self.domaine = domaine
        self.service=service
        self.entreprise=entreprise
        self.zone=zone
        self.phone=phone
        self.description=description
       
    
    def getDomaine(self,domaine):
        domaine = driver.find_elements("xpath","//a[@class='stretched-link text-center']")
        L=[]
        for i in domaine:
            L.append(i.text)
        for j in L:
            if j==self.domaine:
                self.domaine=j
            self.domaine=None
     return self.domaine
    
    def getService(self):
        service=driver.find_elements("xpath""//a[@class='stretched-link text-center']")
        return self.service
    
    def getEnttreprise(self):
        entreprise = driver.find_elements("xpath""//*[@id='company-95413']/div[1]/div/div[1]/div[1]/h2/a/text()")
        return self.entreprise
    
    def getZone(self):
        zone =driver.find_elements("xpath""//div[@class='flex']")
        return self.zone

    def getPhone(self):
        phone = driver.find_elements("xpath""//a[@class='z-10 text-13 t:text-14 text-gray-700 underline hover:no-underline']")
        return self.phone
    
    def getDescritpion(self):
        description = driver.find_elements("xpath""//div[@class='hidden t:block text-gray-700 text-14']")
        return self.description

    #def getPays(self):
    #    return self.Pays

    def getDataframe(self):
        return self.data
    
    def getCsv(self):
        return self.csv
    
    def getExcel(self):
        return self.excel

I = Entreprise("Immobilier","service", "entreprise", "zone", "phone", "description")
print(I.getDomaine("Immobilier"))
