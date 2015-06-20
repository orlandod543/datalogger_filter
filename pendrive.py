__author__ = 'orlando'

import os

class pendrive():
    filepath=''

    def __init__(self,filepath):
        self.filepath = filepath

    def write_append(self,filename,data):
        try:
            with open(self.filepath+filename,"a") as file_descriptor:
                file_descriptor.write(data)
                print data
                file_descriptor.close()
                print 'se ha grabado la informacion en' + self.filepath + filename
            return 0
        except IOError:
            print ' no se puede escribir en el archivo'
            return -1

    def create_file_header(self,filename,header):
        if os.path.isfile(self.filepath+filename) == False: #pregunto si el archivo existe
            print "creando el archivo nuevo"

        try:
            with open(self.filepath+filename,'w') as file_descriptor:
                file_descriptor.write(header) #escribo el header en el archivo
                file_descriptor.close()

        except IOError:
           print " No se puede abrir el archivo"

    def abrir_apuntador_archivo(self,filename):
        try:
            with open(self.filepath+filename,"rb") as file_descriptor:
                return file_descriptor

        except IOError:
            return -1

    def cerrar_apuntador_archivo(self,file_descriptor):
        file_descriptor.close


    def file_exists(self,filename):
        return os.path.isfile(self.filepath+filename) #pregunto si el archivo existe



    def address(self):
        return self.filepath




if __name__ == "__main__":
    p=pendrive('/home/orlando/dataloggerweb/')
    print p.address()
    if p.file_exists('holaprueba'):
        p.write_append('holaprueba','213123'+'\n')
    else:
        p.create_file_header('holaprueba','esto es una prueba para saber si esta funcionando todo'+'\n')
