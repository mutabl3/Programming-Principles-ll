from functools import reduce

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def map_example():
    squares = list(map(lambda x: x**2, numbers))
    print(squares)

def filter_example():
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(evens)

def reduce_example():
    total = reduce(lambda x, y: x + y, numbers)
    print(total)

def combined():
    # sum of squares of even numbers
    result = reduce(
        lambda x, y: x + y,
        map(lambda x: x**2,
            filter(lambda x: x % 2 == 0, numbers))
    )
    print(result)

if __name__ == "__main__":
    map_example()
    filter_example()
    reduce_example()
    combined()