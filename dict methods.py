student ={
    "name":"Harsh",
    "surname":"Giri",
    "sub":{ 
        "phy":90,
        "chem":95,
        "math":98,
        "english":"english",
    },
    "roll":24154015,
}
print(len(student))
print(type(student))

#methods

# print(student.keys())
# print(student["sub"].keys())
# print(student.values())
# print(student.items())
print(list(student.keys()))
