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

fanart = artfolder + 'flag.jpg'

_series_ = []

progress = xbmcgui.DialogProgress()

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#



def CMT_MenuPrincipal(artfolder):
        fanart = artfolder + 'flag.jpg'
        addDir1('[B][COLOR green]CINE[/COLOR][COLOR yellow]M[/COLOR][COLOR red]ATUGA[/COLOR][/B]','url',1004,'',False,fanart)
        addDir1('','url',1004,artfolder,False,fanart)
        addDir('- Pesquisar','http://www.tuga-filmes.us/search?q=',1,artfolder + 'Ze-pesquisar2.png','nao','')
        #addDir('[COLOR yellow]- Filmes/Séries Recentes[/COLOR]','http://www.tuga-filmes.us',32,'','nao','')
	addDir1('[COLOR blue]Filmes:[/COLOR]','url',1004,'',False,fanart)
	addDir('[COLOR yellow]- Todos[/COLOR]','http://www.cinematuga.net/search/label/Filmes',702,'','nao','')
	addDir('[COLOR yellow]- Animação[/COLOR]','http://www.cinematuga.net/search/label/Anima%C3%A7%C3%A3o',702,'','nao',fanart)
        addDir('[COLOR yellow]- Por Ano[/COLOR]','url',709,'','nao','')
	addDir('[COLOR yellow]- Categorias[/COLOR]','url',708,'','nao','')
	addDir('[COLOR yellow]- Top 5 da Semana[/COLOR]','url',718,'','nao','')
	if selfAddon.getSetting('hide-porno') == "false":
			addDir('[B][COLOR red]M+18[/B][/COLOR]','url',719,'','nao','')
	#addDir1('[COLOR blue]Séries:[/COLOR]','url',1004,'',False,fanart)
	#addDir('[COLOR yellow]- A a Z[/COLOR]','url',41,'','nao','')
        #addDir('[COLOR yellow]- Recentes[/COLOR]','http://www.tuga-filmes.us/search/label/Séries',44,'','nao','')

def CMT_Menu_Filmes_Top_5(artfolder):
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
        url_top_5 = 'http://www.cinematuga.net'
        top_5_source = CMT_abrir_url(url_top_5)
        if selfAddon.getSetting('movies-view') == "0":
                addDir1('[B][COLOR blue]TOP 5 da Semana[/COLOR][/B]','url',1004,'',False,'')
                addDir1('','url',1004,artfolder,False,'')
                
        html_top5 = re.findall("<div class='item-thumbnail'>(.*?)<div style='clear: both;'>", top_5_source, re.DOTALL)
	for item in html_top5:
                percent = int( ( i / 5.0 ) * 100)
                message = str(i) + " de " + '5'
                progress.update( percent, "", message, "" )
                print str(i) + " de " + '5'
                #if selfAddon.getSetting('series-thumb-TFV') == "false": xbmc.sleep( 50 )
                #xbmc.sleep( 50 )
                if progress.iscanceled():
                        break
                urletitulo = re.compile("<div class='item-title'><a href='(.+?)'>(.+?)</a></div>").findall(item)
                try:
                        html_source = CMT_abrir_url(urletitulo[0][0])
                except: html_source = ''
                items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
                thumbnail = re.compile('src="(.+?)"').findall(items[0])
                print urletitulo,thumbnail
                try:
                        if "Temporada" in urletitulo[0][1]:
                                num_mode = 712
                        else:
                                num_mode = 703
                        addDir('[B][COLOR green]' + urletitulo[0][1] + ' [/COLOR][/B]',urletitulo[0][0],num_mode,thumbnail[0].replace('s72-c','s320'),'','')
                except: pass
                i = i + 1

