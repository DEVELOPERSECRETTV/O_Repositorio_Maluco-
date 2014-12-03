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



import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,os#,TopPt,TugaFilmesTV
from Funcoes import thetvdb_api, themoviedb_api, themoviedb_api_tv, theomapi_api, themoviedb_api_IMDB, themoviedb_api_IMDB_episodios, themoviedb_api_TMDB
from Funcoes import thetvdb_api_tvdbid, thetvdb_api_episodes, themoviedb_api_search_imdbcode, themoviedb_api_pagina, themoviedb_api_IMDB1, theomapi_api_nome
from Funcoes import addDir, addDir1, addDir2, addLink, addLink1, addDir_teste, addDir_trailer, addDir_episode
from Funcoes import get_params,abrir_url
import json
from array import array
from string import capwords
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
net=Net()

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
perfil = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
tmdb_base_url = 'http://d3gtl9l2a4fn1j.cloudfront.net/t/p/w1280'

arr_series1 = [['' for i in range(87)] for j in range(1)]
arr_series = ['' for i in range(500)]
arrai_series = ['' for i in range(500)]
todas_series = ['' for i in range(500)]
sinopse_series = ['' for i in range(500)]
_series = []
_series_ = []
_filmes_ = []
arr_filmes = ['' for i in range(200)]
arrai_filmes = ['' for i in range(200)]
thumb_filmes = ['' for i in range(200)]
arr_filmes[4] = '0'
i=arr_filmes[4]

arr_filmes_anima = []
arrai_filmes_anima = []

#http://www.omdbapi.com/?i=tt0903624http://api.themoviedb.org/3/movie/now_playing?api_key=3e7807c4a01f18298f64662b257d7059&append_to_response=overview&page=1

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
##        try:
##		html_source = abrir_url(url_TFV)
##	except: html_source = ''
##	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
##	if items != []:
##		num = len(items)
##	try:
##		html_source = abrir_url(url_TPT)
##	except: html_source = ''
##	items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
##	if items != []:
##		num = num + len(items)
	num = 29 + 0.0
	#----------------------------------------------------------------------------------------------------
	site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
        progress.update( percent, 'A Procurar Últimos Episódios em '+site, message, "" )
        i = 1
        try:
		html_source = abrir_url(url_TPT)
	except: html_source = ''
	items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        sinopse = ''
                        fanart = ''
                        thumb = ''
                        qualidade = ''
                        urltrailer = ''
                        audio_filme = ''

                        urltr = re.compile('"https://www.youtube.com/(.+?)"').findall(item)
                        if urltr: urltrailer = 'https://www.youtube.com/'+urltr[0]
                        
                        urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(item)
                        if 'title=' in urletitulo[0][0]: urletitulo = re.compile('<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>').findall(item)
                        qualid = re.compile("<b>QUALIDADE:.+?/b>(.+?)<br/>").findall(item)
                        if not qualid: qualid = re.compile("<b>VERSÃO:.+?</b>(.+?)<br/>").findall(item)
                        if qualid:
                                qualidade = qualid[0]
                                qualidade = qualidade.replace('[',' - ')
                                qualidade = qualidade.replace(']','')
                        else:
                                qualid = re.compile("\nQUALIDADE:\xc2\xa0(.+?)<br/>").findall(item)
                                if qualid:
                                        qualidade = qualid[0]
                                        qualidade = qualidade.replace('[',' - ')
                                        qualidade = qualidade.replace(']','')
                                else:
                                        qualid = re.compile("<b>VERS.+?</b>(.+?)<br/>").findall(item)
                                        if qualid:
                                                qualidade = qualid[0]
                                                qualidade = qualidade.replace('[',' - ')
                                                qualidade = qualidade.replace(']','')
                                        else:
                                                qualidade = ''

                        genr = re.compile("NERO:.+?/b>(.+?)<br/>").findall(item)
                        if genr: genero = genr[0]
                        
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
                                                        audio = re.compile('<b>AUDIO:.+?<strong>(.+?)</strong>').findall(item)
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

                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        tirar_ano = '(' + str(q_a_q_a) + ')'
                                        nome = nome.replace(tirar_ano,'')

                        percent = int( ( i / num ) * 100)
                        message = nome
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        
                        n = re.compile('(.+?)[[].+?[]]').findall(nome)
                        if n: nome_pesquisa = n[0]
                        thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme)
                        ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                        if ftart:  
                                fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                        snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                        if snpse and sinopse == '': sinopse = snpse[0]
      
                        ano_filme = '('+ano_filme+')'
                        qualidade = '('+qualidade
                        audio_filme = audio_filme+')'
                        try:
                                #addDir_teste('[COLOR orange]TPT | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0],233,thumb,sinopse,fanart.replace('w500','w1280'),ano_filme.replace('(','').replace(')',''),genero)
                                addDir_trailer('[COLOR orange]TPT | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0],233,thumb,sinopse,fanart.replace('w500','w1280'),ano_filme.replace('(','').replace(')',''),genero,nome_pesquisa,urletitulo[0][0])

                        except: pass
                        i = i + 1
        else: pass
        if items != []:
                proxima_TPT = re.compile('</span><a class="nextpostslink" rel="next" href="(.+?)">&raquo;</a><a class="last"').findall(html_source)
                try:
                        url_TPT = proxima_TPT[0].replace('#038;','').replace('&amp;','&')
                except: pass
        else: url_TPT = 'http:'
        #----------------------------------------------------------------------------------------------------
	site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv'
	progress.update(percent, 'A Procurar Últimos Episódios em '+site, message, "")
        try:
		html_source = abrir_url(url_TFV)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        thumb = ''
                        fanart = ''
                        genero = ''
                        sinopse = ''
                        
                        gene = re.compile("nero</b>:(.+?)<br />").findall(item)
                        if gene: genero = gene[0]
                        else: genero = ''
                        resumo = re.compile("<b>Resumo</b>:(.+?)<br />").findall(item)
                        if resumo: sinopse = resumo[0]
                        else: sinopse = ''
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

                        percent = int( ( i / num ) * 100)
                        message = nome
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        
                        n = re.compile('(.+?)[(].+?[)]').findall(nome)
                        if n: nome_original = n[0]
                        else: nome_original = nome

                        nome_pesquisa = nome_original
                        thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano.replace('(','').replace(')',''))
                        ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                        if ftart:
                                fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                if thumb == '' or 's1600' in thumb: thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                        snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                        if snpse and sinopse == '': sinopse = snpse[0]

			try:
				#addDir_teste('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano + '[/COLOR][COLOR red] ' + qualidade + '[/COLOR]',urletitulo[0][0],42,thumb.replace('s72-c','s320'),sinopse,fanart.replace('w500','w1280'),ano,genero)
				addDir_trailer('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano + '[/COLOR][COLOR red] ' + qualidade + '[/COLOR]',urletitulo[0][0],42,thumb.replace('s72-c','s320'),sinopse,fanart.replace('w500','w1280'),ano,genero,nome_pesquisa,urletitulo[0][0])

			except: pass
			i = i + 1
        else: pass
        if items != []:
                proxima_TFV = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
                url_TFV = proxima_TFV[0].replace('&amp;','&')
        else: url_TFV = 'http:'
        #----------------------------------------------------------------------------------------------------
        url_MVT = 'http:'
        url_TFC = 'http:'
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "fim": 'fim',"xpto":'xpto'}
        url_ultimos_episodios = urllib.urlencode(parameters)
        addDir('[B]Página Seguinte >>[/B]',url_ultimos_episodios,508,artfolder + 'PAGS1.png','','')
        progress.close()

        

        

