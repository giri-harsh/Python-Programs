universe = [[1,2,3],
            [1,2,3,4],
            [1,2],
            [1,2,3]]

world_nine=universe[2][1]
print(world_nine)

universe.append([1,2,3,4,5])
print(universe)
print(len(universe[4]))
universe[1].pop()
print(universe)