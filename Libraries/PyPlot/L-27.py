from matplotlib import pyplot as plt
import random

x = [i for i in range (1,101)] #makes range in form of a list of 0 to 100 values

y = []
for i in range(100):
    y.append(random.randint(1,101))
    
plt.plot(x,y)
plt.show()


plt.scatter(x,y)