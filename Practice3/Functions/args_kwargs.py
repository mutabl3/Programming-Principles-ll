def args(*args):
    print(args)
    return sum(args)

print(args(10,20,30))

def kwargs(**kwargs):
    print(kwargs)       
    for key, value in kwargs.items():
        print(f"{key}: {value}")

kwargs(name="Amir", age=18, city="Almaty")