def Filmes_Filmes_Filmes(url):
        
        #folder = perfil
        
        conta_os_items = 0
        a = 1
        percent = 0
        message = ''
        site = ''
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar Filmes...'+site, message, "" )
        urlss = urllib.unquote(url)
        print urlss
        #addLink(urlss,'','')
        #return
        urls=re.compile('url_TFC=(.+?)&url_CMT=(.+?)&url_FTT=(.+?)&url_TFV=(.+?)&url_MVT=(.+?)&xpto=xpto&url_CME=(.+?)&url_TPT=(.+?)&fim=fim').findall(urlss)
        url_TFV = urls[0][3]
        url_TFC = urls[0][0]
        url_MVT = urls[0][4]
        url_TPT = urls[0][6]
        url_FTT = urls[0][2]
        url_CMT = urls[0][1]
        url_CME = urls[0][5]
        #i = int(arr_filmes[4])
        i = 1
        #--------------------------------------------------
        num = 0
        try:
		html_source = abrir_url(url_TFV)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		num = len(items)
	try:
		html_source = abrir_url(url_TFC)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	try:
		html_source = abrir_url(url_MVT)
	except: html_source = ''
	items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	try:
		html_source = abrir_url(url_TPT)
	except: html_source = ''
	items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	try:
		html_source = abrir_url(url_FTT)
	except: html_source = ''
	items = re.findall("<div class='post-body entry-content'>(.+?)<div class='post-outer'>", html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	try:
		html_source = abrir_url(url_CMT)
	except: html_source = ''
	items = re.findall("<h3 class='post-title entry-title'(.*?)<span class='post-location'>", html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	try:
		html_source = abrir_url(url_CME)
	except: html_source = ''
	items = re.findall("<h3 class='post-title entry-title'(.+?)<div class='post-outer'>", html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	num = num + 0.0
	i = 1
        a = 1
	percent = int( ( a / num ) * 100)
        message = str(a) + " de " + str(int(num))
        progress.update( percent, 'A Procurar Filmes...', message, "" )
	#----------------------------------------------------------------------------------------------------
	site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
        progress.update( percent, 'A Procurar Filmes em '+site, message, "" )
        
def TPTMASHUP(url):
        i = 1
        url_TPT = url
        percent = 0
        message = 'Por favor aguarde.'
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar Filmes...', message, "" )
        _filmes_ = []
        folder = perfil
        Filmes_File = open(folder + 'filmesTPT.txt', 'w')
        Filmes_Fi = open(folder + 'filmesTPT.txt', 'r')
        read_Filmes_File = ''
        for line in Filmes_Fi:
                read_Filmes_File = read_Filmes_File + line
                if line!='':_filmes_.append(line)
        try:
		html_source = abrir_url(url_TPT)
	except: html_source = ''
	items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:

                        sinopse = ''
                        genero = ''
                        fanart = ''
                        thumb = ''
                        qualidade = ''
                        imdbcode = ''
                        audio_filme = ''
                                
                        urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(item)
                        if 'title=' in urletitulo[0][0]: urletitulo = re.compile('<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>').findall(item)
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

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                                
##                        percent = int( ( a / num ) * 100)
##                        message = str(a) + " de " + str(int(num))
##                        progress.update( percent, 'A Procurar Filmes em '+site, message, "" )
##                        print str(a) + " de " + str(int(num))
##                        if progress.iscanceled():
##                                break
                                
                                
                        qualid = re.compile("<b>QUALIDADE:.+?/b>(.+?)<br/>").findall(item)
                        if not qualid: qualid = re.compile("<b>VERSÃO:.+?</b>(.+?)<br/>").findall(item)
                        if qualid:
                                qualidade = qualid[0]
                                qualidade = qualidade.replace('[',' - ')
                                qualidade = qualidade.replace(']','')
                        else:
                                qualid = re.compile("\nQUALIDADE:\xc2\xa0(.+?)<br/>").findall(item)
                                if qualid:
                                        qualidade = qualid[0]
                                        qualidade = qualidade.replace('[',' - ')
                                        qualidade = qualidade.replace(']','')
                                else:
                                        qualid = re.compile("<b>VERS.+?</b>(.+?)<br/>").findall(item)
                                        if qualid:
                                                qualidade = qualid[0]
                                                qualidade = qualidade.replace('[',' - ')
                                                qualidade = qualidade.replace(']','')
                                        else:
                                                qualidade = ''

                        genr = re.compile("NERO:.+?/b>(.+?)<br/>").findall(item)
                        if genr: genero = genr[0]

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
                                                        audio = re.compile('<b>AUDIO:.+?<strong>(.+?)</strong>').findall(item)
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
                                
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        tirar_ano = '(' + str(q_a_q_a) + ')'
                                        nome = nome.replace(tirar_ano,'')
                        O_Nome = nome
                        progress.update( percent, 'A Procurar Filmes.', '[COLOR green]'+O_Nome+'[/COLOR]', "" )
##                        n_f = re.compile('.net/(.*)').findall(urletitulo[0][0])
##                        nome_filme = n_f[0]#nome
##                        if nome_filme in read_Filmes_File:
##                                for x in range(len(_filmes_)):
##                                        if nome_filme in _filmes_[x]:
##                                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_filmes_[x])
##                                                if _n: nomes = _n[0]
##                                                else: nomes = '---'
##                                                if nome_filme == nomes:
##                                                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_filmes_[x])
##                                                        if _i: imdbcode = _i[0]
##                                                        else: imdbcode = '---'
##                                                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_filmes_[x])
##                                                        if _t: thumb = _t[0]
##                                                        else: thumb = '---'
##                                                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_filmes_[x])
##                                                        if _a: ano_filme = _a[0]
##                                                        else: ano_filme = '---'
##                                                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_filmes_[x])
##                                                        if _f: fanart = _f[0]
##                                                        else: fanart = '---'
##                                                        _g = re.compile('[|]GENERO[|](.+?)[|]SINOPSE[|]').findall(_filmes_[x])
##                                                        if _g: genero = _g[0]
##                                                        else: genero = '---'
##                                                        _s = re.compile('[|]SINOPSE[|](.*)').findall(_filmes_[x])
##                                                        if _s: s = _s[0]
##                                                        if '|END|' in s: sinopse = s.replace('|END|','')
##                                                        else:
##                                                                si = re.compile('SINOPSE[|](.+?)\n(.+?)[|]END[|]').findall(_filmes_[x])
##                                                                if si: sinopse = si[0][0] + ' ' + si[0][1]
##                                                                else: sinopse = '---'
                        try:
                        #else:
                                if fanart == '': fanart = '---'
                                if genero == '': genero = '---'
                                if sinopse == '': sinopse = '---'
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
                                nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?)[:] ').findall(nome)
                                if nnnn: nome_pesquisa = nnnn[0]
                                else: nome_pesquisa = nome
                                if imdbcode != '':
                                        try:
                                                fanart,tmdb_id,poster,sin = themoviedb_api_IMDB().fanart_and_id(str(imdbcode),ano_filme)
                                                if sinopse == '': sinopse = sin
                                                if fanart == '': fanart,tmb,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano_filme)
                                                if thumb == '': thumb = poster
                                        except:pass
                                else:
                                        try:
                                                fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano_filme)
                                                if thumb == '': thumb = poster
                                        except: pass

                                #Filmes_File.write('NOME|'+str(nome_filme)+'|IMDBCODE|'+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb)+'|ANO|'+str(ano_filme.replace('(','').replace(')',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|SINOPSE|'+str(sinopse)+'|END|\n')
                        except: pass        
                        if fanart == '---': fanart = ''
                        ano_filme = '('+ano_filme+')'
                        qualidade = '('+qualidade
                        audio_filme = audio_filme+')'
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        if sinopse == '' or sinopse == '---':
                                imc = re.compile('IMDB(.+?)IMDB').findall(imdbcode)
                                if imc: imc = imc[0]
                                else: imc = imdbcode
                                fafa,tmtm,popo,sinopse = themoviedb_api_IMDB().fanart_and_id(imc,ano_filme.replace('(','').replace(')',''))
                        try:
                                nome_final = '[COLOR orange]TPT | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow] ' +ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]'
                                Filmes_File.write('NOME|'+str(nome_final)+'|IMDBCODE|'+str(urletitulo[0][0])+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb)+'|ANO|'+str(ano_filme.replace('(','').replace(')',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|ONOME|'+str(O_Nome)+'|SINOPSE|'+str(sinopse)+'|END|\n')
##                                if 'IMDB' in imdbcode:
##                                        addDir_trailer('[COLOR orange]TPT | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow] ' +ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0]+imdbcode,233,thumb,sinopse,fanart.replace('w500','w1280'),ano_filme.replace('(','').replace(')',''),genero,O_Nome,urletitulo[0][0])
##                                else:
##                                        addDir_trailer('[COLOR orange]TPT | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',233,thumb,sinopse,fanart.replace('w500','w1280'),ano_filme.replace('(','').replace(')',''),genero,O_Nome,urletitulo[0][0])
                                # addDir_teste('[COLOR orange]TPT | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',233,thumb,'[COLOR yellow]INFO:[/COLOR][COLOR red]'+qualidade.replace('(','')+audio_filme.replace(')','')+'[/COLOR]'+'\n'+sinopse,fanart.replace('w500','w1280'),ano_filme.replace('(','').replace(')',''),genero)
                        except: pass
##                        i = i + 1
##                        a = a + 1
                
        else: pass
        if items != []:
                proxima_TPT = re.compile('</span><a class="nextpostslink" rel="next" href="(.+?)">&raquo;</a><a class="last"').findall(html_source)
                try:
                        url_TPT = proxima_TPT[0].replace('#038;','').replace('&amp;','&')
                except: pass
        else: url_TPT = 'http:'
        Filmes_File.write('PAGINA|'+url_TPT+'|PAGINA')
        Filmes_File.close()
        Filmes_Fi.close()
        
        #----------------------------------------------------------------------------------------------------
##        site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].com'
##        progress.update( percent, 'A Procurar Filmes em '+site, message, "" )
def TFCMASHUP(url):
        url_TFC = url
        percent = 0
        message = 'Por favor aguarde.'
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar Filmes...', message, "" )
        _filmes_ = []
        folder = perfil
        Filmes_File = open(folder + 'filmesTFC.txt', 'w')
        Filmes_Fi = open(folder + 'filmesTFC.txt', 'r')
        read_Filmes_File = ''
        for line in Filmes_Fi:
                read_Filmes_File = read_Filmes_File + line
                if line!='':_filmes_.append(line)
        try:
		html_source = abrir_url(url_TFC)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
##                        percent = int( ( a / num ) * 100)
##                        message = str(a) + " de " + str(int(num))
##                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
##                        print str(a) + " de " + str(int(num))
##                        if progress.iscanceled():
##                                break
                        #if selfAddon.getSetting('movie-fanart-TFC') == "false": xbmc.sleep( 50 )
                        fanart = ''
                        thumb = ''
                        versao = ''
                        sinopse = ''
                        imdbcode = ''
                        genero = ''
                        qualidade = ''

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
                                        ano = ''
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
                        O_Nome = nome
                        progress.update( percent, 'A Procurar Filmes..', '[COLOR green]'+O_Nome+'[/COLOR]', "" )
##                        n_f = re.compile('.info/(.+?)[.]html').findall(urletitulo[0][0])
##                        nome_filme = n_f[0]#nome
##                        if nome_filme in read_Filmes_File:
##                                for x in range(len(_filmes_)):
##                                        if nome_filme in _filmes_[x]:
##                                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_filmes_[x])
##                                                if _n: nomes = _n[0]
##                                                else: nomes = '---'
##                                                if nome_filme == nomes:
##                                                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_filmes_[x])
##                                                        if _i: imdbcode = _i[0]
##                                                        else: imdbcode = '---'
##                                                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_filmes_[x])
##                                                        if _t: thumb = _t[0]
##                                                        else: thumb = '---'
##                                                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_filmes_[x])
##                                                        if _a: ano = _a[0]
##                                                        else: ano = '---'
##                                                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_filmes_[x])
##                                                        if _f: fanart = _f[0]
##                                                        else: fanart = '---'
##                                                        _g = re.compile('[|]GENERO[|](.+?)[|]END[|]').findall(_filmes_[x])
##                                                        if _g: genero = _g[0]
##                                                        else: genero = '---'
####                                                        _s = re.compile('[|]SINOPSE[|](.*)').findall(_filmes_[x])
####                                                        if _s: s = _s[0]
####                                                        if '|END|' in s: sinopse = s.replace('|END|','')
####                                                        else:
####                                                                si = re.compile('SINOPSE[|](.+?)\n(.+?)[|]END[|]').findall(_filmes_[x])
####                                                                if si: sinopse = si[0][0] + ' ' + si[0][1]
####                                                                else: sinopse = '---'
                        try:
                        #else:
                                if genero == '': genero = '---'
                                if sinopse == '': sinopse = '---'
                                if fanart == '': fanart = '---'
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
                                if qualidade == '': qualidade = '---'
                                nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?)[:] ').findall(nome)
                                if nnnn : nome_pesquisa = nnnn[0]
                                if nnnn: nome_pesquisa = nnnn[0]
                                else: nome_pesquisa = nome
                                #fanart,tmdb_id,poster,overview = themoviedb_api_IMDB().fanart_and_id(str(imdbcode),ano_filme)
                                try:
                                        fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano)
                                        if thumb == '': thumb = poster
                                except: pass
