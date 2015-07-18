__author__ = 'orlando'

import re
import urllib
import socket
import twitter_alarm
from math import sqrt
from time import localtime, strftime

class webserver():
    var_dict={}
    T3_low_enviado = False
    T3_high_enviado = False
    T4_low_enviado = False
    T4_high_enviado = False
    T8_low_enviado = False
    T8_high_enviado = False
    P0_P7_low_enviado = False
    P0_P7_med_low_enviado = False
    P0_P7_med_high_enviado = False
    P0_P7_high_enviado = False
    apiKey_tw = 'wwQbSJIMe8R9pT6xgIUcubBje'
    apiSecret_tw = 'YOPH52doq7TbltkniTOwcEP8KNYirX8qbqdONXuIgKIxEjUNce'
    accessToken_tw = '3378120419-Lu7iqOnDTOEk4g3YzipgjRCwiLVqVkbhuEapIm0'
    accessTokenSecret_tw = '0H19jwVd8r5YweA0YDKrNhBDBaPrsF8rStg4tlaYAeicw'

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
        self.tw_alarm = twitter_alarm.twitter_alarm(self.apiKey_tw,self.apiSecret_tw,self.accessToken_tw,self.accessTokenSecret_tw) #inicio el servidor de twitter
        self.tw_alarm.send_message('El datalogger se encuentra funcionando')

    def pull(self):


        for i in self.variables: #itero sobre las variables para obtener los valores
                url = self.main_address + i + ".html"
                try:
                    htmlfile = urllib.urlopen(url) #abro la pagina web y leo la pagina
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
                #print i , ":", self.var_dict[i]

        #print 'comienzo a calcular'
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

        self.alarmas()
        return self.var_dict

    def calculate_dp_total(self): #en este metodo calculo la variable dp total
        P0 = self.var_dict['P0']
        P7 = self.var_dict['P7']

        self.var_dict['dp_tot'] = round(float(P0-P7),1)

        return self.var_dict['dp_tot']

    def calculate_inlet(self):
        P0 = self.var_dict['P0']
        P2 = self.var_dict['P2']

        self.var_dict['inlet'] = round(float(P0-P2),1)

        return self.var_dict['inlet']

    def calculate_bell(self):
        P2 = self.var_dict['P2']
        P4 = self.var_dict['P4']

        self.var_dict['bell'] = round(float(P2 - P4),1)

        return self.var_dict['bell']

    def calculate_cyclon(self):
        P4 = self.var_dict['P4']
        P5 = self.var_dict['P5']

        self.var_dict['cyclon'] = round(float(P4-P5),1)

        return self.var_dict['cyclon']

    def calculate_qin(self):
        P0 = self.var_dict['P0']
        P2 = self.var_dict['P2']

        if P0 != P2 and P2 < P0 :
            self.var_dict['Qin'] = round(float(0.259*0.001520531*sqrt(2*(P0-P2)*100/1.17)*3600),1) #hace el calculo redondeado a 1 decimal
        else:
            self.var_dict['Qin'] = 0

        return self.var_dict['Qin']

    def calculate_packing(self):
        P0 = self.var_dict['P0']
        P7 = self.var_dict['P7']
        P2 = self.var_dict['P2']
        P4 = self.var_dict['P4']

        if (P0-P7)>=5 and (P2-P4)!=0:
            self.var_dict['packing'] = round(float((P0-P2)/(P2-P4)),1)
        else:
            self.var_dict['packing'] = 0

        return self.var_dict['packing']

    def calculate_inlet_per(self):
        dp_tot = self.var_dict['dp_tot']

        if dp_tot != 0 and dp_tot > 0 :
            self.var_dict['inlet_per'] = round(float(self.calculate_inlet() / dp_tot),1)
        else:
            self.var_dict['inlet_per'] = 0

        return self.var_dict['inlet_per']

    def calculate_bell_per(self):
        dp_tot = self.var_dict['dp_tot']

        if dp_tot != 0 and dp_tot > 0 :
            self.var_dict['bell_per'] = round(float(self.calculate_bell()/dp_tot),1)
        else:
            self.var_dict['bell_per'] = 0
        return self.var_dict['bell_per']

    def calculate_cylon_per(self):
        dp_tot = self.var_dict['dp_tot']

        if dp_tot != 0 and dp_tot > 0:
            self.var_dict['cyclon_per'] = round(float(self.calculate_cyclon()/dp_tot),1)
        else:
            self.var_dict['cyclon_per'] = 0
        return self.var_dict['cyclon_per']

    def calculate_cooler_filt1(self):
        P5 = self.var_dict['P5']
        P6 = self.var_dict['P6']

        self.var_dict['cooler_filt1'] = round(float(P5 - P6),1)
        return self.var_dict['cooler_filt1']

    def calculate_cooler_filt1_per(self):
        dp_tot = self.var_dict['dp_tot']

        if dp_tot != 0 and dp_tot > 0:
            self.var_dict['cooler_filt1_per'] = round(float(self.calculate_cooler_filt1()/dp_tot),1)
        else:
            self.var_dict['cooler_filt1_per'] = 0
        return self.var_dict['cooler_filt1_per']

    def calculate_filt2(self):
        P6 = self.var_dict['P6']
        P7 = self.var_dict['P7']

        self.var_dict['filt2'] = round(float(P6-P7),1)

        return self.var_dict['filt2']

    def calculate_filt2_per(self):
        dp_tot = self.var_dict['dp_tot']

        if dp_tot != 0 and dp_tot > 0:
            self.var_dict['filt2_per'] = round(float(self.calculate_filt2()/dp_tot),1)
        else:
            self.var_dict['filt2_per'] = 0
        return self.var_dict['filt2_per']

    def calculate_qout(self):
        Qin = self.var_dict['Qin']

        if Qin != 0 :
            self.var_dict['Qout'] = round(float(2.17*Qin),2)
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
        self.pull()
        datastr = date + ","

        for i in self.variables_calc:
            datastr += str(self.var_dict[i]) #lleno el datastring con las variables
            if not self.variables_calc[len(self.variables_calc) - 1] == i:  #si no es la ultima variable arreglo una coma
                datastr += ","
        datastr += "\n"
        print datastr
        return datastr

    def alarmas(self): #esta funcion es la que levanta las banderas de las alarmas y envia los mensajes a twitter
        #defino los threshold
        T3_high = 1100
        T3_low = 800
        T4_high =500
        T4_low  = 400
        T8_high = 170
        P0_P7_high = 100
        P0_P7_medium = 60
        P0_P7_low = 40

        #analizo las alarmas de T3
        T3 = self.var_dict['T3']

        if T3 < T3_high and T3 > T3_low: #Si el valor se encuntra dentro de de esos rangos
            #reseteo las banderas
            self.T3_high_enviado = False
            self.T3_low_enviado = False
        else:
            if T3 > T3_high and self.T3_high_enviado == False:
                self.tw_alarm.send_message('T3 se encuentra por encima de '+str(T3_high)+'. T3='+str(T3))
                self.T3_high_enviado =True
            if T3 < T3_low and self.T3_low_enviado == False:
                self.tw_alarm.send_message('T3 se encuentra por debajo de ' + str(T3_low)+ '. T3='+str(T3))
                self.T3_low_enviado = True

        #analizo las alarmas de T4
        T4 = self.var_dict['T4']

        if T4 < T4_high and T4 > T4_low: #Si el valor se encuntra dentro de de esos rangos
            #reseteo las banderas
            self.T4_high_enviado = False
            self.T4_low_enviado = False
        else:
            if T4 > T4_high and self.T4_high_enviado == False:
                self.tw_alarm.send_message('T4 se encuentra por encima de '+str(T4_high) +'. T4='+ str(T4))
                self.T4_high_enviado =True
            if T4 < T4_low and self.T4_low_enviado == False:
                self.tw_alarm.send_message('T4 se encuentra por debajo de ' +str(T4_low) +'. T4=' + str(T4))
                self.T4_low_enviado = True

        #analizo las alarmas de T8
        T8 = self.var_dict['T8']

        if T8 < T8_high and self.T8_low_enviado == False: #Si el valor se encuntra por debajo del limite
            self.tw_alarm.send_message('T8 se encuentra por debajo de ' +str(T8_high) + '. T8=' + str(T8))
            self.T8_low_enviado = True
            self.T8_high_enviado = False
        if T8 > T8_high and self.T8_high_enviado == False:
            self.tw_alarm.send_message('T8 se encuentra por encima de ' +str(T8_high) + '. T8=' + str(T8))
            self.T8_high_enviado = True
            self.T8_low_enviado = False

        #analizo las alarmas de P0-P7
        P0_P7 = round(float(abs(self.var_dict['P0']-self.var_dict['P7'])),1)

        if P0_P7 <P0_P7_low and self.P0_P7_low_enviado == False: #si P0-P7 esta por debajo del valor minimo
            self.tw_alarm.send_message('P0-P7 se encuentra por debajo de ' + str(P0_P7_low) + '. P0-P7=' + str(P0_P7))
            self.P0_P7_low_enviado = True
            self.P0_P7_high_enviado = False
            self.P0_P7_med_low_enviado = False
            self.P0_P7_med_high_enviado = False

        if P0_P7 > P0_P7_high and self.P0_P7_high_enviado == False: #si P0-P7 esta por encima del valor maximo
            self.tw_alarm.send_message('P0-P7 se encuentra por encima de ' + str(P0_P7_high) + '. P0-P7=' + str(P0_P7))
            self.P0_P7_high_enviado = True
            self.P0_P7_low_enviado = False
            self.P0_P7_med_low_enviado = False
            self.P0_P7_med_high_enviado = False

        if P0_P7 > P0_P7_low and P0_P7 < P0_P7_high:
            if P0_P7 < P0_P7_medium and self.P0_P7_med_low_enviado == False:
                self.tw_alarm.send_message('P0-P7 es mayor que ' + str(P0_P7_low) + ' Y esta por debajo de ' + str(P0_P7_medium) + '. P0-P7=' + str(P0_P7))
                self.P0_P7_med_low_enviado = True
                self.P0_P7_med_high_enviado = False
                self.P0_P7_high_enviado == False
                self.P0_P7_low_enviado == False
            if P0_P7 > P0_P7_medium and self.P0_P7_med_high_enviado == False:
                self.tw_alarm.send_message('P0-P7 es mayor que ' + str(P0_P7_low) + ' Y esta por encima de ' + str(P0_P7_medium) + '. P0-P7=' + str(P0_P7))
                self.P0_P7_med_high_enviado = True
                self.P0_P7_med_low_enviado = False
                self.P0_P7_high_enviado == False
                self.P0_P7_low_enviado == False



            #comienzo a revisar las variables


            #comenzamos a analizar las condiciones de las banderas











if __name__ == "__main__":
    var = ['T1','T3','T4','T8','T12','T13','T14','P0','P2','P4','P5','P6','P7','O1','O2']
    p=webserver("http://46.229.95.116/awp/PulseDynamics/IO/IO_",var,2)
    print p.pull_datastring()



