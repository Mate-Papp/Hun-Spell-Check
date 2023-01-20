import random
from itertools import count
import os

def directory_separate():
    import os
    disk_url_base = [*__file__]
    disk_url_base.reverse()
    for i in range(len(disk_url_base)):
        if disk_url_base[0] != '\\':
            del disk_url_base[0]
            
    disk_url = ""
    disk_url_base.reverse()
    for j in range(len(disk_url_base)):
        disk_url=disk_url + disk_url_base[j]
    return disk_url

def lineread(line, f):
    g = f.readlines()
    h = [*g[line-1]]
    h.reverse()
    del h[0]
    resoult = ""
    h.reverse()
    for i in range(len(h)):
        resoult = resoult + h[i]
    return resoult

def str_exists(array_or_string,word):
    if str(array_or_string).find("<_io.TextIOWrapper") != -1:
        array_or_string = array_or_string.readlines()
    for i in range(len(array_or_string)):
        g =array_or_string[i].upper()[:-1]
        y = word.upper()
        if g == y:
            return True, i
    return False 

def str_auto_repair(sentence_base):
    sentence_recommendation = ""
    sentence_base = sentence_base.upper() 
    sentence = sentence_base.split()
    sentence2=[]
    írásjelek=[]
    file = open(directory_separate() + "Toldalék-Module.txt", "r", encoding='utf-8')
    tol = file.readlines()
    fo = open(directory_separate() + "Lexicon-Module.txt", "r", encoding='utf-8')
    g = fo.readlines()
    toldalék=[]
    errors=[]
    sentence3=[]
    for i in range(len(sentence)):
        toldalék.append("")
        sentence2.append(sentence[i].replace(".","").replace("!","").replace("+","").replace("?","").replace(",","").replace(";","").replace("_","").replace("[","").replace("]","").replace("(","").replace(")",""))
        if len(sentence2[i])!=len(sentence[i]):
            írásjelek.append(sentence[i][+len(sentence2[i]):] + " ")
        else:
            írásjelek.append(" ")
        if str_exists(open(directory_separate() + "Lexicon-Module.txt", "r", encoding='utf-8'),sentence2[i])==False and len(sentence2[i])<=3:
            f = open(directory_separate() + "Lexicon-Module.txt", "a", encoding='utf-8')
            f.write(sentence2[i])
            f.write("\n")
            f.close()
            sentence_recommendation = sentence_recommendation + sentence2[i] + írásjelek[i]
        elif str_exists(open(directory_separate() + "Lexicon-Module.txt", "r", encoding='utf-8'),sentence2[i])==False:
            b=0
            for ir in range(len(tol)):
                tol[ir] = tol[ir].upper()
                if sentence2[i].find(tol[ir][:-1]) != -1 and sentence2[i][:-1].find(tol[ir][:-1]) == -1 and len(tol[ir][:-1])<len(sentence2[i]):
                    if str_exists(open(directory_separate() + "Lexicon-Module.txt", "r", encoding='utf-8'),sentence2[i][:-len(tol[ir][:-1])])!=False:
                        sentence_recommendation = sentence_recommendation + sentence2[i] + írásjelek[i]
                        b=1
                    else:
                        sentence2[i]=sentence2[i][:-len(tol[ir][:-1])]
                        írásjelek[i]=tol[ir][:-1]+írásjelek[i]
                        toldalék[i]=(tol[ir][:-1])
            if b==0:
                errors.append(sentence3[i])
                u=0
                for t in range(len(sentence[i])-2):
                    if t>3:
                        sim_db=0
                        two_split=[sentence[i][+t:],sentence[i][:-(len(sentence[i])-t)]]
                        for z in range(len(g)):
                            if g[z][:-1]==two_split[1]:
                                sim_db=sim_db+1
                        for s in range(len(g)):
                            if g[s][:-1]==two_split[0]:
                                sim_db=sim_db+1
                        if sim_db==2:
                            sentence_recommendation = sentence_recommendation + two_split[1] + " " + two_split[0] + írásjelek[i][+len(toldalék[i]):]
                            u=1
                            break
                if u==0:       
                    spells = [*sentence2[i]]
                    similarities = []
                    lenghts = []
                    for d in range(len(g)):
                        f=0
                        #szotarban lévő szó és ellenőrzése
                        g[d] = g[d][:-1]
                        if len(spells)-1<=len(g[d]) and len(spells)+1>=len(g[d]):
                            f = f+2
                        #begépelt betűk feldolgozása
                        for in_d in range(len(spells)):
                            if (g[d].find(sentence2[i][+1:])!=-1 or g[d].find(sentence2[i])!=-1) and len(spells)>=5:
                                f=100
                            if len(spells)<6:
                                if in_d == 0:
                                    if g[d].find(spells[in_d])==0:
                                        f=f+4
                                else:
                                    if g[d][+in_d:].find(spells[in_d])!=-1 and g[d][+in_d:].find(spells[in_d-1])<g[d][+in_d:].find(spells[in_d]):
                                        f=f+2
                            else:
                                if in_d == 0:
                                    if g[d].find(spells[in_d])!=-1:
                                        f=f+2
                                else:
                                    if g[d][+in_d:].find(spells[in_d])!=-1 and g[d][+in_d:].find(spells[in_d-1])<g[d][+in_d:].find(spells[in_d]):
                                        f=f+2
                        similarities.append(f)
                        lenghts.append(len(g[d]))
                    o=0
                    ht=0
                    trt=0
                    for h in range(len(similarities)):
                        if similarities[h]>o:
                            o=similarities[h]
                            ht=lenghts[h]
                            trt=similarities[h]
                            hg=lineread(h+1,open(directory_separate() + "Lexicon-Module.txt", "r", encoding='utf-8'))
                        elif similarities[h]==o:
                            if ht>lenghts[h]:
                                ht=lenghts[h]
                                trt=similarities[h]
                                hg=lineread(h+1,open(directory_separate() + "Lexicon-Module.txt", "r", encoding='utf-8'))
                    if hg.find(toldalék[i])!=-1 and toldalék[i]!="":
                        hg=hg[:-len(toldalék[i])]            
                    if trt<len(sentence2[i])*2:
                        for w in range(len(errors)):
                            f = open(directory_separate() + "Lexicon-Module.txt", "a", encoding='utf-8')
                            f.write(errors[w])
                            f.write("\n")
                            f.close()
                        errors.clear()
                        sentence_recommendation = sentence_recommendation + sentence2[i] + írásjelek[i]        
                    else :
                        sentence_recommendation = sentence_recommendation  + hg + írásjelek[i]     
        else:
            sentence_recommendation = sentence_recommendation + sentence2[i] + írásjelek[i]
    return sentence_recommendation

for i in count(0):
    x = input()
    print(str_auto_repair(x)) 
