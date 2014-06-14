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



import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket
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
arr_filmes = ['' for i in range(200)]
arrai_filmes = ['' for i in range(200)]
thumb_filmes = ['' for i in range(200)]
arr_filmes[4] = '0'
i=arr_filmes[4]

arr_filmes_anima = []
arrai_filmes_anima = []

progress = xbmcgui.DialogProgress()

#-----------------------------------------------------------------------------------------------------------------------------------------------#



def Filmes_Filmes_Filmes(url):
        a = 1
        percent = 0
        message = ''
        site = ''
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar...'+site, message, "" )
        urlss = urllib.unquote(url)
        print urlss
        urls=re.compile('url_TFC=(.+?)&url_MVT=(.+?)&url_TFV=(.+?)&xpto=xpto&url_TPT=(.+?)&fim=fim').findall(urlss)
        url_TFV = urls[0][2]
        url_TFC = urls[0][0]
        url_MVT = urls[0][1]
        url_TPT = urls[0][3]
        i = int(arr_filmes[4])
        #--------------------------------------------------
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
	num = num + 0.0
	#--------------------------------------------------
        try:
		html_source = MASH_abrir_url(url_TFV)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		num_perc = len(items)*.01
		site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv'
		#addDir(str(num_perc)+'  '+str(len(items)),'',507,artfolder + 'ze-TFV1.png','','')
		for item in items:
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        progress.update(percent, 'A Procurar em '+site, message, "")
                        print str(a) + " de " + str(int(num))
                        xbmc.sleep( 100 )
                        if progress.iscanceled():
                                break
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
                        nome_filme = nome#+'[COLOR orange] | TFV[/COLOR]'
                        nome = nome.replace(' ',"")
                        nome = nome.replace('  ',"")
                        nome = nome.replace('   ',"")
                        if nome not in arr_filmes:
                                arr_filmes[i]=nome
                                arrai_filmes[i]=nome_filme
                                thumb_filmes[i]=thumbnail[0]
                        i = i + 1
                        a = a + 1
        else: pass
        if items != []:
                proxima_TFV = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
                url_TFV = proxima_TFV[0].replace('&amp;','&')
        else: pass
        #----------------------------------------------------------------------------------------------------
        i = 1
        #mensagemprogresso.create('Tuga-Filmes.com', 'A Pesquisar','Por favor aguarde...')
        try:
		html_source = MASH_abrir_url(url_TFC)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
	#addDir(str(len(items)),'url',8,'','nao','')
	#if str(len(items)) > 0:
	if items != []:
		print len(items)
		num_perc = len(items)*.01
		site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].com'
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
                        nome_filme = nome#+'[COLOR orange] | TFC[/COLOR]'
                        nome = nome.replace(' ',"")
                        nome = nome.replace('  ',"")
                        nome = nome.replace('   ',"")
                        if nome not in arr_filmes:
                                if 'ASSISTIR O FILME' in item:
                                        percent = int( ( a / num ) * 100)
                                        message = str(a) + " de " + str(int(num))
                                        progress.update( percent, 'A Procurar em '+site, message, "" )
                                        print str(a) + " de " + str(int(num))
                                        xbmc.sleep( 100 )
                                        if progress.iscanceled():
                                                break
                                        a = a + 1
                                        arr_filmes.insert(i,nome)
                                        arrai_filmes.insert(i,nome_filme)
                                        thumb_filmes.insert(i,thumb)
                        else: arrai_filmes[arr_filmes.index(nome)]=arrai_filmes[arr_filmes.index(nome)]#+'[COLOR orange] | TFC[/COLOR]'
                        i = i + 1
        else: pass
        if items != []:
                proxima_TFC = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
                url_TFC = proxima_TFC[0].replace('&amp;','&')
        else: pass
        #----------------------------------------------------------------------------------------------------
        i = 3
	try:
		html_source = MASH_abrir_url(url_MVT)
	except: html_source = ''
	items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		num_perc = len(items)*.01
		site = '[B][COLOR green]MOVIE[/COLOR][COLOR yellow]-[/COLOR][COLOR red]TUGA[/COLOR][/B]'
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
                        nome = titulo[0] + ' (' + ano[0].replace(' ','') + ')'
                        if 'Dear John' in nome and ano[0] == '2013': nome = nome.replace('Dear John','12 Anos Escravo')
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8230;',"...")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('  '," ")
                        nome_filme = nome#+'[COLOR orange] | MVT[/COLOR]'
                        nome = nome.replace(' ',"")
                        nome = nome.replace('  ',"")
                        nome = nome.replace('   ',"")
                        if nome not in arr_filmes:
                                percent = int( ( a / num ) * 100)
                                message = str(a) + " de " + str(int(num))
                                progress.update( percent, 'A Procurar em '+site, message, "" )
                                print str(a) + " de " + str(int(num))
                                xbmc.sleep( 100 )
                                if progress.iscanceled():
                                        break
                                a = a + 1
                                arr_filmes.insert(i,nome)
                                arrai_filmes.insert(i,nome_filme)
                                thumb_filmes.insert(i,thumbnail.replace('s72-c','s320'))
                        else: arrai_filmes[arr_filmes.index(nome)]=arrai_filmes[arr_filmes.index(nome)]#+'[COLOR orange] | MVT[/COLOR]'
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
        i = 0
        try:
		html_source = MASH_abrir_url(url_TPT)
	except: html_source = ''
	items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		num_perc = len(items)*.01
		site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
		#addDir(str(num_perc)+'  '+str(len(items)),'',507,artfolder + 'ze-TFV1.png','','')
		for item in items:
                        urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(item)
                        if 'title=' in urletitulo[0][0]: urletitulo = re.compile('<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>').findall(item)
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
                        nome = nome + ' (' + ano_filme.replace(' ','') + ') '
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#038;',"&")
                        nome = nome.replace('(PT-PT)',"")
                        nome = nome.replace('(PT/PT)',"")
                        nome = nome.replace('[PT-PT]',"")
                        nome = nome.replace('[PT/PT]',"")
                        nome = nome.replace('  '," ")
                        nome_filme = nome#+'[COLOR orange] | TPT[/COLOR]'
                        nome = nome.replace(' ',"")
                        nome = nome.replace('  ',"")
                        nome = nome.replace('   ',"")
                        if nome not in arr_filmes:
                                percent = int( ( a / num ) * 100)
                                message = str(a) + " de " + str(int(num))
                                progress.update( percent, 'A Procurar em '+site, message, "" )
                                print str(a) + " de " + str(int(num))
                                xbmc.sleep( 100 )
                                if progress.iscanceled():
                                        break
                                a = a + 1
                                arr_filmes.insert(i,nome)
                                arrai_filmes.insert(i,nome_filme)
                                thumb_filmes.insert(i,thumbnail[0].replace('s72-c','s320'))
                        #else: arrai_filmes[arr_filmes.index(nome)]=arrai_filmes[arr_filmes.index(nome)]+'[COLOR orange] | TPT[/COLOR]'
                        i = i + 1
        else: pass
        if items != []:
                #proxima_TPT = re.compile('.*href="(.+?)">Next &rarr;</a>').findall(html_source)
                proxima_TPT = re.compile('</span><a class="nextpostslink" href="(.+?)">&raquo;</a><a class="last"').findall(html_source)
                try:
                        url_TPT = proxima_TPT[0].replace('#038;','').replace('&amp;','&')
                except: pass
        else: pass
        #----------------------------------------------------------------------------------------------------
        #x = int(arr_filmes[5])        
        for x in range(len(arrai_filmes)):
        #for x in range(12):
                if arrai_filmes[x] != '':           #8
                        addDir(arrai_filmes[x],'url',8,thumb_filmes[x],'nao','')
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "fim": 'fim',"xpto":'xpto'}
        url_filmes_filmes = urllib.urlencode(parameters)
        #Filmes_Filmes_Filmes(url_filmes_filmes)
        addDir('[COLOR yellow]Página Seguinte >>[/COLOR]',url_filmes_filmes,507,artfolder + 'filmes.png','','')



