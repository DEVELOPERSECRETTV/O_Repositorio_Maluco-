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
from array import array
from string import capwords


addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

arr_series1 = [['' for i in range(87)] for j in range(1)]
arr_series = ['' for i in range(100)]
arr_filmes = ['' for i in range(100)]
arrai_filmes = ['' for i in range(100)]
thumb_filmes = ['' for i in range(100)]
arr_filmes[4] = '0'
i=arr_filmes[4] 



#-----------------------------------------------------------------------------------------------------------------------------------------------#



def Filmes_Filmes_Filmes(url):
        #xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        #xbmc.executebuiltin("Container.SetViewMode(504)")
        conta_items = 1
        if conta_items == 1:      
                mensagemprogresso = xbmcgui.DialogProgress()
                mensagemprogresso.create('Filmes', 'A Pesquisar','Por favor aguarde...')
                mensagemprogresso.update(0)
        urlss = urllib.unquote(url)
        print urlss
        urls=re.compile('url_TFC=(.+?)&url_MVT=(.+?)&url_TFV=(.+?)&xpto=xpto&url_TPT=(.+?)&fim=fim').findall(urlss)
        url_TFV = urls[0][2]
        url_TFC = urls[0][0]
        url_MVT = urls[0][1]
        url_TPT = urls[0][3]
        i = int(arr_filmes[4])
        try:
		html_source = MASH_abrir_url(url_TFV)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		num_perc = len(items)*.01
		#addDir(str(num_perc)+'  '+str(len(items)),'',507,artfolder + 'ze-TFV1.png','','')
		for item in items:
                        urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)
                        ano = re.compile("<b>Ano</b>: (.+?)<br />").findall(item)
                        if not ano: ano = ''
                        thumbnail = re.compile('src="(.+?)"').findall(item)
                        if 'width' in thumbnail[0]:
                                thumb = re.compile('(.+?) width.+?').findall(thumbnail[0])
                                thumbnail[0] = thumb[0]
                        print urletitulo,thumbnail
                        nome = urletitulo[0][1]
                        if ano:
                                a_q = re.compile('\d+')
                                qq_aa = a_q.findall(nome)
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) == 4:
                                                tirar_ano = '(' + str(q_a_q_a) + ')'
                                                nome = nome.replace(tirar_ano,'')
                        nome = nome+' ('+ano[0]+')'
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8230;',"...")
                        nome = nome.replace('  '," ")
                        nome = nome.replace('&#8211;',"-")
                        nome_filme = nome
                        nome = nome.replace(' ',"")
                        nome = nome.replace('  ',"")
                        nome = nome.replace('   ',"")
                        if nome not in arr_filmes:
                                arr_filmes[i]=nome
                                arrai_filmes[i]=nome_filme
                                thumb_filmes[i]=thumbnail[0]
                        i = i + 1
                        conta_items = conta_items + 1   
                        if conta_items == 10:      
                                mensagemprogresso.update(10)
                        if conta_items == 20:
                                mensagemprogresso.update(20)
        proxima_TFV = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
        url_TFV = proxima_TFV[0].replace('&amp;','&')        
        #----------------------------------------------------------------------------------------------------
        i = 1
        #mensagemprogresso.create('Tuga-Filmes.com', 'A Pesquisar','Por favor aguarde...')
        try:
		html_source = MASH_abrir_url(url_TFC)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		num_perc = len(items)*.01
		#addDir(str(num_perc)+'  '+str(len(items)),'',507,artfolder + 'ze-TFV1.png','','')
		for item in items:
			urletitulo = re.compile("<a href=\'(.+?)\' title=\'(.+?)\'>").findall(item)
			ano = re.compile('<b>VERS\xc3\x83O:.+?</b><span style="font-size: x-small;">(.+?)<').findall(item)
			thumbnail = re.compile('<img alt="" border="0" src="(.+?)"').findall(item)
			if thumbnail: thumb = thumbnail[0]
			else: thumb = ''
			print urletitulo,thumbnail
			if ano != []:
                                for q_a in ano:
                                        a_q = re.compile('\d+')
                                        qq_aa = a_q.findall(q_a)
                                        for q_a_q_a in qq_aa:
                                                if len(q_a_q_a) == 4:
                                                        ano = ' (' + q_a_q_a + ')'
                        if len(ano) < 4: ano = ''
			nome = urletitulo[0][1] + ano
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8230;',"...")
                        nome = nome.replace('  '," ")
                        nome = nome.replace('&#8211;',"-")
                        nome_filme = nome
                        nome = nome.replace(' ',"")
                        nome = nome.replace('  ',"")
                        nome = nome.replace('   ',"")
                        if nome not in arr_filmes:
                                arr_filmes.insert(i,nome)
                                arrai_filmes.insert(i,nome_filme)
                                thumb_filmes.insert(i,thumb)
                        #else: arrai_filmes[arr_filmes.index(nome)]=arrai_filmes[arr_filmes.index(nome)]+'/TFC
                        i = i + 1
                        conta_items = conta_items + 1
                        if conta_items == 30:
                                mensagemprogresso.update(30)
                        if conta_items == 38:
                                mensagemprogresso.update(40)
        proxima_TFC = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
        url_TFC = proxima_TFC[0].replace('&amp;','&')
        #----------------------------------------------------------------------------------------------------
        i = 3
	try:
		html_source = MASH_abrir_url(url_MVT)
	except: html_source = ''
	items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		num_perc = len(items)*.01
		#addDir(str(num_perc)+'  '+str(len(items)),'',507,artfolder + 'ze-TFV1.png','','')
		for item in items:
			url = re.compile('<div class="btns"><a href="(.+?)" target="Player">').findall(item)
			if 'http' not in url[0]:
                                url = 'http:' + url[0] 
                        titulo = re.compile("<strong>T\xc3\xadtulo original:</strong>(.+?)</div>").findall(item)
                        ano = re.compile('<strong>Lan\xc3\xa7amento:</strong>(.+?)</div>').findall(item)
                        thumb = re.compile('src="(.+?)"').findall(item)
                        if 'http' not in thumb[0]:
                                thumbnail = 'http:' + thumb[0]
                        else: thumbnail = thumb[0]
                        nome = titulo[0] + ' (' + ano[0] + ')'
                        if 'Dear John' in nome and ano[0] == '2013': nome = nome.replace('Dear John','12 Anos Escravo')
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8230;',"...")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('  '," ")
                        nome_filme = nome
                        nome = nome.replace(' ',"")
                        nome = nome.replace('  ',"")
                        nome = nome.replace('   ',"")
                        if nome not in arr_filmes:
                                arr_filmes.insert(i,nome)
                                arrai_filmes.insert(i,nome_filme)
                                thumb_filmes.insert(i,thumbnail.replace('s72-c','s320'))
                        #else: arrai_filmes[arr_filmes.index(nome)]=arrai_filmes[arr_filmes.index(nome)]+'/MVT'
                        i = i + 1
                        conta_items = conta_items + 1
                        if conta_items == 40:
                                mensagemprogresso.update(50)
                        if conta_items == 48:
                                mensagemprogresso.update(60)
        proxima_MVT = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
	try:
                url_MVT = proxima_MVT[0].replace('%3A',':')
                url_MVT = proxima_MVT[0].replace('&amp;','&')
	except: pass
        #----------------------------------------------------------------------------------------------------
        i = 0
        try:
		html_source = MASH_abrir_url(url_TPT)
	except: html_source = ''
	items = re.findall('<h1 class="entry-title">(.*?)</article>', html_source, re.DOTALL)
	if items != []:
		print len(items)
		num_perc = len(items)*.01
		#addDir(str(num_perc)+'  '+str(len(items)),'',507,artfolder + 'ze-TFV1.png','','')
		for item in items:
                        urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(item)
                        if '[' in urletitulo[0][1] and not ('PT' in urletitulo[0][1] or 'Tri' in urletitulo[0][1] or 'Qua' in urletitulo[0][1]):
                                urletitulo = re.compile('[[](.+?)[]]').findall(urletitulo[0][1])
                                nome = urletitulo[0]
                        else: nome = urletitulo[0][1]
                        #if '[' in urletitulo[0][1]: urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)[[].+?</a>').findall(item)
                        ano = re.compile("<b>ANO:.+?/b>(.+?)<br/>").findall(item)
                        thumbnail = re.compile('src="(.+?)"').findall(item)
                        print urletitulo,thumbnail
                        #nome = urletitulo[0][1]
                        if not ano:
                                ano = re.compile("\nANO:\xc2\xa0(.+?)<br/>").findall(item)
                                if ano:
                                        ano_filme = ': ' + ano[0]
                                else:
                                        ano_filme = ''     
                        if ano:
                                ano_filme = ano[0]
                                a_q = re.compile('\d+')
                                qq_aa = a_q.findall(nome)
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) == 4:
                                                tirar_ano = '(' + str(q_a_q_a) + ')'
                                                nome = nome.replace(tirar_ano,'')
                        nome = nome + ' (' + ano_filme + ') '
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('(PT-PT)',"")
                        nome = nome.replace('(PT/PT)',"")
                        nome = nome.replace('[PT-PT]',"")
                        nome = nome.replace('[PT/PT]',"")
                        nome = nome.replace('  '," ")
                        nome_filme = nome
                        nome = nome.replace(' ',"")
                        nome = nome.replace('  ',"")
                        nome = nome.replace('   ',"")
                        if nome not in arr_filmes:
                                arr_filmes.insert(i,nome)
                                arrai_filmes.insert(i,nome_filme)
                                thumb_filmes.insert(i,thumbnail[0].replace('s72-c','s320'))
                        #else: arrai_filmes[arr_filmes.index(nome)]=arrai_filmes[arr_filmes.index(nome)]+'/TPT'
                        i = i + 1
                        conta_items = conta_items + 1
                        if conta_items == 58:
                                mensagemprogresso.update(70)
                        if conta_items == 68:
                                mensagemprogresso.update(80)
        proxima_TPT = re.compile('.*href="(.+?)">Next &rarr;</a>').findall(html_source)
        try:
                url_TPT = proxima_TPT[0].replace('#038;','')
        except: pass
        #----------------------------------------------------------------------------------------------------
        mensagemprogresso.update(100)
        mensagemprogresso.close()
        #x = int(arr_filmes[5])        
        for x in range(len(arrai_filmes)):
        #for x in range(12):
                if arrai_filmes[x] != '':
                        addDir(arrai_filmes[x],'url',8,thumb_filmes[x],'nao','')
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "fim": 'fim',"xpto":'xpto'}
        url_filmes_filmes = urllib.urlencode(parameters)
        addDir('[COLOR yellow]Página Seguinte >>[/COLOR]',url_filmes_filmes,507,artfolder + 'ze-TFV1.png','','')



