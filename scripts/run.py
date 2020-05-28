from surver import surv
from threading import Thread

def main():
    ip = '192.168.178.1'
    img_folder = '20200528/images'
    user = 'surv'
    pwd = 'survpasswort'
    s = surv(ip, img_folder, user, pwd)

    # Getting the pictures
    p1 = Thread(target=s.get_fromFTP())
    # Detecting faces on pictures
    p2 = Thread(target=s.detect_faces())


    p1.start()
    p2.start()

    p1.join()
    p2.join()


if __name__ == '__main__':

    main()