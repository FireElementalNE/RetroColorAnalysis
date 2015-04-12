__author__ = 'fire'
import os

def remove_all_thumbs():
    directory_search = '.'
    for root, dirnames, filenames in os.walk(directory_search):
        for filename in filenames:
            if filename == "Thumbs.db":
                os.remove(os.path.join(root, filename))

if __name__ == "__main__":
    remove_all_thumbs()