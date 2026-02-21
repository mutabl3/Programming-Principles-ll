numbers = list(map(int,input().split()))

squared = list(map(lambda x: x ** 2, numbers))
print(squared)

evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)

sorting = sorted(numbers, key=lambda x: x)
print(sorting)