def Series_Series(url):
        html_series_source = MASH_abrir_url(url)
	html_items_series = re.findall("<div class=\'widget Label\' id=\'Label3\'>\n<h2>S\xc3\xa9ries(.*?)<div class=\'clear\'>", html_series_source, re.DOTALL)
        print len(html_items_series)
        i=0
        for item_series in html_items_series:
                series = re.compile("<a dir=\'ltr\' href=\'(.+?)\'>(.+?)</a>").findall(item_series)
                for endereco_series,nome_series in series:
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        nome_series = nome_series.replace('&#8217;',"'")
                        nome_series = nome_series.replace('&#8230;',"...")
                        if nome_series != 'Agents of S.H.I.E.L.D':
                                arr_series[i]=nome_series
                                i=i+1
                        #arr_series[6][1]=endereco_series
                        #addDir(nome_series,endereco_series,47,artfolder + 'ze-TFV1.png','nao','')
        url = 'http://toppt.net/'
        html_series_source = MASH_abrir_url(url)
	html_items_series = re.findall('<h1 class="widget-title">SERIES</h1>(.+?)</div></aside>', html_series_source, re.DOTALL)
        print len(html_items_series)
        for item_series in html_items_series:
                series = re.compile('<a href="(.+?)">(.+?)</a>').findall(item_series)
                for endereco_series,nome_series in series:
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        nome_series = nome_series.replace('&#8217;',"'")
                        nome_series = nome_series.replace('&#8230;',"...")
                        nome_series = nome_series.replace('&#8211;',"-")
                        if (nome_series not in arr_series) and (nome_series != 'Da Vincis Demons'):
                                arr_series.append(nome_series)
                                i=i+1
        arr_series.sort(key = lambda k : k.lower())
        addDir1('[B][COLOR blue]Séries[/COLOR][/B] (' + str(i) + ')','','',artfolder + 'ze-TFV1.png',False,'')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
        for x in range(len(arr_series)):
                if arr_series[x] != '': addDir(arr_series[x],'url',9,artfolder + 'ze-TFV1.png','nao','')
        xbmcplugin.setContent(int(sys.argv[1]), 'TvShows')
        xbmc.executebuiltin("Container.SetViewMode(551)")


