array = ["a", "a", "a", "b"]

print(array)
print(all([array[n] == array[n+1] for n in range(3)]))


cells = [
    ['a', 'b', 'c'],
    ['a', 'b', 'c'],
    ['a', 'b', 'c']
]

print(cells)
print(list(zip(*cells)))
