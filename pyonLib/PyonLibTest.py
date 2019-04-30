import pyonLIB as V
J=V.SERCOM(2)
J.write(2)
J.clear()
for X in range(23):
    J.write([X,12])
    print(X,J.read())
J.close()
