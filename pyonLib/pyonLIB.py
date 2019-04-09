def Dec(X):
    Z=0
    if(type(X)==list):
        for Y in X:
            Z*=2
            Z+=Y
            return(chr(Z))
    if type(X)==int:
        return(chr(X))        
#def Bi(X): 
    
## ClassName=SERCOM(numberOf8BitDataSetsToRecive,ComPortNumber)
class SERCOM:
    def __init__(self,numberReceive,COM):
        import serial
        self.ser = serial.Serial()
        self.ser.port='COM'+str(COM)
        self.ser.baudrate=9600
        self.ser.open()
        self.ser.timeout=1
        self.ser.readline()
        self.ser.timeout=0.1
        self.RN=numberReceive
        ##Place data in this format data=[[1,0,0,1,0,1,0,0],[0,0,0,1,0,0,0,1]] or [148,17]
    def write(self,data):
        DATA=""
        for Z in data:
            DATA+=Dec(Z)
        if (self.ser.writable()):
            self.ser.write(DATA)
            ##it will return a int if you want I can make it so it will return the binary
    def read(self):
         if(self.ser.readable()):
            P=(self.ser.read(self.RN))
            return(P)

