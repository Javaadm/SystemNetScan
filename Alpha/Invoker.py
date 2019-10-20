from Alpha.PassPage import PassPage
from Alpha.pass_blr import BlrPass
from Alpha.Pass import Pass
from Alpha.pass_ukr import UkrPass
from PIL import Image
import requests
import json
import urllib
import os

# passport = UkrPass("images/pass.pdf", "images/", deletion_key=False, analysis_key=False, debugging=True)
# print (passport.pass_info)
# passport.create_file()


uk_text = "Звьоздкiна"
uk_text = "дірка"
test_text = "motherfucker"
token = "trnsl.1.1.20191015T182147Z.9149070483935154.5a837d98ca74bcdc2da3180d0ef575c9e1fea05d"
url_trans = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

data = {
        'key': token,
        'lang': "en-ru",
        'text': test_text}


webRequest = requests.get(url_trans, params=data)
print(webRequest.text)

data = {
        'key': token,
        'lang': "uk-ru",
        'text': uk_text}


webRequest = requests.get(url_trans, params=data)
print(webRequest.text)

# req = urllib.Request()
# req.add_header()
# response = urllib.urlopen(req, json.dumps(data))
#
# print(response)
