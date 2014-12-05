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



import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,threading
import TopPt,TugaFilmesTV,TugaFilmesCom,MovieTuga,FoitaTuga,Cinematuga,CinematugaEu,CinemaEmCasa

from Funcoes import thetvdb_api, themoviedb_api, themoviedb_api_tv, theomapi_api, themoviedb_api_IMDB, themoviedb_api_IMDB_episodios, themoviedb_api_TMDB
from Funcoes import thetvdb_api_tvdbid, thetvdb_api_episodes, themoviedb_api_search_imdbcode, themoviedb_api_pagina, themoviedb_api_IMDB1, theomapi_api_nome
from Funcoes import addDir, addDir1, addDir2, addLink, addLink1, addDir_teste, addDir_trailer, addDir_episode
from Funcoes import get_params,abrir_url

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def FILMES_ANIMACAO_pesquisar(nome_pesquisa,nomesite,url):
        #antes_de = nome_pesquisa
        nome_pp = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]][[]COLOR yellow[]].+?[[]/COLOR[]]').findall(nome_pesquisa)
        if nome_pp: nome_pesquisa = nome_pp[0]
        imdb = re.compile('IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        pesquisa_imdb = nome_pesquisa
        pp = nome_pesquisa
        progress = xbmcgui.DialogProgress()
        percent = 0
        message = 'Por favor aguarde'
        site = ''
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar...'+site, message, "" )
        #n_pesquisa = re.compile('(.+?)[(].+?[)]').findall(nome_pesquisa)
        #if n_pesquisa: nome_pesquisa = n_pesquisa[0]
##        pesquisou = nome_pesquisa
##        if '-' in nome_pesquisa:
##                nome_p = re.compile('.+?[-](.+?)').findall(nome_pesquisa)
##                if len(nome_p[0])>2:
##                        nome_pesquisa = nome_p[0]
##        else:
##                if ':' in nome_pesquisa:
##                        nome_p = re.compile('(.+?)[:].+?').findall(nome_pesquisa)
##                        nome_pesquisa = nome_p[0]
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
        nome_pesquisa = nome_pesquisa.lower()
        pesquisou = nome_pesquisa
        conta = 0
        if '.' not in nome_pesquisa:
                a_q = re.compile('\w+')
                qq_aa = a_q.findall(nome_pesquisa)
                nome_pesquisa = ''
                for q_a_q_a in qq_aa:
                        if len(q_a_q_a) > 0 or q_a_q_a == '1' or q_a_q_a == '2' or q_a_q_a == '3' or q_a_q_a == '4'or q_a_q_a == '5' or q_a_q_a == '6':
                        #if len(q_a_q_a) > 1:
                                if conta == 0:
                                        nome_pesquisa = q_a_q_a
                                        conta = 1
                                else:
                                        nome_pesquisa = nome_pesquisa + '+' + q_a_q_a
        nome_pesquisa = nome_pesquisa.lower()
        nome_pesquisa = nome_pesquisa.replace('  ','')
        encode=urllib.quote(nome_pesquisa)
 
        a = 0
        site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
	percent = int( ( a / 8.0 ) * 100)
        message = ''
        progress.update(percent, 'A Procurar em '+site, message, "")
        print str(a) + " de " + str(int(a))
	url_pesquisa = 'http://toppt.net/?s=' + str(encode) + 'IMDB'+imdbcode+'IMDB'	
	if nomesite != 'TPT': FILMES_ANIMACAO_encontrar_fontes_filmes_TPT(url_pesquisa,pesquisou)
##                TPT = threading.Thread(name='TPT', target=FILMES_ANIMACAO_encontrar_fontes_filmes_TPT , args=(url_pesquisa,pesquisou,))
##                TPT.start()

	a = 1
	site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].com'
	percent = int( ( a / 8.0 ) * 100)
        message = ''
        progress.update(percent, 'A Procurar em '+site, message, "")
        print str(a) + " de " + str(int(a))
	url_pesquisa = 'http://www.tuga-filmes.info/search?q=' + str(encode) + 'IMDB'+imdbcode+'IMDB'	
	if nomesite != 'TFC': FILMES_ANIMACAO_encontrar_fontes_filmes_TFC(url_pesquisa,pesquisou)
##                TFC = threading.Thread(name='TFC', target=FILMES_ANIMACAO_encontrar_fontes_filmes_TFC , args=(url_pesquisa,pesquisou,))
##                TFC.start()
                
	a = 2
	site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv'
        percent = int( ( a / 8.0 ) * 100)
        message = ''
        progress.update(percent, 'A Procurar em '+site, message, "")
        print str(a) + " de " + str(int(a))
	url_pesquisa = 'http://www.tuga-filmes.us/search?q=' + str(encode) + 'IMDB'+imdbcode+'IMDB'	
	if nomesite != 'TFV': FILMES_ANIMACAO_encontrar_fontes_pesquisa_TFV(url_pesquisa,pesquisou)
