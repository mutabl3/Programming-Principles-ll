def create_and_write():
    with open('sample.txt', 'w') as f:
        f.write("Line 1\n")
        f.write("Line 2\n")
        f.write("Line 3\n")

def append_to_file():
    with open('sample.txt', 'a') as f:
        f.write("Appended line\n")

if __name__ == "__main__":
    create_and_write()
    append_to_file()