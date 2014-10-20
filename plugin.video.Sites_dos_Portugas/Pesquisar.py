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



import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,time,os


addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

 
#mensagemprogresso = xbmcgui.Dialog().ok
	
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def pesquisar():
	keyb = xbmc.Keyboard('', 'Escreva o parâmetro de pesquisa')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		pesquisou = search
                #nome_pesquisa = nome_pesquisa.replace("'",'')
                a_q = re.compile('\w+')
                qq_aa = a_q.findall(search)
                search = ''
                conta = 0
                for q_a_q_a in qq_aa:
                        if len(q_a_q_a) > 2 or q_a_q_a == '1' or q_a_q_a == '2' or q_a_q_a == '3':
                        #if len(q_a_q_a) > 2:
                                if conta == 0:
                                        search = q_a_q_a
                                        conta = 1
                                else: search = search + '+' + q_a_q_a
		encode=urllib.quote(search)
		progress = xbmcgui.DialogProgress()
		a = 1
                percent = 0
                message = ''
                site = ''
                progress.create('Progresso', 'A Procurar')
                progress.update( percent, 'A Procurar...'+site, message, "" )
                xbmc.sleep( 500 )
		a = 0
                site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv'
                percent = int( ( a / 6.0 ) * 100)
                message = ''
                progress.update(percent, 'A Procurar em '+site, message, "")
                print str(a) + " de " + str(int(a))
                xbmc.sleep( 100 )
		url_pesquisa = 'http://www.tuga-filmes.us/search?q=' + str(encode)
		encontrar_fontes_pesquisa_TFV(url_pesquisa,pesquisou)
		a= 1
                site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].com'
                percent = int( ( a / 6.0 ) * 100)
                message = ''
                progress.update(percent, 'A Procurar em '+site, message, "")
                print str(a) + " de " + str(int(a))
                xbmc.sleep( 100 )
		url_pesquisa = 'http://www.tuga-filmes.info/search?q=' + str(encode)
		encontrar_fontes_filmes_TFC(url_pesquisa)
		a = 2
                site = '[B][COLOR green]MOVIE[/COLOR][COLOR yellow]-[/COLOR][COLOR red]TUGA[/COLOR][/B]'
                percent = int( ( a / 6.0 ) * 100)
                message = ''
                progress.update(percent, 'A Procurar em '+site, message, "")
                print str(a) + " de " + str(int(a))
                xbmc.sleep( 100 )
		url_pesquisa = 'http://www.movie-tuga.blogspot.pt/search?q=' + str(encode)
		encontrar_fontes_pesquisa_MVT(url_pesquisa)
		a = 3
                site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
                percent = int( ( a / 6.0 ) * 100)
                message = ''
                progress.update(percent, 'A Procurar em '+site, message, "")
                print str(a) + " de " + str(int(a))
                xbmc.sleep( 100 )
		url_pesquisa = 'http://toppt.net/?s=' + str(encode)
		encontrar_fontes_filmes_TPT(url_pesquisa)

                a = 4
                site = '[B][COLOR green]FOIT[/COLOR][COLOR yellow]A[/COLOR][COLOR red]TUGA[/COLOR][/B]'
                percent = int( ( a / 6.0 ) * 100)
                message = ''
                progress.update(percent, 'A Procurar em '+site, message, "")
                print str(a) + " de " + str(int(a))
                xbmc.sleep( 100 )
                url_pesquisa = 'http://foitatugacinemaonline.blogspot.pt/?q=' + str(encode)
                encontrar_fontes_pesquisa_FTT(url_pesquisa)

                a = 5
                site = '[B][COLOR green]CINE[/COLOR][COLOR yellow]M[/COLOR][COLOR red]ATUGA[/COLOR][/B]'
                percent = int( ( a / 6.0 ) * 100)
                message = ''
                progress.update(percent, 'A Procurar em '+site, message, "")
                print str(a) + " de " + str(int(a))
                xbmc.sleep( 100 )
                url_pesquisa = 'http://www.cinematuga.net/search?q=' + str(encode)
                encontrar_fontes_pesquisa_CMT(url_pesquisa)
		
		if selfAddon.getSetting('movies-view') == "0":
                        addDir1('','','',artfolder + 'banner.png',False,'')		
                        addDir('[COLOR yellow]Nova Pesquisa[/COLOR]','url',1,artfolder + 'banner.png','nao','')
                        addDir('[COLOR yellow]Menu Principal[/COLOR]','','',artfolder + 'banner.png','nao','')
                a = 6
                site = '[B][COLOR green]CINE[/COLOR][COLOR yellow]M[/COLOR][COLOR red]ATUGA[/COLOR][/B]'
                percent = int( ( a / 6.0 ) * 100)
                message = ''
                progress.update(percent, 'A Procurar em '+site, message, "")
                print str(a) + " de " + str(int(a))
                xbmc.sleep( 100 )

                xbmcplugin.setContent(int(sys.argv[1]), 'movies')
                xbmc.executebuiltin("Container.SetViewMode(500)")
                xbmcplugin.endOfDirectory(int(sys.argv[1]))


