#! /usr/bin/env python3
'''
Try to remove duplicate folders
'''
from glob import glob
from shutil import rmtree

# main program
if __name__ == "__main__":
    folders = set(glob('*'))
    to_delete = set()
    for folder in folders:
        if len(folder) > 10 and folder[:10] in folders:
            to_delete.add(folder)
    if len(to_delete) == 0:
        print("No duplicate folders detected"); exit()
    print('\n'.join(sorted(to_delete)))
    if input("Delete %d folders? (y/N) " % len(to_delete)).lower().startswith('y'):
        for folder in to_delete:
            rmtree(folder)
