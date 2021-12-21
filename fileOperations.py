"""
Author: Yashkir Ramsamy
Contact: me@yashkir.co.za
Date: 2020/07/13

Purpose: Managing File I/O
"""
import pickle


def writeToFile(file, object):
    f = open(file, 'wb')
    print("Saving", object)
    pickle.dump(object, f)
    f.close()
    print("NOTICE: Saved hash")


def readFromFile(file):
    f = open(file, 'rb')
    object = pickle.load(f)
    f.close()
    return object
