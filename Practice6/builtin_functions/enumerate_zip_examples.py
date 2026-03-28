names = ['Amir', 'Alina', 'Damir']
ages = [20, 19, 21]
grades = [85, 92, 78]

def enumerate_example():
    for i, name in enumerate(names, 1):
        print(f"{i}. {name}")

def zip_example():
    for name, age in zip(names, ages):
        print(f"{name} - {age}")

def zip_with_enumerate():
    for i, (name, grade) in enumerate(zip(names, grades), 1):
        print(f"{i}. {name}: {grade}")

def dict_from_zip():
    result = dict(zip(names, ages))
    print(result)

if __name__ == "__main__":
    enumerate_example()
    zip_example()
    zip_with_enumerate()
    dict_from_zip()