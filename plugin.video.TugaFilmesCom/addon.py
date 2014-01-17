#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2014 OMaluco
#
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


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,urlresolver
from array import array

addon_id = 'plugin.video.TugaFilmesCom'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
breve_array = array('c')
a=[]

mensagemok = xbmcgui.Dialog().ok


#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#



def MenuPrincipal():
        addDir1('[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].com','','',artfolder + 'banner1.png',False,'')
        addDir1('','','',artfolder + 'banner1.png',False,'')
	addDir('[COLOR yellow]Menu Filmes[/COLOR]','url',8,artfolder + 'banner1.png','nao','')
	addDir('[COLOR yellow]Animação[/COLOR]','http://www.tuga-filmes.com/search/label/Anima%C3%A7%C3%A3o',3,artfolder + 'banner1.png','nao','')
        addDir1('','','',artfolder + 'banner1.png',False,'')
	addDir('Pesquisar','http://www.tuga-filmes.com/search?q=',5,artfolder + 'banner1.png','nao','')

def Menu_Filmes():
        addDir1('[B][COLOR blue]Menu Filmes[/COLOR][/B]','','',artfolder + 'banner1.png',False,'')
        addDir1('','','',artfolder + 'banner1.png',False,'')
	addDir('[COLOR yellow]Ver Todos[/COLOR]','http://www.tuga-filmes.com/',3,artfolder + 'banner1.png','nao','')
	addDir('[COLOR yellow]Destaques[/COLOR]','http://www.tuga-filmes.com/search/label/destaque',3,artfolder + 'banner1.png','nao','')
	addDir('[COLOR yellow]2013[/COLOR]','http://www.tuga-filmes.com/search/label/-%20Filmes%202013',3,artfolder + 'banner1.png','nao','')
        addDir('[COLOR yellow]Top 10[/COLOR]','url',10,artfolder + 'banner1.png','nao','')
        #addDir('[COLOR yellow]Brevemente[/COLOR]','url',12,artfolder + 'banner1.png','nao','')
	addDir('[COLOR yellow]Categorias[/COLOR]','url',9,artfolder + 'banner1.png','nao','')
	addDir('[B][COLOR red]M+18[/B][/COLOR]','url',17,artfolder + 'banner1.png','nao','')
        addDir1('','','',artfolder + 'banner1.png',False,'')
	addDir('Pesquisar','http://www.tuga-filmes.com/search?q=',5,artfolder + 'banner1.png','nao','')

def Menu_Series():
        addDir1('[B][COLOR blue]Menu Séries[/COLOR][/B]','','',artfolder + 'banner1.png',False,'')
        addDir1('','','',artfolder + 'banner1.png',False,'')
	addDir('[COLOR yellow]Ver Todas[/COLOR]','url',12,artfolder + 'banner1.png','nao','')
        addDir('[COLOR yellow]Episódios Recentes[/COLOR]','http://www.tuga-filmes.tv/search/label/S%C3%A9ries',15,artfolder + 'banner1.png','nao','')
        addDir1('','','',artfolder + 'banner1.png',False,'')
	addDir('Pesquisar','http://www.tuga-filmes.com/search?q=',16,artfolder + 'banner1.png','nao','')

def Menu_Filmes_Top_10():
        url_top_10 = 'http://www.tuga-filmes.com/'
        top_10_source = abrir_url(url_top_10)
        addDir1('[B][COLOR blue]TOP 10[/COLOR][/B]','','',artfolder + 'banner1.png',False,'')
        addDir1('','','',artfolder + 'banner1.png',False,'')
        filmes_top_10 = re.compile("<img alt=\'\' border=\'0\' height=\'72\' src=\'(.+?)\' width=\'72\'/>\n</a>\n</div>\n<div class=\'item-title\'><a href=\'(.+?)\'>(.+?)</a></div>\n</div>\n<div style=\'clear: both;\'>").findall(top_10_source)
	for iconimage_filmes_top_10,endereco_top_10,nome_top_10 in filmes_top_10:
		addDir(nome_top_10,endereco_top_10,4,iconimage_filmes_top_10.replace('s72-c','s320').replace('.gif','.jpg'),'nao','')