##                TFV = threading.Thread(name='TFV', target=FILMES_ANIMACAO_encontrar_fontes_pesquisa_TFV , args=(url_pesquisa,pesquisou,))
##                TFV.start()
	
	a = 3
	site = '[B][COLOR green]CINE[/COLOR][COLOR yellow]M[/COLOR][COLOR red]ATUGA.eu[/COLOR][/B]'
	percent = int( ( a / 8.0 ) * 100)
        message = ''
        progress.update(percent, 'A Procurar em '+site, message, "")
        print str(a) + " de " + str(int(a))
	url_pesquisa = 'http://www.cinematuga.eu/search?q=' + str(encode) + 'IMDB'+imdbcode+'IMDB'
	if nomesite != 'CME': FILMES_ANIMACAO_encontrar_fontes_filmes_CME(url_pesquisa,pesquisou)
##                CME = threading.Thread(name='CME', target=FILMES_ANIMACAO_encontrar_fontes_filmes_CME , args=(url_pesquisa,pesquisou,))
##                CME.start()

	a = 4
	site = '[B][COLOR green]FOIT[/COLOR][COLOR yellow]A[/COLOR][COLOR red]TUGA[/COLOR][/B]'
	percent = int( ( a / 8.0 ) * 100)
        message = ''
        progress.update(percent, 'A Procurar em '+site, message, "")
        print str(a) + " de " + str(int(a))
	url_pesquisa = 'http://foitatugacinemaonline.blogspot.pt/search?q=' + str(encode) + '&submit=Buscar' + 'IMDB'+imdbcode+'IMDB'	
	if nomesite != 'FTT': FILMES_ANIMACAO_encontrar_fontes_pesquisa_FTT(url_pesquisa)
##                FTT = threading.Thread(name='FTT', target=FILMES_ANIMACAO_encontrar_fontes_pesquisa_FTT , args=(url_pesquisa,))
##                FTT.start()

	a = 5
	site = '[B][COLOR green]CINE[/COLOR][COLOR yellow]M[/COLOR][COLOR red]ATUGA.net[/COLOR][/B]'
	percent = int( ( a / 8.0 ) * 100)
        message = ''
        progress.update(percent, 'A Procurar em '+site, message, "")
        print str(a) + " de " + str(int(a))
	url_pesquisa = 'http://www.cinematuga.net/search?q=' + str(encode) + 'IMDB'+imdbcode+'IMDB'	
	if nomesite != 'CMT': FILMES_ANIMACAO_encontrar_fontes_pesquisa_CMT(url_pesquisa,pesquisou)
##                CMT = threading.Thread(name='CMT', target=FILMES_ANIMACAO_encontrar_fontes_pesquisa_CMT , args=(url_pesquisa,pesquisou,))
##                CMT.start()

	a = 6
	site = '[B][COLOR green]MOVIE[/COLOR][COLOR yellow]-[/COLOR][COLOR red]TUGA[/COLOR][/B]'
	percent = int( ( a / 8.0 ) * 100)
        message = ''
        progress.update(percent, 'A Procurar em '+site, message, "")
        print str(a) + " de " + str(int(a))
	url_pesquisa = 'http://www.movie-tuga.blogspot.pt/search?q=' + str(encode) + 'IMDB'+imdbcode+'IMDB'	
	if nomesite != 'MVT': FILMES_ANIMACAO_encontrar_fontes_pesquisa_MVT(url_pesquisa)
##                MVT = threading.Thread(name='MVT', target=FILMES_ANIMACAO_encontrar_fontes_pesquisa_MVT , args=(url_pesquisa,))
##                MVT.start()
                
	a = 7
	site = '[B][COLOR green]CINEM[/COLOR][COLOR yellow]A[/COLOR][COLOR red]EMCASA[/COLOR][/B]'
	percent = int( ( a / 8.0 ) * 100)
        message = ''
        progress.update(percent, 'A Procurar em '+site, message, "")
        print str(a) + " de " + str(int(a))
	url_pesquisa = 'http://www.cinemaemcasa.pt/search?q=' + str(encode) + 'IMDB'+imdbcode+'IMDB'
	if nomesite != 'CMC': FILMES_ANIMACAO_encontrar_fontes_filmes_CMC(url_pesquisa,pesquisou)
