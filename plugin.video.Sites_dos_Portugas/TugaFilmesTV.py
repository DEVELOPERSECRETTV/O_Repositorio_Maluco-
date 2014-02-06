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

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#



def TFV_MenuPrincipal(artfolder):
        addDir1('[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv','','',artfolder + 'ze-TFV1.png',False,'')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
	addDir('[COLOR yellow]Menu Filmes[/COLOR]','url',37,artfolder + 'ze-TFV1.png','nao','')
	addDir('[COLOR yellow]Menu Séries[/COLOR]','url',40,artfolder + 'ze-TFV1.png','nao','')
	addDir('[COLOR yellow]Filmes Animação[/COLOR]','http://www.tuga-filmes.tv/search/label/Anima%C3%A7%C3%A3o',32,artfolder + 'ze-TFV1.png','nao','')
        addDir('[COLOR yellow]Recentes[/COLOR]','http://www.tuga-filmes.tv',32,artfolder + 'ze-TFV1.png','nao','')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
	addDir('Pesquisar','http://www.tuga-filmes.tv/search?q=',1,artfolder + 'Ze-pesquisar1.png','nao','')
	#addDir('[COLOR brown]ChangeLog[/COLOR]','http://o-repositorio-maluco.googlecode.com/svn/trunk/changelogs/changelog_TugaFilmesTV.txt',56,artfolder + 'ze-TFV1.png','nao','')
 
def TFV_Menu_Filmes(artfolder):
        addDir1('[B][COLOR blue]Menu Filmes[/COLOR][/B]','','',artfolder + 'ze-TFV1.png',False,'')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
	addDir('[COLOR yellow]Ver Todos[/COLOR]','http://www.tuga-filmes.tv/search/label/Filmes',32,artfolder + 'ze-TFV1.png','nao','')
        addDir('[COLOR yellow]Ver por Ano[/COLOR]','url',39,artfolder + 'ze-TFV1.png','nao','')
	addDir('[COLOR yellow]Categorias[/COLOR]','url',38,artfolder + 'ze-TFV1.png','nao','')
	addDir('[COLOR yellow]Top 5 da Semana[/COLOR]','url',48,artfolder + 'ze-TFV1.png','nao','')
	if selfAddon.getSetting('hide-porno') == "false":
			addDir('[B][COLOR red]M+18[/B][/COLOR]','url',49,artfolder + 'ze-TFV1.png','nao','')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
	addDir('Pesquisar','http://www.tuga-filmes.tv/search?q=',1,artfolder + 'Ze-pesquisar1.png','nao','')

def TFV_Menu_Series(artfolder):
        addDir1('[B][COLOR blue]Menu Séries[/COLOR][/B]','','',artfolder + 'ze-TFV1.png',False,'')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
	addDir('[COLOR yellow]A a Z[/COLOR]','url',41,artfolder + 'ze-TFV1.png','nao','')
        addDir('[COLOR yellow]Recentes[/COLOR]','http://www.tuga-filmes.tv/search/label/Séries',44,artfolder + 'ze-TFV1.png','nao','')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
	addDir('Pesquisar','http://www.tuga-filmes.tv/search?q=',1,artfolder + 'Ze-pesquisar1.png','nao','')

def TFV_Menu_Filmes_Top_5(artfolder):
        url_top_5 = 'http://www.tuga-filmes.tv'
        top_5_source = TFV_abrir_url(url_top_5)
        addDir1('[B][COLOR blue]TOP 5 da Semana[/COLOR][/B]','','',artfolder + 'ze-TFV1.png',False,'')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
        filmes_top_5 = re.compile("<img alt=\'.+?\' height=\'50\' src=\'.+?\' width=\'50\'/>\n<a href=\'(.+?)\'").findall(top_5_source)
	for endereco_top_5 in filmes_top_5:
                try:
                        html_source = TFV_abrir_url(endereco_top_5)
                except: html_source = ''
                items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
                if items != []:
                        print len(items)
                        for item in items:
                                urletitulo = re.compile("<b>Título Original:</b>(.+?)<br />").findall(item)
                                qualidade = re.compile("<b>Qualidade</b>: (.+?)<br />").findall(item)
                                ano = re.compile("<b>Ano</b>: (.+?)<br />").findall(item)
                                thumbnail = re.compile('src="(.+?)"').findall(item)
                                print urletitulo,thumbnail
                                try:
                                        if "Temporada" in urletitulo[0]:
                                                num_mode = 42
                                        else:
                                                num_mode = 33
                                        addDir('[B][COLOR green]' + urletitulo[0] + ' [/COLOR][/B][COLOR yellow](' + ano[0] + ')[/COLOR][COLOR red] (' + qualidade[0] + ')[/COLOR]',endereco_top_5,num_mode,thumbnail[0].replace('s72-c','s320'),'','')
                                except: pass

