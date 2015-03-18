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


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,time,os,urlparse,HTMLParser,json
h = HTMLParser.HTMLParser()
from array import array
import TugaFilmesTV,TopPt,TugaFilmesCom,MovieTuga,FilmesAnima,Pesquisar,Mashup,Funcoes,CinematugaEu,Cinematuga,CinemaEmCasa,PesquisaExterna
from Funcoes import thetvdb_api, themoviedb_api, themoviedb_api_tv, theomapi_api, themoviedb_api_IMDB, themoviedb_api_IMDB_episodios, themoviedb_api_TMDB
from Funcoes import thetvdb_api_tvdbid, thetvdb_api_episodes, themoviedb_api_search_imdbcode, themoviedb_api_pagina, themoviedb_api_IMDB1, theomapi_api_nome
from Funcoes import addDir, addDir1, addDir2, addLink, addLink1, addDir_teste, addDir_trailer, addDir_episode
from Funcoes import get_params,abrir_url

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

progress = xbmcgui.DialogProgress()

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    PLAY    ------------------------------------------------------------------#

def PLAY_movie_url(url,name,iconimage,checker,fanart):#,nomeAddon):
        url = url.replace('////','///')
        try:
                import urlresolver
        except: pass
        #if 'vk.com' not in url and 'video.mail.ru' not in url:
                #dp = xbmcgui.DialogProgress()
                #dp.create(name,'A sincronizar vídeos e legendas')
                #dp.update(0)
        if '///' in url:
                if '////' in url: nome = re.compile('////(.+?)[)].+?[(].+?[)]').findall(url)
                else: nome = re.compile('///(.+?)[)].+?[(].+?[)]').findall(url)
                if not nome:
                        nome = re.compile('///(.*)').findall(url)
                        if nome: nomefilme = nome[0]
                else: nomefilme = nome[0] + ')'
                urlvid = re.compile('(.+?)///').findall(url)
                if urlvid: url = urlvid[0]
                #if nomefilme.replace(' ','') != name.replace(' ',''):
                #name = nomefilme + ' ' + name
        #addLink(url,'','','')
        iframe_url = url
	if "clipstube" in url :
		try:
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			match=re.compile("var hq_video_file = '(.+?)'").findall(link3)
			if not match: match=re.compile("var normal_video_file = '(.+?)'").findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
				checker = ''
				url = match[0]
			else:
				checker = subtitle[0]
				url = match[0]
		except: pass
	if "video.pw" in url :
		try:

			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			imagem=re.compile('var vscreenshot = "(.+?)"').findall(link3)
			if imagem: iconimage = imagem[0]
			match=re.compile('var vurl2 = "(.+?)"').findall(link3)
			if match: url = match[0]
			else: url = ''
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []: checker = ''
			else: checker = subtitle[0]

		except: pass
	if "drive.google" in url or "docs.google" in url :
		try:
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
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
		except: pass
	if "thevideo.me" in url:
		try:
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			if link3:
                                mp4 = re.compile('[|]logo[|]100[|](.+?)[|]label[|]').findall(link3)
                                if mp4: mp4 = mp4[0]
                                else: mp4='111'
			else: mp4 = '--'
			imagem = re.compile('<span id=.+?><img src="(.+?)"').findall(link3)
			if imagem:
                                iconimage = imagem[0]
                                ip = re.compile('(.+?)/i/').findall(iconimage)
                                if ip: ip = ip[0]
			todassources = re.compile('[|]sharing(.+?)sources[|]').findall(link3)
			sourc = re.compile('.+?[|](.+?)0p[|]').findall(todassources[0])
			addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,iconimage,False,fanart)
			i = 1
			a = 0
			if len(sourc) == 5:
                                sources = re.compile('[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|]').findall(todassources[0])
                                for x in range(5):
                                        url = ip + '/' + sources[0][a] + '/v.' + mp4
                                        a = a + 2
                                        addLink(sources[0][i]+'0p | '+name,url,iconimage,fanart)
                                        i = a + 1
        
                        if len(sourc) == 4:
                                sources = re.compile('[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|]').findall(todassources[0])
                                for x in range(4):
                                        url = ip + '/' + sources[0][a] + '/v.' + mp4
                                        a = a + 2
                                        addLink(sources[0][i]+'0p | '+name,url,iconimage,fanart)
                                        i = a + 1
        
			if len(sourc) == 3:
                                sources = re.compile('[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|]').findall(todassources[0])
                                for x in range(3):
                                        url = ip + '/' + sources[0][a] + '/v.' + mp4
                                        a = a + 2
                                        addLink(sources[0][i]+'0p | '+name,url,iconimage,fanart)
                                        i = a + 1
 
			if len(sourc) == 2:
                                sources = re.compile('[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|]').findall(todassources[0])
                                for x in range(2):
                                        url = ip + '/' + sources[0][a] + '/v.' + mp4
                                        a = a + 2
                                        addLink(sources[0][i]+'0p | '+name,url,iconimage,fanart)
                                        i = a + 1
                                           
                        if len(sourc) == 1:
                                sources = re.compile('[|]mp4[|](.+?)[|](.+?)0p[|]').findall(todassources[0])
                                url = ip + '/' + sources[0][0] + '/v.' + mp4
                                addLink(sources[0][1]+'0p | '+name,url,iconimage,fanart)

		except: pass
	if "vidzi.tv" in url:       
		try:
                        if 'embed-' in iframe_url:
                                iframe_url = url.replace('vidzi.tv/embed-','vidzi.tv/')
                                tiraurl = re.compile('(.+?)-').findall(iframe_url)
                                if tiraurl: iframe_url = tiraurl[0]+'.html'
                        print iframe_url
                        link3 = abrir_url(iframe_url)
                        match=re.compile('file: "(.+?)"').findall(link3)
                        subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
                        imagem = re.compile('image: "(.+?)"').findall(link3)
                        if imagem: iconimage = imagem[0]
                        addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,iconimage,False,fanart)
                        for link in match:
                                if '.m3u8' in link:
                                        url = link
                                        addLink('m3u8 | '+name,url,iconimage,fanart)
                                if '.mp4' in link:
                                        url = link
                                        addLink('mp4 | '+name,url,iconimage,fanart)
                                if '.srt' in link: checker = link
                except: pass                
	if "vidzen" in url:
		try:
                        #iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
                                checker = ''
			else:
				checker = subtitle[0]
			match=re.compile('streamer: "(.+?)"').findall(link3)
			if not match:
                                match=re.compile('file: "(.+?)"').findall(link3)
                                if match: url = match[0]
                        else: url = match[0]
			if not match:
                                match=re.compile('var[|]type[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|][|](.+?)[|].+?provider[|](.+?)[|](.+?)[|]file').findall(link3)
                                if match: url = 'http://'+match[0][4]+'.'+match[0][3]+'.'+match[0][2]+'.'+match[0][1]+':'+match[0][0]+'/'+match[0][6]+'/v.'+match[0][5]#+'?start=0'
			imagem=re.compile('[[]IMG[]](.+?)[[]/IMG[]]').findall(link3)
			if imagem: iconimage = imagem[0]
			#addLink(url,url,iconimage,fanart)
		except: pass
	if "playfreehd" in url:
		try:
			if 'embed' in iframe_url:
                                print iframe_url
                                link3 = abrir_url(iframe_url)
                                imagem = re.compile("var preview_img = '(.+?)';").findall(link3)
                                if imagem: iconimage = imagem[0]
                                match=re.compile("var hq_video_file = '(.+?)';").findall(link3)
                                if match:
                                        url = match[0]+'?start=0'
                                        if '.flv' in url: flv = '.flv | '
                                        else: flv = ''
                                        addLink('HQ | '+flv+name,url,iconimage,fanart)
                                match=re.compile("var normal_video_file = '(.+?)';").findall(link3)
                                if match:
                                        url = match[0]+'?start=0'
                                        if '.flv' in url: flv = '.flv | '
                                        else: flv = ''
                                        addLink('SD | '+flv+name,url,iconimage,fanart)
                        if 'embed' not in iframe_url:
                                print iframe_url
                                link3 = abrir_url(iframe_url)
                                link = re.compile('<param name="FlashVars" value="plugins=plugins/proxy.swf&proxy.link=http://filehoot.com/(.+?).html;captions.file').findall(link3)
                                if link:
                                        link = 'http://filehoot.com/embed-'+link[0]+'-640x360.html'
                                        link3 = abrir_url(link)
                                imagem = re.compile('image: "(.+?)"').findall(link3)
                                if imagem: iconimage = imagem[0]
                                match=re.compile('file: "(.+?)"').findall(link3)
                                if match:
                                        
                                        url = match[0]
                                        iframe_url = url
		except: pass
	if "divxstage" in url:
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
	if "vidbull" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
    			#addLink(match[0],match[0],'')
    			#return url
		except: pass
	if "vodlocker" in url:
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
	if "played.to" in url:
                #addLink('sim1','','')
		try:
                        #addLink('sim','','')
                        #iframe_url = url
                        print iframe_url
                        link3 = abrir_url(iframe_url)
                        imagem = re.compile('image: "(.+?)"').findall(link3)
			if imagem: iconimage = imagem[0]
                        tit=re.compile('var vtitle = "(.+?)"').findall(link3)
                        match=re.compile('file: "(.+?)"').findall(link3)
                        subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
                        if subtitle == []:
                                checker = ''
                                if match: url = match[0]
                        else:
                                if checker: checker = subtitle[0]
                                if match: url = match[0]
                except: pass
	if "cloudzilla" in url:
		try:
			#iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			imagem = re.compile('var vthumbnail = "(.+?)"').findall(link3)
			if imagem: iconimage = imagem[0]
			tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			match=re.compile('var vurl = "(.+?)"').findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
				checker = ''
				if match: url = match[0]
			else:
				if checker: checker = subtitle[0]
				if match: url = match[0]
			#addLink(match[0],match[0],'')
			#return
		except: pass
	if "vodlocker" in url:
		try:
                        #if '/video/' in url: url = url.replace('/video/','/embed/')
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
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
			link3 = abrir_url(iframe_url)
			addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,artfolder,False,fanart)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
                        match=re.compile('var vars = {.+?"url240":"(.+?)"').findall(link3)
			if match: addLink('240p | '+name,match[0].replace('\/','/'),iconimage,fanart)
			match=re.compile('var vars = {.+?"url360":"(.+?)"').findall(link3)
			if match: addLink('360p | '+name,match[0].replace('\/','/'),iconimage,fanart)
			match=re.compile('var vars = {.+?"url480":"(.+?)"').findall(link3)
			if match: addLink('480p | '+name,match[0].replace('\/','/'),iconimage,fanart)
			match=re.compile('var vars = {.+?"url720":"(.+?)"').findall(link3)
			if match: addLink('720p | '+name,match[0].replace('\/','/'),iconimage,fanart)
			match=re.compile('var vars = {.+?"url1080":"(.+?)"').findall(link3)
			if match: addLink('1080p | '+name,match[0].replace('\/','/'),iconimage,fanart)
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
	if "filehoot" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	if "video.mail.ru" in url or 'videoapi.my.mail' in url:
                #addLink(url,'','')
		try:
			iframe_url = url###http://api.video.mail.ru/videos/mail/megafilmeshdtv/_myvideo/874.json
			print iframe_url
			#addLink(iframe_url,'','')
			addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,artfolder,False,fanart)
			iframe_url = iframe_url.replace('/embed','').replace('.html','.json')
                        try:
                                link3 = abrir_url(iframe_url)
                        except: link3 = ''
                        if link3 != '':
                                imagem = re.compile('"poster":"(.+?)"').findall(link3)
                                if imagem: iconimage = imagem[0]
                                match = re.compile('"key":"(.+?)","url":"(.+?)"').findall(link3)
                                for res,link in match:
                                        addLink(res+' | '+name,link,iconimage,fanart)
                        else:
                                try:
                                        link3 = abrir_url(iframe_url)
                                except: link3 = ''
                                tit=re.compile('<title>(.+?)</title>').findall(link3)
                                if link3 != '':
                                        if 'sd' in link3 and 'md' in link3:
                                                match=re.compile('videoPresets = {"sd":"(.+?)","md":"(.+?)"}').findall(link3)
                                                if not match:
                                                        match=re.compile('"videos":{"sd":"(.+?)&expire_at=.+?","hd":"(.+?)&expire_at=.+?"}').findall(link3)
                                                        if not match: match=re.compile('"url":"(.+?)"').findall(link3)
                                                if match:
                                                        addLink('SD | '+name,match[0][0],iconimage,fanart)
                                                        addLink('HD | '+name,match[0][1],iconimage,fanart)
                                        elif 'sd' in link3 and 'md' not in link3:
                                                match=re.compile('videoPresets = {"sd":"(.+?)"').findall(link3)
                                                if match:
                                                        addLink('SD | '+name,match[0],iconimage,fanart)
                                        elif 'hd' in link3 and 'md' not in link3:
                                                match=re.compile('"md":"(.+?)"}').findall(link3)
                                                if match:
                                                        addLink('HD | '+name,match[0],iconimage,fanart)                            
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
			link3 = abrir_url(iframe_url)
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
##                        iframe_url = url
##			print iframe_url
##			addLink(url,'','','')
##                        link3=abrir_url(iframe_url)
##                        jsU = JsUnpackerV2()
##                        link3 = jsU.unpackAll(link3)
##                        url=re.compile('file:"(.+?)"').findall(link3)[-1]
##                        addLink(url,'','','')
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
    			#addLink(url,'','','')
    			#checker = url.replace('.avi','.srt')
		except: pass
	if "dropvideo" in url:
		try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			imagem = re.compile('var vscreenshot = "(.+?)"').findall(link3)
			if imagem: iconimage = imagem[0]
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
			link3 = abrir_url(iframe_url)
			tit=re.compile('title: "(.+?)"').findall(link3)
			match=re.compile('file: "(.+?)"').findall(link3)
			subtitle=re.compile("addSubtitles[(]'(.+?)'").findall(link3)
			if match:
                                #addLink(tit[0]+match[0],match[0],'')
                                if subtitle == []:
                                        checker = ''
                                        url = match[0].replace('\/','/')
                                else:
                                        checker = subtitle[0]
                                        url = match[0].replace('\/','/')
                        else:
                                iframe_url = url.replace('/embed/','/video-link/')
                                link3 = abrir_url(iframe_url)
                                if link3 != []:
                                        match=re.compile('"url":"(.+?)"}').findall(link3)
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
			link3 = abrir_url(iframe_url)
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
			#addLink(url,'','')
    		except:pass
    	if "videomega" in url:
		try:
                        urli,checker = videomega_resolver(iframe_url)
                        uli=re.compile('(.+?)[|]Host=').findall(urli)
                        if uli: url=uli[0]
                        else: url=urli