##                CMC = threading.Thread(name='CMC', target=FILMES_ANIMACAO_encontrar_fontes_filmes_CMC , args=(url_pesquisa,pesquisou,))
##                CMC.start()
	
        a = 8
	site = '[B][COLOR green]CINEM[/COLOR][COLOR yellow]A[/COLOR][COLOR red]EMCASA[/COLOR][/B]'
	percent = int( ( a / 8.0 ) * 100)
        message = ''
        progress.update(percent, 'A Procurar em '+site, message, "")
        print str(a) + " de " + str(int(a))

        try: TFV.join()
        except: pass

        try: TFC.join()
        except: pass

        try: MVT.join()
        except: pass

        try: TPT.join()
        except: pass

        try: FTT.join()
        except: pass
        
        try: CMT.join()
        except: pass

        try: CME.join()
        except: pass

        try: CMC.join()
        except: pass

##        #xbmc.sleep(1000)
##        for a in range(100):
##                percent = int( ( a / 100.0 ) * 100)
##                progress.update( percent, 'A Procurar Filmes...', message, "" )
##                xbmc.sleep(5)

        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)



#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def FILMES_ANIMACAO_encontrar_fontes_pesquisa_TFV(url,pesquisou):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbc = imdb[0]
        else: imdbc = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]

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
                                imdbcode = ''
                                fanart = ''
                                thumb = ''

                                imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                                if imdb: imdbcode = imdb[0]
                                else: imdbcode = ''
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
                                if thumbnail: thumb = thumbnail[0]
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
                                        if 'Temporada' not in nome and 'Season' not in nome and 'Mini-Série' not in nome:
                                                if imdbc != '' and imdbcode != '':
                                                        if imdbcode == imdbc:
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
                                                                
                                                                name = '[COLOR orange]TFV | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR]'
                                                                iconimage = thumb.replace('s72-c','s320')
                                                                addDir1(name,'url',1001,iconimage,False,fanart)
                                                                TugaFilmesTV.TFV_links('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0].replace(' ','') + ')[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',iconimage,fanart)
                                                                num_f = num_f + 1
                                                else:
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
                                                        
                                                        name = '[COLOR orange]TFV | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR]'
                                                        iconimage = thumb.replace('s72-c','s320')
                                                        addDir1(name,'url',1001,iconimage,False,fanart)
                                                        TugaFilmesTV.TFV_links('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0].replace(' ','') + ')[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',iconimage,fanart)
                                                        num_f = num_f + 1
                                except: pass
                        except: pass
        else: return
        return


#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def FILMES_ANIMACAO_encontrar_fontes_filmes_TFC(url,pesquisou):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbc = imdb[0]
        else: imdbc = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]
        
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
                                imdbcode = ''
                                fanart = ''
                                thumb = ''
                                genero = ''
                                qualidade = ''

                                imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                                if imdb: imdbcode = imdb[0]
                                else: imdbcode = ''

                                
                                pt_en_f = re.compile('<iframe (.+?)</iframe>').findall(item)
                                if '---------------------------------------' in item and len(pt_en_f) > 1: versao = '[COLOR blue] 2 VERSÕES[/COLOR]'
                                urletitulo = re.compile("<a href=\'(.+?)\' title=\'(.+?)\'>").findall(item)
                                qualidade_ano = re.compile('<b>VERS\xc3\x83O:.+?</b><span style="font-size: x-small;">(.+?)<').findall(item)
                                thumbnail = re.compile('<img alt="" border="0" src="(.+?)"').findall(item)
                                if thumbnail: thumb = thumbnail[0]
                                print urletitulo,thumbnail
                                nome = urletitulo[0][1]
                                nome = nome.replace('&#8216;',"'")
                                nome = nome.replace('&#8217;',"'")
                                nome = nome.replace('&#8211;',"-")
                                nome = nome.replace('&#39;',"'")
                                nome = nome.replace('&amp;','&')
                                nome_pesquisa = urletitulo[0][1]
                                nome_pesquisa = nome_pesquisa.replace('&#8217;',"'")
                                nome_pesquisa = nome_pesquisa.replace('&#8211;',"-")
                                nome_pesquisa = nome_pesquisa.replace('&#038;',"&")
                                nome_pesquisa = nome_pesquisa.replace('&#39;',"'")
                                nome_pesquisa = nome_pesquisa.replace('&amp;','&')
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
                                                ano = ''
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
                                
                                if imdbcode == '':
                                        conta = 0
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
                                        html_imdbcode = abrir_url(url_imdb)
                                        filmes_imdb = re.findall('<div class="findSection">(.*?)<div class="findMoreMatches">', html_imdbcode, re.DOTALL)
                                        imdbcd = re.compile('/title/(.+?)/[?]ref').findall(filmes_imdb[0])
                                        imdbcode = imdbcd[0]
                                
                                try:
                                        if imdbc != '' and imdbcode != '' and 'BREVEMENTE' not in item:
                                                if imdbcode == imdbc:
                                                        nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                                                        if not nnnn: nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                                                        if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                                                        if not nnnn: nnnn = re.compile('(.+?)[:] ').findall(nome)
                                                        if nnnn : nome_pesquisa = nnnn[0]
                                                        if nnnn: nome_pesquisa = nnnn[0]
                                                        else: nome_pesquisa = nome
                                                        try:
                                                                fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano)
                                                                if thumb == '': thumb = poster
                                                        except: pass
                                                        name = '[COLOR orange]TFC | [/COLOR][B][COLOR green]' + urletitulo[0][1].replace('&#39;',"'") + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR][COLOR red] (' + qualidade + ')[/COLOR]' + versao
                                                        iconimage = thumb.replace('s1600','s320').replace('.gif','.jpg')
                                                        addDir1(name,'url',1001,iconimage,False,fanart)
                                                        TugaFilmesCom.TFC_links('[B][COLOR green]' + urletitulo[0][1].replace('&#39;',"'") + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',iconimage,fanart)
                                                        num_f = num_f + 1
                                        else:
                                                if 'BREVEMENTE' not in item:
                                                        nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                                                        if not nnnn: nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                                                        if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                                                        if not nnnn: nnnn = re.compile('(.+?)[:] ').findall(nome)
                                                        if nnnn : nome_pesquisa = nnnn[0]
                                                        if nnnn: nome_pesquisa = nnnn[0]
                                                        else: nome_pesquisa = nome
                                                        try:
                                                                fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano)
                                                                if thumb == '': thumb = poster
                                                        except:pass
                                                        name = '[COLOR orange]TFC | [/COLOR][B][COLOR green]' + urletitulo[0][1].replace('&#39;',"'") + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR][COLOR red] (' + qualidade + ')[/COLOR]' + versao
                                                        iconimage = thumb.replace('s1600','s320').replace('.gif','.jpg')
                                                        addDir1(name,'url',1001,iconimage,False,fanart)
                                                        TugaFilmesCom.TFC_links('[B][COLOR green]' + urletitulo[0][1].replace('&#39;',"'") + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',iconimage,fanart)
                                                        num_f = num_f + 1
                                except: pass
                        except: pass
        else: return
        return


#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def FILMES_ANIMACAO_encontrar_fontes_pesquisa_MVT(url):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbc = imdb[0]
        else: imdbc = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]
        
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
	if items != []:
                num_f = 0
		print len(items)
		for item in items:
                        try:
                                imdbcode = ''
                                fanart = ''
                                thumb 

                                imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                                if imdb: imdbcode = imdb[0]
                                else: imdbcode = ''
                                
                                url = re.compile('<div class="btns"><a href="(.+?)" target="Player">').findall(item)
                                if 'http' not in url[0]:
                                        urllink = 'http:' + url[0]
                                else: urllink = url[0]
                                titulo = re.compile("<div id='titulosingle'><h3>(.+?)</h3></div>").findall(item)
                                if not titulo: titulo = re.compile("<strong>T\xc3\xadtulo original:</strong>(.+?)</div>").findall(item)
                                if 'Qualidade:' in item:
                                        qualidade = re.compile("<strong>Qualidade:</strong>(.+?)</div>").findall(item)
                                        qualidade_filme = qualidade[0].replace('&#8211;',"-")
                                else:
                                        qualidade_filme = ''
                                ano = re.compile('<strong>Lan\xc3\xa7amento:</strong>(.+?)</div>').findall(item)
                                if ano: ano_filme = ano[0].replace(' ','').replace('20013','2013')
                                else: ano_filme = ''
                                thumbnail = re.compile('src="(.+?)"').findall(item)
                                if 'http' not in thumbnail[0]:
                                        thumb = 'http:' + thumbnail[0]
                                else: thumb = thumbnail[0]

                                titulo[0] = titulo[0].replace('&#8217;',"'")
                                titulo[0] = titulo[0].replace('&#8211;',"-")
                                titulo[0] = titulo[0].replace('&#038;',"&")
                                titulo[0] = titulo[0].replace('&#39;',"'")
                                titulo[0] = titulo[0].replace('&amp;','&')

                                conta = 0
                                if imdbcode == '':
                                        nome_pesquisa = titulo[0]
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
                                        html_imdbcode = abrir_url(url_imdb)
                                        filmes_imdb = re.findall('<div class="findSection">(.*?)<div class="findMoreMatches">', html_imdbcode, re.DOTALL)
                                        imdbcd = re.compile('/title/(.+?)/[?]ref').findall(filmes_imdb[0])
                                        imdbcode = imdbcd[0]

                                
                                try:
                                        if imdbc != '' and imdbcode != '':
                                                if imdbcode == imdbc:
                                                        nome = titulo[0]
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
                                                        name = '[COLOR orange]MVT | [/COLOR][B][COLOR green]' + titulo[0] + ' [/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]'
                                                        iconimage = thumb.replace('s72-c','s320').replace(' ','%20')
                                                        addDir1(name,'url',1001,iconimage,False,fanart)
                                                        MovieTuga.MVT_links('[B][COLOR green]' + titulo[0] + ' [/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR]',urllink.replace(' ','%20')+'IMDB'+imdbcode+'IMDB',iconimage,fanart)
                                                        num_f = num_f + 1
                                        else:
                                                nome = titulo[0]
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
                                                name = '[COLOR orange]MVT | [/COLOR][B][COLOR green]' + titulo[0] + ' [/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]'
                                                iconimage = thumb.replace('s72-c','s320').replace(' ','%20')
                                                addDir1(name,'url',1001,iconimage,False,fanart)
                                                MovieTuga.MVT_links('[B][COLOR green]' + titulo[0] + ' [/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR]',urllink.replace(' ','%20')+'IMDB'+imdbcode+'IMDB',iconimage,fanart)
                                                num_f = num_f + 1
                                except: pass
                        except: pass
        else: return
        return


