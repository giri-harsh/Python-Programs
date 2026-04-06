l1=[1,4,9,16,25,36,49,64,81,100]
key=int(input("Enter the number to search: "))
for val in l1:
    if val==key:
        print("Number found at index: ",l1.index(val))
        break
else:
    print("num not found")