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
from array import array
from string import capwords


arrai_nome_series = ['' for i in range(50)]
arrai_endereco_series = ['' for i in range(50)]
arrai_series = [['' for j in range(2)] for i in range(200)]
arr_series = []

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

mensagemprogresso = xbmcgui.DialogProgress()
progress = xbmcgui.DialogProgress()

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#



def TPT_MenuPrincipal(artfolder):
        url_toppt = 'http://toppt.net/'
        toppt_source = TPT_abrir_url(url_toppt)
        saber_url_todos = re.compile('<a href="(.+?)">filmes</a></li>').findall(toppt_source)
        saber_url_M18 = re.compile('<option class="level-0" value="(.+?)">m18</option>').findall(toppt_source)
        saber_url_animacao = re.compile('<a href="(.+?)">Animacao</a></li>').findall(toppt_source)
        saber_url_series = re.compile('<a href="(.+?)">Series</a></li>').findall(toppt_source)
        if not saber_url_series: saber_url_series = re.compile('<a href="(.+?)">SERIES</a></li>').findall(toppt_source)
        addDir1('[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]','','',artfolder + 'ze-TPT1.png',False,'')
        addDir1('','','',artfolder + 'ze-TPT1.png',False,'')
        addDir('- Pesquisar','url',1,artfolder + 'Ze-pesquisar2.png','nao','')
	addDir1('[COLOR blue]Filmes:[/COLOR]','','',artfolder + 'ze-TPT1.png',False,'')
	addDir('[COLOR yellow]- Todos[/COLOR]',saber_url_todos[0],232,artfolder + 'ze-TPT1.png','nao','')
        addDir('[COLOR yellow]- Por Ano[/COLOR]','url',239,artfolder + 'ze-TPT1.png','nao','')
	addDir('[COLOR yellow]- Categorias[/COLOR]','url',238,artfolder + 'ze-TPT1.png','nao','')
	addDir('[COLOR yellow]- Animação[/COLOR]',saber_url_animacao[0],232,artfolder + 'ze-TPT1.png','nao','')
	if selfAddon.getSetting('hide-porno') == "false":
			addDir('[B][COLOR red]M+18[/B][/COLOR]','http://toppt.net/?cat=' + saber_url_M18[0],232,artfolder + 'ze-TPT1.png','nao','')		
	addDir1('[COLOR blue]Séries:[/COLOR]','','',artfolder + 'ze-TPT1.png',False,'')
	addDir('[COLOR yellow]- A a Z[/COLOR]','url',241,artfolder + 'ze-TPT1.png','nao','')
        addDir('[COLOR yellow]- Recentes[/COLOR]',saber_url_series[0],232,artfolder + 'ze-TPT1.png','nao','')

def TPT_Menu_Posts_Recentes(artfolder):
        url_recentes = 'http://toppt.net/'
        recentes_source = TPT_abrir_url(url_recentes)
        if selfAddon.getSetting('movies-view') == "0":
                addDir1('[B][COLOR blue]Recentes[/COLOR][/B]','','',artfolder + 'ze-TPT1.png',False,'')
                addDir1('','','',artfolder + 'ze-TPT1.png',False,'')
        posts_recentes = re.compile('<a href="(.+?)">.+?</a>\n</li>\n<li>\n').findall(recentes_source)
        for endereco_recentes in posts_recentes:                
                try:
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('(PT-PT)',"")
                        nome = nome.replace('(PT/PT)',"")
                        nome = nome.replace('[PT-PT]',"")
                        nome = nome.replace('[PT/PT]',"")
                        addDir('[B][COLOR green]' + nome + '[/COLOR][/B]',endereco_recentes,233,'','','')
                except: pass

def TPT_Menu_Filmes_Por_Ano(artfolder):
        url_ano = 'http://toppt.net/'
        ano_source = TPT_abrir_url(url_ano)
        filmes_por_ano = re.compile('<option class="level-0" value="(.+?)">(.+?)</option>').findall(ano_source)
	for num_cat,nome_ano in filmes_por_ano:
                endereco_ano = 'http://toppt.net/?cat=' + str(num_cat)
		addDir('[COLOR yellow]' + nome_ano + '[/COLOR] ',endereco_ano,232,artfolder + 'ze-TPT1.png','nao','')
		if str(nome_ano) == '2014': break

