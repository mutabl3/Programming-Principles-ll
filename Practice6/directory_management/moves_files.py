import os
import shutil

def create_test():
    os.makedirs('src', exist_ok=True)
    os.makedirs('dst', exist_ok=True)
    with open('src/test.txt', 'w') as f:
        f.write("test")

def move_file():
    shutil.move('src/test.txt', 'dst/test.txt')
    print("Moved")

def copy_file():
    shutil.copy2('dst/test.txt', 'src/copy.txt')
    print("Copied")

def cleanup():
    shutil.rmtree('src')
    shutil.rmtree('dst')
    print("Cleaned")

if __name__ == "__main__":
    create_test()
    move_file()
    copy_file()
    cleanup()