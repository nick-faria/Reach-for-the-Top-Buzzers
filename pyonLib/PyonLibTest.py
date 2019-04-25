import pyonLIB as V
J=V.SERCOM(8)
for X in range(20):
    J.write(X)
    print(X,J.read())
J.close()
