class Data():
    def __init__(self,Type):
        self.Type=Type
        self.Ques=[]
        self.Ans=[]
    def read(self,Type,List,Loc):
        if("POINT" in Type and "AM I?"):
            Count=0
            while(len(self.Ans)<1 and len(self.Ques)<4):
                L=List[Loc+Count]
                if("CLUE" in L):
                    if ("AM I?" not in L):
                        C=0
                        J=""
                        while("AM I?" not in J):
                            C+=1
                            J=List[Loc+Count+C]
                            if(C>=12):
                                J=""
                                break
                        self.Ans.append(L+J)
                    else:
                        self.Ans.append(L)
        else:
            QNum=firstInt(self.Type)
            Count=0
            while(len(self.Ans)<QNum and len(self.Ques)<QNum):
                J=List[Loc+Count]
                P=check(List[Loc+Count])
                if P==".":
                    if ("?" not in J):
                       C=1
                        P=List[Loc+Count+C]
                       while (check(P)!="A"):
                           P=List[Loc+Count+C]
                           if (("© REACH FOR THE" not in P) and ("SCHOOREACH PACK #2" not in P) and (("Page" not in P) or ("of" not in P))):
                               J+=P
                               
def Foot(P):
    return((("© REACH FOR THE" not in P) and ("SCHOOREACH PACK #2" not in P) and (("Page" not in P) or ("of" not in P))))
def firstInt(Text):
    for X in Text:
        try:
            J=int(X)
            return(J)
        except ValueError:
            J=0
def check(String):
    hasint=True
    for X in String:
        try:
            int(X)
            print(X)            
        except(ValueError):
            if(X in ["\n","\t"," "]):
                continue
            else:
                return(X)
                break

File = open("test.txt",'r')
##Texts=File.read()
##print(Texts)
Count=-1
Quest=[]
Text=File.readlines()
for X in range(len(Text)):
    J=check(Text[X])
    if(J=='-'):
        Count+=1
        V=0
        Quest.append(Data(Text[X]))
    if(J=='.'):
        Quest[Count].Ques.append((Text[X]))
        if('?' not in Text[X]):
            Quest[Count].Ques[V]+=Text[X+1]
    if(J=="A"):
        Quest[Count].Ans.append(Text[X])
        
            
print(X)
