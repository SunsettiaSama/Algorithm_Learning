import threading
import time

def print_letter(letter, sem_current, sem_next, count):
    for _ in range(count):
        sem_current.acquire()      # 等待自己的许可
        print(letter, end='', flush=True)
        sem_next.release()         # 唤醒下一个线程

def main():
    total_cycles = 5               # 每个字母打印几次，总输出长度 = total_cycles * 3
    sem_A = threading.Semaphore(1) # A 初始可用
    sem_B = threading.Semaphore(0)
    sem_C = threading.Semaphore(0)

    tA = threading.Thread(target=print_letter, args=('A', sem_A, sem_B, total_cycles))
    tB = threading.Thread(target=print_letter, args=('B', sem_B, sem_C, total_cycles))
    tC = threading.Thread(target=print_letter, args=('C', sem_C, sem_A, total_cycles))

    tA.start()
    tB.start()
    tC.start()

    tA.join()
    tB.join()
    tC.join()
    print()   # 换行

if __name__ == '__main__':
    main()







import threading 
import time

def print_letter(letter, sem_current, sem_next, count):

    for _ in range(count):
        sem_current.acquire()
        print(letter, end = "", flush = True)
        sem_next.release()

def main():
    total_cycle = 5

    sem_A = threading.Semaphore(1)
    sem_B = threading.Semaphore(0)
    sem_C = threading.Semaphore(0)

    tA = threading.Thread(target = print_letter, args = ("A", sem_A, sem_B, total_cycle))
    tB = threading.Thread(target = print_letter, args = ("B", sem_B, sem_C, total_cycle))
    tC = threading.Thread(target = print_letter, args = ("C", sem_C, sem_A, total_cycle))

    tA.start()
    tB.start()
    tC.start()

    tA.join()
    tB.join()
    tC.join()

    print()

if __name__ == '__main__':
    main()



import threading
import time

def print_letter(letter, sem_a: threading.Semaphore, sem_b: threading.Semaphore, count):
    for _ in range(count):
        sem_a.acquire()
        print(letter, end = "")
        sem_b.release()

    return 

def main():
    count = 5

    sem_a = threading.Semaphore(1)
    sem_b = threading.Semaphore(0)
    sem_c = threading.Semaphore(0)

    tA = threading.Thread(target = print_letter, args = ("A", sem_a, sem_b, count))
    tB = threading.Thread(target = print_letter, args = ("B", sem_b, sem_c, count))
    tC = threading.Thread(target = print_letter, args = ("C", sem_c, sem_a, count))
    
    tA.start()
    tB.start()
    tC.start()

    tA.join()
    tB.join()
    tC.join()

    print()

if __name__ == '__main__':
    main()


