print("Enter marks of 5 subs respectively out of 100")
a = float(input())
b = float(input())
c = float(input())
d = float(input())
e = float(input())
# percent = sum / total *100
sum =a+b+c+d+e
percent = (sum/500)*100
print("Percent obtained : ",percent)

if (percent>=90) : 
    print("Grade A")
elif(percent<90 and percent >=80):
    print("Grade B")
elif(percent<80 and percent>=70):
    print ("Grade C")
else :
    print("Grade D")


