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
    def write(self,data):
        DATA=""
        for Z in data:
            DATA+=Dec(Z)
        if (self.ser.writable()):
            self.ser.write(DATA)
    def read(self):
         if(self.ser.readable()):
            P=(self.ser.read(self.RN))
            return(ord(P))