##                        if "iframe" not in url:
##                                id_videomega = re.compile('ref=(.*)').findall(url)[0]
##                                iframe_url = 'http://videomega.tv/iframe.php?ref=' + id_videomega
##                        else: iframe_url = url
##                        print iframe_url
##                        link3 = abrir_url(iframe_url)
##                        match=re.compile('document.write\(unescape\("(.+?)"\)').findall(link3)
##                        print match
##                        tit=re.compile('<div id="title">&nbsp;&nbsp;&nbsp;(.+?)</div>').findall(link3)
##                        video_url_escape = urllib.unquote(match[0])
##                        match=re.compile('file: "(.+?)"').findall(video_url_escape)
##                        subtitle=re.compile('"file": "(.+?)"').findall(video_url_escape)
##                        if subtitle==[]:
##                                subtitle=re.compile('[[][{]file: "(.+?)"').findall(video_url_escape)      
##                        if subtitle == []:
##                                checker = ''
##                                url = match[0]
##                        else:
##                                checker = subtitle[0].replace('http://videomega.tv/servesrt.php?s=','')
##                                url = match[0]
##                        #addLink(checker,match[0],'')
		except: pass
        #addLink(url,url,'','')
        #if 'vk.com' not in iframe_url and 'video.mail.ru' not in iframe_url and 'videoapi.my.mail' not in iframe_url and 'vidzi.tv' not in iframe_url and 'playfreehd' not in iframe_url  and 'thevideo.me' not in iframe_url:# and 'iiiiiiiiii' in url:
        try:
                addLink(name,url,iconimage,fanart)
        except: pass
        return

