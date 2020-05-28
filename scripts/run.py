from surver import surv
from threading import Thread

def main():
    ip = # { Adress of FTP server }
    img_folder = # { Directory where to store the pictures }
    user = #  { Username of FTP server }
    pwd = # { Password of FTP server }
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
