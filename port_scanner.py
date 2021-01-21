import socket
import argparse
from threading import Thread
import time

threadpool_job_list = []
go = True



def get_args(args):
    if args.domain:
        domains = [str(args.domain)]
    elif args.domains:
        domains = [d for d in args.domains.split(',')]
    else:
        quit("no domain specified")

    if args.port:
        p = int(args.port)
        ports = [p,p]
    elif args.ports:
        if int(args.ports) == -1:
            ports = [0, 65535]
        else:
            ports = [int(p) for p in args.ports.split(',')]
    else:
        quit("no port specified")

    if args.threads:
        threads = int(args.threads)
    else:
        threads = 10

    return (domains,ports,threads)


def check_port_open(host,port):
    try:
        sock = socket.socket()
        sock.connect((host,port))
        open=True
    except:
        open=False
    try:
        sock.close()
    except:
        time.sleep(0.5)
    return open


def workthread_function(wait_time):
    global threadpool_job_list, go
    time.sleep(2*wait_time)
    while go:
        if not go: return -1
        try:
            (host,port) = threadpool_job_list.pop(0)
            if check_port_open(host, port):
                print(f"{host} is open on port {port}"," "*10)
            else:
                print(f"{host} is closed on port {port}"," "*5, end="\r")
        except IndexError:
            time.sleep(1)
        except KeyboardInterrupt:
            go = False

def main():
    global go
    parser=argparse.ArgumentParser()
    parser.add_argument("-D", "--domains", help="comma seperated list of domains to scan")
    parser.add_argument("-d", "--domain", help="single domain to scan (priority if both specified)")
    parser.add_argument("-P", "--ports", help="comma seperated list of start and end ports to scan (-1 for all)")
    parser.add_argument("-p", "--port", help="single port to scan (priority if both specified)")
    parser.add_argument("-t", "--threads", help="how many threads to use (default 10)")

    args=parser.parse_args()
    (domains, ports, threads) = get_args(args)

    threadpool = []
    for thr in range(threads):
        threadpool.append(Thread(target=workthread_function, args=[thr/threads]))
        threadpool[thr].start()

    try:
        for host in domains:
            for port in range(ports[0],ports[1]+1):
                threadpool_job_list.append((host,port))
                if not go:
                    return -1
                if len(threadpool_job_list) > threads*5:
                    time.sleep(0.5)
    except KeyboardInterrupt:
        go = False

    while len(threadpool_job_list) > 0:
        time.sleep(1)
    go = False
    for thr in range(threads):
        threadpool[thr].join()

if __name__ == "__main__":
    main()