def TFV_Menu_Filmes_Por_Ano(artfolder):
        url_ano = 'http://www.tuga-filmes.tv'
        ano_source = TFV_abrir_url(url_ano)
        filmes_por_ano = re.compile("<a dir=\'ltr\' href=\'(.+?)\'>Filmes (.+?)</a>\n<span dir=\'ltr\'>(.+?)</span>").findall(ano_source)
	for endereco_ano,nome_ano,num_filmes_ano in filmes_por_ano:
		addDir('[COLOR yellow]' + nome_ano + '[/COLOR] ' + num_filmes_ano,endereco_ano,32,artfolder + 'ze-TFV1.png','nao','')

def TFV_Menu_Filmes_Por_Categorias(artfolder):
        url_categorias = 'http://www.tuga-filmes.tv'
        html_categorias_source = TFV_abrir_url(url_categorias)
	html_items_categorias = re.findall("<div class=\'widget Label\' id=\'Label1\'>\n<h2>Categorias</h2>(.*?)<div class=\'clear\'>", html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<a dir=\'ltr\' href=\'(.+?)\'>(.+?)</a>").findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        addDir('[COLOR yellow]' + nome_categoria + '[/COLOR] ',endereco_categoria,32,artfolder + 'ze-TFV1.png','nao','')

def TFV_Menu_Series_A_a_Z(artfolder):
        url_series = 'http://www.tuga-filmes.tv'
	html_series_source = TFV_abrir_url(url_series)
	html_items_series = re.findall("<div class=\'widget Label\' id=\'Label3\'>\n<h2>S\xc3\xa9ries(.*?)<div class=\'clear\'>", html_series_source, re.DOTALL)
        num_series = re.compile("<div class=\'widget Label\' id=\'Label3\'>\n<h2>S\xc3\xa9ries (.+?)</h2>").findall(html_series_source)
        addDir1('[B][COLOR blue]Séries[/COLOR][/B] ' + num_series[0],'','',artfolder + 'ze-TFV1.png',False,'')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
        print len(html_items_series)
        for item_series in html_items_series:
                series = re.compile("<a dir=\'ltr\' href=\'(.+?)\'>(.+?)</a>").findall(item_series)
                for endereco_series,nome_series in series:
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        addDir('[COLOR yellow]' + nome_series + '[/COLOR] ',endereco_series,47,artfolder + 'ze-TFV1.png','nao','')



#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#

		

def TFV_encontrar_fontes_filmes(url,artfolder):
	try:
		html_source = TFV_abrir_url(url)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        audio_filme = ''
                        urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)
                        qualidade = re.compile("<b>Qualidade</b>: (.+?)<br />").findall(item)
                        ano = re.compile("<b>Ano</b>: (.+?)<br />").findall(item)
                        audio = re.compile("<b>.+?udio</b>(.+?)<br />").findall(item)
                        if audio != []:
                                if 'Portug' in audio[0]:
                                        audio_filme = ': PT-PT'
                                else:
                                        audio_filme = audio[0]
                        thumbnail = re.compile('src="(.+?)"').findall(item)
                        print urletitulo,thumbnail
                        nome = urletitulo[0][1]
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('(PT-PT)',"")
                        nome = nome.replace('(PT/PT)',"")
                        nome = nome.replace('[PT-PT]',"")
                        nome = nome.replace('[PT/PT]',"")
                        if ano:
                                a_q = re.compile('\d+')
                                qq_aa = a_q.findall(nome)
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) == 4:
                                                tirar_ano = '(' + str(q_a_q_a) + ')'
                                                nome = nome.replace(tirar_ano,'')
                        if qualidade:
                                qualidade = qualidade[0]
                        else:
                                qualidade = ''
                        try:
                                if "Temporada" in urletitulo[0][1]:
                                        num_mode = 42
                                else:
                                        num_mode = 33
                                addDir('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano[0] + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR]',urletitulo[0][0],num_mode,thumbnail[0].replace('s72-c','s320'),'','')
                        except: pass
	else:
		items = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(html_source)
		for endereco,nome in items:
                        try:
                                if "Temporada" in nome:
                                        num_mode = 42
                                else:
                                        num_mode = 33
                                addDir(nome,endereco,num_mode,'','','')
                        except:pass
	proxima = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
	if proxima[0] != '':
                try:
                        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
                        addDir("[B]Página Seguinte >>[/B]",proxima[0],32,artfolder + 'ze-TFV1.png','','')
                except:pass
        
#----------------------------------------------------------------------------------------------------------------------------------------------#	