def PLAY_movie(url,name,iconimage,checker,fanart):#,nomeAddon):
        nomeAddon = ''
        percent = 0
        message = ''
        progress.create(name, 'A preparar vídeo...')
        progress.update( percent, "", message, "" )
        #addLink(url,'','')
        url = url.replace('////','///')
        try:
                import urlresolver
        except: pass
        #if 'vk.com' not in url and 'video.mail.ru' not in url:
                #dp = xbmcgui.DialogProgress()
                #dp.create(name,'A sincronizar vídeos e legendas')
                #dp.update(0)
        if '///' in url:
                if '////' in url: nome = re.compile('////(.+?)[)].+?[(].+?[)]').findall(url)
                else: nome = re.compile('///(.+?)[)].+?[(].+?[)]').findall(url)
                if not nome:
                        nome = re.compile('///(.*)').findall(url)
                        if nome: nomefilme = nome[0]
                else: nomefilme = nome[0] + ')'
                urlvid = re.compile('(.+?)///').findall(url)
                if urlvid: url = urlvid[0]
                #if nomefilme.replace(' ','') != name.replace(' ',''):
                name = nomefilme + ' ' + name
        #name = namet
        iframe_url = url
	if "clipstube" in url :
		try:
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			match=re.compile("var hq_video_file = '(.+?)'").findall(link3)
			if not match: match=re.compile("var normal_video_file = '(.+?)'").findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
				checker = ''
				url = match[0]
			else:
				checker = subtitle[0]
				url = match[0]
		except: pass
	elif "video.pw" in url :
		try:

			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			imagem=re.compile('var vscreenshot = "(.+?)"').findall(link3)
			if imagem: iconimage = imagem[0]
			match=re.compile('var vurl2 = "(.+?)"').findall(link3)
			if match: url = match[0]
			else: url = ''
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []: checker = ''
			else: checker = subtitle[0]

		except: pass
	elif "drive.google" in url or "docs.google" in url :
		try:
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
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
        elif "streamin" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	elif "thevideo.me" in url:
		try:
                        _nomeservidor_ = []
                        _linkservidor_ = []
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			if link3:
                                mp4 = re.compile('[|]logo[|]100[|](.+?)[|]label[|]').findall(link3)
                                if mp4: mp4 = mp4[0]
                                else: mp4='111'
			else: mp4 = '--'
			imagem = re.compile('<span id=.+?><img src="(.+?)"').findall(link3)
			if imagem:
                                iconimage = imagem[0]
                                ip = re.compile('(.+?)/i/').findall(iconimage)
                                if ip: ip = ip[0]
			todassources = re.compile('[|]sharing(.+?)sources[|]').findall(link3)
			sourc = re.compile('.+?[|](.+?)0p[|]').findall(todassources[0])
			addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,iconimage,False,fanart)
			i = 1
			a = 0
			if len(sourc) == 5:
                                sources = re.compile('[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|]').findall(todassources[0])
                                for x in range(5):
                                        url = ip + '/' + sources[0][a] + '/v.' + mp4
                                        _linkservidor_.append(url)
                                        a = a + 2
                                        _nomeservidor_.append(sources[0][i]+'0p | '+name)
                                        addLink(sources[0][i]+'0p | '+name,url,iconimage,fanart)
                                        i = a + 1
        
                        if len(sourc) == 4:
                                sources = re.compile('[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|]').findall(todassources[0])
                                for x in range(4):
                                        url = ip + '/' + sources[0][a] + '/v.' + mp4
                                        _linkservidor_.append(url)
                                        a = a + 2
                                        _nomeservidor_.append(sources[0][i]+'0p | '+name)
                                        addLink(sources[0][i]+'0p | '+name,url,iconimage,fanart)
                                        i = a + 1
        
			if len(sourc) == 3:
                                sources = re.compile('[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|]').findall(todassources[0])
                                for x in range(3):
                                        url = ip + '/' + sources[0][a] + '/v.' + mp4
                                        _linkservidor_.append(url)
                                        a = a + 2
                                        _nomeservidor_.append(sources[0][i]+'0p | '+name)
                                        addLink(sources[0][i]+'0p | '+name,url,iconimage,fanart)
                                        i = a + 1
 
			if len(sourc) == 2:
                                sources = re.compile('[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|]').findall(todassources[0])
                                for x in range(2):
                                        url = ip + '/' + sources[0][a] + '/v.' + mp4
                                        _linkservidor_.append(url)
                                        a = a + 2
                                        _nomeservidor_.append(sources[0][i]+'0p | '+name)
                                        addLink(sources[0][i]+'0p | '+name,url,iconimage,fanart)
                                        i = a + 1
                                           
                        if len(sourc) == 1:
                                sources = re.compile('[|]mp4[|](.+?)[|](.+?)0p[|]').findall(todassources[0])
                                url = ip + '/' + sources[0][0] + '/v.' + mp4
                                addLink(sources[0][1]+'0p | '+name,url,iconimage,fanart)
                                #addLink(sources[0][0],'','','')
                                nm = sources[0][1]+'0p | '+name
                                _nomeservidor_.append(nm)
                                _linkservidor_.append(url)
          
		except: pass