def Menu_Filmes_Por_Categorias():
        url_categorias = 'http://www.tuga-filmes.com/'
        html_categorias_source = abrir_url(url_categorias)
        addDir1('[B][COLOR blue]Categorias[/COLOR][/B]','','',artfolder + 'banner1.png',False,'')
        addDir1('','','',artfolder + 'banner1.png',False,'')
	html_items_categorias = re.findall("<div id=\'nav-cat\'>(.*?)</div>", html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<a href=\'/(.+?)\'>(.+?)</a>").findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        categoria_endereco = url_categorias + endereco_categoria
                        addDir('[COLOR yellow]' + nome_categoria + '[/COLOR]',categoria_endereco,3,artfolder + 'banner1.png','nao','')

def Menu_Filmes_Brevemente():
        url_brevemente = 'http://www.tuga-filmes.com/'
	html_brevemente_source = abrir_url(url_brevemente)
	addDir1('[B][COLOR blue]Brevemente[/COLOR][/B]','','',artfolder + 'banner1.png',False,'')
        addDir1('','','',artfolder + 'banner1.png',False,'')
        todos_brevemente = re.findall("<marquee(.*?)</marquee>", html_brevemente_source, re.DOTALL)
        print len(todos_brevemente)
        for items_brevemente in todos_brevemente:
                item_brevemente = re.compile("<a href=\'(.+?)\' target=\'_blank\'><img height=\'140px\' src=\'(.+?)\' width=\'100px\'/></a>").findall(items_brevemente)
                for brevemente_url,iconimage_brevemente in item_brevemente:
                        nome_brevemente = re.compile('http://www.tuga-filmes.com/.+?/.+?/(.+?).html').findall(brevemente_url)
                        nome_brevemente = nome_brevemente[0].replace('-',' ')
                        addDir('[COLOR yellow]' + nome_brevemente + '[/COLOR]',brevemente_url,4,iconimage_brevemente,'nao','')
   
def Link_M18():
        url_m18 = 'http://www.blogger.com/blogin.g?blogspotURL=http://www.tuga-filmes.info/'
	html_m18 = abrir_url(url_m18)
	m18 = re.compile('<a class="maia-button maia-button-primary" href="(.+?)" target="_parent">COMPREENDO E (.+?)</a>').findall(html_m18)
	print m18
	addDir(m18[0][1],m18[0][0],15,'','nao','')

def Menu_M18(url):
        addDir('[COLOR yellow]Ver Todos[/COLOR]',url,15,artfolder + 'banner1.png','nao','')

        

#----------------------------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------  Pesquisar  ---------------------------------------------------------------#



def pesquisar_filmes():
	keyb = xbmc.Keyboard('', 'Escreva o parâmetro de pesquisa')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		encode=urllib.quote(search)
		url_pesquisa = 'http://www.tuga-filmes.com/search?q=' + str(encode)
		encontrar_fontes_filmes(url_pesquisa)

def pesquisar_series():
	keyb = xbmc.Keyboard('', 'Escreva o parâmetro de pesquisa')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		encode=urllib.quote(search)
		url_pesquisa = 'http://www.tuga-filmes.com/search?q=' + str(encode)
		encontrar_fontes_series(url_pesquisa)	



#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#

		

def encontrar_fontes_filmes(url):
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)</span><br />", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
			urletitulo = re.compile("<a href=\'(.+?)\' title=.+?>Assistir Online - </div>(.+?)<div id=\'player\'>").findall(item)
			thumbnail = re.compile('src="(.+?)"').findall(item)
			print urletitulo,thumbnail
			try:
				addDir(urletitulo[0][1].replace('&#8217;',"'"),urletitulo[0][0],4,thumbnail[0].replace('s72-c','s320').replace('.gif','.jpg'),'','')
			except: pass
	else:
		items = re.compile("<a href=\'(.+?)\' title=.+?>Assistir Online - </div>(.+?)<div id=\'player\'>").findall(html_source)
		for endereco,nome in items:
			addDir(nome.replace('&#8217;',"'"),endereco,4,'','','')
	proxima = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
	try:
                addDir1('','','','',False,'')
		addDir("[B][COLOR red]Página Seguinte >>[/B][/COLOR]",proxima[0].replace('#038;',''),3,"",'','')
	except: pass

#----------------------------------------------------------------------------------------------------------------------------------------------#
	
def resolve_not_videomega_filmes(name,url,id_video,conta_id_video):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link4=response.read()
        response.close()
        match = re.compile('<iframe frameborder="0" height="450" scrolling="no" src="(.+?)" .+?></iframe>').findall(link4)
        url=match[0]
        if "videomega" in url:
		try:
                        url = 'http://videomega.tv/iframe.php?ref=' + id_video
                        print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,1,iconimage,'','')
		except: pass
        if "vidto.me" in url:
		try:
                        url = 'http://vidto.me/' + id_video + '.html'
                        print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,1,iconimage,'','')
		except: pass
        if "dropvideo" in url:
		try:
                        url = 'http://dropvideo.com/embed/' + id_video
			print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,1,iconimage,'','')
		except:pass
	if "streamin.to" in url:
                try:
                        url = 'http://streamin.to/embed-' + id_video + '.html'
			print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,1,iconimage,'','')
                except:pass                        
        if "putlocker" in url:
                try:
                        url = 'http://www.putlocker.com/embed/' + id_video
                        print url
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Putlocker)[/COLOR][/B]',url,1,iconimage,'','')
    		except:pass
    	if "nowvideo" in url:
                try:
                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video
                        print url
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,1,iconimage,'','')
    		except:pass
    	return