def Series_Series(url):
        percent = 0
        message = ''
        site = ''
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar...'+site, message, "" )
        #---------------------------------------------------------------------------
        s = 1
        try:
                html_series_source = MASH_abrir_url(url)
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
	html_items_series = re.findall('<h3 class="widgettitle">SERIES</h3>(.*?)<div id="footer-widgets" class="clearfix">', html_series_source, re.DOTALL)
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
                html_series_source = MASH_abrir_url(url)
        except: html_series_source = ''
	html_items_series = re.findall("<div class=\'widget Label\' id=\'Label3\'>\n<h2>S\xc3\xa9ries(.*?)<div class=\'clear\'>", html_series_source, re.DOTALL)
        i=1
        for item_series in html_items_series:
                series = re.compile("<a dir=\'ltr\' href=\'(.+?)\'>(.+?)</a>").findall(item_series)
                for endereco_series,nome_series in series:
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(s)
                        progress.update( percent, 'A Procurar em '+site, message, "" )
                        print str(i) + " de " + str(s)
                        if selfAddon.getSetting('series-thumb-mashup') == "false": xbmc.sleep( 50 )
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
                        if selfAddon.getSetting('series-thumb-mashup') == "true":
                                try:
                                        html_source = MASH_abrir_url(endereco_series)
                                except: html_source = ''
                                items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
                                if items != []:
                                        thumbnail = re.compile('src="(.+?)"').findall(items[0])
                                        if thumbnail : thumb = thumbnail[0]
                        else: thumb = artfolder + 'series.png'
                        arr_series[i]=nome_series
                        arrai_series[i]=nome_series+'[COLOR orange] \/ TFV[/COLOR]'+'|'+thumb+'|'+endereco_series
                        i=i+1
        url = 'http://toppt.net/'
        site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
        try:
                html_series_source = MASH_abrir_url(url)
        except: html_series_source = ''
	html_items_series = re.findall('<h3 class="widgettitle">SERIES</h3>(.*?)<div id="footer-widgets" class="clearfix">', html_series_source, re.DOTALL)
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
                        if selfAddon.getSetting('series-thumb-mashup') == "true":
                                try:
                                        html_source = MASH_abrir_url(endereco_series)
                                except: html_source = ''
                                items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
                                if items != []:
                                        thumbnail = re.compile('src="(.+?)"').findall(items[0])
                                        if thumbnail : thumb = thumbnail[0]
                        else: thumb = artfolder + 'series.png'
                        if nome_series in arr_series:
                                arrai_series[arr_series.index(nome_series)]=arrai_series[arr_series.index(nome_series)].replace('[COLOR orange] \/ TFV[/COLOR]','[COLOR orange] \/ TFV \/ TPT[/COLOR]')
                                arrai_series[arr_series.index(nome_series)]=arrai_series[arr_series.index(nome_series)]+'|'+endereco_series
                        if nome_series not in arr_series:
                                percent = int( ( i / num ) * 100)
                                message = str(i) + " de " + str(s)
                                progress.update( percent, 'A Procurar em '+site, message, "" )
                                print str(i) + " de " + str(s)
                                if selfAddon.getSetting('series-thumb-mashup') == "false": xbmc.sleep( 50 )
                                if progress.iscanceled():
                                        break
                                arr_series[i]=nome_series
                                arrai_series[i]=nome_series+'[COLOR orange] \/ TPT[/COLOR]'+'|'+thumb+'|'+endereco_series
                                i=i+1
        if selfAddon.getSetting('series-thumb-mashup') == "false":
                addDir1('[B][COLOR blue]Séries[/COLOR][/B] (' + str(i) + ')','','',artfolder + 'series.png',False,'')
                addDir1('','','',artfolder + 'series.png',False,'')
        arrai_series.sort()
        for x in range(len(arrai_series)):
                if arrai_series[x] != '':
                        _s = re.compile('(.+?)[|](.+?)[|](.+?)[|](.*)').findall(arrai_series[x])
                        if _s: addDir(_s[0][0].replace('\/','|'),_s[0][2]+'|'+_s[0][3],9,_s[0][1],'nao','')
                        else:
                                _s = re.compile('(.+?)[|](.+?)[|](.*)').findall(arrai_series[x])
                                addDir(_s[0][0].replace('\/','|'),_s[0][2],9,_s[0][1],'nao','')



