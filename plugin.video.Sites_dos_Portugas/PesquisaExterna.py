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
import Play

#from string import capwords
import string
from Funcoes import thetvdb_api, themoviedb_api, themoviedb_api_tv, theomapi_api, themoviedb_api_IMDB, themoviedb_api_IMDB_episodios, themoviedb_api_TMDB
from Funcoes import thetvdb_api_tvdbid, thetvdb_api_episodes, themoviedb_api_search_imdbcode, themoviedb_api_pagina, themoviedb_api_IMDB1, theomapi_api_nome
from Funcoes import addDir, addDir1, addDir2, addLink, addLink1, addDir_teste, addDir_trailer, addDir_episode, addDir_trailer1_filmes, addDir_trailer_filmes
from Funcoes import addDir_trailer1, addDir_episode1
from Funcoes import get_params,abrir_url

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

progress = xbmcgui.DialogProgress()
resultados = []

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def pesquisar(nome_pesquisa,url,automatico):
        #resultados.append(nome_pesquisa+url+year'|URL|'+'--'+'|THUMB|'+'--'+'|FANART|'+'--')
        
        nome_original = nome_pesquisa
        
##        qualsite = re.compile('IMDB.+?IMDB(.*)').findall(url)
##        if qualsite: nomesite = qualsite[0]
##        else: nomesite = ''
##
##        qualurl = re.compile('(.+?)IMDB.+?IMDB').findall(url)
##        if qualurl: qualurl = qualurl[0]
##        else: qualurl = ''
        
        nomesite = ''
        
        nome_pp = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]][[]COLOR yellow[]].+?[[]/COLOR[]]').findall(nome_pesquisa)
        if nome_pp: nome_pesquisa = nome_pp[0]
        else: nome_pesquisa = nome_pesquisa
        
        imdb = re.compile('IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''

        pesquisa_imdb = nome_pesquisa
        pp = nome_pesquisa
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

        threads = []

	url_pesquisa = 'http://toppt.net/?s=' + str(encode)	
	if nomesite != 'TPT':
                try:
                        html_source = abrir_url(url_pesquisa)
                except: html_source = ''
                i=0
                items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
                if not items: items = re.findall('<div class="postmeta-primary">(.*?)<div id="sidebar-primary">', html_source, re.DOTALL)
                for item in items:                        
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        TPT = threading.Thread(name='TPT'+str(i), target=FILMES_ANIMACAO_encontrar_fontes_filmes_TPT , args=(str(a),url_pesquisa,pesquisou,imdbcode,item,))
                        threads.append(TPT)
                        TPT.start()
                        TPT.join()

	url_pesquisa = 'http://www.tuga-filmes.info/search?q=' + str(encode)	
	if nomesite != 'TFC':
                try:
                        html_source = abrir_url(url_pesquisa)
                except: html_source = ''
                i=0
                items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
                for item in items:                        
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        TFC = threading.Thread(name='TFC'+str(i), target=FILMES_ANIMACAO_encontrar_fontes_filmes_TFC , args=(str(a),url_pesquisa,pesquisou,imdbcode,item,))
                        threads.append(TFC)
                        TFC.start()
                        TFC.join()

	url_pesquisa = 'http://www.tuga-filmes.us/search?q=' + str(encode)
	if nomesite != 'TFV':
                try:
                        html_source = abrir_url(url_pesquisa)
                except: html_source = ''
                i=0
                items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
                for item in items:                        
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        TFV = threading.Thread(name='TFV'+str(i), target=FILMES_ANIMACAO_encontrar_fontes_pesquisa_TFV , args=(str(a),url_pesquisa,pesquisou,imdbcode,item,))
                        threads.append(TFV)
                        TFV.start()
                        TFV.join()

	url_pesquisa = 'http://www.cinematuga.eu/search?q=' + str(encode)
	if nomesite != 'CME':
                try:
                        html_source = abrir_url(url_pesquisa)
                except: html_source = ''
                i=0
                items = re.findall("<h3 class='post-title entry-title'(.+?)<div class='post-footer'>", html_source, re.DOTALL)
                for item in items:                        
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        CME = threading.Thread(name='CME'+str(i), target=FILMES_ANIMACAO_encontrar_fontes_filmes_CME , args=(str(a),url_pesquisa,pesquisou,imdbcode,item,))
                        threads.append(CME)
                        CME.start()
                        CME.join()

	url_pesquisa = 'http://foitatugacinemaonline.blogspot.pt/search?q=' + str(encode) + '&submit=Buscar'	
	if nomesite != 'FTT':
                try:
                        html_source = abrir_url(url_pesquisa)
                except: html_source = ''
                i=0
                items = re.findall("<h3 class='post-title entry-title'(.+?)<div class='post-footer'>", html_source, re.DOTALL)
                for item in items:                        
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        FTT = threading.Thread(name='FTT'+str(i), target=FILMES_ANIMACAO_encontrar_fontes_pesquisa_FTT, args=(str(a),url_pesquisa,pesquisou,imdbcode,item,))
                        threads.append(FTT)
                        FTT.start()
                        FTT.join()

	url_pesquisa = 'http://www.cinematuga.net/search?q=' + str(encode)	
	if nomesite != 'CMT':
                try:
                        html_source = abrir_url(url_pesquisa)
                except: html_source = ''
                i=0
                items = re.findall("<h3 class='post-title entry-title'(.*?)<span class='post-location'>", html_source, re.DOTALL)
                for item in items:                        
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        CMT = threading.Thread(name='CMT'+str(i), target=FILMES_ANIMACAO_encontrar_fontes_pesquisa_CMT, args=(str(a),url_pesquisa,pesquisou,imdbcode,item,))
                        threads.append(CMT)
                        CMT.start()
                        CMT.join()

	url_pesquisa = 'http://www.movie-tuga.blogspot.pt/search?q=' + str(encode)	
	if nomesite != 'MVT':
                try:
                        html_source = abrir_url(url_pesquisa)
                except: html_source = ''
                i=0
                items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)                
                if not items: items = re.findall("<div class=\'entry\'>(.+?)<div class='clear'>", html_source, re.DOTALL)
                aaaa = len(items)
                for item in items:                        
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        MVT = threading.Thread(name='MVT'+str(i), target=FILMES_ANIMACAO_encontrar_fontes_pesquisa_MVT, args=(str(a),url_pesquisa,pesquisou,imdbcode,item,))
                        threads.append(MVT)
                        MVT.start()
                        MVT.join()

	url_pesquisa = 'http://www.cinemaemcasa.pt/search?q=' + str(encode)
	if nomesite != 'CMC':
                try:
                        html_source = abrir_url(url_pesquisa)
                except: html_source = ''
                i=0
                items = re.findall("<h2 class='post-title entry-title'>(.+?)<div class='post-footer'>", html_source, re.DOTALL)
                for item in items:                        
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        CMC = threading.Thread(name='CMC'+str(i), target=FILMES_ANIMACAO_encontrar_fontes_filmes_CMC, args=(str(a),url_pesquisa,pesquisou,imdbcode,item,))
                        threads.append(CMC)
                        CMC.start()
                        CMC.join()

