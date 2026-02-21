is_student = True
is_teacher = False

age = 20
has_license = True

can_drive = age >= 18 and has_license

can_enter = (age >= 18) or has_license
cannot_enter = not can_enter

print(is_student)
print(is_teacher)
print(age > 18)
print(can_drive)
print(can_enter)
print(cannot_enter)