def TPT_Menu_Filmes_Por_Categorias(artfolder):
        url_categorias = 'http://toppt.net/'
        html_categorias_source = TPT_abrir_url(url_categorias)
	html_items_categorias = re.findall('<h3 class="widgettitle">FILMES</h3>(.*?)<h3 class="widgettitle">MUSICAS</h3>', html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile('<a href="(.+?)">(.+?)</a>').findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        if nome_categoria != '2011' and nome_categoria != '2012' and nome_categoria != '2013' and nome_categoria != '2014':
                                addDir('[COLOR yellow]' + nome_categoria + '[/COLOR] ',endereco_categoria,232,artfolder + 'ze-TPT1.png','nao','')

def TPT_Menu_Series_A_a_Z(artfolder):
        i = 1
        conta = 0
        conta_items = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
        url_series = 'http://toppt.net/'
	html_series_source = TPT_abrir_url(url_series)
	html_items_series = re.findall('<h3 class="widgettitle">SERIES</h3>(.*?)<div id="footer-widgets" class="clearfix">', html_series_source, re.DOTALL)	
        print len(html_items_series)
        for item_series in html_items_series:
                series = re.compile('<a href="(.+?)">(.+?)</a>').findall(item_series)
                num = len(series) + 0.0
                for endereco_series,nome_series in series:
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(len(series))
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(len(series))
                        if selfAddon.getSetting('series-thumb-TPT') == "false": xbmc.sleep( 50 )
                        if progress.iscanceled():
                                break
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        nome_series = nome_series.replace('&#8217;',"'")
                        nome_series = nome_series.replace('&#8230;',"...")
                        nome_series = nome_series.lower()
                        nome_series = nome_series.title()
                        if selfAddon.getSetting('series-thumb-TPT') == "true":
                                try:
                                        nome_pesquisa = arr_series[x][0]
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
                                        try:
                                                html_pesquisa = TPT_abrir_url(arr_series[x][1])
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                thumbnail = re.compile('src="(.+?)"').findall(items_pesquisa[0])
                                                if thumbnail:
                                                        thumb = thumbnail[0].replace('w92','w600')
                                                else:
                                                        thumb = ''
                                                                        
                                        else: thumb = ''
                                except: pass
                        else: thumb = artfolder + 'ze-TPT1.png'
                        arr_series.append((nome_series,endereco_series,thumb))
                        i = i + 1
        if selfAddon.getSetting('series-thumb-TPT') == "false":
                addDir1('[B][COLOR blue]Séries[/COLOR][/B] (' + str(len(series)) + ')','','',artfolder + 'ze-TPT1.png',False,'')
                addDir1('','','',artfolder + 'ze-TPT1.png',False,'')
        arr_series.sort()
        for x in range(len(arr_series)):
                addDir('[COLOR yellow]' + arr_series[x][0] + '[/COLOR]',arr_series[x][1]+'-series-',232,arr_series[x][2],'nao','')



#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#

		

def TPT_encontrar_fontes_filmes(url,artfolder):
        if '-series-' in url:
                series = 1
                url = url.replace('-series-','')
        else: series = 0
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
        i = 1
        if 'Seguinte' not in name:
                if selfAddon.getSetting('movies-view') == "0":
                        addDir1(name + ':','','',iconimage,False,'')
                        addDir1('','','',iconimage,False,'')
	try:
		html_source = TPT_abrir_url(url)
	except: html_source = ''
	items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        fanart = ''
                        thumb = ''
                        num = len(items) + 0.0
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(len(items))
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(len(items))
                        #xbmc.sleep( 500 )
                        if progress.iscanceled():
                                break
                        audio_filme = ''
                        urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(item)
                        if 'title=' in urletitulo[0][0]: urletitulo = re.compile('<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>').findall(item)
                        qualidade = re.compile("<b>QUALIDADE:.+?/b>(.+?)<br/>").findall(item)
                        if not qualidade: qualidade = re.compile("<b>VERSÃO:.+?</b>(.+?)<br/>").findall(item)
                        ano = re.compile("<b>ANO:.+?/b>(.+?)<br/>").findall(item)
                        audio = re.compile("<b>AUDIO:.+?/b>(.+?)<br/>").findall(item)
                        thumbnail = re.compile('src="(.+?)"').findall(item)
                        if thumbnail: thumb = thumbnail[0].replace('s72-c','s320')
                        print urletitulo,thumbnail
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
                        if fanart == '':
                                nome_pesquisa = nome
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
                                a_q = re.compile('\w+')
                                qq_aa = a_q.findall(nome_pesquisa)
                                nome_pesquisa = ''
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) > 1 or q_a_q_a == '1' or q_a_q_a == '2' or q_a_q_a == '3' or q_a_q_a == '4'or q_a_q_a == '5' or q_a_q_a == '6':
                                                nome_pesquisa = nome_pesquisa + '+' + q_a_q_a
                                if 'Temporada' in urletitulo[0][1]: url_pesquisa = 'http://www.themoviedb.org/search/tv?query=' + nome_pesquisa
                                else: url_pesquisa = 'http://www.themoviedb.org/search/movie?query=' + nome_pesquisa
                                try:
                                        html_pesquisa = TPT_abrir_url(url_pesquisa)
                                except: html_pesquisa = ''
                                items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                if items_pesquisa != []:
                                        if thumb == '':
                                                thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail: thumb = thumbnail[0].replace('w92','w600')
                                        url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(items_pesquisa[0])
                                        if url_filme_pesquisa:
                                                url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                try:
                                                        html_pesquisa = TPT_abrir_url(url_pesquisa)
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
                        if fanart == '': fanart = thumb
                        ano_filme = '('+ano_filme+')'
                        qualidade = '('+qualidade
                        audio_filme = audio_filme+')'
                        if series == 1:
                                n = re.compile('[(](.+?)[)]').findall(nome)
                                if n: nome = n[0]
                                else:
                                        n = re.compile('[[](.+?)[]]').findall(nome)
                                        if n: nome = n[0]
                                qualidade = ''
                                ano_filme = ''
                                audio_filme = ''
                                
                        try:
                                addDir_teste('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0],233,thumb,'',fanart,ano_filme,'')
                        except: pass
                        i = i + 1
	else:
		items = re.compile('<h1 class="entry-title"><a href="(.+?)" .+?>(.+?)</a>').findall(html_source)
		for endereco,nome in items:
                        try:
                                addDir(nome,endereco,233,'','','')
                        except:pass
	proxima = re.compile('</span><a class="nextpostslink" href="(.+?)">&raquo;</a><a class="last"').findall(html_source)
	try:
		addDir("Página Seguinte >>",proxima[0].replace('#038;','').replace('&amp;','&'),232,artfolder + 'ze-TPT1.png','','')
        except:pass
        progress.close()


#----------------------------------------------------------------------------------------------------------------------------------------------#
                

def TPT_encontrar_videos_filmes(name,url):
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
        conta_id_video = 0
        contaultimo = 0
        addDir1(name,'','',iconimage,False,'')
        addDir1('','','',iconimage,False,'')
	try:
		link2=TPT_abrir_url(url)
	except: link2 = ''
	if link2:
                newmatch = re.findall('<span id=.+?DOWNLOAD',link2,re.DOTALL)
                if not newmatch: newmatch = re.findall('<span id=.+?<nav class="navigation post-navigation"',link2,re.DOTALL)
                if newmatch:
			linksseccao = re.findall('<p>PARTE (\d+)<br.+?\n(.+?)</p>',newmatch[0],re.DOTALL)
			if linksseccao:
                                if len(linksseccao) > 1:
                                        linksseccao = re.findall('<p>PARTE (\d+)<br.+?\n(.+?)<p>&nbsp;</p>',newmatch[0],re.DOTALL)
                                        for parte1,parte2 in linksseccao:
                                                conta_id_video = 0
                                                addDir1('[COLOR blue] Parte '+parte1+'[/COLOR]','','',iconimage,False,'')					
                                                match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                                match = re.compile('"window.open(.+?)"').findall(parte2)
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                if len(linksseccao) == 1:
                                        linksseccao = re.findall('<p>PARTE (\d+)<br.+?\n(.+?)<p>&nbsp;</p>',newmatch[0],re.DOTALL)
                                        for parte1,parte2 in linksseccao:
                                                conta_id_video = 0
                                                addDir1('[COLOR blue] Parte '+parte1+'[/COLOR]','','',iconimage,False,'')					
                                                match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                                match = re.compile('"window.open(.+?)"').findall(parte2)
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                        linksseccao = re.findall('<p>PARTE(\d+)</p>\n(.+?)<p>&nbsp;</p>',newmatch[0],re.DOTALL)
                                        for parte1,parte2 in linksseccao:
                                                conta_id_video = 0
                                                addDir1('[COLOR blue] Parte '+parte1+'[/COLOR]','','',iconimage,False,'')					
                                                match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                                match = re.compile('"window.open(.+?)"').findall(parte2)
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video)
			else:
                                linksseccao = re.findall('<span style="color:.+?">(.+?)</span><br.+?>(.+?)Ver Aqui</a></p>',newmatch[0],re.DOTALL)
				if linksseccao:			
					for parte1,parte2 in linksseccao:
                                                parte1=parte1.replace('[','(').replace(']',')').replace('<strong>','').replace('</strong>','')
                                                conta_id_video = 0
						addDir1('[COLOR blue]'+parte1+'[/COLOR]','','',iconimage,False,'')					
						match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
						for url in match:
                                                        conta_id_video = conta_id_video + 1
							TPT_resolve_not_videomega_filmes(url,conta_id_video)
						match = re.compile('<a href="(.+?)" target="_blank">').findall(parte2)
						if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
						for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video)
						match = re.compile('"window.open(.+?)"').findall(parte2)
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video)
				else:
					linksseccao = re.findall('<span style="color:.+?"><strong>(.+?)</strong></span><br.+?>(.+?)Ver Aqui</a></p>',newmatch[0],re.DOTALL)
                                        if linksseccao:			
                                                for parte1,parte2 in linksseccao:
                                                        parte1=parte1.replace('[','(').replace(']',')').replace('<strong>','').replace('</strong>','')
                                                        conta_id_video = 0
                                                        addDir1('[COLOR blue]'+parte1+'[/COLOR]','','',iconimage,False,'')					
                                                        match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                        if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                        for url in match:
                                                                conta_id_video = conta_id_video + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                                        match = re.compile('<a href="(.+?)" target="_blank">').findall(parte2)
                                                        if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                        for url in match:
                                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                        conta_id_video = conta_id_video + 1
                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                                        match = re.compile('"window.open(.+?)"').findall(parte2)
                                                        for url in match:
                                                                conta_id_video = conta_id_video + 1
                                                                url = url.replace("'","").replace("(","").replace(")","")
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                        else:
                                                lin = re.findall('.+?EPIS',newmatch[0],re.DOTALL)
                                                linksseccao = re.findall('ODIO (.+?)<br.+?>\n(.+?)EPIS',newmatch[0],re.DOTALL)
                                                linksseccaoultimo = re.findall('ODIO (.+?)<br.+?>\n(.+?)</p>',newmatch[0],re.DOTALL)
                                                num = len(lin) + 0.0
                                                if linksseccao:
                                                        ultima_parte = ''
                                                        for parte1,parte2 in linksseccao:
                                                                percent = int( ( i / num ) * 100)
                                                                message = str(i) + " de " + str(len(lin))
                                                                progress.update( percent, "", message, "" )
                                                                print str(i) + " de " + str(len(lin))
                                                                xbmc.sleep( 500 )
                                                                if progress.iscanceled():
                                                                        break
                                                                conta_id_video = 0
                                                                if parte1 != ultima_parte: addDir1('[COLOR blue] Episódio '+parte1+'[/COLOR]','','',iconimage,False,'')
                                                                ultepi = int(parte1)
                                                                match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                                for url in match:
                                                                        conta_id_video = conta_id_video + 1
                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                                for url in match:
                                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                conta_id_video = conta_id_video + 1
                                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                                                match = re.compile('"window.open(.+?)"').findall(parte2)
                                                                for url in match:
                                                                        conta_id_video = conta_id_video + 1
                                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                                                i = i + 1
                                                        conta_id_video = 0
                                                        nmatch = re.findall(url+'.+?DOWNLOAD',link2,re.DOTALL)
                                                        if not nmatch: nmatch = re.findall(url+'.+?<nav class="navigation post-navigation"',link2,re.DOTALL)
                                                        linksseccao = re.findall('ODIO (.+?)</p>\n<p><b>(.+?)EPIS',nmatch[0],re.DOTALL)
                                                        if linksseccao:
                                                                for parte1,parte2 in linksseccao:
                                                                        addDir1('[COLOR blue] Episódio '+parte1+'[/COLOR]','','',iconimage,False,'')
                                                                        match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                                        if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                                        for url in match:
                                                                                conta_id_video = conta_id_video + 1
                                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                                        if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                                        for url in match:
                                                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                                                        match = re.compile('"window.open(.+?)"').findall(parte2)
                                                                        for url in match:
                                                                                conta_id_video = conta_id_video + 1
                                                                                url = url.replace("'","").replace("(","").replace(")","")
                                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                                        conta_id_video = 0
                                                        v_id = re.compile('=(.*)').findall(url)
                                                        if not v_id: v_id = re.compile('//(.*)').findall(url)
                                                        contamatch = re.findall('ODIO (.+?)</p>\n<p><b>',newmatch[0],re.DOTALL)
                                                        linksseccao = re.findall(v_id[0]+'(.+?)<img',newmatch[0],re.DOTALL)
                                                        if linksseccao:
                                                                match = re.compile('ODIO (.+?)<br').findall(linksseccao[0])
                                                                if not match: match = re.compile('ODIO (.+?)</p>').findall(linksseccao[0])
                                                                if match: addDir1('[COLOR blue] Episódio '+match[0]+'[/COLOR]','','',iconimage,False,'')
                                                                match = re.compile('<iframe.+?src="(.+?)"').findall(linksseccao[0])
                                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(linksseccao[0])	
                                                                for url in match:
                                                                        conta_id_video = conta_id_video + 1
                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(linksseccao[0])
                                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(linksseccao[0])
                                                                for url in match:
                                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                conta_id_video = conta_id_video + 1
                                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                                                match = re.compile('"window.open(.+?)"').findall(linksseccao[0])
                                                                for url in match:
                                                                        conta_id_video = conta_id_video + 1
                                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                                        ####################################################################
                                                else:
                                                        match = re.compile('<iframe.+?src="(.+?)"').findall(newmatch[0])
                                                        if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(newmatch[0])
                                                        for url in match:
                                                                conta_id_video = conta_id_video + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(newmatch[0])
                                                        if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(newmatch[0])
                                                        for url in match:
                                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                        conta_id_video = conta_id_video + 1
                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                                        match = re.compile('"window.open(.+?)"').findall(newmatch[0])
                                                        for url in match:
                                                                conta_id_video = conta_id_video + 1
                                                                url = url.replace("'","").replace("(","").replace(")","")
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video)
		else:
			newmatch = re.findall('EM PT/PT:.+?<nav class="navigation post-navigation"',link2,re.DOTALL)
			if newmatch:
				linksseccao = re.findall('<p>PARTE (\d+)<br.+?\n(.+?)</p>',newmatch[0],re.DOTALL)
				if linksseccao:
					for parte1,parte2 in linksseccao:
                                                conta_id_video = 0
						addDir1('[COLOR bue] Parte '+parte1+'[/COLOR]',urlfinal,'',iconimage,False,'')					
						match = re.compile('<iframe src="(.+?)"').findall(parte2)	
						for url in match:
                                                        conta_id_video = conta_id_video + 1
							TPT_resolve_not_videomega_filmes(url,conta_id_video)
						match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
						if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
						for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video)
						match = re.compile('"window.open(.+?)"').findall(parte2)
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                else:
					linksseccao = re.findall('EPISODIO (.+?)<br.+?\n(.+?)</p>',newmatch[0],re.DOTALL)
					if linksseccao:
                                                ultima_parte = ''
						for parte1,parte2 in linksseccao:
                                                        conta_id_video = 0
							if parte1 != ultima_parte: addDir('[COLOR yellow] Episódio '+parte1+'[/COLOR]',urlfinal,'',iconimage,False,'')
							ultima_parte = parte1
							match = re.compile('<iframe src="(.+?)"').findall(parte2)	
							for url in match:
                                                                conta_id_video = conta_id_video + 1
								TPT_resolve_not_videomega_filmes(url,conta_id_video)
							match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
							match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
							match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
							for url in match:
                                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                        conta_id_video = conta_id_video + 1
                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video)
							match = re.compile('"window.open(.+?)"').findall(parte2)
                                                        for url in match:
                                                                conta_id_video = conta_id_video + 1
                                                                url = url.replace("'","").replace("(","").replace(")","")
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video)
					else:
						match = re.compile('<iframe src="(.+?)"').findall(newmatch[0])	
						for url in match:
                                                        conta_id_video = conta_id_video + 1
							TPT_resolve_not_videomega_filmes(url,conta_id_video)
						match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(newmatch[0])
                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(newmatch[0])
						for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video)
						match = re.compile('"window.open(.+?)"').findall(newmatch[0])
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video)
		
