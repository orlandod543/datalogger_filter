__author__ = 'orlando'

import os

class pendrive():
    filepath=''

    def __init__(self,filepath):
        self.filepath = filepath

    def write_append(self,filename,data):
        """
        method that append a string to a file
        If there is an error, catches it and does nothing
        Input: str filename, str data
        Output: None
        """
        try:
            with open(self.filepath+filename,"a") as file_descriptor:
                file_descriptor.write(data)
                file_descriptor.close()
        except IOError:
            pass
        return None

    def create_file_header(self,filename,header):
        """
        Creates the file header.
        Raises IOError if it fails
        Input: str filename, str header
        Output: None
        """
        try:
            with open(self.filepath+filename,'w') as file_descriptor:
                file_descriptor.write(header) #escribo el header en el archivo
                file_descriptor.close()
        except IOError:
           pass
        return None


    def file_exists(self,filename):
        """
        Check if filename file_exists
        Input: str filename
        Output: bool
        """
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
