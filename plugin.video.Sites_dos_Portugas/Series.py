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



import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,urlresolver


addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

 
mensagemok = xbmcgui.Dialog().ok
	
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def SERIES_pesquisar(nome_pesquisa):
        pesquisou = nome_pesquisa
        a_q = re.compile('\w+')
        qq_aa = a_q.findall(nome_pesquisa)
        nome_pesquisa = ''
        for q_a_q_a in qq_aa:
                #if len(q_a_q_a) > 2 or q_a_q_a == '1'or q_a_q_a == '2' or q_a_q_a == '3':
                if len(q_a_q_a) > 2:
                        nome_pesquisa = nome_pesquisa + ' ' + q_a_q_a
        encode=urllib.quote(nome_pesquisa)
	url_pesquisa = 'http://www.tuga-filmes.tv/search?q=' + str(encode)
	SERIES_encontrar_fontes_pesquisa_TFV(url_pesquisa,pesquisou)
	#url_pesquisa = 'http://www.tuga-filmes.com/search?q=' + str(encode)
	#SERIES_encontrar_fontes_filmes_TFC(url_pesquisa)
	#url_pesquisa = 'http://www.movie-tuga.blogspot.pt/search?q=' + str(encode)
	#SERIES_encontrar_fontes_pesquisa_MVT(url_pesquisa)
	url_pesquisa = 'http://toppt.net/?s=' + str(encode)
	SERIES_encontrar_fontes_TPT(url_pesquisa)
	addDir1('','','',artfolder + 'banner.png',False,'')		
        addDir('Pesquisar','inicio',1,artfolder + 'banner.png','nao','')
        addDir('Menu Principal','','',artfolder + 'banner.png','nao','')

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def SERIES_encontrar_fontes_pesquisa_TFV(url,pesquisou):
        addDir1('[B][COLOR blue]----- [/COLOR][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv[B][COLOR blue] -----[/COLOR][/B]','','','',False,'')
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
			urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)
			ano = re.compile("<b>Ano</b>: (.+?)<br />").findall(item)
			qualidade = re.compile("<b>Qualidade</b>: (.+?)<br />").findall(item)
			thumbnail = re.compile('src="(.+?)"').findall(item)
			print urletitulo,thumbnail
			nome = urletitulo[0][1]
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        tirar_ano = '(' + str(q_a_q_a) + ')'
                                        nome = nome.replace(tirar_ano,'')
			try:
				addDir('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0] + ')[/COLOR][COLOR red] (' + qualidade[0] + ')[/COLOR]',urletitulo[0][0],42,thumbnail[0].replace('s72-c','s320'),'sim','')
			except: pass
	else:
		addDir1('- No Match Found -','','','',False,'')
	return

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def SERIES_encontrar_fontes_TPT(url):
        addDir1('[B][COLOR blue]----- [/COLOR][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.com[/COLOR][COLOR blue] -----[/COLOR][/B]','','','',False,'')
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall('<span class="cat-links">(.*?)</article>', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        if 'Nomeados' not in item:
                                audio_filme = ''
                                urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(item)
                                if '[' in urletitulo[0][1] and ('Season' or 'Temporada' or 'Epis') not in urletitulo[0][1]:
                                        urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)[[].+?</a>').findall(item)
                                info = re.compile("<p>ANO: (.+?) AUDIO: (.+?) QUALIDADE: (.+?) TAMANHO: .+? GENERO: .+? TRAILER:").findall(item)
                                if not info: info = re.compile("<p>ANO: (.+?)AUDIO: (.+?)FORMATO: AVI XvidQUALIDADE: (.+?) TAMANHO:").findall(item)
                                if not info:
                                        qualidade = ''
                                        ano = ''
                                        audio = ''
                                        #genero = ''
                                else:
                                        qualidade = info[0][2]
                                        ano = info[0][0]
                                        audio = ': ' + info[0][1]
                                        #genero = info[0][3]
                                #if genero == '':
                                generos = re.compile('title="View all posts in online series" rel="category">(.+?)</a>').findall(item)
                                if generos:
                                        genero = generos[0]
                                else:
                                        genero = ''
                                print urletitulo
                                nome = urletitulo[0][1]
                                nome = nome.replace('&#8217;',"'")
                                nome = nome.replace('&#8211;',"-")
                                nome = nome.replace('(PT-PT)',"")
                                nome = nome.replace('(PT/PT)',"")
                                nome = nome.replace('[PT-PT]',"")
                                nome = nome.replace('[PT/PT]',"")    
                                a_q = re.compile('\d+')
                                qq_aa = a_q.findall(nome)
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) == 4:
                                                tirar_ano = '(' + str(q_a_q_a) + ')'
                                                nome = nome.replace(tirar_ano,'')
                                qualidade = qualidade.replace('[',' - ')
                                qualidade = qualidade.replace(']','')
                                try:
                                        if "Temporada" or "Season" in nome:
                                                num_mode = 242
                                        else:
                                                nome = nome.replace('['," ")
                                                nome = nome.replace(']'," ")
                                                num_mode = 233
                                        #addDir('[B][COLOR green]' + nome + '[/COLOR][/B]',urletitulo[0][0],num_mode,thumbnail[0].replace('s72-c','s320'),'','')
                                        if 'series' in genero or 'Series' in genero: addDir('[B][COLOR green]- ' + nome + '[/COLOR][/B][COLOR yellow](' + ano + ')[/COLOR][COLOR red] (' + qualidade + audio + ')[/COLOR]',urletitulo[0][0],num_mode,'','','')
                                except: pass
        else:
                addDir1('- No Match Found -','','','',False,'')
        return

#----------------------------------------------------------------------------------------------------------------------------------------------#
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
#----------------------------------------------------------------------------------------------------------------------------------------------#

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'flag.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,checker,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&checker="+urllib.quote_plus(checker)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'flag.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
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
#----------------------------------------------------------------------------------------------------------------------------------------------#
          
params=get_params()
url=None
name=None
mode=None
checker=None
iconimage=None
fanart=None

try: url=urllib.unquote_plus(params["url"])
except: pass

try: name=urllib.unquote_plus(params["name"])
except: pass

try: mode=int(params["mode"])
except: pass

try: checker=urllib.unquote_plus(params["checker"])
except: pass

try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

try: fanart=urllib.unquote_plus(params["fanart"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Checker: "+str(checker)
print "Iconimage: "+str(iconimage)



#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
