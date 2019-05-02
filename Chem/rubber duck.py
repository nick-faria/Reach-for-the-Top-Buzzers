import time
import pygame
import textwrap
from pygame.font import*
from  pygame.locals import*
def insertline(text,x,y,F,S,CL):
    TT=""
    for(X) in text:
        if (X=='\n'):
            A=F.render(TT,True,CL)
            S.blit(A,(x,y))
            TT=""
            y+=F.get_height()+2
        else:
            TT+=X
    S.blit(F.render(TT,True,CL),(x,y))
items=pygame.image.load("5.0.png")
png1=pygame.image.load("2.png")
HAZ=pygame.image.load("$.png")
ov=pygame.image.load("7.png")

##'batangbatangchegungsuhgungsuhche', 'sansserif', 'bookmanoldstyle', 'lettergothicstdslantedopentype', 'myriadproboldopentype', 'esriusmutcd2', 'esriusmutcd3', 'lucidahandwriting', 'esriusmutcd1', 'haettenschweiler', 'calisto', 'kozminpr6nregularopentype', 'curlz', 'gisha', 'isocp2', 'isocp3', 'commercialscript', 'californianfb', 'euclidfraktur', 'jokerman', 'bell'
CLOCK=pygame.time.Clock()
pygame.init()
pygame.font.init()
SZX=1200
SZY=700
SURF = pygame.display.set_mode((SZX,SZY))
##FONT=pygame.font.Font("freesansbold.ttf",12)
##FONT=pygame.font.SysFont('batangbatangchegungsuhgungsuhche',12)
#FONT=pygame.font.SysFont('kozminpr6nregularopentype',12)
FONT=pygame.font.SysFont('calisto',22)
FONT1=pygame.font.SysFont('calisto',40,bold=True)
FONT2=pygame.font.SysFont('calisto',55,bold=True,italic=True)

FONTH=FONT.get_height()
TickSpeed=128
LOOP=True
##LOOP=False
class BOX:
    ##pygame.draw.rect(SURF,CL,(X,Y,X2,Y2))
    def __init__(self,S,X,Y,SZX,SZY,TX,F,CL1,CL2):
        self.X=X
        self.Y=Y
        self.SZX=SZX
        self.SZY=SZY
        self.TX1=F.render(TX,True,CL2)
        self.TX2=F.render(TX,True,CL1)
        self.XT=int(round((SZX-F.size(TX)[0])/2)+X)
        self.YT=int(round((SZY-F.size(TX)[1])/2))+Y
        self.CL1=CL1
        self.CL2=CL2
        self.S=S
    def draw(self):
        POS=pygame.mouse.get_pos()
        CLICK=pygame.mouse.get_pressed()[0]
        X=POS[0]
        Y=POS[1]
        if((X>=self.X and X<=self.X+self.SZX)and(Y>=self.Y and Y<=self.Y+self.SZY)):
            pygame.draw.rect(self.S,self.CL2,(self.X,self.Y,self.SZX,self.SZY))
            self.S.blit(self.TX2,(self.XT,self.YT))
            if(CLICK):
                return(True)
            else:
                return(False)
        else:
            pygame.draw.rect(self.S,self.CL1,(self.X,self.Y,self.SZX,self.SZY))
            self.S.blit(self.TX1,(self.XT,self.YT))
            return(False)