##		progress.close()
##                index = xbmcgui.Dialog().select('Escolha o Stream', _nomeservidor_)
##                if index > -1:
##                        playlist = xbmc.PlayList(1)
##                        playlist.clear()             
##                        playlist.add(_linkservidor_[index],xbmcgui.ListItem(name, thumbnailImage=str(iconimage)))
##                        MyPlayer(nome_addon=nome_addon,checker=checker).PlayStream(playlist)
##                        #Play.PLAY_movie(_linkservidor_[index],_nomeservidor_[index],iconimage,'',fanart)
                        
	elif "vidzi.tv" in url:       
		try:
                        if 'embed-' in iframe_url:
                                iframe_url = url.replace('vidzi.tv/embed-','vidzi.tv/')
                                tiraurl = re.compile('(.+?)-').findall(iframe_url)
                                if tiraurl: iframe_url = tiraurl[0]+'.html'
                        print iframe_url
                        link3 = abrir_url(iframe_url)
                        match=re.compile('file: "(.+?)"').findall(link3)
                        subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
                        imagem = re.compile('image: "(.+?)"').findall(link3)
                        if imagem: iconimage = imagem[0]
                        addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,iconimage,False,fanart)
                        for link in match:
                                if '.m3u8' in link:
                                        url = link
                                        addLink('m3u8 | '+name,url,iconimage,fanart)
                                if '.mp4' in link:
                                        url = link
                                        addLink('mp4 | '+name,url,iconimage,fanart)
                                if '.srt' in link: checker = link
                except: pass                
	elif "vidzen" in url:
		try:
                        #iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
                                checker = ''
			else:
				checker = subtitle[0]
			match=re.compile('streamer: "(.+?)"').findall(link3)
			if not match:
                                match=re.compile('file: "(.+?)"').findall(link3)
                                if match: url = match[0]
                        else: url = match[0]
			if not match:
                                match=re.compile('var[|]type[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|][|](.+?)[|].+?provider[|](.+?)[|](.+?)[|]file').findall(link3)
                                if match: url = 'http://'+match[0][4]+'.'+match[0][3]+'.'+match[0][2]+'.'+match[0][1]+':'+match[0][0]+'/'+match[0][6]+'/v.'+match[0][5]#+'?start=0'
			imagem=re.compile('[[]IMG[]](.+?)[[]/IMG[]]').findall(link3)
			if imagem: iconimage = imagem[0]
			#addLink(url,url,iconimage,fanart)
		except: pass
	elif "playfreehd" in url:
		try:
			if 'embed' in iframe_url:
                                print iframe_url
                                link3 = abrir_url(iframe_url)
                                imagem = re.compile("var preview_img = '(.+?)';").findall(link3)
                                if imagem: iconimage = imagem[0]
                                match=re.compile("var hq_video_file = '(.+?)';").findall(link3)
                                if match:
                                        url = match[0]+'?start=0'
                                        if '.flv' in url: flv = '.flv | '
                                        else: flv = ''
                                        addLink('HQ | '+flv+name,url,iconimage,fanart)
                                match=re.compile("var normal_video_file = '(.+?)';").findall(link3)
                                if match:
                                        url = match[0]+'?start=0'
                                        if '.flv' in url: flv = '.flv | '
                                        else: flv = ''
                                        addLink('SD | '+flv+name,url,iconimage,fanart)
                        if 'embed' not in iframe_url:
                                print iframe_url
                                link3 = abrir_url(iframe_url)
                                link = re.compile('<param name="FlashVars" value="plugins=plugins/proxy.swf&proxy.link=http://filehoot.com/(.+?).html;captions.file').findall(link3)
                                if link:
                                        link = 'http://filehoot.com/embed-'+link[0]+'-640x360.html'
                                        link3 = abrir_url(link)
                                imagem = re.compile('image: "(.+?)"').findall(link3)
                                if imagem: iconimage = imagem[0]
                                match=re.compile('file: "(.+?)"').findall(link3)
                                if match:
                                        
                                        url = match[0]
                                        iframe_url = url
		except: pass
	elif "divxstage" in url:
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
	elif "vidbull" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
    			#addLink(match[0],match[0],'')
    			#return url
		except: pass
	elif "vodlocker" in url:
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
	elif "played.to" in url:
                #addLink('sim1','','')
		try:
                        #addLink('sim','','')
                        #iframe_url = url
                        print iframe_url
                        link3 = abrir_url(iframe_url)
                        imagem = re.compile('image: "(.+?)"').findall(link3)
			if imagem: iconimage = imagem[0]
                        tit=re.compile('var vtitle = "(.+?)"').findall(link3)
                        match=re.compile('file: "(.+?)"').findall(link3)
                        subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
                        if subtitle == []:
                                checker = ''
                                if match: url = match[0]
                        else:
                                if checker: checker = subtitle[0]
                                if match: url = match[0]
                except: pass
	elif "cloudzilla" in url:
		try:
			#iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			imagem = re.compile('var vthumbnail = "(.+?)"').findall(link3)
			if imagem: iconimage = imagem[0]
			tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			match=re.compile('var vurl = "(.+?)"').findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
				checker = ''
				if match: url = match[0]
			else:
				if checker: checker = subtitle[0]
				if match: url = match[0]
			#addLink(match[0],match[0],'')
			#return
		except: pass
	elif "vodlocker" in url:
		try:
                        #if '/video/' in url: url = url.replace('/video/','/embed/')
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
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
	elif "vk.com" in url:
		try:
                        #if '/video/' in url: url = url.replace('/video/','/embed/')
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,artfolder,False,fanart)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
                        match=re.compile('var vars = {.+?"url240":"(.+?)"').findall(link3)
			if match: addLink('240p | '+name,match[0].replace('\/','/'),iconimage,fanart)
			match=re.compile('var vars = {.+?"url360":"(.+?)"').findall(link3)
			if match: addLink('360p | '+name,match[0].replace('\/','/'),iconimage,fanart)
			match=re.compile('var vars = {.+?"url480":"(.+?)"').findall(link3)
			if match: addLink('480p | '+name,match[0].replace('\/','/'),iconimage,fanart)
			match=re.compile('var vars = {.+?"url720":"(.+?)"').findall(link3)
			if match: addLink('720p | '+name,match[0].replace('\/','/'),iconimage,fanart)
			match=re.compile('var vars = {.+?"url1080":"(.+?)"').findall(link3)
			if match: addLink('1080p | '+name,match[0].replace('\/','/'),iconimage,fanart)
		except: pass
        elif "streamcloud" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	elif "filehoot" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	elif "video.mail.ru" in url or 'videoapi.my.mail' in url:
                #addLink(url,'','')
		try:
			iframe_url = url###http://api.video.mail.ru/videos/mail/megafilmeshdtv/_myvideo/874.json
			print iframe_url
			#addLink(iframe_url,'','')
			addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,artfolder,False,fanart)
			iframe_url = iframe_url.replace('/embed','').replace('.html','.json')
                        try:
                                link3 = abrir_url(iframe_url)
                        except: link3 = ''
                        if link3 != '':
                                imagem = re.compile('"poster":"(.+?)"').findall(link3)
                                if imagem: iconimage = imagem[0]
                                match = re.compile('"key":"(.+?)","url":"(.+?)"').findall(link3)
                                for res,link in match:
                                        addLink(res+' | '+name,link,iconimage,fanart)
                        else:
                                try:
                                        link3 = abrir_url(iframe_url)
                                except: link3 = ''
                                tit=re.compile('<title>(.+?)</title>').findall(link3)
                                if link3 != '':
                                        if 'sd' in link3 and 'md' in link3:
                                                match=re.compile('videoPresets = {"sd":"(.+?)","md":"(.+?)"}').findall(link3)
                                                if not match:
                                                        match=re.compile('"videos":{"sd":"(.+?)&expire_at=.+?","hd":"(.+?)&expire_at=.+?"}').findall(link3)
                                                        if not match: match=re.compile('"url":"(.+?)"').findall(link3)
                                                if match:
                                                        addLink('SD | '+name,match[0][0],iconimage,fanart)
                                                        addLink('HD | '+name,match[0][1],iconimage,fanart)
                                        elif 'sd' in link3 and 'md' not in link3:
                                                match=re.compile('videoPresets = {"sd":"(.+?)"').findall(link3)
                                                if match:
                                                        addLink('SD | '+name,match[0],iconimage,fanart)
                                        elif 'hd' in link3 and 'md' not in link3:
                                                match=re.compile('"md":"(.+?)"}').findall(link3)
                                                if match:
                                                        addLink('HD | '+name,match[0],iconimage,fanart)                            
		except: pass
	elif "flashx" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
        elif "youtu" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	elif "youwatch" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	elif "hostingbulk" in url:
		try:
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
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
        elif "vidto.me" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
    			#checker = url.replace('.avi','.srt')
		except: pass
	elif "dropvideo" in url:
		try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			imagem = re.compile('var vscreenshot = "(.+?)"').findall(link3)
			if imagem: iconimage = imagem[0]
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
	elif "putlocker" in url:
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
    	elif "nowvideo" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	elif "primeshare" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	elif "allmyvideos" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	elif "vkontakte" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	elif "videoslasher" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	elif "sockshare" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	elif "firedrive" in url:
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
    	elif "videowood" in url:
                try:
                        iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			tit=re.compile('title: "(.+?)"').findall(link3)
			match=re.compile('file: "(.+?)"').findall(link3)
			subtitle=re.compile("addSubtitles[(]'(.+?)'").findall(link3)
			if match:
                                #addLink(tit[0]+match[0],match[0],'')
                                if subtitle == []:
                                        checker = ''
                                        url = match[0].replace('\/','/')
                                else:
                                        checker = subtitle[0]
                                        url = match[0].replace('\/','/')
                        else:
                                iframe_url = url.replace('/embed/','/video-link/')
                                link3 = abrir_url(iframe_url)
                                if link3 != []:
                                        match=re.compile('"url":"(.+?)"}').findall(link3)
                                        if subtitle == []:
                                                checker = ''
                                                url = match[0].replace('\/','/')
                                        else:
                                                checker = subtitle[0]
                                                url = match[0].replace('\/','/')
			#addLink(name+match[0],match[0],'')
    		except:pass
    	elif "movshare" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	elif "video.tt" in url or "videott" in url:
                try:
                        iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
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
			#addLink(url,'','')
    		except:pass
    	elif "videomega" in url or '(Videomega)' in name:
		try:
                        #addLink(url,'','','')
                        urli,checker = videomega_resolver(iframe_url)
                        uli=re.compile('(.+?)[|]Host=').findall(urli)
                        if uli: url=uli[0]
                        else: url=urli
                        #addLink(url,'','','')