#----------------------------------------------------------------------------------------------------------------------------------------------#

def encontrar_videos_filmes(name,url):
        conta_id_video = 0
	addDir1('[B][COLOR blue]' + name + '[/COLOR][/B]','','',iconimage,False,'')
        addDir1('','','',iconimage,False,'')
        try:
                fonte = abrir_url(url)
        except: fonte = ''
        fontes = re.findall("Clique aqui(.+?)", fonte, re.DOTALL)
        numero_de_fontes = len(fontes)
	if fonte:
                #-------------------- Videomega
                match = re.compile('<iframe frameborder="0" height="450" scrolling="no" src="(.+?)" .+?></iframe>').findall(fonte)
                conta_video = len(match)
		for url in match:
                        conta_id_video = conta_id_video + 1
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',match[0],1,iconimage,'','')
                #-------------------------------
                #----------------- Not Videomega
		if numero_de_fontes > 0:
                        conta_video = 0
                        match = re.compile('<a href="(.+?)" .+? target=".+?">Clique aqui para ver!</a>').findall(fonte)
                        url = match[0]
                        if url != '':
                                try:
                                        for url in match:
                                                identifica_video = re.compile('=(.*)').findall(match[conta_video])
                                                id_video = identifica_video[0]
                                                conta_video = conta_video + 1
                                                conta_id_video = conta_id_video + 1
                                                resolve_not_videomega_filmes(name,url,id_video,conta_id_video)
                                except:pass
                #-------------------------------



#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------    M18   -----------------------------------------------------------------#


                                
def encontrar_fontes_M18(url):
        url_m18 = 'http://www.blogger.com/blogin.g?blogspotURL=http://www.tuga-filmes.info/'
	html_m18 = abrir_url(url_m18)
	m18 = re.compile('<a class="maia-button maia-button-primary" href="http://www.tuga-filmes.info/(.+?)" target="_parent">').findall(html_m18)
	print m18
	url = 'http://www.tuga-filmes.info/search/label/Filmes' + m18[0]
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)<br />", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
			urletitulo = re.compile("<a href=\'(.+?)\' title=.+?>Assistir Online - </div>(.+?)<div id=\'player\'>").findall(item)
			thumbnail = re.compile('src="(.+?)"').findall(item)
			print urletitulo,thumbnail
			try:
				addDir(urletitulo[0][1].replace('&#8217;',"'"),urletitulo[0][0] + m18[0],13,thumbnail[0].replace('s72-c','s320'),'','')
			except: pass
	else:
		items = re.compile("<a href=\'(.+?)\' title=.+?>Assistir Online - </div>(.+?)<div id=\'player\'>").findall(html_source)
		for endereco,nome in items:
			addDir(nome.replace('&#8217;',"'"),endereco + m18[0],4,'','','')
	proxima = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
	try:
                addDir1('','','','',False,'')
		addDir('[B][COLOR red]Página Seguinte >>[/B][/COLOR]' + proxima[0].replace('amp;','') + m18[0],proxima[0].replace('amp;','') + m18[0],15,"",'','')
	except: pass

#----------------------------------------------------------------------------------------------------------------------------------------------#
	
def resolve_not_videomega_M18(name,url,id_video,conta_id_video):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link4=response.read()
        response.close()
        match = re.compile('<iframe frameborder="0" height="450" scrolling="no" src="(.+?)" .+?></iframe>').findall(link4)
        url=match[0]
        if "videomega" in url:
		try:
                        url = 'http://videomega.tv/iframe.php?ref=' + id_video
                        print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,1,iconimage,'','')
		except: pass
        if "vidto.me" in url:
		try:
                        url = 'http://vidto.me/' + id_video + '.html'
                        print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,1,iconimage,'','')
		except: pass
        if "dropvideo" in url:
		try:
                        url = 'http://dropvideo.com/embed/' + id_video
			print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,1,iconimage,'','')
		except:pass
	if "streamin.to" in url:
                try:
                        url = 'http://streamin.to/embed-' + id_video + '.html'
			print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,1,iconimage,'','')
                except:pass                        
        if "putlocker" in url:
                try:
                        url = 'http://www.putlocker.com/embed/' + id_video
                        print url
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Putlocker)[/COLOR][/B]',url,1,iconimage,'','')
    		except:pass
    	if "nowvideo" in url:
                try:
                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video
                        print url
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,1,iconimage,'','')
    		except:pass
    	return

