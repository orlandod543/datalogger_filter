
import time
import dropbox_log
import webserver_pull
import pendrive
from time import localtime, strftime
time_sample = 30 # defino el tiempo de muestreo en seegundos
time_upload_db = 3600 #defino el tiempo de subida a dropbox en segundos tambien

app_key = 'esipcaghf8ayg6m'
app_secret = '66hyaeakvpzrrxc'
access_token = 'QL-hU5_KShUAAAAAAAALMCIFlNcHRN-GQQOA3PvGtaShc_EPlakjUhyJD026tmLT'
access_token_pd = 'oEgHuggfnPAAAAAAAAACOOkjlzybdPgSd8ZPWHkxqUA9d-bnthhTaY_BSJiZoX5D'

pendrivepath = '/home/orlando/dataloggerweb/'
#pendrivepath = "/media/pendrive/"
db_folder = "/mnt/sda1/"

url = "http://46.229.95.116/awp/PulseDynamics/IO/IO_"
timeout = 2


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

    webserver=webserver_pull.webserver(url,variables,2) #inicio el objeto webserver

    p = pendrive.pendrive(pendrivepath) #inicio el objeto pendrive

    dropbox_orlando =dropbox_log.dropbox_log(access_token,db_folder) #inicio el dropbox de orlando

    dropbox_pd = dropbox_log.dropbox_log(access_token_pd,db_folder) #inicio el dropbox de pulse dynamics



    pull = True #esta variable me indica cuando debo de hacer un pull de datos
    db_counter = 0
    start_time = time.time()
    db_time = 0
    start_db_time =time_upload_db + 100


    while True:
        print 'han pasado exactamente tantos ' + str(time.time()-start_time) + ' desde el ultimo muestreo'
        start_time = time.time()

        #Esta es la parte que obtiene los datos del servidos

        
        while pull:

            date = strftime("%y-%m-%d-%H:%M:%S", localtime()) #obtengo la hora del momento de la toma de muestras
            filename = date[:8]+'.txt'

            datastr = webserver.pull_datastring() #utilizo la clase webserver para que me devuelva el string con los datos

            pull=False

        #       Esta es la parte que grava los datos al pendrive    

        if p.file_exists(filename) == False: #pregunto si el archivo existe
            print "creando el archivo nuevo"
            datastr = "HH:MM:SS,"
            for i in webserver.variables_calc:
                datastr += i
                if not webserver.variables_calc[len(webserver.variables_calc) - 1] == i: #aqui inicio el header con las variables que quiero
                    datastr +=","
            datastr +='\n'
            print datastr
            p.create_file_header(filename,datastr)

        else:
            p.write_append(filename,datastr)


            ## Esta parte es la que sube las cosas a dropbox

        if (time.time()-start_db_time>= time_upload_db):
            print 'tiempo de subir a bropbox, han pasado'+ str(time.time()-start_db_time)+'segundos'

            dropbox_orlando.send_overwrite(pendrivepath,filename,db_folder) #subo el archivo a mi dropbox
            dropbox_pd.send_overwrite(pendrivepath,filename,db_folder) #subo el archivo al dropbox de pulse dynamics
            start_db_time = time.time()


        print "el tiempo es " + str(time.time()-start_time)
        if (time.time()-start_time)>= time_sample:
            pull= True
        else:
            time.sleep(time_sample-(time.time()-start_time))
            pull = True



    
        
    



