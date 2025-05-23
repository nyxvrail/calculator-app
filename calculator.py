# eroare ramasa 9.9.9.9 punct intre cifre, limitare doar la unul singur + 06*4=24 punere punct cand 0 e uramt de alte cifre
import pygame
import sys
import re
pygame.init()
latime,lungime=600,600#ecran principal
lbuton,lungbuton=95,150#butoane principale
lbuton2,lungbuton2=75,140#butoane semne 
font=pygame.font.Font(None,40)
font2=pygame.font.Font(None,30)
negru=(0,0,0)
gri=(211,211,211)
alb=(255,255,255)
c=(123,0,23)#culoare random
evenimente=[]# de fapt e o lista cu obiecte de tip rect
dictb = {
    0: "1",
    1: "2",
    2: "3",
    3: "4",
    4: "5",
    5: "6",
    6: "7",
    7: "8",
    8: "9",
    9: "0",
    10: "C",
    11: ".",
    12:"+",
    13:"-",
    14:"*",
    15:"/",
    16:"="
}

ecran_principal=pygame.display.set_mode((latime,lungime))
def ecran_de_calculat(text_pe_ecran):
    pygame.draw.rect(ecran_principal,negru,(0,0,latime,latime//3))
    numere_pe_ecran=font.render(text_pe_ecran,True,gri)# font.render(care text, enhancer ?,culoare)
    ecran_principal.blit(numere_pe_ecran,(20,30))

def butoane():
    evenimente.clear()
    k=0
    for i in range (4):#butoane cu numere
        for j in range(3):
            dreptunghi=pygame.Rect(j*(lungbuton+5),202+i*(lbuton+5),lungbuton,lbuton)
            #202 pozitie in jos,sare peste ecran de calculat
            #pozitie in functie de latimea si lungimea unui buton ex buton 3 se afla la 2 butoane in stanga celor 2 si la pozitia
            #i=1 de latimea unui buton sub ecran de calculat
            pygame.draw.rect(ecran_principal,c,dreptunghi)
            evenimente.append(dreptunghi)
            text=font.render(dictb[k],True,gri) #unde dictb[k] e defapt textul de pe fiecare buton
            text_rect=text.get_rect(center=dreptunghi.center)
            ecran_principal.blit(text,text_rect)
            k=k+1
    #al doilea loop pentru cea dea doua matrice de butoane */-+= 
    for i in range(5):
        dreptunghi=pygame.Rect(3*(lungbuton+5),202+i*(lbuton2+5),lungbuton2,lbuton2)#3 lungimi mai incolo,
        #incepe tot de la 202 de ecran de clalculat, 5 ala e diferenta dintre butoane
        pygame.draw.rect(ecran_principal,alb,dreptunghi)
        evenimente.append(dreptunghi)
        text=font.render(dictb[k],True,negru)
        text_rect=text.get_rect(center=dreptunghi.center)#dreptunghiul textului aflat in mijlocul dreptunghiului butonului creat anterior
        ecran_principal.blit(text,text_rect)
        # ~ care_ecran.blit(ce anume, unde anume)
        k=k+1
def calcul(expresie):
    try:
        de_afisat=""# de fapt e stringul rezultatului final
        expresie="".join(expresie)
        exp_ini=re.split(r'[+*/-]',expresie)
        exp_ini = [x for x in exp_ini if x.strip() != '']
        semn=[s for s in expresie if s in ['+','-','/','*']]
        #lista semn= fiecare semn in expresie unde semn este +-*/ si nu altceva
        if len(semn)==len(exp_ini):#tratarea exceptiei cand primul numar este negativ
            semn.pop(0)
            exp_ini[0]=str(float(exp_ini[0])*-1)
        exp_ini,semn=im_imp(exp_ini,semn)
        de_afisat=ad_sc(exp_ini,semn)
        #mai inati imultire si impartire apoi adunare si scadere
        #un singur numar ramane
        de_afisat=float(de_afisat)
        if de_afisat.is_integer() and de_afisat<=9999999999999:
            return str(round(de_afisat))
        else:
            return str(round(de_afisat,10))
    except:
        return "Eroare"
def afisare_rez(text):
    text2=font.render(text,True,gri)
    ecran_principal.blit(text2,(400,150))# e rezultatul plasat in josul ecranului la dreapta
def afisare_eroare(text):
    text2=font2.render(text,True,c)
    ecran_principal.blit(text2,(300,150))
def afisare_eroare_limita(text):
    text2=font2.render(text,True,c)
    ecran_principal.blit(text2,(300,150))    
def ad_sc(exp_ini,semn):
    i=0
    while i<len(semn):
        #exemplu exp_ini=[1,2] si semn=[+] 1+2
        if semn[i]=="+":
            exp_ini[i]=float(exp_ini[i])+float(exp_ini[i+1])
            semn.pop(i) #sterge semnul
            exp_ini.pop(i+1)# si cifra de dupa ex [1,2] -> [3,2] -> [3]
        elif semn[i]=="-":
            exp_ini[i]=float(exp_ini[i])-float(exp_ini[i+1])
            semn.pop(i)
            exp_ini.pop(i+1)
        else:
            i=i+1
    
    return exp_ini[0]# adica singurul nr ramas
            
def im_imp(exp_ini,semn):
    i=0
    while i<len(semn):
        if semn[i]=="*":
            exp_ini[i]=float(exp_ini[i])*float(exp_ini[i+1])
            semn.pop(i)
            exp_ini.pop(i+1)
        elif semn[i]=="/":
            exp_ini[i]=float(exp_ini[i])/float(exp_ini[i+1])
            semn.pop(i)
            exp_ini.pop(i+1)
        else:
            i=i+1
  
    return exp_ini,semn # tupla (lista cu numere ,lista de semne care contin doar + si -)
    

def main():
    frameuri_loop=True
    expresie=[]
    rez=""# tot stringul rezultatului final
    err="Nu se poate imparti la 0"
    lim="Ai atins limita de caractere"
    ok_zero=0
    ok_dublu_semn=0
    ok_numere_lipite=0
    ok_semn_in_fata=0
    ok_limita_atinsa=0
    while frameuri_loop:
        ecran_principal.fill(gri)
        ecran_de_calculat("".join(expresie))
        afisare_rez(rez)
        if ok_zero==1:
            afisare_eroare(err)
        if ok_limita_atinsa==1:
            afisare_eroare_limita(lim)
        butoane()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                frameuri_loop=False
            if event.type==pygame.MOUSEBUTTONDOWN:#e click?
                for i in range(len(evenimente)):# ia fiecare dreptunghi in parte si verifica daca clikul e in interiorul unuia
                    if evenimente[i].collidepoint(event.pos):# este poz clikul-ui in interiorul dreptunghiului ??? true-da, false nu
                        if i==10:
                            #dreptunghi[10], dictb{10:"C"} corespunde pt ca sunt puse in ordine
                            expresie.clear()
                            rez=""
                            ok_zero=0
                            ok_dublu_semn=0
                            ok_numere_lipite=0
                            ok_limita_atinsa=0
                        elif i==16:# dict{16:"="}
                            if not expresie or expresie == ["="]:
                                continue
                            ok_numere_lipite=1
                            ok_limita_atinsa=0
                            if expresie[-1] in [".","-","+","/","*"]: #tratarea unei exceptii cand ut. face egal cu un semn in aer la final
                                expresie.pop()
                            if not expresie:
                                continue
                            rez=calcul(expresie)
                            if rez=="Eroare":
                                rez=""
                                ok_zero=1
                            else:
                                expresie.clear()
                                expresie.append(rez)# in caz ca se mai doreste folosit mai departe
                        elif len(expresie)>15 or len(rez)>10:
                            ok_limita_atinsa=1
                            rez=""
                        elif ok_limita_atinsa==0:
                            if i<10:
                                ok_dublu_semn=0
                                ok_semn_in_fata=0
                            if i>11:
                                ok_numere_lipite=0
                            if i>10 and i<16 and not expresie:
                                ok_semn_in_fata=1
                            if i>10 and i<16 and expresie and expresie[-1] in [".","-","+","/","*"]:
                                ok_dublu_semn=1
                            if ok_zero==0 and ok_dublu_semn==0 and ok_numere_lipite==0 and ok_semn_in_fata==0:
                                expresie.append(dictb[i]) # adauga la expresie semne sau numere
        pygame.display.flip()
    pygame.quit()
main()