##                        if "iframe" not in url:
##                                id_videomega = re.compile('ref=(.*)').findall(url)[0]
##                                iframe_url = 'http://videomega.tv/iframe.php?ref=' + id_videomega
##                        else: iframe_url = url
##                        print iframe_url
##                        link3 = abrir_url(iframe_url)
##                        match=re.compile('document.write\(unescape\("(.+?)"\)').findall(link3)
##                        print match
##                        tit=re.compile('<div id="title">&nbsp;&nbsp;&nbsp;(.+?)</div>').findall(link3)
##                        video_url_escape = urllib.unquote(match[0])
##                        match=re.compile('file: "(.+?)"').findall(video_url_escape)
##                        subtitle=re.compile('"file": "(.+?)"').findall(video_url_escape)
##                        if subtitle==[]:
##                                subtitle=re.compile('[[][{]file: "(.+?)"').findall(video_url_escape)      
##                        if subtitle == []:
##                                checker = ''
##                                url = match[0]
##                        else:
##                                checker = subtitle[0].replace('http://videomega.tv/servesrt.php?s=','')
##                                url = match[0]
##                        #addLink(checker,match[0],'')
		except: pass
	nome_addon = nomeAddon
	#addLink(url,'','','')
	#return
        #if 'vk.com' not in url and 'video.mail.ru' not in url and 'video.tt' not in url:
        if 'vk.com' not in iframe_url and 'video.mail.ru' not in iframe_url and 'videoapi.my.mail' not in iframe_url and 'vidzi.tv' not in iframe_url and 'playfreehd' not in iframe_url  and 'thevideo.me' not in iframe_url:# and 'iiiiiiiiii' in url:
                try:
                        #addLink(name,url,iconimage,fanart)
                        playlist = xbmc.PlayList(1)
                        playlist.clear()

                        liz=xbmcgui.ListItem(name, thumbnailImage=iconimage)
                        #xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,liz)
                        playlist.add(url,liz)

                        MyPlayer(nome_addon=nome_addon,checker=checker).PlayStream(playlist)
                        
##                        playlist = xbmc.PlayList(1)
##                        playlist.clear()             
##                        playlist.add(url,xbmcgui.ListItem(name, thumbnailImage=str(iconimage)))
##                        MyPlayer(nome_addon=nome_addon,checker=checker).PlayStream(playlist)
                except: pass
        #return
                
class MyPlayer(xbmc.Player):
        def __init__( self, *args, **kwargs ):
                xbmc.Player.__init__( self )
                #self.nomeaddon = kwargs[ "nome_addon" ]
                self.checkerSubs = kwargs[ "checker" ]
                self.Playable = 'Nao'

        def PlayStream(self, playlist):  
                self.play(playlist)
                progress.close()
                if self.checkerSubs == '' or self.checkerSubs == None: pass
                else: self.setSubtitles(self.checkerSubs)
                if not self.isPlaying() and self.Playable == 'Nao':
                        xbmcgui.Dialog().ok('SITES dos PORTUGAS', 'Este stream está offline.', 'Tente outro stream.')
                while self.isPlaying():
                        xbmc.sleep(1000)

        def onPlayBackStarted(self):
                self.Playable = 'Sim'
                progress.close()
                            
        def onPlayBackEnded(self):
                self.Playable = 'Nao'
                progress.close()

        def onPlayBackStopped(self):
                self.Playable = 'Nao'
                progress.close()