#----------------------------------------------------------------------------------------------------------------------------------------------#

def encontrar_videos_M18(name,url):
        conta_id_video = 0
	addDir1('[B][COLOR blue]' + name + '[/COLOR][/B]','','',iconimage,False,'')
        addDir1('','','',iconimage,False,'')
        try:
                fonte = abrir_url(url)
        except: fonte = ''
        fontes = re.findall("Link Alternativo(.+?)", fonte, re.DOTALL)
        numero_de_fontes = len(fontes)
	try:
		link2=abrir_url(url)
	except: link2 = ''
	if link2:
                #-------------------- Videomega
                match = re.compile('<iframe .+? src="(.+?)" .+?></iframe>').findall(link2)
                conta_video = len(match)
		for url in match:
                        if "videomega" in match[0]:
                                conta_id_video = conta_id_video + 1
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',match[0],1,iconimage,'','')
                        if "play.flashx" in match[0]:
                                conta_id_video = conta_id_video + 1
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](FlashX)[/COLOR][/B]',match[0],1,iconimage,'','')
		if numero_de_fontes > 0:
                        conta_video = 0
                        match = re.compile('<a href="(.+?)">Link Alternativo</a>').findall(link2)
                        url = match[0]
                        conta_id_video = conta_id_video + 1
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamcloud)[/COLOR][/B]',url,1,iconimage,'','')

                #-------------------------------



#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#



def play_movie(url,name,iconimage,checker,fanart):
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
	if "putlocker" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
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
    	if "videomega" in url:
		try:
			if "iframe" not in url:
				id_videomega = re.compile('ref=(.*)').findall(url)[0]
				iframe_url = 'http://videomega.tv/iframe.php?ref=' + id_videomega
			else: iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			match=re.compile('document.write\(unescape\("(.+?)"\)').findall(link3)
			print match
			tit=re.compile('<div id="title">&nbsp;&nbsp;&nbsp;(.+?)</div>').findall(link3)
			video_url_escape = urllib.unquote(match[0])
			match=re.compile('file: "(.+?)"').findall(video_url_escape)
			subtitle=re.compile('"file": "(.+?)"').findall(video_url_escape)
			if subtitle == []:
				checker = ''
				url = match[0]
			else:
				checker = subtitle[0]
				url = match[0]
		except: pass
	dp = xbmcgui.DialogProgress()
	dp.create("TugaFilmesTv",'A sincronizar vídeos e legendas')
	dp.update(0)
	playlist = xbmc.PlayList(1)
	playlist.clear()             
	playlist.add(url,xbmcgui.ListItem(name, thumbnailImage=str(iconimage)))
	addLink('Voltar',url,'')
	dp.update(1, 'A reproduzir o filme.')
	if dp.iscanceled(): return
        dp.close()
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)
	if checker == '' or checker == None: pass
	else: xbmcPlayer.setSubtitles(checker)

#----------------------------------------------------------------------------------------------------------------------------------------------#
	
def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

#----------------------------------------------------------------------------------------------------------------------------------------------#
              
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

#----------------------------------------------------------------------------------------------------------------------------------------------#

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'five_wall_color.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addLink1(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'five_wall_color.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,checker,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&checker="+urllib.quote_plus(checker)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'five_wall_color.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir1(name,url,mode,iconimage,folder,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'five_wall_color.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
        return ok


        
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#


          
params=get_params()
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


if mode==None or url==None or len(url)<1:
        print ""
        MenuPrincipal()

elif mode==1:
	print ""
	play_movie(url,name,iconimage,checker,fanart)

elif mode==2:
	MenuPrincipal()

elif mode==3:
	encontrar_fontes_filmes(url)

elif mode==4:
	encontrar_videos_filmes(name,url)

elif mode==5:
        pesquisar_filmes()

elif mode==6:
        resolve_videomega_filmes(url,conta_id_video)

elif mode==7:
        resolve_not_videomega_filmes(name,url,id_video,conta_id_video,nome_fonte_video)

elif mode==8:
        Menu_Filmes()

elif mode==9:
        Menu_Filmes_Por_Categorias()

elif mode==10:
        Menu_Filmes_Top_10()

elif mode==11:
        Menu_Series()

elif mode==12:
        Menu_Filmes_Brevemente()

elif mode==13:
        encontrar_videos_M18(name,url)

elif mode==14:
        resolve_not_videomega_M18(name,url,id_video,conta_id_video,nome_fonte_video)

elif mode==15:
	encontrar_fontes_M18(url)

elif mode==16:
        pesquisar_M18()

elif mode==17:
        Link_M18()

elif mode==18:
        Menu_M18(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))

