import pandas as pd
import numpy as np

dict1 ={
    "name":["harsh","komal","rajjo","aayushman","aadya"],
    "marks":[90,80,70,60,50],
    "age":[20,21,22,23,24],
}
df=pd.DataFrame(dict1)
print(df)

# to convert the data frame into csv file
df.to_csv("Freinds.csv")


# to get file without index
df.to_csv("friends_no_index.csv",index=False)
df.head(2)
df.tail(2)
df.describe()

# to read the csv file
harsh = pd.read_csv("friend1.csv")
harsh

#to change a value
harsh["marks"][1]=100
harsh.to_csv("harsh.csv")
# to change the index to something else
harsh.index=["first","second","third","fourth","fifth"]
harsh

#trying to edit a name and marks
harsh["name"][3]="mansi"
harsh["marks"][3]=99
harsh
print(type(harsh["name"]))

