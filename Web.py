import time
import requests
import io
import os
import json
import codecs
from lxml import html
from pprint import pprint

def strtotime(string, format_string = "%d.%m.%Y"):
    tuple = time.strptime(string, format_string)
    return int(time.mktime(tuple))

#Local variables:=====================================================================================================
file_search   = 'res/images.html'
file_user     = 'res/user_html.html'
file_output   = 'res/result.html'
acstoken      = '5acf44005acf44005ae1d6e4835a95785a55acf5acf4400020f126825246c07ea11bf56'
vkVers        = '5.74'
#http://www.mapcoordinates.net/ru
#http://www.latlong.net/Show-Latitude-Longitude.html
coords = {'veranda'     : ('12.859227','100.896771'),
          'night_market': ('12.891365','100.874036'),
          'hawaii'      : ('19.638169','-155.520949')}
proc_place    = 'hawaii'
lat           = coords.get(proc_place)[0]
lon           = coords.get(proc_place)[1]
img_folder    = 'img__'+lat+'__'+lon+'/'
count         = '100'
radius        = '2000'
sort          = '1'
min_timestamp = str(strtotime("01.01.2001"))
max_timestamp = str(strtotime("01.06.2018"))
url_base = 'https://api.vk.com/method/photos.search?'
user_list = []
#=====================================================================================================================

def download_image(image_url,owner_id):
    print("download_image >  "+str(image_url))
    r = requests.get(url=image_url,stream=True) #settings.STATICMAP_URL.format(**data),
    path = img_folder + owner_id +'_'+ image_url.rsplit('/', 1)[-1]
    #print("IMAGE : "+path)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)


def get_user_info(user_id):
 global user_list
 if [user_id] not in user_list:
    user_list.append([user_id])
    par_usr  = 'user_ids='+ str(user_id) +'&fields=sex,bdate,city&v='+ vkVers +'&access_token='+ acstoken
    url_user = 'https://api.vk.com/method/users.get?'+par_usr
    r = requests.get(url_user)
    with open(file_user, 'wb') as output_file:
        output_file.write(r.text.encode('utf-8'))
    with io.open(file_user, encoding='utf-8', errors='ignore') as file:
        udata = json.load(file)
        #Print FULL JSON
        #print(json.dumps(udata, sort_keys=True, indent=4))
        #if udata['response'] == []:
        if 'response' in udata:
          #print('Exists search Data!')
          for rows in udata['response']:
            if 'city' in rows:
              print(str(rows['first_name']) + " " + str(rows['last_name']) + " ("+ str(rows.get('bdate', '-'))         + ") ("+ str(rows['city']['id']) +")" + str(rows['city']['title']))
        else:
          print('No search Data!')
 else:
     print('User already in LIST')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#http://www.mapcoordinates.net/ru
#http://www.latlong.net/Show-Latitude-Longitude.html

def main():
 if not os.path.exists(img_folder):
     os.makedirs(img_folder)

 par='lat='+lat+'&long='+lon+'&start_time='+min_timestamp+'&end_time='+max_timestamp+'&sort='+sort+'&count='+count+'&radius='+radius+'&v='+vkVers+'&access_token='+acstoken
 url = url_base+par
 r = requests.get(url)

 print(r.text.encode('utf-8'))

 with open(file_search, 'wb') as output_file:
   output_file.write(r.text.encode('utf-8'))

 with io.open(file_search, encoding='utf-8', errors='ignore') as file:
     data = json.load(file)
     #Print FULL JSON
     #print(json.dumps(data, sort_keys=True, indent=4))
     if data['response']==[]:
        print('No search Data!')
     else:
        #print('Exists search Data!')
        #print('album_id  - id        - owner_id  - photo_1280')
       with open(file_output, 'w') as f1:
        f1.write("<!DOCTYPE><html><html><head><meta charset=utf-8></head><body>" + os.linesep)
        for rows in data['response']['items']:
            if rows['owner_id']>0:
             get_user_info(rows['owner_id'])
             #https://vk.com/dev/photos.search
             if 'photo_1280' in rows:
                 imgph = str(rows.get('photo_1280'))
             elif 'photo_807' in rows:
                 imgph = str(rows.get('photo_807'))
             elif 'photo_604' in rows:
                 imgph = str(rows.get('photo_604'))
             else:
                 #go to next loop iteration
                 continue

             f1.write('<a href="' + imgph + '"</a>LINK FULL SIZE<br>' + os.linesep)
             download_image(imgph,str(rows['owner_id']))
             f1.write("<a href=https://vk.com/id"+str(rows['owner_id'])+">PAGE</a>")
             f1.write('<img src="'+ imgph + '" width="400" height="400"</img><br><br>' + os.linesep)

            #print(str(rows['album_id']) + " - " + str(rows['id']) + " - [" + str(rows['owner_id']))
            print('-------------------------------------------------------------------------------------')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

main()
print('There are ' + str(len(user_list)) + ' users.')
print(user_list)

