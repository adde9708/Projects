from multiprocessing import Process, Pipe
import time


def reader_proc(pipe):
    p_output, p_input = pipe

    p_input.close()
    while True:
        msg = p_output.recv()
        if msg == 'DONE':
            break


def writer(count, p_input):
    for i in range(count):
        p_input.send(i)
    p_input.send('DONE')


if __name__ == '__main__':

    for count in [10 ** 4, 10 ** 5, 10 ** 6]:
        p_output, p_input = Pipe()
        reader_p = Process(target=reader_proc, args=((p_output, p_input),))
        reader_p.daemon = True
        reader_p.start()
        _start = time.time()
        writer(count, p_input)
        p_output.close()
        reader_p.join()
        print("Sending {0} numbers to Pipe() took {1} seconds".format(count, (time.time() - _start)))
