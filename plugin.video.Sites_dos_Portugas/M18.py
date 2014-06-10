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


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket
from array import array
from string import capwords

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------    M18_TFC  --------------------------------------------------------------#


   
def M18_TFC_Link_M18(artfolder):
        url_m18 = 'http://www.blogger.com/blogin.g?blogspotURL=http://www.tuga-filmes.info/'
	html_m18 = M18_abrir_url(url_m18)
	m18 = re.compile('<a class="maia-button maia-button-primary" href="(.+?)" target="_parent">COMPREENDO E (.+?)</a>').findall(html_m18)
	print m18
	addDir(m18[0][1],m18[0][0],84,'','nao','')

def M18_TFC_Menu_M18(url,artfolder):
        addDir('[COLOR yellow]Ver Todos[/COLOR]',url,84,artfolder + 'banner1.png','nao','')
                                
def M18_TFC_encontrar_fontes_M18(url):
        url_m18 = 'http://www.blogger.com/blogin.g?blogspotURL=http://www.tuga-filmes.info/'
	html_m18 = M18_abrir_url(url_m18)
	m18 = re.compile('<a class="maia-button maia-button-primary" href="http://www.tuga-filmes.info/(.+?)" target="_parent">').findall(html_m18)
	print m18
	url = 'http://www.tuga-filmes.info/search/label/Filmes' + m18[0]
	try:
		html_source = M18_abrir_url(url)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)<br />", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
			urletitulo = re.compile("<a href=\'(.+?)\' title=.+?>Assistir Online - </div>(.+?)<div id=\'player\'>").findall(item)
			thumbnail = re.compile('src="(.+?)"').findall(item)
			print urletitulo,thumbnail
			try:
				addDir(urletitulo[0][1].replace('&#8217;',"'"),urletitulo[0][0] + m18[0],82,thumbnail[0].replace('s72-c','s320'),'','')
			except: pass
	else:
		items = re.compile("<a href=\'(.+?)\' title=.+?>Assistir Online - </div>(.+?)<div id=\'player\'>").findall(html_source)
		for endereco,nome in items:
			addDir(nome.replace('&#8217;',"'"),endereco + m18[0],73,'','','')
	proxima = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
	try:
                addDir1('','','','',False,'')
		addDir('[B][COLOR red]Página Seguinte >>[/B][/COLOR]' + proxima[0].replace('amp;','') + m18[0],proxima[0].replace('amp;','') + m18[0],84,"",'','')
	except: pass
	
def M18_TFC_resolve_not_videomega_M18(name,url,id_video,conta_id_video):
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
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,70,iconimage,'','')
		except: pass
        if "vidto.me" in url:
		try:
                        url = 'http://vidto.me/' + id_video + '.html'
                        print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,70,iconimage,'','')
		except: pass
        if "dropvideo" in url:
		try:
                        url = 'http://dropvideo.com/embed/' + id_video
			print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,70,iconimage,'','')
		except:pass
	if "streamin.to" in url:
                try:
                        url = 'http://streamin.to/embed-' + id_video + '.html'
			print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,70,iconimage,'','')
                except:pass                        
        if "putlocker" in url:
                try:
                        url = 'http://www.putlocker.com/embed/' + id_video
                        print url
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Putlocker)[/COLOR][/B]',url,70,iconimage,'','')
    		except:pass
    	if "nowvideo" in url:
                try:
                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video
                        print url
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,70,iconimage,'','')
    		except:pass
    	return

def M18_TFC_encontrar_videos_M18(name,url):
        conta_id_video = 0
	addDir1('[B][COLOR blue]' + name + '[/COLOR][/B]','','',iconimage,False,'')
        addDir1('','','',iconimage,False,'')
        try:
                fonte = M18_abrir_url(url)
        except: fonte = ''
        fontes = re.findall("Link Alternativo(.+?)", fonte, re.DOTALL)
        numero_de_fontes = len(fontes)
	try:
		link2=M18_abrir_url(url)
	except: link2 = ''
	if link2:
                #-------------------- Videomega
                match = re.compile('<iframe .+? src="(.+?)" .+?></iframe>').findall(link2)
                conta_video = len(match)
		for url in match:
                        if "videomega" in match[0]:
                                conta_id_video = conta_id_video + 1
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',match[0],70,iconimage,'','')
                        if "play.flashx" in match[0]:
                                conta_id_video = conta_id_video + 1
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](FlashX)[/COLOR][/B]',match[0],70,iconimage,'','')
		if numero_de_fontes > 0:
                        conta_video = 0
                        match = re.compile('<a href="(.+?)">Link Alternativo</a>').findall(link2)
                        url = match[0]
                        conta_id_video = conta_id_video + 1
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamcloud)[/COLOR][/B]',url,70,iconimage,'','')

                #-------------------------------



#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------    M18_TFV  --------------------------------------------------------------#


def M18_TFV_Menu_M18(artfolder):
        addDir1('[B][COLOR blue]Menu M+18[/COLOR][/B]','','',artfolder + 'banner.png',False,'')
        addDir1('','','',artfolder + 'banner.png',False,'')
	addDir('[COLOR yellow]Ver Todos[/COLOR]','http://extraporn.net/',52,artfolder + 'banner.png','nao','')
	addDir('[COLOR yellow]Categorias[/COLOR]','url',50,artfolder + 'banner.png','nao','')
        addDir('[COLOR yellow]30 mais Recentes[/COLOR]','url',51,artfolder + 'banner.png','nao','')
        addDir1('','','',artfolder + 'banner.png',False,'')
	addDir('Pesquisar','http://extraporn.net/?s=',54,artfolder + 'banner.png','nao','')

