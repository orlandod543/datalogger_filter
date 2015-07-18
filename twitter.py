__author__ = 'orlando'

import sys
from twython import Twython

tweetStr = "Hola como estan soy el cogenerador de Pulse Dynamics y me estan creando en estos momentos un perfil"

# your twitter consumer and access information goes here
# note: these are garbage strings and won't work
apiKey = 'wwQbSJIMe8R9pT6xgIUcubBje'
apiSecret = 'YOPH52doq7TbltkniTOwcEP8KNYirX8qbqdONXuIgKIxEjUNce'
accessToken = '3378120419-Lu7iqOnDTOEk4g3YzipgjRCwiLVqVkbhuEapIm0'
accessTokenSecret = '0H19jwVd8r5YweA0YDKrNhBDBaPrsF8rStg4tlaYAeicw'

api = Twython(apiKey,apiSecret,accessToken,accessTokenSecret)

api.update_status(status=tweetStr)

print "Tweeted: " + tweetStr