def CMT_Menu_Filmes_Por_Ano(artfolder):
        url_ano = 'http://www.cinematuga.net'
        html_categorias_source = CMT_abrir_url(url_ano)
	html_items_categorias = re.findall("<h2>FILMES POR ANO</h2>(.*?)<div class=\'clear\'>", html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<option value='(.+?)'>(.+?)\n[(](.+?)[)]\n</option>").findall(item_categorias)
                for endereco_categoria,nome_categoria,total_categoria in filmes_por_categoria:
                        addDir('[COLOR yellow]' + nome_categoria.replace('Filmes  ','').replace('Filmes ','') + '[/COLOR] ('+total_categoria+')',endereco_categoria,702,'','nao','')

def CMT_Menu_Filmes_Por_Categorias(artfolder):
        url_categorias = 'http://www.cinematuga.net'
        html_categorias_source = CMT_abrir_url(url_categorias)
	html_items_categorias = re.findall("<h2>CATEGORIAS</h2>(.*?)<div class=\'clear\'>", html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<option value='(.+?)'>(.+?)\n[(](.+?)[)]\n</option>").findall(item_categorias)
                for endereco_categoria,nome_categoria,total_categoria in filmes_por_categoria:
                        addDir('[COLOR yellow]' + nome_categoria + '[/COLOR] ('+total_categoria+')',endereco_categoria,702,'','nao','')

def CMT_Menu_Series_A_a_Z(artfolder):
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
        folder = addonfolder + '/resources/'
        Series_File = open(folder + 'series.txt', 'a')
        Series_Fi = open(folder + 'series.txt', 'r')
        read_Series_File = ''
        for line in Series_Fi:
                read_Series_File = read_Series_File + line
                if line!='':_series_.append(line)
        url_series = 'http://www.tuga-filmes.us'
	html_series_source = CMT_abrir_url(url_series)
	html_items_series = re.findall("<div class=\'widget Label\' id=\'Label3\'>(.*?)<div class=\'clear\'>", html_series_source, re.DOTALL)
        num_series = re.compile("<a dir=\'ltr\' href=\'(.+?)\'>(.+?)</a>").findall(html_items_series[0])
        #if selfAddon.getSetting('series-thumb-TFV') == "false":
        if selfAddon.getSetting('series-view-TFV') == "0" or selfAddon.getSetting('series-view-TFV') == "0":
                addDir1('[B][COLOR blue]Séries[/COLOR][/B] ' + '('+str(len(num_series))+')','url',1004,'',False,'')
                addDir1('','url',1004,artfolder,False,'')
        print len(html_items_series)
        num = len(num_series) + 0.0
        for item_series in html_items_series:
                series = re.compile("<a dir=\'ltr\' href=\'(.+?)\'>(.+?)</a>").findall(item_series)
                for endereco_series,nome_series in series:
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(len(num_series))
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(len(num_series))
                        #if selfAddon.getSetting('series-thumb-TFV') == "false": xbmc.sleep( 50 )
                        xbmc.sleep( 50 )
                        if progress.iscanceled():
                                break
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        nome_series = nome_series.lower()
                        nome_series = nome_series.title()
                        if nome_series in read_Series_File:
                                for x in range(len(_series_)):
                                        if nome_series in _series_[x]:
                                                thumbnail = re.compile('.+?[|](.*)').findall(_series_[x])
                                                if thumbnail : thumb = thumbnail[0]
                        else:
                        #if selfAddon.getSetting('series-thumb-TFV') == "true":
                                try:
                                        nome_pesquisa = nome_series
                                        nome_pesquisa = nome_pesquisa.replace('é','e')
                                        nome_pesquisa = nome_pesquisa.replace('ê','e')
                                        nome_pesquisa = nome_pesquisa.replace('á','a')
                                        nome_pesquisa = nome_pesquisa.replace('ã','a')
                                        nome_pesquisa = nome_pesquisa.replace('è','e')
                                        nome_pesquisa = nome_pesquisa.replace('í','i')
                                        nome_pesquisa = nome_pesquisa.replace('ó','o')
                                        nome_pesquisa = nome_pesquisa.replace('ô','o')
                                        nome_pesquisa = nome_pesquisa.replace('õ','o')
                                        nome_pesquisa = nome_pesquisa.replace('ú','u')
                                        nome_pesquisa = nome_pesquisa.replace('Ú','U')
                                        nome_pesquisa = nome_pesquisa.replace('ç','c')
                                        nome_pesquisa = nome_pesquisa.replace('&#189;','½')
                                        if '.' not in nome_pesquisa:
                                                a_q = re.compile('\w+')
                                                qq_aa = a_q.findall(nome_pesquisa)
                                                nome_pesquisa = ''
                                                for q_a_q_a in qq_aa:
                                                        if len(q_a_q_a) > 1 or q_a_q_a == '1'or q_a_q_a == '2' or q_a_q_a == '3' or q_a_q_a == '4'or q_a_q_a == '5' or q_a_q_a == '6':
                                                                nome_pesquisa = nome_pesquisa + '+' + q_a_q_a
                                        url_pesquisa = 'http://www.themoviedb.org/search/tv?query=' + nome_pesquisa
                                        try:
                                                html_pesquisa = CMT_abrir_url(endereco_series)
                                                #html_pesquisa = CMT_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_pesquisa, re.DOTALL)
                                        #items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                thumbnail = re.compile('src="(.+?)"').findall(items_pesquisa[0])
                                                #thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail:
                                                        thumb = thumbnail[0].replace('s1600','s320')
                                                        #thumb = thumbnail[0].replace('w92','w600')
                                                else:
                                                        thumb = ''
                                                                        
                                        #else: thumb = ''
                                        else: thumb = ''
                                        Series_File.write(nome_series+'|'+thumb+'\n')
                                except: pass
                        #else: thumb = ''
                        addDir('[COLOR yellow]' + nome_series + '[/COLOR] ',endereco_series+'\/series\/'+nome_series+'\/',47,thumb.replace('s72-c','s320'),'nao','')
                        #---------------------------------------------------------------
                        i = i + 1
                        #---------------------------------------------------------------
        Series_Fi.close()
        Series_File.close()
        
        

#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#


def CMT_encontrar_fontes_filmes(url,artfolder):
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
	try:
		html_source = CMT_abrir_url(url)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	conta_items = 0
	if items != []:
		print len(items)
		num = len(items) + 0.0
		for item in items:
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(len(items))
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(len(items))
                        if selfAddon.getSetting('movie-fanart-TFV') == "false": xbmc.sleep( 50 )
                        if progress.iscanceled():
                                break
                        thumb = ''
                        fanart = ''
                        versao = ''
                        audio_filme = ''
                        #if 'Portug' and 'Legendado' in item: versao = '[COLOR blue]2 VERSÕES[/COLOR]'
                        genero = re.compile("nero</b>:(.+?)<br />").findall(item)
                        if genero: genre = genero[0]
                        else: genre = ''
                        resumo = re.compile("<b>Resumo</b>:(.+?)<br />").findall(item)
                        if resumo: sinopse = resumo[0]
                        else: sinopse = ''
                        titulooriginal = re.compile("tulo Original:</b>(.+?)<br />").findall(item)
                        if titulooriginal:
                                nome_original = titulooriginal[0]
                                #addDir1(nome_original,'','','',False,'')
                        else:
                                titulooriginal = re.compile("<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>(.+?)<br />").findall(item)
                                if titulooriginal:
                                        nome_original = titulooriginal[0]
                                else: nome_original = ''
                                #addDir1(nome_original,'','','',False,'')
                        urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)
                        qualidade = re.compile("<b>Qualidade</b>: (.+?)<br />").findall(item)
                        ano = re.compile("<b>Ano</b>: (.+?)<br />").findall(item)
                        audio = re.compile("<b>.+?udio</b>(.+?)<br />").findall(item)
                        imdb_code = re.compile('<b>Mais INFO</b>: <a href="http://www.imdb.com/title/(.+?)/" target="_blank">IMDb</a>').findall(item)
                        if audio != []:
                                if 'Portug' in audio[0]:
                                        audio_filme = ': PT-PT'
                                else:
                                        audio_filme = audio[0]
                        thumbnail = re.compile('src="(.+?)"').findall(item)
                        if thumbnail: thumb = thumbnail[0]
                        else: thumb = ''
                        print urletitulo,thumb
                        nome = urletitulo[0][1]
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&#183;',"-")
                        nome = nome.replace('&amp;','&')
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
                        #fanart = artfolder + 'flag.jpg'
                        if fanart == '':
                                nome_pesquisa = nome_original
                                nome_pesquisa = nome_pesquisa.replace('é','e')
                                nome_pesquisa = nome_pesquisa.replace('ê','e')
                                nome_pesquisa = nome_pesquisa.replace('á','a')
                                nome_pesquisa = nome_pesquisa.replace('ã','a')
                                nome_pesquisa = nome_pesquisa.replace('è','e')
                                nome_pesquisa = nome_pesquisa.replace('í','i')
                                nome_pesquisa = nome_pesquisa.replace('ó','o')
                                nome_pesquisa = nome_pesquisa.replace('ô','o')
                                nome_pesquisa = nome_pesquisa.replace('õ','o')
                                nome_pesquisa = nome_pesquisa.replace('ú','u')
                                nome_pesquisa = nome_pesquisa.replace('Ú','U')
                                nome_pesquisa = nome_pesquisa.replace('ç','c')
                                nome_pesquisa = nome_pesquisa.replace('&#189;','½')
                                nome_pesquisa = nome_pesquisa.replace('.',"")
                                a_q = re.compile('\w+')
                                qq_aa = a_q.findall(nome_pesquisa)
                                nome_pesquisa = ''
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) > 1 or q_a_q_a == '1' or q_a_q_a == '2' or q_a_q_a == '3' or q_a_q_a == '4'or q_a_q_a == '5' or q_a_q_a == '6':
                                                nome_pesquisa = nome_pesquisa + '+' + q_a_q_a
                                if 'Temporada' in urletitulo[0][1]: url_pesquisa = 'http://www.themoviedb.org/search/tv?query=' + nome_pesquisa
                                else: url_pesquisa = 'http://www.themoviedb.org/search/movie?query=' + nome_pesquisa
                                if thumb == '' or 'legendas.tv' in thumb:# or 's1600' in thumb:
                                        try:
                                                html_pesquisa = CMT_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail: thumb = thumbnail[0].replace('w92','w600')
                                if selfAddon.getSetting('movie-fanart-TFV') == "true":
                                        try:
                                                html_pesquisa = CMT_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(items_pesquisa[0])
                                                if url_filme_pesquisa:
                                                        url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                        try:
                                                                html_pesquisa = CMT_abrir_url(url_pesquisa)
                                                        except: html_pesquisa = ''
                                                        url_fan = re.findall('<div id="backdrops" class="image_carousel">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                                        if url_fan:
                                                                for urls_fanart in url_fan:
                                                                        url_fanart = re.compile('src="(.+?)"').findall(urls_fanart)
                                                                        if url_fanart:
                                                                                fanart = url_fanart[0].replace('w300','w1280')
                                                                        else:
                                                                                fanart = thumb
                                        else: fanart = thumb
                        if selfAddon.getSetting('movie-fanart-TFV') == "true":
                                if fanart == '': fanart = thumb
                        if qualidade:
                                qualidade = qualidade[0]
                        else:
                                qualidade = ''
                        try:
                                if "Temporada" in urletitulo[0][1]:
                                        num_mode = 712
                                else:
                                        num_mode = 703
                                addDir_teste('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0],num_mode,thumb.replace('s72-c','s320'),sinopse,fanart,ano[0],genre)
                        except: pass
                        #---------------------------------------------------------------
                        i = i + 1
                        #---------------------------------------------------------------
	else:
		items = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(html_source)
		for endereco,nome in items:
                        try:
                                if "Temporada" in nome:
                                        num_mode = 712
                                else:
                                        num_mode = 703
                                addDir(nome,endereco,num_mode,'','','')
                        except:pass
	proxima = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
	if proxima[0] != '':
                try:
                        addDir("[B]Página Seguinte >>[/B]",proxima[0].replace('&amp;','&'),702,'','','')
                except:pass
        
        
#----------------------------------------------------------------------------------------------------------------------------------------------#	


def CMT_encontrar_videos_filmes(name,url):
        nomeescolha = name
        conta_id_video = 0
        conta_os_items = 0
	addDir1(name,'url',1004,iconimage,False,'')
        addDir1('','url',1004,artfolder,False,'')     
	try:
		link2=CMT_abrir_url(url)
	except: link2 = ''
	nao = 0
        matchvid = re.findall("Assitir online(.+?)</iframe>", link2, re.DOTALL)
        if not matchvid:
                nao = 1
                matchvid = re.findall("<div class='video-item'>(.+?)<div class='clear'>", link2, re.DOTALL)
        #addDir1(str(len(matchvid)),'url',1004,artfolder,False,'')
        for matchs in matchvid:
                try:
                        nome = re.compile('(.+?)\n.+?').findall(matchs)
                        if not nome: nome = re.compile('(.+?)</b>').findall(matchs)
                        if nao == 0: addDir1('[COLOR blue]'+nome[0]+':[/COLOR]','url',1004,artfolder,False,'')
                        urlvideo = re.compile('<iframe.+?src="(.+?)"').findall(matchs)
                        if not urlvideo: urlvideo = re.compile('src="(.+?)"').findall(matchs)
                        url = urlvideo[0]
                        conta_id_video = conta_id_video + 1
                        conta_os_items = conta_os_items + 1
                        CMT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha)
                except: pass
        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(nomeescolha)
        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
        nn = nomeescolha.replace('[B][COLOR green]','--').replace('[/COLOR][/B]','--').replace('[COLOR orange]','').replace('CMT | ','')
        n = re.compile('--(.+?)--').findall(nn)
        addDir1('','url',1004,artfolder,False,'')
        addDir('[COLOR yellow]PESQUISAR FILME: [/COLOR]'+n[0],'url',7,iconimage,'','')



#----------------------------------------------------------------------------------------------------------------------------------------------#

#def CMT_resolve_not_videomega_filmes(name,url,id_video,conta_id_video):
def CMT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha):
        url = url + '///' + nomeescolha
        if "videomega" in url:
		try:
                        fonte_id = '(Videomega)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "vidto.me" in url:
		try:
                        match = re.compile('http://vidto.me/embed-(.+?).html').findall(url)
			if match:
				id_video = match[0]
				url = 'http://vidto.me/' + id_video + '.html' + '///' + nomeescolha
			fonte_id = '(Vidto.me)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "dropvideo" in url:
		try:
                        url = url.replace('/video/','/embed/')
                        fonte_id = '(DropVideo)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'','')
		except:pass
	if "vidzi.tv" in url:
                try:
                        fonte_id = '(Vidzi.tv)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidzi.tv)[/COLOR][/B]',url,30,iconimage,'','')
                except:pass
        if "vodlocker" in url:
		try:
                        fonte_id = '(Vodlocker)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vodlocker)[/COLOR][/B]',url,30,iconimage,'','')
		except:pass
	if "played.to" in url:
                try:
                        fonte_id = '(Played.to)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Played.to)[/COLOR][/B]',url,30,iconimage,'','')
                except:pass
        if "cloudzilla" in url:
                try:
                        fonte_id = '(Cloudzilla)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Cloudzilla)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "divxstage" in url:
                try:
                        fonte_id = '(Divxstage)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Divxstage)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "vidzen" in url:
                try:
                        fonte_id = '(Vidzen)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidzen)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
	if "streamin.to" in url:
                try:
                        fonte_id = '(Streamin)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B]',url,30,iconimage,'','')
                except:pass                        
    	if "nowvideo" in url:
                try:
                        fonte_id = '(Nowvideo)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "primeshare" in url:
                try:
                        fonte_id = '(Primeshare)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Primeshare.tv)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "videoslasher" in url:
                try:
                        fonte_id = '(VideoSlasher)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoSlasher)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "sockshare" in url:
                try:
                        fonte_id = '(Sockshare)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Sockshare)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "putlocker" in url:
                try:
                        url = url.replace('putlocker.com/embed/','firedrive.com/file/')
                        fonte_id = '(Firedrive)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	else:
                if "firedrive" in url:
                        try:
                                fonte_id = '(Firedrive)'
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'','')
                        except:pass
    	if "movshare" in url:
                try:
                        fonte_id = '(Movshare)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Movshare)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
        if "video.tt" in url:
                try:
                        url = url.replace('///' + nomeescolha,'')
                        url = url.replace('/video/','/e/')
                        url = url.replace('/video/','/e/')
                        url = url.replace('http://www.video.tt/e/','http://video.tt/e/')
                        url = url.replace('http://www.video.tt/embed/','http://video.tt/e/')
                        url = url.replace('http://video.tt/e/','http://video.tt/player_control/settings.php?v=')+'&fv=v1.2.74'
                        url = url + '///' + nomeescolha
                        fonte_id = '(Video.tt)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Video.tt)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(VideoWood)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoWood)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	#_servidores_[conta_os_items] = ('[B][COLOR yellow]'+fonte_id+'[/COLOR][/B]')
        #_ligacao_[conta_os_items] = url
    	return


