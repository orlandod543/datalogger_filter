__author__ = 'orlando'
import sys
from time import localtime, strftime

from twython import Twython

class twitter_alarm(Twython):

    def __init__(self,apiKey,apiSecret,accessToken,accessTokenSecret):
        Twython.__init__(self,apiKey,apiSecret,accessToken,accessTokenSecret)

    def encendido(self):
        date = strftime("%y/%m/%d-%H:%M:%S", localtime()) #obtengo la hora del momento de la toma de muestras
        Twtstring = date +'   '+ 'Buenos dias a todos el datalogger se encuentra encendido y funcionando'
        try:
            self.update_status(status=Twtstring)
        except:
            print 'No se pudo enviar la notificaci[on a twitter'
        print Twtstring

    def send_message(self,message):
        date = strftime("%y/%m/%d-%H:%M:%S", localtime())
        Twtstring = date + ' '+ message
        try:
            self.update_status(status=Twtstring)
        except:
            print 'No se pudo enviar la notificaci[on a twitter'
        print Twtstring




if __name__ == "__main__":
    apiKey = 'wwQbSJIMe8R9pT6xgIUcubBje'
    apiSecret = 'YOPH52doq7TbltkniTOwcEP8KNYirX8qbqdONXuIgKIxEjUNce'
    accessToken = '3378120419-Lu7iqOnDTOEk4g3YzipgjRCwiLVqVkbhuEapIm0'
    accessTokenSecret = '0H19jwVd8r5YweA0YDKrNhBDBaPrsF8rStg4tlaYAeicw'
    twitter = twitter_alarm(apiKey,apiSecret,accessToken,accessTokenSecret)
    twitter.encendido()


