#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2014 OMaluco 
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#-----------------------------------------------------------------------------------------------------------------------------------------------#
# Créditos: Este addon foi desenvolvido a partir do addon PT Video Mashup desenvolvido por enen92
#-----------------------------------------------------------------------------------------------------------------------------------------------#


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,time,os

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    PLAY    ------------------------------------------------------------------#


def PLAY_movie(url,name,iconimage,checker,fanart):
        import urlresolver
        #if 'vk.com' not in url and 'video.mail.ru' not in url:
                #dp = xbmcgui.DialogProgress()
                #dp.create(name,'A sincronizar vídeos e legendas')
                #dp.update(0)
	nome = re.compile('///(.+?)[)].+?[(].+?[)]').findall(url)
	if not nome:
                nome = re.compile('///(.*)').findall(url)
                nomefilme = nome[0]
	else: nomefilme = nome[0] + ')'
	urlvid = re.compile('(.+?)///').findall(url)
	url = urlvid[0]
	name = nomefilme + ' ' + name
	if "drive.google" in url or "docs.google" in url :
		try:
			iframe_url = url
			print iframe_url
			link3 = PLAY_abrir_url(iframe_url)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			match=re.compile('"fmt_stream_map":".+?[|](.+?)[,]').findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
				checker = ''
				url = match[0].replace('\u0026','&').replace('\u003d','=')
			else:
				checker = subtitle[0]
				url = match[0].replace('\u0026','&').replace('\u003d','=')
		except: pass
        if "streamin" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
    			#return url
		except: pass
	if "cloudzilla" in url:
		try:
			iframe_url = url
			print iframe_url
			link3 = PLAY_abrir_url(iframe_url)
			tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			match=re.compile('var vurl = "(.+?)"').findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
				checker = ''
				url = match[0]
			else:
				checker = subtitle[0]
				url = match[0]
		except: pass
	if "vodlocker" in url:
		try:
                        #if '/video/' in url: url = url.replace('/video/','/embed/')
			iframe_url = url
			print iframe_url
			link3 = PLAY_abrir_url(iframe_url)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			match=re.compile('file: "(.+?)"').findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
				checker = ''
				url = match[0]
			else:
				checker = subtitle[0]
				url = match[0]
			#addLink(name+match[0],match[0],'')
		except: pass
	if "vk.com" in url:
		try:
                        #if '/video/' in url: url = url.replace('/video/','/embed/')
			iframe_url = url
			print iframe_url
			link3 = PLAY_abrir_url(iframe_url)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
                        match=re.compile('var vars = {.+?"url240":"(.+?)"').findall(link3)
			if match: addLink('240p',match[0].replace('\/','/'),'')
			match=re.compile('var vars = {.+?"url360":"(.+?)"').findall(link3)
			if match: addLink('360p',match[0].replace('\/','/'),'')
			match=re.compile('var vars = {.+?"url480":"(.+?)"').findall(link3)
			if match: addLink('480p',match[0].replace('\/','/'),'')
			match=re.compile('var vars = {.+?"url720":"(.+?)"').findall(link3)
			if match: addLink('720p',match[0].replace('\/','/'),'')
			match=re.compile('var vars = {.+?"url1080":"(.+?)"').findall(link3)
			if match: addLink('1080p',match[0].replace('\/','/'),'')
		except: pass
        if "streamcloud" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	if "video.mail.ru" in url:
		try:
			iframe_url = url
			print iframe_url
			link3 = PLAY_abrir_url(iframe_url)
			#tit=re.compile('"videoTitle":"(.+?)"').findall(link3)
			tit=re.compile('<title>(.+?)</title>').findall(link3)
			#v_key = re.compile('video_key=(.+?)&expire_at=(.+?)"').findall(link3)
			if 'sd' in link3 and 'md' in link3:
                                match=re.compile('videoPresets = {"sd":"(.+?)","md":"(.+?)"}').findall(link3)
                                #match=re.compile('"videos":{"sd":"(.+?)&expire_at=.+?","hd":"(.+?)&expire_at=.+?"}').findall(link3)
                                #matchHD=re.compile('"videos":{"sd":"(.+?)&expire_at=.+?","hd":"(.+?)&expire_at=.+?"}').findall(link3)
                                #vl=match[0][0]+'&video_key='+v_key[0][0]+'&expire_at='+v_key[0][1]
                                if match:
                                        addLink('SD',match[0][0],'')
                                        addLink('HD',match[0][1],'')
			if 'sd' in link3 and 'md' not in link3:
                                match=re.compile('videoPresets = {"sd":"(.+?)"').findall(link3)
                                #match=re.compile('"videos":{"sd":"(.+?)"}').findall(link3)
                                if match:
                                        #url=match[0]
                                        addLink('SD',match[0],'')
                        if 'hd' in link3 and 'md' not in link3:
                                match=re.compile('"md":"(.+?)"}').findall(link3)
                                #match=re.compile('"videos":{"hd":"(.+?)"}').findall(link3)
                                if match:
                                        addLink('HD',match[0],'')
			#subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			#if subtitle == []:
				#checker = ''
				#url=match[0]
			#else:
				#checker = subtitle[0]
				#url = match[0]
		except: pass
	if "flashx" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
        if "youtu" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	if "youwatch" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	if "hostingbulk" in url:
		try:
			iframe_url = url
			print iframe_url
			link3 = PLAY_abrir_url(iframe_url)
			#tit=re.compile('title: "(.+?)"').findall(link3)
			match=re.compile('http[|]player[|]type[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|]com[|]hostingbulk[|]provider[|](.+?)[|]video[|](.+?)[|][|]file[|]').findall(link3)
			#subtitle=re.compile("addSubtitles('(.+?)', '', false)").findall(link3)
			#subtitle = []
			url = 'http://'+match[0][3]+'.'+match[0][2]+'.'+match[0][1]+'.'+match[0][0]+'/d/'+match[0][5]+'/video.'+match[0][4]+'?start=0'
			#if subtitle == []:
				#checker = ''
				#url = match[0]
			#else:
				#checker = subtitle[0]
				#url = match[0]
		except: pass
        if "vidto.me" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	if "dropvideo" in url:
		try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
			iframe_url = url
			print iframe_url
			link3 = PLAY_abrir_url(iframe_url)
			tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			match=re.compile('var vurl2 = "(.+?)"').findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
				checker = ''
				url = match[0]
			else:
				checker = subtitle[0]
				url = match[0]
			#addLink(name+match[0],match[0],'')
		except: pass
	if "putlocker" in url:
                try:
                        url = url.replace('putlocker.com/embed/','firedrive.com/file/')
                        #sources = []
                        #hosted_media = urlresolver.HostedMediaFile(url)
                        #sources.append(hosted_media)
                        #source = urlresolver.choose_source(sources)
                        #if source: 
                                #url = source.resolve()
                        #else: url = ''
                        #addLink(url,url,'')
    		except:pass
    	if "nowvideo" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	if "primeshare" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	if "allmyvideos" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	if "vkontakte" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	if "videoslasher" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	if "sockshare" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	if "firedrive" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
                        #addLink(url,url,'')
    		except:pass
    	if "videowood" in url:
                try:
                        iframe_url = url
			print iframe_url
			link3 = PLAY_abrir_url(iframe_url)
			tit=re.compile('title: "(.+?)"').findall(link3)
			#match=re.compile('file: "(.+?)"').findall(link3)
			subtitle=re.compile("addSubtitles[(]'(.+?)'").findall(link3)
			iframe_url = url.replace('/embed/','/video-link/')
			print iframe_url
			link3 = PLAY_abrir_url(iframe_url)
			#print iframe_url
			#link3 = PLAY_abrir_url(iframe_url)
			match=re.compile('"url":"(.+?)"}').findall(link3)
			#subtitle = []
			if subtitle == []:
				checker = ''
				url = match[0].replace('\/','/')
			else:
				checker = subtitle[0]
				url = match[0].replace('\/','/')
			#addLink(name+match[0],match[0],'')
    		except:pass
    	if "movshare" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	if "video.tt" in url or "videott" in url:
                try:
                        iframe_url = url
			print iframe_url
			link3 = PLAY_abrir_url(iframe_url)
			id_video = re.compile('http://video.tt/player_control/settings.php?v=(.+?)&fv=v1.2.74').findall(url)
			if not id_video: id_video = re.compile('"vcode":"(.+?)"').findall(link3)
			v_key=re.compile('"time":"(.+?)"}').findall(link3)
			tit=re.compile('Title=(.+?)&SourceURL=').findall(link3)
			tt=re.compile('"st":(.+?),"tst"').findall(link3)
			vlink='http://gs.video.tt/s?v='+id_video[0]+'&r=1&t='+tt[0]+'&u=&c='+v_key[0]+'&start=0'
			subtitle=re.compile("addSubtitles[(]'(.+?)'").findall(link3)
			#subtitle = []
			if subtitle == []:
				checker = ''
				url = vlink
			else:
				checker = subtitle[0]
				url = vlink
			#addLink('Ver Filme',url,'')
                        #addLink(id_video[0],vlink,'')
                        #addLink(tt[0],vlink,'')
                        #addLink(v_key[0],vlink,'')
                        #addLink(vlink,vlink,'')
    		except:pass
    	if "videomega" in url:
		try:
			if "iframe" not in url:
				id_videomega = re.compile('ref=(.*)').findall(url)[0]
				iframe_url = 'http://videomega.tv/iframe.php?ref=' + id_videomega
			else: iframe_url = url
			print iframe_url
			link3 = PLAY_abrir_url(iframe_url)
			match=re.compile('document.write\(unescape\("(.+?)"\)').findall(link3)
			print match
			tit=re.compile('<div id="title">&nbsp;&nbsp;&nbsp;(.+?)</div>').findall(link3)
			video_url_escape = urllib.unquote(match[0])
			match=re.compile('file: "(.+?)"').findall(video_url_escape)
			subtitle=re.compile('"file": "(.+?)"').findall(video_url_escape)
			if subtitle==[]:
                                subtitle=re.compile('[[][{]file: "(.+?)"').findall(video_url_escape)
                                
			if subtitle == []:
				checker = ''
				url = match[0]
			else:
				checker = subtitle[0].replace('http://videomega.tv/servesrt.php?s=','')
				url = match[0]
			#addLink(checker,match[0],'')
		except: pass
        #if 'vk.com' not in url and 'video.mail.ru' not in url and 'video.tt' not in url:
        if 'vk.com' not in url and 'video.mail.ru' not in url:
                try:
                        ####addLink(name+url,match[0],'')
                        playlist = xbmc.PlayList(1)
                        playlist.clear()             
                        playlist.add(url,xbmcgui.ListItem(name, thumbnailImage=str(iconimage)))
                        addLink(name,url,iconimage)
                        #dp.update(33)
                        #if dp.iscanceled(): return
                        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
                        #dp.update(66)
                        xbmcPlayer.play(playlist)
                        #dp.update(100)
                        #dp.close()
                        #xbmc.Player().play(url)
                        if checker == '' or checker == None: pass
                        else: xbmcPlayer.setSubtitles(checker)
                except: pass

#----------------------------------------------------------------------------------------------------------------------------------------------#
	
def PLAY_abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

#----------------------------------------------------------------------------------------------------------------------------------------------#
              
def PLAY_get_params():
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

#----------------------------------------------------------------------------------------------------------------------------------------------#

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'flag.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addLink1(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'flag.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,checker,fanart):
        text = 'nnnnnn'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&checker="+urllib.quote_plus(checker)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'flag.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": text } )
        cm = []
	cm.append(('Sinopse', 'XBMC.Action(Info)'))
	liz.addContextMenuItems(cm, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir1(name,url,mode,iconimage,folder,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'flag.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
        return ok



#----------------------------------------------------------------------------------------------------------------------------------------------#
	
params=PLAY_get_params()
url=None
name=None
mode=None
checker=None
iconimage=None
fanart=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:        
        checker=urllib.unquote_plus(params["checker"])
except:
        pass
try:        
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Checker: "+str(checker)
print "Iconimage: "+str(iconimage)


