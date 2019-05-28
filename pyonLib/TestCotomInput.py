import pyonLIB as V
J=V.SERCOM(1)
while True:
    V =int (input("what number do you want to send(-1 to close)"))
    J.write(V)
    J.clear()
    for Z in range(5):
        print(J.read)
    if V==-1:
        break


J.close()
