import os

def create_dirs():
    os.makedirs('nested/a/b/c', exist_ok=True)
    print("Directories created")

def list_files():
    items = os.listdir('.')
    for item in items:
        print(item)

def find_txt_files():
    for file in os.listdir('.'):
        if file.endswith('.txt'):
            print(file)

if __name__ == "__main__":
    create_dirs()
    list_files()
    find_txt_files()