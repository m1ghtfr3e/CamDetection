import time
import getpass
from surver import surv
from threading import Thread


def getFTP(obj):

    fetch = Thread(target=obj.fetch_FTP)
    fetch.daemon = True
    fetch.start()
    fetch.join()
    
    return

def detect(obj):

    det = Thread(target=obj.detect_faces)
    det.daemon = True
    det.start()
    det.join()

    return

def upFTP(obj):

    upl = Thread(target=obj.upload_FTP)
    upl.daemon = True
    upl.start()
    upl.daemon()

    return

def main(obj):

    try:

        while True:
            getFTP(obj)
            detect(obj)
            upFTP(obj)

            print('[+] Waiting for 300 sec now.\n')

            # Change number (seconds) due to your preferences
            time.sleep(300)

    except Exception:
        raise Exception

    except KeyboardInterrupt:
        print('[!] Program manually stopped.\n')

    return


if __name__ == '__main__':

    ip = input('IP of FTP server: ')
    img_folder = input('Folder to download from: ')
    user = input('Username of FTP: ')
    pwd = getpass.getpass()

    # Initalizing surv obj
    S = surv(ip, img_folder, user, pwd)

    # Giving the class object as parameter to func
    main(S)