#----------------------------------------------------------------------------------------------------------------------------------------------#

def TPT_resolve_not_videomega_filmes(url,conta_id_video):
        url = url + '///' + name
        if "videomega" in url:
		try:
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "vidto.me" in url:
		try:
                        match = re.compile('http://vidto.me/embed-(.+?).html').findall(url)
			if match:
				id_video = match[0]
				url = 'http://vidto.me/' + id_video + '.html' + '///' + name
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "dropvideo" in url:
		try:
                        url = url.replace('/video/','/embed/')
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'','')
		except:pass
	if "streamin.to" in url:
                try:
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,30,iconimage,'','')
                except:pass                        
    	if "nowvideo" in url:
                try:
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "primeshare" in url:
                try:
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Primeshare.tv)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "videoslasher" in url:
                try:
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoSlasher)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "sockshare" in url:
                try:
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Sockshare)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "putlocker" in url:
                try:
                        url = url.replace('putlocker.com/embed/','firedrive.com/file/')
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	else:
                if "firedrive" in url:
                        try:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'','')
                        except:pass
    	if "movshare" in url:
                try:
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Movshare)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
        if "video.tt" in url:
                try:
                        url = url.replace('///'+name,'')
                        url = url.replace('/video/','/e/')
                        url = url.replace('/video/','/e/')
                        url = url.replace('http://www.video.tt/e/','http://video.tt/e/')
                        url = url.replace('http://www.video.tt/embed/','http://video.tt/e/')
                        url = url.replace('http://video.tt/e/','http://video.tt/player_control/settings.php?v=')+'&fv=v1.2.74'
                        url = url + '///' + name
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Video.tt)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoWood)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	return
   
	
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

	
def TPT_abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

#----------------------------------------------------------------------------------------------------------------------------------------------#
              
def TPT_get_params():
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

def addDir2(nome,url,mode,iconimage,checker,fanart):
        text = 'nnnnnn'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&nome="+urllib.quote_plus(nome)+"&checker="+urllib.quote_plus(checker)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(nome, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'flag.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": nome, "Plot": text } )
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
	
params=TPT_get_params()
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
        nome=urllib.unquote_plus(params["nome"])
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