##                                addLink(ano,'','')
##                                addLink(fanart,'','')
##                                addLink(thumb,'','')
##                                addLink(nome_filme,'','')
##                                addLink(genero,'','')
##                                addLink(sinopse,'','')
##                                addLink(imdbcode,'','')
                      ###          Filmes_File.write('NOME|'+str(nome_filme)+'|IMDBCODE|'+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb.replace('s1600','s320').replace('.gif','.jpg'))+'|ANO|'+str(ano.replace('(','').replace(')',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|END|\n')
                                #Filmes_File.write('NOME|'+nome_filme+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|THUMB|'+thumb.replace('s1600','s320').replace('.gif','.jpg')+'|ANO|'+ano.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|\n')
                        except: pass
                        
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        if qualidade == '': qualidade = '---'
			try:
                                if 'ASSISTIR O FILME' in item:
                                        nome_final = '[COLOR orange]TFC | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR][COLOR red] (' + qualidade + ')[/COLOR]' + versao
                                        Filmes_File.write('NOME|'+str(nome_final)+'|IMDBCODE|'+urletitulo[0][0]+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb.replace('s1600','s320').replace('.gif','.jpg'))+'|ANO|'+str(ano.replace('(','').replace(')',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|ONOME|'+str(O_Nome)+'|SINOPSE|'+str(sinopse)+'|END|\n')
##                                        if 'IMDB' in imdbcode:
##                                                addDir_trailer('[COLOR orange]TFC | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR][COLOR red] (' + qualidade + ')[/COLOR]' + versao,urletitulo[0][0]+imdbcode,73,thumb.replace('s1600','s320').replace('.gif','.jpg'),sinopse,fanart.replace('w500','w1280'),ano,qualidade,O_Nome,urletitulo[0][0])
##                                        else:
##                                                addDir_trailer('[COLOR orange]TFC | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR][COLOR red] (' + qualidade + ')[/COLOR]' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',73,thumb.replace('s1600','s320').replace('.gif','.jpg'),sinopse,fanart.replace('w500','w1280'),ano,qualidade,O_Nome,urletitulo[0][0])
			except: pass
##			a = a + 1
##                        i = i + 1
                
        else: pass
        if items != []:
                proxima_TFC = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
                url_TFC = proxima_TFC[0].replace('&amp;','&')
        else: url_TFC = 'http:'
        Filmes_File.write('PAGINA|'+url_TFC+'|PAGINA')
        Filmes_File.close()
        Filmes_Fi.close()
        #----------------------------------------------------------------------------------------------------
##        site = '[B][COLOR green]FOIT[/COLOR][COLOR yellow]A[/COLOR][COLOR red]TUGA[/COLOR][/B]'
##	progress.update(percent, 'A Procurar Filmes em '+site, message, "")
def FTTMASHUP(url):
        url_FTT = url
        percent = 0
        message = 'Por favor aguarde.'
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar Filmes...', message, "" )
	_filmes_ = []
        folder = perfil
        Filmes_File = open(folder + 'filmesFTT.txt', 'w')
        Filmes_Fi = open(folder + 'filmesFTT.txt', 'r')
        read_Filmes_File = ''
        for line in Filmes_Fi:
                read_Filmes_File = read_Filmes_File + line
                if line!='':_filmes_.append(line)
        try:
		html_source = abrir_url(url_FTT)
	except: html_source = ''
	items = re.findall("<a class='comment-link'(.+?)<div class='post-outer'>", html_source, re.DOTALL)
	if items != []:
		for item in items:
##                        percent = int( ( a / num ) * 100)
##                        message = str(a) + " de " + str(int(num))
##                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
##                        print str(a) + " de " + str(int(num))
##                        if progress.iscanceled():
##                                break
                        #if selfAddon.getSetting('movie-fanart-FTT') == "false": xbmc.sleep( 50 )

                        genero = ''
                        sinopse = ''
                        thumb = ''
                        fanart = ''
                        anofilme= ''
                        qualidade_filme = ''
                        imdbcode = ''
                        audio_filme = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''

                        urletitulo = re.compile("<a href='(.+?)' title='(.+?)'>").findall(item)
                        if not urletitulo: urletitulo = re.compile("<a href='(.+?)'>(.+?)</a>").findall(item)
                        if urletitulo:
                                urlvideo = urletitulo[0][0]
                                nome = urletitulo[0][1]
                        else:
                                urlvideo = ''
                                nome = ''

                        snpse = re.compile('Sinopse.png"></a></div>\n(.+?)\n').findall(item)
                        if not snpse: snpse = re.compile('Sinopse.png" /></a></div>\n(.+?)\n').findall(item)
                        if snpse: sinopse = snpse[0]
                        sinopse = sinopse.replace('&#8216;',"'")
                        sinopse = sinopse.replace('&#8217;',"'")
                        sinopse = sinopse.replace('&#8220;',"'")
                        sinopse = sinopse.replace('&#8221;',"'")
                        sinopse = sinopse.replace('&#8211;',"-")
                        sinopse = sinopse.replace('&#39;',"'")
                        sinopse = sinopse.replace('&amp;','&')
                                
                        ano = re.compile('<strong>Lan\xc3\xa7amento:</strong>(.+?)</div>').findall(item)
                        if ano: anofilme = ano[0]
                        else: anofilme = ''

                        generos = re.compile("rel='tag'>(.+?)</a>").findall(item)
                        conta = 0
                        for gener in generos:
                                if conta == 0:
                                        if gener.replace(' ','') != anofilme.replace(' ',''):
                                                genero = gener
                                                conta = conta + 1
                                else:
                                        if gener.replace(' ','') != anofilme.replace(' ',''):
                                                genero = genero +'  '+ gener
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(genero)
                        conta = 0
                        for q_a_q_a in qq_aa:
                                genero = genero.replace(str(q_a_q_a)+'  ','')
                        
                        thumbnail = re.compile('<img height=".+?" src="(.+?)" width=".+?"').findall(item)
                        if thumbnail: thumb = thumbnail[0].replace('s72-c','s320').replace('s1600','s320')
                        else:         
                                #thumbnail = re.compile('<a href="(.+?)" imageanchor="1"').findall(item)        
                                thumbnail = re.compile('document.write[(]bp_thumbnail_resize[(]"(.+?)",".+?"[)]').findall(item)
                                if thumbnail: thumb = thumbnail[0].replace('s72-c','s320').replace('s1600','s320')
                                else:
                                        #if not thumbnail: thumbnail = re.compile("<meta content='(.+?)' itemprop='image_url'/>").findall(item)
                                        thumbnail = re.compile('<a href="(.+?)" imageanchor="1"').findall(item)
                                        if thumbnail: thumb = thumbnail[0].replace('s72-c','s320').replace('s1600','s320')
                                        else:
                                                thumbnail = re.compile('<img alt="image" height=".+?" src="(.+?)" width=".+?"').findall(item)
                                                if thumbnail: thumb = thumbnail[0].replace('s72-c','s320').replace('s1600','s320')
                                                else:
                                                        thumbnail = re.compile('<img src="(.+?)" height=".+?" width=".+?"').findall(item)
                                                        if thumbnail: thumb = thumbnail[0].replace('s72-c','s320').replace('s1600','s320')
                        if 'container' in thumb:
                                thumbnail = re.compile('url=(.+?)blogspot(.+?)&amp;container').findall(thumb)
                                if thumbnail: thumb = thumbnail[0][0].replace('%3A',':').replace('%2F','/')+'blogspot'+thumbnail[0][1].replace('%3A',':').replace('%2F','/')

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
                                        nome = nome.replace(tirar_ano,'')
                                        tirar_ano = '-' + str(q_a_q_a)
                                        nome = nome.replace(tirar_ano,'')
                                        tirar_ano = str(q_a_q_a)
                                        nome = nome.replace(tirar_ano,'')

                        if '[PT/PT]' in nome:
                                audio_filme = 'PT/PT'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')
                        if '[PT-PT]' in nome:
                                audio_filme = 'PT-PT'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')
                        if '[PT/BR]' in nome:
                                audio_filme = 'PT/BR'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')
                        if '[PT-BR]' in nome:
                                audio_filme = 'PT-BR'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')
                        if '[PT/PT]' in nome:
                                audio_filme = 'PT/PT'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')
                        if '(PT-PT)' in nome:
                                audio_filme = 'PT-PT'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')
                        if '(PT/BR)' in nome:
                                audio_filme = 'PT/BR'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')
                        if '(PT-BR)' in nome:
                                audio_filme = 'PT-BR'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')
                        if 'PT/PT' in nome:
                                audio_filme = 'PT/PT'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')
                        if 'PT-PT' in nome:
                                audio_filme = 'PT-PT'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')
                        if 'PT/BR' in nome:
                                audio_filme = 'PT/BR'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')
                        if 'PT-BR' in nome:
                                audio_filme = 'PT-BR'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')

                        if audio_filme!= '': audio_filme = ': '+audio_filme

                        nome = nome.replace('-- ',"")
                        nome = nome.replace(' --',"")
                        nome = nome.replace('--',"")

                        nome = nome.replace('((','(')
                        nome = nome.replace('))',')')
                        nome = nome.replace('()','(')
                        nome = nome.replace('  ','')
                        nome = nome.replace(' - []','')
                        nome = nome.replace('[]','')

                        O_Nome = nome
                        progress.update( percent, 'A Procurar Filmes...', '[COLOR green]'+O_Nome+'[/COLOR]', "" )
##                        n_f = re.compile('.pt/(.+?)[.]html').findall(urletitulo[0][0])
##                        nome_filme = n_f[0]#nome
##                        if nome_filme in read_Filmes_File:
##                                for x in range(len(_filmes_)):
##                                        if nome_filme in _filmes_[x]:
##                                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_filmes_[x])
##                                                if _n: nomes = _n[0]
##                                                else: nomes = '---'
##                                                if nome_filme == nomes:
##                                                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_filmes_[x])
##                                                        if _i: imdbcode = _i[0]
##                                                        else: imdbcode = '---'
##                                                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_filmes_[x])
##                                                        if _t: thumb = _t[0]
##                                                        else: thumb = '---'
##                                                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_filmes_[x])
##                                                        if _a: ano_filme = _a[0]
##                                                        else: ano_filme = '---'
##                                                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_filmes_[x])
##                                                        if _f: fanart = _f[0]
##                                                        else: fanart = '---'
##                                                        _g = re.compile('[|]GENERO[|](.+?)[|]QUALIDADE[|]').findall(_filmes_[x])
##                                                        if _g: genero = _g[0]
##                                                        else: genero = '---'
##                                                        _q = re.compile('[|]QUALIDADE[|](.+?)[|]END[|]').findall(_filmes_[x])
##                                                        if _q: qualidade_filme = _q[0]
##                                                        else: qualidade_filme = ''
                        try:
                        #else:
                                
                                try:
                                        fonte_video = abrir_url(urlvideo)
                                except: fonte_video = ''
                                fontes_video = re.findall("<div class='post-body entry-content'>(.*?)<div style='clear: both;'>", fonte_video, re.DOTALL)
                                if fontes_video != []:
                                        qualid = re.compile('ASSISTIR ONLINE (.*)\n').findall(fontes_video[0])
                                        if qualid: qualidade_filme = qualid[0].replace('/ ',' ').replace('</b>','').replace('</span>','').replace('LEGENDADO','') + audio_filme
                                        else:
                                                qualid = re.compile('[[]</span><span style=".+?"><span style=".+?">(.+?)</span><span style=".+?">[]]').findall(fontes_video[0])
                                                if qualid: qualidade_filme = qualid[0].replace('/ ','').replace('</b>','').replace('</span>','') + audio_filme
                                                else: qualidade_filme = '---'
                                nnnn = re.compile('.+?[(](.+?)[)]').findall(nome)
                                if not nnnn: nnnn = re.compile('.+?[[](.+?)[]]').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?)[:] ').findall(nome)
                                if nnnn : nome_pesquisa = nnnn[0]
                                else: nome_pesquisa = nome
                                if imdbcode != '':
                                        try:
                                                fanart,tmdb_id,poster,sin = themoviedb_api_IMDB().fanart_and_id(str(imdbcode),anofilme)
                                                if sinopse == '' or '<div class="separator" style="clear: both; text-align: center;">' in sinopse: sinopse = sin
                                                if fanart == '': fanart,tmb,poster = themoviedb_api().fanart_and_id(nome_pesquisa,anofilme)
                                                if thumb == ''  or 'IMDb.png' in thumb or 'Sinopse' in thumb: thumb = poster
                                        except:pass
                                else:
                                        try:
                                                fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,anofilme)
                                                if thumb == ''  or 'IMDb.png' in thumb or 'Sinopse' in thumb: thumb = poster
                                        except: pass
                                

                                if genero == '': genero = '---'
                                if sinopse == '': sinopse = '---'
                                if fanart == '': fanart = '---'
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
                               # if 'Temporada' not in nome and 'temporada' not in nome:
                                   #     Filmes_File.write('NOME|'+nome_filme+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|THUMB|'+str(thumb)+'|ANO|'+anofilme+'|FANART|'+str(fanart)+'|GENERO|'+genero+'|QUALIDADE|'+qualidade_filme.replace('</div>','')+'|END|\n')
                        except: pass
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        
                        try:
                                if 'Temporada' not in O_Nome and 'temporada' not in O_Nome:
                                        nome_final = '[COLOR orange]FTT | [/COLOR][B][COLOR green]' + O_Nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme.replace('</div>','') + ')[/COLOR]'
                                        Filmes_File.write('NOME|'+nome_final+'|IMDBCODE|'+urlvideo+'IMDB'+imdbcode+'IMDB'+'|THUMB|'+str(thumb)+'|ANO|'+anofilme+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|ONOME|'+str(O_Nome)+'|SINOPSE|'+str(sinopse)+'|END|\n')

##                                        if 'IMDB' in imdbcode:
##                                                addDir_trailer('[COLOR orange]FTT | [/COLOR][B][COLOR green]' + O_Nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme.replace('</div>','') + ')[/COLOR]',urlvideo+imdbcode,603,thumb,sinopse,fanart.replace('w500','w1280'),anofilme,genero,O_Nome,urlvideo)
##                                        else:
##                                                addDir_trailer('[COLOR orange]FTT | [/COLOR][B][COLOR green]' + O_Nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme.replace('</div>','') + ')[/COLOR]',urlvideo+'IMDB'+imdbcode+'IMDB',603,thumb,sinopse,fanart.replace('w500','w1280'),anofilme,genero,O_Nome,urlvideo)
                        except: pass
##                        i = i + 1
##                        a = a + 1
                        
                        #---------------------------------------------------------------
	else: pass	
	if items != []:
                proxima = re.compile("<a class='blog-pager-older-link' href='(.+?)' id='Blog1_blog-pager-older-link'").findall(html_source)
                proxima_p = proxima[0]
		url_FTT = proxima_p.replace('&amp;','&')
	else: url_FTT = 'http:'
	Filmes_File.write('PAGINA|'+url_FTT+'|PAGINA')
	Filmes_File.close()
        Filmes_Fi.close()
#------------------------------------------------------------------------------------------------------------------------
##	site = '[B][COLOR green]CINE[/COLOR][COLOR yellow]M[/COLOR][COLOR red]ATUGA.net[/COLOR][/B]'
##	progress.update(percent, 'A Procurar Filmes em '+site, message, "")
def CMTMASHUP(url):
        url_CMT = url
        percent = 0
        message = 'Por favor aguarde.'
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar Filmes...', message, "" )
	_filmes_ = []
        folder = perfil
        Filmes_File = open(folder + 'filmesCMTnet.txt', 'w')
        Filmes_Fi = open(folder + 'filmesCMTnet.txt', 'r')
        read_Filmes_File = ''
        for line in Filmes_Fi:
                read_Filmes_File = read_Filmes_File + line
                if line!='':_filmes_.append(line)
        try:
		html_source = abrir_url(url_CMT)
	except: html_source = ''
	items = re.findall("<h3 class='post-title entry-title'(.*?)<span class='post-location'>", html_source, re.DOTALL)
	conta_items = 0
	if items != []:
		print len(items)
		for item in items:
##                        percent = int( ( a / num ) * 100)
##                        message = str(a) + " de " + str(int(num))
##                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
##                        print str(a) + " de " + str(int(num))
##                        if progress.iscanceled():
##                                break
                        #if selfAddon.getSetting('movie-fanart-CMT') == "false": xbmc.sleep( 50 )
                        thumb = ''
                        fanart = ''
                        versao = ''
                        genero = ''
                        sinopse = ''
                        audio_filme = ''
                        imdbcode = ''
                        ano_filme = ''

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
                        ################urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)
                        urletitulo = re.compile("<a href='(.+?)'>(.+?)</a>").findall(item)
                        qualidade = re.compile("<b>Qualidade</b>: (.+?)<br />").findall(item)
                        if not qualidade: qualidade = re.compile("Ass.+?tir online .+?[(](.+?)[)]").findall(item)
                        if qualidade: qualidade = qualidade[0].replace('<b>','').replace('</b>','')
                        else: qualidade = ''
                        ano = re.compile("<b>Ano</b>: (.+?)<br />").findall(item)
                        if ano: ano_filme = ano[0]
                        else: ano_filme = ''
                        #return
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
                        nome = nome.replace('(PT-BR)',"")
                        nome = nome.replace('(PT/BR)',"")
                        nome = nome.replace('[PT-PT]',"")
                        nome = nome.replace('[PT/PT]',"")
                        nome = nome.replace('PT-PT)',"")
                        nome = nome.replace('PT/PT)',"")
                        nome = nome.replace('PT-PT]',"")
                        nome = nome.replace('PT/PT]',"")
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        tirar_ano = '(' + str(q_a_q_a) + ')'
                                        nome = nome.replace(tirar_ano,'')
                                        if ano_filme == '': ano_filme = str(q_a_q_a)
                        O_Nome = nome
                        progress.update( percent, 'A Procurar Filmes....', '[COLOR green]'+O_Nome+'[/COLOR]', "" )
##                        n_f = re.compile('.net/(.+?)[.]html').findall(urletitulo[0][0])#'.org/(.+?)[.]html'
##                        nome_filme = n_f[0]#nome
##                        if nome_filme in read_Filmes_File:
##                                for x in range(len(_filmes_)):
##                                        if nome_filme in _filmes_[x]:
##                                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_filmes_[x])
##                                                if _n: nomes = _n[0]
##                                                else: nomes = '---'
##                                                if nome_filme == nomes:
##                                                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_filmes_[x])
##                                                        if _i: imdbcode = _i[0]
##                                                        else: imdbcode = '---'
##                                                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_filmes_[x])
##                                                        if _t: thumb = _t[0]
##                                                        else: thumb = '---'
##                                                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_filmes_[x])
##                                                        if _a: ano_filme = _a[0]
##                                                        else: ano_filme = '---'
##                                                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_filmes_[x])
##                                                        if _f: fanart = _f[0]
##                                                        else: fanart = '---'
##                                                        _g = re.compile('[|]GENERO[|](.+?)[|]END[|]').findall(_filmes_[x])
##                                                        if _g: genre = _g[0]
##                                                        else: genre = '---'
####                                                        _s = re.compile('[|]SINOPSE[|](.*)').findall(_filmes_[x])
####                                                        if _s: s = _s[0]
####                                                        if '|END|' in s: sinopse = s.replace('|END|','')
####                                                        else:
####                                                                si = re.compile('SINOPSE[|](.+?)\n(.+?)[|]END[|]').findall(_filmes_[x])
####                                                                if si: sinopse = si[0][0] + ' ' + si[0][1]
####                                                                else: sinopse = '---'
                        try:
                        #else:
                                if thumb == '': thumb = poster
                                if genre == '': genre = '---'
                                if sinopse == '': sinopse = '---'
                                if fanart == '': fanart = '---'
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
                                nnnn = re.compile('(.+?): ').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                                if nnnn : nome_pesquisa = nnnn[0]
                                else: nome_pesquisa = nome
                                if imdbcode != '':
                                        try:
                                                fanart,tmdb_id,poster,sin = themoviedb_api_IMDB().fanart_and_id(str(imdbcode),ano_filme.replace(' ',''))
                                                if sinopse == '': sinopse = sin
                                                if fanart == '': fanart,tmb,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano_filme.replace(' ',''))
                                        except:
                                                fanart = '---'
                                                tmdb_id = '---'
                                                poster = ''
                                else:
                                        try:
                                                fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano_filme.replace(' ',''))
                                        except: 
                                                fanart = '---'
                                                tmdb_id = '---'
                                                poster = ''
                                #Filmes_File.write('NOME|'+str(nome_filme)+'|IMDBCODE|'+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb.replace('s72-c','s320'))+'|ANO|'+str(ano_filme.replace(' ',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(genre)+'|END|\n')
                        except: pass                              
                        if thumb == '': thumb = '---'
                        if genre == '': genre = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        if sinopse == '' or sinopse == '---':
                                imc = re.compile('IMDB(.+?)IMDB').findall(imdbcode)
                                if imc: imc = imc[0]
                                else: imc = imdbcode
                                fafa,tmtm,popo,sinopse = themoviedb_api_IMDB().fanart_and_id(imc,ano_filme.replace(' ','').replace(' ',''))
                        try:
                                nome_final = '[COLOR orange]CMT | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow](' + ano_filme.replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao
                                Filmes_File.write('NOME|'+str(nome_final)+'|IMDBCODE|'+urletitulo[0][0]+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb.replace('s72-c','s320'))+'|ANO|'+str(ano_filme.replace(' ',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(genre)+'|ONOME|'+str(O_Nome)+'|SINOPSE|'+str(sinopse)+'|END|\n')
##                                if 'IMDB' in imdbcode:
##                                        addDir_trailer('[COLOR orange]CMT | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow](' + ano_filme.replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+imdbcode,703,thumb.replace('s72-c','s320'),sinopse,fanart.replace('w500','w1280'),ano_filme.replace(' ',''),genre,O_Nome,urletitulo[0][0])
##                                else:
##                                        addDir_trailer('[COLOR orange]CMT | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow](' + ano_filme.replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',703,thumb.replace('s72-c','s320'),sinopse,fanart.replace('w500','w1280'),ano_filme.replace(' ',''),genre,O_Nome,urletitulo[0][0])

                        except: pass
                        #---------------------------------------------------------------
##                        i = i + 1
##                        a = a + 1
                        #---------------------------------------------------------------

	else: pass
	if items != []:
                        proxima = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
                        url_CMT = proxima[0].replace('&amp;','&')
        else: url_CMT = 'http:'
        Filmes_File.write('PAGINA|'+url_CMT+'|PAGINA')
        Filmes_File.close()
        Filmes_Fi.close()
#------------------------------------------------------------------------------------------------------------------------------------
##	site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv'
##	progress.update(percent, 'A Procurar Filmes em '+site, message, "")
def TFVMASHUP(url):
        url_TFV = url
        percent = 0
        message = 'Por favor aguarde.'
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar Filmes...', message, "" )
	_filmes_ = []
        folder = perfil
        Filmes_File = open(folder + 'filmesTFV.txt', 'w')
        Filmes_Fi = open(folder + 'filmesTFV.txt', 'r')
        read_Filmes_File = ''
        for line in Filmes_Fi:
                read_Filmes_File = read_Filmes_File + line
                if line!='':_filmes_.append(line)
        try:
		html_source = abrir_url(url_TFV)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
##                        percent = int( ( a / num ) * 100)
##                        message = str(a) + " de " + str(int(num))
##                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
##                        print str(a) + " de " + str(int(num))
##                        if progress.iscanceled():
##                                break
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
                        if qualidade: qualidade = qualidade[0]
                        else: qualidade = ''
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
                                        
                        O_Nome = nome
                        progress.update( percent, 'A Procurar Filmes.....', '[COLOR green]'+O_Nome+'[/COLOR]', "" )
##                        n_f = re.compile('.us/(.+?)[.]html').findall(urletitulo[0][0])
##                        nome_filme = n_f[0]#nome
##                        if nome_filme in read_Filmes_File:
##                                for x in range(len(_filmes_)):
##                                        if nome_filme in _filmes_[x]:
##                                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_filmes_[x])
##                                                if _n: nomes = _n[0]
##                                                else: nomes = '---'
##                                                if nome_filme == nomes:
##                                                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_filmes_[x])
##                                                        if _i: imdbcode = _i[0]
##                                                        else: imdbcode = '---'
##                                                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_filmes_[x])
##                                                        if _t: thumb = _t[0]
##                                                        else: thumb = '---'
##                                                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_filmes_[x])
##                                                        if _a: ano_filme = _a[0]
##                                                        else: ano_filme = '---'
##                                                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_filmes_[x])
##                                                        if _f: fanart = _f[0]
##                                                        else: fanart = '---'
##                                                        _g = re.compile('[|]GENERO[|](.+?)[|]END[|]').findall(_filmes_[x])
##                                                        if _g: genre = _g[0]
##                                                        else: genre = '---'
                        try:
                        #else:
                                if thumb == '': thumb = '---'
                                if genre == '': genre = '---'
                                if sinopse == '': sinopse = '---'
                                if fanart == '---': fanart = ''
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
                                nnnn = re.compile('.+?[(](.+?)[)]').findall(nome)
                                if not nnnn: nnnn = re.compile('.+?[[](.+?)[]]').findall(nome)
                                if nnnn : nome_pesquisa = nnnn[0]
                                else: nome_pesquisa = nome
                                if imdbcode != '':
                                        try:
                                                fanart,tmdb_id,poster,sin = themoviedb_api_IMDB().fanart_and_id(str(imdbcode),ano[0].replace(' ',''))
                                                if sinopse == '': sinopse = sin
                                                if fanart == '': fanart,tmb,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano[0].replace(' ',''))
                                                if thumb == '' or 's1600' in thumb: thumb = poster
                                        except:pass
                                else:
                                        try:
                                                fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano[0].replace(' ',''))
                                                if thumb == '' or 's1600' in thumb: thumb = poster
                                        except:pass

                                #Filmes_File.write('NOME|'+str(nome_filme)+'|IMDBCODE|'+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb.replace('s72-c','s320'))+'|ANO|'+str(ano[0].replace(' ',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(genre)+'|END|\n')
                        except: pass
                        
                        if thumb == '': thumb = '---'
                        if genre == '': genre = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        
                        
                        try:
                                nome_final = '[COLOR orange]TFV | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao
                                Filmes_File.write('NOME|'+str(nome_final)+'|IMDBCODE|'+urletitulo[0][0]+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb.replace('s72-c','s320'))+'|ANO|'+str(ano[0].replace(' ',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(genre)+'|ONOME|'+str(O_Nome)+'|SINOPSE|'+str(sinopse)+'|END|\n')
##                                if "Temporada" in urletitulo[0][1] or 'Season'  in urletitulo[0][1] or 'Mini-Série' in urletitulo[0][1]:
##                                        num_mode = 42
##                                else:
##                                        num_mode = 33
##                                if 'IMDB' in imdbcode:
##                                        addDir_trailer('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+imdbcode,num_mode,thumb.replace('s72-c','s320'),sinopse,fanart.replace('w500','w1280'),ano[0].replace(' ',''),genre,O_Nome,urletitulo[0][0])
##                                else:
##                                        addDir_trailer('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',num_mode,thumb.replace('s72-c','s320'),sinopse,fanart.replace('w500','w1280'),ano[0].replace(' ',''),genre,O_Nome,urletitulo[0][0])
                        except: pass
##                        i = i + 1
##                        a = a + 1
        else: pass
        if items != []:
                proxima_TFV = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
                url_TFV = proxima_TFV[0].replace('&amp;','&')
        else: url_TFV = 'http:'
        Filmes_File.write('PAGINA|'+url_TFV+'|PAGINA')
        Filmes_File.close()
        Filmes_Fi.close()
        #----------------------------------------------------------------------------------------------------
##        site = '[B][COLOR green]MOVIE[/COLOR][COLOR yellow]-[/COLOR][COLOR red]TUGA[/COLOR][/B]'
##        progress.update( percent, 'A Procurar Filmes em '+site, message, "" )
##        i = 3
def MVTMASHUP(url):
        url_MVT = url
        percent = 0
        message = 'Por favor aguarde.'
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar Filmes...', message, "" )
        _filmes_ = []
        folder = perfil
        Filmes_File = open(folder + 'filmesMVT.txt', 'w')
        Filmes_Fi = open(folder + 'filmesMVT.txt', 'r')
        read_Filmes_File = ''
        for line in Filmes_Fi:
                read_Filmes_File = read_Filmes_File + line
                if line!='':_filmes_.append(line)
	try:
		html_source = abrir_url(url_MVT)
	except: html_source = ''
	items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
##                        percent = int( ( a / num ) * 100)
##                        message = str(a) + " de " + str(int(num))
##                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
##                        print str(a) + " de " + str(int(num))
##                        if progress.iscanceled():
##                                break

                        thumb = ''
                        genero = ''
                        sinopse = ''
                        fanart = ''
                        imdbcode = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
                        url = re.compile('<div class="btns"><a href="(.+?)" target="Player">').findall(item)
                        if 'http' not in url[0]:
                                url[0] = 'http:' + url[0]

                        snpse = re.compile("<div id='imgsinopse'>(.+?)</div>").findall(item)
                        if snpse: sinopse = snpse[0]
                        sinopse = sinopse.replace('&#8216;',"'")
                        sinopse = sinopse.replace('&#8217;',"'")
                        sinopse = sinopse.replace('&#8211;',"-")
                        sinopse = sinopse.replace('&#8220;',"'")
                        sinopse = sinopse.replace('&#8221;',"'")
                        sinopse = sinopse.replace('&#39;',"'")
                        sinopse = sinopse.replace('&amp;','&')
                        
                        gen = re.compile("nero:</strong>(.+?)</div>").findall(item)
                        if gen: genero = gen[0]
                                               
                        if 'Qualidade:' in item:
                                qualidade = re.compile("<strong>Qualidade:</strong>(.+?)</div>").findall(item)
                                qualidade_filme = qualidade[0].replace('&#8211;',"-")
                        else:
                                qualidade_filme = ''
                                
                        ano = re.compile('<strong>Lan\xc3\xa7amento:</strong>(.+?)</div>').findall(item)
                        
                        thumbnail = re.compile('src="(.+?)"').findall(item)
                        if 'http' not in thumbnail[0]: thumbnail[0] = 'http:' + thumbnail[0]
                        if thumbnail: thumb = thumbnail[0].replace('s72-c','s320')

                        titulo = re.compile("<strong>T\xc3\xadtulo original:</strong>(.+?)</div>").findall(item)
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
                        #return
                        O_Nome = nome
                        progress.update( percent, 'A Procurar Filmes......', '[COLOR green]'+O_Nome+'[/COLOR]', "" )
##                        n_f = re.compile('filmes/(.+?)[.]pt[.]vu').findall(url[0].replace(' ','%20'))
##                        nome_filme = n_f[0]#nome
##                        #return
##                        if nome_filme in read_Filmes_File:
##                                for x in range(len(_filmes_)):
##                                        if nome_filme in _filmes_[x]:
##                                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_filmes_[x])
##                                                if _n: nomes = _n[0]
##                                                else: nomes = '---'
##                                                if nome_filme == nomes:
##                                                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_filmes_[x])
##                                                        if _i: imdbcode = _i[0]
##                                                        else: imdbcode = '---'
##                                                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_filmes_[x])
##                                                        if _t: thumb = _t[0]
##                                                        else: thumb = '---'
##                                                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_filmes_[x])
##                                                        if _a: ano_filme = _a[0]
##                                                        else: ano_filme = '---'
##                                                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_filmes_[x])
##                                                        if _f: fanart = _f[0]
##                                                        else: fanart = '---'
##                                                        _g = re.compile('[|]GENERO[|](.+?)[|]END[|]').findall(_filmes_[x])
##                                                        if _g: genero = _g[0]
##                                                        else: genero = '---'
                        try:
                        #else:
                                if thumb == '': thumb = '---'
                                if genero == '': genero = '---'
                                if sinopse == '': sinopse = '---'
                                if fanart == '': fanart = '---'
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
                                if ano: ano_filme = ano[0].replace('20013','2013').replace(' ','')
                                else: ano_filme = '---'
        ##                        nnnn = re.compile('.+?[(](.+?)[)]').findall(nome)
        ##                        if not nnnn: nnnn = re.compile('.+?[[](.+?)[]]').findall(nome)
        ##                        #if not nnnn: nnnn = re.compile('(.+?)[:]').findall(nome)
        ##                        #if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
        ##                        if nnnn : nome_pesquisa = nnnn[0]
        ##                        else: nome_pesquisa = nome
                                nome_pesquisa = nome
                                if imdbcode != '':
                                        try:
                                                fanart,tmdb_id,poster,sin = themoviedb_api_IMDB().fanart_and_id(str(imdbcode),ano_filme)
                                                if sinopse == '': sinopse = sin
                                                if fanart == '': fanart,tmb,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano_filme)
                                        except:pass
                                else:
                                        try:
                                                fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano_filme)
                                        except:pass

                                #Filmes_File.write('NOME|'+str(nome_filme)+'|IMDBCODE|'+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb.replace(' ','%20'))+'|ANO|'+str(ano_filme)+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|END|\n')
                        except: pass
                        
                        if thumb == '': thumb = '---'
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        if ano: ano_filme = ano[0]
                        else: ano_filme = '---'
                        ano_filme=ano_filme.replace('20013','2013')
                        try:
                                nome_final = '[COLOR orange]MVT | [/COLOR][B][COLOR green]' + O_Nome + ' [/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]'
                                Filmes_File.write('NOME|'+str(nome_final)+'|IMDBCODE|'+url[0].replace(' ','%20')+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb.replace(' ','%20'))+'|ANO|'+str(ano_filme)+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|ONOME|'+str(O_Nome)+'|SINOPSE|'+str(sinopse)+'|END|\n')
