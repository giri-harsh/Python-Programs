x = 0
def move():
    global x 
    x = x+1
    return x

move()
print(x)

for i in range (5):
    result = move()
    print("x",i,"times :",result) 

