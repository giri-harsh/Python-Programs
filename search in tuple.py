tup =(1,4,9,16,25,36,49,64,81,100)
# print(type(tup))
n = int(input("Enter a num to search"))
i=0
while i<len(tup):
    if tup[i]==n:
        print("element found at : ",i)
        break
    
    
    
    i+=1
else :
        print("Element not found",n)