##                                if 'IMDB' in imdbcode:
##                                        addDir_trailer('[COLOR orange]MVT | [/COLOR][B][COLOR green]' + O_Nome + ' [/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',url[0].replace(' ','%20')+imdbcode,103,thumb.replace(' ','%20'),sinopse,fanart.replace('w500','w1280').replace(' ','%20'),ano_filme,genero,O_Nome,url[0])
##                                else:
##                                        addDir_trailer('[COLOR orange]MVT | [/COLOR][B][COLOR green]' + O_Nome + ' [/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',url[0].replace(' ','%20')+'IMDB'+imdbcode+'IMDB',103,thumb.replace(' ','%20'),sinopse,fanart.replace('w500','w1280').replace(' ','%20'),ano_filme,genero,O_Nome,url[0])

                        except: pass
##                        a = a + 1
##                        i = i + 1
        else: pass
        if items != []:
                proxima_MVT = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
                try:
                        url_MVT = proxima_MVT[0].replace('%3A',':')
                        url_MVT = proxima_MVT[0].replace('&amp;','&')
                except: pass
        else: url_MVT = 'http:'
        Filmes_File.write('PAGINA|'+url_MVT+'|PAGINA')
        Filmes_File.close()
        Filmes_Fi.close()
        #----------------------------------------------------------------------------------------------------
