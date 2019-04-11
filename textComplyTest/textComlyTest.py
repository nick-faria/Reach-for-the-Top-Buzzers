class Data():
    def __init__(self,Type):
        self.Type=Type
        self.Ques=[]
        self.Ans=[]
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
