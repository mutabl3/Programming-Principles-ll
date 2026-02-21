class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return "Animal sound"

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
    
    def speak(self):
        return f"{self.name} says: Woof!"

class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name)
        self.color = color
    
    def speak(self):
        return f"{self.name} says: Meow!"

class Flyable:
    def fly(self):
        return "Can fly"

class Swimmable:
    def swim(self):
        return "Can swim"

class Duck(Animal, Flyable, Swimmable):
    def __init__(self, name):
        super().__init__(name)
    
    def speak(self):
        return f"{self.name} says: Quack!"

dog = Dog("Bobik", "Shepherd")
cat = Cat("Murka", "Orange")
duck = Duck("Donald")

print(dog.speak())
print(cat.speak())
print(duck.speak())
print(duck.fly())
print(duck.swim())
print(f"{dog.name} - {dog.breed}")
print(f"{cat.name} - {cat.color}")