multidim_array = [
    [1,2,3],
    [4,5,6],
    [7,8,9]
]


result = []
[result.extend(el) for el in multidim_array]

print(result)