# -*- coding: utf-8 -*-
#Библиотеки, които използват python и Kodi в тази приставка
import re
import sys
import os
import urllib
import urllib2
import xbmc, xbmcplugin,xbmcgui,xbmcaddon
import base64
import cookielib

#Място за дефиниране на константи, които ще се използват няколкократно из отделните модули
__addon_id__= 'plugin.video.telenet'
__Addon = xbmcaddon.Addon(__addon_id__)
__settings__ = xbmcaddon.Addon(id=__addon_id__)
username = xbmcaddon.Addon().getSetting('settings_username')
password = xbmcaddon.Addon().getSetting('settings_password')
MUA = 'Mozilla/5.0 (Linux; Android 5.0.2; bg-bg; SAMSUNG GT-I9195 Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Version/1.0 Chrome/18.0.1025.308 Mobile Safari/535.19' #За симулиране на заявка от мобилно устройство
UA = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0' #За симулиране на заявка от  компютърен браузър
baseurl = base64.b64decode("aHR0cDovL3RlbGVuZXQuYmc=")

#инициализация
if not username or not password or not __settings__:
        xbmcaddon.Addon().openSettings()

req = urllib2.Request(baseurl)
req.add_header('User-Agent', UA)
req.add_header('Referer', baseurl)
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
f = opener.open(req)
data = f.read()
params = {'email': username,
          'password': password,
          'submit': 'Вход',
          'login': 'true'}
login = baseurl + '/login'
req = urllib2.Request(login, urllib.urlencode(params))
req.add_header('User-Agent', UA)
req.add_header('Referer', baseurl)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
f = opener.open(req)
data = f.read()

#Меню с директории в приставката
def CATEGORIES():
        addDir('Телевизия',baseurl+'/live',1,'DefaultFolder.png')
        #addDir('Радио',baseurl+'/radios',1,'DefaultFolder.png')


#Разлистване видеата на първата подадена страница
def INDEXPAGES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        req.add_header('Referer', baseurl)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        f = opener.open(req)
        data = f.read()
        #f.close()
        match = re.compile('a href="(.+?)" class=".+?">\n.*\n.*src="(.+?)".*\n.*\n.*\n.*\n.*<h3>(.+?)</h3>').findall(data)
        for link,thumbnail,title in match:
         addLink(title,link,2,thumbnail)


#Зареждане на видео
def PLAY(name,url,iconimage):
        req = urllib2.Request(url)
        print 'parvourl'+url
        req.add_header('User-Agent', UA)
        req.add_header('Referer', url)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        f = opener.open(req)
        data = f.read()
        #f.close()
        matchp = re.compile("playlist: '(.+?)'").findall(data)
        for firststep in matchp:
         print 'playlistat e '+firststep
         req = urllib2.Request(firststep)
         req.add_header('User-Agent', UA)
         req.add_header('Referer', url)
         opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
         f = opener.open(req)
         data = f.read()
         #f.close()
         #print data
         matchl = re.compile('<jwplayer:file>(.+?)</jwplayer:file>').findall(data)
         for secondstep in matchl:
          print 'jwplayerfailat e '+secondstep
          final_url = secondstep.replace('amp;', '')
          print 'finalniqtlink e'+final_url
          li = xbmcgui.ListItem(iconImage=iconimage, thumbnailImage=iconimage, path=final_url+'|X-Forwarded-For='+baseurl+'&User-Agent='+urllib.quote_plus(UA)+'&Referer='+url)
          li.setInfo('video', { 'title': name })
          try:
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
          except:
            xbmc.executebuiltin("Notification('Грешка','Видеото липсва на сървъра!')")






#Модул за добавяне на отделно заглавие и неговите атрибути към съдържанието на показваната в Kodi директория - НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty("IsPlayable" , "true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok



#Модул за добавяне на отделна директория и нейните атрибути към съдържанието на показваната в Kodi директория - НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


#НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param







params=get_params()
url=None
name=None
iconimage=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        name=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass


#Списък на отделните подпрограми/модули в тази приставка - трябва напълно да отговаря на кода отгоре
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
    
elif mode==1:
        print ""+url
        INDEXPAGES(url)

elif mode==2:
        print ""+url
        PLAY(name,url,iconimage)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
