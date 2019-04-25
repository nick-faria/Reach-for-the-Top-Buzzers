def Dec(X):
    Z=0
    if(type(X)==list):
        V=[]
        for Z in X:
            if type(Z) is list:
                for Y in Z:
                    Z*=2
                    Z+=Y
                    V.append(chr(Z))
            elif type(X)==int:
                print(X)
                V.append(chr(X))
            elif type(X)==str:
                for j in X:
                    V.append(j)
    elif type(X)==int:
        return([chr(X)])
    elif type(X)==str:
        return(X)
#def Bi(X): 

class SERCOM:   
    def __init__(self,numberReceive):
        import serial
        self.ser = serial.Serial()
        self.ser.baudrate=9600
        for X in range(1,50):
            I=str(X)
            if len(I)==1:
                I="0"+I
            self.ser.port='COM'+I
            
##            if (self.ser.isatty()):
##                self.ser.open()
##                int("AS")
##                print(J)
##                break
##            elif(True):
##                print(I+"AS")
            try:
                self.ser.open()
                break
            except serial.SerialException as error:
            else:
                return
##        else:
##            print("Error port not found")
##            quit
##            return(None)
        self.ser.timeout=1
        self.ser.readline()
        self.ser.timeout=0.1
        self.RN=numberReceive
    def write(self,data):
        DATA=""
        DATA=Dec(data)
        if (self.ser.writable()):
            self.ser.write(DATA)
    def read(self):
         if(self.ser.readable()):
            P=(self.ser.read(self.RN))
            if len(P) >1:
                H=[]
                for K in P:
                    H.append(ord(K))
                return(H)
            else:
                return(ord(P))
    def close(self):
        self.ser.close()