##        [i.start() for i in threads]
##        [i.join() for i in threads]

        _nomeservidor_ = []
        _linkservidor_ = []
        _thumbimage_ = []
        _legendas_ = []

        audioTPT = ''
        audioTFC = ''
        audioTFV = ''
        audioFTT = ''
        audioCMC = ''
        automatico = automatico.upper()
        encontrou = 'nao'
        i = 0
        if resultados != []:
                        
                for x in range(len(resultados)):
                        audio_audio = re.compile('(.+?)[|]AUDIO[|](.*)').findall(resultados[x])
                        if audio_audio and 'TOPPT' in audio_audio[0][0]:
                                #_nomeservidor_.append(resultados[x])
                                audioTPT = ' | '+audio_audio[0][1].replace(' ','').replace('PORTUGUESPT','PT-PT')
                        if audio_audio and 'TUGAFILMES.COM' in audio_audio[0][0]:
                                #_nomeservidor_.append(resultados[x])
                                audioTFC = ' | '+audio_audio[0][1].replace(' ','').replace('PORTUGUESPT','PT-PT')
                        if audio_audio and 'TUGAFILMES.TV' in audio_audio[0][0]:
                                #_nomeservidor_.append(resultados[x])
                                audioTFV = ' | '+audio_audio[0][1].replace(' ','').replace('PORTUGUESPT','PT-PT')
                        if audio_audio and 'FOITATUGA' in audio_audio[0][0]:
                                #_nomeservidor_.append(resultados[x])
                                audioFTT = ' | '+audio_audio[0][1].replace(':','').replace('/','-').replace(' ','').replace('PORTUGUESPT','PT-PT')
                        if audio_audio and 'CINEMAEMCASA' in audio_audio[0][0]:
                                #_nomeservidor_.append(resultados[x])
                                audioCMC = ' | '+audio_audio[0][1].replace(':','').replace('/','-').replace(' ','').replace('&nbsp;','').replace('ê','Ê').replace('PORTUGUESPT','PT-PT')
                        
                        res = re.compile('(.+?)[|]URL[|](.+?)[|]THUMB[|](.+?)[|]FANART').findall(resultados[x])
                        if res and 'AUDIO' not in resultados[x]:
                                i = i + 1
                                a = str(i)
                                if i < 10: a = '0'+a
                                
                                if 'TOPPT' in res[0][0]: audio = audioTPT
                                elif 'TUGAFILMES.COM' in res[0][0]: audio = audioTFC
                                elif 'TUGAFILMES.TV' in res[0][0]: audio = audioTFV
                                elif 'FOITATUGA' in res[0][0]: audio = audioFTT
                                elif 'CINEMAEMCASA' in res[0][0]: audio = audioCMC
                                else: audio = ''
                                
                                _nomeservidor_.append(res[0][0].replace('SITESdosPORTUGAS',str(a))+audio)                                                  
                                _linkservidor_.append(res[0][1])
                                _thumbimage_.append(res[0][2])
                                subs = re.compile('[|]SUBTITLES[|](.*)').findall(resultados[x])
                                if subs: _legendas_.append(subs[0])
                                else: _legendas_.append('---')
                if automatico != '' and automatico != None:
                        for x in range(len(_nomeservidor_)):
                                if automatico in _nomeservidor_[x]:
                                        nomefilme = name
                                        progress.create(nomefilme, 'A preparar vídeo.')
                                        progress.update( 98, '', 'Por favor aguarde...', "" )

                                        if _legendas_[x] == '---': checker = ''
                                        else: checker = _legendas_[x]

                                        playlist = xbmc.PlayList(1)
                                        playlist.clear()

                                        liz=xbmcgui.ListItem(nome_original, thumbnailImage=_thumbimage_[x])
                                        xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,liz)
                                        playlist.add(_linkservidor_[x],liz)

                                        encontrou = 'sim'
                                        
                        if encontrou == 'sim':
                                if 'VIDTO.ME' in nomedostream or 'NOWVIDEO' in nomedostream or 'MOVSHARE' in nomedostream or 'FIREDRIVE' in nomedostream or 'PUTLOCKER' in nomedostream or 'SOCKSHARE' in nomedostream:
                                        PLAY_movie(_linkservidor_[x],nome_original,iconimage,'',fanart)
                                else:
                                        MyPlayer1(nomefilme=nomefilme,checker=checker).PlayStream(playlist)
                        else:
                                #try: xbmcgui.Dialog().notification('Não foram encontrados streams '+automatico, 'Por favor escolha outro.', artfolder + 'SDPI.png', 1500, sound=False)
                                #except: xbmc.executebuiltin("Notification(%s,%s, 1500, %s)" % ('Não foram encontrados streams '+automatico, 'Por favor escolha outro.', artfolder + 'SDPI.png'))
                                xbmcgui.Dialog().ok('[B][COLOR green]SITES[/COLOR][COLOR yellow]dos[/COLOR][COLOR red]PORTUGAS[/COLOR][/B]', 'Não foram encontrados streams '+automatico, 'Por favor escolha outro stream.')
                                
                                indexservidores = xbmcgui.Dialog().select
                                index = indexservidores('[B][COLOR green]SITES[/COLOR][COLOR yellow]dos[/COLOR][COLOR red]PORTUGAS[/COLOR][/B]', _nomeservidor_)
                                if index > -1:
                                        nomedostream = _nomeservidor_[index]
                                        nome_addon = ''
                                        checker = ''
                                        if 'VIDTO.ME' in nomedostream or 'NOWVIDEO' in nomedostream or 'MOVSHARE' in nomedostream or 'FIREDRIVE' in nomedostream or 'PUTLOCKER' in nomedostream or 'SOCKSHARE' in nomedostream:
                                                PLAY_movie(_linkservidor_[index],nome_original,iconimage,'',fanart)
                                        else:
                                                nomefilme = name
                                                progress.create(nomefilme, 'A preparar vídeo.')
                                                progress.update( 98, '', 'Por favor aguarde...', "" )

                                                if _legendas_[index] == '---': checker = ''
                                                else: checker = _legendas_[index]

                                                playlist = xbmc.PlayList(1)
                                                playlist.clear()

                                                liz=xbmcgui.ListItem(nome_original, thumbnailImage=_thumbimage_[index])
                                                xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,liz)
                                                playlist.add(_linkservidor_[index],liz)

                                                MyPlayer1(nomefilme=nomefilme,checker=checker).PlayStream(playlist)
                                
                else:                       
                        indexservidores = xbmcgui.Dialog().select
                        index = indexservidores('[B][COLOR green]SITES[/COLOR][COLOR yellow]dos[/COLOR][COLOR red]PORTUGAS[/COLOR][/B]', _nomeservidor_)
                        if index > -1:
                                nomedostream = _nomeservidor_[index]
                                nome_addon = ''
                                checker = ''
                                if 'VIDTO.ME' in nomedostream or 'NOWVIDEO' in nomedostream or 'MOVSHARE' in nomedostream or 'FIREDRIVE' in nomedostream or 'PUTLOCKER' in nomedostream or 'SOCKSHARE' in nomedostream:
                                        PLAY_movie(_linkservidor_[index],nome_original,iconimage,'',fanart)
                                else:
                                        nomefilme = name
                                        progress.create(nomefilme, 'A preparar vídeo.')
                                        progress.update( 98, '', 'Por favor aguarde...', "" )

                                        if _legendas_[index] == '---': checker = ''
                                        else: checker = _legendas_[index]

                                        playlist = xbmc.PlayList(1)
                                        playlist.clear()

                                        liz=xbmcgui.ListItem(nome_original, thumbnailImage=_thumbimage_[index])
                                        xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,liz)
                                        playlist.add(_linkservidor_[index],liz)

                                        MyPlayer1(nomefilme=nomefilme,checker=checker).PlayStream(playlist)
        else:
                try: xbmcgui.Dialog().notification('[B][COLOR green]SITES[/COLOR][COLOR yellow]dos[/COLOR][COLOR red]PORTUGAS[/COLOR][/B]', 'Não existem fontes disponíveis.', artfolder + 'SDPI.png', 1500, sound=False)
                except: xbmc.executebuiltin("Notification(%s,%s, 1500, %s)" % ('[B][COLOR green]SITES[/COLOR][COLOR yellow]dos[/COLOR][COLOR red]PORTUGAS[/COLOR][/B]', 'Não existem fontes disponíveis.', artfolder + 'SDPI.png'))

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def FILMES_ANIMACAO_encontrar_fontes_pesquisa_TFV(FILMEN,url,pesquisou,imdbc,item):

        num_f = 0
        if item != '':
                if item != '':
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
                                                                #addDir1(name,'url',1001,iconimage,False,fanart)
                                                                TFV_links('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0].replace(' ','') + ')[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',iconimage,fanart)
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
                                                        #addDir1(name,'url',1001,iconimage,False,fanart)
                                                        TFV_links('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0].replace(' ','') + ')[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',iconimage,fanart)
                                                        num_f = num_f + 1
                                except: pass
                        except: pass
        else: return
        return


#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def FILMES_ANIMACAO_encontrar_fontes_filmes_TFC(FILMEN,url,pesquisou,imdbc,item):
        pt_en = 0
        num_f = 0
        if item != '':
                if item != '':
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
                                                        #resultados.append('TUGAFILMES.COM|AUDIO|'+qualidade.upper()+versao)
                                                        #addDir1(name,'url',1001,iconimage,False,fanart)
                                                        TFC_links('[B][COLOR green]' + urletitulo[0][1].replace('&#39;',"'") + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',iconimage,fanart)
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
                                                        #resultados.append('TUGAFILMES.COM|AUDIO|'+qualidade.upper()+versao)
                                                        #addDir1(name,'url',1001,iconimage,False,fanart)
                                                        TFC_links('[B][COLOR green]' + urletitulo[0][1].replace('&#39;',"'") + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',iconimage,fanart)
                                                        num_f = num_f + 1
                                except: pass
                        except: pass
        else: return
        return


#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def FILMES_ANIMACAO_encontrar_fontes_pesquisa_MVT(FILMEN,url,pesquisou,imdbc,item):

        num_f = 0
        if item != '':
                if item != '':
                        try:
                                thumb = ''
                                fanart = ''
                                sinopse = ''
                                genero = ''
                                imdbcode = ''

                                imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                                if imdb: imdbcode = imdb[0]
                                else: imdbcode = ''
                                
                                url = re.compile('<div class="btns"><a href="(.+?)" target="Player">').findall(item)
                                if not url: re.compile("<a href='(.+?)'>").findall(item)
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

                                conta = 0
                                if imdbcode == '':
                                        nome_pesquisa = titulo[0] + '+' + ano_filme
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
                                        if imdbcd: imdbcode = imdbcd[0]
                                
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
                                                        #addDir1(name,'url',1001,iconimage,False,fanart)
                                                        MVT_links('[B][COLOR green]' + titulo[0] + ' [/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR]',urllink.replace(' ','%20')+'IMDB'+imdbcode+'IMDB',iconimage,fanart)
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
                                                #addDir1(name,'url',1001,iconimage,False,fanart)
                                                MVT_links('[B][COLOR green]' + titulo[0] + ' [/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR]',urllink.replace(' ','%20')+'IMDB'+imdbcode+'IMDB',iconimage,fanart)
                                                num_f = num_f + 1
                                except: pass
                        except: pass
        else: return
        return


#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def FILMES_ANIMACAO_encontrar_fontes_pesquisa_FTT(FILMEN,url,pesquisou,imdbc,item):

        num_f = 0
        if item != '':
                if item != '':
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
                                                        if audio_filme != '': resultados.append('FOITATUGA|AUDIO|'+audio_filme.upper())
                                                        #addDir1(name,'url',1001,iconimage,False,fanart)
                                                        FTT_links('[B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR]',urlvideo+'IMDB'+imdbcode+'IMDB',iconimage,fanart)
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
                                                if audio_filme != '': resultados.append('FOITATUGA|AUDIO|'+audio_filme.upper())
                                                #addDir1(name,'url',1001,iconimage,False,fanart)
                                                FTT_links('[B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR]',urlvideo+'IMDB'+imdbcode+'IMDB',iconimage,fanart)
                                                num_f = num_f + 1
                                except: pass
                        except: pass
        else: return
        return

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def FILMES_ANIMACAO_encontrar_fontes_pesquisa_CMT(FILMEN,url,pesquisou,imdbc,item):

        num_f = 0
        if item != '':
                if item != '':
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
                                                        #addDir1(name,'url',1001,iconimage,False,fanart)
                                                        CMT_links('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano_filme.replace(' ','') + ')[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',iconimage,fanart)
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
                                                #addDir1(name,'url',1001,iconimage,False,fanart)
                                                CMT_links('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano_filme.replace(' ','') + ')[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',iconimage,fanart)
                                                num_f = num_f + 1
                        except: pass
        else: return
        return


#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def FILMES_ANIMACAO_encontrar_fontes_filmes_TPT(FILMEN,url,pesquisou,imdbc,item):

        num_f = 0
        if item != '':
                if item != '':
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
                                                                                resultados.append('TOPPT|AUDIO|'+audio_filme.upper().replace(':',''))
                                                                                #addDir1(name,'url',1001,iconimage,False,fanart)
                                                                                TPT_links('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano_filme + ')[/COLOR]',url+'IMDB'+imdbcode+'IMDB',iconimage,fanart)#,genero,sinopse,ano_filme)
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
                                                                        resultados.append('TOPPT|AUDIO|'+audio_filme.upper().replace(':',''))
                                                                        #addDir1(name,'url',1001,iconimage,False,fanart)
                                                                        TPT_links('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano_filme + ')[/COLOR]',url+'IMDB'+imdbcode+'IMDB',iconimage,fanart)#,genero,sinopse,ano_filme)
                                                                        num_f = num_f + 1
                                                except: pass
                        except: pass
        else: return
        return

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def FILMES_ANIMACAO_encontrar_fontes_filmes_CME(FILMEN,url,pesquisou,imdbc,item):

        num_f = 0
        if item != '':
                if item != '':
                        
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
                                                #addDir1(name,'url',1001,iconimage,False,fanart)
                                                CME_links('[B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR]',urlvideo+'IMDB'+imdbcode+'IMDB',iconimage,fanart)                                              

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
                                        #addDir1(name,'url',1001,iconimage,False,fanart)
                                        CME_links('[B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR]',urlvideo+'IMDB'+imdbcode+'IMDB',iconimage,fanart)                                              
                        except: pass
	else: return
        return


def FILMES_ANIMACAO_encontrar_fontes_filmes_CMC(FILMEN,url,pesquisou,imdbc,item):

        num_f = 0
        if item != '':
                if item != '':
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

                        if imdbcode == '':
                                nome_pesquisa = nome + ' ' + ano_filme
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
                                conta = 0
                                for q_a_q_a in qq_aa:
                                        if conta == 0:
                                                nome_p = q_a_q_a
                                                conta = 1
                                        else:
                                                nome_p = nome_p + '+' + q_a_q_a
                                url_imdb = 'http://www.imdb.com/find?ref_=nv_sr_fn&q=' + nome_p + '&s=all#tt'
                                html_imdbcode = abrir_url(url_imdb)
                                filmes_imdb = re.findall('<div class="findSection">(.*?)<div class="findMoreMatches">', html_imdbcode, re.DOTALL)
                                imdb_c = re.compile('/title/(.+?)/[?]ref').findall(filmes_imdb[0])
                                if imdb_c: imdbcode = imdb_c[0]
                        
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
                                                        resultados.append('CINEMAEMCASA|AUDIO|'+qualidade_filme.upper())
                                                        #addDir1(name,'url',1001,iconimage,False,fanart)
                                                        CMC_links('[COLOR orange]CMC | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',urlfilme.replace(' ','%20')+'IMDB'+imdbcode+'IMDB',iconimage,fanart)                                              
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
                                                resultados.append('CINEMAEMCASA|AUDIO|'+qualidade_filme.upper())
                                                #addDir1(name,'url',1001,iconimage,False,fanart)
                                                CMC_links('[COLOR orange]CMC | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',urlfilme.replace(' ','%20')+'IMDB'+imdbcode+'IMDB',iconimage,fanart)                                              

                                        #addDir_trailer('[COLOR orange]CMC | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',urlfilme.replace(' ','%20')+'IMDB'+imdbcode+'IMDB',903,thumb.replace(' ','%20'),sinopse,fanart,ano_filme,genero,nome,urlfilme)
                        except: pass
        else: return
        return

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#        
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
def TFV_links(name,url,iconimage,fanart):
        iconimage = iconimage
        nomeescolha = name
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]
        conta_id_video = 0    
	try:
		link2=abrir_url(url)
	except: link2 = ''
	fontes = re.findall("Clique aqui(.+?)", link2, re.DOTALL)
        numero_de_fontes = len(fontes)
        Partes = re.findall("PARTE(.+?)", link2, re.DOTALL)
        if imdbcode == '':
                items = re.findall('<div class=\'video-item\'>(.*?)<div class=\'clear\'>', link2, re.DOTALL)
                if items != []:
                        imdb = re.compile('imdb.com/title/(.+?)/').findall(items[0])
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
        #addDir1(name,'url',1001,iconimage,False,fanart)
        items = re.findall('<div class=\'video-item\'>(.*?)<div class=\'clear\'>', link2, re.DOTALL)
        if 'Parte 1' and 'Parte 2' not in link2:
                num_leg = 1
                num_ptpt = 1
                matchvid = re.findall("<div class='id(.+?)'>Assistir(.+?)Clique aqui para ver", items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall("<div class='id(.+?)'>Assistir(.+?)</p>", items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall("<div class='id(.+?)'>Assistir(.+?)\n</p>", items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall("<div class='id(.+?)'> Assistir(.+?)Clique aqui para ver", items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall("<div class='id(.+?)'> Assistir(.+?)</p>", items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall("<div class='id(.+?)'> Assistir(.+?)\n</p>", items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall('<div class="id(.+?)">Assistir(.+?)Clique aqui para ver', items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall('<div class="id(.+?)">Assistir(.+?)</p>', items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall('<div class="id(.+?)">Assistir(.+?)\n</p>', items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall('<div class="id(.+?)"> Assistir(.+?)Clique aqui para ver', items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall('<div class="id(.+?)"> Assistir(.+?)</p>', items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall('<div class="id(.+?)"> Assistir(.+?)\n</p>', items[0], re.DOTALL)
                if matchvid:
                        for servidor,matchsvids in matchvid:
                                if 'Legendado' in matchsvids and num_leg == 1:
                                        num_leg = 0
                                        if num_ptpt == 0: conta_id_video = 0
                                        resultados.append('TUGAFILMES.TV|AUDIO|LEGENDADO')
                                        #addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,'')
                                if 'Portug' in matchsvids or 'PT-PT' in matchsvids:
                                        if num_ptpt == 1:
                                                num_ptpt = 0
                                                if num_leg == 0: conta_id_video = 0
                                                resultados.append('TUGAFILMES.TV|AUDIO|PT-PT')
                                                #addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,'')
                                if '</iframe>' in matchsvids:
                                        videomeg = re.compile('<iframe frameborder="0" height="400" scrolling="no" src="(.+?)"').findall(matchsvids)
                                        if videomeg:
                                                conta_id_video = conta_id_video + 1
                                                fonte_id = '(Videomega)'
                                                #addDir('SITESdosPORTUGAS | TUGAFILMES.TV | VIDEOMEGA',videomeg[0],30,iconimage,'',fanart)
                                                PLAY_movie_url(videomeg[0],fonte_id,iconimage,'',fanart,'TUGAFILMES.TV')
                                                #resultados.append(videomeg[0])
                                                
                                match = re.compile('href="(.+?)"').findall(matchsvids)
                                url = match[0] 
                                if url != '':
                                        try:
                                                for url in match:
                                                        identifica_video = re.compile('=(.*)').findall(url)
                                                        id_video = identifica_video[0]
                                                        conta_id_video = conta_id_video + 1
                                                        if "ep" in servidor: url = 'videomega'
                                                        if "vw" in servidor: url = 'videowood'
                                                        if "dv" in servidor: url = 'dropvideo'
                                                        if "vt" in servidor: url = 'vidto.me'
                                                        if "nv" in servidor: url = 'nowvideo'
                                                        #resultados.append(name+id_video+str(conta_id_video)+'TUGAFILMES.TV|AUDIO|PT-PT'+url)
                                                     ##   TFV_resolve_not_videomega_filmes(name,url,id_video,conta_id_video)    
                                                        #TFV_resolve_not_videomega_filmes(name,url,id_video,conta_id_video)
                                                        if "videomega" in url:
                                                                try:
                                                                        url = 'http://videomega.tv/iframe.php?ref=' + id_video# + '///' + name
                                                                        print url
                                                                        fonte_id = '(Videomega)'
                                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                                except: pass
                                                        if "vidto.me" in url:
                                                                try:
                                                                        url = 'http://vidto.me/' + id_video + '.html' + '///' + name
                                                                        print url
                                                                        fonte_id = '(Vidto.me)'
                                                                        resultados.append('SITESdosPORTUGAS | TUGAFILMES.TV | VIDTO.ME'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                                                                except: pass
                                                        if "dropvideo" in url:
                                                                try:
                                                                        url = 'http://dropvideo.com/embed/' + id_video #+ '///' + name
                                                                        print url
                                                                        fonte_id = '(Dropvideo)'
                                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                                except:pass
                                                        if "streamin.to" in url:
                                                                try:
                                                                        url = 'http://streamin.to/embed-' + id_video + '.html' #+ '///' + name
                                                                        print url
                                                                        fonte_id = '(Streamin)'
                                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,30,iconimage,'',fanart)
                                                                except:pass                        
                                                        if "putlocker" in url:
                                                                try:
                                                                        url = 'http://www.putlocker.com/embed/' + id_video# + '///' + name
                                                                        print url
                                                                        fonte_id = '(Putlocker)'
                                                                        resultados.append('SITESdosPORTUGAS | TUGAFILMES.TV | PUTLOCKER'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Putlocker)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                                except:pass
                                                        if "nowvideo" in url:
                                                                try:
                                                                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video #+ '///' + name
                                                                        print url
                                                                        fonte_id = '(Nowvideo)'
                                                                        resultados.append('SITESdosPORTUGAS | TUGAFILMES.TV | NOWVIDEO'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                                except:pass
                                                        if "videowood" in url:
                                                                try:
                                                                        if '/video/' in url: url = url.replace('/video/','/embed/')
                                                                        url = 'http://www.videowood.tv/embed/' + id_video #+ '///' + name
                                                                        print url
                                                                        fonte_id = '(Videowood)'
                                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoWood)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                                except:pass
                                                        if "firedrive" in url:
                                                                try:
                                                                        url = 'http://www.firedrive.com/file/' + id_video #+ '///' + name
                                                                        fonte_id = '(Firedrive)'
                                                                        resultados.append('SITESdosPORTUGAS | TUGAFILMES.TV | FIREDRIVE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                                except:pass
                                                        #if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url:# and 'iiiiiiiiii' in url:
                                                        if  'vidto.me' not in url and 'nowvideo' not in url and 'movshare' not in url and 'firedrive' not in url and 'putlocker' not in url and 'sockshare' not in url:
                                                                PLAY_movie_url(url,fonte_id,iconimage,'',fanart,'TUGAFILMES.TV')
                                        except:pass
                else:
                        videomeg = re.compile('<iframe frameborder="0" height="400" scrolling="no" src="(.+?)"').findall(link2)
                        if videomeg:
                                conta_id_video = conta_id_video + 1
                                fonte_id = '(Videomega)'
                                PLAY_movie_url(videomeg[0],fonte_id,iconimage,'',fanart,'TUGAFILMES.TV')
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',videomeg[0],30,iconimage,'',fanart)

        if 'Parte 1' and 'Parte 2' in link2:
                matchvid = re.findall("<div class='id(.+?)'>Assistir(.+?)Clique aqui para ver", items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall("<div class='id(.+?)'>Assistir(.+?)</p>", items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall("<div class='id(.+?)'>Assistir(.+?)\n</p>", items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall("<div class='id(.+?)'> Assistir(.+?)Clique aqui para ver", items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall("<div class='id(.+?)'> Assistir(.+?)</p>", items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall("<div class='id(.+?)'> Assistir(.+?)\n</p>", items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall('<div class="id(.+?)">Assistir(.+?)Clique aqui para ver', items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall('<div class="id(.+?)">Assistir(.+?)</p>', items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall('<div class="id(.+?)">Assistir(.+?)\n</p>', items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall('<div class="id(.+?)"> Assistir(.+?)Clique aqui para ver', items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall('<div class="id(.+?)"> Assistir(.+?)</p>', items[0], re.DOTALL)
                if not matchvid: matchvid = re.findall('<div class="id(.+?)"> Assistir(.+?)\n</p>', items[0], re.DOTALL)
                if matchvideo:
                        for parte in matchvideo:
                                nome_video = re.compile('(.+?)</div></h3><p>').findall(parte)
                                if nome_video: nome = nome_video[0]
                                else: nome = ''
                                url_videomega = re.compile('<iframe frameborder="0" height="400" scrolling="no" src="(.+?)"').findall(parte)
                                if url_videomega: url = url_videomega[0]
                                else: url = ''
                                url_not_videomega = re.compile('href="(.+?)"').findall(parte)
                                if url_not_videomega:
                                        url = url_not_videomega[0]
                                        identifica_video = re.compile('=(.*)').findall(url)
                                        id_video = identifica_video[0]
                                if "ep" in servidor: url = 'videomega'
                                if "vw" in servidor: url = 'videowood'
                                if "dv" in servidor: url = 'dropvideo'
                                if "vt" in servidor: url = 'vidto.me'
                                if "nv" in servidor: url = 'nowvideo'
##                                if "videomega" in url:
##                                        try:
##                                                url = url# + '///' + name
##                                                fonte_id = '(Videomega)'
##                                                #addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
##                                        except: pass
                                if url != '':
##                                        req = urllib2.Request(url)
##                                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
##                                        response = urllib2.urlopen(req)
##                                        link4=response.read()
##                                        response.close()
##                                        match = re.compile('<iframe src="(.+?)".+?></iframe></center>').findall(link4)
##                                        url=match[0]
                                        if "videomega" in url:
                                                try:
                                                        url = 'http://videomega.tv/iframe.php?ref=' + id_video# + '///' + name
                                                        print url
                                                        fonte_id = '(Videomega)'
                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except: pass
                                        if "vidto.me" in url:
                                                try:
                                                        url = 'http://vidto.me/' + id_video + '.html' + '///' + name
                                                        print url
                                                        fonte_id = '(Vidto.me)'
                                                        resultados.append('SITESdosPORTUGAS | TUGAFILMES.TV | VIDTO.ME'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                                                except: pass
                                        if "dropvideo" in url:
                                                try:
                                                        url = 'http://dropvideo.com/embed/' + id_video #+ '///' + name
                                                        print url
                                                        fonte_id = '(Dropvideo)'
                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if "streamin.to" in url:
                                                try:
                                                        url = 'http://streamin.to/embed-' + id_video + '.html' #+ '///' + name
                                                        print url
                                                        fonte_id = '(Streamin)'
                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,30,iconimage,'',fanart)
                                                except:pass                        
                                        if "putlocker" in url:
                                                try:
                                                        url = 'http://www.putlocker.com/embed/' + id_video# + '///' + name
                                                        print url
                                                        fonte_id = '(Putlocker)'
                                                        resultados.append('SITESdosPORTUGAS | TUGAFILMES.TV | PUTLOCKER'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Putlocker)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if "nowvideo" in url:
                                                try:
                                                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video #+ '///' + name
                                                        print url
                                                        fonte_id = '(Nowvideo)'
                                                        resultados.append('SITESdosPORTUGAS | TUGAFILMES.TV | NOWVIDEO'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if "videowood" in url:
                                                try:
                                                        if '/video/' in url: url = url.replace('/video/','/embed/')
                                                        url = 'http://www.videowood.tv/embed/' + id_video #+ '///' + name
                                                        print url
                                                        fonte_id = '(Videowood)'
                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoWood)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if "firedrive" in url:
                                                try:
                                                        url = 'http://www.firedrive.com/file/' + id_video #+ '///' + name
                                                        fonte_id = '(Firedrive)'
                                                        resultados.append('SITESdosPORTUGAS | TUGAFILMES.TV | FIREDRIVE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        #if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url:# and 'iiiiiiiiii' in url:
                                        if  'vidto.me' not in url and 'nowvideo' not in url and 'movshare' not in url and 'firedrive' not in url and 'putlocker' not in url and 'sockshare' not in url:
                                                PLAY_movie_url(url,fonte_id,iconimage,'',fanart,'TUGAFILMES.TV')


#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#        
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def TFC_links(name,url,iconimage,fanart):
        iconimage = iconimage
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]
                
        nomeescolha = name
        conta_os_items = 0
        conta_os_items = conta_os_items + 1
        conta_id_video = 0
        try:
                fonte = abrir_url(url)
        except: fonte = ''
        items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", fonte, re.DOTALL)
        if not items: items = re.findall("<div id='postagem'>(.*?)<div class='postmeta'>", fonte, re.DOTALL)
	if items != []:
                imdb = re.compile('imdb.com/title/(.+?)/').findall(items[0])
                if imdb: imdbcode = imdb[0]
                else: imdbcode = ''
        assist = re.findall(">ASSISTIR.+?", fonte, re.DOTALL)
        fontes = re.findall("Ver Aqui.+?", fonte, re.DOTALL)
        numero_de_fontes = len(fontes)
        #addLink(str(len(assist)),'','','')
	if fonte:
                if len(assist) > 1:
                        assistir_fontes = re.findall('>ASSISTIR(.*?)------------------------------', fonte, re.DOTALL)
                        if assistir_fontes:
                                for ass_fon in assistir_fontes:
                                        match = re.compile('<iframe .+? src="(.+?)"').findall(ass_fon)
                                        assis = re.compile('ONLINE(.+?)</span>').findall(ass_fon)
                                        conta_video = len(match)
                                        if assis:
                                                if 'LEGENDADO' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        resultados.append('TUGAFILMES.COM|AUDIO|LEGENDADO')
                                                        #addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,fanart)
                                                if 'PT/PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        resultados.append('TUGAFILMES.COM|AUDIO|PT-PT')
                                                        #addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                                elif 'PT-PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        resultados.append('TUGAFILMES.COM|AUDIO|PT-PT')
                                                        #addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        match = re.compile('<a href="(.+?)" target=".+?">Ver Aqui</a>').findall(ass_fon)
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        conta_os_items = conta_os_items + 1
                                assistir_fontes = re.findall("------------------------------<br />(.*?)='postmeta'>", fonte, re.DOTALL)
                                assistir_fontes = re.findall(">ASSISTIR(.*?)<div class", assistir_fontes[0], re.DOTALL)
                                conta_id_video = 0
                                for ass_fon in assistir_fontes:
                                        match = re.compile('<iframe .+? src="(.+?)"').findall(ass_fon)
                                        assis = re.compile('ONLINE(.+?)</span>').findall(ass_fon)
                                        conta_video = len(match)
                                        if assis:
                                                if 'LEGENDADO' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        resultados.append('TUGAFILMES.COM|AUDIO|LEGENDADO')
                                                        #addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,fanart)
                                                if 'PT/PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        resultados.append('TUGAFILMES.COM|AUDIO|PT-PT')
                                                        #addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                                elif 'PT-PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        resultados.append('TUGAFILMES.COM|AUDIO|PT-PT')
                                                        #addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        match = re.compile('<a href="(.+?)" target=".+?">Ver Aqui</a>').findall(ass_fon)
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        conta_os_items = conta_os_items + 1
                        else:
                                assistir_fontes = re.findall('>ASSISTIR(.*?)</iframe>', fonte, re.DOTALL)
                                conta_id_video = 0
                                for ass_fon in assistir_fontes:
                                        match = re.compile('<iframe .+? src="(.+?)"').findall(ass_fon)
                                        assis = re.compile('ONLINE(.+?)</span>').findall(ass_fon)
                                        conta_video = len(match)
                                        if assis:
                                                if 'LEGENDADO' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        resultados.append('TUGAFILMES.COM|AUDIO|LEGENDADO')
                                                        #addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,fanart)
                                                if 'PT/PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        resultados.append('TUGAFILMES.COM|AUDIO|PT-PT')
                                                        #addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                                elif 'PT-PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        resultados.append('TUGAFILMES.COM|AUDIO|PT-PT')
                                                        #addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        match = re.compile('<a href="(.+?)" target=".+?">Ver Aqui</a>').findall(ass_fon)
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        conta_os_items = conta_os_items + 1
                else:
                        match = re.compile('www.videowood(.+?)" target="_blank">.+?[(]Online').findall(fonte)
                        if not match: match = re.compile('<a href="(.+?)" target="_blank">.+?[(]Online').findall(fonte)
                        for url in match:
                                url = 'http://www.videowood'+url                                
                                id_video = ''
                                conta_id_video = conta_id_video + 1
                                TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                conta_os_items = conta_os_items + 1
                        match = re.compile('<iframe .+? src="(.+?)"').findall(fonte)
                        if match:
                                conta_video = len(match)
                                for url in match:
                                        id_video = ''
                                        conta_id_video = conta_id_video + 1
                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        conta_os_items = conta_os_items + 1
                        else:
                                match = re.compile("<script type='text/javascript' src='(.+?)'></script>").findall(fonte)
                                conta_video = len(match)
                                for url in match:
                                        if 'hashkey' in url:
                                                id_video = ''
                                                conta_id_video = conta_id_video + 1
                                                TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                                conta_os_items = conta_os_items + 1
                        if numero_de_fontes > 0:
                                conta_video = 0
                                match = re.compile('<a href="(.+?)" target=".+?">Ver Aqui</a>').findall(fonte)
                                url = match[0]
                                if url != '':
                                        try:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                                        conta_os_items = conta_os_items + 1
                                        except:pass

def TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart):
        if 'videomega' in url: vidv = url
        url = url + '///' + name
        if "videomega" in url:
		try:
                        if 'hashkey' in url:
                                try:
                                        urlvideomega = abrir_url(vidv)
                                except: urlvideomega = ''
                                if urlvideomega != '':
                                        urlvidlink = re.compile('ref="(.+?)"').findall(urlvideomega)
                                        if urlvidlink: url = 'http://videomega.tv/iframe.php?ref=' + urlvidlink[0] + '///' + name
                        fonte_id = '(Videomega)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
        if "vidto.me" in url:
		try:
                        match = re.compile('http://vidto.me/embed-(.+?).html').findall(url)
			if match:
				id_video = match[0]
				url = 'http://vidto.me/' + id_video + '.html'# + '///' + nomeescolha
			fonte_id = '(Vidto.me)'
			#resultados.append('SITESdosPORTUGAS | FOITATUGA | VIDTO.ME',url,30,iconimage,'',fanart)
			resultados.append('SITESdosPORTUGAS | TUGAFILMES.COM | VIDTO.ME'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)

		except: pass
	if "thevideo.me" in url:
		try:
                        fonte_id = '(TheVideo.me)'
			#addDir('SITESdosPORTUGAS | FOITATUGA | THEVIDEO.ME',url,30,iconimage,'',fanart)
		except:pass
        if "dropvideo" in url:
		try:
                        url = url.replace('/video/','/embed/')
                        fonte_id = '(DropVideo)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "vidzi.tv" in url:
                try:
                        fonte_id = '(Vidzi.tv)'
			#addDir('SITESdosPORTUGAS | FOITATUGA | VIDZI.TV',url,30,iconimage,'',fanart)
                except:pass
        if "vodlocker" in url:
		try:
                        fonte_id = '(Vodlocker)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vodlocker)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "played.to" in url:
                try:
                        fonte_id = '(Played.to)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Played.to)[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "cloudzilla" in url:
                try:
                        fonte_id = '(Cloudzilla)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Cloudzilla)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "divxstage" in url:
                try:
                        fonte_id = '(Divxstage)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Divxstage)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "vidzen" in url:
                try:
                        fonte_id = '(Vidzen)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidzen)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
	if "streamin.to" in url:
                try:
                        fonte_id = '(Streamin)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass                        
    	if "nowvideo" in url:
                try:
                        fonte_id = '(Nowvideo)'
                        #addDir('SITESdosPORTUGAS | FOITATUGA | NOWVIDEO',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | TUGAFILMES.COM | NOWVIDEO'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
    		except:pass
    	if "primeshare" in url:
                try:
                        fonte_id = '(Primeshare)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Primeshare.tv)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videoslasher" in url:
                try:
                        fonte_id = '(VideoSlasher)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoSlasher)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "sockshare" in url:
                try:
                        fonte_id = '(Sockshare)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Sockshare)[/COLOR][/B]',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | TUGAFILMES.COM | SOCKSHARE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
    		except:pass
    	if "putlocker" in url:
                try:
                        url = url.replace('putlocker.com/embed/','firedrive.com/file/')
                        fonte_id = '(Firedrive)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | TUGAFILMES.COM | PUTLOCKER'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
    		except:pass
    	else:
                if "firedrive" in url:
                        try:
                                fonte_id = '(Firedrive)'
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                resultados.append('SITESdosPORTUGAS | TUGAFILMES.COM | FIREDRIVE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                        except:pass
    	if "movshare" in url:
                try:
                        fonte_id = '(Movshare)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Movshare)[/COLOR][/B]',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | TUGAFILMES.COM | MOVSHARE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
    		except:pass
        if "video.tt" in url:
                try:
                        url = url.replace('///' + name,'')
                        url = url.replace('/video/','/e/')
                        url = url.replace('/video/','/e/')
                        url = url.replace('http://www.video.tt/e/','http://video.tt/e/')
                        url = url.replace('http://www.video.tt/embed/','http://video.tt/e/')
                        url = url.replace('http://video.tt/e/','http://video.tt/player_control/settings.php?v=')+'&fv=v1.2.74'
                        url = url + '///' + name
                        fonte_id = '(Video.tt)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Video.tt)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(VideoWood)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoWood)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	#if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url:# and 'iiiiiiiiii' in url:
        if  'vidto.me' not in url and 'nowvideo' not in url and 'movshare' not in url and 'firedrive' not in url and 'putlocker' not in url and 'sockshare' not in url:
                PLAY_movie_url(url,fonte_id,iconimage,'',fanart,'TUGAFILMES.COM')
    	return

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#	
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def TPT_links(nomeescolha,urlescolha,iconimage,fanart):#,genre,plot,year):
        iconimage = iconimage
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(urlescolha)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(urlescolha)
        if not urlimdb: url = urlescolha.replace('IMDBIMDB','')
        else: url = urlimdb[0]
        conta_os_items = 0
        nometitulo = nomeescolha
        i = 1
        conta_id_video = 0
        contaultimo = 0
	try:
		link2=abrir_url(url)
	except: link2 = ''
	if link2:
                if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo and imdbcode == '':
                        items = re.findall('<div class="postmeta-primary">(.*?)<div id="sidebar-primary">', link2, re.DOTALL)
                        if items != []:
                                imdb = re.compile('imdb.com/title/(.+?)/').findall(items[0])
                                if imdb: imdbcode = imdb[0]
                                else: imdbcode = ''
                if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo and 'Mini-Serie' not in nometitulo:
                        newmatch = re.findall('<span id=.+?DOWNLOAD',link2,re.DOTALL)
                        l=1
                else:
                        #newmatch = re.findall('<span id=.+?<img style="height: 40px; width: 465px;"',link2,re.DOTALL)
                        newmatch1 = re.findall('<span id=.+?DOWNLOAD',link2,re.DOTALL)
                        newmatch = re.findall('<img style="height: 90px; width: 200px;".+?DOWNLOAD',link2,re.DOTALL)
                        l=5
                if not newmatch:
                        newmatch = re.findall('<span id=.+?<nav class="navigation post-navigation"',link2,re.DOTALL)
                        l=2
                if not newmatch:
                        newmatch = re.findall('<span id=.+?<br/>\n<img',link2,re.DOTALL)
                        l=3
                if not newmatch:
                        newmatch = re.findall('<span id=.+?<img style="height: 40px; width: 465px;"',link2,re.DOTALL)
                        l=4
                if not newmatch:
                        if newmatch1 != [] and 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-Serie' in nometitulo:
                                lin = re.findall('.+?EPIS',newmatch1[0],re.DOTALL)
                                num = len(lin) + 0.0 - 1
                                linkseriesssss = re.findall('</span>CLIQUE AQUI PARA VER O (.+?)</div>(.+?)</div></div><',newmatch1[0],re.DOTALL)
                                for parte1,parte2 in linkseriesssss:
                                        conta_id_video = 0
                                        addDir1('[COLOR blue]'+parte1+'[/COLOR]','','',iconimage,False,fanart)
                                        match = re.compile('<span class="su-lightbox" data-mfp-src="(.+?)" data-mfp-type="iframe">').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                        i = i + 1
                if newmatch:
                        if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo and 'Mini-Serie' not in nometitulo:
                                match = re.compile('<span class="su-lightbox" data-mfp-src="(.+?)" data-mfp-type="iframe">').findall(newmatch[0])
                                for url in match:
                                        if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                conta_id_video = conta_id_video + 1
                                                conta_os_items = conta_os_items + 1
                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                        else:
                                lin = re.findall('.+?EPIS',newmatch1[0],re.DOTALL)
                                num = len(lin) + 0.0 - 1
                                lin = re.findall('.+?EPIS',newmatch[0],re.DOTALL)
                                num = num + len(lin) + 0.0
                                linkseriesssss = re.findall('</span>CLIQUE AQUI PARA VER O (.+?)</div>(.+?)</div></div><',newmatch1[0],re.DOTALL)
                                for parte1,parte2 in linkseriesssss:
                                        conta_id_video = 0
                                        addDir1('[COLOR blue]'+parte1+'[/COLOR]','','',iconimage,False,fanart)
                                        match = re.compile('<span class="su-lightbox" data-mfp-src="(.+?)" data-mfp-type="iframe">').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                        i = i + 1
			linksseccaopartes = re.findall('.+?PARTE',newmatch[0],re.DOTALL)
			if linksseccaopartes:
                                if len(linksseccaopartes) > 1:
                                        linksseccao = re.findall('RTE(.+?)<.+?>\n(.+?)>PA',newmatch[0],re.DOTALL)
                                        for parte1,parte2 in linksseccao:
                                                conta_id_video = 0
                                                conta_os_items = conta_os_items + 1
                                                #addDir1('[COLOR blue] Parte '+parte1+'[/COLOR]','','',iconimage,False,fanart)					
                                                match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                conta_os_items = conta_os_items + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('"window.open(.+?)"').findall(parte2)
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                        v_id = re.compile('=(.*)').findall(url)
                                        if not v_id: v_id = re.compile('//(.*)').findall(url)
                                        nmatch = re.findall(v_id[0]+'.+?DOWNLOAD',link2,re.DOTALL)
                                        if not nmatch: nmatch = re.findall(v_id[0]+'.+?<nav class="navigation post-navigation"',link2,re.DOTALL)
                                        linksseccao = re.findall('PARTE(.+?)<.+?>\n(.+?)<p>&nbsp;</p>',nmatch[0],re.DOTALL)
                                        for parte1,parte2 in linksseccao:
                                                conta_id_video = 0
                                                conta_os_items = conta_os_items + 1
                                                #addDir1('[COLOR blue] Parte '+parte1+'[/COLOR]','','',iconimage,False,fanart)					
                                                match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                conta_os_items = conta_os_items + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('"window.open(.+?)"').findall(parte2)
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                if len(linksseccaopartes) == 1:
                                        linksseccao = re.findall('<p>PARTE(.+?)<.+?>\n(.+?)<p>&nbsp;</p>',newmatch[0],re.DOTALL)
                                        for parte1,parte2 in linksseccao:
                                                conta_id_video = 0
                                                conta_os_items = conta_os_items + 1
                                                #addDir1('[COLOR blue] Parte '+parte1+'[/COLOR]','','',iconimage,False,fanart)					
                                                match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                conta_os_items = conta_os_items + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('"window.open(.+?)"').findall(parte2)
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                        linksseccao = re.findall('<p>PARTE(\d+)</p>\n(.+?)<p>&nbsp;</p>',newmatch[0],re.DOTALL)
                                        for parte1,parte2 in linksseccao:
                                                conta_id_video = 0
                                                conta_os_items = conta_os_items + 1
                                                #addDir1('[COLOR blue] Parte '+parte1+'[/COLOR]','','',iconimage,False,fanart)					
                                                match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                conta_os_items = conta_os_items + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('"window.open(.+?)"').findall(parte2)
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
			else:
                                linksseccao = re.findall('<span style="color:.+?">(.+?)</span><br.+?>(.+?)Ver Aqui</a></p>',newmatch[0],re.DOTALL)
				if linksseccao:
					for parte1,parte2 in linksseccao:
                                                parte1=parte1.replace('[','(').replace(']',')').replace('<strong>','').replace('</strong>','')
                                                conta_id_video = 0
                                                conta_os_items = conta_os_items + 1
						addDir1('[COLOR blue]'+parte1+'[/COLOR]','','',iconimage,False,fanart)					
						match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
						for url in match:
                                                        conta_id_video = conta_id_video + 1
							conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
						match = re.compile('<a href="(.+?)" target="_blank">').findall(parte2)
						if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
						for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                conta_os_items = conta_os_items + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
						match = re.compile('"window.open(.+?)"').findall(parte2)
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
				else:
					linksseccao = re.findall('<span style="color:.+?"><strong>(.+?)</strong></span><br.+?>(.+?)Ver Aqui</a></p>',newmatch[0],re.DOTALL)
                                        if linksseccao:
                                                for parte1,parte2 in linksseccao:
                                                        parte1=parte1.replace('[','(').replace(']',')').replace('<strong>','').replace('</strong>','')
                                                        conta_id_video = 0
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]'+parte1+'[/COLOR]','','',iconimage,False,fanart)					
                                                        match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                        if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                        for url in match:
                                                                conta_id_video = conta_id_video + 1
                                                                conta_os_items = conta_os_items + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                        match = re.compile('<a href="(.+?)" target="_blank">').findall(parte2)
                                                        if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                        for url in match:
                                                                if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                        conta_id_video = conta_id_video + 1
                                                                        conta_os_items = conta_os_items + 1
                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                        match = re.compile('"window.open(.+?)"').findall(parte2)
                                                        for url in match:
                                                                conta_id_video = conta_id_video + 1
                                                                url = url.replace("'","").replace("(","").replace(")","")
                                                                conta_os_items = conta_os_items + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                        else:
                                                if '<h2 class="title">Sleepy Hollow[Season 1][Completa]</h2>' in link2:
                                                        linksseccao = re.findall('<p>(.+?)<br/>(.+?)</p>',newmatch[0],re.DOTALL)
                                                        if linksseccao:
                                                                for parte1,parte2 in linksseccao:
                                                                        if '<p>' in parte1:
                                                                                pp = re.compile('<p>(.*)').findall(parte1)
                                                                                parte1 = pp[0]
                                                                        conta_id_video = 0
                                                                        conta_os_items = conta_os_items + 1
                                                                        addDir1('[COLOR blue] '+parte1+'[/COLOR]','','',iconimage,False,fanart)					
                                                                        match = re.compile('<iframe src="(.+?)"').findall(parte2)	
                                                                        for url in match:
                                                                                conta_id_video = conta_id_video + 1
                                                                                conta_os_items = conta_os_items + 1
                                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                                        if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                                        for url in match:
                                                                                if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        match = re.compile('"window.open(.+?)"').findall(parte2)
                                                                        for url in match:
                                                                                conta_id_video = conta_id_video + 1
                                                                                url = url.replace("'","").replace("(","").replace(")","")
                                                                                conta_os_items = conta_os_items + 1
                                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                else:
                                                        lin = re.findall('.+?EPIS',newmatch[0],re.DOTALL)
                                                        if len(lin) == 1: linksseccao = re.findall('ODIO (.+?)<.+?>(.+?)<img',newmatch[0],re.DOTALL)
                                                        else: linksseccao = re.findall('ODIO (.+?)<.+?>\n(.+?)EPIS',newmatch[0],re.DOTALL)
                                                        linksseccaoultimo = re.findall('ODIO (.+?)<.+?>\n(.+?)</p>',newmatch[0],re.DOTALL)
                                                        if i == 1: num = len(lin) + 0.0
                                                        if linksseccao:
                                                                ultima_parte = ''
                                                                for parte1,parte2 in linksseccao:
                                                                        conta_id_video = 0
                                                                        if parte1 != ultima_parte:
                                                                                conta_os_items = conta_os_items + 1
                                                                                addDir1('[COLOR blue] Episódio '+parte1+'[/COLOR]','','',iconimage,False,fanart)
                                                                        if 'e' in parte1: ultepi = 'e'
                                                                        else: ultepi = int(parte1)
                                                                        match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                                        if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                                        for url in match:
                                                                                conta_id_video = conta_id_video + 1
                                                                                conta_os_items = conta_os_items + 1
                                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                                        if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                                        for url in match:
                                                                                if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        match = re.compile('"window.open(.+?)"').findall(parte2)
                                                                        for url in match:
                                                                                if 'LINK' not in url:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        i = i + 1
                                                                conta_id_video = 0
                                                                v_id = re.compile('=(.*)').findall(url)
                                                                if not v_id: v_id = re.compile('//(.*)').findall(url)
                                                                nmatch = re.findall(v_id[0]+'.+?DOWNLOAD',link2,re.DOTALL)
                                                                if not nmatch: nmatch = re.findall(v_id[0]+'.+?<nav class="navigation post-navigation"',link2,re.DOTALL)
                                                                linksseccao = re.findall('ODIO (.+?)</p>\n<p><b>(.+?)EPIS',nmatch[0],re.DOTALL)
                                                                if linksseccao:
                                                                        for parte1,parte2 in linksseccao:
                                                                                conta_os_items = conta_os_items + 1
                                                                                addDir1('[COLOR blue] Episódio '+parte1+'[/COLOR]','','',iconimage,False,fanart)
                                                                                match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                                                for url in match:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                                                for url in match:
                                                                                        if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                                conta_id_video = conta_id_video + 1
                                                                                                conta_os_items = conta_os_items + 1
                                                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                match = re.compile('"window.open(.+?)"').findall(parte2)
                                                                                for url in match:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                i = i + 1
                                                                conta_id_video = 0
                                                                v_id = re.compile('=(.*)').findall(url)
                                                                if not v_id: v_id = re.compile('//(.*)').findall(url)
                                                                contamatch = re.findall('ODIO (.+?)</p>\n<p><b>',newmatch[0],re.DOTALL)
                                                                linksseccao = re.findall(v_id[0]+'(.+?)<img',newmatch[0],re.DOTALL)
                                                                if linksseccao:
                                                                        match = re.compile('ODIO (.+?)<br').findall(linksseccao[0])
                                                                        if not match: match = re.compile('ODIO (.+?)</p>').findall(linksseccao[0])
                                                                        if match:
                                                                                conta_os_items = conta_os_items + 1
                                                                                addDir1('[COLOR blue] Episódio '+match[0]+'[/COLOR]','','',iconimage,False,fanart)
                                                                        match = re.compile('<iframe.+?src="(.+?)"').findall(linksseccao[0])
                                                                        if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(linksseccao[0])	
                                                                        for url in match:
                                                                                conta_id_video = conta_id_video + 1
                                                                                conta_os_items = conta_os_items + 1
                                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(linksseccao[0])
                                                                        if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(linksseccao[0])
                                                                        for url in match:
                                                                                if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        match = re.compile('"window.open(.+?)"').findall(linksseccao[0])
                                                                        for url in match:
                                                                                conta_id_video = conta_id_video + 1
                                                                                url = url.replace("'","").replace("(","").replace(")","")
                                                                                conta_os_items = conta_os_items + 1
                                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                ####################################################################
                                                        else:
                                                                linksseccao = re.findall('<p>(.+?)EPISODIO<br/>(.+?)</iframe>',newmatch[0],re.DOTALL)
                                                                if linksseccao:
                                                                        for parte1,parte2 in linksseccao:
                                                                                conta_id_video = 0
                                                                                conta_os_items = conta_os_items + 1
                                                                                addDir1('[COLOR blue] '+parte1+' Episódio[/COLOR]','','',iconimage,False,fanart)					
                                                                                match = re.compile('<iframe src="(.+?)"').findall(parte2)	
                                                                                for url in match:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                                                for url in match:
                                                                                        if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                                conta_id_video = conta_id_video + 1
                                                                                                conta_os_items = conta_os_items + 1
                                                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                match = re.compile('"window.open(.+?)"').findall(parte2)
                                                                                for url in match:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                i = i + 1
                                                                        conta_id_video = 0
                                                                        v_id = re.compile('=(.*)').findall(url)
                                                                        if not v_id: v_id = re.compile('//(.*)').findall(url)
                                                                        nmatch = re.findall(v_id[0]+'(.+?)<img',newmatch[0],re.DOTALL)
                                                                        linksseccao = re.findall('<p>(.+?)EPISODIO<br/>(.+?)</iframe>',nmatch[0],re.DOTALL)
                                                                        for parte1,parte2 in linksseccao:
                                                                                conta_id_video = 0
                                                                                conta_os_items = conta_os_items + 1
                                                                                addDir1('[COLOR blue] '+parte1+' Episódio[/COLOR]','','',iconimage,False,fanart)					
                                                                                match = re.compile('<iframe src="(.+?)"').findall(parte2)	
                                                                                for url in match:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                                                for url in match:
                                                                                        if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                                conta_id_video = conta_id_video + 1
                                                                                                conta_os_items = conta_os_items + 1
                                                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                match = re.compile('"window.open(.+?)"').findall(parte2)
                                                                                for url in match:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                i = i + 1
                                                                        if i != int(num):
                                                                                conta_id_video = 0
                                                                                v_id = re.compile('=(.*)').findall(url)
                                                                                if not v_id: v_id = re.compile('//(.*)').findall(url)
                                                                                nmatch = re.findall(v_id[0]+'(.*)',newmatch[0],re.DOTALL)
                                                                                linksseccao = re.findall('/>(.+?)EPISODIO<br/>(.+?)</iframe>',nmatch[0],re.DOTALL)
                                                                                for parte1,parte2 in linksseccao:
                                                                                        conta_id_video = 0
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        addDir1('[COLOR blue] '+parte1.replace('\n','')+' Episódio[/COLOR]','','',iconimage,False,fanart)					
                                                                                        match = re.compile('<iframe src="(.+?)"').findall(parte2)	
                                                                                        for url in match:
                                                                                                conta_id_video = conta_id_video + 1
                                                                                                conta_os_items = conta_os_items + 1
                                                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                                                        if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                                                        for url in match:
                                                                                                if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                                        conta_id_video = conta_id_video + 1
                                                                                                        conta_os_items = conta_os_items + 1
                                                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                        match = re.compile('"window.open(.+?)"').findall(parte2)
                                                                                        for url in match:
                                                                                                conta_id_video = conta_id_video + 1
                                                                                                url = url.replace("'","").replace("(","").replace(")","")
                                                                                                conta_os_items = conta_os_items + 1
                                                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                        i = i + 1
                                                                else:
                                                                        match = re.compile('<iframe.+?src="(.+?)"').findall(newmatch[0])
                                                                        if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(newmatch[0])
                                                                        for url in match:
                                                                                conta_id_video = conta_id_video + 1
                                                                                conta_os_items = conta_os_items + 1
                                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(newmatch[0])
                                                                        if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(newmatch[0])
                                                                        for url in match:
                                                                                if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        match = re.compile('"window.open(.+?)"').findall(newmatch[0])
                                                                        for url in match:
                                                                                conta_id_video = conta_id_video + 1
                                                                                url = url.replace("'","").replace("(","").replace(")","")
                                                                                conta_os_items = conta_os_items + 1
                                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
		else:
			newmatch = re.findall('EM PT/PT:.+?<nav class="navigation post-navigation"',link2,re.DOTALL)
			if newmatch:
				linksseccao = re.findall('<p>PARTE (\d+)<br.+?\n(.+?)</p>',newmatch[0],re.DOTALL)
				if linksseccao:
					for parte1,parte2 in linksseccao:
                                                conta_id_video = 0
                                                conta_os_items = conta_os_items + 1
						#addDir1('[COLOR blue] Parte '+parte1+'[/COLOR]',urlfinal,'',iconimage,False,'')					
						match = re.compile('<iframe src="(.+?)"').findall(parte2)	
						for url in match:
                                                        conta_id_video = conta_id_video + 1
							conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
						match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
						if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
						for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                conta_os_items = conta_os_items + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
						match = re.compile('"window.open(.+?)"').findall(parte2)
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                else:
					linksseccao = re.findall('EPISODIO (.+?)<br.+?\n(.+?)</p>',newmatch[0],re.DOTALL)
					if linksseccao:
                                                ultima_parte = ''
						for parte1,parte2 in linksseccao:
                                                        conta_id_video = 0
							if parte1 != ultima_parte:
                                                                conta_os_items = conta_os_items + 1
                                                                addDir('[COLOR yellow] Episódio '+parte1+'[/COLOR]',urlfinal,'',iconimage,False,'')
							ultima_parte = parte1
							match = re.compile('<iframe src="(.+?)"').findall(parte2)	
							for url in match:
                                                                conta_id_video = conta_id_video + 1
								conta_os_items = conta_os_items + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
							match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
							match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
							match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
							for url in match:
                                                                if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                        conta_id_video = conta_id_video + 1
                                                                        conta_os_items = conta_os_items + 1
                                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
							match = re.compile('"window.open(.+?)"').findall(parte2)
                                                        for url in match:
                                                                conta_id_video = conta_id_video + 1
                                                                url = url.replace("'","").replace("(","").replace(")","")
                                                                conta_os_items = conta_os_items + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
					else:
						match = re.compile('<iframe src="(.+?)"').findall(newmatch[0])	
						for url in match:
                                                        conta_id_video = conta_id_video + 1
							conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
						match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(newmatch[0])
                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(newmatch[0])
						for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                conta_os_items = conta_os_items + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
						match = re.compile('"window.open(.+?)"').findall(newmatch[0])
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)


def TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart):

        
        if "videomega" in url:
		try:
                        fonte_id = '(Videomega)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
        if "vidto.me" in url:
		try:
                        match = re.compile('http://vidto.me/embed-(.+?).html').findall(url)
			if match:
				id_video = match[0]
				url1 = 'http://vidto.me/' + id_video + '.html'
				fonte_id = '(Vidto.me)'
				url = 'http://vidto.me/' + id_video + '.html'
			else: fonte_id = '(Vidto.me)'
			fonte_id1 = '(Vidto.me)'
			#fonte_id = '(Vidto.me)'+url
			if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('SITESdosPORTUGAS | TOPPT | VIDTO.ME',url,30,iconimage,'',fanart)
                                resultados.append('SITESdosPORTUGAS | TOPPT | VIDTO.ME'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
		except: pass
        if "dropvideo" in url:
		try:
                        #url = url.replace('/video/','/embed/')
                        fonte_id = '(DropVideo)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "vidzi.tv" in url:
                try:
                        fonte_id = '(Vidzi.tv)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('SITESdosPORTUGAS | TOPPT | VIDZI.TV',url,30,iconimage,'',fanart)
                                #resultados.append('SITESdosPORTUGAS | TOPPT | VIDZI.TV'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                except:pass
        if "vodlocker" in url:
		try:
                        fonte_id = '(Vodlocker)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "played.to" in url:
                try:
                        fonte_id = '(Played.to)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "cloudzilla" in url:
                try:
                        fonte_id = '(Cloudzilla)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "divxstage" in url:
                try:
                        fonte_id = '(Divxstage)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "vidzen" in url:
                try:
                        fonte_id = '(Vidzen)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
	if "streamin.to" in url:
                try:
                        fonte_id = '(Streamin)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass                        
    	if "nowvideo" in url:
                try:
                        fonte_id = '(Nowvideo)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('SITESdosPORTUGAS | TOPPT | NOWVIDEO',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | TOPPT | NOWVIDEO'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
    		except:pass
    	if "primeshare" in url:
                try:
                        fonte_id = '(Primeshare)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videoslasher" in url:
                try:
                        fonte_id = '(VideoSlasher)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "sockshare" in url:
                try:
                        fonte_id = '(Sockshare)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('SITESdosPORTUGAS | TOPPT | SOCKSHARE',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | TOPPT | SOCKSHARE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
    		except:pass
    	if "putlocker" in url:
                try:
                        url = url.replace('putlocker.com/embed/','firedrive.com/file/')
                        fonte_id = '(Firedrive)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('SITESdosPORTUGAS | TOPPT | PUTLOCKER',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | TOPPT | PUTLOCKER'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
    		except:pass
    	else:
                if "firedrive" in url:
                        try:
                                fonte_id = '(Firedrive)'
                                #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                        #addDir('SITESdosPORTUGAS | TOPPT | FIREDRIVE',url,30,iconimage,'',fanart)
                                resultados.append('SITESdosPORTUGAS | TOPPT | FIREDRIVE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                        except:pass
    	if "movshare" in url:
                try:
                        fonte_id = '(Movshare)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('SITESdosPORTUGAS | TOPPT | MOVSHARE',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | TOPPT | MOVSHARE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
    		except:pass
        if "video.tt" in url:
                try:
                        url = url.replace('///' + nomeescolha,'')
                        url = url.replace('/video/','/e/')
                        url = url.replace('/video/','/e/')
                        url = url.replace('http://www.video.tt/e/','http://video.tt/e/')
                        url = url.replace('http://www.video.tt/embed/','http://video.tt/e/')
                        url = url.replace('http://video.tt/e/','http://video.tt/player_control/settings.php?v=')+'&fv=v1.2.74'
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:                     
                                url = url
                        fonte_id = '(Video.tt)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('1[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(VideoWood)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "thevideo.me" in url:
                try:
                        #if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(Thevideo.me)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('SITESdosPORTUGAS | TOPPT | THEVIDEO.ME',url,30,iconimage,'',fanart)
    		except:pass
    	#addLink(url,'','','')
        #if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url and 'sockshare' not in url and 'firedrive' not in url and 'movshare' not in url and 'nowvideo' not in url and 'putlocker' not in url:# and 'iiiiiiiiii' in url:
        if  'vidto.me' not in url and 'nowvideo' not in url and 'movshare' not in url and 'firedrive' not in url and 'putlocker' not in url and 'sockshare' not in url:
                PLAY_movie_url(url,fonte_id,iconimage,'',fanart,'TOPPT')
    	return fonte_id

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#	
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def CME_links(name,url,iconimage,fanart):
        iconimage = iconimage
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]
        nomeescolha = name
        colecao = 'nao'
        conta_id_video = 0
        try:
                fonte_video = abrir_url(url)
        except: fonte_video = ''
        fontes_video = re.findall("<h3 class='post-title entry-title(.*?)<div style='clear: both;'>", fonte_video, re.DOTALL)
        numero_de_fontes = len(fontes_video)
        #if 'BREVEMENTE ONLINE' in fonte_video: #addDir1('[COLOR blue]BREVEMENTE ONLINE[/COLOR]','url',1004,artfolder,False,'')
        for fonte_e_url in fontes_video:
                if imdbcode == '':
                        imdb = re.compile('imdb.com/title/(.+?)"').findall(fonte_e_url)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                #if 'BREVEMENTE ONLINE' in fontes_video: addDir1('[COLOR blue]BREVEMENTE ONLINE[/COLOR]','url',1004,artfolder,False,'')
                match1 = re.compile('<script src="(.+?)" type="text/javascript"></script>').findall(fonte_e_url)
                for fonte_id in match1: 
                        if 'videomega' in fonte_id:
                                try:  
                                        if 'hashkey' in fonte_id:
                                                conta_id_video = conta_id_video + 1
                                                try:
                                                        urlvideomega = abrir_url(fonte_id)
                                                except: urlvideomega = ''
                                                if urlvideomega != '':
                                                        urlvidlink = re.compile('ref="(.+?)"').findall(urlvideomega)
                                                        if urlvidlink: url = 'http://videomega.tv/iframe.php?ref=' + urlvidlink[0] + '///' + name
                                                        fonte_serv = '(Videomega)'
                                                        PLAY_movie_url(url,fonte_serv,iconimage,'',fanart,'CINEMATUGA.EU')
                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                        if 'iframe.js' in fonte_id:
                                                conta_id_video = conta_id_video + 1
                                                refvideo = re.compile('<script type="text/javascript">ref="(.+?)".+?</script>').findall(fonte_e_url)
                                                if not refvideo: refvideo = re.compile(">ref='(.+?)'.+?</script>").findall(fonte_e_url)
                                                url = 'http://videomega.tv/iframe.php?ref=' + refvideo[0] + '///' + name
                                                fonte_serv = '(Videomega)'
                                                PLAY_movie_url(url,fonte_serv,iconimage,'',fanart,'CINEMATUGA.EU')
                                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                match2 = re.compile('<iframe.+?src=(.+?) frameborder.+?</iframe>').findall(fonte_e_url)
                for fonte_id in match2:
                        if 'videomega' in fonte_id:
                                try:
                                        conta_id_video = conta_id_video + 1
                                        url = fonte_id + '///' + name
                                        fonte_serv = '(Videomega)'
                                        PLAY_movie_url(url,fonte_serv,iconimage,'',fanart,'CINEMATUGA.EU')
                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                        elif 'dropvideo' in fonte_id:
                                try:
                                        conta_id_video = conta_id_video + 1
                                        url = fonte_id + '///' + name
                                        fonte_serv = '(Dropvideo)'
                                        PLAY_movie_url(url,fonte_serv,iconimage,'',fanart,'CINEMATUGA.EU')
                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Dropvideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                        elif 'vidto.me' in fonte_id:
                                try:
                                        conta_id_video = conta_id_video + 1
                                        fonte_id = fonte_id.replace('embed-','')
                                        refvideo = re.compile('http://vidto.me/embed-(.+?).html').findall(fonte_id)
                                        if refvideo: url = 'http://vidto.me/' + refvideo[0] + '.html' + '///' + name
                                        else: url = fonte_id + '///' + name
                                        #addDir('SITESdosPORTUGAS | CINEMATUGA.EU | VIDTO.ME',url,30,iconimage,'',fanart)
                                        resultados.append('SITESdosPORTUGAS | CINEMATUGA.EU | VIDTO.ME'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                                except:pass
                        else:
                                conta_id_video = conta_id_video + 1
                                CME_resolve_not_videomega_filmes(fonte_id,nomeescolha,conta_id_video,fanart,iconimage)


def CME_resolve_not_videomega_filmes(url,nomeescolha,conta_id_video,fanart,iconimage):
        url = url + '///' + nomeescolha
        if "videomega" in url:
		try:
                        fonte_id = '(Videomega)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
        if "vidto.me" in url:
		try:
                        match = re.compile('http://vidto.me/embed-(.+?).html').findall(url)
			if match:
				id_video = match[0]
				url = 'http://vidto.me/' + id_video + '.html'# + '///' + nomeescolha
			fonte_id = '(Vidto.me)'
			#resultados.append('SITESdosPORTUGAS | FOITATUGA | VIDTO.ME',url,30,iconimage,'',fanart)
			resultados.append('SITESdosPORTUGAS | CINEMATUGA.EU | VIDTO.ME'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)

		except: pass
	if "thevideo.me" in url:
		try:
                        fonte_id = '(TheVideo.me)'
			#addDir('SITESdosPORTUGAS | FOITATUGA | THEVIDEO.ME',url,30,iconimage,'',fanart)
		except:pass
        if "dropvideo" in url:
		try:
                        url = url.replace('/video/','/embed/')
                        fonte_id = '(DropVideo)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "vidzi.tv" in url:
                try:
                        fonte_id = '(Vidzi.tv)'
			#addDir('SITESdosPORTUGAS | FOITATUGA | VIDZI.TV',url,30,iconimage,'',fanart)
                except:pass
        if "vodlocker" in url:
		try:
                        fonte_id = '(Vodlocker)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vodlocker)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "played.to" in url:
                try:
                        fonte_id = '(Played.to)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Played.to)[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "cloudzilla" in url:
                try:
                        fonte_id = '(Cloudzilla)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Cloudzilla)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "divxstage" in url:
                try:
                        fonte_id = '(Divxstage)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Divxstage)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "vidzen" in url:
                try:
                        fonte_id = '(Vidzen)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidzen)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
	if "streamin.to" in url:
                try:
                        fonte_id = '(Streamin)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass                        
    	if "nowvideo" in url:
                try:
                        fonte_id = '(Nowvideo)'
                        #addDir('SITESdosPORTUGAS | FOITATUGA | NOWVIDEO',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | CINEMATUGA.EU | NOWVIDEO'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
    		except:pass
    	if "primeshare" in url:
                try:
                        fonte_id = '(Primeshare)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Primeshare.tv)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videoslasher" in url:
                try:
                        fonte_id = '(VideoSlasher)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoSlasher)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "sockshare" in url:
                try:
                        fonte_id = '(Sockshare)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Sockshare)[/COLOR][/B]',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | CINEMATUGA.EU | SOCKSHARE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
    		except:pass
    	if "putlocker" in url:
                try:
                        url = url.replace('putlocker.com/embed/','firedrive.com/file/')
                        fonte_id = '(Firedrive)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | CINEMATUGA.EU | PUTLOCKER'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
    		except:pass
    	else:
                if "firedrive" in url:
                        try:
                                fonte_id = '(Firedrive)'
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                resultados.append('SITESdosPORTUGAS | CINEMATUGA.EU | FIREDRIVE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                        except:pass
    	if "movshare" in url:
                try:
                        fonte_id = '(Movshare)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Movshare)[/COLOR][/B]',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | CINEMATUGA.EU | MOVSHARE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
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
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Video.tt)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(VideoWood)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoWood)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	#addLink(url,'','','')
    	#if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url:# and 'iiiiiiiiii' in url:
        if  'vidto.me' not in url and 'nowvideo' not in url and 'movshare' not in url and 'firedrive' not in url and 'putlocker' not in url and 'sockshare' not in url:
                PLAY_movie_url(url,fonte_id,iconimage,'',fanart,'CINEMATUGA.EU')
    	return



#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#


def CMC_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart):
        
        
        if "videomega" in url:
		try:
                        fonte_id = '(Videomega)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
        if "vidto.me" in url:
		try:
                        match = re.compile('http://vidto.me/embed-(.+?).html').findall(url)
			if match:
				id_video = match[0]
				url = 'http://vidto.me/' + id_video + '.html'# + '///' + nomeescolha
			fonte_id = '(Vidto.me)'
			#resultados.append('SITESdosPORTUGAS | FOITATUGA | VIDTO.ME',url,30,iconimage,'',fanart)
			resultados.append('SITESdosPORTUGAS | CINEMAEMCASA | VIDTO.ME'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)

		except: pass
	if "thevideo.me" in url:
		try:
                        fonte_id = '(TheVideo.me)'
			#addDir('SITESdosPORTUGAS | FOITATUGA | THEVIDEO.ME',url,30,iconimage,'',fanart)
		except:pass
        if "dropvideo" in url:
		try:
                        url = url.replace('/video/','/embed/')
                        fonte_id = '(DropVideo)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "vidzi.tv" in url:
                try:
                        fonte_id = '(Vidzi.tv)'
			#addDir('SITESdosPORTUGAS | FOITATUGA | VIDZI.TV',url,30,iconimage,'',fanart)
                except:pass
        if "vodlocker" in url:
		try:
                        fonte_id = '(Vodlocker)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vodlocker)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "played.to" in url:
                try:
                        fonte_id = '(Played.to)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Played.to)[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "cloudzilla" in url:
                try:
                        fonte_id = '(Cloudzilla)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Cloudzilla)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "divxstage" in url:
                try:
                        fonte_id = '(Divxstage)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Divxstage)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "vidzen" in url:
                try:
                        fonte_id = '(Vidzen)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidzen)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
	if "streamin.to" in url:
                try:
                        fonte_id = '(Streamin)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass                        
    	if "nowvideo" in url:
                try:
                        fonte_id = '(Nowvideo)'
                        #addDir('SITESdosPORTUGAS | FOITATUGA | NOWVIDEO',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | CINEMAEMCASA | NOWVIDEO'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
    		except:pass
    	if "primeshare" in url:
                try:
                        fonte_id = '(Primeshare)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Primeshare.tv)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videoslasher" in url:
                try:
                        fonte_id = '(VideoSlasher)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoSlasher)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "sockshare" in url:
                try:
                        fonte_id = '(Sockshare)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Sockshare)[/COLOR][/B]',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | CINEMAEMCASA | SOCKSHARE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
    		except:pass
    	if "putlocker" in url:
                try:
                        url = url.replace('putlocker.com/embed/','firedrive.com/file/')
                        fonte_id = '(Firedrive)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | CINEMAEMCASA | PUTLOCKER'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
    		except:pass
    	else:
                if "firedrive" in url:
                        try:
                                fonte_id = '(Firedrive)'
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                resultados.append('SITESdosPORTUGAS | CINEMAEMCASA | FIREDRIVE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                        except:pass
    	if "movshare" in url:
                try:
                        fonte_id = '(Movshare)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Movshare)[/COLOR][/B]',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | CINEMAEMCASA | MOVSHARE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
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
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Video.tt)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(VideoWood)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoWood)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	#addLink(url,'','','')
        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                #if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url and 'sockshare' not in url and 'firedrive' not in url and 'movshare' not in url and 'nowvideo' not in url and 'putlocker' not in url:# and 'iiiiiiiiii' in url:
        if  'vidto.me' not in url and 'nowvideo' not in url and 'movshare' not in url and 'firedrive' not in url and 'putlocker' not in url and 'sockshare' not in url:
                PLAY_movie_url(url,fonte_id.replace(url,''),iconimage,'',fanart,'CINEMAEMCASA')
    	return fonte_id

#---------------------------------------------------------------------------------------------------------

def CMC_links(name,url,iconimage,fanart):
        iconimage = iconimage
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]
        nomeescolha = name
        colecao = 'nao'
        conta_id_video = 0
        conta_os_items = 0
        #addLink(imdbcode,'','','')
        try:
                fonte_video = abrir_url(url)
        except: fonte_video = ''
        
        fontes_video = re.findall("<div class='post-body entry-content'>(.+?)<div class='post-footer'>", fonte_video, re.DOTALL)
        if imdbcode == '':
                imdb = re.compile('imdb.com/title/(.+?)/').findall(fonte_video)
                if imdb: imdbcode = imdb[0]
                else: imdbcode = ''
        numero_de_fontes = len(fontes_video)
        for fonte_e_url in fontes_video:
                matchs = re.compile('<iframe.+?src="(.+?)".+?></iframe>').findall(fonte_e_url)
                for match in matchs:
                        conta_id_video = conta_id_video + 1
                        url = match
                        conta_os_items = conta_os_items + 1
                        CMC_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)



#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#


def MVT_links(name,url,iconimage,fanart):
        iconimage = iconimage
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]
        nomeescolha = name
        colecao = 'nao'
        conta_id_video = 0
        
        try:
                fonte_video = abrir_url(url)
        except: fonte_video = ''
        
        fontes_video = re.findall("<body>(.+?)</body>", fonte_video, re.DOTALL)
##        if imdbcode == '':
##                imdb = re.compile('imdb.com/title/(.+?)/').findall(fonte_video)
##                if imdb: imdbcode = imdb[0]
##                else: imdbcode = ''
        numero_de_fontes = len(fontes_video)
        for fonte_e_url in fontes_video:
                match = re.compile('<option value=(.+?)>(.+?)<').findall(fonte_e_url)
                if not match: match = re.compile('<div class="btns"><a href="(.+?)" target="Player">').findall(fonte_e_url)
                if '<option' in fonte_e_url:
                        for url_video_url_id,cd in match:
                                if url_video_url_id == '""':
                                        if 'CD' in cd:
                                                conta_id_video = 0
                                                cd = cd.replace('Filme Aqui','')
                                                #addDir1('[COLOR blue]' + cd + '[/COLOR]','','',iconimage,False,fanart)
                                        if 'Cole' in cd:
                                                conta_id_video = 0
                                                colecao = 'sim'
                                else:
                                        url_video_url_id = url_video_url_id.replace('"','')
                                if colecao == 'sim' and (('Breve' or 'breve') not in cd):
                                        if 'Cole' not in cd:
                                                conta_id_video = 0
                                                #addDir1('[COLOR blue]' + cd + ':[/COLOR]','','',iconimage,False,fanart)
                                if 'http:' not in url_video_url_id:
                                        url_video = 'http:' + url_video_url_id
                                else:
                                        url_video = url_video_url_id
                                try:
                                        fonte = abrir_url(url_video)
                                except: fonte = ''
                                fontes = re.findall("<body>(.+?)</body>", fonte, re.DOTALL)
                                for fonte_ids in fontes:
                                        if 'videomega' in fonte_ids:
                                                try:
                                                        match = re.compile("<script type=\'text/javascript\'>ref=\'(.+?)\'").findall(fonte_ids)
                                                        conta_id_video = conta_id_video + 1
                                                        id_video = match[0]
                                                        url = 'http://videomega.tv/iframe.php?ref=' + id_video# + '///' + name
                                                        fonte_serv = '(Videomega)'
                                                        PLAY_movie_url(url,fonte_serv,iconimage,'',fanart,'MOVIETUGA')
                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,100,iconimage,'',fanart)
                                                except:pass
                                        elif 'vidto' in fonte_ids:
                                                try:
                                                        match = re.compile('<iframe .+? src=".+?//vidto.me/embed-(.+?)" .+?</iframe>').findall(fonte_ids)
                                                        conta_id_video = conta_id_video + 1
                                                        if match: match = re.compile('(.+?)-').findall(match[0])
                                                        id_video = match[0]
                                                        url = 'http://vidto.me/' + id_video + '.html'# + '///' + name
                                                        #addDir('SITESdosPORTUGAS | MOVIETUGA | VIDTO.ME',url,100,iconimage,'',fanart)
                                                        resultados.append('SITESdosPORTUGAS | MOVIETUGA | VIDTO.ME'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                                                except:pass
                                        else:
                                                match = re.compile('<iframe.+?src="(.+?)".+?</iframe>').findall(fonte_ids)
                                                if match:
                                                        url = match[0]
                                                        conta_id_video = conta_id_video + 1
                                                        MVT_encontrar_streams(url,nomeescolha,iconimage,fanart,conta_id_video)
                else:
 	                if fonte_video:
 		                for fonte_ids in fontes_video:
                                        if 'videomega' in fonte_ids:
                                                try:
                                                        match = re.compile("<script type=\'text/javascript\'>ref=\'(.+?)\'").findall(fonte_ids)
                                                        conta_id_video = conta_id_video + 1
                                                        id_video = match[0]
                                                        url = 'http://videomega.tv/iframe.php?ref=' + id_video# + '///' + name
                                                        fonte_serv = '(Videomega)'
                                                        PLAY_movie_url(url,fonte_serv,iconimage,'',fanart,'MOVIETUGA')
                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,100,iconimage,'',fanart)
                                                except:pass
                                        elif 'vidto' in fonte_ids:
                                                try:
                                                        match = re.compile('<iframe .+? src=".+?//vidto.me/embed-(.+?)" .+?</iframe>').findall(fonte_ids)
                                                        conta_id_video = conta_id_video + 1
                                                        if match: match = re.compile('(.+?)-').findall(match[0])
                                                        id_video = match[0]
                                                        url = 'http://vidto.me/' + id_video + '.html'# + '///' + name
                                                        #addDir('SITESdosPORTUGAS | MOVIETUGA | VIDTO.ME',url,100,iconimage,'',fanart)
                                                        resultados.append('SITESdosPORTUGAS | MOVIETUGA | VIDTO.ME'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                                                except:pass
                                        else:
                                                match = re.compile('<iframe.+?src="(.+?)".+?</iframe>').findall(fonte_ids)
                                                if match:
                                                        url = match[0]
                                                        conta_id_video = conta_id_video + 1
                                                        MVT_encontrar_streams(url,nomeescolha,iconimage,fanart,conta_id_video)

def MVT_encontrar_streams(url,nomeescolha,iconimage,fanart,conta_id_video):
        if "videomega" in url:
		try:
                        fonte_id = '(Videomega)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
        if "vidto.me" in url:
		try:
                        match = re.compile('http://vidto.me/embed-(.+?).html').findall(url)
			if match:
				id_video = match[0]
				url1 = 'http://vidto.me/' + id_video + '.html'
				fonte_id = '(Vidto.me)'
				url = 'http://vidto.me/' + id_video + '.html'
			else: fonte_id = '(Vidto.me)'
			fonte_id1 = '(Vidto.me)'
			#fonte_id = '(Vidto.me)'+url
			if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('SITESdosPORTUGAS | TOPPT | VIDTO.ME',url,30,iconimage,'',fanart)
                                resultados.append('SITESdosPORTUGAS | MOVIETUGA | VIDTO.ME'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
		except: pass
        if "dropvideo" in url:
		try:
                        #url = url.replace('/video/','/embed/')
                        fonte_id = '(DropVideo)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "vidzi.tv" in url:
                try:
                        fonte_id = '(Vidzi.tv)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('SITESdosPORTUGAS | TOPPT | VIDZI.TV',url,30,iconimage,'',fanart)
                                #resultados.append('SITESdosPORTUGAS | TOPPT | VIDZI.TV'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                except:pass
        if "vodlocker" in url:
		try:
                        fonte_id = '(Vodlocker)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "played.to" in url:
                try:
                        fonte_id = '(Played.to)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "cloudzilla" in url:
                try:
                        fonte_id = '(Cloudzilla)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "divxstage" in url:
                try:
                        fonte_id = '(Divxstage)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "vidzen" in url:
                try:
                        fonte_id = '(Vidzen)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
	if "streamin.to" in url:
                try:
                        fonte_id = '(Streamin)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass                        
    	if "nowvideo" in url:
                try:
                        fonte_id = '(Nowvideo)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('SITESdosPORTUGAS | TOPPT | NOWVIDEO',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | MOVIETUGA | NOWVIDEO'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
    		except:pass
    	if "primeshare" in url:
                try:
                        fonte_id = '(Primeshare)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videoslasher" in url:
                try:
                        fonte_id = '(VideoSlasher)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "sockshare" in url:
                try:
                        fonte_id = '(Sockshare)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('SITESdosPORTUGAS | TOPPT | SOCKSHARE',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | MOVIETUGA | SOCKSHARE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
    		except:pass
    	if "putlocker" in url:
                try:
                        url = url.replace('putlocker.com/embed/','firedrive.com/file/')
                        fonte_id = '(Firedrive)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('SITESdosPORTUGAS | TOPPT | PUTLOCKER',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | MOVIETUGA | PUTLOCKER'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
    		except:pass
    	else:
                if "firedrive" in url:
                        try:
                                fonte_id = '(Firedrive)'
                                #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                        #addDir('SITESdosPORTUGAS | TOPPT | FIREDRIVE',url,30,iconimage,'',fanart)
                                resultados.append('SITESdosPORTUGAS | MOVIETUGA | FIREDRIVE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                        except:pass
    	if "movshare" in url:
                try:
                        fonte_id = '(Movshare)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('SITESdosPORTUGAS | TOPPT | MOVSHARE',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | MOVIETUGA | MOVSHARE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
    		except:pass
        if "video.tt" in url:
                try:
                        url = url.replace('///' + nomeescolha,'')
                        url = url.replace('/video/','/e/')
                        url = url.replace('/video/','/e/')
                        url = url.replace('http://www.video.tt/e/','http://video.tt/e/')
                        url = url.replace('http://www.video.tt/embed/','http://video.tt/e/')
                        url = url.replace('http://video.tt/e/','http://video.tt/player_control/settings.php?v=')+'&fv=v1.2.74'
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:                     
                                url = url
                        fonte_id = '(Video.tt)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('1[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(VideoWood)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "thevideo.me" in url:
                try:
                        #if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(Thevideo.me)'
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('SITESdosPORTUGAS | TOPPT | THEVIDEO.ME',url,30,iconimage,'',fanart)
    		except:pass
    	#addLink(url,'','','')
        #if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url and 'sockshare' not in url and 'firedrive' not in url and 'movshare' not in url and 'nowvideo' not in url and 'putlocker' not in url:# and 'iiiiiiiiii' in url:
        if  'vidto.me' not in url and 'nowvideo' not in url and 'movshare' not in url and 'firedrive' not in url and 'putlocker' not in url and 'sockshare' not in url:
                PLAY_movie_url(url,fonte_id,iconimage,'',fanart,'MOVIETUGA')
    	return fonte_id

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def CMT_links(name,url,iconimage,fanart):
        iconimage = iconimage
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]
        nomeescolha = name
        conta_id_video = 0
        conta_os_items = 0    
	try:
		link2=abrir_url(url)
	except: link2 = ''
	if imdbcode == '':
                items = re.findall("<div class='video-item'>(.+?)<div class='clear'>", link2, re.DOTALL)
                if items != []:
                        imdb = re.compile('imdb.com/title/(.+?)/').findall(items[0])
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
	nao = 0
        matchvid = re.findall("Assitir online(.+?)</iframe>", link2, re.DOTALL)
        if not matchvid:
                nao = 1
                matchvid = re.findall("<div class='video-item'>(.+?)<div class='clear'>", link2, re.DOTALL)
        for matchs in matchvid:
                try:
                        nome = re.compile('(.+?)\n.+?').findall(matchs)
                        if not nome: nome = re.compile('(.+?)</b>').findall(matchs)
                        #if nao == 0: addDir1('[COLOR blue]'+nome[0]+':[/COLOR]','url',1004,iconimage,False,fanart)
                        urlvideo = re.compile('<iframe.+?src="(.+?)"').findall(matchs)
                        if not urlvideo: urlvideo = re.compile('src="(.+?)"').findall(matchs)
                        url = urlvideo[0]
                        conta_id_video = conta_id_video + 1
                        conta_os_items = conta_os_items + 1
                        ##############################################CINEMATUGA.NET
                        url = url + '///' + nomeescolha
                        if "videomega" in url:
                                try:
                                        fonte_id = '(Videomega)'
                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except: pass
                        if "vidto.me" in url:
                                try:
                                        match = re.compile('http://vidto.me/embed-(.+?).html').findall(url)
                                        if match:
                                                id_video = match[0]
                                                url = 'http://vidto.me/' + id_video + '.html'# + '///' + nomeescolha
                                        fonte_id = '(Vidto.me)'
                                        #resultados.append('SITESdosPORTUGAS | FOITATUGA | VIDTO.ME',url,30,iconimage,'',fanart)
                                        resultados.append('SITESdosPORTUGAS | CINEMATUGA.NET | VIDTO.ME'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)

                                except: pass
                        if "thevideo.me" in url:
                                try:
                                        fonte_id = '(TheVideo.me)'
                                        #addDir('SITESdosPORTUGAS | FOITATUGA | THEVIDEO.ME',url,30,iconimage,'',fanart)
                                except:pass
                        if "dropvideo" in url:
                                try:
                                        url = url.replace('/video/','/embed/')
                                        fonte_id = '(DropVideo)'
                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                        if "vidzi.tv" in url:
                                try:
                                        fonte_id = '(Vidzi.tv)'
                                        #addDir('SITESdosPORTUGAS | FOITATUGA | VIDZI.TV',url,30,iconimage,'',fanart)
                                except:pass
                        if "vodlocker" in url:
                                try:
                                        fonte_id = '(Vodlocker)'
                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vodlocker)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                        if "played.to" in url:
                                try:
                                        fonte_id = '(Played.to)'
                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Played.to)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                        if "cloudzilla" in url:
                                try:
                                        fonte_id = '(Cloudzilla)'
                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Cloudzilla)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                        if "divxstage" in url:
                                try:
                                        fonte_id = '(Divxstage)'
                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Divxstage)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                        if "vidzen" in url:
                                try:
                                        fonte_id = '(Vidzen)'
                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidzen)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                        if "streamin.to" in url:
                                try:
                                        fonte_id = '(Streamin)'
                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass                        
                        if "nowvideo" in url:
                                try:
                                        fonte_id = '(Nowvideo)'
                                        #addDir('SITESdosPORTUGAS | FOITATUGA | NOWVIDEO',url,30,iconimage,'',fanart)
                                        resultados.append('SITESdosPORTUGAS | CINEMATUGA.NET | NOWVIDEO'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                                except:pass
                        if "primeshare" in url:
                                try:
                                        fonte_id = '(Primeshare)'
                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Primeshare.tv)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                        if "videoslasher" in url:
                                try:
                                        fonte_id = '(VideoSlasher)'
                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoSlasher)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                        if "sockshare" in url:
                                try:
                                        fonte_id = '(Sockshare)'
                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Sockshare)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                        resultados.append('SITESdosPORTUGAS | CINEMATUGA.NET | SOCKSHARE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                                except:pass
                        if "putlocker" in url:
                                try:
                                        url = url.replace('putlocker.com/embed/','firedrive.com/file/')
                                        fonte_id = '(Firedrive)'
                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                        resultados.append('SITESdosPORTUGAS | CINEMATUGA.NET | PUTLOCKER'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                                except:pass
                        else:
                                if "firedrive" in url:
                                        try:
                                                fonte_id = '(Firedrive)'
                                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                resultados.append('SITESdosPORTUGAS | CINEMATUGA.NET | FIREDRIVE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                                        except:pass
                        if "movshare" in url:
                                try:
                                        fonte_id = '(Movshare)'
                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Movshare)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                        resultados.append('SITESdosPORTUGAS | CINEMATUGA.NET | MOVSHARE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
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
                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Video.tt)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                        if "videowood" in url:
                                try:
                                        if '/video/' in url: url = url.replace('/video/','/embed/')
                                        print url
                                        fonte_id = '(VideoWood)'
                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoWood)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass

                        #if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url and 'nowvideo' not in url:# and 'iiiiiiiiii' in url:
                        if  'vidto.me' not in url and 'nowvideo' not in url and 'movshare' not in url and 'firedrive' not in url and 'putlocker' not in url and 'sockshare' not in url:
                                PLAY_movie_url(url,fonte_id,iconimage,'',fanart,'CINEMATUGA.NET')
                except: pass

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def FTT_links(name,url,iconimage,fanart):
        iconimage = iconimage
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]
        nomeescolha = name
        colecao = 'nao'
        conta_id_video = 0
        try:
                fonte_video = abrir_url(url)
        except: fonte_video = ''
        fontes_video = re.findall("<div class='post-body entry-content'>(.*?)<div style='clear: both;'>", fonte_video, re.DOTALL)
        numero_de_fontes = len(fontes_video)
        if 'BREVEMENTE ONLINE' in fonte_video: addDir1('[COLOR blue]BREVEMENTE ONLINE[/COLOR]','url',1004,artfolder,False,'')
        for fonte_e_url in fontes_video:
                if imdbcode == '':
                        imdb = re.compile('imdb.com/title/(.+?)/').findall(fonte_e_url)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                #if 'BREVEMENTE ONLINE' in fontes_video: addDir1('[COLOR blue]BREVEMENTE ONLINE[/COLOR]','url',1004,artfolder,False,'')
                match1 = re.compile('<script src="(.+?)" type="text/javascript"></script>').findall(fonte_e_url)
                for fonte_id in match1: 
                        if 'videomega' in fonte_id:
                                try:  
                                        if 'hashkey' in fonte_id:
                                                conta_id_video = conta_id_video + 1
                                                try:
                                                        urlvideomega = abrir_url(fonte_id)
                                                except: urlvideomega = ''
                                                if urlvideomega != '':
                                                        urlvidlink = re.compile('ref="(.+?)"').findall(urlvideomega)
                                                        if urlvidlink: url = 'http://videomega.tv/iframe.php?ref=' + urlvidlink[0] + '///' + name
                                                        fonte_serv = '(Videomega)'
                                                        PLAY_movie_url(url,fonte_serv,iconimage,'',fanart,'FOITATUGA')
                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                        if 'iframe.js' in fonte_id:
                                                conta_id_video = conta_id_video + 1
                                                refvideo = re.compile('<script type="text/javascript">ref="(.+?)".+?</script>').findall(fonte_e_url)
                                                if not refvideo: refvideo = re.compile(">ref='(.+?)'.+?</script>").findall(fonte_e_url)
                                                url = 'http://videomega.tv/iframe.php?ref=' + refvideo[0] + '///' + name
                                                fonte_serv = '(Videomega)'
                                                PLAY_movie_url(url,fonte_serv,iconimage,'',fanart,'FOITATUGA')
                                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                match2 = re.compile('<iframe.+?src="(.+?)".+?></iframe>').findall(fonte_e_url)
                for fonte_id in match2:
                        if 'videomega' in fonte_id:
                                try:
                                        conta_id_video = conta_id_video + 1
                                        url = fonte_id + '///' + name
                                        fonte_serv = '(Videomega)'
                                        PLAY_movie_url(url,fonte_serv,iconimage,'',fanart,'FOITATUGA')
                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                        elif 'dropvideo' in fonte_id:
                                try:
                                        conta_id_video = conta_id_video + 1
                                        url = fonte_id + '///' + name
                                        fonte_serv = '(Dropvideo)'
                                        PLAY_movie_url(url,fonte_serv,iconimage,'',fanart,'FOITATUGA')
                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Dropvideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                        elif 'vidto.me' in fonte_id:
                                try:
                                        conta_id_video = conta_id_video + 1
                                        fonte_id = fonte_id.replace('embed-','')
                                        refvideo = re.compile('http://vidto.me/embed-(.+?).html').findall(fonte_id)
                                        if refvideo: url = 'http://vidto.me/' + refvideo[0] + '.html' + '///' + name
                                        else: url = fonte_id + '///' + name
                                        #addDir('SITESdosPORTUGAS | FOITATUGA | VIDTO.ME',url,30,iconimage,'',fanart)
                                        resultados.append('SITESdosPORTUGAS | FOITATUGA | VIDTO.ME'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                                except:pass
                        else:
                                conta_id_video = conta_id_video + 1
                                FTT_resolve_not_videomega_filmes(fonte_id,nomeescolha,conta_id_video,fanart,iconimage)


def FTT_resolve_not_videomega_filmes(url,nomeescolha,conta_id_video,fanart,iconimage):
        url = url + '///' + nomeescolha
        if "videomega" in url:
		try:
                        fonte_id = '(Videomega)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
        if "vidto.me" in url:
		try:
                        match = re.compile('http://vidto.me/embed-(.+?).html').findall(url)
			if match:
				id_video = match[0]
				url = 'http://vidto.me/' + id_video + '.html'# + '///' + nomeescolha
			fonte_id = '(Vidto.me)'
			#resultados.append('SITESdosPORTUGAS | FOITATUGA | VIDTO.ME',url,30,iconimage,'',fanart)
			resultados.append('SITESdosPORTUGAS | FOITATUGA | VIDTO.ME'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)

		except: pass
	if "thevideo.me" in url:
		try:
                        fonte_id = '(TheVideo.me)'
			#addDir('SITESdosPORTUGAS | FOITATUGA | THEVIDEO.ME',url,30,iconimage,'',fanart)
		except:pass
        if "dropvideo" in url:
		try:
                        url = url.replace('/video/','/embed/')
                        fonte_id = '(DropVideo)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "vidzi.tv" in url:
                try:
                        fonte_id = '(Vidzi.tv)'
			#addDir('SITESdosPORTUGAS | FOITATUGA | VIDZI.TV',url,30,iconimage,'',fanart)
                except:pass
        if "vodlocker" in url:
		try:
                        fonte_id = '(Vodlocker)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vodlocker)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "played.to" in url:
                try:
                        fonte_id = '(Played.to)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Played.to)[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "cloudzilla" in url:
                try:
                        fonte_id = '(Cloudzilla)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Cloudzilla)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "divxstage" in url:
                try:
                        fonte_id = '(Divxstage)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Divxstage)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "vidzen" in url:
                try:
                        fonte_id = '(Vidzen)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidzen)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
	if "streamin.to" in url:
                try:
                        fonte_id = '(Streamin)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass                        
    	if "nowvideo" in url:
                try:
                        fonte_id = '(Nowvideo)'
                        #addDir('SITESdosPORTUGAS | FOITATUGA | NOWVIDEO',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | FOITATUGA | NOWVIDEO'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
    		except:pass
    	if "primeshare" in url:
                try:
                        fonte_id = '(Primeshare)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Primeshare.tv)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videoslasher" in url:
                try:
                        fonte_id = '(VideoSlasher)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoSlasher)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "sockshare" in url:
                try:
                        fonte_id = '(Sockshare)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Sockshare)[/COLOR][/B]',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | FOITATUGA | SOCKSHARE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
    		except:pass
    	if "putlocker" in url:
                try:
                        url = url.replace('putlocker.com/embed/','firedrive.com/file/')
                        fonte_id = '(Firedrive)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | FOITATUGA | PUTLOCKER'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
    		except:pass
    	else:
                if "firedrive" in url:
                        try:
                                fonte_id = '(Firedrive)'
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                resultados.append('SITESdosPORTUGAS | FOITATUGA | FIREDRIVE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
                        except:pass
    	if "movshare" in url:
                try:
                        fonte_id = '(Movshare)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Movshare)[/COLOR][/B]',url,30,iconimage,'',fanart)
                        resultados.append('SITESdosPORTUGAS | FOITATUGA | MOVSHARE'+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
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
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Video.tt)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(VideoWood)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoWood)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	#if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url and 'nowvideo' not in url:# and 'iiiiiiiiii' in url:
    	if  'vidto.me' not in url and 'nowvideo' not in url and 'movshare' not in url and 'firedrive' not in url and 'putlocker' not in url and 'sockshare' not in url:
                PLAY_movie_url(url,fonte_id,iconimage,'',fanart,'FOITATUGA')
    	return



#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def PLAY_movie_url(url,name,iconimage,checker,fanart,nomeAddon):
        url = url.replace('////','///')
        nomefonte = re.compile('[(](.+?)[)]').findall(name)
        if nomefonte: name = nomefonte[0].replace('(','').replace(')','')
        try:
                import urlresolver
        except: pass
        #if 'vk.com' not in url and 'video.mail.ru' not in url:
                #dp = xbmcgui.DialogProgress()
                #dp.create(name,'A sincronizar vídeos e legendas')
                #dp.update(0)
        if '///' in url:
                if '////' in url: nome = re.compile('////(.+?)[)].+?[(].+?[)]').findall(url)
                else: nome = re.compile('///(.+?)[)].+?[(].+?[)]').findall(url)
                if not nome:
                        nome = re.compile('///(.*)').findall(url)
                        if nome: nomefilme = nome[0]
                else: nomefilme = nome[0] + ')'
                urlvid = re.compile('(.+?)///').findall(url)
                if urlvid: url = urlvid[0]
                #if nomefilme.replace(' ','') != name.replace(' ',''):
                #name = nomefilme + ' ' + name
        #addLink(url,'','','')
        checker = ''
        iframe_url = url
	if "clipstube" in url :
		try:
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			match=re.compile("var hq_video_file = '(.+?)'").findall(link3)
			if not match: match=re.compile("var normal_video_file = '(.+?)'").findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
				checker = ''
				url = match[0]
			else:
				checker = subtitle[0]
				url = match[0]
		except: pass
		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

	if "drive.google" in url or "docs.google" in url :
		try:
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			match=re.compile('"fmt_stream_map":".+?[|](.+?)[,]').findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
				checker = ''
				url = match[0].replace('\u0026','&').replace('\u003d','=')
			else:
				checker = subtitle[0]
				url = match[0].replace('\u0026','&').replace('\u003d','=')
		except: pass
		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

        if "streamin" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

	if "thevideo.me" in url:
		try:
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			if link3:
                                mp4 = re.compile('[|]logo[|]100[|](.+?)[|]label[|]').findall(link3)
                                if mp4: mp4 = mp4[0]
                                else: mp4='111'
			else: mp4 = '--'
			imagem = re.compile('<span id=.+?><img src="(.+?)"').findall(link3)
			if imagem:
                                iconimage = imagem[0]
                                ip = re.compile('(.+?)/i/').findall(iconimage)
                                if ip: ip = ip[0]
			todassources = re.compile('[|]sharing(.+?)sources[|]').findall(link3)
			sourc = re.compile('.+?[|](.+?)0p[|]').findall(todassources[0])
			#addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,iconimage,False,fanart)
			i = 1
			a = 0
			if len(sourc) == 5:
                                sources = re.compile('[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|]').findall(todassources[0])
                                for x in range(5):
                                        url = ip + '/' + sources[0][a] + '/v.' + mp4
                                        a = a + 2                                        
                                        #addLink(sources[0][i]+' | '+name,url,iconimage,fanart)
                                        resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+' | '+sources[0][i]+'0p|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)
                                        i = a + 1
                        if len(sourc) == 4:
                                sources = re.compile('[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|]').findall(todassources[0])
                                for x in range(4):
                                        url = ip + '/' + sources[0][a] + '/v.' + mp4
                                        a = a + 2                                        
                                        #addLink(sources[0][i]+' | '+name,url,iconimage,fanart)
                                        resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+' | '+sources[0][i]+'0p|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)
                                        i = a + 1
			if len(sourc) == 3:
                                sources = re.compile('[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|]').findall(todassources[0])
                                for x in range(3):
                                        url = ip + '/' + sources[0][a] + '/v.' + mp4
                                        a = a + 2                                        
                                        #addLink(sources[0][i]+' | '+name,url,iconimage,fanart)
                                        resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+' | '+sources[0][i]+'0p|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)
                                        i = a + 1
			if len(sourc) == 2:
                                sources = re.compile('[|](.+?)[|](.+?)0p[|](.+?)[|](.+?)0p[|]').findall(todassources[0])
                                for x in range(2):
                                        url = ip + '/' + sources[0][a] + '/v.' + mp4
                                        a = a + 2                                        
                                        #addLink(sources[0][i]+' | '+name,url,iconimage,fanart)
                                        resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+' | '+sources[0][i]+'0p|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)
                                        i = a + 1
                        if len(sourc) == 1:
                                sources = re.compile('[|]mp4[|](.+?)[|](.+?)0p[|]').findall(todassources[0])
                                url = ip + '/' + sources[0][0] + '/v.' + mp4
                                #addLink(sources[0][1]+' | '+name,url,iconimage,fanart)
                                resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+' | '+sources[0][1]+'0p|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

		except: pass
	if "vidzi.tv" in url:       
		try:
                        if 'embed-' in iframe_url:
                                iframe_url = url.replace('vidzi.tv/embed-','vidzi.tv/')
                                tiraurl = re.compile('(.+?)-').findall(iframe_url)
                                if tiraurl: iframe_url = tiraurl[0]+'.html'
                        print iframe_url
                        link3 = abrir_url(iframe_url)
                        match=re.compile('file: "(.+?)"').findall(link3)
                        subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
                        imagem = re.compile('image: "(.+?)"').findall(link3)
                        if imagem: iconimage = imagem[0]
                        #addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,iconimage,False,fanart)
                        for link in match:
                                if '.srt' in link: checker = link
                                if '.m3u8' in link:
                                        url = link
                                        resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+' | M3U8|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)
                                        #addLink('m3u8 | '+name,url,iconimage,fanart)
                                if '.mp4' in link:
                                        url = link
                                        resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+' | MP4|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)
                                        #addLink('mp4 | '+name,url,iconimage,fanart)
                                
                except: pass                
	if "vidzen" in url:
		try:
                        #iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
                                checker = ''
			else:
				checker = subtitle[0]
			match=re.compile('streamer: "(.+?)"').findall(link3)
			if not match:
                                match=re.compile('file: "(.+?)"').findall(link3)
                                if match: url = match[0]
                        else: url = match[0]
			if not match:
                                match=re.compile('var[|]type[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|][|](.+?)[|].+?provider[|](.+?)[|](.+?)[|]file').findall(link3)
                                if match: url = 'http://'+match[0][4]+'.'+match[0][3]+'.'+match[0][2]+'.'+match[0][1]+':'+match[0][0]+'/'+match[0][6]+'/v.'+match[0][5]#+'?start=0'
			imagem=re.compile('[[]IMG[]](.+?)[[]/IMG[]]').findall(link3)
			if imagem: iconimage = imagem[0]
			#addLink(url,url,iconimage,fanart)
		except: pass
		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

	if "playfreehd" in url:
		try:
			if 'embed' in iframe_url:
                                print iframe_url
                                link3 = abrir_url(iframe_url)
                                imagem = re.compile("var preview_img = '(.+?)';").findall(link3)
                                if imagem: iconimage = imagem[0]
                                match=re.compile("var hq_video_file = '(.+?)';").findall(link3)
                                if match:
                                        url = match[0]+'?start=0'
                                        if '.flv' in url: flv = '.flv | '
                                        else: flv = ''
                                        #addLink('HQ | '+flv+name,url,iconimage,fanart)
                                        resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+' | HD|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)
                                match=re.compile("var normal_video_file = '(.+?)';").findall(link3)
                                if match:
                                        url = match[0]+'?start=0'
                                        if '.flv' in url: flv = '.flv | '
                                        else: flv = ''
                                        addLink('SD | '+flv+name,url,iconimage,fanart)
                                        resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+' | SD|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)
                        if 'embed' not in iframe_url:
                                print iframe_url
                                link3 = abrir_url(iframe_url)
                                link = re.compile('<param name="FlashVars" value="plugins=plugins/proxy.swf&proxy.link=http://filehoot.com/(.+?).html;captions.file').findall(link3)
                                if link:
                                        link = 'http://filehoot.com/embed-'+link[0]+'-640x360.html'
                                        link3 = abrir_url(link)
                                imagem = re.compile('image: "(.+?)"').findall(link3)
                                if imagem: iconimage = imagem[0]
                                match=re.compile('file: "(.+?)"').findall(link3)
                                if match:
                                        resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+match[0]+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)
                                        url = match[0]
                                        iframe_url = url
		except: pass
	if "divxstage" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
    			#return url
		except: pass
		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

	if "vidbull" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
    			#addLink(match[0],match[0],'')
    			#return url
		except: pass
		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

	if "vodlocker" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
    			#return url
    		except: pass
    		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

	if "played.to" in url:
                #addLink('sim1','','')
		try:
                        #addLink('sim','','')
                        #iframe_url = url
                        print iframe_url
                        link3 = abrir_url(iframe_url)
                        imagem = re.compile('image: "(.+?)"').findall(link3)
			if imagem: iconimage = imagem[0]
                        tit=re.compile('var vtitle = "(.+?)"').findall(link3)
                        match=re.compile('file: "(.+?)"').findall(link3)
                        subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
                        if subtitle == []:
                                checker = ''
                                if match: url = match[0]
                        else:
                                if checker: checker = subtitle[0]
                                if match: url = match[0]
                except: pass
                resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

	if "cloudzilla" in url:
		try:
			#iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			imagem = re.compile('var vthumbnail = "(.+?)"').findall(link3)
			if imagem: iconimage = imagem[0]
			tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			match=re.compile('var vurl = "(.+?)"').findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
				checker = ''
				if match: url = match[0]
			else:
				if checker: checker = subtitle[0]
				if match: url = match[0]
			#addLink(match[0],match[0],'')
			#return
		except: pass
		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

	if "vodlocker" in url:
		try:
                        #if '/video/' in url: url = url.replace('/video/','/embed/')
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			match=re.compile('file: "(.+?)"').findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
				checker = ''
				url = match[0]
			else:
				checker = subtitle[0]
				url = match[0]
			#addLink(name+match[0],match[0],'')
		except: pass
		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)	

	if "vk.com" in url:
		try:
                        #if '/video/' in url: url = url.replace('/video/','/embed/')
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			#addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,artfolder,False,fanart)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
                        match=re.compile('var vars = {.+?"url240":"(.+?)"').findall(link3)
			if match:
                                #addLink('240p | '+name,match[0].replace('\/','/'),iconimage,fanart)
                                resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+' | 240p|URL|'+match[0]+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)
			match=re.compile('var vars = {.+?"url360":"(.+?)"').findall(link3)
			if match:
                                #addLink('360p | '+name,match[0].replace('\/','/'),iconimage,fanart)
                                resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+' | 360p|URL|'+match[0]+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)
			match=re.compile('var vars = {.+?"url480":"(.+?)"').findall(link3)
			if match:
                                #addLink('480p | '+name,match[0].replace('\/','/'),iconimage,fanart)
                                resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+' | 480p|URL|'+match[0]+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)
			match=re.compile('var vars = {.+?"url720":"(.+?)"').findall(link3)
			if match:
                                #addLink('720p | '+name,match[0].replace('\/','/'),iconimage,fanart)
                                resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+' | 720p|URL|'+match[0]+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)
			match=re.compile('var vars = {.+?"url1080":"(.+?)"').findall(link3)
			if match:
                                #addLink('1080p | '+name,match[0].replace('\/','/'),iconimage,fanart)
                                resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+' | 1080p|URL|'+match[0]+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)
		except: pass
        if "streamcloud" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

	if "filehoot" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

	if "video.mail.ru" in url or 'videoapi.my.mail' in url:
                #addLink(url,'','')
		try:
			iframe_url = url###http://api.video.mail.ru/videos/mail/megafilmeshdtv/_myvideo/874.json
			print iframe_url
			#addLink(iframe_url,'','')
			#addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,artfolder,False,fanart)
			iframe_url = iframe_url.replace('/embed','').replace('.html','.json')
                        try:
                                link3 = abrir_url(iframe_url)
                        except: link3 = ''
                        if link3 != '':
                                imagem = re.compile('"poster":"(.+?)"').findall(link3)
                                if imagem: iconimage = imagem[0]
                                match = re.compile('"key":"(.+?)","url":"(.+?)"').findall(link3)
                                for res,link in match:
                                        #addLink(res+' | '+name,link,iconimage,fanart)
                                        resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+' | '+res+'|URL|'+link+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)
                        else:
                                try:
                                        link3 = abrir_url(iframe_url)
                                except: link3 = ''
                                tit=re.compile('<title>(.+?)</title>').findall(link3)
                                if link3 != '':
                                        if 'sd' in link3 and 'md' in link3:
                                                match=re.compile('videoPresets = {"sd":"(.+?)","md":"(.+?)"}').findall(link3)
                                                if not match:
                                                        match=re.compile('"videos":{"sd":"(.+?)&expire_at=.+?","hd":"(.+?)&expire_at=.+?"}').findall(link3)
                                                        if not match: match=re.compile('"url":"(.+?)"').findall(link3)
                                                if match:
                                                        resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+' | SD|URL|'+match[0][0]+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)
                                                        resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+' | HD|URL|'+match[0][1]+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)
                                                        #addLink('SD | '+name,match[0][0],iconimage,fanart)
                                                        #addLink('HD | '+name,match[0][1],iconimage,fanart)
                                        elif 'sd' in link3 and 'md' not in link3:
                                                match=re.compile('videoPresets = {"sd":"(.+?)"').findall(link3)
                                                if match:
                                                        resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+' | SD|URL|'+match[0]+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)
                                                        #addLink('SD | '+name,match[0],iconimage,fanart)
                                        elif 'hd' in link3 and 'md' not in link3:
                                                match=re.compile('"md":"(.+?)"}').findall(link3)
                                                if match:
                                                        resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+' | HD|URL|'+match[0]+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)
                                                        #addLink('HD | '+name,match[0],iconimage,fanart)                            
		except: pass
	if "flashx" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

        if "youtu" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

	if "youwatch" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

	if "hostingbulk" in url:
		try:
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			#tit=re.compile('title: "(.+?)"').findall(link3)
			match=re.compile('http[|]player[|]type[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|]com[|]hostingbulk[|]provider[|](.+?)[|]video[|](.+?)[|][|]file[|]').findall(link3)
			#subtitle=re.compile("addSubtitles('(.+?)', '', false)").findall(link3)
			#subtitle = []
			url = 'http://'+match[0][3]+'.'+match[0][2]+'.'+match[0][1]+'.'+match[0][0]+'/d/'+match[0][5]+'/video.'+match[0][4]+'?start=0'
			#if subtitle == []:
				#checker = ''
				#url = match[0]
			#else:
				#checker = subtitle[0]
				#url = match[0]
		except: pass
		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

        if "vidto.me" in url:
		try:
##                        iframe_url = url
##			print iframe_url
##			addLink(url,'','','')
##                        link3=abrir_url(iframe_url)
##                        jsU = JsUnpackerV2()
##                        link3 = jsU.unpackAll(link3)
##                        url=re.compile('file:"(.+?)"').findall(link3)[-1]
##                        addLink(url,'','','')
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
    			#addLink(url,'','','')
    			#checker = url.replace('.avi','.srt')
		except: pass
		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

	if "dropvideo" in url:
		try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			imagem = re.compile('var vscreenshot = "(.+?)"').findall(link3)
			if imagem: iconimage = imagem[0]
			tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			match=re.compile('var vurl2 = "(.+?)"').findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
				checker = ''
				url = match[0]
			else:
				checker = subtitle[0]
				url = match[0]
			#addLink(name+match[0],match[0],'')
		except: pass
		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

	if "putlocker" in url:
                try:
                        url = url.replace('putlocker.com/embed/','firedrive.com/file/')
                        #sources = []
                        #hosted_media = urlresolver.HostedMediaFile(url)
                        #sources.append(hosted_media)
                        #source = urlresolver.choose_source(sources)
                        #if source: 
                                #url = source.resolve()
                        #else: url = ''
                        #addLink(url,url,'')
    		except:pass
    		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

    	if "nowvideo" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

    	if "primeshare" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

    	if "allmyvideos" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

    	if "vkontakte" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

    	if "videoslasher" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

    	if "sockshare" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

    	if "firedrive" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
                        #addLink(url,url,'')
    		except:pass
    		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

    	if "videowood" in url:
                try:
                        iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			tit=re.compile('title: "(.+?)"').findall(link3)
			match=re.compile('file: "(.+?)"').findall(link3)
			subtitle=re.compile("addSubtitles[(]'(.+?)'").findall(link3)
			if match:
                                #addLink(tit[0]+match[0],match[0],'')
                                if subtitle == []:
                                        checker = ''
                                        url = match[0].replace('\/','/')
                                else:
                                        checker = subtitle[0]
                                        url = match[0].replace('\/','/')
                        else:
                                iframe_url = url.replace('/embed/','/video-link/')
                                link3 = abrir_url(iframe_url)
                                if link3 != []:
                                        match=re.compile('"url":"(.+?)"}').findall(link3)
                                        if subtitle == []:
                                                checker = ''
                                                url = match[0].replace('\/','/')
                                        else:
                                                checker = subtitle[0]
                                                url = match[0].replace('\/','/')
			#addLink(name+match[0],match[0],'')
    		except:pass
    		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

    	if "movshare" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

    	if "video.tt" in url or "videott" in url:
                try:
                        iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			id_video = re.compile('http://video.tt/player_control/settings.php?v=(.+?)&fv=v1.2.74').findall(url)
			if not id_video: id_video = re.compile('"vcode":"(.+?)"').findall(link3)
			v_key=re.compile('"time":"(.+?)"}').findall(link3)
			tit=re.compile('Title=(.+?)&SourceURL=').findall(link3)
			tt=re.compile('"st":(.+?),"tst"').findall(link3)
			vlink='http://gs.video.tt/s?v='+id_video[0]+'&r=1&t='+tt[0]+'&u=&c='+v_key[0]+'&start=0'
			subtitle=re.compile("addSubtitles[(]'(.+?)'").findall(link3)
			#subtitle = []
			if subtitle == []:
				checker = ''
				url = vlink
			else:
				checker = subtitle[0]
				url = vlink
			#addLink('Ver Filme',url,'')
                        #addLink(id_video[0],vlink,'')
                        #addLink(tt[0],vlink,'')
                        #addLink(v_key[0],vlink,'')
                        #addLink(vlink,vlink,'')
			#addLink(url,'','')
    		except:pass
    		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

    	if "videomega" in url:
		try:
                        if "iframe" not in url:
                                id_videomega = re.compile('ref=(.*)').findall(url)[0]
                                iframe_url = 'http://videomega.tv/iframe.php?ref=' + id_videomega
                        else: iframe_url = url
                        print iframe_url
                        link3 = abrir_url(iframe_url)
                        match=re.compile('document.write\(unescape\("(.+?)"\)').findall(link3)
                        print match
                        tit=re.compile('<div id="title">&nbsp;&nbsp;&nbsp;(.+?)</div>').findall(link3)
                        video_url_escape = urllib.unquote(match[0])
                        match=re.compile('file: "(.+?)"').findall(video_url_escape)
                        subtitle=re.compile('"file": "(.+?)"').findall(video_url_escape)
                        if subtitle==[]:
                                subtitle=re.compile('[[][{]file: "(.+?)"').findall(video_url_escape)      
                        if subtitle == []:
                                checker = ''
                                url = match[0]
                        else:
                                checker = subtitle[0].replace('http://videomega.tv/servesrt.php?s=','')
                                url = match[0]
                        #addLink(checker,match[0],'')
		except: pass
		resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart+'|SUBTITLES|'+checker)

        #addLink(url,url,'','')
##        if 'vk.com' not in iframe_url and 'video.mail.ru' not in iframe_url and 'videoapi.my.mail' not in iframe_url and 'vidzi.tv' not in iframe_url and 'playfreehd' not in iframe_url  and 'thevideo.me' not in iframe_url:# and 'iiiiiiiiii' in url:
##                try:
##                        nomefonte = re.compile('[(](.+?)[)]').findall(name)
##                        if nomefonte: name = nomefonte[0].replace('(','').replace(')','')
##                        #name = string.uppercase(name)
##                        #addLink('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper(),url,iconimage,fanart)
##                        resultados.append('SITESdosPORTUGAS | '+nomeAddon+' | '+name.upper()+'|URL|'+url+'|THUMB|'+iconimage+'|FANART|'+fanart)
##                except: pass
        return

class MyPlayer1(xbmc.Player):
        
        def __init__( self, *args, **kwargs ):
                xbmc.Player.__init__( self )
                self.nomefilme = kwargs[ "nomefilme" ]
                self.checkerSubs = kwargs[ "checker" ]
                self.Playable = 'Nao'

        def PlayStream(self, playlist):
                self.play(playlist)
                progress.close()
                if self.checkerSubs == '' or self.checkerSubs == None: pass
                else: self.setSubtitles(self.checkerSubs)
                if not self.isPlaying() and self.Playable == 'Nao':
                        xbmcgui.Dialog().ok('SITES dos PORTUGAS', 'Este stream está offline.', 'Tente outro stream.')
                while self.isPlaying():
                        xbmc.sleep(1000)

        def onPlayBackStarted(self):
                self.Playable = 'Sim'
                progress.close()
                            
        def onPlayBackEnded(self):
                self.Playable = 'Nao'
                progress.close()

        def onPlayBackStopped(self):
                self.Playable = 'Nao'
                progress.close()

def PLAY_movie(url,name,iconimage,checker,fanart):#,nomeAddon):
        nomeAddon = ''
        progress.create(name, 'A preparar vídeo.')
        progress.update( 98, "", 'Por favor aguarde...', "" )
        
        #addLink(url,'','')
        url = url.replace('////','///')
        try:
                import urlresolver
        except: pass
        #if 'vk.com' not in url and 'video.mail.ru' not in url:
                #dp = xbmcgui.DialogProgress()
                #dp.create(name,'A sincronizar vídeos e legendas')
                #dp.update(0)
        if '///' in url:
                if '////' in url: nome = re.compile('////(.+?)[)].+?[(].+?[)]').findall(url)
                else: nome = re.compile('///(.+?)[)].+?[(].+?[)]').findall(url)
                if not nome:
                        nome = re.compile('///(.*)').findall(url)
                        if nome: nomefilme = nome[0]
                else: nomefilme = nome[0] + ')'
                urlvid = re.compile('(.+?)///').findall(url)
                if urlvid: url = urlvid[0]
                #if nomefilme.replace(' ','') != name.replace(' ',''):
                name = nomefilme + ' ' + name
        iframe_url = url
	if "clipstube" in url :
		try:
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			match=re.compile("var hq_video_file = '(.+?)'").findall(link3)
			if not match: match=re.compile("var normal_video_file = '(.+?)'").findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
				checker = ''
				url = match[0]
			else:
				checker = subtitle[0]
				url = match[0]
		except: pass
	elif "drive.google" in url or "docs.google" in url :
		try:
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			match=re.compile('"fmt_stream_map":".+?[|](.+?)[,]').findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
				checker = ''
				url = match[0].replace('\u0026','&').replace('\u003d','=')
			else:
				checker = subtitle[0]
				url = match[0].replace('\u0026','&').replace('\u003d','=')
		except: pass
        elif "streamin" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	elif "thevideo.me" in url:
		try:
                        _nomeservidor_ = []
                        _linkservidor_ = []
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			if link3:
                                mp4 = re.compile('[|]logo[|]100[|](.+?)[|]label[|]').findall(link3)
                                if mp4: mp4 = mp4[0]
                                else: mp4='111'
			else: mp4 = '--'
			imagem = re.compile('<span id=.+?><img src="(.+?)"').findall(link3)
			if imagem:
                                iconimage = imagem[0]
                                ip = re.compile('(.+?)/i/').findall(iconimage)
                                if ip: ip = ip[0]
			todassources = re.compile('[|]sharing(.+?)sources[|]').findall(link3)
			sourc = re.compile('.+?[|](.+?)0p[|]').findall(todassources[0])
			addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,iconimage,False,fanart)
			i = 1
			a = 0
			if len(sourc) == 5:
                                sources = re.compile('[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|]').findall(todassources[0])
                                for x in range(5):
                                        url = ip + '/' + sources[0][a] + '/v.' + mp4
                                        _linkservidor_.append(url)
                                        a = a + 2
                                        _nomeservidor_.append(sources[0][i]+' | '+name)
                                        addLink(sources[0][i]+' | '+name,url,iconimage,fanart)
                                        i = a + 1
        
                        if len(sourc) == 4:
                                sources = re.compile('[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|]').findall(todassources[0])
                                for x in range(4):
                                        url = ip + '/' + sources[0][a] + '/v.' + mp4
                                        _linkservidor_.append(url)
                                        a = a + 2
                                        _nomeservidor_.append(sources[0][i]+' | '+name)
                                        addLink(sources[0][i]+' | '+name,url,iconimage,fanart)
                                        i = a + 1
        
			if len(sourc) == 3:
                                sources = re.compile('[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|]').findall(todassources[0])
                                for x in range(3):
                                        url = ip + '/' + sources[0][a] + '/v.' + mp4
                                        _linkservidor_.append(url)
                                        a = a + 2
                                        _nomeservidor_.append(sources[0][i]+' | '+name)
                                        addLink(sources[0][i]+' | '+name,url,iconimage,fanart)
                                        i = a + 1
 
			if len(sourc) == 2:
                                sources = re.compile('[|](.+?)[|](.+?)p[|](.+?)[|](.+?)p[|]').findall(todassources[0])
                                for x in range(2):
                                        url = ip + '/' + sources[0][a] + '/v.' + mp4
                                        _linkservidor_.append(url)
                                        a = a + 2
                                        _nomeservidor_.append(sources[0][i]+' | '+name)
                                        addLink(sources[0][i]+' | '+name,url,iconimage,fanart)
                                        i = a + 1
                                           
                        if len(sourc) == 1:
                                sources = re.compile('[|](.+?)[|](.+?)p[|]').findall(todassources[0])
                                url = ip + '/' + sources[0][0] + '/v.' + mp4
                                addLink(sources[0][1]+' | '+name,url,iconimage,fanart)
                                nm = sources[0][1]+' | '+name
                                _nomeservidor_.append(nm)
                                _linkservidor_.append(url)
          
		except: pass
##		progress.close()
##                index = xbmcgui.Dialog().select('Escolha o Stream', _nomeservidor_)
##                if index > -1:
##                        playlist = xbmc.PlayList(1)
##                        playlist.clear()             
##                        playlist.add(_linkservidor_[index],xbmcgui.ListItem(name, thumbnailImage=str(iconimage)))
##                        MyPlayer(nome_addon=nome_addon,checker=checker).PlayStream(playlist)
##                        #PLAY_movie(_linkservidor_[index],_nomeservidor_[index],iconimage,'',fanart)
                        
	elif "vidzi.tv" in url:       
		try:
                        if 'embed-' in iframe_url:
                                iframe_url = url.replace('vidzi.tv/embed-','vidzi.tv/')
                                tiraurl = re.compile('(.+?)-').findall(iframe_url)
                                if tiraurl: iframe_url = tiraurl[0]+'.html'
                        print iframe_url
                        link3 = abrir_url(iframe_url)
                        match=re.compile('file: "(.+?)"').findall(link3)
                        subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
                        imagem = re.compile('image: "(.+?)"').findall(link3)
                        if imagem: iconimage = imagem[0]
                        addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,iconimage,False,fanart)
                        for link in match:
                                if '.m3u8' in link:
                                        url = link
                                        addLink('m3u8 | '+name,url,iconimage,fanart)
                                if '.mp4' in link:
                                        url = link
                                        addLink('mp4 | '+name,url,iconimage,fanart)
                                if '.srt' in link: checker = link
                except: pass                
	elif "vidzen" in url:
		try:
                        #iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
                                checker = ''
			else:
				checker = subtitle[0]
			match=re.compile('streamer: "(.+?)"').findall(link3)
			if not match:
                                match=re.compile('file: "(.+?)"').findall(link3)
                                if match: url = match[0]
                        else: url = match[0]
			if not match:
                                match=re.compile('var[|]type[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|][|](.+?)[|].+?provider[|](.+?)[|](.+?)[|]file').findall(link3)
                                if match: url = 'http://'+match[0][4]+'.'+match[0][3]+'.'+match[0][2]+'.'+match[0][1]+':'+match[0][0]+'/'+match[0][6]+'/v.'+match[0][5]#+'?start=0'
			imagem=re.compile('[[]IMG[]](.+?)[[]/IMG[]]').findall(link3)
			if imagem: iconimage = imagem[0]
			#addLink(url,url,iconimage,fanart)
		except: pass
	elif "playfreehd" in url:
		try:
			if 'embed' in iframe_url:
                                print iframe_url
                                link3 = abrir_url(iframe_url)
                                imagem = re.compile("var preview_img = '(.+?)';").findall(link3)
                                if imagem: iconimage = imagem[0]
                                match=re.compile("var hq_video_file = '(.+?)';").findall(link3)
                                if match:
                                        url = match[0]+'?start=0'
                                        if '.flv' in url: flv = '.flv | '
                                        else: flv = ''
                                        addLink('HQ | '+flv+name,url,iconimage,fanart)
                                match=re.compile("var normal_video_file = '(.+?)';").findall(link3)
                                if match:
                                        url = match[0]+'?start=0'
                                        if '.flv' in url: flv = '.flv | '
                                        else: flv = ''
                                        addLink('SD | '+flv+name,url,iconimage,fanart)
                        if 'embed' not in iframe_url:
                                print iframe_url
                                link3 = abrir_url(iframe_url)
                                link = re.compile('<param name="FlashVars" value="plugins=plugins/proxy.swf&proxy.link=http://filehoot.com/(.+?).html;captions.file').findall(link3)
                                if link:
                                        link = 'http://filehoot.com/embed-'+link[0]+'-640x360.html'
                                        link3 = abrir_url(link)
                                imagem = re.compile('image: "(.+?)"').findall(link3)
                                if imagem: iconimage = imagem[0]
                                match=re.compile('file: "(.+?)"').findall(link3)
                                if match:
                                        
                                        url = match[0]
                                        iframe_url = url
		except: pass
	elif "divxstage" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
    			#return url
		except: pass
	elif "vidbull" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
    			#addLink(match[0],match[0],'')
    			#return url
		except: pass
	elif "vodlocker" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
    			#return url
		except: pass
	elif "played.to" in url:
                #addLink('sim1','','')
		try:
                        #addLink('sim','','')
                        #iframe_url = url
                        print iframe_url
                        link3 = abrir_url(iframe_url)
                        imagem = re.compile('image: "(.+?)"').findall(link3)
			if imagem: iconimage = imagem[0]
                        tit=re.compile('var vtitle = "(.+?)"').findall(link3)
                        match=re.compile('file: "(.+?)"').findall(link3)
                        subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
                        if subtitle == []:
                                checker = ''
                                if match: url = match[0]
                        else:
                                if checker: checker = subtitle[0]
                                if match: url = match[0]
                except: pass
	elif "cloudzilla" in url:
		try:
			#iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			imagem = re.compile('var vthumbnail = "(.+?)"').findall(link3)
			if imagem: iconimage = imagem[0]
			tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			match=re.compile('var vurl = "(.+?)"').findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
				checker = ''
				if match: url = match[0]
			else:
				if checker: checker = subtitle[0]
				if match: url = match[0]
			#addLink(match[0],match[0],'')
			#return
		except: pass
	elif "vodlocker" in url:
		try:
                        #if '/video/' in url: url = url.replace('/video/','/embed/')
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			match=re.compile('file: "(.+?)"').findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
				checker = ''
				url = match[0]
			else:
				checker = subtitle[0]
				url = match[0]
			#addLink(name+match[0],match[0],'')
		except: pass
	elif "vk.com" in url:
		try:
                        #if '/video/' in url: url = url.replace('/video/','/embed/')
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,artfolder,False,fanart)
			#tit=re.compile('var vtitle = "(.+?)"').findall(link3)
                        match=re.compile('var vars = {.+?"url240":"(.+?)"').findall(link3)
			if match: addLink('240p | '+name,match[0].replace('\/','/'),iconimage,fanart)
			match=re.compile('var vars = {.+?"url360":"(.+?)"').findall(link3)
			if match: addLink('360p | '+name,match[0].replace('\/','/'),iconimage,fanart)
			match=re.compile('var vars = {.+?"url480":"(.+?)"').findall(link3)
			if match: addLink('480p | '+name,match[0].replace('\/','/'),iconimage,fanart)
			match=re.compile('var vars = {.+?"url720":"(.+?)"').findall(link3)
			if match: addLink('720p | '+name,match[0].replace('\/','/'),iconimage,fanart)
			match=re.compile('var vars = {.+?"url1080":"(.+?)"').findall(link3)
			if match: addLink('1080p | '+name,match[0].replace('\/','/'),iconimage,fanart)
		except: pass
        elif "streamcloud" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	elif "filehoot" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	elif "video.mail.ru" in url or 'videoapi.my.mail' in url:
                #addLink(url,'','')
		try:
			iframe_url = url###http://api.video.mail.ru/videos/mail/megafilmeshdtv/_myvideo/874.json
			print iframe_url
			#addLink(iframe_url,'','')
			addDir1('[COLOR orange]Escolha o stream:[/COLOR]','url',1004,artfolder,False,fanart)
			iframe_url = iframe_url.replace('/embed','').replace('.html','.json')
                        try:
                                link3 = abrir_url(iframe_url)
                        except: link3 = ''
                        if link3 != '':
                                imagem = re.compile('"poster":"(.+?)"').findall(link3)
                                if imagem: iconimage = imagem[0]
                                match = re.compile('"key":"(.+?)","url":"(.+?)"').findall(link3)
                                for res,link in match:
                                        addLink(res+' | '+name,link,iconimage,fanart)
                        else:
                                try:
                                        link3 = abrir_url(iframe_url)
                                except: link3 = ''
                                tit=re.compile('<title>(.+?)</title>').findall(link3)
                                if link3 != '':
                                        if 'sd' in link3 and 'md' in link3:
                                                match=re.compile('videoPresets = {"sd":"(.+?)","md":"(.+?)"}').findall(link3)
                                                if not match:
                                                        match=re.compile('"videos":{"sd":"(.+?)&expire_at=.+?","hd":"(.+?)&expire_at=.+?"}').findall(link3)
                                                        if not match: match=re.compile('"url":"(.+?)"').findall(link3)
                                                if match:
                                                        addLink('SD | '+name,match[0][0],iconimage,fanart)
                                                        addLink('HD | '+name,match[0][1],iconimage,fanart)
                                        elif 'sd' in link3 and 'md' not in link3:
                                                match=re.compile('videoPresets = {"sd":"(.+?)"').findall(link3)
                                                if match:
                                                        addLink('SD | '+name,match[0],iconimage,fanart)
                                        elif 'hd' in link3 and 'md' not in link3:
                                                match=re.compile('"md":"(.+?)"}').findall(link3)
                                                if match:
                                                        addLink('HD | '+name,match[0],iconimage,fanart)                            
		except: pass
	elif "flashx" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
        elif "youtu" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	elif "youwatch" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	elif "hostingbulk" in url:
		try:
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			#tit=re.compile('title: "(.+?)"').findall(link3)
			match=re.compile('http[|]player[|]type[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|]com[|]hostingbulk[|]provider[|](.+?)[|]video[|](.+?)[|][|]file[|]').findall(link3)
			#subtitle=re.compile("addSubtitles('(.+?)', '', false)").findall(link3)
			#subtitle = []
			url = 'http://'+match[0][3]+'.'+match[0][2]+'.'+match[0][1]+'.'+match[0][0]+'/d/'+match[0][5]+'/video.'+match[0][4]+'?start=0'
			#if subtitle == []:
				#checker = ''
				#url = match[0]
			#else:
				#checker = subtitle[0]
				#url = match[0]
		except: pass
        elif "vidto.me" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
    			#checker = url.replace('.avi','.srt')
		except: pass
	elif "dropvideo" in url:
		try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
			iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			imagem = re.compile('var vscreenshot = "(.+?)"').findall(link3)
			if imagem: iconimage = imagem[0]
			tit=re.compile('var vtitle = "(.+?)"').findall(link3)
			match=re.compile('var vurl2 = "(.+?)"').findall(link3)
			subtitle=re.compile('var vsubtitle = "(.+?)"').findall(link3)
			if subtitle == []:
				checker = ''
				url = match[0]
			else:
				checker = subtitle[0]
				url = match[0]
			#addLink(name+match[0],match[0],'')
		except: pass
	elif "putlocker" in url:
                try:
                        url = url.replace('putlocker.com/embed/','firedrive.com/file/')
                        #sources = []
                        #hosted_media = urlresolver.HostedMediaFile(url)
                        #sources.append(hosted_media)
                        #source = urlresolver.choose_source(sources)
                        #if source: 
                                #url = source.resolve()
                        #else: url = ''
                        #addLink(url,url,'')
    		except:pass
    	elif "nowvideo" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	elif "primeshare" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	elif "allmyvideos" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	elif "vkontakte" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	elif "videoslasher" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	elif "sockshare" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	elif "firedrive" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
                        #addLink(url,url,'')
    		except:pass
    	elif "videowood" in url:
                try:
                        iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			tit=re.compile('title: "(.+?)"').findall(link3)
			match=re.compile('file: "(.+?)"').findall(link3)
			subtitle=re.compile("addSubtitles[(]'(.+?)'").findall(link3)
			if match:
                                #addLink(tit[0]+match[0],match[0],'')
                                if subtitle == []:
                                        checker = ''
                                        url = match[0].replace('\/','/')
                                else:
                                        checker = subtitle[0]
                                        url = match[0].replace('\/','/')
                        else:
                                iframe_url = url.replace('/embed/','/video-link/')
                                link3 = abrir_url(iframe_url)
                                if link3 != []:
                                        match=re.compile('"url":"(.+?)"}').findall(link3)
                                        if subtitle == []:
                                                checker = ''
                                                url = match[0].replace('\/','/')
                                        else:
                                                checker = subtitle[0]
                                                url = match[0].replace('\/','/')
			#addLink(name+match[0],match[0],'')
    		except:pass
    	elif "movshare" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	elif "video.tt" in url or "videott" in url:
                try:
                        iframe_url = url
			print iframe_url
			link3 = abrir_url(iframe_url)
			id_video = re.compile('http://video.tt/player_control/settings.php?v=(.+?)&fv=v1.2.74').findall(url)
			if not id_video: id_video = re.compile('"vcode":"(.+?)"').findall(link3)
			v_key=re.compile('"time":"(.+?)"}').findall(link3)
			tit=re.compile('Title=(.+?)&SourceURL=').findall(link3)
			tt=re.compile('"st":(.+?),"tst"').findall(link3)
			vlink='http://gs.video.tt/s?v='+id_video[0]+'&r=1&t='+tt[0]+'&u=&c='+v_key[0]+'&start=0'
			subtitle=re.compile("addSubtitles[(]'(.+?)'").findall(link3)
			#subtitle = []
			if subtitle == []:
				checker = ''
				url = vlink
			else:
				checker = subtitle[0]
				url = vlink
			#addLink('Ver Filme',url,'')
                        #addLink(id_video[0],vlink,'')
                        #addLink(tt[0],vlink,'')
                        #addLink(v_key[0],vlink,'')
                        #addLink(vlink,vlink,'')
			#addLink(url,'','')
    		except:pass
    	elif "videomega" in url:
		try:
                        if "iframe" not in url:
                                id_videomega = re.compile('ref=(.*)').findall(url)[0]
                                iframe_url = 'http://videomega.tv/iframe.php?ref=' + id_videomega
                        else: iframe_url = url
                        print iframe_url
                        link3 = abrir_url(iframe_url)
                        match=re.compile('document.write\(unescape\("(.+?)"\)').findall(link3)
                        print match
                        tit=re.compile('<div id="title">&nbsp;&nbsp;&nbsp;(.+?)</div>').findall(link3)
                        video_url_escape = urllib.unquote(match[0])
                        match=re.compile('file: "(.+?)"').findall(video_url_escape)
                        subtitle=re.compile('"file": "(.+?)"').findall(video_url_escape)
                        if subtitle==[]:
                                subtitle=re.compile('[[][{]file: "(.+?)"').findall(video_url_escape)      
                        if subtitle == []:
                                checker = ''
                                url = match[0]
                        else:
                                checker = subtitle[0].replace('http://videomega.tv/servesrt.php?s=','')
                                url = match[0]
                        #addLink(checker,match[0],'')
		except: pass
	nome_addon = nomeAddon
	#addLink(url,'','','')
	#return
        #if 'vk.com' not in url and 'video.mail.ru' not in url and 'video.tt' not in url:
        if 'vk.com' not in iframe_url and 'video.mail.ru' not in iframe_url and 'videoapi.my.mail' not in iframe_url and 'vidzi.tv' not in iframe_url and 'playfreehd' not in iframe_url  and 'thevideo.me' not in iframe_url:# and 'iiiiiiiiii' in url:
                try:
                        #addLink(name,url,iconimage,fanart)
                        playlist = xbmc.PlayList(1)
                        playlist.clear()

                        liz=xbmcgui.ListItem(name, thumbnailImage=iconimage)
                        xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,liz)
                        playlist.add(url,liz)

                        MyPlayer(nome_addon=nome_addon,checker=checker).PlayStream(playlist)
                        
