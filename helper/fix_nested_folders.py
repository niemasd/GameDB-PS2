#! /usr/bin/env python3
'''
Try to remove duplicate folders
'''
from glob import glob
from os.path import isdir
from shutil import move, rmtree

# main program
if __name__ == "__main__":
    for game in glob('*'):
        for f in glob('%s/*' % game):
            if isdir(f):
                if len(list(glob('%s/*' % game))) == 1:
                    for txt in glob('%s/*' % f):
                        move(txt, txt.replace(f,game))
                else:
                    rmtree(f)
