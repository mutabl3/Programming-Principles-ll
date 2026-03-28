import os
import shutil

def copy_file():
    shutil.copy('sample.txt', 'sample_backup.txt')
    print("Copied")

def delete_file():
    if os.path.exists('sample_backup.txt'):
        os.remove('sample_backup.txt')
        print("Deleted")

if __name__ == "__main__":
    copy_file()
    delete_file()