#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def encontrar_fontes_pesquisa_TFV(url,pesquisou):
        pesquisado = pesquisou.replace('%20',' ')
        if selfAddon.getSetting('movies-view') == "0":
                addDir1('[B][COLOR blue]Pesquisou : [/COLOR]( ' + pesquisado + ' )[/B]','url',1020,artfolder + 'banner.png',False,'')
                addDir1('','url',1020,artfolder,False,'')
                addDir1('[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv','url',1020,artfolder,False,'')
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
                num_f = 0
		print len(items)
		for item in items:
                        try:
                                audio_filme = ''
                                urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)
                                if "Temporada" in urletitulo[0][1]:
                                        urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)
                                        num_mode = 42
                                else:
                                        urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)
                                        num_mode = 33
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
                                        addDir('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0] + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR]',urletitulo[0][0],num_mode,thumbnail[0].replace('s72-c','s320'),'','')				
                                        num_f = num_f + 1
                                except: pass
                        except: pass
        else: num_f = 0
        if num_f == 0:
                if selfAddon.getSetting('movies-view') == "0": addDir1('- No Match Found -','url',1020,artfolder,False,'')
	return

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def encontrar_fontes_filmes_TFC(url):
        if selfAddon.getSetting('movies-view') == "0":
                addDir1('[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].com','url',1020,artfolder,False,'')
        pt_en = 0
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
	if items != []:
                num_f = 0
		print len(items)
		for item in items:
                        try:
                                versao = ''
                                pt_en_f = re.compile('<iframe (.+?)</iframe>').findall(item)
                                if '---------------------------------------' in item and len(pt_en_f) > 1: versao = '[COLOR blue] 2 VERSÕES[/COLOR]'
                                urletitulo = re.compile("<a href=\'(.+?)\' title=\'(.+?)\'>").findall(item)
                                qualidade_ano = re.compile('<b>VERS\xc3\x83O:.+?</b><span style="font-size: x-small;">(.+?)<').findall(item)
                                thumbnail = re.compile('<img alt="" border="0" src="(.+?)"').findall(item)
                                print urletitulo,thumbnail
                                #urletitulo[0][1] = urletitulo[0][1].replace('&#8217;',"'")
                                #urletitulo[0][1] = urletitulo[0][1].replace('&#8211;',"-")
                                #urletitulo[0][1] = urletitulo[0][1].replace('&#038;',"&")
                                #urletitulo[0][1] = urletitulo[0][1].replace('&#39;',"'")
                                #urletitulo[0][1] = urletitulo[0][1].replace('&amp;','&')
                                ano = 'Ano'
                                qualidade = ''
                                e_qua = 'nao'
                                calid = ''
                                if qualidade_ano != []:
                                        for q_a in qualidade_ano:
                                                #addDir1(q_a,'','','',False,'')
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
                                                #qualidade = q_a
                                        if qualidade == 'PT PT':
                                                qualidade = 'PT-PT'
                                        if qualidade == '':
                                                quali_titi = urletitulo[0][1].replace('á','a')
                                                quali_titi = urletitulo[0][1].replace('é','e')
                                                quali_titi = urletitulo[0][1].replace('í','i')
                                                quali_titi = urletitulo[0][1].replace('ó','o')
                                                quali_titi = urletitulo[0][1].replace('ú','u')
                                                #addDir1(quali_titi,'','','',False,'')
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
                                #addDir1(url,'','','',False,'')
                                if 'Pt Pt' in qualidade:
                                        qualidade = qualidade.replace('Pt Pt','PT-PT')
                                if 'PT PT' in qualidade:
                                        qualidade = qualidade.replace('PT PT','PT-PT')
                                try:
                                        addDir('[COLOR orange]TFC | [/COLOR][B][COLOR green]' + urletitulo[0][1].replace('&#39;',"'") + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR][COLOR red] (' + qualidade + ')[/COLOR]' + versao,urletitulo[0][0],73,thumbnail[0].replace('s1600','s320').replace('.gif','.jpg'),'','')
                                        num_f = num_f + 1
                                except: pass
                        except: pass
        else: num_f = 0
	if num_f == 0:
                if selfAddon.getSetting('movies-view') == "0": addDir1('- No Match Found -','url',1020,artfolder,False,'')
	return

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def encontrar_fontes_pesquisa_MVT(url):
        if selfAddon.getSetting('movies-view') == "0":
                addDir1('[B][COLOR green]MOVIE[/COLOR][COLOR yellow]-[/COLOR][COLOR red]TUGA[/COLOR][/B]','url',1020,artfolder,False,'')
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
	if items != []:
                num_f = 0
		print len(items)
		for item in items:
                        try:
                                url = re.compile('<div class="btns"><a href="(.+?)" target="Player">').findall(item)
                                if 'http' not in url[0]:
                                        urllink = 'http:' + url[0]
                                else: urllink = url[0] 
                                titulo = re.compile("<strong>T\xc3\xadtulo original:</strong>(.+?)</div>").findall(item)
                                if 'Qualidade:' in item:
                                        qualidade = re.compile("<strong>Qualidade:</strong>(.+?)</div>").findall(item)
                                        qualidade_filme = qualidade[0].replace('&#8211;',"-")
                                else:
                                        qualidade_filme = ''
                                ano = re.compile('<strong>Lan\xc3\xa7amento:</strong>(.+?)</div>').findall(item)
                                thumb = re.compile('src="(.+?)"').findall(item)
                                if 'http' not in thumb[0]:
                                        thumbnail = 'http:' + thumb[0]
                                else: thumbnail = thumb[0]
                                print url,thumbnail
                                titulo[0] = titulo[0].replace('&#8217;',"'")
                                titulo[0] = titulo[0].replace('&#8211;',"-")
                                try:
                                        addDir('[COLOR orange]MVT | [/COLOR][B][COLOR green]' + titulo[0] + ' [/COLOR][/B][COLOR yellow](' + ano[0] + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',urllink,103,thumbnail.replace('s72-c','s320'),'','')
                                        num_f = num_f + 1
                                except: pass
                        except: pass
        else: num_f = 0
	if num_f == 0:
                if selfAddon.getSetting('movies-view') == "0": addDir1('- No Match Found -','url',1020,artfolder,False,'')
	return

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#


def encontrar_fontes_filmes_TPT(url):
        if selfAddon.getSetting('movies-view') == "0":
                addDir1('[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR]','url',1020,artfolder,False,'')
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	if '<div class="postmeta-primary">' in html_source: items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	else:
                if selfAddon.getSetting('movies-view') == "0": addDir1('- No Match Found -','url',1020,artfolder,False,'')
                return
	if items != []:
                num_f = 0
		print len(items)
		for item in items:
                        try:
                                audio_filme = ''
                                urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(item)
                                if 'title=' in urletitulo[0][0]: urletitulo = re.compile('<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>').findall(item)
                                url = urletitulo[0][0]
                                try:
                                        html_source = abrir_url(url)
                                except: html_source = ''
                                #addDir1(url,'','','',False,'')
                                items = re.findall('<div class="post-(.*?)<span id="more-', html_source, re.DOTALL)
                                if items != []:
                                        print len(items)
                                        for item in items:
                                                audio_filme = ''
                                                titulo = re.compile('<h2 class="title">(.+?)</h2>').findall(item)
                                                #urlpesq = re.compile('<span class="entry-date"><a href="(.+?)" rel="bookmark">').findall(item)
                                                qualidade = re.compile("<b>QUALIDADE:.+?/b>(.+?)<br/>").findall(item)
                                                if not qualidade: qualidade = re.compile("<b>VERSÃO:.+?</b>(.+?)<br/>").findall(item)
                                                ano = re.compile("<b>ANO:.+?/b>(.+?)<br/>").findall(item)
                                                audio = re.compile("<b>AUDIO:.+?/b>(.+?)<br/>").findall(item)
                                                if qualidade == [] or ano == [] or audio == []:
                                                        qualidade = re.compile("<b>QUALIDADE:.+?/b>(.+?)<b").findall(item)
                                                        ano = re.compile("<b>ANO:.+?/b>(.+?)<b").findall(item)
                                                        audio = re.compile("<b>AUDIO:.+?/b>(.+?)<b").findall(item)    
                                                thumbnail = re.compile('src="(.+?)"').findall(item)
                                                print urletitulo,thumbnail
                                                nome = titulo[0]
                                                nome = nome.replace('&#8217;',"'")
                                                nome = nome.replace('&#8211;',"-")
                                                nome = nome.replace('&#038;',"&")
                                                nome = nome.replace('(PT-PT)',"")
                                                nome = nome.replace('(PT/PT)',"")
                                                nome = nome.replace('[PT-PT]',"")
                                                nome = nome.replace('[PT/PT]',"")
                                                generos = re.compile('id="post-.+?" class="post-.+? post type-post status-publish format-standard hentry (.+?)">').findall(item)
                                                if not generos: generos = re.compile('post type-post status-publish format-standard hentry (.+?)id="post-.+?">').findall(item)
                                                if generos:
                                                        genero = generos[0]
                                                else:
                                                        genero = ''
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
                                                try:
                                                        #addDir(nome,urletitulo[0][0],233,'','','')
                                                        if 'filmes' in genero or 'series' in genero or 'animacao' in genero:
                                                                if 'online' in genero:
                                                                        #if 'OP\xc3\x87\xc3\x83O' in item:
                                                                        addDir('[COLOR orange]TPT | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR]',url,233,thumbnail[0].replace('s72-c','s320'),'','')
                                                                        num_f = num_f + 1
                                                except: pass
                        except: pass
        else: num_f = 0
        if num_f == 0:
                if selfAddon.getSetting('movies-view') == "0": addDir1('- No Match Found -','url',1020,artfolder,False,'')
	return

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def encontrar_fontes_pesquisa_FTT(url):
        if selfAddon.getSetting('movies-view') == "0":
                addDir1('[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv','url',1020,artfolder,False,'')
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall("<div class='post hentry'>(.+?)<div class='post-outer'>", html_source, re.DOTALL)
	#addDir1(str(len(items)),'url',1002,artfolder,False,'')
	if items != []:
		print len(items)
		num_f = 0
		for item in items:
                        try:
                                thumb = ''
                                fanart = ''
                                anofilme= ''
                                qualidade_filme = ''

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
                                nome = nome.replace('(Pedido)',"")
                                
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
                                                
                                #fanart = artfolder + 'flag.jpg'
                                if fanart == 'fgfgfgfgfgfggf':
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
                                                        html_pesquisa = abrir_url(url_pesquisa)
                                                except: html_pesquisa = ''
                                                items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                                if items_pesquisa != []:
                                                        thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                        if thumbnail: thumb = thumbnail[0].replace('w92','w600')
                                        if selfAddon.getSetting('movie-fanart-MVT') == "true":
                                                try:
                                                        html_pesquisa = abrir_url(url_pesquisa)
                                                except: html_pesquisa = ''
                                                items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                                if items_pesquisa != []:
                                                        url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(items_pesquisa[0])
                                                        if url_filme_pesquisa:
                                                                url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                                try:
                                                                        html_pesquisa = abrir_url(url_pesquisa)
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
                                        addDir_teste('[COLOR orange]FTT | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',urlvideo,603,thumb,'',fanart,anofilme,'')
                                        num_f = num_f + 1
                                except: pass
                        except: pass
        else: num_f = 0
        if num_f == 0:
                if selfAddon.getSetting('movies-view') == "0": addDir1('- No Match Found -','url',1020,artfolder,False,'')
	return

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def encontrar_fontes_pesquisa_CMT(url):
        if selfAddon.getSetting('movies-view') == "0":
                addDir1('[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv','url',1020,artfolder,False,'')
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	conta_items = 0
	if items != []:
		print len(items)
		num_f = 0
		for item in items:
                        try:
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
                                if fanart == 'dfgdfgfdggf':
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
                                                        html_pesquisa = abrir_url(url_pesquisa)
                                                except: html_pesquisa = ''
                                                items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                                if items_pesquisa != []:
                                                        thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                        if thumbnail: thumb = thumbnail[0].replace('w92','w600')
                                        if selfAddon.getSetting('movie-fanart-TFV') == "true":
                                                try:
                                                        html_pesquisa = abrir_url(url_pesquisa)
                                                except: html_pesquisa = ''
                                                items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                                if items_pesquisa != []:
                                                        url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(items_pesquisa[0])
                                                        if url_filme_pesquisa:
                                                                url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                                try:
                                                                        html_pesquisa = abrir_url(url_pesquisa)
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
                                        addDir_teste('[COLOR orange]CMT | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0],num_mode,thumb.replace('s72-c','s320'),sinopse,fanart,ano[0],genre)
                                        num_f = num_f + 1
                                except: pass
                        except: pass
        else: num_f = 0
        if num_f == 0:
                if selfAddon.getSetting('movies-view') == "0": addDir1('- No Match Found -','url',1020,artfolder,False,'')
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
