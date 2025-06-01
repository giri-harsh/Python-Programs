# set1 = set()
# set1.add(int(input("Enter an element")))
# set1.add(int(input("Enter an element")))
# set1.add(int(input("Enter an element")))
# print(set1)
# print(len(set1))

# set1.remove(4)

# collection = set( {1,2,3,4,5,6,6,6,6})
# print("unmodified collection",collection)
# print(collection.clear())
# print("popped colection :",collection)

# names = {"harsh","giri","goswami","komal","sharma"}
# print(len(names))
# print(names.pop())
# print(names)
# print(len(names))

set1={8,1,2,4,8}
set2={8,1,2,4,8,16}
set_union=set(set1.union(set2))
print(set_union)
set_intersection=set1.intersection(set2)
print(set_intersection)