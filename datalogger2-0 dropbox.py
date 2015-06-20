import urllib
import re
import time
import dropbox

time_sample = 30 # defino el tiempo de muestreo

app_key = 'esipcaghf8ayg6m'
app_secret = '66hyaeakvpzrrxc'
access_token = 'QL-hU5_KShUAAAAAAAALMCIFlNcHRN-GQQOA3PvGtaShc_EPlakjUhyJD026tmLT'
access_token_pd = 'oEgHuggfnPAAAAAAAAACOOkjlzybdPgSd8ZPWHkxqUA9d-bnthhTaY_BSJiZoX5D'
regex = '\n\n(.+?)\r\n0'
pattern = re.compile(regex,re.MULTILINE)#creo los patrones de busqueda
pendrive = "/run/media/orlando/orlando/"
db_folder = "/mnt/sda1/"



try:
    var_file = open("variables") #abro el archivo que contendra las variables a buscar
except:
    print " no se consigue el archivo de variables, por favor cree uno"
else:
    variables=var_file.read()  #leo las variables y las cargo en un arreglo
    var_file.close()
    variables = variables.split("\n") # me deshago del ultimo valor que es linea nueva
    variables = filter(None,variables) # me deshago de los valores vacios si los hubiera
    var_dict = {}
    
    for i in variables:
        var_dict[i] = int(0) #inicializo el diccionario en cero todo
    print var_dict
    pull = True #esta variable me indica cuando debo de hacer un pull de datos

    db_counter = 0
    while True:
        
        #Esta es la parte que obtiene los datos del servidos

        
        while pull:
            from time import localtime, strftime
            date = strftime("%y-%m-%d-%H:%M:%S", localtime()) #obtengo la hora del momento de la toma de muestras 
            print date
            for i in variables:
                url = "http://46.229.95.116/awp/PulseDynamics/IO/IO_" + i + ".html"
                try:
                    htmlfile = urllib.urlopen(url)
                    htmltext = htmlfile.read()
                except IOError:
                    print "no se puede acceder a la pagina"
                else:
                    #print i
                    valor = re.findall(pattern,htmltext) #busco el valor de acuerdo al patron dado
                    if not valor[0] == []:#si el valor no es vacio(osea encontro un match)
                    #    print valor[0]
                        var_dict[i] = int(round(float(valor[0]))) #guardo la variable como un entero en el diccionario
                    else:
                        var_dict[i] = int(0) #de lo contrario guardo 0
                print i , ":", var_dict[i]
            pull=False

        #       Esta es la parte que grava los datos al pendrive    
        import os
        if os.path.isfile(pendrive+date[:8]+".txt") == False: #pregunto si el archivo existe
            print "creando el archivo nuevo"
            try:
                f = open(pendrive+date[:8]+".txt", "w") #abro el archivo y creo la cabecera
            except IOError:
                print " No se puede abrir el archivo"
            else:
                datastr = "YY-MM-DD-HH:MM:SS," #escribo las variables obtenidas 
                for i in variables:
                    datastr += i #lleno el datastring con las variables
                    if not variables[len(variables) - 1] == i:  #si no es la ultima variable arreglo una coma
                        datastr += ","
                datastr += "\n" #al final de agregar las variables agrego una nueva linea    ]
                print datastr
                try:
                    f.write(datastr)
                except IOError:
                    print ' no se puede escribir en el archivo'
                f.close()                   
        else:
            try:
                f = open(pendrive+date[:8]+".txt","a") # abro el archivo para escritura
            except IOError:
                print " No se puede abrir el archivo"
            else:
                datastr = date + "," #empiezo a crear el datastring
                
                for i in variables:
                    datastr += str(var_dict[i]) #lleno el datastring con las variables
                    if not variables[len(variables) - 1] == i:  #si no es la ultima variable arreglo una coma
                        datastr += ","
                datastr += "\n" #al final de agregar las variables agrego una nueva linea
                print datastr
                try:
                    f.write(datastr)
                except IOError:
                    print ' no se puede escribir en el archivo'
                f.close()

        #Esta es la parte de dropbox
        if db_counter >= 0:
            client = dropbox.client.DropboxClient(access_token)
            print '\n'
            print 'linked account orlando: ', client.account_info()
        
            f = open(pendrive + date[:8] + ".txt", 'rb')
            response = client.put_file(db_folder + date[:8]+ ".txt", f,overwrite = True)
            print '\n'
            print "uploaded orlando:", response
            f.close()
            
            client_pd = dropbox.client.DropboxClient(access_token_pd)
            print '\n'
            print 'linked account pd: ', client_pd.account_info()
            
            f = open(pendrive + date[:8] + ".txt", 'rb')
            response_pd = client_pd.put_file(db_folder + date[:8]+ ".txt", f,overwrite = True)
            print '\n'
            print "uploaded pd:", response_pd
            f.close()
            db_counter = 0
        #Esta es la parte que hace el resto
        db_counter += 1
        time.sleep(30)
        pull=True
    
        
    



