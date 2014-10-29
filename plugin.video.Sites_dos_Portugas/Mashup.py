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



import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,os
from array import array
from string import capwords


addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

arr_series1 = [['' for i in range(87)] for j in range(1)]
arr_series = ['' for i in range(200)]
arrai_series = ['' for i in range(200)]
_series = []
_series_ = []
arr_filmes = ['' for i in range(200)]
arrai_filmes = ['' for i in range(200)]
thumb_filmes = ['' for i in range(200)]
arr_filmes[4] = '0'
i=arr_filmes[4]

arr_filmes_anima = []
arrai_filmes_anima = []



progress = xbmcgui.DialogProgress()

#-----------------------------------------------------------------------------------------------------------------------------------------------#

def ultimos_episodios(url):
        conta_os_items = 0
        a = 1
        percent = 0
        message = ''
        site = ''
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar ...'+site, message, "" )
        urlss = urllib.unquote(url)
        print urlss
        urls=re.compile('url_TFC=(.+?)&url_MVT=(.+?)&url_TFV=(.+?)&xpto=xpto&url_TPT=(.+?)&fim=fim').findall(urlss)
        url_TFV = urls[0][2]
        url_TFC = urls[0][0]
        url_MVT = urls[0][1]
        url_TPT = urls[0][3]
        #i = int(arr_filmes[4])
        i = 0
        #--------------------------------------------------
        num = 0
        try:
		html_source = MASH_abrir_url(url_TFV)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		num = len(items)
	try:
		html_source = MASH_abrir_url(url_TPT)
	except: html_source = ''
	items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	num = num + 0.0
	#----------------------------------------------------------------------------------------------------
	site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
        progress.update( percent, 'A Procurar Filmes em '+site, message, "" )
        i = 1

        n_name = name.replace('[COLOR yellow]','')
        n_name = n_name.replace('[/COLOR]','')
        if '-series-' in url:
                series = 1
                url = url.replace('-series-','')
        else: series = 0
        fan = 'nao'
        if selfAddon.getSetting('series-fanart-TPT') == "true": fan = 'sim'

        try:
		html_source = MASH_abrir_url(url_TPT)
	except: html_source = ''
	items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        sinopse = ''
                        fanart = ''
                        thumb = ''
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(int(num))
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(int(num))
                        if fan == 'nao': xbmc.sleep( 50 )
                        if progress.iscanceled():
                                break
                        audio_filme = ''
                        
                        urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(item)
                        if 'title=' in urletitulo[0][0]: urletitulo = re.compile('<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>').findall(item)
                        qualidade = re.compile("<b>QUALIDADE:.+?/b>(.+?)<br/>").findall(item)
                        if not qualidade: qualidade = re.compile("<b>VERSÃO:.+?</b>(.+?)<br/>").findall(item)
                        snpse = re.compile("<b>SINOPSE:.+?/b>(.+?)<br/>").findall(item)
                        if not snpse: qualidade = re.compile("<b>SINOPSE:.+?</b>(.+?)<br/>").findall(item)
                        if snpse: sinopse = snpse[0]
                        else: sinopse = ''
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
                                if series == 1:
                                        nn = 0
                                        nome_pesquisa = n_name
                                else:
                                        n = re.compile('(.+?)[[].+?[]]').findall(nome)
                                        if n:
                                                nome_pesquisa = n[0]
                                                nn = 1
                                        else:
                                                nome_pesquisa = nome
                                                nn = 2
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
                                if 'Temporada' in urletitulo[0][1] or 'Season' in urletitulo[0][1]: url_pesquisa = 'http://www.themoviedb.org/search/tv?query=' + nome_pesquisa
                                else: url_pesquisa = 'http://www.themoviedb.org/search/movie?query=' + nome_pesquisa
                                if thumb == '':
                                        try:
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail: thumb = thumbnail[0].replace('w92','w600')
                                if fan == 'sim':
                                        try:
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                if nn == 1:#addDir1(str(nn),'','',iconimage,False,'')
                                                        for its in items_pesquisa:
                                                                y = re.compile('<h3><a href=".+?" title=".+?">.+?</a> <span>[(](.+?)[)]</span></h3>').findall(its)
                                                                if y: year = y[0]
                                                                else: year = 0
                                                                if str(year) == str(ano_filme):
                                                                        url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(its)
                                                                        if url_filme_pesquisa:
                                                                                url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                                                try:
                                                                                        html_pesquisa = MASH_abrir_url(url_pesquisa)
                                                                                except: html_pesquisa = ''
                                                                                url_fan = re.findall('<div id="backdrops" class="image_carousel">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                                                                if url_fan:
                                                                                        for urls_fanart in url_fan:
                                                                                                url_fanart = re.compile('src="(.+?)"').findall(urls_fanart)
                                                                                                if url_fanart:
                                                                                                        fanart = url_fanart[0].replace('w300','w1280')
                                                                                                else:
                                                                                                        fanart = thumb
                                                                else:
                                                                        url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(items_pesquisa[0])
                                                                        if url_filme_pesquisa:
                                                                                url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                                                try:
                                                                                        html_pesquisa = MASH_abrir_url(url_pesquisa)
                                                                                except: html_pesquisa = ''
                                                                                url_fan = re.findall('<div id="backdrops" class="image_carousel">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                                                                if url_fan:
                                                                                        for urls_fanart in url_fan:
                                                                                                url_fanart = re.compile('src="(.+?)"').findall(urls_fanart)
                                                                                                if url_fanart:
                                                                                                        fanart = url_fanart[0].replace('w300','w1280')
                                                                                                else:
                                                                                                        fanart = thumb
                                                else:
                                                        url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(items_pesquisa[0])
                                                        if url_filme_pesquisa:
                                                                url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                                try:
                                                                        html_pesquisa = MASH_abrir_url(url_pesquisa)
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
                        if fan == "sim":
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
                                addDir_teste('[COLOR orange]TPT | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0],233,thumb,sinopse,fanart,ano_filme,'')
                        except: pass
                        i = i + 1
        else: pass
        if items != []:
                proxima_TPT = re.compile('</span><a class="nextpostslink" rel="next" href="(.+?)">&raquo;</a><a class="last"').findall(html_source)
                try:
                        url_TPT = proxima_TPT[0].replace('#038;','').replace('&amp;','&')
                except: pass
        else: pass
        #----------------------------------------------------------------------------------------------------
	site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv'
	progress.update(percent, 'A Procurar Filmes em '+site, message, "")
        try:
		html_source = MASH_abrir_url(url_TFV)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        thumb = ''
                        fanart = ''
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(int(num))
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(int(num))
                        #if selfAddon.getSetting('series-fanart-TFV') == "false": xbmc.sleep( 50 )
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
                        if selfAddon.getSetting('series-fanart-TFV') == "true":#if fanart == '':
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
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail: thumb = thumbnail[0].replace('w92','w600')
                                if selfAddon.getSetting('series-fanart-TFV') == "true":
                                        try:
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(items_pesquisa[0])
                                                if url_filme_pesquisa:
                                                        url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                        try:
                                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
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
				addDir_teste('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano + '[/COLOR][COLOR red] ' + qualidade + '[/COLOR]',urletitulo[0][0],42,thumb.replace('s72-c','s320'),'',fanart,ano,'')
			except: pass
			i = i + 1
        else: pass
        if items != []:
                proxima_TFV = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
                url_TFV = proxima_TFV[0].replace('&amp;','&')
        else: pass
        #----------------------------------------------------------------------------------------------------
        url_MVT = 'http:'
        url_TFC = 'http:'
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "fim": 'fim',"xpto":'xpto'}
        url_ultimos_episodios = urllib.urlencode(parameters)
        addDir('[COLOR yellow]Página Seguinte >>[/COLOR]',url_ultimos_episodios,508,artfolder + 'PSEGUINTE.png','','')
        progress.close()

        

        

def Filmes_Filmes_Filmes(url):
        conta_os_items = 0
        a = 1
        percent = 0
        message = ''
        site = ''
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar Filmes...'+site, message, "" )
        urlss = urllib.unquote(url)
        print urlss
        urls=re.compile('url_TFC=(.+?)&url_CMT=(.+?)&url_FTT=(.+?)&url_TFV=(.+?)&url_MVT=(.+?)&xpto=xpto&url_TPT=(.+?)&fim=fim').findall(urlss)
        url_TFV = urls[0][3]
        url_TFC = urls[0][0]
        url_MVT = urls[0][4]
        url_TPT = urls[0][5]
        url_FTT = urls[0][2]
        url_CMT = urls[0][1]
        #i = int(arr_filmes[4])
        i = 0
        #--------------------------------------------------
        num = 0
        try:
		html_source = MASH_abrir_url(url_TFV)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		num = len(items)
	try:
		html_source = MASH_abrir_url(url_TFC)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	try:
		html_source = MASH_abrir_url(url_MVT)
	except: html_source = ''
	items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	try:
		html_source = MASH_abrir_url(url_TPT)
	except: html_source = ''
	items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	try:
		html_source = MASH_abrir_url(url_FTT)
	except: html_source = ''
	items = re.findall("<div class='post hentry'>(.+?)<div class='post-outer'>", html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	try:
		html_source = MASH_abrir_url(url_CMT)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	num = num + 0.0
	#----------------------------------------------------------------------------------------------------
	site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
        progress.update( percent, 'A Procurar Filmes em '+site, message, "" )
        i = 0
        a = 0
        try:
		html_source = MASH_abrir_url(url_TPT)
	except: html_source = ''
	items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        sinopse = ''
                        fanart = ''
                        thumb = ''
                        imdbcode = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        progress.update( percent, 'A Procurar Filmes em '+site, message, "" )
                        print str(a) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        #if selfAddon.getSetting('movie-fanart-TPT') == "false": xbmc.sleep( 50 )
                        audio_filme = ''
                        urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(item)
                        if 'title=' in urletitulo[0][0]: urletitulo = re.compile('<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>').findall(item)
                        qualidade = re.compile("<b>QUALIDADE:.+?/b>(.+?)<br/>").findall(item)
                        if not qualidade: qualidade = re.compile("<b>VERSÃO:.+?</b>(.+?)<br/>").findall(item)
                        snpse = re.compile("<b>SINOPSE:.+?/b>(.+?)<br/>").findall(item)
                        if not snpse: qualidade = re.compile("<b>SINOPSE:.+?</b>(.+?)<br/>").findall(item)
                        if snpse: sinopse = snpse[0]
                        else: sinopse = ''
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
                        if selfAddon.getSetting('movie-fanart-TPT') == "true" and fanart == '':
                                n = re.compile('(.+?)[[].+?[]]').findall(nome)
                                if n:
                                        nome_pesquisa = n[0]
                                        nn = 1
                                else:
                                        nome_pesquisa = nome
                                        nn = 2
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
                                if 'Temporada' in urletitulo[0][1] or 'Season' in urletitulo[0][1]: url_pesquisa = 'http://www.themoviedb.org/search/tv?query=' + nome_pesquisa
                                else: url_pesquisa = 'http://www.themoviedb.org/search/movie?query=' + nome_pesquisa
                                if thumb == '':
                                        try:
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail: thumb = thumbnail[0].replace('w92','w600')

                        #if fanart == '': fanart = thumb
                        ano_filme = '('+ano_filme+')'
                        qualidade = '('+qualidade
                        audio_filme = audio_filme+')'
                        try:
                                addDir_teste('[COLOR orange]TPT | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',233,thumb,sinopse,fanart,ano_filme,'')
                        except: pass
                        i = i + 1
                        a = a + 1
        else: pass
        if items != []:
                proxima_TPT = re.compile('</span><a class="nextpostslink" rel="next" href="(.+?)">&raquo;</a><a class="last"').findall(html_source)
                try:
                        url_TPT = proxima_TPT[0].replace('#038;','').replace('&amp;','&')
                except: pass
        else: pass
        #----------------------------------------------------------------------------------------------------
        site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].com'
        progress.update( percent, 'A Procurar Filmes em '+site, message, "" )
        i = 1
        try:
		html_source = MASH_abrir_url(url_TFC)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
                        print str(a) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        #if selfAddon.getSetting('movie-fanart-TFC') == "false": xbmc.sleep( 50 )
                        fanart = ''
                        thumb = ''
                        versao = ''
                        sinopse = ''
                        imdbcode = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
                        pt_en_f = re.compile('<iframe (.+?)</iframe>').findall(item)
                        if '---------------------------------------' in item and len(pt_en_f) > 1: versao = '[COLOR blue] 2 VERSÕES[/COLOR]'
                        assist = re.findall(">ASSISTIR.+?", item, re.DOTALL)
                        if len(assist) > 1: versao = '[COLOR blue] 2 VERSÕES[/COLOR]'
			urletitulo = re.compile("<a href=\'(.+?)\' title=\'(.+?)\'>").findall(item)
			qualidade_ano = re.compile('<b>VERS\xc3\x83O:.+?</b><span style="font-size: x-small;">(.+?)<').findall(item)
			snpse = re.compile('<b>SINOPSE:.+?</b><span style="font-size: x-small;">(.+?)<').findall(item)
			if snpse: sinopse = snpse[0]
			else: sinopse = ''
			thumbnail = re.compile('<img alt="" border="0" src="(.+?)"').findall(item)
			if thumbnail: thumb = thumbnail[0]
			print urletitulo,thumbnail
			ano = 'Ano'
			qualidade = ''
			e_qua = 'nao'
			calid = ''
			if qualidade_ano != []:
                                for q_a in qualidade_ano:
                                        a_q = re.compile('\d+')
                                        qq_aa = a_q.findall(q_a)
                                        for q_a_q_a in qq_aa:
                                                if len(q_a_q_a) == 4:
                                                        ano = q_a_q_a
                                quali = re.compile('\w+')
                                qualid = quali.findall(q_a)
                                for qua_qua in qualid:
                                        if len(qua_qua) == 4 and qua_qua == ano:
                                                e_qua = 'sim'
                                                qua_qua = ''
                                                espaco = ''
                                                espa = 0
                                        if e_qua == 'sim' and espa < 2:
                                                espa = espa + 1
                                        if e_qua == 'sim' and espa == 2:
                                                qualidade = qualidade + espaco + qua_qua
                                                espaco = ' '
                                if len(ano) < 4:
                                        ano = 'Ano'
                                if qualidade == 'PT PT':
                                        qualidade = 'PT-PT'
                                if qualidade == '':
                                        quali_titi = urletitulo[0][1].replace('á','a')
                                        quali_titi = urletitulo[0][1].replace('é','e')
                                        quali_titi = urletitulo[0][1].replace('í','i')
                                        quali_titi = urletitulo[0][1].replace('ó','o')
                                        quali_titi = urletitulo[0][1].replace('ú','u')
                                        quali = re.compile('\w+')
                                        qualid = quali.findall(q_a)
                                        for qua_qua in qualid:
                                                qua_qua = str.capitalize(qua_qua)
                                                calid = calid + ' ' + qua_qua
                                        tita = re.compile('\w+')
                                        titalo = tita.findall(quali_titi)
                                        for tt in titalo:
                                                tt = str.capitalize(tt)
                                                if tt in calid:
                                                        qualidade = re.sub(tt,'',calid)
                                                        calid = re.sub(tt,'',calid)
                                        qqqq = re.compile('\w+')
                                        qqqqq = qqqq.findall(qualidade)
                                        for qqq in qqqqq:
                                                if qqq in quali_titi:
                                                        qualidade = qualidade.replace(qqq,'')
                                        nnnn = re.compile('\d+')
                                        nnnnn = nnnn.findall(qualidade)
                                        for nnn in nnnnn:
                                                if nnn in ano:
                                                        qualidade = qualidade.replace(nnn,'')
                                        quatit = re.compile('\s+')
                                        qualititulo = quatit.findall(qualidade)
                                        for q_t in qualititulo:
                                                if len(q_t)>1:
                                                        qualidade = qualidade.replace(q_t,'')
                                        if qualidade == 'Pt Pt':
                                                qualidade = 'PT-PT'
                        else:
                                qualidade = ''
                        if 'Pt Pt' in qualidade:
                                qualidade = qualidade.replace('Pt Pt','PT-PT')
                        if 'PT PT' in qualidade:
                                qualidade = qualidade.replace('PT PT','PT-PT')
                        nome = urletitulo[0][1]
                        nome = nome.replace('&#8216;',"'")
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&amp;','&')
                        sinopse = sinopse.replace('&#8216;',"'")
                        sinopse = sinopse.replace('&#8217;',"'")
                        sinopse = sinopse.replace('&#8211;',"-")
                        sinopse = sinopse.replace('&#39;',"'")
                        sinopse = sinopse.replace('&amp;','&')
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        tirar_ano = '(' + str(q_a_q_a) + ')'
                                        nome = nome.replace(tirar_ano,'')
                        
                        if imdbcode == '':
                                conta = 0
                                nome_pesquisa = nome
                                nome_pesquisa = nome_pesquisa.replace('é','e')
                                nome_pesquisa = nome_pesquisa.replace('ê','e')
                                nome_pesquisa = nome_pesquisa.replace('á','a')
                                nome_pesquisa = nome_pesquisa.replace('à','a')
                                nome_pesquisa = nome_pesquisa.replace('ã','a')
                                nome_pesquisa = nome_pesquisa.replace('è','e')
                                nome_pesquisa = nome_pesquisa.replace('í','i')
                                nome_pesquisa = nome_pesquisa.replace('ó','o')
                                nome_pesquisa = nome_pesquisa.replace('ô','o')
                                nome_pesquisa = nome_pesquisa.replace('õ','o')
                                nome_pesquisa = nome_pesquisa.replace('ú','u')
                                nome_pesquisa = nome_pesquisa.replace('Ú','U')
                                nome_pesquisa = nome_pesquisa.replace('ç','c')
                                nome_pesquisa = nome_pesquisa.replace('ç','c')
                                a_q = re.compile('\w+')
                                qq_aa = a_q.findall(nome_pesquisa)
                                nome_p = ''
                                for q_a_q_a in qq_aa:
                                        if conta == 0:
                                                nome_p = q_a_q_a
                                                conta = 1
                                        else:
                                                nome_p = nome_p + '+' + q_a_q_a
                                url_imdb = 'http://www.imdb.com/find?ref_=nv_sr_fn&q=' + nome_p + '&s=all#tt'
                                try:
                                        html_imdbcode = MASH_abrir_url(url_imdb)
                                except: html_imdbcode = ''
                                if html_imdbcode != []: filmes_imdb = re.findall('<div class="findSection">(.*?)<div class="findMoreMatches">', html_imdbcode, re.DOTALL)
                                if filmes_imdb: imdbc = re.compile('/title/(.+?)/[?]ref').findall(filmes_imdb[0])
                                if imdbc: imdbcode = imdbc[0]
                                
                        if selfAddon.getSetting('movie-fanart-TFC') == "true" and fanart == '':
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
                                if thumb == '':
                                        try:
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail: thumb = thumbnail[0].replace('w92','w600')
                                if selfAddon.getSetting('movie-fanart-TFC') == "true":
                                        try:
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(items_pesquisa[0])
                                                if url_filme_pesquisa:
                                                        url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                        try:
                                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
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
                        if selfAddon.getSetting('movie-fanart-TFC') == "true":
                                if fanart == '': fanart = thumb
			try:
				if 'ASSISTIR O FILME' in item: addDir_teste('[COLOR orange]TFC | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR][COLOR red] (' + qualidade + ')[/COLOR]' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',73,thumb.replace('s1600','s320').replace('.gif','.jpg'),sinopse,fanart,ano,'')
			except: pass
			a = a + 1
                        i = i + 1
        else: pass
        if items != []:
                proxima_TFC = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
                url_TFC = proxima_TFC[0].replace('&amp;','&')
        else: pass
        #----------------------------------------------------------------------------------------------------

        site = '[B][COLOR green]FOIT[/COLOR][COLOR yellow]A[/COLOR][COLOR red]TUGA[/COLOR][/B]'
	progress.update(percent, 'A Procurar Filmes em '+site, message, "")
        try:
		html_source = MASH_abrir_url(url_FTT)
	except: html_source = ''
	items = re.findall("<div class='post hentry'>(.+?)<div class='post-outer'>", html_source, re.DOTALL)
	if items != []:
		for item in items:
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
                        print str(a) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        #if selfAddon.getSetting('movie-fanart-MVT') == "false": xbmc.sleep( 50 )

                        thumb = ''
                        fanart = ''
                        anofilme= ''
                        qualidade_filme = ''
                        imdbcode = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''

                        urletitulo = re.compile("<a href='(.+?)'>(.+?)</a>").findall(item)
                        if urletitulo:
                                urlvideo = urletitulo[0][0]
                                nome = urletitulo[0][1]
                        else:
                                urlvideo = ''
                                nome = ''
                                
                        ano = re.compile('<strong>Lan\xc3\xa7amento:</strong>(.+?)</div>').findall(item)
                        if ano: anofilme = ano[0]
                        else: anofilme = ''
                        
                        #thumbnail = re.compile('<a href="(.+?)" imageanchor="1"').findall(item)
                        thumbnail = re.compile('document.write[(]bp_thumbnail_resize[(]"(.+?)",".+?"[)]').findall(item)
                        if thumbnail: thumb = thumbnail[0].replace('s72-c','s320').replace('s1600','s320')
                        else: thumb = ''
                        
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('(Pedido)',"").replace('[Pedido]','')
                        
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        anofilme = str(q_a_q_a)
                                        tirar_ano = '- ' + str(q_a_q_a)
                                        nome = nome.replace(tirar_ano,'--')
                                        tirar_ano = '-' + str(q_a_q_a)
                                        nome = nome.replace(tirar_ano,'--')
                                        tirar_ano = str(q_a_q_a)
                                        nome = nome.replace(tirar_ano,'--')

                        qualidade = re.compile("--(.*)").findall(nome)
                        if qualidade:
                                qualidade_filme = qualidade[0]
                                nome = nome.replace('--','')
                                nome = nome.replace(qualidade_filme,'')
                        else:
                                qualidade_filme = ''
                                nome = nome.replace('--','')

                        if 'PT/PT' in nome:
                                qualidade_filme = 'PT/PT'
                                nome = nome.replace('-'+qualidade_filme,'')
                                nome = nome.replace('- '+qualidade_filme,'')
                                nome = nome.replace(qualidade_filme,'')
                        if 'PT-PT' in nome:
                                qualidade_filme = 'PT-PT'
                                nome = nome.replace('-'+qualidade_filme,'')
                                nome = nome.replace('- '+qualidade_filme,'')
                                nome = nome.replace(qualidade_filme,'')
                        if 'PT/BR' in nome:
                                qualidade_filme = 'PT/BR'
                                nome = nome.replace('-'+qualidade_filme,'')
                                nome = nome.replace('- '+qualidade_filme,'')
                                nome = nome.replace(qualidade_filme,'')
                        if 'PT-BR' in nome:
                                qualidade_filme = 'PT-BR'
                                nome = nome.replace('-'+qualidade_filme,'')
                                nome = nome.replace('- '+qualidade_filme,'')
                                nome = nome.replace(qualidade_filme,'')

                        nome = nome.replace('((','(')
                        nome = nome.replace('))',')')
                        nome = nome.replace('()','(')

                        if imdbcode == '':
                                conta = 0
                                nome_pesquisa = nome
                                nome_pesquisa = nome_pesquisa.replace('é','e')
                                nome_pesquisa = nome_pesquisa.replace('ê','e')
                                nome_pesquisa = nome_pesquisa.replace('á','a')
                                nome_pesquisa = nome_pesquisa.replace('à','a')
                                nome_pesquisa = nome_pesquisa.replace('ã','a')
                                nome_pesquisa = nome_pesquisa.replace('è','e')
                                nome_pesquisa = nome_pesquisa.replace('í','i')
                                nome_pesquisa = nome_pesquisa.replace('ó','o')
                                nome_pesquisa = nome_pesquisa.replace('ô','o')
                                nome_pesquisa = nome_pesquisa.replace('õ','o')
                                nome_pesquisa = nome_pesquisa.replace('ú','u')
                                nome_pesquisa = nome_pesquisa.replace('Ú','U')
                                nome_pesquisa = nome_pesquisa.replace('ç','c')
                                nome_pesquisa = nome_pesquisa.replace('ç','c')
                                a_q = re.compile('\w+')
                                qq_aa = a_q.findall(nome_pesquisa)
                                nome_p = ''
                                for q_a_q_a in qq_aa:
                                        if conta == 0:
                                                nome_p = q_a_q_a
                                                conta = 1
                                        else:
                                                nome_p = nome_p + '+' + q_a_q_a
                                url_imdb = 'http://www.imdb.com/find?ref_=nv_sr_fn&q=' + nome_p + '&s=all#tt'
                                html_imdbcode = MASH_abrir_url(url_imdb)
                                filmes_imdb = re.findall('<div class="findSection">(.*?)<div class="findMoreMatches">', html_imdbcode, re.DOTALL)
                                imdbc = re.compile('/title/(.+?)/[?]ref').findall(filmes_imdb[0])
                                imdbcode = imdbc[0]
                                        
                        #fanart = artfolder + 'FAN.jpg'
                        if selfAddon.getSetting('movie-fanart-MVT') == "true" and fanart == '':
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
                                if thumb == '':# or 's1600' in thumb:
                                        try:
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail: thumb = thumbnail[0].replace('w92','w600')
                                if selfAddon.getSetting('movie-fanart-MVT') == "true":
                                        try:
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(items_pesquisa[0])
                                                if url_filme_pesquisa:
                                                        url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                        try:
                                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
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
                        if selfAddon.getSetting('movie-fanart-MVT') == "true":
                                if fanart == '': fanart = thumb
                        try:
                                addDir_teste('[COLOR orange]FTT | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',urlvideo+'IMDB'+imdbcode+'IMDB',603,thumb,'',fanart,anofilme,'')
                        except: pass
                        i = i + 1
                        a = a + 1
                        #---------------------------------------------------------------
	else: pass	
	if items != []:
                proxima = re.compile("<a class='blog-pager-older-link' href='(.+?)' id='Blog1_blog-pager-older-link'").findall(html_source)
                proxima_p = proxima[0]
		url_FTT = proxima_p.replace('&amp;','&')
	else: pass
#------------------------------------------------------------------------------------------------------------------------
	site = '[B][COLOR green]CINE[/COLOR][COLOR yellow]M[/COLOR][COLOR red]ATUGA[/COLOR][/B]'
	progress.update(percent, 'A Procurar Filmes em '+site, message, "")
	
        try:
		html_source = MASH_abrir_url(url_CMT)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	conta_items = 0
	if items != []:
		print len(items)
		for item in items:
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
                        print str(a) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        #if selfAddon.getSetting('movie-fanart-TFV') == "false": xbmc.sleep( 50 )
                        thumb = ''
                        fanart = ''
                        versao = ''
                        audio_filme = ''
                        imdbcode = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
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
                        else:
                                titulooriginal = re.compile("<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>(.+?)<br />").findall(item)
                                if titulooriginal:
                                        nome_original = titulooriginal[0]
                                else: nome_original = ''
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
                        #fanart = artfolder + 'FAN.jpg'
                        if selfAddon.getSetting('movie-fanart-TFV') == "true" and fanart == '':
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
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail: thumb = thumbnail[0].replace('w92','w600')
                                if selfAddon.getSetting('movie-fanart-TFV') == "true":
                                        try:
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(items_pesquisa[0])
                                                if url_filme_pesquisa:
                                                        url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                        try:
                                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
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
                                addDir_teste('[COLOR orange]CMT | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',num_mode,thumb.replace('s72-c','s320'),sinopse,fanart,ano[0],genre)
                        except: pass
                        #---------------------------------------------------------------
                        i = i + 1
                        a = a + 1
                        #---------------------------------------------------------------

	else: pass
	if items != []:
                        proxima = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
                        url_CMT = proxima[0].replace('&amp;','&')
        else: pass
#------------------------------------------------------------------------------------------------------------------------------------
	site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv'
	progress.update(percent, 'A Procurar Filmes em '+site, message, "")
        try:
		html_source = MASH_abrir_url(url_TFV)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
                        print str(a) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        #if selfAddon.getSetting('movie-fanart-TFV') == "false": xbmc.sleep( 50 )
                        thumb = ''
                        fanart = ''
                        versao = ''
                        audio_filme = ''
                        imdbcode = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
                        if 'Portug' and 'Legendado' in item: versao = '[COLOR blue]2 VERSÕES[/COLOR]'
                        genero = re.compile("nero</b>:(.+?)<br />").findall(item)
                        if genero: genre = genero[0]
                        else: genre = ''
                        resumo = re.compile("<b>Resumo</b>:(.+?)<br />").findall(item)
                        if resumo: sinopse = resumo[0]
                        else: sinopse = ''
                        titulooriginal = re.compile("tulo Original:</b>(.+?)<br />").findall(item)
                        if titulooriginal:
                                nome_original = titulooriginal[0]
                        else:
                                titulooriginal = re.compile("<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>(.+?)<br />").findall(item)
                                if titulooriginal:
                                        nome_original = titulooriginal[0]
                                else: nome_original = ''
                        urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)
                        
                        tto=re.compile('tulo Original:</b>:(.+?)<br').findall(item)
                        if tto: ttor = tto[0]
                        else:
                                tto=re.compile('tulo Original:</b>(.+?)<br').findall(item)
                                if tto: ttor = tto[0]
                        ttp=re.compile('<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>:(.+?)<br').findall(item)
                        if ttp: ttpo = ttp[0]
                        else:
                                ttp=re.compile('<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>(.+?)<br').findall(item)
                                if ttp: ttpo = ttp[0]
                        #urletitulo = re.compile("<h1>(.+?)\n</h1>").findall(item)
                        if ttp and not tto: nome = ttp[0]
                        elif not ttp and tto: nome = tto[0]
                        elif ttp and tto:
                                ttocomp = '['+ tto[0]
                                ttpcomp = '['+ ttp[0]
                                if ttpcomp.replace('[ ','') != ttocomp.replace('[ ',''): nome = ttp[0] +' ['+ tto[0] +']'
                                else: nome = ttp[0]
                        elif not ttp and not tto: nome = urletitulo[0][1]
                        nome = nome.replace('[ ',"[")
                        
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
                        #nome = urletitulo[0][1]
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
                        #fanart = artfolder + 'FAN.jpg'
                        if selfAddon.getSetting('movie-fanart-TFV') == "true" and fanart == '':
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
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail: thumb = thumbnail[0].replace('w92','w600')
                                if selfAddon.getSetting('movie-fanart-TFV') == "true":
                                        try:
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(items_pesquisa[0])
                                                if url_filme_pesquisa:
                                                        url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                        try:
                                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
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
                                        num_mode = 42
                                else:
                                        num_mode = 33
                                addDir_teste('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',num_mode,thumb.replace('s72-c','s320'),sinopse,fanart,ano[0],genre)
                        except: pass
                        i = i + 1
                        a = a + 1
        else: pass
        if items != []:
                proxima_TFV = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
                url_TFV = proxima_TFV[0].replace('&amp;','&')
        else: pass
        #----------------------------------------------------------------------------------------------------
        progress.update( percent, 'A Procurar Filmes em '+site, message, "" )
        site = '[B][COLOR green]MOVIE[/COLOR][COLOR yellow]-[/COLOR][COLOR red]TUGA[/COLOR][/B]'
        i = 3
	try:
		html_source = MASH_abrir_url(url_MVT)
	except: html_source = ''
	items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
                        print str(a) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        #if selfAddon.getSetting('movie-fanart-MVT') == "false": xbmc.sleep( 50 )
                        thumb = ''
                        fanart = ''
                        imdbcode = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
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
                        if 'http' not in thumbnail[0]: thumbnail[0] = 'http:' + thumbnail[0]
                        if thumbnail: thumb = thumbnail[0].replace('s72-c','s320')
                        titulo[0] = titulo[0].replace('&#8217;',"'")
                        titulo[0] = titulo[0].replace('&#8211;',"-")
                        if 'Dear John' in titulo[0] and ano[0] == '2013': titulo[0] = titulo[0].replace('Dear John','12 Anos Escravo')
                        nome = titulo[0]
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('PT',"")
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        tirar_ano = '(' + str(q_a_q_a) + ')'
                                        nome = nome.replace(tirar_ano,'')

                        if imdbcode == '':
                                conta = 0
                                nome_pesquisa = nome
                                nome_pesquisa = nome_pesquisa.replace('é','e')
                                nome_pesquisa = nome_pesquisa.replace('ê','e')
                                nome_pesquisa = nome_pesquisa.replace('á','a')
                                nome_pesquisa = nome_pesquisa.replace('à','a')
                                nome_pesquisa = nome_pesquisa.replace('ã','a')
                                nome_pesquisa = nome_pesquisa.replace('è','e')
                                nome_pesquisa = nome_pesquisa.replace('í','i')
                                nome_pesquisa = nome_pesquisa.replace('ó','o')
                                nome_pesquisa = nome_pesquisa.replace('ô','o')
                                nome_pesquisa = nome_pesquisa.replace('õ','o')
                                nome_pesquisa = nome_pesquisa.replace('ú','u')
                                nome_pesquisa = nome_pesquisa.replace('Ú','U')
                                nome_pesquisa = nome_pesquisa.replace('ç','c')
                                nome_pesquisa = nome_pesquisa.replace('ç','c')
                                a_q = re.compile('\w+')
                                qq_aa = a_q.findall(nome_pesquisa)
                                nome_p = ''
                                for q_a_q_a in qq_aa:
                                        if conta == 0:
                                                nome_p = q_a_q_a
                                                conta = 1
                                        else:
                                                nome_p = nome_p + '+' + q_a_q_a
                                url_imdb = 'http://www.imdb.com/find?ref_=nv_sr_fn&q=' + nome_p + '&s=all#tt'
                                html_imdbcode = MASH_abrir_url(url_imdb)
                                filmes_imdb = re.findall('<div class="findSection">(.*?)<div class="findMoreMatches">', html_imdbcode, re.DOTALL)
                                imdbc = re.compile('/title/(.+?)/[?]ref').findall(filmes_imdb[0])
                                imdbcode = imdbc[0]
                                
                        #fanart = artfolder + 'FAN.jpg'
                        if selfAddon.getSetting('movie-fanart-MVT') == "true" and fanart == '':
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
                                if 'Temporada' in titulo[0]: url_pesquisa = 'http://www.themoviedb.org/search/tv?query=' + nome_pesquisa
                                else: url_pesquisa = 'http://www.themoviedb.org/search/movie?query=' + nome_pesquisa
                                if thumb == '' or 's1600' in thumb:
                                        try:
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail: thumb = thumbnail[0].replace('w92','w600')
                                if selfAddon.getSetting('movie-fanart-MVT') == "true":
                                        try:
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(items_pesquisa[0])
                                                if url_filme_pesquisa:
                                                        url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                        try:
                                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
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
                        if selfAddon.getSetting('movie-fanart-MVT') == "true":
                                if fanart == '': fanart = thumb
                        try:
                                addDir_teste('[COLOR orange]MVT | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + ano[0] + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',url[0].replace(' ','%20')+'IMDB'+imdbcode+'IMDB',103,thumb.replace(' ','%20'),'',fanart,ano[0],'')
                        except: pass
                        a = a + 1
                        i = i + 1
        else: pass
        if items != []:
                proxima_MVT = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
                try:
                        url_MVT = proxima_MVT[0].replace('%3A',':')
                        url_MVT = proxima_MVT[0].replace('&amp;','&')
                except: pass
        else: pass
	#if proxima_MVT:
        #----------------------------------------------------------------------------------------------------
        #x = int(arr_filmes[5])        
        for x in range(len(arrai_filmes)):
        #for x in range(12):
                if arrai_filmes[x] != '':           #8
                        addDir(arrai_filmes[x],'url',8,thumb_filmes[x],'nao','')
                        conta_os_items = conta_os_items + 1
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "url_FTT": url_FTT, "url_CMT": url_CMT, "fim": 'fim',"xpto":'xpto'}
        url_filmes_filmes = urllib.urlencode(parameters)
        progress.close()
        addDir('[COLOR yellow]Página Seguinte >>[/COLOR]',url_filmes_filmes,507,artfolder + 'PSEGUINTE.png','','')



def Series_Series(url):
        conta_os_items = 0
        folder = addonfolder + '/resources/'
        Series_File = open(folder + 'series.txt', 'a')
        Series_Fi = open(folder + 'series.txt', 'r')
        read_Series_File = ''
        for line in Series_Fi:
                read_Series_File = read_Series_File + line
                if line!='':_series_.append(line)
        percent = 0
        message = ''
        site = ''
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar Séries...'+site, message, "" )
        #---------------------------------------------------------------------------
        s = 0
        urltfv = 'http://www.tuga-filmes.us'
        try:
                html_series_source = MASH_abrir_url(urltfv)
        except: html_series_source = ''
	html_items_series = re.findall("<div class=\'widget Label\' id=\'Label3\'>\n<h2>S\xc3\xa9ries(.*?)<div class=\'clear\'>", html_series_source, re.DOTALL)
        for item_series in html_items_series:
                series = re.compile("<a dir=\'ltr\' href=\'.+?\'>(.+?)</a>").findall(item_series)
                for nome_series in series:
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        nome_series = nome_series.replace('&#8217;',"'")
                        nome_series = nome_series.replace('&#8230;',"...")
                        nome_series = nome_series.replace('&#8211;',"-")
                        nome_series = nome_series.lower()
                        nome_series = nome_series.title()
                        nome_series = nome_series.replace('Agents Of S.H.I.E.L.D',"Agents Of S.H.I.E.L.D.")
                        _series.append(nome_series)
			s = s + 1
        urltpt = 'http://toppt.net/'
        try:
                html_series_source = MASH_abrir_url(urltpt)
        except: html_series_source = ''
	html_items_series = re.findall('<a href="http://toppt.net/category/series/">SÈRIES NOVAS</a>(.*?)<div class="clearfix">', html_series_source, re.DOTALL)
        print len(html_items_series)
        for item_series in html_items_series:
                series = re.compile('<a href=".+?">(.+?)</a>').findall(item_series)
                for nome_series in series:
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        nome_series = nome_series.replace('&#8217;',"'")
                        nome_series = nome_series.replace('&#8230;',"...")
                        nome_series = nome_series.replace('&#8211;',"-")
                        nome_series = nome_series.replace('Da Vincis Demons',"Da Vinci'S Demons")
                        nome_series = nome_series.lower()
                        nome_series = nome_series.title()
                        if nome_series not in _series:
                                _series.append(nome_series)
				s = s + 1
	html_items_series = re.findall('href="http://toppt.net/category/series/">SÉRIES</a>(.*?)<div id="main">', html_series_source, re.DOTALL)
        print len(html_items_series)
        for item_series in html_items_series:
                series = re.compile('<a href=".+?">(.+?)</a>').findall(item_series)
                for nome_series in series:
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        nome_series = nome_series.replace('&#8217;',"'")
                        nome_series = nome_series.replace('&#8230;',"...")
                        nome_series = nome_series.replace('&#8211;',"-")
                        nome_series = nome_series.replace('Da Vincis Demons',"Da Vinci'S Demons")
                        nome_series = nome_series.lower()
                        nome_series = nome_series.title()
                        if nome_series not in _series:
                                _series.append(nome_series)
				s = s + 1
	#------------------------------------------------------------------------------
        num = s + 0.0
        site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv'
        try:
                html_series_source = MASH_abrir_url(urltfv)
        except: html_series_source = ''
	html_items_series = re.findall("<div class=\'widget Label\' id=\'Label3\'>\n<h2>S\xc3\xa9ries(.*?)<div class=\'clear\'>", html_series_source, re.DOTALL)
        i=0
        for item_series in html_items_series:
                series = re.compile("<a dir=\'ltr\' href=\'(.+?)\'>(.+?)</a>").findall(item_series)
                for endereco_series,nome_series in series:
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(s)
                        progress.update( percent, 'A Procurar Séries em '+site, message, "" )
                        print str(i) + " de " + str(s)
                        #if selfAddon.getSetting('series-thumb-mashup') == "false": xbmc.sleep( 50 )
                        xbmc.sleep( 50 )
                        if progress.iscanceled():
                                break
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        nome_series = nome_series.replace('&#8217;',"'")
                        nome_series = nome_series.replace('&#8230;',"...")
                        nome_series = nome_series.replace('&#8211;',"-")
                        nome_series = nome_series.lower()
                        nome_series = nome_series.title()
                        nome_series = nome_series.replace('Agents Of S.H.I.E.L.D',"Agents Of S.H.I.E.L.D.")
                        if nome_series in read_Series_File:
                                for x in range(len(_series_)):
                                        if nome_series in _series_[x]:
                                                thumbnail = re.compile('.+?[|](.*)').findall(_series_[x])
                                                if thumbnail : thumb = thumbnail[0]
                        else:
                                try:
                                        html_source = MASH_abrir_url(endereco_series)
                                except: html_source = ''
                                items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
                                if items != []:
                                        thumbnail = re.compile('src="(.+?)"').findall(items[0])
                                        if thumbnail : thumb = thumbnail[0]
                                else: thumb = artfolder + 'series.png'
                                Series_File.write(nome_series+'|'+thumb+'\n')
                        arr_series[i]=nome_series
                        arrai_series[i]=nome_series+'[COLOR orange] \/ TFV[/COLOR]'+'|'+thumb+'|'+endereco_series
                        i=i+1
        Series_Fi.close()
        Series_File.close()
        Series_File = open(folder + 'series.txt', 'a')
        Series_Fi = open(folder + 'series.txt', 'r')
        read_Series_File = ''
        for line in Series_Fi:
                read_Series_File = read_Series_File + line
                if line!='':_series_.append(line)
        url = 'http://toppt.net/'
        site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
        try:
                html_series_source = MASH_abrir_url(url)
        except: html_series_source = ''
	html_items_series = re.findall('<a href="http://toppt.net/category/series/">SÈRIES NOVAS</a>(.*?)<div class="clearfix">', html_series_source, re.DOTALL)
        print len(html_items_series)
        for item_series in html_items_series:
                series = re.compile('<a href="(.+?)">(.+?)</a>').findall(item_series)
                for endereco_series,nome_series in series:
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        nome_series = nome_series.replace('&#8217;',"'")
                        nome_series = nome_series.replace('&#8230;',"...")
                        nome_series = nome_series.replace('&#8211;',"-")
                        nome_series = nome_series.replace('Da Vincis Demons',"Da Vinci'S Demons")
                        nome_series = nome_series.lower()
                        nome_series = nome_series.title()
                        if nome_series in read_Series_File:
                                for x in range(len(_series_)):
                                        if nome_series in _series_[x]:
                                                thumbnail = re.compile('.+?[|](.*)').findall(_series_[x])
                                                if thumbnail : thumb = thumbnail[0]
                        else:
                                try:
                                        html_source = MASH_abrir_url(endereco_series)
                                except: html_source = ''
                                items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
                                if items != []:
                                        thumbnail = re.compile('src="(.+?)"').findall(items[0])
                                        if thumbnail : thumb = thumbnail[0]
                                else: thumb = artfolder + 'series.png'
                                Series_File.write(nome_series+'|'+thumb+'\n')
                        if nome_series in arr_series:
                                contaP = re.compile('(.+?)[|](.+?)[|](.+?)[|](.*)').findall(arrai_series[arr_series.index(nome_series)])
                                if not contaP:
                                        arrai_series[arr_series.index(nome_series)]=arrai_series[arr_series.index(nome_series)].replace('[COLOR orange] \/ TFV[/COLOR]','[COLOR orange] \/ TFV \/ TPT[/COLOR]')
                                        arrai_series[arr_series.index(nome_series)]=arrai_series[arr_series.index(nome_series)]+'|'+endereco_series
                        if nome_series not in arr_series:
                                percent = int( ( i / num ) * 100)
                                message = str(i) + " de " + str(s)
                                progress.update( percent, 'A Procurar Séries em '+site, message, "" )
                                print str(i) + " de " + str(s)
                                #if selfAddon.getSetting('series-thumb-mashup') == "false": xbmc.sleep( 50 )
                                xbmc.sleep( 50 )
                                if progress.iscanceled():
                                        break
                                arr_series[i]=nome_series
                                arrai_series[i]=nome_series+'[COLOR orange] \/ TPT[/COLOR]'+'|'+thumb+'|'+endereco_series
                                i=i+1
        html_items_series = re.findall('href="http://toppt.net/category/series/">SÉRIES</a>(.*?)<div id="main">', html_series_source, re.DOTALL)
        print len(html_items_series)
        for item_series in html_items_series:
                series = re.compile('<a href="(.+?)">(.+?)</a>').findall(item_series)
                for endereco_series,nome_series in series:
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        nome_series = nome_series.replace('&#8217;',"'")
                        nome_series = nome_series.replace('&#8230;',"...")
                        nome_series = nome_series.replace('&#8211;',"-")
                        nome_series = nome_series.replace('Da Vincis Demons',"Da Vinci'S Demons")
                        nome_series = nome_series.lower()
                        nome_series = nome_series.title()
                        if nome_series in read_Series_File:
                                for x in range(len(_series_)):
                                        if nome_series in _series_[x]:
                                                thumbnail = re.compile('.+?[|](.*)').findall(_series_[x])
                                                if thumbnail : thumb = thumbnail[0]
                        else:
                                try:
                                        html_source = MASH_abrir_url(endereco_series)
                                except: html_source = ''
                                items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
                                if items != []:
                                        thumbnail = re.compile('src="(.+?)"').findall(items[0])
                                        if thumbnail : thumb = thumbnail[0]
                                else: thumb = artfolder + 'series.png'
                                Series_File.write(nome_series+'|'+thumb+'\n')
                        if nome_series in arr_series:
                                contaP = re.compile('(.+?)[|](.+?)[|](.+?)[|](.*)').findall(arrai_series[arr_series.index(nome_series)])
                                if not contaP:
                                        arrai_series[arr_series.index(nome_series)]=arrai_series[arr_series.index(nome_series)].replace('[COLOR orange] \/ TFV[/COLOR]','[COLOR orange] \/ TFV \/ TPT[/COLOR]')
                                        arrai_series[arr_series.index(nome_series)]=arrai_series[arr_series.index(nome_series)]+'|'+endereco_series
                        if nome_series not in arr_series:
                                percent = int( ( i / num ) * 100)
                                message = str(i) + " de " + str(s)
                                progress.update( percent, 'A Procurar Séries em '+site, message, "" )
                                print str(i) + " de " + str(s)
                                #if selfAddon.getSetting('series-thumb-mashup') == "false": xbmc.sleep( 50 )
                                xbmc.sleep( 50 )
                                if progress.iscanceled():
                                        break
                                arr_series[i]=nome_series
                                arrai_series[i]=nome_series+'[COLOR orange] \/ TPT[/COLOR]'+'|'+thumb+'|'+endereco_series
                                i=i+1
        arrai_series.sort()
        for x in range(len(arrai_series)):
                if arrai_series[x] != '':
                        _s = re.compile('(.+?)[|](.+?)[|](.+?)[|](.*)').findall(arrai_series[x])
                        if _s:
                                conta_os_items = conta_os_items + 1
                                addDir(_s[0][0].replace('\/','|'),_s[0][2]+'|'+_s[0][3],9,_s[0][1],'nao','')
                        else:
                                _s = re.compile('(.+?)[|](.+?)[|](.*)').findall(arrai_series[x])
                                conta_os_items = conta_os_items + 1
                                addDir(_s[0][0].replace('\/','|'),_s[0][2],9,_s[0][1],'nao','')
        Series_Fi.close()
        Series_File.close()
        progress.close()



def Filmes_Animacao(url):
        conta_os_items = 0
        a = 1
        percent = 0
        message = ''
        site = ''
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar Animação...'+site, message, "" )
        urlss = urllib.unquote(url)
        print urlss
        urls=re.compile('url_TFC=(.+?)&url_CMT=(.+?)&url_FTT=(.+?)&url_TFV=(.+?)&url_MVT=(.+?)&xpto=xpto&url_TPT=(.+?)&fim=fim').findall(urlss)
        url_TFV = urls[0][3]
        url_TFC = urls[0][0]
        url_MVT = urls[0][4]
        url_TPT = urls[0][5]
        url_FTT = urls[0][2]
        url_CMT = urls[0][1]
        #i = int(arr_filmes[4])
        i = 0
        #--------------------------------------------------
        num = 0
        try:
		html_source = MASH_abrir_url(url_TFV)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		num = len(items)
	try:
		html_source = MASH_abrir_url(url_TFC)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	try:
		html_source = MASH_abrir_url(url_MVT)
	except: html_source = ''
	items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	try:
		html_source = MASH_abrir_url(url_TPT)
	except: html_source = ''
	items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	try:
		html_source = MASH_abrir_url(url_FTT)
	except: html_source = ''
	items = re.findall("<div class='post hentry'>(.+?)<div class='post-outer'>", html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	try:
		html_source = MASH_abrir_url(url_CMT)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	num = num + 0.0
	#----------------------------------------------------------------------------------------------------
	site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
        progress.update( percent, 'A Procurar Filmes em '+site, message, "" )
        i = 0
        a = 0
        try:
		html_source = MASH_abrir_url(url_TPT)
	except: html_source = ''
	items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        sinopse = ''
                        fanart = ''
                        thumb = ''
                        imdbcode = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        progress.update( percent, 'A Procurar Filmes em '+site, message, "" )
                        print str(a) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        #if selfAddon.getSetting('movie-fanart-TPT') == "false": xbmc.sleep( 50 )
                        audio_filme = ''
                        urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(item)
                        if 'title=' in urletitulo[0][0]: urletitulo = re.compile('<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>').findall(item)
                        qualidade = re.compile("<b>QUALIDADE:.+?/b>(.+?)<br/>").findall(item)
                        if not qualidade: qualidade = re.compile("<b>VERSÃO:.+?</b>(.+?)<br/>").findall(item)
                        snpse = re.compile("<b>SINOPSE:.+?/b>(.+?)<br/>").findall(item)
                        if not snpse: qualidade = re.compile("<b>SINOPSE:.+?</b>(.+?)<br/>").findall(item)
                        if snpse: sinopse = snpse[0]
                        else: sinopse = ''
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
                        if selfAddon.getSetting('movie-fanart-TPT') == "true" and fanart == '':
                                n = re.compile('(.+?)[[].+?[]]').findall(nome)
                                if n:
                                        nome_pesquisa = n[0]
                                        nn = 1
                                else:
                                        nome_pesquisa = nome
                                        nn = 2
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
                                if 'Temporada' in urletitulo[0][1] or 'Season' in urletitulo[0][1]: url_pesquisa = 'http://www.themoviedb.org/search/tv?query=' + nome_pesquisa
                                else: url_pesquisa = 'http://www.themoviedb.org/search/movie?query=' + nome_pesquisa
                                if thumb == '':
                                        try:
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail: thumb = thumbnail[0].replace('w92','w600')

                        #if fanart == '': fanart = thumb
                        ano_filme = '('+ano_filme+')'
                        qualidade = '('+qualidade
                        audio_filme = audio_filme+')'
                        try:
                                addDir_teste('[COLOR orange]TPT | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',233,thumb,sinopse,fanart,ano_filme,'')
                        except: pass
                        i = i + 1
                        a = a + 1
        else: pass
        if items != []:
                proxima_TPT = re.compile('</span><a class="nextpostslink" rel="next" href="(.+?)">&raquo;</a><a class="last"').findall(html_source)
                try:
                        url_TPT = proxima_TPT[0].replace('#038;','').replace('&amp;','&')
                except: pass
        else: pass
        #----------------------------------------------------------------------------------------------------
        site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].com'
        progress.update( percent, 'A Procurar Filmes em '+site, message, "" )
        i = 1
        try:
		html_source = MASH_abrir_url(url_TFC)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
                        print str(a) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        #if selfAddon.getSetting('movie-fanart-TFC') == "false": xbmc.sleep( 50 )
                        fanart = ''
                        thumb = ''
                        versao = ''
                        sinopse = ''
                        imdbcode = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
                        pt_en_f = re.compile('<iframe (.+?)</iframe>').findall(item)
                        if '---------------------------------------' in item and len(pt_en_f) > 1: versao = '[COLOR blue] 2 VERSÕES[/COLOR]'
                        assist = re.findall(">ASSISTIR.+?", item, re.DOTALL)
                        if len(assist) > 1: versao = '[COLOR blue] 2 VERSÕES[/COLOR]'
			urletitulo = re.compile("<a href=\'(.+?)\' title=\'(.+?)\'>").findall(item)
			qualidade_ano = re.compile('<b>VERS\xc3\x83O:.+?</b><span style="font-size: x-small;">(.+?)<').findall(item)
			snpse = re.compile('<b>SINOPSE:.+?</b><span style="font-size: x-small;">(.+?)<').findall(item)
			if snpse: sinopse = snpse[0]
			else: sinopse = ''
			thumbnail = re.compile('<img alt="" border="0" src="(.+?)"').findall(item)
			if thumbnail: thumb = thumbnail[0]
			print urletitulo,thumbnail
			ano = 'Ano'
			qualidade = ''
			e_qua = 'nao'
			calid = ''
			if qualidade_ano != []:
                                for q_a in qualidade_ano:
                                        a_q = re.compile('\d+')
                                        qq_aa = a_q.findall(q_a)
                                        for q_a_q_a in qq_aa:
                                                if len(q_a_q_a) == 4:
                                                        ano = q_a_q_a
                                quali = re.compile('\w+')
                                qualid = quali.findall(q_a)
                                for qua_qua in qualid:
                                        if len(qua_qua) == 4 and qua_qua == ano:
                                                e_qua = 'sim'
                                                qua_qua = ''
                                                espaco = ''
                                                espa = 0
                                        if e_qua == 'sim' and espa < 2:
                                                espa = espa + 1
                                        if e_qua == 'sim' and espa == 2:
                                                qualidade = qualidade + espaco + qua_qua
                                                espaco = ' '
                                if len(ano) < 4:
                                        ano = 'Ano'
                                if qualidade == 'PT PT':
                                        qualidade = 'PT-PT'
                                if qualidade == '':
                                        quali_titi = urletitulo[0][1].replace('á','a')
                                        quali_titi = urletitulo[0][1].replace('é','e')
                                        quali_titi = urletitulo[0][1].replace('í','i')
                                        quali_titi = urletitulo[0][1].replace('ó','o')
                                        quali_titi = urletitulo[0][1].replace('ú','u')
                                        quali = re.compile('\w+')
                                        qualid = quali.findall(q_a)
                                        for qua_qua in qualid:
                                                qua_qua = str.capitalize(qua_qua)
                                                calid = calid + ' ' + qua_qua
                                        tita = re.compile('\w+')
                                        titalo = tita.findall(quali_titi)
                                        for tt in titalo:
                                                tt = str.capitalize(tt)
                                                if tt in calid:
                                                        qualidade = re.sub(tt,'',calid)
                                                        calid = re.sub(tt,'',calid)
                                        qqqq = re.compile('\w+')
                                        qqqqq = qqqq.findall(qualidade)
                                        for qqq in qqqqq:
                                                if qqq in quali_titi:
                                                        qualidade = qualidade.replace(qqq,'')
                                        nnnn = re.compile('\d+')
                                        nnnnn = nnnn.findall(qualidade)
                                        for nnn in nnnnn:
                                                if nnn in ano:
                                                        qualidade = qualidade.replace(nnn,'')
                                        quatit = re.compile('\s+')
                                        qualititulo = quatit.findall(qualidade)
                                        for q_t in qualititulo:
                                                if len(q_t)>1:
                                                        qualidade = qualidade.replace(q_t,'')
                                        if qualidade == 'Pt Pt':
                                                qualidade = 'PT-PT'
                        else:
                                qualidade = ''
                        if 'Pt Pt' in qualidade:
                                qualidade = qualidade.replace('Pt Pt','PT-PT')
                        if 'PT PT' in qualidade:
                                qualidade = qualidade.replace('PT PT','PT-PT')
                        nome = urletitulo[0][1]
                        nome = nome.replace('&#8216;',"'")
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&amp;','&')
                        sinopse = sinopse.replace('&#8216;',"'")
                        sinopse = sinopse.replace('&#8217;',"'")
                        sinopse = sinopse.replace('&#8211;',"-")
                        sinopse = sinopse.replace('&#39;',"'")
                        sinopse = sinopse.replace('&amp;','&')
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        tirar_ano = '(' + str(q_a_q_a) + ')'
                                        nome = nome.replace(tirar_ano,'')

                        if imdbcode == '':
                                conta = 0
                                nome_pesquisa = nome
                                nome_pesquisa = nome_pesquisa.replace('é','e')
                                nome_pesquisa = nome_pesquisa.replace('ê','e')
                                nome_pesquisa = nome_pesquisa.replace('á','a')
                                nome_pesquisa = nome_pesquisa.replace('à','a')
                                nome_pesquisa = nome_pesquisa.replace('ã','a')
                                nome_pesquisa = nome_pesquisa.replace('è','e')
                                nome_pesquisa = nome_pesquisa.replace('í','i')
                                nome_pesquisa = nome_pesquisa.replace('ó','o')
                                nome_pesquisa = nome_pesquisa.replace('ô','o')
                                nome_pesquisa = nome_pesquisa.replace('õ','o')
                                nome_pesquisa = nome_pesquisa.replace('ú','u')
                                nome_pesquisa = nome_pesquisa.replace('Ú','U')
                                nome_pesquisa = nome_pesquisa.replace('ç','c')
                                nome_pesquisa = nome_pesquisa.replace('ç','c')
                                a_q = re.compile('\w+')
                                qq_aa = a_q.findall(nome_pesquisa)
                                nome_p = ''
                                for q_a_q_a in qq_aa:
                                        if conta == 0:
                                                nome_p = q_a_q_a
                                                conta = 1
                                        else:
                                                nome_p = nome_p + '+' + q_a_q_a
                                url_imdb = 'http://www.imdb.com/find?ref_=nv_sr_fn&q=' + nome_p + '&s=all#tt'
                                html_imdbcode = MASH_abrir_url(url_imdb)
                                filmes_imdb = re.findall('<div class="findSection">(.*?)<div class="findMoreMatches">', html_imdbcode, re.DOTALL)
                                imdbc = re.compile('/title/(.+?)/[?]ref').findall(filmes_imdb[0])
                                imdbcode = imdbc[0]
                                
                        if selfAddon.getSetting('movie-fanart-TFC') == "true" and fanart == '':
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
                                if thumb == '':
                                        try:
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail: thumb = thumbnail[0].replace('w92','w600')
                                if selfAddon.getSetting('movie-fanart-TFC') == "true":
                                        try:
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(items_pesquisa[0])
                                                if url_filme_pesquisa:
                                                        url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                        try:
                                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
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
                        if selfAddon.getSetting('movie-fanart-TFC') == "true":
                                if fanart == '': fanart = thumb
			try:
				if 'ASSISTIR O FILME' in item: addDir_teste('[COLOR orange]TFC | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR][COLOR red] (' + qualidade + ')[/COLOR]' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',73,thumb.replace('s1600','s320').replace('.gif','.jpg'),sinopse,fanart,ano,'')
			except: pass
			a = a + 1
                        i = i + 1
        else: pass
        if items != []:
                proxima_TFC = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
                url_TFC = proxima_TFC[0].replace('&amp;','&')
        else: pass
        #----------------------------------------------------------------------------------------------------
        site = '[B][COLOR green]FOIT[/COLOR][COLOR yellow]A[/COLOR][COLOR red]TUGA[/COLOR][/B]'
	progress.update(percent, 'A Procurar Filmes em '+site, message, "")
        try:
		html_source = MASH_abrir_url(url_FTT)
	except: html_source = ''
	items = re.findall("<div class='post hentry'>(.+?)<div class='post-outer'>", html_source, re.DOTALL)
	if items != []:
		for item in items:
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
                        print str(a) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        #if selfAddon.getSetting('movie-fanart-MVT') == "false": xbmc.sleep( 50 )

                        thumb = ''
                        fanart = ''
                        anofilme= ''
                        qualidade_filme = ''
                        imdbcode = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''

                        urletitulo = re.compile("<a href='(.+?)'>(.+?)</a>").findall(item)
                        if urletitulo:
                                urlvideo = urletitulo[0][0]
                                nome = urletitulo[0][1]
                        else:
                                urlvideo = ''
                                nome = ''
                                
                        ano = re.compile('<strong>Lan\xc3\xa7amento:</strong>(.+?)</div>').findall(item)
                        if ano: anofilme = ano[0]
                        else: anofilme = ''
                        
                        #thumbnail = re.compile('<a href="(.+?)" imageanchor="1"').findall(item)
                        thumbnail = re.compile('document.write[(]bp_thumbnail_resize[(]"(.+?)",".+?"[)]').findall(item)
                        if thumbnail: thumb = thumbnail[0].replace('s72-c','s320').replace('s1600','s320')
                        else: thumb = ''
                        
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('(Pedido)',"").replace('[Pedido]','')
                        
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        anofilme = str(q_a_q_a)
                                        tirar_ano = '- ' + str(q_a_q_a)
                                        nome = nome.replace(tirar_ano,'--')
                                        tirar_ano = '-' + str(q_a_q_a)
                                        nome = nome.replace(tirar_ano,'--')
                                        tirar_ano = str(q_a_q_a)
                                        nome = nome.replace(tirar_ano,'--')

                        qualidade = re.compile("--(.*)").findall(nome)
                        if qualidade:
                                qualidade_filme = qualidade[0]
                                nome = nome.replace('--','')
                                nome = nome.replace(qualidade_filme,'')
                        else:
                                qualidade_filme = ''
                                nome = nome.replace('--','')

                        if 'PT/PT' in nome:
                                qualidade_filme = 'PT/PT'
                                nome = nome.replace('-'+qualidade_filme,'')
                                nome = nome.replace('- '+qualidade_filme,'')
                                nome = nome.replace(qualidade_filme,'')
                        if 'PT-PT' in nome:
                                qualidade_filme = 'PT-PT'
                                nome = nome.replace('-'+qualidade_filme,'')
                                nome = nome.replace('- '+qualidade_filme,'')
                                nome = nome.replace(qualidade_filme,'')
                        if 'PT/BR' in nome:
                                qualidade_filme = 'PT/BR'
                                nome = nome.replace('-'+qualidade_filme,'')
                                nome = nome.replace('- '+qualidade_filme,'')
                                nome = nome.replace(qualidade_filme,'')
                        if 'PT-BR' in nome:
                                qualidade_filme = 'PT-BR'
                                nome = nome.replace('-'+qualidade_filme,'')
                                nome = nome.replace('- '+qualidade_filme,'')
                                nome = nome.replace(qualidade_filme,'')

                        nome = nome.replace('((','(')
                        nome = nome.replace('))',')')
                        nome = nome.replace('()','(')

                        if imdbcode == '':
                                conta = 0
                                nome_pesquisa = nome
                                nome_pesquisa = nome_pesquisa.replace('é','e')
                                nome_pesquisa = nome_pesquisa.replace('ê','e')
                                nome_pesquisa = nome_pesquisa.replace('á','a')
                                nome_pesquisa = nome_pesquisa.replace('à','a')
                                nome_pesquisa = nome_pesquisa.replace('ã','a')
                                nome_pesquisa = nome_pesquisa.replace('è','e')
                                nome_pesquisa = nome_pesquisa.replace('í','i')
                                nome_pesquisa = nome_pesquisa.replace('ó','o')
                                nome_pesquisa = nome_pesquisa.replace('ô','o')
                                nome_pesquisa = nome_pesquisa.replace('õ','o')
                                nome_pesquisa = nome_pesquisa.replace('ú','u')
                                nome_pesquisa = nome_pesquisa.replace('Ú','U')
                                nome_pesquisa = nome_pesquisa.replace('ç','c')
                                nome_pesquisa = nome_pesquisa.replace('ç','c')
                                a_q = re.compile('\w+')
                                qq_aa = a_q.findall(nome_pesquisa)
                                nome_p = ''
                                for q_a_q_a in qq_aa:
                                        if conta == 0:
                                                nome_p = q_a_q_a
                                                conta = 1
                                        else:
                                                nome_p = nome_p + '+' + q_a_q_a
                                url_imdb = 'http://www.imdb.com/find?ref_=nv_sr_fn&q=' + nome_p + '&s=all#tt'
                                html_imdbcode = MASH_abrir_url(url_imdb)
                                filmes_imdb = re.findall('<div class="findSection">(.*?)<div class="findMoreMatches">', html_imdbcode, re.DOTALL)
                                imdbc = re.compile('/title/(.+?)/[?]ref').findall(filmes_imdb[0])
                                imdbcode = imdbc[0]
                                        
                        #fanart = artfolder + 'FAN.jpg'
                        if selfAddon.getSetting('movie-fanart-MVT') == "true" and fanart == '':
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
                                if thumb == '':# or 's1600' in thumb:
                                        try:
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail: thumb = thumbnail[0].replace('w92','w600')
                                if selfAddon.getSetting('movie-fanart-MVT') == "true":
                                        try:
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(items_pesquisa[0])
                                                if url_filme_pesquisa:
                                                        url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                        try:
                                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
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
                        if selfAddon.getSetting('movie-fanart-MVT') == "true":
                                if fanart == '': fanart = thumb
                        try:
                                addDir_teste('[COLOR orange]FTT | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',urlvideo+'IMDB'+imdbcode+'IMDB',603,thumb,'',fanart,anofilme,'')
                        except: pass
                        i = i + 1
                        a = a + 1
                        #---------------------------------------------------------------
	else: pass	
	if items != []:
                proxima = re.compile("<a class='blog-pager-older-link' href='(.+?)' id='Blog1_blog-pager-older-link'").findall(html_source)
                proxima_p = proxima[0]
		url_FTT = proxima_p.replace('&amp;','&')
	else: pass
	#------------------------------------------------------------------------------------------------------------------------
	site = '[B][COLOR green]CINE[/COLOR][COLOR yellow]M[/COLOR][COLOR red]ATUGA[/COLOR][/B]'
	progress.update(percent, 'A Procurar Filmes em '+site, message, "")
	
        try:
		html_source = MASH_abrir_url(url_CMT)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	conta_items = 0
	if items != []:
		print len(items)
		for item in items:
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
                        print str(a) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        #if selfAddon.getSetting('movie-fanart-TFV') == "false": xbmc.sleep( 50 )
                        thumb = ''
                        fanart = ''
                        versao = ''
                        audio_filme = ''
                        imdbcode = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
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
                        else:
                                titulooriginal = re.compile("<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>(.+?)<br />").findall(item)
                                if titulooriginal:
                                        nome_original = titulooriginal[0]
                                else: nome_original = ''
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
                        #fanart = artfolder + 'FAN.jpg'
                        if selfAddon.getSetting('movie-fanart-TFV') == "true" and fanart == '':
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
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail: thumb = thumbnail[0].replace('w92','w600')
                                if selfAddon.getSetting('movie-fanart-TFV') == "true":
                                        try:
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(items_pesquisa[0])
                                                if url_filme_pesquisa:
                                                        url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                        try:
                                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
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
                                addDir_teste('[COLOR orange]CMT | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',num_mode,thumb.replace('s72-c','s320'),sinopse,fanart,ano[0],genre)
                        except: pass
                        #---------------------------------------------------------------
                        i = i + 1
                        a = a + 1
                        #---------------------------------------------------------------

	else: pass
	if items != []:
                        proxima = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
                        url_CMT = proxima[0].replace('&amp;','&')
        else: pass
#------------------------------------------------------------------------------------------------------------------------        
	site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv'
	progress.update(percent, 'A Procurar Filmes em '+site, message, "")
        try:
		html_source = MASH_abrir_url(url_TFV)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
                        print str(a) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        #if selfAddon.getSetting('movie-fanart-TFV') == "false": xbmc.sleep( 50 )
                        thumb = ''
                        fanart = ''
                        versao = ''
                        audio_filme = ''
                        imdbcode = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
                        if 'Portug' and 'Legendado' in item: versao = '[COLOR blue]2 VERSÕES[/COLOR]'
                        genero = re.compile("nero</b>:(.+?)<br />").findall(item)
                        if genero: genre = genero[0]
                        else: genre = ''
                        resumo = re.compile("<b>Resumo</b>:(.+?)<br />").findall(item)
                        if resumo: sinopse = resumo[0]
                        else: sinopse = ''
                        titulooriginal = re.compile("tulo Original:</b>(.+?)<br />").findall(item)
                        if titulooriginal:
                                nome_original = titulooriginal[0]
                        else:
                                titulooriginal = re.compile("<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>(.+?)<br />").findall(item)
                                if titulooriginal:
                                        nome_original = titulooriginal[0]
                                else: nome_original = ''
                        urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)

                        tto=re.compile('tulo Original:</b>:(.+?)<br').findall(item)
                        if tto: ttor = tto[0]
                        else:
                                tto=re.compile('tulo Original:</b>(.+?)<br').findall(item)
                                if tto: ttor = tto[0]
                        ttp=re.compile('<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>:(.+?)<br').findall(item)
                        if ttp: ttpo = ttp[0]
                        else:
                                ttp=re.compile('<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>(.+?)<br').findall(item)
                                if ttp: ttpo = ttp[0]
                        #urletitulo = re.compile("<h1>(.+?)\n</h1>").findall(item)
                        if ttp and not tto: nome = ttp[0]
                        elif not ttp and tto: nome = tto[0]
                        elif ttp and tto:
                                ttocomp = '['+ tto[0]
                                ttpcomp = '['+ ttp[0]
                                if ttpcomp.replace('[ ','') != ttocomp.replace('[ ',''): nome = ttp[0] +' ['+ tto[0] +']'
                                else: nome = ttp[0]
                        elif not ttp and not tto: nome = urletitulo[0][1]
                        nome = nome.replace('[ ',"[")
                        
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
                        #nome = urletitulo[0][1]
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
                        #fanart = artfolder + 'FAN.jpg'
                        if selfAddon.getSetting('movie-fanart-TFV') == "true" and fanart == '':
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
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail: thumb = thumbnail[0].replace('w92','w600')
                                if selfAddon.getSetting('movie-fanart-TFV') == "true":
                                        try:
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(items_pesquisa[0])
                                                if url_filme_pesquisa:
                                                        url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                        try:
                                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
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
                                        num_mode = 42
                                else:
                                        num_mode = 33
                                addDir_teste('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',num_mode,thumb.replace('s72-c','s320'),sinopse,fanart,ano[0],genre)
                        except: pass
                        i = i + 1
                        a = a + 1
        else: pass
        if items != []:
                proxima_TFV = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
                url_TFV = proxima_TFV[0].replace('&amp;','&')
        else: pass
        #----------------------------------------------------------------------------------------------------
        progress.update( percent, 'A Procurar Filmes em '+site, message, "" )
        site = '[B][COLOR green]MOVIE[/COLOR][COLOR yellow]-[/COLOR][COLOR red]TUGA[/COLOR][/B]'
        i = 3
	try:
		html_source = MASH_abrir_url(url_MVT)
	except: html_source = ''
	items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
                        print str(a) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        #if selfAddon.getSetting('movie-fanart-MVT') == "false": xbmc.sleep( 50 )
                        thumb = ''
                        fanart = ''
                        imdbcode = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
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
                        if 'http' not in thumbnail[0]: thumbnail[0] = 'http:' + thumbnail[0]
                        if thumbnail: thumb = thumbnail[0].replace('s72-c','s320')
                        titulo[0] = titulo[0].replace('&#8217;',"'")
                        titulo[0] = titulo[0].replace('&#8211;',"-")
                        if 'Dear John' in titulo[0] and ano[0] == '2013': titulo[0] = titulo[0].replace('Dear John','12 Anos Escravo')
                        nome = titulo[0]
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('PT',"")
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        tirar_ano = '(' + str(q_a_q_a) + ')'
                                        nome = nome.replace(tirar_ano,'')

                        if imdbcode == '':
                                conta = 0
                                nome_pesquisa = nome
                                nome_pesquisa = nome_pesquisa.replace('é','e')
                                nome_pesquisa = nome_pesquisa.replace('ê','e')
                                nome_pesquisa = nome_pesquisa.replace('á','a')
                                nome_pesquisa = nome_pesquisa.replace('à','a')
                                nome_pesquisa = nome_pesquisa.replace('ã','a')
                                nome_pesquisa = nome_pesquisa.replace('è','e')
                                nome_pesquisa = nome_pesquisa.replace('í','i')
                                nome_pesquisa = nome_pesquisa.replace('ó','o')
                                nome_pesquisa = nome_pesquisa.replace('ô','o')
                                nome_pesquisa = nome_pesquisa.replace('õ','o')
                                nome_pesquisa = nome_pesquisa.replace('ú','u')
                                nome_pesquisa = nome_pesquisa.replace('Ú','U')
                                nome_pesquisa = nome_pesquisa.replace('ç','c')
                                nome_pesquisa = nome_pesquisa.replace('ç','c')
                                a_q = re.compile('\w+')
                                qq_aa = a_q.findall(nome_pesquisa)
                                nome_p = ''
                                for q_a_q_a in qq_aa:
                                        if conta == 0:
                                                nome_p = q_a_q_a
                                                conta = 1
                                        else:
                                                nome_p = nome_p + '+' + q_a_q_a
                                url_imdb = 'http://www.imdb.com/find?ref_=nv_sr_fn&q=' + nome_p + '&s=all#tt'
                                html_imdbcode = MASH_abrir_url(url_imdb)
                                filmes_imdb = re.findall('<div class="findSection">(.*?)<div class="findMoreMatches">', html_imdbcode, re.DOTALL)
                                imdbc = re.compile('/title/(.+?)/[?]ref').findall(filmes_imdb[0])
                                imdbcode = imdbc[0]
                                
                        #fanart = artfolder + 'FAN.jpg'
                        if selfAddon.getSetting('movie-fanart-MVT') == "true" and fanart == '':
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
                                if 'Temporada' in titulo[0]: url_pesquisa = 'http://www.themoviedb.org/search/tv?query=' + nome_pesquisa
                                else: url_pesquisa = 'http://www.themoviedb.org/search/movie?query=' + nome_pesquisa
                                if thumb == '' or 's1600' in thumb:
                                        try:
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail: thumb = thumbnail[0].replace('w92','w600')
                                if selfAddon.getSetting('movie-fanart-MVT') == "true":
                                        try:
                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(items_pesquisa[0])
                                                if url_filme_pesquisa:
                                                        url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                        try:
                                                                html_pesquisa = MASH_abrir_url(url_pesquisa)
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
                        if selfAddon.getSetting('movie-fanart-MVT') == "true":
                                if fanart == '': fanart = thumb
                        try:
                                addDir_teste('[COLOR orange]MVT | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + ano[0] + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',url[0].replace(' ','%20')+'IMDB'+imdbcode+'IMDB',103,thumb.replace(' ','%20'),'',fanart,ano[0],'')
                        except: pass
                        a = a + 1
                        i = i + 1
        else: pass
        if items != []:
                proxima_MVT = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
                try:
                        url_MVT = proxima_MVT[0].replace('%3A',':')
                        url_MVT = proxima_MVT[0].replace('&amp;','&')
                except: pass
        else: pass
        #----------------------------------------------------------------------------------------------------
        #x = int(arr_filmes[5])
        sinopse = ''
        for x in range(len(arrai_filmes_anima)):
                conta_os_items = conta_os_items + 1
                addDir(arr_filmes_anima[x],'url',7,arrai_filmes_anima[x][2],sinopse,'')
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "url_FTT": url_FTT, "url_CMT": url_CMT, "fim": 'fim',"xpto":'xpto'}
        url_filmes_animacao = urllib.urlencode(parameters)
        addDir('[COLOR yellow]Página Seguinte >>[/COLOR]',url_filmes_animacao,6,artfolder + 'PSEGUINTE.png','','')




#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#


	
def MASH_abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

#----------------------------------------------------------------------------------------------------------------------------------------------#
              
def MASH_get_params():
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
	liz.setProperty('fanart_image',artfolder + 'FAN.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addLink1(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'FAN.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,checker,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&checker="+urllib.quote_plus(checker)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'FAN.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir1(name,url,mode,iconimage,folder,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'FAN.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
        return ok

def addDir_teste(name,url,mode,iconimage,plot,fanart,year,genre):
        if fanart == '': fanart = artfolder + 'FAN.jpg'
        #text = plot
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&plot="+urllib.quote_plus(plot)+"&year="+urllib.quote_plus(year)+"&genre="+urllib.quote_plus(genre)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',fanart)
        #liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Year": year, "Genre": genre } )
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Year": year, "Genre": genre } )
        #cm = []
	#cm.append(('Sinopse', 'XBMC.Action(Info)'))
	#liz.addContextMenuItems(cm, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok



#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#


          
params=MASH_get_params()
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