def PLAY_episodes(url,name,iconimage,checker,fanart):#,nomeAddon):
        nomeserver = name
        name = nomeserver.replace('(Videomega)','')
        nomeAddon = ''
        percent = 0
        message = ''
        progress.create(name, 'A preparar vídeo...')
        progress.update( percent, "", message, "" )
        #addLink(url,'','')
        url = url.replace('////','///')
        try:
                import urlresolver
        except: pass
        #if 'vk.com' not in url and 'video.mail.ru' not in url:
                #dp = xbmcgui.DialogProgress()
                #dp.create(name,'A sincronizar vídeos e legendas')
                #dp.update(0)
        if '///' in url:
                if '////' in url: nome = re.compile('////(.+?)[)].+?[(].+?[)]').findall(url)
                else: nome = re.compile('///(.+?)[)].+?[(].+?[)]').findall(url)
                if not nome:
                        nome = re.compile('///(.*)').findall(url)
                        if nome: nomefilme = nome[0]
                else: nomefilme = nome[0] + ')'
                urlvid = re.compile('(.+?)///').findall(url)
                if urlvid: url = urlvid[0]
                #if nomefilme.replace(' ','') != name.replace(' ',''):
                #name = nomefilme + ' ' + name
        iframe_url = url
	if "clipstube" in url :
		try:
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			match=re.compile("var hq_video_file = '(.+?)'").findall(link3)
			if not match: match=re.compile("var normal_video_file = '(.+?)'").findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
				checker = ''
				url = match[0]
			else:
				checker = subtitle[0]
				url = match[0]
		except: pass
	elif "drive.google" in url or "docs.google" in url :
		try:
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
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
        elif "streamin" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	elif "thevideo.me" in url:
		try:
                        _nomeservidor_ = []
                        _linkservidor_ = []
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			if link3:
                                mp4 = re.compile('[|]logo[|]100[|](.+?)[|]label[|]').findall(link3)
                                if mp4: mp4 = mp4[0]
                                else: mp4='111'
			else: mp4 = '--'
			imagem = re.compile('<span id=.+?><img src="(.+?)"').findall(link3)
			if imagem:
                                iconimage = imagem[0]
                                ip = re.compile('(.+?)/i/').findall(iconimage)
                                if ip: ip = ip[0]
			todassources = re.compile('[|]sharing(.+?)sources[|]').findall(link3)
			sourc = re.compile('.+?[|](.+?)0p[|]').findall(todassources[0])
			addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,iconimage,False,fanart)
			i = 1
			a = 0
			if len(sourc) == 5:
                                sources = re.compile('[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|]').findall(todassources[0])
                                for x in range(5):
                                        url = ip + '/' + sources[0][a] + '/v.' + mp4
                                        _linkservidor_.append(url)
                                        a = a + 2
                                        _nomeservidor_.append(sources[0][i]+'0p | '+name)
                                        addLink(sources[0][i]+'0p | '+name,url,iconimage,fanart)
                                        i = a + 1
        
                        if len(sourc) == 4:
                                sources = re.compile('[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|]').findall(todassources[0])
                                for x in range(4):
                                        url = ip + '/' + sources[0][a] + '/v.' + mp4
                                        _linkservidor_.append(url)
                                        a = a + 2
                                        _nomeservidor_.append(sources[0][i]+'0p | '+name)
                                        addLink(sources[0][i]+'0p | '+name,url,iconimage,fanart)
                                        i = a + 1
        
			if len(sourc) == 3:
                                sources = re.compile('[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|]').findall(todassources[0])
                                for x in range(3):
                                        url = ip + '/' + sources[0][a] + '/v.' + mp4
                                        _linkservidor_.append(url)
                                        a = a + 2
                                        _nomeservidor_.append(sources[0][i]+'0p | '+name)
                                        addLink(sources[0][i]+'0p | '+name,url,iconimage,fanart)
                                        i = a + 1
 
			if len(sourc) == 2:
                                sources = re.compile('[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|]').findall(todassources[0])
                                for x in range(2):
                                        url = ip + '/' + sources[0][a] + '/v.' + mp4
                                        _linkservidor_.append(url)
                                        a = a + 2
                                        _nomeservidor_.append(sources[0][i]+'0p | '+name)
                                        addLink(sources[0][i]+'0p | '+name,url,iconimage,fanart)
                                        i = a + 1
                                           
                        if len(sourc) == 1:
                                sources = re.compile('[|]mp4[|](.+?)[|](.+?)0p[|]').findall(todassources[0])
                                url = ip + '/' + sources[0][0] + '/v.' + mp4
                                addLink(sources[0][1]+'0p | '+name,url,iconimage,fanart)
                                #addLink(sources[0][0],'','','')
                                nm = sources[0][1]+'0p | '+name
                                _nomeservidor_.append(nm)
                                _linkservidor_.append(url)
          
		except: pass
