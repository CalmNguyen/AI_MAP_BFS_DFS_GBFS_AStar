f=open('maze1.txt','r')
data=f.read()
data=data.replace('-','x')
data=data.replace('+','x')
data=data.replace('|','x')
print(data)
