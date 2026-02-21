class Students:
    university = 'KBTU'
    total_students = 0

    def __init__(self, name, age):
        self.name = name
        self.age = age
        Students.total_students += 1

    def introduce(self):
        return f"{self.name} {self.age}"

    def is_adult(self):
        return self.age >= 18

s1 = Students("Maxim", 17)
s2 = Students("Oleg", 19)

print(s1.introduce())
print(s2.introduce())
print(s1.is_adult())
print(s2.is_adult())
print(s1.university)
print(s2.university)
print(Students.total_students)