##		progress.close()
##                index = xbmcgui.Dialog().select('Escolha o Stream', _nomeservidor_)
##                if index > -1:
##                        playlist = xbmc.PlayList(1)
##                        playlist.clear()             
##                        playlist.add(_linkservidor_[index],xbmcgui.ListItem(name, thumbnailImage=str(iconimage)))
##                        MyPlayer(nome_addon=nome_addon,checker=checker).PlayStream(playlist)
##                        #Play.PLAY_movie(_linkservidor_[index],_nomeservidor_[index],iconimage,'',fanart)
                        
	elif "vidzi.tv" in url:       
		try:
                        if 'embed-' in iframe_url:
                                iframe_url = url.replace('vidzi.tv/embed-','vidzi.tv/')
                                tiraurl = re.compile('(.+?)-').findall(iframe_url)
                                if tiraurl: iframe_url = tiraurl[0]+'.html'
                        print iframe_url
                        link3 = abrir_url(iframe_url)
                        match=re.compile('file: "(.+?)"').findall(link3)
                        subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
                        imagem = re.compile('image: "(.+?)"').findall(link3)
                        if imagem: iconimage = imagem[0]
                        addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,iconimage,False,fanart)
                        for link in match:
                                if '.m3u8' in link:
                                        url = link
                                        addLink('m3u8 | '+name,url,iconimage,fanart)
                                if '.mp4' in link:
                                        url = link
                                        addLink('mp4 | '+name,url,iconimage,fanart)
                                if '.srt' in link: checker = link
                except: pass                
	elif "vidzen" in url:
		try:
                        #iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
                                checker = ''
			else:
				checker = subtitle[0]
			match=re.compile('streamer: "(.+?)"').findall(link3)
			if not match:
                                match=re.compile('file: "(.+?)"').findall(link3)
                                if match: url = match[0]
                        else: url = match[0]
			if not match:
                                match=re.compile('var[|]type[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|][|](.+?)[|].+?provider[|](.+?)[|](.+?)[|]file').findall(link3)
                                if match: url = 'http://'+match[0][4]+'.'+match[0][3]+'.'+match[0][2]+'.'+match[0][1]+':'+match[0][0]+'/'+match[0][6]+'/v.'+match[0][5]#+'?start=0'
			imagem=re.compile('[[]IMG[]](.+?)[[]/IMG[]]').findall(link3)
			if imagem: iconimage = imagem[0]
			#addLink(url,url,iconimage,fanart)
		except: pass
	elif "playfreehd" in url:
		try:
			if 'embed' in iframe_url:
                                print iframe_url
                                link3 = abrir_url(iframe_url)
                                imagem = re.compile("var preview_img = '(.+?)';").findall(link3)
                                if imagem: iconimage = imagem[0]
                                match=re.compile("var hq_video_file = '(.+?)';").findall(link3)
                                if match:
                                        url = match[0]+'?start=0'
                                        if '.flv' in url: flv = '.flv | '
                                        else: flv = ''
                                        addLink('HQ | '+flv+name,url,iconimage,fanart)
                                match=re.compile("var normal_video_file = '(.+?)';").findall(link3)
                                if match:
                                        url = match[0]+'?start=0'
                                        if '.flv' in url: flv = '.flv | '
                                        else: flv = ''
                                        addLink('SD | '+flv+name,url,iconimage,fanart)
                        if 'embed' not in iframe_url:
                                print iframe_url
                                link3 = abrir_url(iframe_url)
                                link = re.compile('<param name="FlashVars" value="plugins=plugins/proxy.swf&proxy.link=http://filehoot.com/(.+?).html;captions.file').findall(link3)
                                if link:
                                        link = 'http://filehoot.com/embed-'+link[0]+'-640x360.html'
                                        link3 = abrir_url(link)
                                imagem = re.compile('image: "(.+?)"').findall(link3)
                                if imagem: iconimage = imagem[0]
                                match=re.compile('file: "(.+?)"').findall(link3)
                                if match:
                                        
                                        url = match[0]
                                        iframe_url = url
		except: pass
	elif "divxstage" in url:
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
	elif "vidbull" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
    			#addLink(match[0],match[0],'')
    			#return url
		except: pass
	elif "vodlocker" in url:
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
	elif "played.to" in url:
                #addLink('sim1','','')
		try:
                        #addLink('sim','','')
                        #iframe_url = url
                        print iframe_url
                        link3 = abrir_url(iframe_url)
                        imagem = re.compile('image: "(.+?)"').findall(link3)
			if imagem: iconimage = imagem[0]
                        tit=re.compile('var vtitle = "(.+?)"').findall(link3)
                        match=re.compile('file: "(.+?)"').findall(link3)
                        subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
                        if subtitle == []:
                                checker = ''
                                if match: url = match[0]
                        else:
                                if checker: checker = subtitle[0]
                                if match: url = match[0]
                except: pass
	elif "cloudzilla" in url:
		try:
			#iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			imagem = re.compile('var vthumbnail = "(.+?)"').findall(link3)
			if imagem: iconimage = imagem[0]
			tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			match=re.compile('var vurl = "(.+?)"').findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
				checker = ''
				if match: url = match[0]
			else:
				if checker: checker = subtitle[0]
				if match: url = match[0]
			#addLink(match[0],match[0],'')
			#return
		except: pass
	elif "vodlocker" in url:
		try:
                        #if '/video/' in url: url = url.replace('/video/','/embed/')
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
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
	elif "vk.com" in url:
		try:
                        #if '/video/' in url: url = url.replace('/video/','/embed/')
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,artfolder,False,fanart)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
                        match=re.compile('var vars = {.+?"url240":"(.+?)"').findall(link3)
			if match: addLink('240p | '+name,match[0].replace('\/','/'),iconimage,fanart)
			match=re.compile('var vars = {.+?"url360":"(.+?)"').findall(link3)
			if match: addLink('360p | '+name,match[0].replace('\/','/'),iconimage,fanart)
			match=re.compile('var vars = {.+?"url480":"(.+?)"').findall(link3)
			if match: addLink('480p | '+name,match[0].replace('\/','/'),iconimage,fanart)
			match=re.compile('var vars = {.+?"url720":"(.+?)"').findall(link3)
			if match: addLink('720p | '+name,match[0].replace('\/','/'),iconimage,fanart)
			match=re.compile('var vars = {.+?"url1080":"(.+?)"').findall(link3)
			if match: addLink('1080p | '+name,match[0].replace('\/','/'),iconimage,fanart)
		except: pass
        elif "streamcloud" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	elif "filehoot" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	elif "video.mail.ru" in url or 'videoapi.my.mail' in url:
                #addLink(url,'','')
		try:
			iframe_url = url###http://api.video.mail.ru/videos/mail/megafilmeshdtv/_myvideo/874.json
			print iframe_url
			#addLink(iframe_url,'','')
			addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,artfolder,False,fanart)
			iframe_url = iframe_url.replace('/embed','').replace('.html','.json')
                        try:
                                link3 = abrir_url(iframe_url)
                        except: link3 = ''
                        if link3 != '':
                                imagem = re.compile('"poster":"(.+?)"').findall(link3)
                                if imagem: iconimage = imagem[0]
                                match = re.compile('"key":"(.+?)","url":"(.+?)"').findall(link3)
                                for res,link in match:
                                        addLink(res+' | '+name,link,iconimage,fanart)
                        else:
                                try:
                                        link3 = abrir_url(iframe_url)
                                except: link3 = ''
                                tit=re.compile('<title>(.+?)</title>').findall(link3)
                                if link3 != '':
                                        if 'sd' in link3 and 'md' in link3:
                                                match=re.compile('videoPresets = {"sd":"(.+?)","md":"(.+?)"}').findall(link3)
                                                if not match:
                                                        match=re.compile('"videos":{"sd":"(.+?)&expire_at=.+?","hd":"(.+?)&expire_at=.+?"}').findall(link3)
                                                        if not match: match=re.compile('"url":"(.+?)"').findall(link3)
                                                if match:
                                                        addLink('SD | '+name,match[0][0],iconimage,fanart)
                                                        addLink('HD | '+name,match[0][1],iconimage,fanart)
                                        elif 'sd' in link3 and 'md' not in link3:
                                                match=re.compile('videoPresets = {"sd":"(.+?)"').findall(link3)
                                                if match:
                                                        addLink('SD | '+name,match[0],iconimage,fanart)
                                        elif 'hd' in link3 and 'md' not in link3:
                                                match=re.compile('"md":"(.+?)"}').findall(link3)
                                                if match:
                                                        addLink('HD | '+name,match[0],iconimage,fanart)                            
		except: pass
	elif "flashx" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
        elif "youtu" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	elif "youwatch" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	elif "hostingbulk" in url:
		try:
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
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
        elif "vidto.me" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
    			#checker = url.replace('.avi','.srt')
		except: pass
	elif "dropvideo" in url:
		try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			imagem = re.compile('var vscreenshot = "(.+?)"').findall(link3)
			if imagem: iconimage = imagem[0]
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
	elif "putlocker" in url:
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
    	elif "nowvideo" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	elif "primeshare" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	elif "allmyvideos" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	elif "vkontakte" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	elif "videoslasher" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	elif "sockshare" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	elif "firedrive" in url:
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
    	elif "videowood" in url:
                #addLink(url,'','','')
                try:
                        iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			tit=re.compile('title: "(.+?)"').findall(link3)
			match=re.compile('file: "(.+?)"').findall(link3)
			subtitle=re.compile("addSubtitles[(]'(.+?)'").findall(link3)
			if match:
                                #addLink(tit[0]+match[0],match[0],'')
                                if subtitle == []:
                                        checker = ''
                                        url = match[0].replace('\/','/')
                                else:
                                        checker = subtitle[0]
                                        url = match[0].replace('\/','/')
                        else:
                                iframe_url = url.replace('/embed/','/video-link/')
                                link3 = abrir_url(iframe_url)
                                if link3 != []:
                                        match=re.compile('"url":"(.+?)"}').findall(link3)
                                        if subtitle == []:
                                                checker = ''
                                                url = match[0].replace('\/','/')
                                        else:
                                                checker = subtitle[0]
                                                url = match[0].replace('\/','/')
			#addLink(name+match[0],match[0],'')
    		except:pass
    	elif "movshare" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	elif "video.tt" in url or "videott" in url:
                try:
                        iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
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
			#addLink(url,'','')
    		except:pass
    	elif "videomega" in url or '(Videomega)' in nomeserver:
		try:
                        #addLink(nomeserver,'','','')
                        urli,checker = videomega_resolver(iframe_url)
                        uli=re.compile('(.+?)[|]Host=').findall(urli)
                        if uli: url=uli[0]
                        else: url=urli
##                        if "iframe" not in url:
##                                id_videomega = re.compile('ref=(.*)').findall(url)[0]
##                                iframe_url = 'http://videomega.tv/iframe.php?ref=' + id_videomega
##                        else: iframe_url = url
##                        print iframe_url
##                        link3 = abrir_url(iframe_url)
##                        match=re.compile('document.write\(unescape\("(.+?)"\)').findall(link3)
##                        print match
##                        tit=re.compile('<div id="title">&nbsp;&nbsp;&nbsp;(.+?)</div>').findall(link3)
##                        video_url_escape = urllib.unquote(match[0])
##                        match=re.compile('file: "(.+?)"').findall(video_url_escape)
##                        subtitle=re.compile('"file": "(.+?)"').findall(video_url_escape)
##                        if subtitle==[]:
##                                subtitle=re.compile('[[][{]file: "(.+?)"').findall(video_url_escape)      
##                        if subtitle == []:
##                                checker = ''
##                                url = match[0]
##                        else:
##                                checker = subtitle[0].replace('http://videomega.tv/servesrt.php?s=','')
##                                url = match[0]
##                        #addLink(checker,match[0],'','')
		except: pass
	nome_addon = nomeAddon
	#addLink(url,'','','')
	#return
        #if 'vk.com' not in url and 'video.mail.ru' not in url and 'video.tt' not in url:
        if 'vk.com' not in iframe_url and 'video.mail.ru' not in iframe_url and 'videoapi.my.mail' not in iframe_url and 'vidzi.tv' not in iframe_url and 'playfreehd' not in iframe_url  and 'thevideo.me' not in iframe_url:# and 'iiiiiiiiii' in url:
                try:
                        #addLink(name,url,iconimage,fanart)
                        playlist = xbmc.PlayList(1)
                        playlist.clear()

                        liz=xbmcgui.ListItem(name, thumbnailImage=iconimage)
                        #xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,liz)
                        playlist.add(url,liz)

                        MyPlayer(nome_addon=nome_addon,checker=checker).PlayStream(playlist)
                        
