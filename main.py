import string
import random
import os
import sys
import threading 
import httplib2
import time

if not os.path.exists('Image'):
    os.makedirs('Image')

if len(sys.argv) < 2:
    sys.exit("\033[37mUsage: python3 " + sys.argv[0] + " (Number of threads)")
THREAD_AMOUNT = int(sys.argv[1])

print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\nThis script is for educational purposes only! Use on your own responsibility!\n=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=")
input("Press ENTER if you have read and accept that you are fully responsible for using this script!\n")

INVALID = [0, 503, 5082, 4939, 4940, 4941, 12003, 5556]

def scrape_pictures(thread_id):
    while True:
        url = 'http://i.imgur.com/'
        length = random.choice((5, 6))
        
        if length == 5:
            url += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
        else:
            url += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))
            url += ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))
        
        url += '.jpg'

        filename = url.rsplit('/', 1)[-1]
        file_path = os.path.join('Image', filename) 

        h = httplib2.Http('.cache' + str(thread_id))
        response, content = h.request(url)

        if response.status == 200:
            with open(file_path, 'wb') as out:
                out.write(content)

            file_size = os.path.getsize(file_path)
            if file_size in INVALID:
                print("[-] Invalid: " + url)
                os.remove(file_path)
            else:
                print("[+] Valid: " + url)
        else:
            print(f"[-] Failed to download {url}: {response.status}")

threads = []

for i in range(1, THREAD_AMOUNT + 1):
    try:
        thread = threading.Thread(target=scrape_pictures, args=(i,))
        thread.start()
        threads.append(thread)
    except Exception as e:
        print(f'Error starting thread {i}: {e}')

print(f'Successfully started {THREAD_AMOUNT} threads.')

for thread in threads:
    thread.join()