#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Séries  -----------------------------------------------------------------#


                                
def CMT_encontrar_fontes_series_recentes(url):
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
	try:
		html_source = CMT_abrir_url(url)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		num = len(items) + 0.0
		for item in items:
                        thumb = ''
                        fanart = ''
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(len(items))
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(len(items))
                        if selfAddon.getSetting('series-fanart-TFV') == "false": xbmc.sleep( 200 )
                        if progress.iscanceled():
                                break
			urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)
			ano = re.compile("<b>Ano</b>: (.+?)<br />").findall(item)
			if ano: ano = '('+ano[0]+')'
			qualidade = re.compile("<b>Qualidade</b>: (.+?)<br />").findall(item)
			if qualidade: qualidade = '('+qualidade[0]+')'
			thumbnail = re.compile('src="(.+?)"').findall(item)
			if thumbnail: thumb = thumbnail[0]
                        else: thumb = ''
			print urletitulo,thumbnail
			nome = urletitulo[0][1]
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&amp;','&')
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        tirar_ano = '(' + str(q_a_q_a) + ')'
                                        nome = nome.replace(tirar_ano,'')
                        n = re.compile('(.+?)[(].+?[)]').findall(nome)
                        if n: nome_original = n[0]
                        else: nome_original = nome
                        if fanart == '':
                                nome_pesquisa = nome_original
                                #addDir1(nome_pesquisa,'','','',False,'')
                                nome_pesquisa = nome_pesquisa.replace('é','e')
                                nome_pesquisa = nome_pesquisa.replace('ê','e')
                                nome_pesquisa = nome_pesquisa.replace('á','a')
                                nome_pesquisa = nome_pesquisa.replace('ã','a')
                                nome_pesquisa = nome_pesquisa.replace('è','e')
                                nome_pesquisa = nome_pesquisa.replace('í','i')
                                nome_pesquisa = nome_pesquisa.replace('ó','o')
                                nome_pesquisa = nome_pesquisa.replace('ô','o')
                                nome_pesquisa = nome_pesquisa.replace('õ','o')
                                nome_pesquisa = nome_pesquisa.replace('ú','u')
                                nome_pesquisa = nome_pesquisa.replace('Ú','U')
                                nome_pesquisa = nome_pesquisa.replace('ç','c')
                                nome_pesquisa = nome_pesquisa.replace('&#189;','½')
                                nome_pesquisa = nome_pesquisa.replace('Agents Of S.H.I.E.L.D',"Agents Of S.H.I.E.L.D.")
                                nome_pesquisa = nome_pesquisa.replace('.',"")
                                a_q = re.compile('\w+')
                                qq_aa = a_q.findall(nome_pesquisa)
                                nome_pesquisa = ''
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) > 1 or q_a_q_a == '1' or q_a_q_a == '2' or q_a_q_a == '3' or q_a_q_a == '4'or q_a_q_a == '5' or q_a_q_a == '6':
                                                nome_pesquisa = nome_pesquisa + '+' + q_a_q_a
                                url_pesquisa = 'http://www.themoviedb.org/search/tv?query=' + nome_pesquisa
                                if thumb == '' or 's1600' in thumb:
                                        try:
                                                html_pesquisa = CMT_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail: thumb = thumbnail[0].replace('w92','w600')
                                if selfAddon.getSetting('series-fanart-TFV') == "true":
                                        try:
                                                html_pesquisa = CMT_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(items_pesquisa[0])
                                                if url_filme_pesquisa:
                                                        url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                        try:
                                                                html_pesquisa = CMT_abrir_url(url_pesquisa)
                                                        except: html_pesquisa = ''
                                                        url_fan = re.findall('<div id="backdrops" class="image_carousel">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                                        if url_fan:
                                                                for urls_fanart in url_fan:
                                                                        url_fanart = re.compile('src="(.+?)"').findall(urls_fanart)
                                                                        if url_fanart:
                                                                                fanart = url_fanart[0].replace('w300','w1280')
                                                                        else:
                                                                                fanart = thumb
                                        else: fanart = thumb
                        if selfAddon.getSetting('series-fanart-TFV') == "true":
                                if fanart == '': fanart = thumb
			try:
				addDir_teste('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano + '[/COLOR][COLOR red] ' + qualidade + '[/COLOR]',urletitulo[0][0],42,thumb.replace('s72-c','s320'),'',fanart,ano,'')
			except: pass
			i = i + 1
	else:
		items = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(html_source)
		for endereco,nome in items:
			addDir(nome,endereco,42,'','','')
	proxima = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
        try:
                if selfAddon.getSetting('movies-view') == "0": addDir1('','url',1004,artfolder,False,'')
                addDir("Página Seguinte >>",proxima[0],44,'','','')
        except: pass

#----------------------------------------------------------------------------------------------------------------------------------------------#

def CMT_encontrar_fontes_series_A_a_Z(url):
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
        url = url.replace('\/','|')
        nome_orig = re.compile('[|].+?[|](.+?)[|]').findall(url)
        nome_original = nome_orig[0]
        if selfAddon.getSetting('movies-view') == "0":
                addDir1('[B][COLOR blue]' + name + '[/COLOR][/B]','url',1004,'',False,'')
                addDir1('','url',1004,artfolder,False,'')
        if '|series|' in url:
                series = 1
                u = re.compile('(.+?)[|].+?[|].+?[|]').findall(url)
                url = u[0]
        else: series = 0
	try:
		html_source = CMT_abrir_url(url)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		num = len(items) + 0.0
		for item in items:
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(len(items))
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(len(items))
                        if selfAddon.getSetting('series-fanart-TFV') == "false": xbmc.sleep( 200 )
                        if progress.iscanceled():
                                break
                        thumb = ''
                        fanart = ''
			urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)
			ano = re.compile("<b>Ano</b>: (.+?)<br />").findall(item)
			if ano: ano = '('+ano[0]+')'
			qualidade = re.compile("<b>Qualidade</b>: (.+?)<br />").findall(item)
			if qualidade: qualidade = '('+qualidade[0]+')'
			thumbnail = re.compile('src="(.+?)"').findall(item)
			if thumbnail: thumb = thumbnail[0]
                        else: thumb = ''
			print urletitulo,thumbnail
			nome = urletitulo[0][1]
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&amp;','&')
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
                        if fanart == '':
                                nome_pesquisa = nome_original
                                nome_pesquisa = nome_pesquisa.replace('é','e')
                                nome_pesquisa = nome_pesquisa.replace('ê','e')
                                nome_pesquisa = nome_pesquisa.replace('á','a')
                                nome_pesquisa = nome_pesquisa.replace('ã','a')
                                nome_pesquisa = nome_pesquisa.replace('è','e')
                                nome_pesquisa = nome_pesquisa.replace('í','i')
                                nome_pesquisa = nome_pesquisa.replace('ó','o')
                                nome_pesquisa = nome_pesquisa.replace('ô','o')
                                nome_pesquisa = nome_pesquisa.replace('õ','o')
                                nome_pesquisa = nome_pesquisa.replace('ú','u')
                                nome_pesquisa = nome_pesquisa.replace('Ú','U')
                                nome_pesquisa = nome_pesquisa.replace('ç','c')
                                nome_pesquisa = nome_pesquisa.replace('&#189;','½')
                                nome_pesquisa = nome_pesquisa.replace('Agents Of S.H.I.E.L.D',"Agents Of S.H.I.E.L.D.")
                                nome_pesquisa = nome_pesquisa.replace('.',"")
                                a_q = re.compile('\w+')
                                qq_aa = a_q.findall(nome_pesquisa)
                                nome_pesquisa = ''
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) > 1 or q_a_q_a == '1' or q_a_q_a == '2' or q_a_q_a == '3' or q_a_q_a == '4'or q_a_q_a == '5' or q_a_q_a == '6':
                                                nome_pesquisa = nome_pesquisa + '+' + q_a_q_a
                                url_pesquisa = 'http://www.themoviedb.org/search/tv?query=' + nome_pesquisa
                                if thumb == '' or 's1600' in thumb:
                                        try:
                                                html_pesquisa = CMT_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail: thumb = thumbnail[0].replace('w92','w600')
                                if selfAddon.getSetting('series-fanart-TFV') == "true":
                                        try:
                                                html_pesquisa = CMT_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(items_pesquisa[0])
                                                if url_filme_pesquisa:
                                                        url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                        try:
                                                                html_pesquisa = CMT_abrir_url(url_pesquisa)
                                                        except: html_pesquisa = ''
                                                        url_fan = re.findall('<div id="backdrops" class="image_carousel">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                                        if url_fan:
                                                                for urls_fanart in url_fan:
                                                                        url_fanart = re.compile('src="(.+?)"').findall(urls_fanart)
                                                                        if url_fanart:
                                                                                fanart = url_fanart[0].replace('w300','w1280')
                                                                        else:
                                                                                fanart = thumb
                                        else: fanart = thumb
                        if selfAddon.getSetting('series-fanart-TFV') == "true":
                                if fanart == '': fanart = thumb
                        if series == 1:
                                n = re.compile('[(](.+?)[)]').findall(nome)
                                qualidade = ''
                                ano = ''
                                if n: nome = n[0]
			try:
				addDir_teste('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano + '[/COLOR][COLOR red] ' + qualidade + '[/COLOR]',urletitulo[0][0],42,thumb.replace('s72-c','s320'),'',fanart,ano,'')
			except: pass
			i = i + 1
	else:
		items = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(html_source)
		for endereco,nome in items:
			addDir(nome,endereco,42,'','','')

#----------------------------------------------------------------------------------------------------------------------------------------------#

def CMT_encontrar_videos_series(name,url):
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
        conta_id_video = 0
	try:
		link_series=CMT_abrir_url(url)
	except: link_series = ''
	fontes = re.findall("Epis(.+?)", link_series, re.DOTALL)
        numero_de_fontes = len(fontes)
        if 'http://js.tuga-filmes.tv/counter/counter.html' in link_series: numero_de_fontes = numero_de_fontes - 1
        addDir1(name + ' ' + str(numero_de_fontes) + ' links','url',1004,iconimage,False,'')
        addDir1('','url',1004,artfolder,False,'')
	if link_series:
                try:
                        items_series = re.findall("<div class=\'id(.*?)</p>", link_series, re.DOTALL)
                        divide = numero_de_fontes + 0.0
                        for item_vid_series in items_series:
                                try:
                                        percent = int( ( i / divide ) * 100)
                                        message = str(i) + " de " + str(numero_de_fontes) + ' Links'
                                        progress.update( percent, "", message, "" )
                                        print str(i) + " de " + str(numero_de_fontes) + ' Links'
                                        xbmc.sleep( 50 )
                                        if progress.iscanceled():
                                                break
                                        if 'videomega' in item_vid_series:
                                                try:                                      
                                                        videomega_video_nome = re.compile('>(.+?)</div></h3><p>').findall(item_vid_series)
                                                        videomega_video_url = re.compile('<iframe .+? src="(.+?)"').findall(item_vid_series)
                                                        nome = videomega_video_nome[0]
                                                        nome = nome.replace('&#8217;',"'")
                                                        nome = nome.replace('&#8211;',"-")
                                                        nome = nome.replace('&#39;',"'")
                                                        nome = nome.replace('&amp;','&')
                                                        addDir('[B][COLOR green]' + nome + '[/COLOR] - Fonte : [COLOR yellow](Videomega)[/COLOR][/B]',videomega_video_url[0],30,iconimage,'','')
                                                except:pass
                                        if 'ep' and 'src' and 'iframe' in item_vid_series:
                                                try:
                                                        not_videomega_video_url = re.compile('<iframe .+? src="(.+?)"').findall(item_vid_series)
                                                        not_videomega_video_nome = re.compile('>(.+?)</div></h3><p>').findall(item_vid_series)                                                        
                                                        nome_cada_episodio = not_videomega_video_nome[0]
                                                        url = not_videomega_video_url[0]
                                                        identifica_video = re.compile('=(.*)').findall(not_videomega_video_url[0])                                                        
                                                        id_video = identifica_video[0]
                                                        src_href = 'src'
                                                        nome_cada_episodio = nome_cada_episodio.replace('&#8217;',"'")
                                                        nome_cada_episodio = nome_cada_episodio.replace('&#8211;',"-")
                                                        nome_cada_episodio = nome_cada_episodio.replace('&#39;',"'")
                                                        nome_cada_episodio = nome_cada_episodio.replace('&amp;','&')
                                                        CMT_resolve_not_videomega_series(name,url,id_video,nome_cada_episodio,src_href)
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
                                                        nome_cada_episodio = nome_cada_episodio.replace('&#8217;',"'")
                                                        nome_cada_episodio = nome_cada_episodio.replace('&#8211;',"-")
                                                        nome_cada_episodio = nome_cada_episodio.replace('&#39;',"'")
                                                        nome_cada_episodio = nome_cada_episodio.replace('&amp;','&')
                                                        CMT_resolve_not_videomega_series(name,url,id_video,nome_cada_episodio,src_href)
                                                except:pass
                                        i = i + 1
                                except:pass
                except:pass
        
#----------------------------------------------------------------------------------------------------------------------------------------------#
	
def CMT_resolve_not_videomega_series(name,url,id_video,nome_cada_episodio,src_href):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link4=response.read()
        response.close()
        if src_href == 'href':
                match = re.compile('<iframe src="(.+?)".+?></iframe>').findall(link4)
        if src_href == 'src':
                match = re.compile('<iframe .+? src="(.+?)" .+?></iframe>').findall(link4)
        url=match[0]        
        if "videomega" in url:
		try:
                        url = 'http://videomega.tv/iframe.php?ref=' + id_video + '///' + name
                        print url
			addDir('[B][COLOR green]' + nome_cada_episodio + '[/COLOR] - Fonte : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "vidto.me" in url:
		try:
                        url = 'http://vidto.me/' + id_video + '.html' + '///' + name
                        print url
			addDir('[B][COLOR green]' + nome_cada_episodio + '[/COLOR] - Fonte : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "dropvideo" in url:
		try:
                        url = 'http://dropvideo.com/embed/' + id_video + '///' + name
			print url
			addDir('[B][COLOR green]' + nome_cada_episodio + '[/COLOR] - Fonte : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'','')
		except:pass
	if "streamin.to" in url:
                try:
                        url = 'http://streamin.to/embed-' + id_video + '.html' + '///' + name
			print url
			addDir('[B][COLOR green]' + nome_cada_episodio + '[/COLOR] - Fonte : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,30,iconimage,'','')
                except:pass                        
        if "putlocker" in url:
                try:
                        url = 'http://www.putlocker.com/embed/' + id_video + '///' + name
                        print url
                        addDir('[B][COLOR green]' + nome_cada_episodio + '[/COLOR] - Fonte : [COLOR yellow](Putlocker)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "nowvideo" in url:
                try:
                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video + '///' + name
                        print url
                        addDir('[B][COLOR green]' + nome_cada_episodio + '[/COLOR] - Fonte : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        url = 'http://www.videowood.tv/embed/' + id_video + '///' + name
                        print url
                        addDir('[B][COLOR green]' + nome_cada_episodio + '[/COLOR] - Fonte : [COLOR yellow](VideoWood)[/COLOR][/B]',url,70,iconimage,'','')
    		except:pass
    	return
                


#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#


	
def CMT_abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

#----------------------------------------------------------------------------------------------------------------------------------------------#
              
def CMT_get_params():
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
        if fanart == '': fanart = artfolder + 'flag.jpg'
        #text = checker
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&checker="+urllib.quote_plus(checker)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',fanart)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
        #cm = []
	#cm.append(('Sinopse', 'XBMC.Action(Info)'))
	#liz.addContextMenuItems(cm, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir1(name,url,mode,iconimage,folder,fanart):
        if fanart == '': fanart = artfolder + 'flag.jpg'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',fanart)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
        return ok

def addDir_vazio(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	#liz.setProperty('fanart_image',fanart)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addDir_teste(name,url,mode,iconimage,plot,fanart,year,genre):
        if fanart == '': fanart = artfolder + 'flag.jpg'
        #text = checker
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&plot="+urllib.quote_plus(plot)+"&year="+urllib.quote_plus(year)+"&genre="+urllib.quote_plus(genre)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',fanart)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Year": year, "Genre": genre } )
        #cm = []
	#cm.append(('Sinopse', 'XBMC.Action(Info)'))
	#liz.addContextMenuItems(cm, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


#----------------------------------------------------------------------------------------------------------------------------------------------#
	
params=CMT_get_params()
url=None
name=None
mode=None
checker=None
iconimage=None
fanart=None
year=None
plot=None
genre=None

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
try:        
        plot=urllib.unquote_plus(params["plot"])
except:
        pass
try:        
        year=urllib.unquote_plus(params["year"])
except:
        pass
try:        
        genre=urllib.unquote_plus(params["genre"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Checker: "+str(checker)
print "Iconimage: "+str(iconimage)
print "Plot: "+str(plot)
print "Year: "+str(year)
print "Genre: "+str(genre)