##                        playlist = xbmc.PlayList(1)
##                        playlist.clear()             
##                        playlist.add(url,xbmcgui.ListItem(name, thumbnailImage=str(iconimage)))
##                        MyPlayer(nome_addon=nome_addon,checker=checker).PlayStream(playlist)

                except: pass
        #return
                
class MyPlayer(xbmc.Player):
        def __init__( self, *args, **kwargs ):
                xbmc.Player.__init__( self )
                self.nomeaddon = kwargs[ "nome_addon" ]
                self.checkerSubs = kwargs[ "checker" ]
                self.Playable = 'Nao'

        def PlayStream(self, playlist):
                self.play(playlist)
                progress.close()
                if self.checkerSubs == '' or self.checkerSubs == None: pass
                else: self.setSubtitles(self.checkerSubs)
                if not self.isPlaying() and self.Playable == 'Nao':
                        xbmcgui.Dialog().ok('SITES dos PORTUGAS', 'Este stream está offline.', 'Tente outro stream.')
                while self.isPlaying():
                        xbmc.sleep(1000)

        def onPlayBackStarted(self):
                self.Playable = 'Sim'
                progress.close()
                            
        def onPlayBackEnded(self):
                self.Playable = 'Nao'
                progress.close()

        def onPlayBackStopped(self):
                self.Playable = 'Nao'
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
mvoutv=None
automatico=None

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
try: mvoutv=urllib.unquote_plus(params["mvoutv"])
except: pass
try: automatico=urllib.unquote_plus(params["automatico"])
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
print "MvouTv: "+str(mvoutv)
print "Automatico: "+str(automatico)
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