def Filmes_Animacao(url):
        a = 1
        percent = 0
        message = ''
        site = ''
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar...'+site, message, "" )
        urlss = urllib.unquote(url)
        print urlss
        urls=re.compile('url_TFC=(.+?)&url_MVT=(.+?)&url_TFV=(.+?)&xpto=xpto&url_TPT=(.+?)&fim=fim').findall(urlss)
        url_TFV = urls[0][2]
        url_TFC = urls[0][0]
        url_MVT = urls[0][1]
        url_TPT = urls[0][3]
        i = int(arr_filmes[4])
        #--------------------------------------------------
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
	num = num + 0.0
	#--------------------------------------------------
	site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv'
        try:
		html_source = MASH_abrir_url(url_TFV)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        progress.update( percent, 'A Procurar em '+site, message, "" )
                        print str(a) + " de " + str(int(num))
                        xbmc.sleep( 100 )
                        if progress.iscanceled():
                                break
                        urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)
                        ano = re.compile("<b>Ano</b>: (.+?)<br />").findall(item)
                        if not ano: ano = ''
                        thumbnail = re.compile('src="(.+?)"').findall(item)
                        print urletitulo,thumbnail
                        nome = urletitulo[0][1]
                        endereco_filme = urletitulo[0][0]
                        thumb = thumbnail[0]
                        if ano:
                                a_q = re.compile('\d+')
                                qq_aa = a_q.findall(nome)
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) == 4:
                                                tirar_ano = '(' + str(q_a_q_a) + ')'
                                                nome = nome.replace(tirar_ano,'')
                        nome = nome+' ('+ano[0].replace(' ','')+')'
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8230;',"...")
                        nome = nome.replace('  '," ")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.lower()
                        nome = nome.title()
                        nome_filme = nome
                        #nome = 'TFV - '+nome
                        #nome = nome.replace(' ',"")
                        #nome = nome.replace('  ',"")
                        #nome = nome.replace('   ',"")
                        if nome not in arr_filmes_anima:
                                arr_filmes_anima.append(nome)
                                arrai_filmes_anima.append((nome_filme,endereco_filme,thumb))
                                #thumb_filmes[i]=thumbnail[0]
                        i = i + 1
                        a = a + 1
        else: pass
        if items != []:
                proxima_TFV = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
                url_TFV = proxima_TFV[0].replace('&amp;','&')
        else: pass
        #----------------------------------------------------------------------------------------------------
        i = 1
        site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].com'
        try:
		html_source = MASH_abrir_url(url_TFC)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        nao = 0
			urletitulo = re.compile("<a href=\'(.+?)\' title=\'(.+?)\'>").findall(item)
			ano = re.compile('<b>VERS\xc3\x83O:.+?</b><span style="font-size: x-small;">(.+?)<').findall(item)
			thumbnail = re.compile('<img alt="" border="0" src="(.+?)"').findall(item)
			print urletitulo,thumbnail
			endereco_filme = urletitulo[0][0]
			thumb = thumbnail[0]
			if ano != []:
                                for q_a in ano:
                                        a_q = re.compile('\d+')
                                        qq_aa = a_q.findall(q_a)
                                        for q_a_q_a in qq_aa:
                                                if len(q_a_q_a) == 4:
                                                        ano = ' (' + q_a_q_a + ')'
                        if len(ano) < 4: ano = ''
			nome = urletitulo[0][1] + ' '+ano.replace(' ','')
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8230;',"...")
                        nome = nome.replace('  '," ")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.lower()
                        nome = nome.title()
                        nome_filme = nome
                        #nome = 'TFC - '+nome
                        #nome = nome.replace(' ',"")
                        #nome = nome.replace('  ',"")
                        #nome = nome.replace('   ',"")
                        if nome not in arr_filmes_anima:
                                if 'ASSISTIR O FILME' in item:
                                        percent = int( ( a / num ) * 100)
                                        message = str(a) + " de " + str(int(num))
                                        progress.update( percent, 'A Procurar em '+site, message, "" )
                                        print str(a) + " de " + str(int(num))
                                        xbmc.sleep( 100 )
                                        if progress.iscanceled():
                                                break
                                        a = a + 1
                                        arr_filmes_anima.insert(i,nome)
                                        arrai_filmes_anima.insert(i,(nome_filme,endereco_filme,thumb))
                        #else: arrai_filmes[arr_filmes.index(nome)]=arrai_filmes[arr_filmes.index(nome)]+'/TFC
                        i = i + 1
        else: pass
        if items != []:
                proxima_TFC = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
                url_TFC = proxima_TFC[0].replace('&amp;','&')
        else: pass
        #----------------------------------------------------------------------------------------------------
        i = 3
        site = '[B][COLOR green]MOVIE[/COLOR][COLOR yellow]-[/COLOR][COLOR red]TUGA[/COLOR][/B]'
	try:
		html_source = MASH_abrir_url(url_MVT)
	except: html_source = ''
	items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        nao = 0
			url = re.compile('<div class="btns"><a href="(.+?)" target="Player">').findall(item)
			if 'http' not in url[0]:
                                url = 'http:' + url[0]
                                endereco_filme = url
                        else: endereco_filme = url[0]
                        titulo = re.compile("<div id='titulosingle'><h3>(.+?)</h3></div>").findall(item)
                        if not titulo: titulo = re.compile("<strong>T\xc3\xadtulo original:</strong>(.+?)</div>").findall(item)
                        ano = re.compile('<strong>Lan\xc3\xa7amento:</strong>(.+?)</div>').findall(item)
                        thumb = re.compile('src="(.+?)"').findall(item)
                        if 'http' not in thumb[0]:
                                thumbnail = 'http:' + thumb[0].replace('s72-c','s320')
                        else: thumbnail = thumb[0].replace('s72-c','s320')
                        nome = titulo[0] + ' (' + ano[0].replace(' ','') + ')'
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('PT-PT',"")
                        nome = nome.replace('PT',"")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8230;',"...")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('  '," ")
                        nome = nome.lower()
                        nome = nome.title()
                        nome_filme = nome
                        #nome = 'MVT - '+nome
                        #nome = nome.replace(' ',"")
                        #nome = nome.replace('  ',"")
                        #nome = nome.replace('   ',"")
                        if nome not in arr_filmes_anima:
                                percent = int( ( a / num ) * 100)
                                message = str(a) + " de " + str(int(num))
                                progress.update( percent, 'A Procurar em '+site, message, "" )
                                print str(a) + " de " + str(int(num))
                                xbmc.sleep( 100 )
                                if progress.iscanceled():
                                        break
                                a = a + 1
                                arr_filmes_anima.insert(i,nome)
                                arrai_filmes_anima.insert(i,(nome_filme,endereco_filme,thumbnail))
                        #else: arrai_filmes[arr_filmes.index(nome)]=arrai_filmes[arr_filmes.index(nome)]+'/MVT'
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
        i = 0
        site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
        try:
		html_source = MASH_abrir_url(url_TPT)
	except: html_source = ''
	items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        nao = 0
                        urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(item)
                        if 'title=' in urletitulo[0][0]: urletitulo = re.compile('<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>').findall(item)
                        if '[' in urletitulo[0][1] and not ('PT' in urletitulo[0][1] or 'Tri' in urletitulo[0][1] or 'Qua' in urletitulo[0][1]):
                                urletitulo = re.compile('[[](.+?)[]]').findall(urletitulo[0][1])
                                nome = urletitulo[0]
                        else: nome = urletitulo[0][1]
                        ano = re.compile("<b>ANO:.+?/b>(.+?)<br/>").findall(item)
                        thumbnail = re.compile('src="(.+?)"').findall(item)
                        print urletitulo,thumbnail
                        endereco_filme = urletitulo[0][0]
			thumb = thumbnail[0].replace('s72-c','s320')
                        if not ano:
                                ano = re.compile("\nANO:\xc2\xa0(.+?)<br/>").findall(item)
                                if ano:
                                        ano_filme = ano[0]
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
                        nome = nome + ' (' + ano_filme + ')'
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#038;',"&")
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
                        nome = nome.lower()
                        nome = nome.title()
                        #nome = 'TPT - '+nome
                        nome_filme = nome
                        #nome = nome.replace(' ',"")
                        #nome = nome.replace('  ',"")
                        #nome = nome.replace('   ',"")
                        try:
                                a=arr_filmes_anima.index('TPT - Rio 2')
                                if a>0:addDir(str(a),'url',7,'','','')
                        except: pass
                        if nome not in arr_filmes_anima:
                                percent = int( ( a / num ) * 100)
                                message = str(a) + " de " + str(int(num))
                                progress.update( percent, 'A Procurar em '+site, message, "" )
                                print str(a) + " de " + str(int(num))
                                xbmc.sleep( 100 )
                                if progress.iscanceled():
                                        break
                                a = a + 1
                                arr_filmes_anima.insert(i,nome)
                                arrai_filmes_anima.insert(i,(nome_filme,endereco_filme,thumb))
                        #else: arrai_filmes[arr_filmes.index(nome)]=arrai_filmes[arr_filmes.index(nome)]+'/TPT'
                        i = i + 1
                        nome_exp = 'TPT - O Filme Lego'
                        if nome_exp in arr_filmes_anima: addDir(str(arr_filmes_anima.index(nome_exp)),'url',7,'','','')
        else: pass
        if items != []:
                #proxima_TPT = re.compile('.*href="(.+?)">Next &rarr;</a>').findall(html_source)
                proxima_TPT = re.compile('</span><a class="nextpostslink" href="(.+?)">&raquo;</a><a class="last"').findall(html_source)
                try:
                        url_TPT = proxima_TPT[0].replace('#038;','').replace('&amp;','&')
                except: pass
        else: pass
        #----------------------------------------------------------------------------------------------------
        #x = int(arr_filmes[5])
        sinopse = ''
        for x in range(len(arrai_filmes_anima)):
                addDir(arr_filmes_anima[x],'url',7,arrai_filmes_anima[x][2],sinopse,'')
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "fim": 'fim',"xpto":'xpto'}
        url_filmes_animacao = urllib.urlencode(parameters)
        addDir('[COLOR yellow]Página Seguinte >>[/COLOR]',url_filmes_animacao,6,artfolder + 'animacao.png','','')




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