V=500
B=75
OV=BOX(SURF,50,150,V,B,"Overview",FONT1,(225,30,30),(30,255,255))
EOH=BOX(SURF,50,250,V,B,"Effects on Humans",FONT1,(30,225,30),(225,30,225))
IOE=BOX(SURF,50,350,V,B,"Impact on the Environment",FONT1,(30,30,225),(225,225,30))
CSP=BOX(SURF,50,450,V,B,"Chemical Properties",FONT1,(155,255,55),(100,0,200))
UOT=BOX(SURF,150+V,150,V,B,"Usage of Trclosan",FONT1,(225,30,30),(30,225,225))
ALT=BOX(SURF,150+V,250,V,B,"Alternatives",FONT1,(30,225,30),(225,30,225))
BIB=BOX(SURF,150+V,350,V,B,"Bibliography",FONT1,(30,30,225),(225,225,30))
QUIT=BOX(SURF,150+V,450,V,B,"Quit",FONT1,(155,255,55),(100,0,200))
Back=BOX(SURF,10,10,100,50,"Back",FONT1,(225,30,30),(0,30,30))
Screen=1
while(LOOP):
    SURF.fill((255,255,255))
    
    if(Screen==1):
        insertline(("Triclosan"),((-FONT2.size("Triclosan")[0]+SZX)/2),25, FONT2,SURF,(88,185,25))
        if(OV.draw()):
            Screen=2
        if(EOH.draw()):
            Screen=3
        if(IOE.draw()):
            Screen=4
        if(CSP.draw()):
            Screen=5
        if(UOT.draw()):
            Screen=6
        if(ALT.draw()):
            Screen=7
        if(BIB.draw()):
            Screen=8
        if(QUIT.draw()):
            LOOP=False
    if(Screen==2):
        insertline("Triclosan is an anthropogenic antibacterial substance\n used in cosmetics, non-prescription drugs and in \nhospitals. With the widespread use of triclosan which has\n an increasing presence in the environment. Triclosan has\n been a growing concern of its effects on the environment\n and human health. \n",150,75,FONT,SURF,(77,1,250))
        SURF.blit(ov,(75,250))
        if(Back.draw()):
            Screen=1
    if(Screen==3):
        insertline("Triclosan currently has a high presence in the human\n body with 75 percent of urine samples tested to contain \nhigh levels of triclosan. Making it a major concern about\n the effects of triclosan. The current studies on the effects\n of triclosan has yielded incompatible results with some \nstudies stating that triclosan is harmless and while others \nreport that exposure to triclosan can cause irritation on the \nskin. Making it unclear of its effects on human health. It \nwas hypothesised that Triclosan was a chloroform \ngenerator stating that in the right circumstance it could \ndouble the amount of chloroform. Chloroform is a known \ncarcinogen it raises the concern of products with triclosan \nto be carcinogenic.\n",150,75,FONT,SURF,(77,1,250))
        if(Back.draw()):
            Screen=1
    if(Screen==4):
        insertline("Triclosan makes its presence into the the environment by \nthe means of the sewage. with products that contain \ntriclosan being washed down the drain that would \neventually reach the aquatic environment. The bacteria is \nhighly vulnerable to triclosan which is primarily used as an \nantibacterial agent. As well in medical and reach facilities\n",150,75,FONT,SURF,(77,1,250))
        SURF.blit(HAZ,(725,50))
        if(Back.draw()):
            Screen=1
    if(Screen==5):
        insertline("Triclosan most commonly comes in a white crystalline \npowder. The Molar mass of triclosan is 289.536 g/mol.  \nTriclosan is also an hydrophilic substance that has a \nsolubility of In water, 10 mg/L at 20 deg C. Which also has \na resistance against ph. Allowing it to remain active over\n long periods of time.\n",150,75,FONT,SURF,(77,1,250))
        SURF.blit(png1,(725,50))
        if(Back.draw()):
            Screen=1
    if(Screen==6):
        insertline("Triclosan is used as an antibacterial agent used in\n cosmetics, drugs, and personal care products. For it’s \nhigh phs resistance and the fact that it is only breaks\n down in light Triclosan is also used in hospitals and \nbiomedical research.\n",150,75,FONT,SURF,(77,1,250))
        SURF.blit(items,(725,50))
        if(Back.draw()):
            Screen=1
    if(Screen==7):
        insertline("Due to the environmental hazard and also the carcinic\n nature of triclosan it is best to reduce the usage of \nTriclosan, but to do so there must be an alternative for\n Triclosan. One of the possible alternatives is \nchloroxylenol. Chloroxylenol although is concentrated\n form is an irritant it is not an environmental hazard.\n Making it safe alternative to triclosan.\n",150,75,FONT,SURF,(77,1,250))
        if(Back.draw()):
            Screen=1
    if(Screen==8):
        insertline("Canada, Health. “Triclosan.” Canada.ca, 15 Jan. 2019, \n     www.canada.ca/en/health-canada/services/chemicals-product-safety/triclosan.html.\nDhillon, Gurpreet Singh et al. “Triclosan: current status, occurrence, environmental risks and \n     bioaccumulation potential” International journal of environmental research and public health vol. \n     12,5 5657-84. 22 May. 2015, doi:10.3390/ijerph120505657\nEnvironment and Climate Change Canada. “Environment and Climate Change Canada - \n     Triclosan.” Environment and Climate Change Canada - Triclosan, 16 Feb. 2017, \n     www.ec.gc.ca/ese-ees/default.asp?lang=En&n=F6CF7AA4-1.\nNational Center for Biotechnology Information. PubChem Database. \n     4-Chloro-3,5-dimethylphenol, CID=2723, https://pubchem.ncbi.nlm.nih.gov/compound/2723 \n     (accessed on Mar. 22, 2019) \nNational Center for Biotechnology Information. PubChem Database. Triclosan, CID=5564, \n     https://pubchem.ncbi.nlm.nih.gov/compound/5564 (accessed on Mar. 22, 2019)\nSCCS (Scientific Committee on Consumer Safety), Opinion on\n     triclosan (antimicrobial resistance), 22 June 2010",150,75,FONT,SURF,(77,1,250))
        if(Back.draw()):
            Screen=1
        
    ##insertline("SCORE: \n ham \n game\\",10,10,FONT,SURF,(77,1,250))
    ##SURF.blit(SCDSP,(0,0))
    ##if(YH.draw()):
    ##    print("SS")
    
    for event in pygame.event.get():
        if event.type==QUIT:
            LOOP=False
            
        
    pygame.display.update()
    CLOCK.tick(TickSpeed)
pygame.quit()
quit()
