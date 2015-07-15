__author__ = 'orlando'

import dropbox


class dropbox_log(dropbox.client.DropboxClient):


    def __init__(self,access_token,folder):
        try:
            dropbox.client.DropboxClient.__init__(self,access_token)
            self.db_folder = folder
        except:
            print "No se pudo configurar el token"


    def send_overwrite(self,folder,filename,db_folder):
        print 'linked account: ', self.info_cuenta()
        try:
            f = open(folder + filename, 'rb')
        except IOError:
            return -1

        try:
            response = self.put_file(db_folder+filename, f,overwrite = True)
            print "uploaded:", response
        except:
            print "No se pudo enviar el archivo"
        f.close()

    def info_cuenta(self):
        print 'linked account: ', self.account_info()


if __name__ == "__main__":
    folder = '/mnt/sda1'
    access_token = 'QL-hU5_KShUAAAAAAAALMCIFlNcHRN-GQQOA3PvGtaShc_EPlakjUhyJD026tmLT'
    p=dropbox_log(access_token,folder)
    #p.send_overwrite()
    print p.info_cuenta()
    print p.db_folder