##                        playlist = xbmc.PlayList(1)
##                        playlist.clear()             
##                        playlist.add(url,xbmcgui.ListItem(name, thumbnailImage=str(iconimage)))
##                        MyPlayer(nome_addon=nome_addon,checker=checker).PlayStream(playlist)
                except: pass
        #return

def abrir_url_tommy(url,referencia,form_data=None,erro=True):
	print "A fazer request tommy de: " + url
	from t0mm0.common.net import Net
	net = Net()
	try:
		if form_data==None:link = net.http_GET(url,referencia).content
		else:link= net.http_POST(url,form_data=form_data,headers=referencia).content.encode('latin-1','ignore')
		return link

	except urllib2.HTTPError, e:
		return "Erro"
	except urllib2.URLError, e:
		return "Erro"
	
def videomega_resolver(referer):
        #referer='http://www.tuga-filmes.com/toy-story-perdidos-no-tempo/'
        
        ref = '---'
        #return
	html = abrir_url(referer)
	if re.search('http://videomega.tv/iframe.js',html):
		lines = html.splitlines()
		aux = ''
		for line in lines:
			if re.search('http://videomega.tv/iframe.js',line):
				aux = line
				break;
		ref = re.compile('ref="(.+?)"').findall(line)[0]
	else:
		try:
			hashk = re.compile('"http://videomega.tv/validatehash.php\?hashkey\=(.+?)"').findall(html)[0]
			ref = re.compile('ref="(.+?)"').findall(abrir_url("http://videomega.tv/validatehash.php?hashkey="+hashk))[0]
			#addLink(ref,'','','')
		except:
			try:
				hashk = re.compile("'http://videomega.tv/validatehash.php\?hashkey\=(.+?)'").findall(html)[0]
				ref = re.compile('ref="(.+?)"').findall(abrir_url("http://videomega.tv/validatehash.php?hashkey="+hashk))[0]
				#addLink(ref,'','','')
			except:
				try:
                                        iframe = re.compile('"http://videomega.tv/iframe.php\?(.+?)"').findall(html)[0] + '&'
                                        ref = re.compile('ref=(.+?)&').findall(iframe)[0]
				except:
                                        try:
                                                iframe = re.compile('"http://videomega.tv/cdn.php\?(.+?)"').findall(html)[0] + '&'
                                                ref = re.compile('ref=(.+?)&').findall(iframe)[0]
                                        except:
                                                try:
                                                        iframe = re.compile('<iframe.+?src=http://videomega.tv/cdn.php\?(.+?) frameborder.+?</iframe>').findall(html)[0] + '&'
                                                        ref = re.compile('ref=(.+?)&').findall(iframe)[0]
                                                except:
                                                        try:
                                                                #iframe = re.compile('=(.*)').findall(referer)[0] + '&'
                                                                ref = re.compile('=(.*)').findall(referer)[0]
                                                        except: pass



        if '+link+' in ref: ref = re.compile('=(.*)').findall(referer)[0]
        #addLink(referer+'-'+ref,'','','')
        if ref=='---':
                url = 'http://videomega.tv/validatehash.php?hashkey='+hashk#+'&width=650&height=480&val=1'
                #url = 'http://videomega.tv/cdn.php?ref='+hashk+'&width=650&height=480&val=1'
                ref_data={'Host':'videomega.tv',
			  'Connection':'Keep-alive',
			  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			  'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
			  'Referer':referer}
                ref = re.compile('ref="(.+?)"').findall(abrir_url_tommy(url,ref_data))[0]
        #addLink(referer+'-'+ref,'','','')

        ref_data={'Host':'videomega.tv',
                  'Connection':'Keep-alive',
		  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		  'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
		  'Referer':referer}
        url = 'http://videomega.tv/cdn.php?ref='+ref+'&width=638&height=431&val=1'
	iframe_html = abrir_url_tommy(url,ref_data)
	url_video = re.compile('<source src="(.+?)"').findall(iframe_html)[0]
	try: url_legendas = re.compile('<track kind="captions" src="(.+?)"').findall(iframe_html)[0]
	except: url_legendas = '-'
        return url_video,url_legendas

##	
##	ref_data={'Host':'videomega.tv',
##			  'Connection':'Keep-alive',
##			  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
##			  'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
##			  'Referer':referer}
##	url = 'http://videomega.tv/iframe.php?ref=' + ref #anterior
##	url = 'http://videomega.tv/cdn.php?ref='+ref #agora
##	iframe_html = abrir_url_tommy(url,ref_data)
##	code = re.compile('document.write\(unescape\("(.+?)"\)\)\;').findall(iframe_html)
##	id = re.compile('<div id="(.+?)" name="adblock"').findall(iframe_html)[0]
##	texto = ''
##	for c in code:
##		aux = urllib.unquote(c)
##		if re.search(id,aux):
##			texto = aux
##			break
##	if texto == '': return ['-','-']
##	try: url_video = re.compile('file:"(.+?)"').findall(texto)[0]
##	except: 
##		try: url_video = re.compile('file: "(.+?)"').findall(texto)[0]
##		except: url_video = '-'
##	if not 'mp4' in url_video: return ['-','-']
##	try: url_legendas = re.compile('http://videomega.tv/servesrt.php\?s=(.+?).srt').findall(texto)[0] + '.srt'
##	except: url_legendas = '-'
##	ref_data={'Host':url_video.split('/')[2],
##			  'Connection':'Keep-alive',
##			  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
##			  'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
##			  'Referer':'http://videomega.tv/player/jwplayer.flash.swf'}
##	#addLink(urltrailer+url_video+headers_str(ref_data),'','','')
##	return url_video+headers_str(ref_data),url_legendas

def headers_str(headers):
	start = True
	headers_str = ''
	for k,v in headers.items():
		if start:
			headers_str += '|'+urllib.quote_plus(k)+'='+urllib.quote_plus(v)
			start = False
		else: headers_str += '&'+urllib.quote_plus(k)+'='+urllib.quote_plus(v)
	return headers_str
                
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
	
params=get_params()
url=None
name=None
mode=None
checker=None
iconimage=None
fanart=None
year=None
plot=None
genre=None
episod=None
air=None
namet=None
urltrailer=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: urltrailer=urllib.unquote_plus(params["urltrailer"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: namet=urllib.unquote_plus(params["namet"])
except: pass
try: nome=urllib.unquote_plus(params["nome"])
except: pass
try: mode=int(params["mode"])
except: pass
try: checker=urllib.unquote_plus(params["checker"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: fanart=urllib.unquote_plus(params["fanart"])
except: pass
try: plot=urllib.unquote_plus(params["plot"])
except: pass
try: year=urllib.unquote_plus(params["year"])
except: pass
try: genre=urllib.unquote_plus(params["genre"])
except: pass
try: episod=urllib.unquote_plus(params["episod"])
except: pass
try: air=urllib.unquote_plus(params["air"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Checker: "+str(checker)
print "Iconimage: "+str(iconimage)
print "Plot: "+str(plot)
print "Year: "+str(year)
print "Genre: "+str(genre)
print "Fanart: "+str(fanart)
print "Episode: "+str(episod)
print "Namet: "+str(namet)
print "Urltrailer: "+str(urltrailer)
