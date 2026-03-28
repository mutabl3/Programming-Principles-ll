def read_entire_file():
    with open('sample.txt', 'r') as f:
        content = f.read()
        print(content)

def read_line_by_line():
    with open('sample.txt', 'r') as f:
        for line in f:
            print(line.strip())

def read_all_lines():
    with open('sample.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            print(line.strip())

if __name__ == "__main__":
    read_entire_file()
    read_line_by_line()
    read_all_lines()