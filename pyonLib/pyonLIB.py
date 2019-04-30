#Cmbiles the n
def Dec(X):
    Z=0
    ##checks if list
    if(type(X)==list):
        V=""
        for Z in X:
            if type(Z) is list:
                for Y in Z:
                    Z*=2
                    Z+=Y
                V+=(chr(Z))
            elif type(Z)==int:
                V+=(chr(Z))
            elif type(Z)==str:
                V+=Z
        return([V])
    elif type(X)==int:
        return(chr(X))
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
            try:
                self.ser.open()
                break
            except serial.SerialException as error:
                None
            else:
                print("error port not found")
                return
##        else:
##            print("Error port not found")
##            quit
##            return(None)
        self.ser.timeout=1
        self.ser.readline()
        self.ser.timeout=0.1
        print(self.ser.writeTimeout)
        self.RN=numberReceive
    def write(self,data):##Note if giving binary place the list in a list because I have it in the write comand if there is a single list it will treat the ints as indivisual numbers but if there is a a list in a list it will treat the second list as binary this is so there could be multiple variables sent to the arduino
        DATA=""
        DATA=Dec(data)
        if (self.ser.writable()):
            DV=[]
            ##for D in DATA:
            self.ser.writelines(DATA)
##            for K in DATA[0]:
##                self.ser.write([K])
    def read(self,ReadNumber=0):
        if ReadNumber==0:
            ReadNumber=self.RN
        if(self.ser.readable()):
            P=(self.ser.read(ReadNumber))
            if len(P) >1:
                H=[]
                for K in P:
                    H.append(ord(K))
                return(H)
            elif len(P)==1:
                return(ord(P))
            else:
                return(P)
    def clear(self):
        self.ser.readall()      
    def close(self):
        self.ser.close()