##        site = '[B][COLOR green]CINE[/COLOR][COLOR yellow]M[/COLOR][COLOR red]ATUGA.eu[/COLOR][/B]'
##        progress.update( percent, 'A Procurar Filmes em '+site, message, "" )
##        i = 3
def CMEMASHUP(url):
        url_CME = url
        percent = 0
        message = 'Por favor aguarde.'
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar Filmes...', message, "" )
        _filmes_ = []
        folder = perfil
        Filmes_File = open(folder + 'filmesCME.txt', 'w')
        Filmes_Fi = open(folder + 'filmesCME.txt', 'r')
        read_Filmes_File = ''
        for line in Filmes_Fi:
                read_Filmes_File = read_Filmes_File + line
                if line!='':_filmes_.append(line)
        try:
		html_source = abrir_url(url_CME)
	except: html_source = ''
	items = re.findall("<h3 class='post-title entry-title'(.+?)<div class='post-outer'>", html_source, re.DOTALL)
	if items != []:
		for item in items:
##                        percent = int( ( a / num ) * 100)
##                        message = str(a) + " de " + str(int(num))
##                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
##                        print str(a) + " de " + str(int(num))
##                        if progress.iscanceled():
##                                break
                        
                        thumb = ''
                        genero = ''
                        sinopse = ''
                        fanart = ''
                        anofilme= ''
                        qualidade_filme = ''
                        imdbcode = ''
                        audio_filme = ''

                        imdb = re.compile('imdb.com/title/(.+?)"').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''

                        urletitulo = re.compile("<a href='(.+?)' title='(.+?)'>").findall(item)
                        if not urletitulo: urletitulo = re.compile("<a href='(.+?)'>(.+?)</a>").findall(item)
                        if urletitulo:
                                urlvideo = urletitulo[0][0].replace('#more','')
                                nome = urletitulo[0][1]
                        else:
                                urlvideo = ''
                                nome = ''
                                
                        snpse = re.compile('<b>sinopse</b><br>\n(.+?)<br>\n').findall(item)
                        if snpse: sinopse = snpse[0]
                        sinopse = sinopse.replace('&#8216;',"'")
                        sinopse = sinopse.replace('&#8217;',"'")
                        sinopse = sinopse.replace('&#8220;',"'")
                        sinopse = sinopse.replace('&#8221;',"'")
                        sinopse = sinopse.replace('&#8211;',"-")
                        sinopse = sinopse.replace('&#39;',"'")
                        sinopse = sinopse.replace('&amp;','&')
                                
                        ano = re.compile('<strong>Lan\xc3\xa7amento:</strong>(.+?)</div>').findall(item)
                        if ano: anofilme = ano[0]
                        else: anofilme = ''

                        generos = re.compile("rel='tag'>(.+?)</a>").findall(item)
                        conta = 0
                        for gener in generos:
                                if conta == 0:
                                        if gener.replace(' ','') != anofilme.replace(' ',''):
                                                genero = gener
                                                conta = conta + 1
                                else:
                                        if gener.replace(' ','') != anofilme.replace(' ',''):
                                                genero = genero +'  '+ gener
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(genero)
                        conta = 0
                        for q_a_q_a in qq_aa:
                                genero = genero.replace(str(q_a_q_a)+'  ','')

                        thumbnail = re.compile("<meta content='(.+?)' itemprop='image_url'/>").findall(item)
                        if not thumbnail: thumbnail = re.compile('<img class="alignleft" src="(.+?)">').findall(item)
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
                                        tirar_ano = '('+str(q_a_q_a)+')'
                                        nome = nome.replace(tirar_ano,'')

                        if audio_filme != '': qualidade_filme = qualidade_filme# + ' - ' + audio_filme

                        O_Nome = nome
                        progress.update( percent, 'A Procurar Filmes.......', '[COLOR green]'+O_Nome+'[/COLOR]', "" )
