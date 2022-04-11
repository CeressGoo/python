from random import randint
from time import time, sleep
from multiprocessing import Process
from os import getpid

'''
def download_task(filename):
    print('Downloading %s ....' % filename)
    time_to_done = randint(5,10)
    sleep(time_to_done)
    print('%sDownload succeeded! %d seconds are consumed.' % (filename, time_to_done))
'''

def downloader(filename):
    print('Launching download process at pid = %d.' % getpid())
    print('Starting downloading %s ...' % filename)
    time_to_done = randint(5,10)
    sleep(time_to_done)
    print('Download of %s finished! %d seconds are consumed.' % (filename, time_to_done))

def main():
    start = time()
    p1 = Process(target=downloader, args=('myfile01', ))
    p1.start()
    p2 = Process(target=downloader, args=('myfile02', ))
    p2.start()
    p1.join()
    p2.join()
    end = time()
    print('Time elapsed = %.2f seconds.' % (end - start))

if __name__ == "__main__":
    main()