def TFV_encontrar_videos_filmes(name,url):
        conta_id_video = 0
	addDir1(name,'','',iconimage,False,'')
        addDir1('','','',iconimage,False,'')
        try:
                fonte = TFV_abrir_url(url)
        except: fonte = ''
        fontes = re.findall("Clique aqui(.+?)", fonte, re.DOTALL)
        numero_de_fontes = len(fontes)
	try:
		link2=TFV_abrir_url(url)
	except: link2 = ''
	if link2:
                #parameters = {"nome_texto" : name, "url": url, "addonid": 'TFV'}
                #nome_textbox = urllib.urlencode(parameters)
                #addDir('[COLOR blue]Sinopse[/COLOR]',nome_textbox,57,iconimage,'nao','')
                #trailer = re.compile('<b>Trailer</b>: <a href="(.+?)" target="_blank">').findall(link2)
                #if trailer: addDir('[COLOR blue]Trailer[/COLOR]',trailer[0],30,iconimage,'nao','')
                #-------------------- Videomega
                match = re.compile('<iframe frameborder="0" height="400" scrolling="no" src="(.+?)"').findall(link2)
                conta_video = len(match)
		for url in match:
                        conta_id_video = conta_id_video + 1
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',match[0],30,iconimage,'','')
                #-------------------------------
                #----------------- Not Videomega
		if numero_de_fontes > 0:
                        conta_video = 0
                        match = re.compile('<a href="(.+?)" .+? target=".+?">Clique aqui para ver!</a>').findall(link2)
                        url = match[0]
                        if url != '':
                                try:
                                        for url in match:
                                                identifica_video = re.compile('=(.*)').findall(match[conta_video])
                                                id_video = identifica_video[0]
                                                conta_video = conta_video + 1
                                                conta_id_video = conta_id_video + 1
                                                TFV_resolve_not_videomega_filmes(name,url,id_video,conta_id_video)
                                except:pass
                #-------------------------------

#----------------------------------------------------------------------------------------------------------------------------------------------#

def TFV_resolve_not_videomega_filmes(name,url,id_video,conta_id_video):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link4=response.read()
        response.close()
        match = re.compile('<iframe src="(.+?)" scrolling="no" frameborder="0" width="870px" height="500px"></iframe></center>').findall(link4)
        url=match[0]
        if "videomega" in url:
		try:
                        url = 'http://videomega.tv/iframe.php?ref=' + id_video
                        print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "vidto.me" in url:
		try:
                        url = 'http://vidto.me/' + id_video + '.html'
                        print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "dropvideo" in url:
		try:
                        url = 'http://dropvideo.com/embed/' + id_video
			print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'','')
		except:pass
	if "streamin.to" in url:
                try:
                        url = 'http://streamin.to/embed-' + id_video + '.html'
			print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,30,iconimage,'','')
                except:pass                        
        if "putlocker" in url:
                try:
                        url = 'http://www.putlocker.com/embed/' + id_video
                        print url
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Putlocker)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "nowvideo" in url:
                try:
                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video
                        print url
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	return


#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Séries  -----------------------------------------------------------------#


                                
def TFV_encontrar_fontes_series_recentes(url):
	try:
		html_source = TFV_abrir_url(url)
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
		items = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(html_source)
		for endereco,nome in items:
			addDir(nome,endereco,42,'','','')
	proxima = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
        try:
                addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
                addDir("Página Seguinte >>",proxima[0],44,artfolder + 'ze-TFV1.png','','')
        except: pass

#----------------------------------------------------------------------------------------------------------------------------------------------#
                                
def TFV_encontrar_fontes_series_A_a_Z(url):
        addDir1('[B][COLOR blue]' + name + '[/COLOR][/B]','','',artfolder + 'ze-TFV1.png',False,'')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
	try:
		html_source = TFV_abrir_url(url)
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
				addDir('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0] + ')[/COLOR][COLOR red] (' + qualidade[0] + ')[/COLOR]',urletitulo[0][0],42,thumbnail[0].replace('s72-c','s320'),'','')
			except: pass
	else:
		items = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(html_source)
		for endereco,nome in items:
			addDir(nome,endereco,42,'','','')



#----------------------------------------------------------------------------------------------------------------------------------------------#