##                        n_f = re.compile('.eu/(.+?)[.]html').findall(urlvideo)
##                        nome_filme = n_f[0]#nome
##                        if nome_filme in read_Filmes_File:
##                                for x in range(len(_filmes_)):
##                                        if nome_filme in _filmes_[x]:
##                                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_filmes_[x])
##                                                if _n: nomes = _n[0]
##                                                else: nomes = '---'
##                                                if nome_filme == nomes:
##                                                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_filmes_[x])
##                                                        if _i: imdbcode = _i[0]
##                                                        else: imdbcode = '---'
##                                                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_filmes_[x])
##                                                        if _t: thumb = _t[0]
##                                                        else: thumb = '---'
##                                                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_filmes_[x])
##                                                        if _a: ano_filme = _a[0]
##                                                        else: ano_filme = '---'
##                                                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_filmes_[x])
##                                                        if _f: fanart = _f[0]
##                                                        else: fanart = '---'
##                                                        _g = re.compile('[|]GENERO[|](.+?)[|]END[|]').findall(_filmes_[x])
##                                                        if _g: genero = _g[0]
##                                                        else: genero = '---'
                        try:
                        #else:
                                if genero == '': genero = '---'
                                if sinopse == '': sinopse = '---'
                                if fanart == '---': fanart = ''
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
                                nnnn = re.compile('.+?[(](.+?)[)]').findall(nome)
                                if not nnnn: nnnn = re.compile('.+?[[](.+?)[]]').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?)[:] ').findall(nome) 
                                if nnnn :
                                        if 'Trilogia' in nnnn[0]: nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                                        nome_pesquisa = nnnn[0]
                                else: nome_pesquisa = nome
                                if imdbcode != '':
                                        try:
                                                fanart,tmdb_id,poster,sin = themoviedb_api_IMDB().fanart_and_id(str(imdbcode),anofilme)
                                                if sinopse == '': sinopse = sin
                                                if fanart == '': fanart,tmb,poster = themoviedb_api().fanart_and_id(nome_pesquisa,anofilme)
                                                if thumb == ''  or 'IMDb.png' in thumb or 'Sinopse' in thumb: thumb = poster
                                        except:pass
                                else:
                                        try:
                                                fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,anofilme)
                                                if thumb == ''  or 'IMDb.png' in thumb or 'Sinopse' in thumb: thumb = poster
                                        except: pass
                                #Filmes_File.write('NOME|'+str(nome_filme)+'|IMDBCODE|'+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb)+'|ANO|'+str(anofilme)+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|END|\n')
                        except: pass
                        
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        try:
                                nome_final = '[COLOR orange]CME | [/COLOR][B][COLOR green]' + O_Nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme.replace('</div>','') + ')[/COLOR]'
                                Filmes_File.write('NOME|'+str(nome_final)+'|IMDBCODE|'+urlvideo+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb)+'|ANO|'+str(anofilme)+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|ONOME|'+str(O_Nome)+'|SINOPSE|'+str(sinopse)+'|END|\n')
##                                if 'IMDB' in imdbcode:
##                                        addDir_trailer('[COLOR orange]CME | [/COLOR][B][COLOR green]' + O_Nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme.replace('</div>','') + ')[/COLOR]',urlvideo+imdbcode,803,thumb,sinopse,fanart,anofilme,genero,O_Nome,urlvideo)
##                                else:
##                                        addDir_trailer('[COLOR orange]CME | [/COLOR][B][COLOR green]' + O_Nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme.replace('</div>','') + ')[/COLOR]',urlvideo+'IMDB'+imdbcode+'IMDB',803,thumb,sinopse,fanart,anofilme,genero,O_Nome,urlvideo)
                        except: pass
                        #---------------------------------------------------------------
##                        i = i + 1
##                        a = a + 1
                        #---------------------------------------------------------------
        else: pass
        if items != []:
                proxima_CME = re.compile("<a class='blog-pager-older-link' href='(.+?)' id='Blog1_blog-pager-older-link'").findall(html_source)	
                try:
                        url_CME = proxima_CME[0].replace('&amp;','&')
                except: pass
	else: url_CME = 'http:'
	Filmes_File.write('PAGINA|'+url_CME+'|PAGINA')
        Filmes_File.close()
        Filmes_Fi.close()
##        return url_CME
       #----------------------------------------------------------------------------------------------------
def CMCMASHUP(url):
        i = 0
        return

def PAGSEGUINTE():	
        for x in range(len(arrai_filmes)):
                if arrai_filmes[x] != '':           #8
                        addDir(arrai_filmes[x],'url',7,thumb_filmes[x],'nao','')
                        conta_os_items = conta_os_items + 1
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "url_FTT": url_FTT, "url_CMT": url_CMT, "url_CME": url_CME, "fim": 'fim',"xpto":'xpto'}
        url_filmes_filmes = urllib.urlencode(parameters)
        progress.close()
        addDir('[B]Página Seguinte >>[/B]',url_filmes_filmes,507,artfolder + 'PAGS1.png','','')


