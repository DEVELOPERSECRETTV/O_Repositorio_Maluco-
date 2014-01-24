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



import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,urlresolver

addon_id = 'plugin.video.MovieTuga'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

mensagemok = xbmcgui.Dialog().ok


#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#



def MenuPrincipal():
        addDir1('[B][COLOR green]MOVIE[/COLOR][COLOR yellow]-[/COLOR][COLOR red]TUGA[/COLOR][/B]','','',artfolder + 'banner.png',False,'')
        addDir1('','','',artfolder + 'banner.png',False,'')
	addDir('[COLOR yellow]Menu Filmes[/COLOR]','url',6,artfolder + 'banner.png','nao','')
	addDir('[COLOR yellow]Animação[/COLOR]','http://movie-tuga.blogspot.pt/search/label/animacao?&max-results=15',3,artfolder + 'banner.png','nao','')
        addDir1('','','',artfolder + 'banner.png',False,'')
	addDir('Pesquisar','http://www.tuga-filmes.com/search?q=',5,artfolder + 'banner.png','nao','')

def Menu_Filmes():
        addDir1('[B][COLOR blue]Menu Filmes[/COLOR][/B]','','',artfolder + 'banner.png',False,'')
        addDir1('','','',artfolder + 'banner.png',False,'')
	addDir('[COLOR yellow]Ver Todos[/COLOR]','http://www.movie-tuga.blogspot.pt/',3,artfolder + 'banner.png','nao','')
	addDir('[COLOR yellow]Categorias[/COLOR]','url',7,artfolder + 'banner.png','nao','')
        addDir1('','','',artfolder + 'banner.png',False,'')
	addDir('Pesquisar','http://www.tuga-filmes.com/search?q=',5,artfolder + 'banner.png','nao','')

