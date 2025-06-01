inventory = ['apple','bread','milk','eggs']
str = inventory[0] 
print(str)
inventory[1]='sugar'
print(inventory)
print(len((inventory)))  
print(max(inventory))
print(min(inventory))


inventory.append('hat')
print(inventory)
inventory.insert(0,'salt')
print(inventory)


inventory.pop()
print(inventory)

inventory.remove('apple')
print(inventory)

inventory.clear()
print(inventory)


inventory = []
print(inventory)