#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def FILMES_ANIMACAO_encontrar_fontes_pesquisa_FTT(url):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbc = imdb[0]
        else: imdbc = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]

	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall("<h3 class='post-title entry-title'(.+?)<div class='post-footer'>", html_source, re.DOTALL)
	#addLink(str(len(items)),'','')
	if items != []:
		print len(items)
		num_f = 0
		for item in items:
                        try:
                                thumb = ''
                                fanart = ''
                                anofilme= ''
                                qualidade_filme = ''
                                imdbcode = ''
                                audio_filme = ''
                                genero = ''
                                sinopse = ''

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
                                        
                                

                                snpse = re.compile('Sinopse.png"></a></div>\n(.+?)\n').findall(item)
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
                                                nome = nome.replace(tirar_ano,'--')
                                                tirar_ano = '-' + str(q_a_q_a)
                                                nome = nome.replace(tirar_ano,'--')
                                                tirar_ano = str(q_a_q_a)
                                                nome = nome.replace(tirar_ano,'--')

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

                                nome = nome.replace('-- ',"")
                                nome = nome.replace(' --',"")
                                nome = nome.replace('--',"")

                                if audio_filme!= '': audio_filme = ': '+audio_filme

                                nome = nome.replace('((','(')
                                nome = nome.replace('))',')')
                                nome = nome.replace('()','(')
                                nome = nome.replace('  ','')
                                nome = nome.replace(' - []','')
                                nome = nome.replace('[]','')

                                try:
                                        fonte_video = abrir_url(urlvideo)
                                except: fonte_video = ''
                                fontes_video = re.findall("<div class='post-body entry-content'>(.*?)<div style='clear: both;'>", fonte_video, re.DOTALL)
                                if fontes_video != []:
                                        qualid = re.compile('ASSISTIR ONLINE (.*)\n').findall(fontes_video[0])
                                        if qualid: qualidade_filme = qualid[0].replace('/ ',' ').replace('</b>','').replace('</span>','').replace('LEGENDADO','')+audio_filme
                                        else:
                                                qualid = re.compile('[[]</span><span style=".+?"><span style=".+?">(.+?)</span><span style=".+?">[]]').findall(fontes_video[0])
                                                if qualid: qualidade_filme = qualid[0].replace('/ ','').replace('</b>','').replace('</span>','')+audio_filme

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
                                        html_imdbcode = abrir_url(url_imdb)
                                        filmes_imdb = re.findall('<div class="findSection">(.*?)<div class="findMoreMatches">', html_imdbcode, re.DOTALL)
                                        imdbcd = re.compile('/title/(.+?)/[?]ref').findall(filmes_imdb[0])
                                        imdbcode = imdbcd[0]

                                
                                try:
                                        if imdbc != '' and imdbcode != '':
                                                if imdbcode == imdbc:
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
                                                        
                                                        name = '[COLOR orange]FTT | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme.replace('</div>','') + ')[/COLOR]'
                                                        iconimage = thumb
                                                        addDir1(name,'url',1001,iconimage,False,fanart)
                                                        FoitaTuga.FTT_links('[B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR]',urlvideo+'IMDB'+imdbcode+'IMDB',iconimage,fanart)
                                                        num_f = num_f + 1
                                        else:
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
                                                
                                                name = '[COLOR orange]FTT | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme.replace('</div>','') + ')[/COLOR]'
                                                iconimage = thumb
                                                addDir1(name,'url',1001,iconimage,False,fanart)
                                                FoitaTuga.FTT_links('[B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR]',urlvideo+'IMDB'+imdbcode+'IMDB',iconimage,fanart)
                                                num_f = num_f + 1
                                except: pass
                        except: pass
        else: return
        return

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def FILMES_ANIMACAO_encontrar_fontes_pesquisa_CMT(url,pesquisou):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbc = imdb[0]
        else: imdbc = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]

	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall("<h3 class='post-title entry-title'(.*?)<span class='post-location'>", html_source, re.DOTALL)
	conta_items = 0
	if items != []:
		print len(items)
		num_f = 0
		for item in items:
                        sinopse = ''
                        genre = ''
                        thumb = ''
                        fanart = ''
                        versao = ''
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
                        ano = re.compile("<b>Ano</b>: (.+?)<br />").findall(item)
                        if ano: ano_filme = ano[0]
                        else: ano_filme = ''
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
                                        if ano_filme == '': ano_filme = str(q_a_q_a)

                                                                                                                                                

                        if qualidade:
                                qualidade = qualidade[0].replace('<b>','').replace('</b>','')
                        else:
                                qualidade = ''
                                
                        if genre == '': genre = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'

                        try:
                                if "Temporada" in urletitulo[0][1]:
                                        num_mode = 712
                                else:
                                        num_mode = 703
                                if "Temporada" not in nome and "Season" not in nome:
                                        if imdbc != '' and imdbcode != '':
                                                if imdbcode == imdbc:
                                ##                        nnnn = re.compile('(.+?): ').findall(nome)
                                ##                        if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                                ##                        if nnnn : nome_pesquisa = nnnn[0]
                                                        nome_pesquisa = nome
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
                                                        name = '[COLOR orange]CMT | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano_filme.replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao
                                                        iconimage = thumb.replace('s72-c','s320')
                                                        addDir1(name,'url',1001,iconimage,False,fanart)
                                                        Cinematuga.CMT_links('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano_filme.replace(' ','') + ')[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',iconimage,fanart)
                                                        num_f = num_f + 1
                                        else:
                        ##                        nnnn = re.compile('(.+?): ').findall(nome)
                        ##                        if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                        ##                        if nnnn : nome_pesquisa = nnnn[0]
                                                nome_pesquisa = nome
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
                                                name = '[COLOR orange]CMT | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao
                                                iconimage = thumb.replace('s72-c','s320')
                                                addDir1(name,'url',1001,iconimage,False,fanart)
                                                Cinematuga.CMT_links('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano_filme.replace(' ','') + ')[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',iconimage,fanart)
                                                num_f = num_f + 1
                        except: pass
        else: return
        return


#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def FILMES_ANIMACAO_encontrar_fontes_filmes_TPT(url,pesquisou):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbc = imdb[0]
        else: imdbc = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	if '<div class="postmeta-primary">' in html_source: items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	else: return
        if not items: items = re.findall('<div class="postmeta-primary">(.*?)<div id="sidebar-primary">', html_source, re.DOTALL)
	if items != []:
                num_f = 0
		print len(items)
		for item in items:
                        try:
                                audio_filme = ''
                                imdbcode = ''
                                genero = ''
                                sinopse = ''
                                fanart = ''
                                thumb = ''
                                qualidade = ''
                                imdbcode = ''
                                imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                                if imdb: imdbcode = imdb[0]
                                else: imdbcode = ''

                                urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(item)
                                if 'title=' in urletitulo[0][0]: urletitulo = re.compile('<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>').findall(item)
                                url = urletitulo[0][0]
                                try:
                                        html_source = abrir_url(url)
                                except: html_source = ''
                                items = re.findall('<div class="post-(.*?)<span id="more-', html_source, re.DOTALL)
                                if items != []:
                                        print len(items)
                                        for item in items:
                                                fanart = ''
                                                thumb = ''
                                                audio_filme = ''
                                                titulo = re.compile('<h2 class="title">(.+?)</h2>').findall(item)
                                                #urlpesq = re.compile('<a href="(.+?)" rel="bookmark">').findall(item)
                                                qualidade = re.compile("<b>QUALIDADE:.+?/b>(.+?)<br/>").findall(item)
                                                if not qualidade: qualidade = re.compile("<b>VERSÃO:.+?</b>(.+?)<br/>").findall(item)
                                                ano = re.compile("<b>ANO:.+?/b>(.+?)<br/>").findall(item)
                                                audio = re.compile("<b>AUDIO:.+?/b>(.+?)<br/>").findall(item)    
                                                thumbnail = re.compile('src="(.+?)"').findall(item)
                                                if thumbnail: thumb = thumbnail[0]
                                                print urletitulo,thumbnail
                                                nome = titulo[0]
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
                                                
                                                #addLink(fanart,'','')       
                                                if genero == '': genero = '---'
                                                if sinopse == '': sinopse = '---'
                                                if fanart == '': fanart = ''
                                                if imdbcode == '': imdbcode = '---'
                                                if thumb == '': thumb = '---'
                                                try:
                                                        nomecomp = nome.lower()
                                                        if imdbc != '' and imdbcode != '':
                                                                if imdbcode == imdbc:
                                                                        if 'online' in genero and not 'series' in genero and 'INDISPONIVEL' not in html_source:
                                                                        #if 'series' in genero:
                                                                                #if 'OP\xc3\x87\xc3\x83O' in item:
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
                                                                                
                                                                                name = '[COLOR orange]TPT | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR]'
                                                                                iconimage = thumb.replace('s72-c','s320')
                                                                                addDir1(name,'url',1001,iconimage,False,fanart)
                                                                                TopPt.TPT_links('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano_filme + ')[/COLOR]',url+'IMDB'+imdbcode+'IMDB',iconimage,fanart)#,genero,sinopse,ano_filme)
                                                                                num_f = num_f + 1
                                                        else:
                                                                if 'online' in genero and not 'series' in genero and 'INDISPONIVEL' not in html_source:
                                                                        #if nomecomp in pesquisou:
                                                                #if 'series' in genero:
                                                                        #if 'OP\xc3\x87\xc3\x83O' in item:
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
                                                                        name = '[COLOR orange]TPT | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR]'
                                                                        iconimage = thumb.replace('s72-c','s320')
                                                                        addDir1(name,'url',1001,iconimage,False,fanart)
                                                                        TopPt.TPT_links('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano_filme + ')[/COLOR]',url+'IMDB'+imdbcode+'IMDB',iconimage,fanart)#,genero,sinopse,ano_filme)
                                                                        num_f = num_f + 1
                                                except: pass
                        except: pass
        else: return
        return

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def FILMES_ANIMACAO_encontrar_fontes_filmes_CME(url,pesquisou):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbc = imdb[0]
        else: imdbc = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]

        try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall("<h3 class='post-title entry-title'(.+?)<div class='post-footer'>", html_source, re.DOTALL)
	if items != []:
		for item in items:
                        
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

                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'

                        try:
                                if imdbc != '' and imdbcode != '':
                                        if imdbcode == imdbc:
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
                                                                if fanart == '': fanart,tmb,pter = themoviedb_api().fanart_and_id(nome_pesquisa,anofilme)
                                                                if thumb == ''  or 'IMDb.png' in thumb or 'Sinopse' in thumb: thumb = poster
                                                        except:pass
                                                else:
                                                        try:
                                                                fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,anofilme)
                                                                if thumb == ''  or 'IMDb.png' in thumb or 'Sinopse' in thumb: thumb = poster
                                                        except: pass
                                                
                                                name = '[COLOR orange]CME | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme.replace('</div>','') + ')[/COLOR]'
                                                iconimage = thumb
                                                addDir1(name,'url',1001,iconimage,False,fanart)
                                                CinematugaEu.CME_links('[B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR]',urlvideo+'IMDB'+imdbcode+'IMDB',iconimage,fanart)                                              

                                else:
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
                                        
                                        name = '[COLOR orange]CME | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme.replace('</div>','') + ')[/COLOR]'
                                        iconimage = thumb
                                        addDir1(name,'url',1001,iconimage,False,fanart)
                                        CinematugaEu.CME_links('[B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR]',urlvideo+'IMDB'+imdbcode+'IMDB',iconimage,fanart)                                              
                        except: pass
	else: return
        return