def Filmes_Animacao(url):
        conta_items = 1
        if conta_items == 1:      
                mensagemprogresso = xbmcgui.DialogProgress()
                mensagemprogresso.create('Animação', 'A Pesquisar','Por favor aguarde...')
                mensagemprogresso.update(0)
        urlss = urllib.unquote(url)
        print urlss
        urls=re.compile('url_TFC=(.+?)&url_MVT=(.+?)&url_TFV=(.+?)&xpto=xpto&url_TPT=(.+?)&fim=fim').findall(urlss)
        url_TFV = urls[0][2]
        url_TFC = urls[0][0]
        url_MVT = urls[0][1]
        url_TPT = urls[0][3]
        i = int(arr_filmes[4])
        try:
		html_source = MASH_abrir_url(url_TFV)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)
                        ano = re.compile("<b>Ano</b>: (.+?)<br />").findall(item)
                        if not ano: ano = ''
                        thumbnail = re.compile('src="(.+?)"').findall(item)
                        print urletitulo,thumbnail
                        nome = urletitulo[0][1]
                        if ano:
                                a_q = re.compile('\d+')
                                qq_aa = a_q.findall(nome)
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) == 4:
                                                tirar_ano = '(' + str(q_a_q_a) + ')'
                                                nome = nome.replace(tirar_ano,'')
                        nome = nome+' ('+ano[0]+')'
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8230;',"...")
                        nome = nome.replace('  '," ")
                        nome = nome.replace('&#8211;',"-")
                        nome_filme = nome
                        nome = nome.replace(' ',"")
                        nome = nome.replace('  ',"")
                        nome = nome.replace('   ',"")
                        if nome not in arr_filmes:
                                arr_filmes[i]=nome
                                arrai_filmes[i]=nome_filme
                                thumb_filmes[i]=thumbnail[0]
                        i = i + 1
                        conta_items = conta_items + 1   
                        if conta_items == 10:      
                                mensagemprogresso.update(10)
                        if conta_items == 20:
                                mensagemprogresso.update(20)
        proxima_TFV = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
        url_TFV = proxima_TFV[0].replace('&amp;','&')        
        #----------------------------------------------------------------------------------------------------
        i = 1
        try:
		html_source = MASH_abrir_url(url_TFC)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
			urletitulo = re.compile("<a href=\'(.+?)\' title=\'(.+?)\'>").findall(item)
			ano = re.compile('<b>VERS\xc3\x83O:.+?</b><span style="font-size: x-small;">(.+?)<').findall(item)
			thumbnail = re.compile('<img alt="" border="0" src="(.+?)"').findall(item)
			print urletitulo,thumbnail
			if ano != []:
                                for q_a in ano:
                                        a_q = re.compile('\d+')
                                        qq_aa = a_q.findall(q_a)
                                        for q_a_q_a in qq_aa:
                                                if len(q_a_q_a) == 4:
                                                        ano = ' (' + q_a_q_a + ')'
                        if len(ano) < 4: ano = ''
			nome = urletitulo[0][1] + ano
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8230;',"...")
                        nome = nome.replace('  '," ")
                        nome = nome.replace('&#8211;',"-")
                        nome_filme = nome
                        nome = nome.replace(' ',"")
                        nome = nome.replace('  ',"")
                        nome = nome.replace('   ',"")
                        if nome not in arr_filmes:
                                arr_filmes.insert(i,nome)
                                arrai_filmes.insert(i,nome_filme)
                                thumb_filmes.insert(i,thumbnail[0])
                        #else: arrai_filmes[arr_filmes.index(nome)]=arrai_filmes[arr_filmes.index(nome)]+'/TFC
                        i = i + 1
                        conta_items = conta_items + 1
                        if conta_items == 30:
                                mensagemprogresso.update(30)
                        if conta_items == 38:
                                mensagemprogresso.update(40)
        proxima_TFC = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
        url_TFC = proxima_TFC[0].replace('&amp;','&')
        #----------------------------------------------------------------------------------------------------
        i = 3
	try:
		html_source = MASH_abrir_url(url_MVT)
	except: html_source = ''
	items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
			url = re.compile('<div class="btns"><a href="(.+?)" target="Player">').findall(item)
			if 'http' not in url[0]:
                                url = 'http:' + url[0] 
                        titulo = re.compile("<strong>T\xc3\xadtulo original:</strong>(.+?)</div>").findall(item)
                        ano = re.compile('<strong>Lan\xc3\xa7amento:</strong>(.+?)</div>').findall(item)
                        thumb = re.compile('src="(.+?)"').findall(item)
                        if 'http' not in thumb[0]:
                                thumbnail = 'http:' + thumb[0]
                        else: thumbnail = thumb[0]
                        nome = titulo[0] + ' (' + ano[0] + ')'
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('PT-PT',"")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8230;',"...")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('  '," ")
                        nome_filme = nome
                        nome = nome.replace(' ',"")
                        nome = nome.replace('  ',"")
                        nome = nome.replace('   ',"")
                        if nome not in arr_filmes:
                                arr_filmes.insert(i,nome)
                                arrai_filmes.insert(i,nome_filme)
                                thumb_filmes.insert(i,thumbnail.replace('s72-c','s320'))
                        #else: arrai_filmes[arr_filmes.index(nome)]=arrai_filmes[arr_filmes.index(nome)]+'/MVT'
                        i = i + 1
                        conta_items = conta_items + 1
                        if conta_items == 40:
                                mensagemprogresso.update(50)
                        if conta_items == 48:
                                mensagemprogresso.update(60)
        proxima_MVT = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
	try:
                url_MVT = proxima_MVT[0].replace('%3A',':')
                url_MVT = proxima_MVT[0].replace('&amp;','&')
	except: pass
        #----------------------------------------------------------------------------------------------------
        i = 0
        try:
		html_source = MASH_abrir_url(url_TPT)
	except: html_source = ''
	items = re.findall('<h1 class="entry-title">(.*?)</article>', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(item)
                        if '[' in urletitulo[0][1] and not ('PT' in urletitulo[0][1] or 'Tri' in urletitulo[0][1] or 'Qua' in urletitulo[0][1]):
                                urletitulo = re.compile('[[](.+?)[]]').findall(urletitulo[0][1])
                                nome = urletitulo[0]
                        else: nome = urletitulo[0][1]
                        ano = re.compile("<b>ANO:.+?/b>(.+?)<br/>").findall(item)
                        thumbnail = re.compile('src="(.+?)"').findall(item)
                        print urletitulo,thumbnail
                        if not ano:
                                ano = re.compile("\nANO:\xc2\xa0(.+?)<br/>").findall(item)
                                if ano:
                                        ano_filme = ano[0]
                                else:
                                        ano_filme = ''     
                        if ano:
                                ano_filme = ano[0]
                                a_q = re.compile('\d+')
                                qq_aa = a_q.findall(nome)
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) == 4:
                                                tirar_ano = '(' + str(q_a_q_a) + ')'
                                                nome = nome.replace(tirar_ano,'')
                        nome = nome + ' (' + ano_filme + ')'
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('(PT-PT)',"")
                        nome = nome.replace('(PT/PT)',"")
                        nome = nome.replace('[PT-PT]',"")
                        nome = nome.replace('[PT/PT]',"")
                        nome = nome.replace('  '," ")
                        nome_filme = nome
                        nome = nome.replace(' ',"")
                        nome = nome.replace('  ',"")
                        nome = nome.replace('   ',"")
                        if nome not in arr_filmes:
                                arr_filmes.insert(i,nome)
                                arrai_filmes.insert(i,nome_filme)
                                thumb_filmes.insert(i,thumbnail[0].replace('s72-c','s320'))
                        #else: arrai_filmes[arr_filmes.index(nome)]=arrai_filmes[arr_filmes.index(nome)]+'/TPT'
                        i = i + 1
                        conta_items = conta_items + 1
                        if conta_items == 58:
                                mensagemprogresso.update(70)
                        if conta_items == 68:
                                mensagemprogresso.update(80)
        proxima_TPT = re.compile('.*href="(.+?)">Next &rarr;</a>').findall(html_source)
        try:
                url_TPT = proxima_TPT[0].replace('#038;','')
        except: pass
        #----------------------------------------------------------------------------------------------------
        #x = int(arr_filmes[5])
        sinopse = 'teste ahahahahaha'
        for x in range(len(arrai_filmes)):
        #for x in range(12):
                if arrai_filmes[x] != '':
                        addDir(arrai_filmes[x],'url',7,thumb_filmes[x],sinopse,'')
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "fim": 'fim',"xpto":'xpto'}
        url_filmes_animacao = urllib.urlencode(parameters)
        addDir('[COLOR yellow]Página Seguinte >>[/COLOR]',url_filmes_animacao,6,artfolder + 'ze-TFV1.png','','')
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        xbmc.executebuiltin("Container.SetViewMode(50)")



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