def Series_Series(url):
        origem = url
        conta_os_items = 0
        folder = perfil
        Series_File = open(folder + 'series.txt', 'a')
        Series_Fi = open(folder + 'series.txt', 'r')
        read_Series_File = ''
        for line in Series_Fi:
                read_Series_File = read_Series_File + line
                if line!='':_series_.append(line)
        if origem == 'urlTODAS':
                percent = 0
                message = ''
                site = ''
                progress.create('Progresso', 'A Procurar')
                progress.update( percent, 'A Procurar Séries...'+site, message, "" )
        #---------------------------------------------------------------------------
        s = 0
        urltfv = 'http://www.tuga-filmes.us'
        try:
                html_series_source = abrir_url(urltfv)
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
                html_series_source = abrir_url(urltpt)
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
                html_series_source = abrir_url(urltfv)
        except: html_series_source = ''
	html_items_series = re.findall("<div class=\'widget Label\' id=\'Label3\'>\n<h2>S\xc3\xa9ries(.*?)<div class=\'clear\'>", html_series_source, re.DOTALL)
        i=0
        p=1
        for item_series in html_items_series:
                series = re.compile("<a dir=\'ltr\' href=\'(.+?)\'>(.+?)</a>").findall(item_series)
                for endereco_series,nome_series in series:
                        thumb = ''
                        fanart = ''
                        versao = ''
                        audio_filme = ''
                        imdbcode = ''
                        genre = ''
                        sinopse = ''
                        if origem == 'urlTODAS':
                                percent = int( ( p / num ) * 100)
                                message = str(p) + " de " + str(int(num))
                                progress.update( percent, 'A Procurar Séries em '+site, message, "" )
                                print str(p) + " de " + str(int(num))
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
                                #arr_series[i] = nome_series
                                for x in range(len(_series_)):
                                        if nome_series in _series_[x]:
                                                #nomeesta = re.compile(
                                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_series_[x])
                                                if _n: nome = _n[0]
                                                else: nome = '---'
                                                if nome_series in nome:
                                                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_series_[x])
                                                        if _i: imdbcode = _i[0]
                                                        else: imdbcode = '---'
                                                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_series_[x])
                                                        if _t: thumb = _t[0]
                                                        else: thumb = '---'
                                                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_series_[x])
                                                        if _a: ano_filme = _a[0]
                                                        else: ano_filme = '---'
                                                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_series_[x])
                                                        if _f: fanart = _f[0]
                                                        else: fanart = '---'
                                                        _g = re.compile('[|]GENERO[|](.+?)[|]SINOPSE[|]').findall(_series_[x])
                                                        if _g: genre = _g[0]
                                                        else: genre = '---'
                                                        _s = re.compile('[|]SINOPSE[|](.*)').findall(_series_[x])
                                                        if _s: s = _s[0]
                                                        if '|END|' in s: sinopse = s.replace('|END|','')
                                                        else:
                                                                si = re.compile('SINOPSE[|](.+?)\n(.+?)[|]END[|]').findall(_series_[x])
                                                                if si: sinopse = si[0][0] + ' ' + si[0][1]
                                                                else: sinopse = '---'
                                                        if fanart == '' or fanart == '---':
                                                                if selfAddon.getSetting('Fanart') == "true":
                                                                        nome_pesquisa = nome_series
                                                                        thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme.replace('(','').replace(')',''))
                                                                        ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                                                        if ftart: fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                                        if thumb == '' or 's1600' in thumb: thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                                                                        snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                                        if sinopse == '---':
                                                                                if snpse: sinopse = snpse[0]
                                                        todas_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|THUMB|'+thumb.replace('s72-c','s320')+'|ANO|'+ano_filme.replace('  ','').replace(' ','')+'|FANART|'+fanart+'|GENERO|'+genre+'|SINOPSE|'+sinopse+'|END|'
                                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|THUMB|'+thumb.replace('s72-c','s320')+'|ANO|'+ano_filme.replace('  ','').replace(' ','')+'|FANART|'+fanart+'|GENERO|'+genre+'|SINOPSE|'+sinopse+'|END|'
                                                        arr_series[i] = nome_series
                                                        
                                                                        
                        else:
                                #return
                                try:
                                        html_source = abrir_url(endereco_series)
                                except: html_source = ''
                                items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
                                thumb = ''
                                fanart = ''
                                versao = ''
                                audio_filme = ''
                                imdbcode = ''
                                genre = ''
                                sinopse = ''
                                

                                imdb = re.compile('imdb.com/title/(.+?)/').findall(items[0])
                                if imdb: imdbcode = imdb[0]
                                else: imdbcode = ''
                                #return
                                try:
                                        if 'Portug' and 'Legendado' in items[0]: versao = '[COLOR blue]2 VERSÕES[/COLOR]'
                                        genero = re.compile("nero</b>:(.+?)<br />").findall(items[0])
                                        if genero: genre = genero[0]
                                        else: genre = ''
                                        resumo = re.compile("<b>Resumo</b>:(.+?)<br />").findall(items[0])
                                        if resumo: sinopse = resumo[0]
                                        else: sinopse = ''
                                        sinopse = sinopse.replace('&#8216;',"'")
                                        sinopse = sinopse.replace('&#8217;',"'")
                                        sinopse = sinopse.replace('&#8211;',"-")
                                        sinopse = sinopse.replace('&#8220;',"'")
                                        sinopse = sinopse.replace('&#8221;',"'")
                                        sinopse = sinopse.replace('&#39;',"'")
                                        sinopse = sinopse.replace('&amp;','&')
                                        #return
                                        titulooriginal = re.compile("tulo Original:</b>(.+?)<br />").findall(items[0])
                                        if titulooriginal:
                                                nome_original = titulooriginal[0]
                                        else:
                                                titulooriginal = re.compile("<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>(.+?)<br />").findall(items[0])
                                                if titulooriginal:
                                                        nome_original = titulooriginal[0]
                                                else: nome_original = ''
                                        urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(items[0])

                                        tto=re.compile('tulo Original:</b>:(.+?)<br').findall(items[0])
                                        if tto: ttor = tto[0]
                                        else:
                                                tto=re.compile('tulo Original:</b>(.+?)<br').findall(items[0])
                                                if tto: ttor = tto[0]
                                        ttp=re.compile('<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>:(.+?)<br').findall(items[0])
                                        if ttp: ttpo = ttp[0]
                                        else:
                                                ttp=re.compile('<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>(.+?)<br').findall(items[0])
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
                                        
                                        qualidade = re.compile("<b>Qualidade</b>: (.+?)<br />").findall(items[0])
                                        ano = re.compile("<b>Ano</b>: (.+?)<br />").findall(items[0])
                                        audio = re.compile("<b>.+?udio</b>(.+?)<br />").findall(items[0])
                                        imdb_code = re.compile('<b>Mais INFO</b>: <a href="http://www.imdb.com/title/(.+?)/" target="_blank">IMDb</a>').findall(items[0])
                                        if audio != []:
                                                if 'Portug' in audio[0]:
                                                        audio_filme = ': PT-PT'
                                                else:
                                                        audio_filme = audio[0]
                                        thumbnail = re.compile('src="(.+?)"').findall(items[0])
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
                                                        
                                        if ano: ano_filme = ano[0]
                                        else: ano_filme = '---'
                                        
                                        if selfAddon.getSetting('Fanart') == "true":
                                                nome_pesquisa = nome_series
                                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme.replace('(','').replace(')',''))
                                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                                if ftart: fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                if thumb == '' or 's1600' in thumb: thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                if snpse and sinopse == '': sinopse = snpse[0]

                                        if qualidade:
                                                qualidade = qualidade[0]
                                        else:
                                                qualidade = ''
                                        
                                        if genre == '': genre = '---'
                                        if sinopse == '': sinopse = '---'
                                        if fanart == '': fanart = '---'
                                        if imdbcode == '': imdbcode = '---'
                                        if thumb == '': thumb = '---'
                                        #Series_File.write('NOME|'+nome_series+'|SINOPSE|'+sinopse+'|END|\n')
                                        Series_File.write('NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb.replace('s72-c','s320')+'|ANO|'+ano_filme.replace('  ','').replace(' ','')+'|FANART|'+fanart+'|GENERO|'+genre+'|SINOPSE|'+sinopse+'|END|\n')
                                except: pass
                        #if nome_series in arr_series:
                                #arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|THUMB|'+thumb.replace('s72-c','s320')+'|ANO|'+ano_filme.replace('  ','').replace(' ','')+'|FANART|'+fanart+'|GENERO|'+genre+'|SINOPSE|'+sinopse+'|END|'
                        if genre == '': genre = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '': fanart = '---'
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        if nome_series not in arr_series:
                                if fanart == '' or fanart == '---':
                                        if selfAddon.getSetting('Fanart') == "true":
                                                nome_pesquisa = nome_series
                                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme.replace('(','').replace(')',''))
                                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                                if ftart: fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                if thumb == '' or 's1600' in thumb: thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                if sinopse == '---':
                                                        if snpse: sinopse = snpse[0]
                                arr_series[i] = nome_series
                                if 'IMDB' in imdbcode:
                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|'+endereco_series+'|THUMB|'+thumb.replace('s72-c','s320')+'|ANO|'+ano_filme.replace('  ','').replace(' ','')+'|FANART|'+fanart+'|GENERO|'+genre+'|SINOPSE|'+sinopse+'|END|'
                                        todas_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|'+endereco_series+'|THUMB|'+thumb.replace('s72-c','s320')+'|ANO|'+ano_filme.replace('  ','').replace(' ','')+'|FANART|'+fanart+'|GENERO|'+genre+'|SINOPSE|'+sinopse+'|END|'
                                else:
                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb.replace('s72-c','s320')+'|ANO|'+ano_filme.replace('  ','').replace(' ','')+'|FANART|'+fanart+'|GENERO|'+genre+'|SINOPSE|'+sinopse+'|END|'
                                        todas_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb.replace('s72-c','s320')+'|ANO|'+ano_filme.replace('  ','').replace(' ','')+'|FANART|'+fanart+'|GENERO|'+genre+'|SINOPSE|'+sinopse+'|END|'                                
                        i = i + 1
                        p = p + 1
        Series_Fi.close()
        Series_File.close()
        #return
        Series_File = open(folder + 'series.txt', 'a')
        Series_Fi = open(folder + 'series.txt', 'r')
        read_Series_File = ''
        for line in Series_Fi:
                read_Series_File = read_Series_File + line
                if line!='':_series_.append(line)
        url = 'http://toppt.net/'
        site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
        try:
                html_series_source = abrir_url(url)
        except: html_series_source = ''
	html_items_series = re.findall('<a href="http://toppt.net/category/series/">SÈRIES NOVAS</a>(.*?)<div class="clearfix">', html_series_source, re.DOTALL)
        print len(html_items_series)
        for item_series in html_items_series:
                series = re.compile('<a href="(.+?)">(.+?)</a>').findall(item_series)
                for endereco_series,nome_series in series:
                        genero = ''
                        sinopse = ''
                        fanart = ''
                        thumb = ''
                        qualidade = ''
                        imdbcode = ''
                        audio_filme = ''
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        nome_series = nome_series.replace('&#8217;',"'")
                        nome_series = nome_series.replace('&#8230;',"...")
                        nome_series = nome_series.replace('&#8211;',"-")
                        nome_series = nome_series.replace('NCIS ',"NCIS:")
                        nome_series = nome_series.replace('Da Vincis Demons',"Da Vinci'S Demons")
                        nome_series = nome_series.lower()
                        nome_series = nome_series.title()
                        ##########################################################
                        if nome_series in read_Series_File:
                                #arr_series[i] = nome_series
                                for x in range(len(_series_)):
                                        if nome_series in _series_[x]:
                                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_series_[x])
                                                if _n: nome = _n[0]
                                                else: nome = '---'
                                                if nome_series in nome:
                                                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_series_[x])
                                                        if _i: imdbcode = _i[0]
                                                        else: imdbcode = '---'
                                                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_series_[x])
                                                        if _t: thumb = _t[0]
                                                        else: thumb = '---'
                                                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_series_[x])
                                                        if _a: ano_filme = _a[0]
                                                        else: ano_filme = '---'
                                                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_series_[x])
                                                        if _f: fanart = _f[0]
                                                        else: fanart = '---'
                                                        _g = re.compile('[|]GENERO[|](.+?)[|]SINOPSE[|]').findall(_series_[x])
                                                        if _g: genero = _g[0]
                                                        else: genero = '---'
                                                        _s = re.compile('[|]SINOPSE[|](.*)').findall(_series_[x])
                                                        if _s: s = _s[0]
                                                        if '|END|' in s: sinopse = s.replace('|END|','')
                                                        else:
                                                                si = re.compile('SINOPSE[|](.+?)\n(.+?)[|]END[|]').findall(_series_[x])
                                                                if si: sinopse = si[0][0] + ' ' + si[0][1]
                                                                else: sinopse = '---'
                                                        #arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                                        #arr_series[i] = nome_series
                        else:
                                try:
                                        html_source = abrir_url(endereco_series)
                                except: html_source = ''
                                items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
                                genero = ''
                                sinopse = ''
                                fanart = ''
                                thumb = ''
                                qualidade = ''
                                imdbcode = ''
                                audio_filme = ''

                                imdb = re.compile('imdb.com/title/(.+?)/').findall(items[0])
                                if imdb: imdbcode = imdb[0]
                                else: imdbcode = ''

                                try:
                                        urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(items[0])
                                        if 'title=' in urletitulo[0][0]: urletitulo = re.compile('<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>').findall(items[0])
                                        
                                        qualid = re.compile("<b>QUALIDADE:.+?/b>(.+?)<br/>").findall(items[0])
                                        if not qualid: qualid = re.compile("<b>VERSÃO:.+?</b>(.+?)<br/>").findall(items[0])
                                        if qualid:
                                                qualidade = qualid[0]
                                                qualidade = qualidade.replace('[',' - ')
                                                qualidade = qualidade.replace(']','')
                                        else:
                                                qualid = re.compile("\nQUALIDADE:\xc2\xa0(.+?)<br/>").findall(items[0])
                                                if qualid:
                                                        qualidade = qualid[0]
                                                        qualidade = qualidade.replace('[',' - ')
                                                        qualidade = qualidade.replace(']','')
                                                else:
                                                        qualid = re.compile("<b>VERS.+?</b>(.+?)<br/>").findall(items[0])
                                                        if qualid:
                                                                qualidade = qualid[0]
                                                                qualidade = qualidade.replace('[',' - ')
                                                                qualidade = qualidade.replace(']','')
                                                        else:
                                                                qualidade = ''

                                        genr = re.compile("NERO:.+?/b>(.+?)<br/>").findall(items[0])
                                        if genr: genero = genr[0]
                                        
                                        ano = re.compile("<b>ANO:.+?/b>(.+?)<br/>").findall(items[0])
                                        audio = re.compile("<b>AUDIO:.+?/b>(.+?)<br/>").findall(items[0])
                                        thumbnail = re.compile('src="(.+?)"').findall(items[0])
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
                                                        audio = re.compile('<b>AUDIO: </b>(.+?)<span style="color: red;"><b>(.+?)</b></span><br/>').findall(items[0])
                                                        if audio:
                                                                audio_filme = ': ' + audio[0][0] + audio[0][1]
                                                        else:
                                                                audio = re.compile('<b>AUDIO: </b> <b><span style="color: red;">(.+?)</span> <span style="color: #38761d;">(.+?)</span></b><br/>').findall(items[0])
                                                                if audio:
                                                                        audio_filme = audio[0][0] + audio[0][1]
                                                                        if 'Portug' or 'PORTUG' in audio_filme:
                                                                                audio_filme = ': PT-PT'
                                                                else:
                                                                        audio = re.compile('<b>AUDIO:.+?<strong>(.+?)</strong>').findall(items[0])
                                                                        if audio:
                                                                                audio_filme = audio[0][0] + audio[0][1]
                                                                                if 'Portug' or 'PORTUG' in audio_filme:
                                                                                        audio_filme = ': PT-PT'
                                                else:
                                                        audio_filme = ': ' + audio[0]
                                        if not audio:
                                                audio = re.compile("\nAUDIO:\xc2\xa0(.+?)<br/>").findall(items[0])
                                                if audio:
                                                        audio_filme = ': ' + audio[0]
                                                else:
                                                        audio_filme = ''
                                        if not ano:
                                                ano = re.compile("\nANO:\xc2\xa0(.+?)<br/>").findall(items[0])
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
                                        
                                        a_q = re.compile('\d+')
                                        qq_aa = a_q.findall(nome)
                                        for q_a_q_a in qq_aa:
                                                if len(q_a_q_a) == 4:
                                                        tirar_ano = '(' + str(q_a_q_a) + ')'
                                                        nome = nome.replace(tirar_ano,'')
                                                        
                                        if selfAddon.getSetting('Fanart') == "true":
                                                nome_pesquisa = nome_series
                                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme)
                                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                                if ftart: fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                if snpse and sinopse == '': sinopse = snpse[0]
                                
                                        ano_filme = '('+ano_filme+')'
                                        qualidade = '('+qualidade
                                        audio_filme = audio_filme+')'
                                        if genero == '': genero = '---'
                                        if sinopse == '': sinopse = '---'
                                        if fanart == '': fanart = '---'
                                        if imdbcode == '': imdbcode = '---'
                                        if thumb == '': thumb = '---'
                                        #Series_File.write('NOME|'+nome_series+'|SINOPSE|'+sinopse+'|END|\n')
                                        Series_File.write('NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|\n')
                                except: pass
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '': fanart = '---'
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        if nome_series in arr_series:
                                _imdb = re.compile('[|]IMDBCODE[|](.+?)[|](.+?)[|](.+?)[|]THUMB[|]').findall(arrai_series[arr_series.index(nome_series)])
                                if not _imdb:
                                        _imdb = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(arrai_series[arr_series.index(nome_series)])
                                        if _imdb:
                                                if 'toppt' not in _imdb[0]:
                                                        imdb = _imdb[0]
                                                        arrai_series[arr_series.index(nome_series)]=arrai_series[arr_series.index(nome_series)].replace(imdb,imdb+'|'+endereco_series)
                                                        todas_series[arr_series.index(nome_series)]=todas_series[arr_series.index(nome_series)].replace(imdb,imdb+'|'+endereco_series)

                        if nome_series not in arr_series:
                                if origem == 'urlTODAS':
                                        percent = int( ( p / num ) * 100)
                                        message = str(p) + " de " + str(int(num))
                                        progress.update( percent, 'A Procurar Séries em '+site, message, "" )
                                        print str(p) + " de " + str(int(num))
                                        if progress.iscanceled():
                                                break
                                if fanart == '' or fanart == '---':
                                        if selfAddon.getSetting('Fanart') == "true":
                                                nome_pesquisa = nome_series
                                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme.replace('(','').replace(')',''))
                                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                                if ftart: fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                if sinopse == '---':
                                                        if snpse: sinopse = snpse[0]
                                arr_series[i] = nome_series
                                if 'IMDB' in imdbcode:
                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                        todas_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                else:
                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                        todas_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                i = i + 1
                                p = p + 1
        Series_Fi.close()
        Series_File.close()
        #return
        Series_File = open(folder + 'series.txt', 'a')
        Series_Fi = open(folder + 'series.txt', 'r')
        read_Series_File = ''
        for line in Series_Fi:
                read_Series_File = read_Series_File + line
                if line!='':_series_.append(line)
        html_items_series = re.findall('href="http://toppt.net/category/series/">SÉRIES</a>(.*?)<div id="main">', html_series_source, re.DOTALL)
        print len(html_items_series)
        for item_series in html_items_series:
                series = re.compile('<a href="(.+?)">(.+?)</a>').findall(item_series)
                for endereco_series,nome_series in series:
                        genero = ''
                        sinopse = ''
                        fanart = ''
                        thumb = ''
                        qualidade = ''
                        imdbcode = ''
                        audio_filme = ''
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        nome_series = nome_series.replace('&#8217;',"'")
                        nome_series = nome_series.replace('&#8230;',"...")
                        nome_series = nome_series.replace('&#8211;',"-")
                        nome_series = nome_series.replace('NCIS ',"NCIS:")
                        nome_series = nome_series.replace('Da Vincis Demons',"Da Vinci'S Demons")
                        nome_series = nome_series.lower()
                        nome_series = nome_series.title()
                        if nome_series in read_Series_File:
                                #arr_series[i] = nome_series
                                for x in range(len(_series_)):
                                        if nome_series in _series_[x]:
                                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_series_[x])
                                                if _n: nome = _n[0]
                                                else: nome = '---'
                                                if nome_series in nome:
                                                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_series_[x])
                                                        if _i: imdbcode = _i[0]
                                                        else: imdbcode = '---'
                                                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_series_[x])
                                                        if _t: thumb = _t[0]
                                                        else: thumb = '---'
                                                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_series_[x])
                                                        if _a: ano_filme = _a[0]
                                                        else: ano_filme = '---'
                                                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_series_[x])
                                                        if _f: fanart = _f[0]
                                                        else: fanart = '---'
                                                        _g = re.compile('[|]GENERO[|](.+?)[|]SINOPSE[|]').findall(_series_[x])
                                                        if _g: genero = _g[0]
                                                        else: genero = '---'
                                                        _s = re.compile('[|]SINOPSE[|](.*)').findall(_series_[x])
                                                        if _s: s = _s[0]
                                                        if '|END|' in s: sinopse = s.replace('|END|','')
                                                        else:
                                                                si = re.compile('SINOPSE[|](.+?)\n(.+?)[|]END[|]').findall(arrai_series[x])
                                                                if si: sinopse = si[0][0] + ' ' + si[0][1]
                                                                else: sinopse = '---'
                                                        #arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                                        #arr_series[i] = nome_series
                        else:
                                try:
                                        html_source = abrir_url(endereco_series)
                                except: html_source = ''
                                items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
                                genero = ''
                                sinopse = ''
                                fanart = ''
                                thumb = ''
                                qualidade = ''
                                imdbcode = ''
                                audio_filme = ''

                                imdb = re.compile('imdb.com/title/(.+?)/').findall(items[0])
                                if imdb: imdbcode = imdb[0]
                                else: imdbcode = ''

                                try:
                                        urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(items[0])
                                        if 'title=' in urletitulo[0][0]: urletitulo = re.compile('<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>').findall(items[0])
                                        
                                        qualid = re.compile("<b>QUALIDADE:.+?/b>(.+?)<br/>").findall(items[0])
                                        if not qualid: qualid = re.compile("<b>VERSÃO:.+?</b>(.+?)<br/>").findall(items[0])
                                        if qualid:
                                                qualidade = qualid[0]
                                                qualidade = qualidade.replace('[',' - ')
                                                qualidade = qualidade.replace(']','')
                                        else:
                                                qualid = re.compile("\nQUALIDADE:\xc2\xa0(.+?)<br/>").findall(items[0])
                                                if qualid:
                                                        qualidade = qualid[0]
                                                        qualidade = qualidade.replace('[',' - ')
                                                        qualidade = qualidade.replace(']','')
                                                else:
                                                        qualid = re.compile("<b>VERS.+?</b>(.+?)<br/>").findall(items[0])
                                                        if qualid:
                                                                qualidade = qualid[0]
                                                                qualidade = qualidade.replace('[',' - ')
                                                                qualidade = qualidade.replace(']','')
                                                        else:
                                                                qualidade = ''

                                        genr = re.compile("NERO:.+?/b>(.+?)<br/>").findall(items[0])
                                        if genr: genero = genr[0]
                                        
                                        ano = re.compile("<b>ANO:.+?/b>(.+?)<br/>").findall(items[0])
                                        audio = re.compile("<b>AUDIO:.+?/b>(.+?)<br/>").findall(items[0])
                                        thumbnail = re.compile('src="(.+?)"').findall(items[0])
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
                                                        audio = re.compile('<b>AUDIO: </b>(.+?)<span style="color: red;"><b>(.+?)</b></span><br/>').findall(items[0])
                                                        if audio:
                                                                audio_filme = ': ' + audio[0][0] + audio[0][1]
                                                        else:
                                                                audio = re.compile('<b>AUDIO: </b> <b><span style="color: red;">(.+?)</span> <span style="color: #38761d;">(.+?)</span></b><br/>').findall(items[0])
                                                                if audio:
                                                                        audio_filme = audio[0][0] + audio[0][1]
                                                                        if 'Portug' or 'PORTUG' in audio_filme:
                                                                                audio_filme = ': PT-PT'
                                                                else:
                                                                        audio = re.compile('<b>AUDIO:.+?<strong>(.+?)</strong>').findall(items[0])
                                                                        if audio:
                                                                                audio_filme = audio[0][0] + audio[0][1]
                                                                                if 'Portug' or 'PORTUG' in audio_filme:
                                                                                        audio_filme = ': PT-PT'
                                                else:
                                                        audio_filme = ': ' + audio[0]
                                        if not audio:
                                                audio = re.compile("\nAUDIO:\xc2\xa0(.+?)<br/>").findall(items[0])
                                                if audio:
                                                        audio_filme = ': ' + audio[0]
                                                else:
                                                        audio_filme = ''
                                        if not ano:
                                                ano = re.compile("\nANO:\xc2\xa0(.+?)<br/>").findall(items[0])
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
                                        
                                        a_q = re.compile('\d+')
                                        qq_aa = a_q.findall(nome)
                                        for q_a_q_a in qq_aa:
                                                if len(q_a_q_a) == 4:
                                                        tirar_ano = '(' + str(q_a_q_a) + ')'
                                                        nome = nome.replace(tirar_ano,'')
                                                        
                                        if selfAddon.getSetting('Fanart') == "true":
                                                nome_pesquisa = nome_series
                                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme)
                                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                                if ftart: fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                if snpse and sinopse == '': sinopse = snpse[0]
                                                
                                        ano_filme = '('+ano_filme+')'
                                        qualidade = '('+qualidade
                                        audio_filme = audio_filme+')'
                                        if genero == '': genero = '---'
                                        if sinopse == '': sinopse = '---'
                                        if fanart == '': fanart = '---'
                                        if imdbcode == '': imdbcode = '---'
                                        if thumb == '': thumb = '---'
                                        #Series_File.write('NOME|'+nome_series+'|SINOPSE|'+sinopse+'|END|\n')
                                        Series_File.write('NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|\n')
                                except:pass
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '': fanart = '---'
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        if nome_series in arr_series:
                                _imdb = re.compile('[|]IMDBCODE[|](.+?)[|](.+?)[|](.+?)[|]THUMB[|]').findall(arrai_series[arr_series.index(nome_series)])
                                if not _imdb:
                                        _imdb = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(arrai_series[arr_series.index(nome_series)])
                                        if _imdb:
                                                if 'toppt' not in _imdb[0]:
                                                        imdb = _imdb[0]
                                                        arrai_series[arr_series.index(nome_series)]=arrai_series[arr_series.index(nome_series)].replace(imdb,imdb+'|'+endereco_series)
                                                        todas_series[arr_series.index(nome_series)]=todas_series[arr_series.index(nome_series)].replace(imdb,imdb+'|'+endereco_series)

                        if nome_series not in arr_series:
                                if origem == 'urlTODAS': 
                                        percent = int( ( p / num ) * 100)
                                        message = str(p) + " de " + str(int(num))
                                        progress.update( percent, 'A Procurar Séries em '+site, message, "" )
                                        print str(p) + " de " + str(int(num))
                                        if progress.iscanceled():
                                                break
                                if fanart == '' or fanart == '---':
                                        if selfAddon.getSetting('Fanart') == "true":
                                                nome_pesquisa = nome_series
                                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme.replace('(','').replace(')',''))
                                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                                if ftart: fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                if sinopse == '---':
                                                        if snpse: sinopse = snpse[0]
                                arr_series[i] = nome_series
                                if 'IMDB' in imdbcode:
                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                        todas_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                else:
                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                        todas_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                i = i + 1
                                p = p + 1
        if origem == 'urlTFV' or origem == 'urlTPT':
                todas_series.sort()
                SeriesFile = open(folder + 'series.txt', 'w')
                for x in range(len(todas_series)):
                        if todas_series[x] != '': SeriesFile.write(todas_series[x]+'\n')
                SeriesFile.close()
                Series_Fi.close()
                Series_File.close()
                return
        arrai_series.sort()
        a = 1
        for x in range(len(arrai_series)):
                if arrai_series[x] != '':
                        _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(arrai_series[x])
                        if _n: nome = _n[0]
                        else: nome = '---'
                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(arrai_series[x])
                        if _i: imdbcode = _i[0]
                        else: imdbcode = '---'
                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(arrai_series[x])
                        if _t: thumb = _t[0]
                        else: thumb = '---'
                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(arrai_series[x])
                        if _a: ano = _a[0]
                        else: ano = '---'
                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(arrai_series[x])
                        if _f:
                                if fanart == '---': fanart == ''
                                else: fanart = _f[0]
                        else: fanart = ''
                        _g = re.compile('[|]GENERO[|](.+?)[|]SINOPSE[|]').findall(arrai_series[x])
                        if _g: genero = _g[0]
                        else: genero = '---'
                        _s = re.compile('[|]SINOPSE[|](.*)').findall(arrai_series[x])
                        if _s: s = _s[0]
                        if '|END|' in s: sinopse = s.replace('|END|','')
                        else:
                                si = re.compile('SINOPSE[|](.+?)\n(.+?)[|]END[|]').findall(arrai_series[x])
                                if si: sinopse = si[0][0] + ' ' + si[0][1]
                                else: sinopse = '---'
                        urltrailer = re.compile('IMDB.+?IMDB[|](.+?)[|].+?').findall(imdbcode)
                        if urltrailer: urltrailer = urltrailer[0]
                        else:
                                urltrailer = re.compile('IMDB.+?IMDB[|](.+?)').findall(imdbcode)
                                if urltrailer: urltrailer = urltrailer[0]
                        if fanart == '---': fanart = ''
                        addDir_trailer('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR]',imdbcode,3006,thumb,sinopse,fanart.replace('w500','w1280'),ano,genero,nome,urltrailer)
        todas_series.sort()
        SeriesFile = open(folder + 'series.txt', 'w')
        for x in range(len(todas_series)):
                if todas_series[x] != '': SeriesFile.write(todas_series[x]+'\n')
        SeriesFile.close()
        Series_Fi.close()
        Series_File.close()
        progress.close()


#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
          
params=get_params()
url=None
name=None
mode=None
checker=None
iconimage=None
fanart=None
year=None
plot=None
genre=None
episod=None
air=None
namet=None
urltrailer=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: urltrailer=urllib.unquote_plus(params["urltrailer"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: namet=urllib.unquote_plus(params["namet"])
except: pass
try: nome=urllib.unquote_plus(params["nome"])
except: pass
try: mode=int(params["mode"])
except: pass
try: checker=urllib.unquote_plus(params["checker"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: fanart=urllib.unquote_plus(params["fanart"])
except: pass
try: plot=urllib.unquote_plus(params["plot"])
except: pass
try: year=urllib.unquote_plus(params["year"])
except: pass
try: genre=urllib.unquote_plus(params["genre"])
except: pass
try: episod=urllib.unquote_plus(params["episod"])
except: pass
try: air=urllib.unquote_plus(params["air"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Checker: "+str(checker)
print "Iconimage: "+str(iconimage)
print "Plot: "+str(plot)
print "Year: "+str(year)
print "Genre: "+str(genre)
print "Fanart: "+str(fanart)
print "Episode: "+str(episod)
print "Namet: "+str(namet)
print "Urltrailer: "+str(urltrailer)


