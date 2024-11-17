import string
import random
import os
import sys
import threading  # изменено для Python 3
import httplib2
import time

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
        
        url += '.jpg'  # добавляем расширение файла .jpg

        filename = url.rsplit('/', 1)[-1]

        h = httplib2.Http('.cache' + str(thread_id))
        response, content = h.request(url)

        if response.status == 200:  # проверяем статус ответа
            with open(filename, 'wb') as out:
                out.write(content)

            file_size = os.path.getsize(filename)
            if file_size in INVALID:
                print("[-] Invalid: " + url)
                os.remove(filename)
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

# Делаем так, чтобы основной поток не завершался
for thread in threads:
    thread.join()