def FILMES_ANIMACAO_encontrar_fontes_filmes_CMC(url,pesquisou):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbc = imdb[0]
        else: imdbc = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]

        try:
		html_source = abrir_url(url)
	except: html_source = ''
        items = re.findall("<h2 class='post-title entry-title'>(.+?)<div class='post-footer'>", html_source, re.DOTALL)
        #addLink(str(len(items)),'','','')
	if items != []:
		for item in items:
                        
                        thumb = ''
                        fanart = ''
                        sinopse = ''
                        genero = ''
                        imdbcode = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
                        urltitulo = re.compile("<a href='(.+?)'>\n(.+?)\n</a>").findall(item)
                        if urltitulo:
                                urlfilme = urltitulo[0][0]
                                nome = urltitulo[0][1]
                        else:
                                urlfilme = ''
                                nome = ''

                        snpse = re.compile("<div id='imgsinopse'>(.+?)</div>").findall(item)
                        if snpse: sinopse = snpse[0]
                        sinopse = sinopse.replace('&#8216;',"'")
                        sinopse = sinopse.replace('&#8217;',"'")
                        sinopse = sinopse.replace('&#8211;',"-")
                        sinopse = sinopse.replace('&#8220;',"'")
                        sinopse = sinopse.replace('&#8221;',"'")
                        sinopse = sinopse.replace('&#39;',"'")
                        sinopse = sinopse.replace('&amp;','&')
                        
                        gen = re.compile('nero: </span><span style="color: white;">(.+?)</span></b></span>').findall(item)
                        if gen: genero = gen[0]
                        
                        qualidade = re.compile("<strong>Qualidade:</strong>(.+?)</div>").findall(item)
                        if qualidade: qualidade_filme = qualidade[0].replace('&#8211;',"-")
                        else: qualidade_filme = ''

                        audio = re.compile('Audio: </span><span style="color: white;">(.+?)</span></b></span>').findall(item)
                        if audio and qualidade_filme == '': qualidade_filme = audio[0]
                                
                        ano = re.compile('>Ano: </span><span style="color: white;">(.+?)</span></b></span>').findall(item)
                        if ano: ano_filme = ano[0]
                        else: ano_filme = ''
                        
                        thumbnail = re.compile('<a href="(.+?)" imageanchor="1"').findall(item)
                        if thumbnail: thumb = thumbnail[0].replace('s72-c','s320')
                        else: thumb = ''

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
                        
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        #addLink(imdbcode+imdbc,'','','')
                        try:
                                if imdbc != '' and imdbcode != '':
                                        if imdbcode == imdbc:
                                                if 'Temporada' not in nome:
                                                        nnnn = re.compile('.+?[(](.+?)[)]').findall(nome)
                                                        if not nnnn: nnnn = re.compile('.+?[[](.+?)[]]').findall(nome)
                                                        if not nnnn: nnnn = re.compile('(.+?)[:]').findall(nome)
                                                        if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                                                        if nnnn : nome_pesquisa = nnnn[0]
                                                        else: nome_pesquisa = nome
                                                        #nome_pesquisa = nome
                                                        #addLink(imdbcode,'','')
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
                                                                except:pass
                                                        name = '[COLOR orange]CMC | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]'
                                                        iconimage = thumb
                                                        addDir1(name,'url',1001,iconimage,False,fanart)
                                                        CinemaEmCasa.CMC_links('[COLOR orange]CMC | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',urlfilme.replace(' ','%20')+'IMDB'+imdbcode+'IMDB',iconimage,fanart)                                              
                                else:
                                        if 'Temporada' not in nome:
                                                nnnn = re.compile('.+?[(](.+?)[)]').findall(nome)
                                                if not nnnn: nnnn = re.compile('.+?[[](.+?)[]]').findall(nome)
                                                if not nnnn: nnnn = re.compile('(.+?)[:]').findall(nome)
                                                if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                                                if nnnn : nome_pesquisa = nnnn[0]
                                                else: nome_pesquisa = nome
                                                #nome_pesquisa = nome
                                                #addLink(imdbcode,'','')
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
                                                        except:pass
                                                name = '[COLOR orange]CMC | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]'
                                                iconimage = thumb
                                                addDir1(name,'url',1001,iconimage,False,fanart)
                                                CinemaEmCasa.CMC_links('[COLOR orange]CMC | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',urlfilme.replace(' ','%20')+'IMDB'+imdbcode+'IMDB',iconimage,fanart)                                              

                                        #addDir_trailer('[COLOR orange]CMC | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',urlfilme.replace(' ','%20')+'IMDB'+imdbcode+'IMDB',903,thumb.replace(' ','%20'),sinopse,fanart,ano_filme,genero,nome,urlfilme)
                        except: pass
        else: return
        return

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
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