def M18_TFV_Menu_M18_Categorias(artfolder):
        url_categorias = 'http://extraporn.net/'
        html_categorias_source = M18_abrir_url(url_categorias)
	html_items_categorias = re.findall('<div id="categories-3" class="widget_categories">(.*?)</option>\n</select>', html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile('<option class="level-0" value=".+?">(.+?)</option>').findall(item_categorias)
                for nome_categoria in filmes_por_categoria:
                        endereco_categoria = 'http://extraporn.net/category/' + nome_categoria
                        addDir('[COLOR yellow]' + nome_categoria + '[/COLOR] ',endereco_categoria,52,artfolder + 'banner.png','nao','')

def M18_TFV_Menu_M18_30_Recentes(artfolder):
        url_recente = 'http://extraporn.net/'
        html_recente_source = M18_abrir_url(url_recente)
	html_items_recente = re.findall('<div id="recent-posts-3" class="widget_recent_entries">(.*?)<!--/sidebar-->', html_recente_source, re.DOTALL)
        print len(html_items_recente)
        for item_recente in html_items_recente:
                filmes_por_recente = re.compile('<a href="(.+?)" title="(.+?)">').findall(item_recente)
                for endereco_recente,nome_recente in filmes_por_recente:
                        nome_recente = nome_recente.replace('&#8217;',"'")
                        nome_recente = nome_recente.replace('&#8211;',"-")
                        addDir('[COLOR yellow]' + nome_recente + '[/COLOR] ',endereco_recente,53,artfolder + 'banner.png','nao','')

def M18_TFV_pesquisar_M18():
	keyb = xbmc.Keyboard('', 'Escreva o parâmetro de pesquisa')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		encode=urllib.quote(search)
		url_pesquisa = 'http://extraporn.net/?s=' + str(encode)
		pesquisou = str(encode)
		M18_TFV_encontrar_fontes_pesquisa_M18(url_pesquisa,pesquisou)


def M18_TFV_encontrar_fontes_pesquisa_M18(url,pesquisou):
        pesquisado = pesquisou.replace('%20',' ')
        addDir1('[B][COLOR blue]Pesquisou : [/COLOR]( ' + pesquisado + ' )[/B]','','',artfolder + 'banner.png',False,'')
        addDir1('','','',artfolder + 'banner.png',False,'')
	try:
		html_source = M18_abrir_url(url)
	except: html_source = ''
	items = re.findall('<div class="boxentry">(.*?)<div class="boxmetadata">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
			urletitulo = re.compile('<a href="(.+?)" title="(.+?)">').findall(item)
			thumbnail = re.compile('src="(.+?)"').findall(item)
			print urletitulo,thumbnail
			nome = urletitulo[0][1]
			nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
			try:
				addDir(nome,urletitulo[0][0],53,thumbnail[0].replace('s72-c','s320'),'','')
			except: pass
	else:
		items = re.compile('<a href="(.+?)" title="(.+?)">').findall(html_source)
		for endereco,nome in items:
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
			addDir(nome,endereco,53,'','','')
	addDir1('','','',artfolder + 'banner.png',False,'')
	addDir('[COLOR red]Nova Pesquisa[/COLOR]','http://www.tuga-filmes.tv/search?q=',56,artfolder + 'banner.png','nao','')

def M18_TFV_encontrar_fontes_M18(url):
	try:
		html_source = M18_abrir_url(url)
	except: html_source = ''
	items = re.findall('<div class="boxentry">(.*?)<div class="boxmetadata">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
			urletitulo = re.compile('<a href="(.+?)" title="(.+?)">').findall(item)
			thumbnail = re.compile('src="(.+?)"').findall(item)
			print urletitulo,thumbnail
			nome = urletitulo[0][1]
			nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
			try:
				addDir(nome,urletitulo[0][0],53,thumbnail[0].replace('s72-c','s320'),'','')
			except: pass
	else:
		items = re.compile('<a href="(.+?)" title="(.+?)">').findall(html_source)
		for endereco,nome in items:
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
			addDir(nome,endereco,53,'','','')
	proxima = re.compile(".*<a href='(.+?)' class='nextpostslink'>&raquo;</a>").findall(html_source)
        try:
                addDir1('','','',artfolder + 'banner.png',False,'')
                addDir("[B][COLOR red]Página Seguinte >>[/B][/COLOR]",proxima[0],52,artfolder + 'banner.png','','')
        except: pass

def M18_TFV_encontrar_videos_M18(name,url):
        conta_id_video = 0
	addDir1('[B][COLOR blue]' + name + '[/COLOR][/B]','','',iconimage,False,'')
        addDir1('','','',iconimage,False,'')
        try:
                fonte = M18_abrir_url(url)
        except: fonte = ''
        fontes = re.findall("videosection(.+?)", fonte, re.DOTALL)
        numero_de_fontes = len(fontes)
	try:
		link2=M18_abrir_url(url)
	except: link2 = ''
	if link2:
                #-------------------- Videomega
                match = re.compile('<iframe style="background-color: black"width="650" height="450" scrolling="no" frameborder="0" src="(.+?)"></iframe>').findall(link2)
                conta_video = len(match)
		for url in match:
                        conta_id_video = conta_id_video + 1
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',match[0],30,iconimage,'','')
                #-------------------------------



#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#


	
def M18_abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

#----------------------------------------------------------------------------------------------------------------------------------------------#
              
def M18_get_params():
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


          
params=M18_get_params()
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


