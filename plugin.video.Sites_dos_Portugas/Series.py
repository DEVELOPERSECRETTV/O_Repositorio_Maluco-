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



import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket


addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

 
#mensagemok = xbmcgui.Dialog().ok
	
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def SERIES_pesquisar(nome_pesquisa):
        progress = xbmcgui.DialogProgress()
        percent = 0
        message = ''
        site = ''
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar...'+site, message, "" )
        xbmc.sleep( 500 )
        if selfAddon.getSetting('movies-view') == "0":
                addDir1('[B][COLOR blue]Séries:[/COLOR][/B]','','','',False,'')
                addDir1('','','','',False,'')
        pesquisou = nome_pesquisa
        if '|' in url:
                _url = re.compile('(.+?)[|](.*)').findall(url)
                url_TFV = _url[0][0]
                url_TPT = _url[0][1]
        else:
                if 'tuga-filmes' in url:
                        url_TPT = ''
                        url_TFV = url
                if 'toppt' in url:
                        url_TFV = ''
                        url_TPT = url
        a = 0
        site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv'
        percent = int( ( a / 2.0 ) * 100)
        message = ''
        progress.update(percent, 'A Procurar em '+site, message, "")
        print str(a) + " de " + str(int(a))
        xbmc.sleep( 100 )
	SERIES_encontrar_fontes_pesquisa_TFV(url_TFV,pesquisou)
	a = 1
	site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
	percent = int( ( a / 2.0 ) * 100)
        message = ''
        progress.update(percent, 'A Procurar em '+site, message, "")
        print str(a) + " de " + str(int(a))
        xbmc.sleep( 100 )
	SERIES_encontrar_fontes_TPT(url_TPT)
	if selfAddon.getSetting('movies-view') == "0":
                addDir1('','','',artfolder + 'banner.png',False,'')		
                addDir('[COLOR yellow]Pesquisar[/COLOR]','url',1,artfolder + 'banner.png','nao','')
                addDir('[COLOR yellow]Menu Principal[/COLOR]','','',artfolder + 'banner.png','nao','')
        a = 2
	site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
	percent = int( ( a / 2.0 ) * 100)
        message = ''
        progress.update(percent, 'A Procurar em '+site, message, "")
        print str(a) + " de " + str(int(a))
        xbmc.sleep( 100 )
        

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def SERIES_encontrar_fontes_pesquisa_TFV(url,pesquisou):
        if selfAddon.getSetting('movies-view') == "0": addDir1('[B][COLOR yellow]----- [/COLOR][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv[B][COLOR yellow] -----[/COLOR][/B]','','','',False,'')
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
				if 'Season' in nome or 'Temporada' in nome or 'Seasons' in nome or 'Temporadas' in nome:
                                        n = re.compile('[(](.+?)[)]').findall(nome)
                                        if n: nome = n[0]
                                        addDir('[B][COLOR orange]TFV | [/COLOR][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0] + ')[/COLOR][COLOR red] (' + qualidade[0] + ')[/COLOR]',urletitulo[0][0],42,thumbnail[0].replace('s72-c','s320'),'sim','')
			except: pass
	else:
		if selfAddon.getSetting('movies-view') == "0": addDir1('- No Match Found -','','','',False,'')
	return

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def SERIES_encontrar_fontes_TPT(url):
        if selfAddon.getSetting('movies-view') == "0":
                addDir1('[B][COLOR yellow]----- [/COLOR][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][COLOR yellow] -----[/COLOR][/B]','','','',False,'')
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	if '<div class="postmeta-primary">' in html_source: items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	else:
                if selfAddon.getSetting('movies-view') == "0": addDir1('- No Match Found -','','','',False,'')
                return
	if items != []:
                num_f = 0
		print len(items)
		for item in items:
                        audio_filme = ''
                        ano_filme = ''
                        qualidade = ''
                        urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(item)
                        if 'title=' in urletitulo[0][0]: urletitulo = re.compile('<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>').findall(item)
                        qualidade = re.compile("<b>QUALIDADE:.+?/b>(.+?)<br/>").findall(item)
                        if not qualidade: qualidade = re.compile("<b>VERSÃO:.+?</b>(.+?)<br/>").findall(item)
                        ano = re.compile("<b>ANO:.+?/b>(.+?)<br/>").findall(item)
                        audio = re.compile("<b>AUDIO:.+?/b>(.+?)<br/>").findall(item)
                        thumbnail = re.compile('src="(.+?)"').findall(item)
                        if thumbnail: thumb = thumbnail[0].replace('s72-c','s320')
                        print urletitulo,thumbnail
                        url = urletitulo[0][0]
                        nome = urletitulo[0][1]
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#038;',"&")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('(PT-PT)',"")
                        nome = nome.replace('(PT/PT)',"")
                        nome = nome.replace('[PT-PT]',"")
                        nome = nome.replace('[PT/PT]',"")
                        nome = nome.replace('[PT-BR]',"")
                        nome = nome.replace('[PT/BR]',"")
                        nome = nome.replace(' (PT-PT)',"")
                        nome = nome.replace(' (PT/PT)',"")
                        nome = nome.replace(' [PT-PT]',"")
                        nome = nome.replace(' [PT/PT]',"")
                        nome = nome.replace(' [PT-BR]',"")
                        nome = nome.replace(' [PT/BR]',"")
                        nome = nome.replace('  '," ")
                        if audio:
                                if len(audio[0]) > 15:
                                        audio = re.compile('<b>AUDIO: </b>(.+?)<span style="color: red;"><b>(.+?)</b></span><br/>').findall(item)
                                        if audio:
                                                audio_filme = ': ' + audio[0][0] + audio[0][1]
                                        else:
                                                audio = re.compile('<b>AUDIO: </b> <b><span style="color: red;">(.+?)</span> <span style="color: #38761d;">(.+?)</span></b><br/>').findall(item)
                                                if audio:
                                                        audio_filme = audio[0][0] + audio[0][1]
                                                        if 'Portug' or 'PORTUG' in audio_filme:
                                                                audio_filme = ': PT-PT'
                                else:
                                        audio_filme = ': ' + audio[0]
                        if not audio:
                                audio = re.compile("\nAUDIO:\xc2\xa0(.+?)<br/>").findall(item)
                                if audio:
                                        audio_filme = ': ' + audio[0]
                                else:
                                        audio_filme = ''
                        if not ano:
                                ano = re.compile("\nANO:\xc2\xa0(.+?)<br/>").findall(item)
                                if ano:
                                        ano_filme = ': ' + ano[0].replace(' ','')
                                else:
                                        ano_filme = ''     
                        if ano:
                                ano_filme = ano[0].replace(' ','')
                                a_q = re.compile('\d+')
                                qq_aa = a_q.findall(nome)
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) == 4:
                                                tirar_ano = '(' + str(q_a_q_a) + ')'
                                                nome = nome.replace(tirar_ano,'')
                        if qualidade:
                                qualidade = qualidade[0]
                                qualidade = qualidade.replace('[',' - ')
                                qualidade = qualidade.replace(']','')
                        else:
                                qualidade = re.compile("\nQUALIDADE:\xc2\xa0(.+?)<br/>").findall(item)
                                if qualidade:
                                        qualidade = qualidade[0]
                                        qualidade = qualidade.replace('[',' - ')
                                        qualidade = qualidade.replace(']','')
                                else:
                                        qualidade = ''
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        tirar_ano = '(' + str(q_a_q_a) + ')'
                                        nome = nome.replace(tirar_ano,'')
                        try:
                                if 'Season' in nome or 'Temporada' in nome or 'Seasons' in nome or 'Temporadas' in nome:
                                        n = re.compile('[[](.+?)[]][[](.+?)[]]').findall(nome)
                                        if n: nome = n[0][0]+' - '+n[0][1]
                                        else:
                                                n = re.compile('[[](.+?)[]] [[](.+?)[]]').findall(nome)
                                                if n: nome = n[0][0]+' - '+n[0][1]
                                                else:
                                                        n = re.compile('[[](.+?)[]]').findall(nome)
                                                        if n: nome = n[0]
                                        #if 'series' in genero:
                                                #if 'online' in genero:
                                                        #if 'OP\xc3\x87\xc3\x83O' in item:
                                        nome = nome.replace('Season','Temporada')
                                        nome = nome.replace('Seasons','Temporadas')
                                        addDir('[B][COLOR orange]TPT | [/COLOR][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR]',url,233,thumbnail[0].replace('s72-c','s320'),'','')
                                        num_f = num_f + 1
                        except: pass
        if num_f == 0:
                if selfAddon.getSetting('movies-view') == "0": addDir1('- No Match Found -','','','',False,'')
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
