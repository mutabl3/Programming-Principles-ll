for i in range(1, 8):
    if i == 3:
        continue
    if i == 6:
        break
    print(i, end=" ")

print()

i = 0
while i < 8:
    i += 1
    if i == 3:
        continue
    if i == 6:
        break
    print(i, end=" ")