def Menu_Filmes_Por_Categorias():
        url_categorias = 'http://www.movie-tuga.blogspot.pt/'
        html_categorias_source = abrir_url(url_categorias)
        addDir1('[B][COLOR blue]Categorias[/COLOR][/B]','','',artfolder + 'banner1.png',False,'')
        addDir1('','','',artfolder + 'banner1.png',False,'')
	html_items_categorias = re.findall("<div id=\'menu-categorias\'>(.*?)</div>", html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<a href=\'(.+?)\' title=\'.+?\'>(.+?)</a>").findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        addDir('[COLOR yellow]' + nome_categoria + '[/COLOR]',endereco_categoria + '?&max-results=15',3,artfolder + 'banner.png','nao','')

       

#----------------------------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------  Pesquisar  ---------------------------------------------------------------#



def pesquisar_filmes():
	keyb = xbmc.Keyboard('', 'Escreva o parâmetro de pesquisa')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		encode=urllib.quote(search)
		url_pesquisa = 'http://www.movie-tuga.blogspot.pt/search?q=' + str(encode)
		encontrar_fontes_pesquisa(url_pesquisa)

		
def encontrar_fontes_pesquisa(url):
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
			url = re.compile('<div class="btns"><a href="(.+?)" target="Player">').findall(item)
			if 'http' not in url[0]:
                                url[0] = 'http:' + url[0] 
                        titulo = re.compile("<strong>T\xc3\xadtulo original:</strong>(.+?)</div>").findall(item)
                        if 'Qualidade:' in item:
                                qualidade = re.compile("<strong>Qualidade:</strong>(.+?)</div>").findall(item)
                                qualidade_filme = qualidade[0].replace('&#8211;',"-")
                        else:
                                qualidade_filme = ''
                        ano = re.compile('<strong>Lan\xc3\xa7amento:</strong>(.+?)</div>').findall(item)
			thumbnail = re.compile('src="(.+?)"').findall(item)
			print url,thumbnail
			titulo[0] = titulo[0].replace('&#8217;',"'")
                        titulo[0] = titulo[0].replace('&#8211;',"-")
			try:
				addDir('[B][COLOR green]' + titulo[0] + ' [/COLOR][/B][COLOR yellow](' + ano[0] + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',url[0],4,thumbnail[0].replace('s72-c','s320'),'','')
			except: pass



#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#

		

def encontrar_fontes_filmes(url):
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        url = re.compile('<div class="btns"><a href="(.+?)" target="Player">').findall(item)
                        if 'http' not in url[0]:
                                url[0] = 'http:' + url[0] 
                        titulo = re.compile("<strong>T\xc3\xadtulo original:</strong>(.+?)</div>").findall(item)
                        if 'Qualidade:' in item:
                                qualidade = re.compile("<strong>Qualidade:</strong>(.+?)</div>").findall(item)
                                qualidade_filme = qualidade[0].replace('&#8211;',"-")
                        else:
                                qualidade_filme = ''
                        ano = re.compile('<strong>Lan\xc3\xa7amento:</strong>(.+?)</div>').findall(item)
                        thumbnail = re.compile('src="(.+?)"').findall(item)
                        print url,thumbnail
                        titulo[0] = titulo[0].replace('&#8217;',"'")
                        titulo[0] = titulo[0].replace('&#8211;',"-")
                        try:
                                addDir('[B][COLOR green]' + titulo[0] + ' [/COLOR][/B][COLOR yellow](' + ano[0] + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',url[0],4,thumbnail[0].replace('s72-c','s320'),'','')
                        except: pass
	proxima = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
	try:
                proxima_p = proxima[0].replace('%3A',':')
                addDir1('','','','',False,'')
		addDir("[B]Página Seguinte >>[/B]",proxima_p.replace('&amp;','&'),3,"",'','')
	except: pass



#----------------------------------------------------------------------------------------------------------------------------------------------#

def encontrar_videos_filmes(name,url):
        colecao = 'nao'
        addDir1(name,'','',iconimage,False,'')
        addDir1('','','',iconimage,False,'')
        conta_id_video = 0
        try:
                fonte_video = abrir_url(url)
        except: fonte_video = ''
        fontes_video = re.findall("<body>(.+?)</body>", fonte_video, re.DOTALL)
        #addDir(fontes_video[0],url,1,iconimage,'','')
        numero_de_fontes = len(fontes_video)
        for fonte_e_url in fontes_video:                
                #addDir(str(len(fontes_video)),url,1,iconimage,'','')
                match = re.compile('<option value=(.+?)>(.+?)<').findall(fonte_e_url)
                #addDir(str(len(match)),url,1,iconimage,'','')
                if '<option' in fonte_e_url:
                        for url_video_url_id,cd in match:
                                if url_video_url_id == '""':
                                        if 'CD' in cd:
                                                conta_id_video = 0
                                                cd = cd.replace('Filme Aqui','')
                                                addDir1('[COLOR blue]' + cd + '[/COLOR]','','',iconimage,False,'')
                                        if 'Cole' in cd:
                                                conta_id_video = 0
                                                colecao = 'sim'
                                                #addDir1('[COLOR blue]' + cd + '[/COLOR]','','',iconimage,False,'')
                                else:
                                        url_video_url_id = url_video_url_id.replace('"','')
                                if colecao == 'sim' and (('Breve' or 'breve') not in cd):
                                        if 'Cole' not in cd:
                                                conta_id_video = 0
                                                addDir1('[COLOR blue]' + cd + ':[/COLOR]','','',iconimage,False,'')
                                if 'http:' not in url_video_url_id:
                                        url_video = 'http:' + url_video_url_id
                                else:
                                        url_video = url_video_url_id
                                #addDir(url_video,url,1,iconimage,'','')
                                try:
                                        fonte = abrir_url(url_video)
                                except: fonte = ''
                                fontes = re.findall("<body>(.+?)</body>", fonte, re.DOTALL)
                                for fonte_id in fontes:
                                        if 'videomega' in fonte_id:
                                                try:
                                                        match = re.compile("<script type=\'text/javascript\'>ref=\'(.+?)\'").findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        id_video = match[0]
                                                        url = 'http://videomega.tv/iframe.php?ref=' + id_video
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,1,iconimage,'','')
                                                except:pass
                                        if 'vidto' in fonte_id:
                                                try:
                                                        match = re.compile('<iframe .+? src="//vidto.me/embed-(.+?)-755x390.html" .+?</iframe>').findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        id_video = match[0]
                                                        url = 'http://vidto.me/' + id_video + '.html'
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,1,iconimage,'','')
                                                except:pass
                else:
 	                if fonte_video:
 		                for fonte_id in fontes_video:
                                        if 'videomega' in fonte_id:
                                                try:
                                                        match = re.compile("<script type=\'text/javascript\'>ref=\'(.+?)\'").findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        id_video = match[0]
                                                        url = 'http://videomega.tv/iframe.php?ref=' + id_video
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,1,iconimage,'','')
                                                except:pass
                                        if 'vidto' in fonte_id:
                                                try:
                                                        match = re.compile('<iframe .+? src="//vidto.me/embed-(.+?)-755x390.html" .+?</iframe>').findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        id_video = match[0]
                                                        url = 'http://vidto.me/' + id_video + '.html'
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,1,iconimage,'','')
                                                except:pass



#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#



def play_movie(url,name,iconimage,checker,fanart):
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
	dp.create("MovieTuga",'A sincronizar vídeos e legendas')
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
	liz.setProperty('fanart_image',artfolder + 'Wall.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addLink1(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'Wall.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,checker,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&checker="+urllib.quote_plus(checker)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'Wall.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir1(name,url,mode,iconimage,folder,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'Wall.jpg')
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
        Menu_Filmes()

elif mode==7:
        Menu_Filmes_Por_Categorias()

elif mode==8:
        Menu_Filmes_Brevemente()

xbmcplugin.endOfDirectory(int(sys.argv[1]))

