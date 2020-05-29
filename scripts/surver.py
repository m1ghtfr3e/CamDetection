import os
import ftplib
import cv2

class surv:

    def __init__(self, ftp, path, user, pwd, target_folder='./ftpsurv/',):
        self._ftp = ftp
        self._path = path
        self._user = user
        self._pwd = pwd
        self.target_folder = target_folder
        self.faces = target_folder + 'faces/'    # Own folder for detected faces
        self._detect = '20200529/detect'

    def fetch_FTP(self):

        ''' Pictures from IP camera
            are saved on a local FTP;
            This method fetches those
            pictures and saves them
            in default or specified
            folder -> target_folder;
        '''

        ftp = ftplib.FTP()
        ftp.connect(self._ftp)
        ftp.login(self._user, self._pwd)
        ftp.cwd(self._path)
        
        files = ftp.nlst()

        def fetch(files):

            ''' Process to fetch
                is just started if 
                directory is not
                empty;
            '''
    
            for f in files:
                ftp.retrbinary('RETR %s' %f , open(self.target_folder + f, 'wb').write)

                # Deleting pictures from ftp server when finished
                ftp.delete(f)
            print('[+] All files fetched and deleted.\n')

        # Define when to fetch files
        if len(files) > 0:
            fetch(files)
        else:
            pass

        return

    def upload_FTP(self):

        ftp = ftplib.FTP()
        ftp.connect(self._ftp)
        ftp.login(self._user, self._pwd)
        ftp.cwd(self._detect)

        for f in os.listdir(self.faces):
            print(f)
            ff = open(self.faces + f, 'rb')
            ftp.storbinary('STOR %s' %f, ff)
        print('[+] Detection pictures uploaded to FTP successfully.\n')

        return

    def detect_faces(self):

        ''' Detecting faces on
            the saved pictures;
            Results are saved in
            an own folder:
            self.faces -> ./faces/;
        '''
        cv2.useOptimized()

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

        print('[+] Starting detection.\n')

        # Iterating through all pictures in directory and perform face detection
        for root, dirs, files in os.walk(self.target_folder):
            for fname in files:
                src = os.path.join(root, fname)
                img = cv2.imread(src)
                
                # In order to find faces, gray pictures are needed
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Defining the MultiScale
                faces = face_cascade.detectMultiScale(gray, 1.05, 3)

                for (x, y, w, h) in faces:
                    # Drawing a green rectangle around found faces
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Saving detected faces in own folder
                    crop_face = img[y:y+h, x:x+w]

                cv2.imwrite(self.faces + fname, img)
                cv2.imwrite(self.faces + '/crop/' + fname, crop_face)
        print('[+] Detected pictures saved.\n')
        return
