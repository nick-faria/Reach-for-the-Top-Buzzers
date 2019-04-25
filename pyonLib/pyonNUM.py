import serial
ser = serial.Serial()
ser.port='COM28'
ser.baudrate=9600
ser.open()
LOOP=1002
##\r at the start
##for X in range(15):
V=0
X=0
J=0
JL="A"
ser.timeout=1
ser.readline()
ser.timeout=0.1
##ser.write("SEED")
while(X<12):
    print("As if"+str(X))
    if (ser.writable()):
        ser.write(JL)
##        ser.write(str(X%10)+str((X+2)%10))
 ##       ser.write(str(X%10)+str((X+2)%10))

        print("WAR "+str(X)+" AND "+str(X+2))
    if(ser.readable()):
##        ser.getWriteTimeout
        P=(ser.read(8))
        JL=input("INPUT)")
##        P=((ser.readline()))
        Jam=""
        Count=True
##       for Q in P:
##            Jam+=str(Q)
##            if(len(Jam)>=2):
##              try:
##                    P=(chr(long(Jam)))
##                except ValueError:
##                   P=P
##                Jam=""
##        print(P)
##        if not (P):
##            V=(input("esfd"))
        print(P)
        ##if (ser.writable()):
           ## ser.write(V+str(X)+"J="+str(J))
        X+=1
    else:
        V=(input("esfdaaaaa"))
        ser.write(V)
    if(V=="0"):
        break
    J+=1
    ##LOOP=input("Ss")
    ##ser.write(str(LOOP))
##ser.close()
ser.close()







