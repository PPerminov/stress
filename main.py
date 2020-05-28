import os
import sys
from time import time
import multiprocessing
from random import randint


def worker(params):
    try:
        read_priority = int(os.environ['READ_PRIORITY'])
        globalFilesList = params[1]
        globalDict = params[0]
        MaxFileSize = globalDict['MaxFileSize']
        PID = params[2]
        global randomData
        while True:
            if not free_space(globalDict['MaxFileSize'] * 100, globalDict['work_path']):
                filename = globalFilesList.pop(0)
                print(PID, 'clean', 'start', filename)
                try:
                    os.remove(globalDict['work_path'] + "/" +
                              filename)
                except:
                    print(PID, 'clean', 'failed', filename)
                continue
            if randint(1, 6654578566966) % read_priority != 0:  # very hacky stuff
                try:
                    filename = globalFilesList.pop(0)
                except:
                    print(PID, 'read', 'error', 'globalFilesList')
                    continue
                try:
                    with open(globalDict['work_path'] + "/" + filename, 'rb', 0) as f:
                        print(PID, time(), 'read', 'start', filename, 0)
                        counter = len(f.read())
                    print(PID, time(), 'read', 'complete', filename, counter)
                except:
                    print(PID, time(), 'read', 'error', filename, 0)
                globalFilesList.append(filename)
            else:
                syms = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
                filename = []
                while len(filename) < 128:
                    filename.append(syms[randint(0, len(syms) - 1)])
                filename = ''.join(filename)
                size = randint(0, globalDict['MaxFileSize'])
                try:
                    with open(globalDict['work_path'] + "/" + filename, 'wb', 0) as w:
                        print(PID, time(), 'write', 'start', filename, 0)
                        w.write(randomData[0:size])
                    print(PID, time(), 'write', 'complete', filename, size)
                    globalFilesList.append(filename)
                except:
                    print(PID, time(), 'write', 'error', filename)
    except KeyboardInterrupt:
        return


def free_space(size, folder):
    s = os.statvfs(folder)
    return s.f_bsize * s.f_bavail > size


def create_file(filename, sizeMB, write_to_disk=False):  # пишет рандомный битовый файл
    with open('/dev/urandom', 'rb') as rand1:
        if write_to_disk:
            print('Writing random file')
            if os.path.isfile(filename) and os.stat(filename).st_size != sizeMB:
                with open(filename, 'wb') as fileW:
                    fileW.write(rand1.read(sizeMB))
        else:
            return rand1.read(sizeMB)
    print('Complete writing/reading random file')
    return


def s_quit(pool):
    pool.close()
    pool.terminate()
    sys.exit(666)

mfile = 10
# mfile = os.environ['MAXFILESIZE'] if os.environ['MAXFILESIZE'] else 10
randomData = create_file('randomFileName', mfile * 1024 * 1024, False)


def manager():
    global randomData
    globalDict = multiprocessing.Manager().dict()
    globalFilesList = multiprocessing.Manager().list()
    globalDict['processes'] = int(os.environ['DISK_IO_PROCESSES'])
    globalDict['MaxFileSize'] = int(os.environ['MAXFILESIZE']) * 1024 * 1024
    globalDict['remove'] = int(os.environ['INITIAL_REMOVE'])
    globalDict['work_path'] = os.environ['WORK_PATH']
    globalDict['debug'] = bool(int(os.environ['DEBUG']))
    globalDict['randomFileName'] = globalDict['work_path'] + "/" + "randomFile"
    old_files = os.walk(globalDict['work_path'])
    if globalDict['debug']:
        for key, value in globalDict:
            print(key, ":", value)
    if globalDict['remove'] != 0:
        for a, b, c in old_files:
            for file_ in c:
                if file_ != 'randomFile':
                    delete_file = globalDict['work_path'] + "/" + file_
                    if globalDict['debug']:
                        print(time(), 'delete', delete_file)
                    try:
                        os.remove(delete_file)
                    except:
                        pass
                    if globalDict['debug']:
                        print(time(), 'deleted' if not os.path.isfile(
                            delete_file) else 'error', delete_file)
    else:
        for a, b, c in old_files:
            for file_ in c:
                if globalDict['debug']:
                    print(time(), 'add', file_)
                if len(file_) == 128:
                    globalFilesList.append(file_)
    input_ = []
    for id in range(globalDict['processes']):
        input_.append([globalDict, globalFilesList,
                       id])
    if globalDict['debug']:
        print(input_)
    try:
        pool = multiprocessing.Pool(globalDict['processes'])  # херачим пул
        pool.map(worker, input_)  # запускаем пул
    except KeyboardInterrupt:
        s_quit(pool)


def logsgenerator():
    import sys
    syms = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', ' ', 'o', 'p', 'q', 'r', 's', 't', '-', '!', '"', '$', '/',
            '=', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6',
            '7', '8', '9', '0']

    counter = 0
    delta = randint(100, 600)
    time1 = time()
    while True:
        string = ""
        l = randint(0, 666)
        while l != 0:
            string += syms[randint(0, len(syms) - 1)]
            l -= 1
        print(string)
        counter += 1
        if counter % 1000 == 0:
            # print(time() - time1)
            if time() - time1 > delta:
                print(counter)
                sys.exit(12)


if __name__ == "__main__":
    print(os.getenv("GENERATE_SOME_LOGS"))
    if os.getenv("GENERATE_SOME_LOGS") == "1":
        # if randint(6666666666666666) % 48597 == 0:
        logsgenerator()
    else:
        manager()
