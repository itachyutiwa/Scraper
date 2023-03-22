def main():
    from model import Entreprise
    I = Entreprise("Domaine","service", "entreprise", "zone", "phone")
    a = I.ListeDomaine()
    print(a) #ok
    tmp1 = input("Choisissez le secteur à scraper dans la liste:? \n")
    b = I.getDomaine(tmp1)
    #print(b)
    c = I.getService(tmp1)
    #print(c)
    d = I.ListeService(tmp1)
    print(d)
    e = I.choixService(tmp1).keys()
    #print(e)
    tmp2 = input("Choisissez le domaine à scraper dans la liste:? \n")
    
    f= I.getInfos(tmp1,tmp2)
    return f

if __name__=="__main__":
    rs = main()
    print(rs)
