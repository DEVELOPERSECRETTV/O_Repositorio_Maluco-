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
import TugaFilmesTV,TopPt,TugaFilmesCom,MovieTuga,Series,FilmesAnima,Pesquisar,Mashup

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

progress = xbmcgui.DialogProgress()

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    PLAY    ------------------------------------------------------------------#


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
        iframe_url = url
	if "clipstube" in url :
		try:
			iframe_url = url
			print iframe_url
			link3 = PLAY_abrir_url(iframe_url)
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
		except: pass
	if "vidzi.tv" in url:       
		try:
                        if 'embed-' in iframe_url:
                                iframe_url = url.replace('vidzi.tv/embed-','vidzi.tv/')
                                tiraurl = re.compile('(.+?)-').findall(iframe_url)
                                if tiraurl: iframe_url = tiraurl[0]+'.html'
                        print iframe_url
                        link3 = PLAY_abrir_url(iframe_url)
                        match=re.compile('file: "(.+?)"').findall(link3)
                        subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
                        imagem = re.compile('image: "(.+?)"').findall(link3)
                        if imagem: iconimage = imagem[0]
                        addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,artfolder,False,'')
                        for link in match:
                                if '.m3u8' in link:
                                        url = link
                                        addLink('m3u8 | '+name,url,iconimage)
                                if '.mp4' in link:
                                        url = link
                                        addLink('mp4 | '+name,url,iconimage)
                                if '.srt' in link: checker = link
                except: pass                
	if "vidzen" in url:
		try:
                        #iframe_url = url
			print iframe_url
			link3 = PLAY_abrir_url(iframe_url)
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
			#addLink(url,url,iconimage)
		except: pass
	if "playfreehd" in url:
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
                        link3 = PLAY_abrir_url(iframe_url)
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
			link3 = PLAY_abrir_url(iframe_url)
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
			addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,artfolder,False,'')
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
                        match=re.compile('var vars = {.+?"url240":"(.+?)"').findall(link3)
			if match: addLink('240p | '+name,match[0].replace('\/','/'),iconimage)
			match=re.compile('var vars = {.+?"url360":"(.+?)"').findall(link3)
			if match: addLink('360p | '+name,match[0].replace('\/','/'),iconimage)
			match=re.compile('var vars = {.+?"url480":"(.+?)"').findall(link3)
			if match: addLink('480p | '+name,match[0].replace('\/','/'),iconimage)
			match=re.compile('var vars = {.+?"url720":"(.+?)"').findall(link3)
			if match: addLink('720p | '+name,match[0].replace('\/','/'),iconimage)
			match=re.compile('var vars = {.+?"url1080":"(.+?)"').findall(link3)
			if match: addLink('1080p | '+name,match[0].replace('\/','/'),iconimage)
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
			addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,artfolder,False,'')
			if 'sd' in link3 and 'md' in link3:
                                match=re.compile('videoPresets = {"sd":"(.+?)","md":"(.+?)"}').findall(link3)
                                #match=re.compile('"videos":{"sd":"(.+?)&expire_at=.+?","hd":"(.+?)&expire_at=.+?"}').findall(link3)
                                #matchHD=re.compile('"videos":{"sd":"(.+?)&expire_at=.+?","hd":"(.+?)&expire_at=.+?"}').findall(link3)
                                #vl=match[0][0]+'&video_key='+v_key[0][0]+'&expire_at='+v_key[0][1]
                                if match:
                                        addLink('SD | '+name,match[0][0],iconimage)
                                        addLink('HD | '+name,match[0][1],iconimage)
			if 'sd' in link3 and 'md' not in link3:
                                match=re.compile('videoPresets = {"sd":"(.+?)"').findall(link3)
                                #match=re.compile('"videos":{"sd":"(.+?)"}').findall(link3)
                                if match:
                                        #url=match[0]
                                        addLink('SD | '+name,match[0],iconimage)
                        if 'hd' in link3 and 'md' not in link3:
                                match=re.compile('"md":"(.+?)"}').findall(link3)
                                #match=re.compile('"videos":{"hd":"(.+?)"}').findall(link3)
                                if match:
                                        addLink('HD | '+name,match[0],iconimage)
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
    			#checker = url.replace('.avi','.srt')
		except: pass
	if "dropvideo" in url:
		try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
			iframe_url = url
			print iframe_url
			link3 = PLAY_abrir_url(iframe_url)
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
			link3 = PLAY_abrir_url(iframe_url)
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
                                link3 = PLAY_abrir_url(iframe_url)
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
			#addLink(url,'','')
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
	nome_addon = nomeAddon
	#addLink(url+'  ','','')
	#return
        #if 'vk.com' not in url and 'video.mail.ru' not in url and 'video.tt' not in url:
        if 'vk.com' not in iframe_url and 'video.mail.ru' not in iframe_url and 'vidzi.tv' not in iframe_url:# and 'iiiiiiiiii' in url:
                try:
                        playlist = xbmc.PlayList(1)
                        playlist.clear()             
                        playlist.add(url,xbmcgui.ListItem(name, thumbnailImage=str(iconimage)))
                        MyPlayer(nome_addon=nome_addon,checker=checker).PlayStream(playlist)
                except: pass
                
class MyPlayer(xbmc.Player):
        def __init__( self, *args, **kwargs ):
                xbmc.Player.__init__( self )
                self.nomeaddon = kwargs[ "nome_addon" ]
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
                progress.close()

        def onPlayBackStopped(self):
                progress.close()
                
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
	liz.setProperty('fanart_image',artfolder + 'FAN3.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addLink1(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'FAN3.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,checker,fanart):
        text = 'nnnnnn'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&checker="+urllib.quote_plus(checker)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'FAN3.jpg')
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
	liz.setProperty('fanart_image',artfolder + 'FAN3.jpg')
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


