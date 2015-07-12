__author__ = 'orlando'

import re
import urllib
import socket

from math import sqrt
from time import localtime, strftime

class webserver():
    var_dict={}

    def __init__(self,main_address,variables,timeout):
        self.main_address = main_address #asigno la direccion del servidor
        self.variables = variables # asigno el tuple de variables que buscar en el servidor
        #Variables_cal contiene la lista de variables del servidor mas las que hay que calcular
        self.variables_calc = []
        for i in self.variables:
            self.variables_calc.append(i)

        self.variables_calc.append('Qin') #anexo las variables a calcular
        self.variables_calc.append('inlet')
        self.variables_calc.append('inlet_per')
        self.variables_calc.append('bell')
        self.variables_calc.append('bell_per')
        self.variables_calc.append('packing')
        self.variables_calc.append('cyclon')
        self.variables_calc.append('cyclon_per')
        self.variables_calc.append('cooler_filt1')
        self.variables_calc.append('cooler_filt1_per')
        self.variables_calc.append('filt2')
        self.variables_calc.append('filt2_per')
        self.variables_calc.append('dp_tot')
        self.variables_calc.append('Qout')
        self.variables_calc.append('ATEX')

        self.timeout = timeout #asigno el timeout de cada conexion
        socket.setdefaulttimeout(self.timeout) #defino el timeout del url

        for i in self.variables_calc:
            self.var_dict[i] = ''


        regex = '\n\n(.+?)\r\n0'
        self.pattern = re.compile(regex,re.MULTILINE)#creo los patrones de busqueda


    def pull(self):


        for i in self.variables:
                url = self.main_address + i + ".html"
                try:
                    htmlfile = urllib.urlopen(url)
                    htmltext = htmlfile.read()
                except IOError:
                    print "no se puede acceder a la pagina"
                    self.var_dict[i] = int(-1)
                else:
                    #print i
                    valor = re.findall(self.pattern,htmltext) #busco el valor de acuerdo al patron dado
                    if not valor[0] == []:#si el valor no es vacio(osea encontro un match)
                    #    print valor[0]
                        self.var_dict[i] = round(float(valor[0]),1) #guardo la variable como un entero en el diccionario
                    else:
                        self.var_dict[i] = int(0) #de lo contrario guardo 0
                print i , ":", self.var_dict[i]

        print 'comienzo a calcular'
        self.calculate_dp_total()
        self.calculate_qin()
        self.calculate_inlet()
        self.calculate_inlet_per()
        self.calculate_bell()
        self.calculate_bell_per()
        self.calculate_cyclon()
        self.calculate_cylon_per()
        self.calculate_packing()
        self.calculate_cooler_filt1()
        self.calculate_cooler_filt1_per()
        self.calculate_filt2()
        self.calculate_filt2_per()
        self.calculate_qout()
        self.calculate_ATEX()

        return self.var_dict

    def calculate_dp_total(self): #en este metodo calculo la variable dp total
        P0 = self.var_dict['P0']
        P7 = self.var_dict['P7']

        self.var_dict['dp_tot'] = P0-P7

        return self.var_dict['dp_tot']

    def calculate_inlet(self):
        P0 = self.var_dict['P0']
        P2 = self.var_dict['P2']

        self.var_dict['inlet'] = P0-P2

        return self.var_dict['inlet']

    def calculate_bell(self):
        P2 = self.var_dict['P2']
        P4 = self.var_dict['P4']

        self.var_dict['bell'] = P2 - P4

        return self.var_dict['bell']

    def calculate_cyclon(self):
        P4 = self.var_dict['P4']
        P5 = self.var_dict['P5']

        self.var_dict['cyclon'] = P4-P5

        return self.var_dict['cyclon']

    def calculate_qin(self):
        P0 = self.var_dict['P0']
        P2 = self.var_dict['P2']

        if P0 != P2 and P2 < P0 :
            self.var_dict['Qin'] = 0.259*0.001520531*sqrt(2*(P0-P2)*100/1.17)*3600
        else:
            self.var_dict['Qin'] = 0

        return self.var_dict['Qin']

    def calculate_packing(self):
        P0 = self.var_dict['P0']
        P7 = self.var_dict['P7']
        P2 = self.var_dict['P2']
        P4 = self.var_dict['P4']

        if (P0-P7)>=5 and (P2-P4)!=0:
            self.var_dict['packing'] = (P0-P2)/(P2-P4)
        else:
            self.var_dict['packing'] = 0

        return self.var_dict['packing']

    def calculate_inlet_per(self):
        dp_tot = self.var_dict['dp_tot']

        if dp_tot != 0 and dp_tot > 0 :
            self.var_dict['inlet_per'] = self.calculate_inlet() / dp_tot
        else:
            self.var_dict['inlet_per'] = 0

        return self.var_dict['inlet_per']

    def calculate_bell_per(self):
        dp_tot = self.var_dict['dp_tot']

        if dp_tot != 0 and dp_tot > 0 :
            self.var_dict['bell_per'] = self.calculate_bell()/dp_tot
        else:
            self.var_dict['bell_per'] = 0
        return self.var_dict['bell_per']

    def calculate_cylon_per(self):
        dp_tot = self.var_dict['dp_tot']

        if dp_tot != 0 and dp_tot > 0:
            self.var_dict['cyclon_per'] = self.calculate_cyclon()/dp_tot
        else:
            self.var_dict['cyclon_per'] = 0
        return self.var_dict['cyclon_per']

    def calculate_cooler_filt1(self):
        P5 = self.var_dict['P5']
        P6 = self.var_dict['P6']

        self.var_dict['cooler_filt1'] = P5 - P6
        return self.var_dict['cooler_filt1']

    def calculate_cooler_filt1_per(self):
        dp_tot = self.var_dict['dp_tot']

        if dp_tot != 0 and dp_tot > 0:
            self.var_dict['cooler_filt1_per'] = self.calculate_cooler_filt1()/dp_tot
        else:
            self.var_dict['cooler_filt1_per'] = 0
        return self.var_dict['cooler_filt1_per']

    def calculate_filt2(self):
        P6 = self.var_dict['P6']
        P7 = self.var_dict['P7']

        self.var_dict['filt2'] = P6-P7

        return self.var_dict['filt2']

    def calculate_filt2_per(self):
        dp_tot = self.var_dict['dp_tot']

        if dp_tot != 0 and dp_tot > 0:
            self.var_dict['filt2_per'] = self.calculate_filt2()/dp_tot
        else:
            self.var_dict['filt2_per'] = 0
        return self.var_dict['filt2_per']

    def calculate_qout(self):
        Qin = self.var_dict['Qin']

        if Qin != 0 :
            self.var_dict['Qout'] = 2,17*Qin
        else :
            self.var_dict['Qout'] = 0

        return self.var_dict['Qout']

    def calculate_ATEX(self):
        O1 = self.var_dict['O1']
        O2 = self.var_dict['O2']

        if O1 <500 or O2 <500 :
            self.var_dict['ATEX'] = 'NOK'
        else:
            self.var_dict['ATEX'] = 'OK'

        return self.var_dict['ATEX']

    def pull_datastring(self): #esta funcion hace un pull del webserver y saca de una vez el string de datos
        date = strftime("%H:%M:%S", localtime()) #obtengo la hora del momento de la toma de muestras
        print date
        self.pull()
        datastr = date + ","

        for i in self.variables_calc:
            datastr += str(self.var_dict[i]) #lleno el datastring con las variables
            if not self.variables_calc[len(self.variables_calc) - 1] == i:  #si no es la ultima variable arreglo una coma
                datastr += ","
        datastr += "\n"
        return datastr










if __name__ == "__main__":
    var = ['T1','T3','T4','T8','T12','T13','T14','P0','P2','P4','P5','P6','P7','O1','O2']
    p=webserver("http://46.229.95.116/awp/PulseDynamics/IO/IO_",var,2)
    print p.pull_datastring()



