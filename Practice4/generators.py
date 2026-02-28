my_iter = iter([1, 2, 3])
print(next(my_iter)) 

def my_range(max):
    current = 2
    while current < max:
        yield current
        current += 1

diff = my_range(5)

print(next(diff))
print(next(diff))
print(next(diff))

gen_exp = (x**2 for x in range(10) if x % 2 == 0)
print(*list(gen_exp))