def TFV_encontrar_videos_series(name,url):
        conta_id_video = 0
        try:
                fonte = TFV_abrir_url(url)
        except: fonte = ''
        fontes = re.findall("Epis(.+?)", fonte, re.DOTALL)
        numero_de_fontes = len(fontes)
        addDir1(name + ' ' + str(numero_de_fontes) + ' links','','',iconimage,False,'')
        addDir1('','','',iconimage,False,'')
	try:
		link_series=TFV_abrir_url(url)
	except: link_series = ''
	if link_series:
                #parameters = {"nome_texto" : name, "url": url}
                #nome_textbox = urllib.urlencode(parameters)
                #addDir('[COLOR blue]Sinopse[/COLOR]',nome_textbox,57,iconimage,'nao','')
                #trailer = re.compile('<b>Trailer</b>: <a href="(.+?)" target="_blank">').findall(link_series)
                #addDir('[COLOR blue]Trailer[/COLOR]',trailer[0],30,iconimage,'nao','')
                try:
                        items_series = re.findall("<div class=\'id(.*?)</p>", link_series, re.DOTALL)
                        for item_vid_series in items_series:
                                try:
                                        if 'videomega' in item_vid_series:
                                                try:                                      
                                                        videomega_video_nome = re.compile('>(.+?)</div></h3><p>').findall(item_vid_series)
                                                        videomega_video_url = re.compile('<iframe frameborder="0" height="400" scrolling="no" src="(.+?)"').findall(item_vid_series)
                                                        addDir('[B][COLOR green]' + videomega_video_nome[0] + '[/COLOR] - Fonte : [COLOR yellow](Videomega)[/COLOR][/B]',videomega_video_url[0],1,iconimage,'','')
                                                except:pass
                                        if 'ep' and 'src' and 'iframe' in item_vid_series:
                                                try:
                                                        not_videomega_video_url = re.compile('<iframe frameborder="0" height="400" scrolling="no" src="(.+?)"').findall(item_vid_series)
                                                        not_videomega_video_nome = re.compile('>(.+?)</div></h3><p>').findall(item_vid_series)                                                        
                                                        nome_cada_episodio = not_videomega_video_nome[0]
                                                        url = not_videomega_video_url[0]
                                                        identifica_video = re.compile('=(.*)').findall(not_videomega_video_url[0])                                                        
                                                        id_video = identifica_video[0]
                                                        src_href = 'src'
                                                        TFV_resolve_not_videomega_series(name,url,id_video,nome_cada_episodio,src_href)
                                                except:pass
                                        if 'href' and 'Clique' in item_vid_series:
                                                try:
                                                        not_videomega_video_url = re.compile('<a href="(.+?)"').findall(item_vid_series)
                                                        not_videomega_video_nome = re.compile('>(.+?)</div></h3><p>').findall(item_vid_series)
                                                        nome_cada_episodio = not_videomega_video_nome[0]
                                                        url = not_videomega_video_url[0]
                                                        identifica_video = re.compile('=(.*)').findall(not_videomega_video_url[0])                                                        
                                                        id_video = identifica_video[0]
                                                        src_href = 'href'
                                                        TFV_resolve_not_videomega_series(name,url,id_video,nome_cada_episodio,src_href)
                                                except:pass                                                                                                             
                                except:pass
                except:pass
        
#----------------------------------------------------------------------------------------------------------------------------------------------#
	
def TFV_resolve_not_videomega_series(name,url,id_video,nome_cada_episodio,src_href):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link4=response.read()
        response.close()
        if src_href == 'href':
                match = re.compile('<iframe src="(.+?)" scrolling="no" frameborder="0" width="870px" height="500px"></iframe>').findall(link4)
        if src_href == 'src':
                match = re.compile('<iframe .+? src="(.+?)" .+?></iframe>').findall(link4)
        url=match[0]        
        if "videomega" in url:
		try:
                        url = 'http://videomega.tv/iframe.php?ref=' + id_video
                        print url
			addDir('[B][COLOR green]' + nome_cada_episodio + '[/COLOR] - Fonte : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "vidto.me" in url:
		try:
                        url = 'http://vidto.me/' + id_video + '.html'
                        print url
			addDir('[B][COLOR green]' + nome_cada_episodio + '[/COLOR] - Fonte : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "dropvideo" in url:
		try:
                        url = 'http://dropvideo.com/embed/' + id_video
			print url
			addDir('[B][COLOR green]' + nome_cada_episodio + '[/COLOR] - Fonte : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'','')
		except:pass
	if "streamin.to" in url:
                try:
                        url = 'http://streamin.to/embed-' + id_video + '.html'
			print url
			addDir('[B][COLOR green]' + nome_cada_episodio + '[/COLOR] - Fonte : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,30,iconimage,'','')
                except:pass                        
        if "putlocker" in url:
                try:
                        url = 'http://www.putlocker.com/embed/' + id_video
                        print url
                        addDir('[B][COLOR green]' + nome_cada_episodio + '[/COLOR] - Fonte : [COLOR yellow](Putlocker)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "nowvideo" in url:
                try:
                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video
                        print url
                        addDir('[B][COLOR green]' + nome_cada_episodio + '[/COLOR] - Fonte : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	return
                


#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#


	
def TFV_abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

#----------------------------------------------------------------------------------------------------------------------------------------------#
              
def TFV_get_params():
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
        #cm = []
	#cm.append(('Sinopse', 'XBMC.Action(Info)'))
	#liz.addContextMenuItems(cm, replaceItems=True)
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
	
params=TFV_get_params()
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


