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



import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,time,os,threading#,TopPt,TugaFilmesTV
from Funcoes import thetvdb_api, themoviedb_api, themoviedb_api_tv, theomapi_api, themoviedb_api_IMDB, themoviedb_api_IMDB_episodios, themoviedb_api_TMDB, thetvdb_api_IMDB
from Funcoes import thetvdb_api_tvdbid, thetvdb_api_episodes, themoviedb_api_search_imdbcode, themoviedb_api_pagina, themoviedb_api_IMDB1, theomapi_api_nome
from Funcoes import addDir, addDir1, addDir2, addLink, addLink1, addDir_teste, addDir_trailer, addDir_episode, addDir_trailer1, addDir_episode1, addDir_episode_false
from Funcoes import get_params,abrir_url
from TugaFilmesTV import TFV_resolve_not_videomega_series
##from TopPt import TPT_resolve_not_videomega_filmes
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
_ser = []
arr_filmes = ['' for i in range(200)]
arrai_filmes = ['' for i in range(200)]
thumb_filmes = ['' for i in range(200)]
arr_filmes[4] = '0'
i=arr_filmes[4]
filmesTPT = []
filmesTFV = []
filmesTFC = []
filmesMVT = []
filmesFTT = []
filmesCMT = []
filmesCME = []
filmesCMC = []
filmes = []

fanfan = []
fanfan1 = []

arr_filmes_anima = []
arrai_filmes_anima = []

#http://www.omdbapi.com/?i=tt0903624http://api.themoviedb.org/3/movie/now_playing?api_key=3e7807c4a01f18298f64662b257d7059&append_to_response=overview&page=1

progress = xbmcgui.DialogProgress()

#-----------------------------------------------------------------------------------------------------------------------------------------------#
def ultimos_episodios(url):

        urlss = urllib.unquote(url)
        print urlss
        urls=re.compile('url_TFC=(.+?)&url_MVT=(.+?)&url_TFV=(.+?)&xpto=xpto&url_TPT=(.+?)&fim=fim').findall(urlss)
        url_TFV = urls[0][2]
        url_TFC = urls[0][0]
        url_MVT = urls[0][1]
        url_TPT = urls[0][3]
        #addLink(urlss,'','','')
        
        percent = 0
##        message = 'Por favor aguarde.'
##        progress.create('Progresso', 'A Procurar')
##        progress.update( percent, 'A Procurar Últimos Episódios...', message, "" )

##        builtin = 'XBMC.Notification(%s,%s, 8000, %s)'
##        log = xbmc.executebuiltin(builtin % ('A Procurar Últimos Episódios.', 'Por favor aguarde...',artfolder + 'SDPI.png'))
        try: xbmcgui.Dialog().notification('A Procurar Últimos Episódios.', 'Por favor aguarde...', artfolder + 'SDPI.png', 8000, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, 8000, %s)" % ('A Procurar Últimos Episódios.', 'Por favor aguarde...', artfolder + 'SDPI.png'))

        #----------------------------------------------------------------------------------------------------
        threads = []
        
        i = 0
        try:
                try:
                        html_source = abrir_url(url_TPT)
                except: html_source = ''
                itemsTPT = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
                if itemsTPT != []:
                        proxima_TPT = re.compile('</span><a class="nextpostslink" rel="next" href="(.+?)">&raquo;</a><a class="last"').findall(html_source)
                        try:
                                url_TPT = proxima_TPT[0].replace('#038;','').replace('&amp;','&')
                        except: pass
                else: url_TPT = 'http:'

                for item in itemsTPT:
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        TPT = threading.Thread(name='TPT'+str(i), target=ultimos_ep_TPT , args=('FILME'+str(a)+'FILME'+item,))
                        threads.append(TPT)
                        _filmes_.append(TPT)
        except: pass

        [i.start() for i in threads]

        [i.join() for i in threads]

        threads = []
        i = 0
        try:
                try:
                        html_source = abrir_url(url_TFV)
                except: html_source = ''
                itemsTFV = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
                if itemsTFV != []:
                        try:
                                proxima_TFV = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
                                url_TFV = proxima_TFV[0].replace('&amp;','&')
                        except: pass
                else: url_TFV = 'http:'

                for item in itemsTFV:
                        thumb = ''
                        fanart = ''
                        genero = ''
                        sinopse = ''
                        imdbcode = ''
                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
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
                        nome_pesquisa = nome_original
                        passaurlimdbcode = urletitulo[0][0]+'IMDB'+imdbcode+'IMDB'
                        
                        nome_fi = '[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano.replace(' ','') + '[/COLOR][COLOR red] ' + qualidade + '[/COLOR] '
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        item = 'FILME'+str(a)+'FILME'+item
                        #TFV = threading.Thread(name='TFV'+str(i), target=ultimos_ep_TFV , args=('FILME'+str(a)+'FILME'+item,))
                        TFV1 = threading.Thread(name='TFV1'+str(i), target=busca_tvid , args=(item,passaurlimdbcode,nome_pesquisa,nome_fi,imdbcode,))
                        #TFV2 = threading.Thread(name='TFV2'+str(i), target=ultimos_ep_TFV , args=('FILME'+str(a)+'FILME'+item,nome_pesquisa,imdbcode,tv_id,))
                        threads.append(TFV1)
                        _filmes_.append(TFV1)
##                        i = i + 1
##                        a = str(i)
##                        if i < 10: a = '0'+a
##                        TFV = threading.Thread(name='TFV'+str(i), target=ultimos_ep_TFV , args=('FILME'+str(a)+'FILME'+item,))
##                        threads.append(TFV)
        except: pass

        [i.start() for i in threads]

        [i.join() for i in threads]

        [i.start() for i in fanfan]

        [i.join() for i in fanfan]

        [i.start() for i in fanfan1]

        [i.join() for i in fanfan1]

        num_filmes = 0

        for x in range(len(_filmes_)):
                num_filmes = num_filmes + 1

        num_total = num_filmes + 0.0
        progress.create('[B][COLOR green]SITES[/COLOR][COLOR yellow]dos[/COLOR][COLOR red]PORTUGAS[/COLOR][/B]', '')
        for a in range(num_filmes):
                percent = int( ( a / num_total ) * 100)
                message = str(a+1) + " de " + str(num_filmes)
                progress.update( percent, 'A Finalizar ...', message, "" )
                xbmc.sleep(12)
        
        url_MVT = 'http:'
        url_TFC = 'http:'
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "fim": 'fim',"xpto":'xpto'}
        url_ultimos_episodios = urllib.urlencode(parameters)
        addDir('[B]Página Seguinte >>[/B]',url_ultimos_episodios,508,artfolder + 'PAGS1.png','','')
        progress.close()
        
#----------------------------------------------------------------------------------------------------
        
def ultimos_ep_TPT(item):
        
        if item != '':
                try:
                        FILMEN = re.compile('FILME(.+?)FILME').findall(item)
                        FILMEN = FILMEN[0]
                        sinopse = ''
                        fanart = ''
                        thumb = ''
                        qualidade = ''
                        urltrailer = ''
                        audio_filme = ''
                        imdbcode = ''

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

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
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

                        n = re.compile('(.+?)[[].+?[]]').findall(nome)
                        if n: nome_pesquisa = n[0]
                        tv_id, sinopse = thetvdb_api_IMDB()._id(nome_pesquisa,imdbcode)
                        if tv_id != '':
                                fanart = 'http://thetvdb.com/banners/fanart/original/' + tv_id + '-1.jpg'
                                try:
                                        urllib2.urlopen(fanart)
                                except urllib2.HTTPError, e:
                                        fanart = 'http://thetvdb.com/banners/fanart/original/' + tv_id + '-2.jpg'
                                if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + tv_id + '-1.jpg'
                        else:
                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme+'|'+imdbcode)
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
                                #addLink(nome,'','','')
                                nome_fi = '[COLOR orange]TPT | [/COLOR][B][COLOR green]' + nome+ '[/COLOR][/B][COLOR yellow] ' +ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]'
                                nome_final = '[COLOR orange]TPT | [/COLOR][B][COLOR green]' + nome+ '[/COLOR][/B][COLOR yellow] ' +ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]'
                                filmesTPT.append(FILMEN+'NOME|'+str(nome_final)+'|IMDBCODE|'+str(urletitulo[0][0])+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb)+'|ANO|'+str(ano_filme.replace('(','').replace(')',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|ONOME|'+str(nome_pesquisa)+'|SINOPSE|'+str(sinopse)+'|END|\n')
                                TPT_Ultimos(nome_fi,urletitulo[0][0]+'IMDB'+str(imdbcode)+'IMDB',thumb,fanart,item,tv_id)
                        except: pass
                except: pass
        else: pass

#----------------------------------------------------------------------------------------------------

def ultimos_ep_TFV(item,passaurlimdbcode,nome_pesquisa,nome_fi,imdbcode,tv_id):
        
        if item != '':

                try:
                        FILMEN = re.compile('FILME(.+?)FILME').findall(item)
                        FILMEN = FILMEN[0]
                        item = 'FILME'+FILMEN+'FILME'+item
                        url = 'http://thetvdb.com/api/23B3F3D91B980C9F/series/'+str(tv_id)+'/pt.xml'
                        try: html_source = abrir_url(url)
                        except: html_source = ''
                        fan = re.compile('<fanart>(.+?)</fanart>').findall(html_source)#(fanart,name,url,item,tvdbid)
                        try: fanart = 'http://thetvdb.com/banners/'+fan[0]
                        except: fanart = ''
                        #addLink(tv_id+passaurlimdbcode+nome_pesquisa+nome_fi+imdbcode,'','',fanart)
                        TFV3 = threading.Thread(name='TFV3'+FILMEN, target=TFV_Ultimos , args=(fanart,nome_fi,passaurlimdbcode,item,tv_id,))
                        fanfan1.append(TFV3)

		except: pass
        else: pass

def busca_tvid(item,passaurlimdbcode,nome_pesquisa,nome_fi,imdbcode):
        FILMEN = re.compile('FILME(.+?)FILME').findall(item)
        FILMEN = FILMEN[0]
        item = 'FILME'+FILMEN+'FILME'+item
        tv_id, sinopse = thetvdb_api_IMDB()._id(nome_pesquisa,imdbcode)
        #addLink(tv_id+passaurlimdbcode+nome_pesquisa+nome_fi+imdbcode,'','','')
        TFV2 = threading.Thread(name='TFV2'+FILMEN, target=ultimos_ep_TFV , args=(item,passaurlimdbcode,nome_pesquisa,nome_fi,imdbcode,tv_id,))
        fanfan.append(TFV2)
        
#----------------------------------------------------------------------------------------------------

def TFV_Ultimos(fanart,name,url,item,tvdbid):
        FILMEN = re.compile('FILME(.+?)FILME').findall(item)
        FILMEN = FILMEN[0]

        ####################
        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(name)
        if nnn: nnnn = re.compile('(.+?)[(].+?[)]').findall(nnn[0])
        if nnnn : n_pesquisa = nnnn[0]
        else:
                nnn = re.compile('IMDB.+?IMDB(.*)').findall(url)
                if nnn: n_pesquisa = nnn[0]
                else: n_pesquisa = ''

        namet = n_pesquisa

        nnn = re.compile('[[]COLOR yellow[]](.+?)[[]/COLOR[]]').findall(name)
        if nnn: nnnn = re.compile('[(](.+?)[)]').findall(nnn[0])
        if nnn : anne = nnnn[0]
        else: anne = ''
        
        imdb = re.compile('IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''

        season = re.compile('Temporada(.+?)[-].+?[(]').findall(name)
        if season: season = season[0]
        else:
                season = re.compile('Temporada(.+?)[(]').findall(name)
                if season: season = season[0]
                else:
                        season = re.compile('[(](.+?)[-].+?[)]').findall(name)
                        if season: season = season[0]
                        else:
                                season = re.compile('[(](.+?)[)]').findall(name)
                                if season: season = season[0]
                                else: season = ''

        temporada = re.compile('(\d+)').findall(season)
        if temporada:
                temporada = temporada[0]
                temporadat = temporada[0]
        else:
                temporada = ''
                temporadat = ''
        a_q = re.compile('\d+')
        qq_aa = a_q.findall(temporada)
        for q_a_q_a in qq_aa:
                if len(q_a_q_a) == 1:
                        temporadat = '0'+temporada
                else: temporadat = temporada

        #tvdbid = thetvdb_api_tvdbid()._id(n_pesquisa,anne)
        #addLink(season+'-'+imdbcode+'-'+tvdbid+'-'+temporadat+'-'+anne+'-'+n_pesquisa+'-'+name,'','','')
        #return
        #######################
        
        urlseries = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlseries: url = url.replace('IMDBIMDB','')
        else: url = urlseries[0]

        urltrailer = url
        #addLink(imdbcode+'-'+tvdbid+'-'+temporadat+'-'+anne+'-'+n_pesquisa+'-'+name,'','','')
        episodioanterior = ''
        episodio = ''
        episodiot = ''
        #return
        f_id = ''
        i = 0
        conta_id_video = 0
        
	nome_antes = '[COLOR orange]TFV | [/COLOR][B][COLOR green]' + namet + '[/COLOR][/B] | '

        if item != '':

                try:
                        items_series = re.findall("<div class='id(.+?)</a>", item, re.DOTALL)
                        if not items_series: items_series = re.findall("<div class='id(.+?)</p>", item, re.DOTALL)
                        n_items = len(items_series)
##                        if 'calendar_title' in items[0]: n_items = n_items - 1
                        if 'calendar_title' in item: n_items = n_items - 1
                        divide = n_items + 0.0
      
                        for item_vid_series in items_series:
                                not_vi = re.compile('>(.+?)</div></h3>').findall(item_vid_series)
                                if not not_vi: not_vi = re.compile('>(.+?)</div></h3>').findall(item_vid_series)
                                if 'div class=' in not_vi[0]: not_vi = re.compile('>(.*)').findall(not_vi[0])
                                nomecada = not_vi[0]
                                e1 = re.compile('(\d+) [-] ').findall(nomecada)
                                if e1: e1 = e1[0]

                        for item_vid_series in items_series:
                                not_vi = re.compile('>(.+?)</div></h3>').findall(item_vid_series)
                                if not not_vi: not_vi = re.compile('>(.+?)</div></h3>').findall(item_vid_series)
                                if 'div class=' in not_vi[0]: not_vi = re.compile('>(.*)').findall(not_vi[0])
                                nomecada = not_vi[0]
                                e = re.compile('(\d+) [-] ').findall(nomecada)
                                if e: e = e[0]
                                #addLink(namet+'-'+e+'-'+e1,'','','')

                                #addLink(item_vid_series,'','','')
                                not_videomeganome = re.compile('>(.+?)</div></h3>').findall(item_vid_series)
                                if not not_videomeganome: not_videomeganome = re.compile('>(.+?)</div></h3>').findall(item_vid_series)
                                if 'div class=' in not_videomeganome[0]: not_videomeganome = re.compile('>(.*)').findall(not_videomeganome[0])
                                nomecadaepisodio = not_videomeganome[0]
                                episodioanterior = re.compile('(\d+) [-] ').findall(nomecadaepisodio)
                                if episodioanterior: episodioanterior = episodioanterior[0]
                                
                                if e == e1:
                                        #addLink(e1+'sim'+e,'','','')
                                        try:
                                                if 'videomega' in item_vid_series:
                                                        try:
                                                                videomega_video_url = re.compile('<iframe .+? src="(.+?)"').findall(item_vid_series)
                                                                nome = videomega_video_nome[0]
                                                                nome = nome.replace('&#8217;',"'")
                                                                nome = nome.replace('&#8211;',"-")
                                                                nome = nome.replace('&#39;',"'")
                                                                nome = nome.replace('&amp;','&')
                                                                addDir('[B][COLOR green]' + nome + '[/COLOR] - Fonte : [COLOR yellow](Videomega)[/COLOR][/B]',videomega_video_url[0],30,iconimage,'',fanart)
                                                        except:pass
                                                        
                                                if 'ep' and 'src' and 'iframe' in item_vid_series:
                                                        try:
                                                                not_videomega_video_url = re.compile('<iframe .+? src="(.+?)"').findall(item_vid_series)
                                                                nome_cada_episodio = nomecadaepisodio
                                                                url = not_videomega_video_url[0]
                                                                identifica_video = re.compile('=(.*)').findall(not_videomega_video_url[0])                                                        
                                                                id_video = identifica_video[0]
                                                                src_href = 'src'
                                                                nome_cada_episodio = nome_cada_episodio.replace('&#8217;',"'")
                                                                nome_cada_episodio = nome_cada_episodio.replace('&#8211;',"-")
                                                                nome_cada_episodio = nome_cada_episodio.replace('&#39;',"'")
                                                                nome_cada_episodio = nome_cada_episodio.replace('&amp;','&')
                                                                if "ep" in item_vid_series: url = 'videomega'
                                                                if "vw" in item_vid_series: url = 'videowood'
                                                                if "dv" in item_vid_series: url = 'dropvideo'
                                                                if "vt" in item_vid_series: url = 'vidto.me'
                                                                if "nv" in item_vid_series: url = 'nowvideo'
                                                                try:
                                                                        fonte_id = TFV_resolve_not_videomega_series(name,url,id_video,nome_cada_episodio,src_href)
                                                                except: pass
                                                        except:pass
                                                        
                                                if 'href' and 'Clique' in item_vid_series:
                                                        try:
                                                                not_videomega_video_url = re.compile('href="(.+?)"').findall(item_vid_series)
                                                                if not not_videomega_video_url: not_videomega_video_url = re.compile("href='(.+?)'").findall(item_vid_series)
                                                                if not_videomega_video_url: url = not_videomega_video_url[0]
                                                                else: url = ''

                                                                identifica_video = re.compile('=(.*)').findall(not_videomega_video_url[0])                                                        
                                                                if identifica_video: id_video = identifica_video[0]
                                                                else: id_video = ''
                                                                
                                                                src_href = 'href'
                                                                
                                                                if "ep" in item_vid_series: url = 'videomega'
                                                                if "vw" in item_vid_series: url = 'videowood'
                                                                if "dv" in item_vid_series: url = 'dropvideo'
                                                                if "vt" in item_vid_series: url = 'vidto.me'
                                                                if "nv" in item_vid_series: url = 'nowvideo'

                                                                nome_cada_episodio = nomecadaepisodio
                                                                
                                                                nome_cada_episodio = nome_cada_episodio.replace('&#8217;',"'")
                                                                nome_cada_episodio = nome_cada_episodio.replace('&#8211;',"-")
                                                                nome_cada_episodio = nome_cada_episodio.replace('&#39;',"'")
                                                                nome_cada_episodio = nome_cada_episodio.replace('&amp;','&')
                                                                #addLink(nome_cada_episodio,'','')
                                                                #addLink(url,'','')
                                                                
                                                                try:
                                                                        fonte_id = TFV_resolve_not_videomega_series(name,url,id_video,nome_cada_episodio,src_href)
                                                                except: pass
                                                        except:pass
                                                                                        
                                        except:pass

                                        if f_id == '': f_id = fonte_id
                                        else: f_id = f_id + '|' + fonte_id

                        episodio = re.compile('(\d+) [-] ').findall(nomecadaepisodio)
                        if episodio:
                                episodiot = episodio[0]
                                episodio = episodio[0]
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(episodio)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 1:
                                        episodiot = '0'+episodio

                        try:
                                epi_nome,air,sin,th = thetvdb_api_episodes()._id(str(tvdbid),str(temporada),str(episodio))

                                try:
                                        addDir_episode_false(nome_antes+' [COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,th,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer)
                                        f_id = ''
                                except: pass
                        except:                                     
                                nomeepisodio = re.compile(' [-] (.*)').findall(nomecadaepisodio)
                                if nomeepisodio: nomeepisodio = nomeepisodio[0]
                                else: nomeepisodio = nomecadaepisodio

                                addDir_episode_false(nome_antes+' [COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+nomeepisodio+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+nomeepisodio+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer)
                                f_id = ''
                                
                except:pass

#------------------------------------------------------------------------------------------------
                
        
def TPT_Ultimos(name,url,iconimage,fanart,item,tvdbid):
        #addLink(name,'',iconimage,fanart)
        if 'Season' in name or 'Temporada' in name or 'Mini-Série' in name or 'Mini-Serie' in name or 'Minisérie' in name or 'Miniserie' in name:
                n = re.compile('[[](.+?)[]][[](.+?)[]]').findall(name)
                if not n: n = re.compile('[[](.+?)[]] [[](.+?)[]]').findall(name)
                if n: nome = n[0][0]+' - '+n[0][1]
                else:
                        n = re.compile('[(](.+?)[)][(](.+?)[)]').findall(name)
                        if not n: n = re.compile('[(](.+?)[)] [(](.+?)[)]').findall(name)
                        if n: nome = n[0][0]+' - '+n[0][1]
                        else:
                                n = re.compile('[[](.+?)[]]').findall(name)
                                if n: nome = n[0]
                                else:
                                        n = re.compile('[(](.+?)[)]').findall(name)
                                        if n: nome = n[0]

                nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(name)
                if nnn: nnnn = re.compile('(.+?)[[].+?[]].+?[]]').findall(nnn[0])
                if nnnn : n_pesquisa = nnnn[0]
                else:
                        nnn = re.compile('IMDB.+?IMDB(.*)').findall(url)
                        if nnn: n_pesquisa = nnn[0]
                        else: n_pesquisa = ''

                namet = n_pesquisa

                season = re.compile('[[](.+?)[]].+?[]]').findall(nnn[0])
                if season: season = season[0]
                else:
                        season = re.compile('[[](.+?)[]]').findall(nnn[0])
                        if season: season = season[0]
                        else:
                                season = re.compile('(.+?)[-].+?').findall(name)
                                if season: season = season[0]
                                else: season = ''
                temporada = re.compile('(\d+)').findall(season)
                if temporada:
                        temporada = temporada[0]
                        temporadat = temporada[0]
                else:
                        temporada = ''
                        temporadat = ''
                a_q = re.compile('\d+')
                qq_aa = a_q.findall(temporada)
                for q_a_q_a in qq_aa:
                        if len(q_a_q_a) == 1:
                                temporadat = '0'+temporada
                        else: temporadat = temporada

                nnn = re.compile('[[]COLOR yellow[]](.+?)[[]/COLOR[]]').findall(name)
                if nnn and '(' not in nnn[0]: anne = nnn[0].replace(' ','')
                else:
                        if nnn: nnnn = re.compile('[(](.+?)[)]').findall(nnn[0])
                        if nnn: anne = nnnn[0]
                        else: anne = ''

                imdb = re.compile('IMDB(.+?)IMDB').findall(url)
                if imdb: imdbcode = imdb[0]
                else: imdbcode = ''

                #tvdbid = thetvdb_api_tvdbid()._id(n_pesquisa,anne)
                #addLink(temporadat+'-'+anne+'-'+n_pesquisa,'','','')
                #return
        episodiot = ''
        episodio = ''
        tmdbcode = ''
        f_id = ''
        iconimage = iconimage
        nomeescolha = name
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]
        urltrailer = url
        if 'TPT' not in name: name = '[COLOR orange]TPT | [/COLOR]' + name
        if 'TPT' not in nomeescolha: nomeescolha = '[COLOR orange]TPT | [/COLOR]' + nomeescolha
        conta_os_items = 0
        nometitulo = nomeescolha
        i = 1
        conta_id_video = 0
        contaultimo = 0
        l= 0
	try:
		link2=abrir_url(url)
	except: link2 = ''
	#addLink(url,'','','')
        episodioanterior = ''
	nome_antes = '[COLOR orange]TPT | [/COLOR][B][COLOR green]' + namet + '[/COLOR][/B] | '
	if link2:
                if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo and 'Mini-Serie' not in nometitulo and 'Minisérie' not in nometitulo and 'Miniserie' not in nometitulo:
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
                        newmatch = re.findall('EM PT/PT:.+?<nav class="navigation post-navigation"',link2,re.DOTALL)
                        
                linkseries = re.findall('</span>CLIQUE AQUI PARA VER O (.+?)</div>(.+?)</div></div>',link2,re.DOTALL)
                if not linkseries: linkseries = re.findall('<span style="color:.+?">(.+?)</span><br.+?>(.+?)Ver Aqui</a></p>',link2,re.DOTALL)
                if not linkseries: linkseries = re.findall('<span style="color:.+?"><strong>(.+?)</strong></span><br.+?>(.+?)Ver Aqui</a></p>',link2,re.DOTALL)
                if not linkseries: linkseries = re.findall('ODIO (.+?)<.+?>(.+?)<img',newmatch[0],re.DOTALL)
                if not linkseries: linkseries = re.findall('ODIO (.+?)<.+?>\n(.+?)EPIS',newmatch[0],re.DOTALL)
                if not linkseries: linkseries = re.findall('<p>(.+?)EPISODIO<br/>(.+?)</iframe>',newmatch[0],re.DOTALL)
                if not linkseries: linkseries = re.findall('EPISODIO (.+?)<br.+?\n(.+?)</p>',newmatch[0],re.DOTALL)
                                                        #linksseccaoultimo = re.findall('ODIO (.+?)<.+?>\n(.+?)</p>',newmatch[0],re.DOTALL)
                if '<h2 class="title">Sleepy Hollow[Season 1][Completa]</h2>' in link2:
                        linkseries = re.findall('<p>(.+?)<br/>(.+?)</p>',newmatch[0],re.DOTALL)
                #for parte1,parte2 in linkseries:
                if linkseries:
                        parte1 = linkseries[0][0]
                        try:
                                episodio = re.compile('(\d+)').findall(linkseries[0][0])
                                if episodio:
                                        episodiot = episodio[0]
                                        episodio = episodio[0]
                                a_q = re.compile('\d+')
                                qq_aa = a_q.findall(episodio)
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) == 1:
                                                episodiot = '%02d' % int(episodio)#'0'+episodio
                        except: pass                        
                        #addLink(parte1+'-'+namet,'','','')              
                        try:
                                try:
                                        epi_nome,air,sin,th = thetvdb_api_episodes()._id(str(tvdbid),str(temporada),str(episodio))
                                        iconimage = th
                                except: pass
                                conta_id_video = 0
                                                
                                match = re.compile('<span class="su-lightbox" data-mfp-src="(.+?)" data-mfp-type="iframe">').findall(linkseries[0][1])
                                for url in match:
                                        if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                conta_id_video = conta_id_video + 1
                                                conta_os_items = conta_os_items + 1
                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                if f_id == '': f_id = fonte_id
                                                else: f_id = f_id + '|' + fonte_id
                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(linkseries[0][1])
                                for url in match:
                                        if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                conta_id_video = conta_id_video + 1
                                                conta_os_items = conta_os_items + 1
                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                if f_id == '': f_id = fonte_id
                                                else: f_id = f_id + '|' + fonte_id
                                match = re.compile('"window.open(.+?)"').findall(linkseries[0][1])
                                for url in match:
                                        if "videomega" in url or "vidto.me" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                conta_id_video = conta_id_video + 1
                                                url = url.replace("'","").replace("(","").replace(")","")
                                                conta_os_items = conta_os_items + 1
                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                if f_id == '': f_id = fonte_id
                                                else: f_id = f_id + '|' + fonte_id
                                try:

                                        #label = temporada + 'x' + '%02d' % int(episodiot) + ' . ' + epi_nome
                                        addDir_episode_false(nome_antes+'[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer)
                                except:
                                        if 'EPI' not in linkseries[0][0] and 'Epi' not in linkseries[0][0]: parte1 = linkseries[0][0]+'º EPISÓDIO'
                                        addDir_episode_false(nome_antes+'[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer)

                                f_id = ''
                                i = i + 1
                        except: pass



def TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart):
        
        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                url = url + '///' + nomeescolha
        
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
				fonte_id = '(Vidto.me)'+url1
				url = 'http://vidto.me/' + id_video + '.html' + '///' + nomeescolha
			else: fonte_id = '(Vidto.me)'+url
			fonte_id1 = '(Vidto.me)'+url
			#fonte_id = '(Vidto.me)'+url
			if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id1.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
        if "dropvideo" in url:
		try:
                        url = url.replace('/video/','/embed/')
                        fonte_id = '(DropVideo)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "vidzi.tv" in url:
                try:
                        fonte_id = '(Vidzi.tv)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "vodlocker" in url:
		try:
                        fonte_id = '(Vodlocker)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "played.to" in url:
                try:
                        fonte_id = '(Played.to)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "cloudzilla" in url:
                try:
                        fonte_id = '(Cloudzilla)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "divxstage" in url:
                try:
                        fonte_id = '(Divxstage)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "vidzen" in url:
                try:
                        fonte_id = '(Vidzen)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
	if "streamin.to" in url:
                try:
                        fonte_id = '(Streamin)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass                        
    	if "nowvideo" in url:
                try:
                        fonte_id = '(Nowvideo)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "primeshare" in url:
                try:
                        fonte_id = '(Primeshare)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videoslasher" in url:
                try:
                        fonte_id = '(VideoSlasher)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "sockshare" in url:
                try:
                        fonte_id = '(Sockshare)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "putlocker" in url:
                try:
                        url = url.replace('putlocker.com/embed/','firedrive.com/file/')
                        fonte_id = '(Firedrive)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	else:
                if "firedrive" in url:
                        try:
                                fonte_id = '(Firedrive)'+url
                                if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
                        except:pass
    	if "movshare" in url:
                try:
                        fonte_id = '(Movshare)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
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
                                url = url + '///' + nomeescolha
                        fonte_id = '(Video.tt)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('1[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(VideoWood)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "thevideo.me" in url:
                try:
                        #if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(Thevideo.me)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	#addLink(url,'','','')
        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url and 'sockshare' not in url and 'firedrive' not in url and 'movshare' not in url and 'nowvideo' not in url and 'putlocker' not in url:# and 'iiiiiiiiii' in url:
                        Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'').replace(url+'///'+nomeescolha,'')+'[/COLOR][/B]',iconimage,'',fanart)
    	return fonte_id
                
########################################################################################################################################################
######################################################   FILMES   ######################################################################################

def Filmes_Filmes_Filmes(url):
        i= 0
        return
        
def TPTMASHUP(item):

        folder = perfil
        Filmes_File = open(folder + 'filmesTPT.txt', 'w')
        
        if item != '':
                try:
                        FILMEN = re.compile('FILME(.+?)FILME').findall(item)
                        FILMEN = FILMEN[0]
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
##                        progress.update( percent, 'A Procurar Filmes '+pontos, '[COLOR green]'+O_Nome+'[/COLOR]', "" )
##                        pontos = pontos +'.'

                        try:
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
                                filmesTPT.append(FILMEN+'NOME|'+str(nome_final)+'|IMDBCODE|'+str(urletitulo[0][0])+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb)+'|ANO|'+str(ano_filme.replace('(','').replace(')',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|ONOME|'+str(O_Nome)+'|SINOPSE|'+str(sinopse)+'|END|\n')
                        except: pass
                except: pass
        else: pass
        
        filmesTPT.sort()
        for x in range(len(filmesTPT)):
                Filmes_File.write(str(filmesTPT[x]))
        #Filmes_File.write('PAGINA|'+url_TPT+'|PAGINA')
        Filmes_File.close()

        
        #----------------------------------------------------------------------------------------------------
def TFCMASHUP(item):

        folder = perfil
        Filmes_File = open(folder + 'filmesTFC.txt', 'w')
        
        if item != '':
                try:
                        FILMEN = re.compile('FILME(.+?)FILME').findall(item)
                        FILMEN = FILMEN[0]
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
                        
                        
                        try:
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
                                try:
                                        fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano)
                                        if thumb == '': thumb = poster
                                except: pass
                        except: pass
                        
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        if qualidade == '': qualidade = '---'
			try:
                                if 'ASSISTIR O FILME' in item:
##                                        progress.update( percent, 'A Procurar Filmes '+pontos, '[COLOR green]'+O_Nome+'[/COLOR]', "" )
##                                        pontos = pontos+'.'
                                        nome_final = '[COLOR orange]TFC | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR][COLOR red] (' + qualidade + ')[/COLOR]' + versao
                                        filmesTFC.append(FILMEN+'NOME|'+str(nome_final)+'|IMDBCODE|'+urletitulo[0][0]+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb.replace('s1600','s320').replace('.gif','.jpg'))+'|ANO|'+str(ano.replace('(','').replace(')',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|ONOME|'+str(O_Nome)+'|SINOPSE|'+str(sinopse)+'|END|\n')
			except: pass
		except: pass
        else: pass
        
        filmesTFC.sort()
        for x in range(len(filmesTFC)):
                Filmes_File.write(str(filmesTFC[x]))
        #Filmes_File.write('PAGINA|'+url_TFC+'|PAGINA')
        Filmes_File.close()

        #----------------------------------------------------------------------------------------------------
        
def FTTMASHUP(item):

        folder = perfil
        Filmes_File = open(folder + 'filmesFTT.txt', 'w')
        
        if item != '':
                try:
                        FILMEN = re.compile('FILME(.+?)FILME').findall(item)
                        FILMEN = FILMEN[0]
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
                        

                        try:
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
                        except: pass
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        
                        try:
                                if 'Temporada' not in O_Nome and 'temporada' not in O_Nome:
##                                        progress.update( percent, 'A Procurar Filmes '+pontos, '[COLOR green]'+O_Nome+'[/COLOR]', "" )
##                                        pontos = pontos+'.'
                                        nome_final = '[COLOR orange]FTT | [/COLOR][B][COLOR green]' + O_Nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme.replace('</div>','') + ')[/COLOR]'
                                        filmesFTT.append(FILMEN+'NOME|'+nome_final+'|IMDBCODE|'+urlvideo+'IMDB'+imdbcode+'IMDB'+'|THUMB|'+str(thumb)+'|ANO|'+anofilme+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|ONOME|'+str(O_Nome)+'|SINOPSE|'+str(sinopse)+'|END|\n')
                        except: pass
                except: pass
	else: pass	
	
	filmesFTT.sort()
        for x in range(len(filmesFTT)):
                Filmes_File.write(str(filmesFTT[x]))
	#Filmes_File.write('PAGINA|'+url_FTT+'|PAGINA')
	Filmes_File.close()

#------------------------------------------------------------------------------------------------------------------------

def CMTMASHUP(item):

        folder = perfil
        Filmes_File = open(folder + 'filmesCMTnet.txt', 'w')
        
        if item != '':
                try:
                        FILMEN = re.compile('FILME(.+?)FILME').findall(item)
                        FILMEN = FILMEN[0]
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
##                        progress.update( percent, 'A Procurar Filmes '+pontos, '[COLOR green]'+O_Nome+'[/COLOR]', "" )
##                        pontos = pontos+'.'

                        try:
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
                                filmesCMT.append(FILMEN+'NOME|'+str(nome_final)+'|IMDBCODE|'+urletitulo[0][0]+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb.replace('s72-c','s320'))+'|ANO|'+str(ano_filme.replace(' ',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(genre)+'|ONOME|'+str(O_Nome)+'|SINOPSE|'+str(sinopse)+'|END|\n')
                        except: pass
                except: pass
	else: pass
	
        filmesCMT.sort()
        for x in range(len(filmesCMT)):
                Filmes_File.write(str(filmesCMT[x]))
        #Filmes_File.write('PAGINA|'+url_CMT+'|PAGINA')
        Filmes_File.close()

#------------------------------------------------------------------------------------------------------------------------------------

def TFVMASHUP(item):

        folder = perfil
        Filmes_File = open(folder + 'filmesTFV.txt', 'w')
        
        if item != '':
                try:
                        FILMEN = re.compile('FILME(.+?)FILME').findall(item)
                        FILMEN = FILMEN[0]
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
##                        progress.update( percent, 'A Procurar Filmes '+pontos, '[COLOR green]'+O_Nome+'[/COLOR]', "" )
##                        pontos = pontos+'.'

                        try:
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
                        except: pass
                        
                        if thumb == '': thumb = '---'
                        if genre == '': genre = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        
                        
                        try:
                                nome_final = '[COLOR orange]TFV | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow] (' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao
                                filmesTFV.append(FILMEN+'NOME|'+str(nome_final)+'|IMDBCODE|'+urletitulo[0][0]+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb.replace('s72-c','s320'))+'|ANO|'+str(ano[0].replace(' ',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(genre)+'|ONOME|'+str(O_Nome)+'|SINOPSE|'+str(sinopse)+'|END|\n')
                        except: pass
                except: pass
        else: pass
        
        filmesTFV.sort()
        for x in range(len(filmesTFV)):
                Filmes_File.write(str(filmesTFV[x]))
        #Filmes_File.write('PAGINA|'+url_TFV+'|PAGINA')
        Filmes_File.close()

        #----------------------------------------------------------------------------------------------------

def MVTMASHUP(item):

        folder = perfil
        Filmes_File = open(folder + 'filmesMVT.txt', 'w')
        
        if item != '':
                try:
                        FILMEN = re.compile('FILME(.+?)FILME').findall(item)
                        FILMEN = FILMEN[0]
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

                        O_Nome = nome
##                        progress.update( percent, 'A Procurar Filmes '+pontos, '[COLOR green]'+O_Nome+'[/COLOR]', "" )
##                        pontos = pontos+'.'

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
                                filmesMVT.append(FILMEN+'NOME|'+str(nome_final)+'|IMDBCODE|'+url[0].replace(' ','%20')+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb.replace(' ','%20'))+'|ANO|'+str(ano_filme)+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|ONOME|'+str(O_Nome)+'|SINOPSE|'+str(sinopse)+'|END|\n')
                        except: pass
                except: pass
        else: pass
        
        filmesMVT.sort()
        for x in range(len(filmesMVT)):
                Filmes_File.write(str(filmesMVT[x]))
        #Filmes_File.write('PAGINA|'+url_MVT+'|PAGINA')
        Filmes_File.close()

        #----------------------------------------------------------------------------------------------------

def CMEMASHUP(item):

        folder = perfil
        Filmes_File = open(folder + 'filmesCME.txt', 'w')
        
        if item != '':
                try:
                        FILMEN = re.compile('FILME(.+?)FILME').findall(item)
                        FILMEN = FILMEN[0]                                
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
##                        progress.update( percent, 'A Procurar Filmes '+pontos, '[COLOR green]'+O_Nome+'[/COLOR]', "" )
##                        pontos = pontos+'.'

                        try:
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
                        except: pass
                        
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        try:
                                nome_final = '[COLOR orange]CME | [/COLOR][B][COLOR green]' + O_Nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme.replace('</div>','') + ')[/COLOR]'
                                filmesCME.append(FILMEN+'NOME|'+str(nome_final)+'|IMDBCODE|'+urlvideo+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb)+'|ANO|'+str(anofilme)+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|ONOME|'+str(O_Nome)+'|SINOPSE|'+str(sinopse)+'|END|\n')
                        except: pass
                except: pass
        else: pass
        
	filmesCME.sort()
        for x in range(len(filmesCME)):
                Filmes_File.write(str(filmesCME[x]))
	#Filmes_File.write('PAGINA|'+url_CME+'|PAGINA')
        Filmes_File.close()

       #----------------------------------------------------------------------------------------------------
        
def CMCMASHUP(item):

        folder = perfil
        Filmes_File = open(folder + 'filmesCMC.txt', 'w')
        
        if item != '':
                try:
                        FILMEN = re.compile('FILME(.+?)FILME').findall(item)
                        FILMEN = FILMEN[0]                        
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
                                        
                        O_Nome = nome
                        
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
                        
                        
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'

                        try:
                                if 'Temporada' not in nome:
##                                        progress.update( percent, 'A Procurar Filmes '+pontos, '[COLOR green]'+O_Nome+'[/COLOR]', "" )
##                                        pontos = pontos+'.'
                                        nome_final = '[COLOR orange]CMC | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]'
                                        filmesCMC.append(FILMEN+'NOME|'+str(nome_final)+'|IMDBCODE|'+urlfilme.replace(' ','%20')+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb.replace(' ','%20'))+'|ANO|'+str(ano_filme)+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|ONOME|'+str(O_Nome)+'|SINOPSE|'+str(sinopse)+'|END|\n')
                        except: pass
                except: pass
	else: pass
        
	filmesCMC.sort()
        for x in range(len(filmesCMC)):
                Filmes_File.write(str(filmesCMC[x]))
	#Filmes_File.write('PAGINA|'+url_CMC+'|PAGINA')
        Filmes_File.close()


def PAGSEGUINTE():	
        for x in range(len(arrai_filmes)):
                if arrai_filmes[x] != '':           #8
                        addDir(arrai_filmes[x],'url',7,thumb_filmes[x],'nao','')
                        conta_os_items = conta_os_items + 1
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "url_FTT": url_FTT, "url_CMT": url_CMT, "url_CME": url_CME, "fim": 'fim',"xpto":'xpto'}
        url_filmes_filmes = urllib.urlencode(parameters)
        progress.close()
        addDir('[B]Página Seguinte >>[/B]',url_filmes_filmes,507,artfolder + 'PAGS1.png','','')

########################################################################################################################################################
############################################################   SÉRIES   ################################################################################        

def Series_Series(url):
        
##        percent = 0
##        message = 'Por favor aguarde.'
##        progress.create('Progresso', 'A Procurar')
##        progress.update( percent, 'A Procurar Séries (A/Z) ...', message, "" )
        
                
        num = 0
        i = 0
        thr = 0
        
        threads = []

        for i in range(len(filmes)):
                filmes[i] = ''
        
        try:
                folder = perfil
                
                try: Filmes_Fi = open(folder + 'Series1.txt', 'r')
                except:
                        Filmes_File = open(folder + 'Series1.txt', 'a')
                        Filmes_File.close()
                        Filmes_Fi = open(folder + 'Series1.txt', 'r')
                read_Filmes_File = ''
                for line in Filmes_Fi:
                        read_Filmes_File = read_Filmes_File + line
                        if line!='':filmes.append(line)
                if read_Filmes_File != '':
                        try: xbmcgui.Dialog().notification('A Procurar Séries (A/Z).', 'Por favor aguarde...', artfolder + 'SDPI.png', 2000, sound=False)
                        except: xbmc.executebuiltin("Notification(%s,%s, 2000, %s)" % ('A Procurar Séries (A/Z).', 'Por favor aguarde...', artfolder + 'SDPI.png'))
##                        builtin = 'XBMC.Notification(%s,%s, 2000, %s)'
##                        log = xbmc.executebuiltin(builtin % ('A Procurar Séries (A/Z).', 'Por favor aguarde...',artfolder + 'SDPI.png'))
                else:
                        try: xbmcgui.Dialog().notification('A Procurar Séries (A/Z).', 'Por favor aguarde...', artfolder + 'SDPI.png', 12000, sound=False)
                        except: xbmc.executebuiltin("Notification(%s,%s, 12000, %s)" % ('A Procurar Séries (A/Z).', 'Por favor aguarde...', artfolder + 'SDPI.png'))
##                        builtin = 'XBMC.Notification(%s,%s, 12000, %s)'
##                        log = xbmc.executebuiltin(builtin % ('A Procurar Séries (A/Z).', 'Por favor aguarde...',artfolder + 'SDPI.png'))
                try:
                        html_source = abrir_url('http://www.tuga-filmes.us')
                except: html_source = ''
                html_items_series = re.findall("<div class=\'widget Label\' id=\'Label3\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
                num_series = re.compile("<a dir=\'ltr\' href=\'(.+?)\'>(.+?)</a>").findall(html_items_series[0])
                print len(html_items_series)
                num = len(num_series) + 0.0
                for item_series in html_items_series:
                        series = re.compile("<a dir=\'ltr\' href=\'(.+?)\'>(.+?)</a>").findall(item_series)
                        for endereco_series,nome_series in series:
                                nome_series = nome_series.replace('&amp;','&')
                                nome_series = nome_series.replace('&#39;',"'")
                                nome_series = nome_series.replace('&#8217;',"'")
                                nome_series = nome_series.replace('&#8230;',"...")
                                nome_series = nome_series.replace('&#8211;',"-")
                                nome_series = nome_series.lower()
                                nome_series = nome_series.title()
                                nome_series = nome_series.replace('Agents Of S.H.I.E.L.D',"Agents Of S.H.I.E.L.D.")
                                if nome_series not in read_Filmes_File:
                                        _series.append(nome_series)
                                        _ser.append('NOME|'+nome_series+'|NOME|'+endereco_series+'|')
                                        i = i + 1
                                        a = str(i)
                                        if i < 10: a = '00'+a
                                        if i < 100 and i > 9: a = '0'+a
                                        TFV = threading.Thread(name='TFV'+str(i), target=Series_TFV, args=('FILME'+str(a)+'FILME',endereco_series,nome_series,))
                                        threads.append(TFV)
                                else: _ser.append('NOME|'+nome_series+'|NOME|'+endereco_series+'|')
                try:
                        html_source = abrir_url('http://toppt.net/')
                except: html_source = ''
                html_items_series = re.findall('<a href="http://toppt.net/category/series/">SÈRIES NOVAS</a>(.*?)<div class="clearfix">', html_source, re.DOTALL)
                for item_series in html_items_series:
                        series = re.compile('<a href="(.+?)">(.+?)</a>').findall(item_series)
                        for endereco_series,nome_series in series:
                                nome_series = nome_series.replace('&amp;','&')
                                nome_series = nome_series.replace('&#39;',"'")
                                nome_series = nome_series.replace('&#8217;',"'")
                                nome_series = nome_series.replace('&#8230;',"...")
                                nome_series = nome_series.replace('&#8211;',"-")
                                nome_series = nome_series.replace('Da Vincis Demons',"Da Vinci'S Demons")
                                nome_series = nome_series.replace('NCIS Los Angeles',"NCIS: Los Angeles")
                                nome_series = nome_series.lower()
                                nome_series = nome_series.title()
                                if nome_series not in read_Filmes_File and nome_series not in _series:
                                        _series.append(nome_series)
                                        _ser.append('NOME|'+nome_series+'|NOME|'+endereco_series+'|')
                                        i = i + 1
                                        a = str(i)
                                        if i < 10: a = '00'+a
                                        if i < 100 and i > 9: a = '0'+a
                                        TPT = threading.Thread(name='TPT'+str(i), target=Series_TPT, args=('FILME'+str(a)+'FILME',endereco_series,nome_series,))
                                        threads.append(TPT)
                                else: _ser.append('NOME|'+nome_series+'|NOME|'+endereco_series+'|')

                html_items_series = re.findall('href="http://toppt.net/category/series/">SÉRIES</a>(.*?)<div id="main">', html_source, re.DOTALL)
                for item_series in html_items_series:
                        series = re.compile('<a href="(.+?)">(.+?)</a>').findall(item_series)
                        for endereco_series,nome_series in series:
                                nome_series = nome_series.replace('&amp;','&')
                                nome_series = nome_series.replace('&#39;',"'")
                                nome_series = nome_series.replace('&#8217;',"'")
                                nome_series = nome_series.replace('&#8230;',"...")
                                nome_series = nome_series.replace('&#8211;',"-")
                                nome_series = nome_series.replace('Da Vincis Demons',"Da Vinci'S Demons")
                                nome_series = nome_series.replace('NCIS Los Angeles',"NCIS: Los Angeles")
                                nome_series = nome_series.lower()
                                nome_series = nome_series.title()
                                if nome_series not in read_Filmes_File and nome_series not in _series:
                                        _series.append(nome_series)
                                        _ser.append('NOME|'+nome_series+'|NOME|'+endereco_series+'|')
                                        i = i + 1
                                        a = str(i)
                                        if i < 10: a = '00'+a
                                        if i < 100 and i > 9: a = '0'+a
                                        TPT = threading.Thread(name='TPT'+str(i), target=Series_TPT, args=('FILME'+str(a)+'FILME',endereco_series,nome_series,))
                                        threads.append(TPT)
                                else: _ser.append('NOME|'+nome_series+'|NOME|'+endereco_series+'|')
                Filmes_Fi.close()
        except: pass
        
        for i in range(int(len(threads)/3)):
                threads[i].start()
        for i in range(int(len(threads)/3)):
                threads[i].join()

        for i in range(int(len(threads)/3),int(2*(len(threads)/3))):
                threads[i].start()
        for i in range(int(len(threads)/3),int(2*(len(threads)/3))):
                threads[i].join()

        for i in range(int(2*(len(threads)/3)),len(threads)):
                threads[i].start()
        for i in range(int(2*(len(threads)/3)),len(threads)):
                threads[i].join()
                
##        [i.start() for i in threads]
##
##        [i.join() for i in threads]

        filmes.sort()
        
        folder = perfil 
        Filmes_File = open(folder + 'Series1.txt', 'w')
        for x in range(len(filmes)):
                if filmes[x] != '':
                        Filmes_File.write(str(filmes[x]))
        Filmes_File.close()
        
##        Filmes_File = open(folder + 'S.txt', 'w')
##        _ser.sort()
##        for x in range(len(_ser)):
##                if _ser[x] != '':
##                        Filmes_File.write(str(_ser[x])+'\n')
##        Filmes_File.close()

        try:
                _sites_ = ['Series1.txt']
                folder = perfil
                num_filmes = 0
                num_filmes = len(filmes)

                for site in _sites_:
                        _filmes_ = []
                        Filmes_Fi = open(folder + site, 'r')
                        read_Filmes_File = ''
                        for line in Filmes_Fi:
                                read_Filmes_File = read_Filmes_File + line
                                if line!='':_filmes_.append(line)

                        for x in range(len(_filmes_)):
                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_filmes_[x])
                                if _n: nome = _n[0]
                                else: nome = '---'
                                _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_filmes_[x])
                                if _i: imdbcode = _i[0]
                                else: imdbcode = '---'
                                urltrailer = re.compile('IMDB.+IMDB[|](.*)').findall(imdbcode)
                                if urltrailer: urltrailer = urltrailer[0]
                                else: urltrailer = '---'
                                _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_filmes_[x])
                                if _t: thumb = _t[0]
                                else: thumb = '---'
                                _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_filmes_[x])
                                if _a: ano_filme = _a[0]
                                else: ano_filme = '---'
                                _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_filmes_[x])
                                if _f: fanart = _f[0]
                                else: fanart = ''
                                if fanart == '---': fanart = ''
                                _g = re.compile('[|]GENERO[|](.+?)[|]ONOME[|]').findall(_filmes_[x])
                                if _g: genero = _g[0]
                                else: genero = '---'
                                _o = re.compile('[|]ONOME[|](.+?)[|]SINOPSE[|]').findall(_filmes_[x])
                                if _o: O_Nome = _o[0]
                                else: O_Nome = '---'
                                _p = re.compile('PAGINA[|](.+?)[|]PAGINA').findall(_filmes_[x])
                                if _p: P_url = _p[0]
                                else: P_url = '---'
                                _s = re.compile('[|]SINOPSE[|](.*)').findall(_filmes_[x])
                                if _s: s = _s[0]
                                if '|END|' in s: sinopse = s.replace('|END|','')
                                else:
                                        si = re.compile('SINOPSE[|](.+?)\n(.+?)[|]END[|]').findall(_filmes_[x])
                                        if si: sinopse = si[0][0] + ' ' + si[0][1]
                                        else: sinopse = '---'
                                        
                                num_mode = 3006
                                
                                if nome != '---':
                                        for x in range(len(_ser)):
                                                if _ser[x] != '':
                                                        nn = re.compile('NOME[|](.+?)[|]NOME[|](.+?)[|]').findall(_ser[x])
                                                        for nm, ul in nn:
                                                                if nm == O_Nome and ul != urltrailer:
                                                                        imdbcode = imdbcode + '|' + ul
                                        #num_filmes = num_filmes + 1
                                        addDir_trailer1(nome,imdbcode,num_mode,thumb,sinopse,fanart,ano_filme,genero,O_Nome,urltrailer,'Tvshows',num_filmes)
                                xbmc.sleep(12)
                        Filmes_Fi.close()

##                num_total = num_filmes + 0.0
##                progress.create('[B][COLOR green]SITES[/COLOR][COLOR yellow]dos[/COLOR][COLOR red]PORTUGAS[/COLOR][/B]', '')
##                for a in range(num_filmes):
##                        percent = int( ( a / num_total ) * 100)
##                        message = str(a+1) + " de " + str(num_filmes)
##                        progress.update( percent, 'A Finalizar ...', message, "" )
##                        xbmc.sleep(12)
        except: pass

##        progress.close()

        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(515)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
def Series_TFV(FILMN,endereco,nome_series):
        try:
                html_source = abrir_url(endereco)
        except: html_source = ''
        items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
        if items != '':
                try:
                        item = items[0]
                        FILMEN = re.compile('FILME(.+?)FILME').findall(FILMN)
                        FILMEN = FILMEN[0]
                        #addLink(FILMEN,'','','')
                        thumb = ''
                        fanart = ''
                        imdbcode = ''
                        genre = ''
                        sinopse = ''
                        ano_filme = ''

                        imdb = re.compile('"http://www.imdb.com/title/(.+?)/"').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
                        genero = re.compile("nero</b>:(.+?)<br />").findall(item)
                        if genero: genre = genero[0]
                        else: genre = ''
                        
                        resumo = re.compile("<b>Resumo</b>:(.+?)<br />").findall(item)
                        if resumo: sinopse = resumo[0]
                        else: sinopse = ''
                        sinopse = sinopse.replace('&#8216;',"'")
                        sinopse = sinopse.replace('&#8217;',"'")
                        sinopse = sinopse.replace('&#8211;',"-")
                        sinopse = sinopse.replace('&#8220;',"'")
                        sinopse = sinopse.replace('&#8221;',"'")
                        sinopse = sinopse.replace('&#39;',"'")
                        sinopse = sinopse.replace('&amp;','&')
                        
                        ano = re.compile("<b>Ano</b>: (.+?)<br />").findall(item)
                        if ano: ano_filme = ano[0]
                        else: ano_filme = ''

                        thumbnail = re.compile('src="(.+?)"').findall(item)
                        if thumbnail: thumb = thumbnail[0]
                        else: thumb = ''
                        
                        nome_pesquisa = nome_series
                        tv_id, sinopse = thetvdb_api_IMDB()._id(nome_pesquisa,imdbcode)
                        if tv_id != '':
                                fanart = 'http://thetvdb.com/banners/fanart/original/' + tv_id + '-1.jpg'
                                try:
                                        urllib2.urlopen(fanart)
                                except urllib2.HTTPError, e:
                                        fanart = 'http://thetvdb.com/banners/fanart/original/' + tv_id + '-2.jpg'
                                if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + tv_id + '-1.jpg'
                        else:
                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme+'|'+imdbcode)
                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                if ftart:  
                                        fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                        if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                if snpse and sinopse == '': sinopse = snpse[0]

                        if genre == '': genre = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '': fanart = '---'
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        if ano_filme == '': ano_filme = '---'
                        try:
                                #addLink(nome,'','','')
                                nome_final = '[B][COLOR green]' + nome_series + '[/COLOR][/B][COLOR yellow] (' + ano_filme.replace(' ','') + ')[/COLOR]'
                                filmes.append('NOME|'+str(nome_final)+'|IMDBCODE|'+'IMDB'+str(imdbcode)+'IMDB'+'|'+endereco+'|THUMB|'+str(thumb.replace('s72-c','s320'))+'|ANO|'+str(ano_filme.replace(' ',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(genre)+'|ONOME|'+str(nome_series)+'|SINOPSE|'+str(sinopse)+'|END|\n')
                                #addDir_trailer('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',num_mode,thumb.replace('s72-c','s320'),sinopse,fanart,ano[0],genre,nome_pesquisa,urletitulo[0][0])
                        except: pass

                except: pass	
        else: pass
        filmes.sort()
        
def Series_TPT(FILMN,endereco_series,nome_series):
        try:
                html_source = abrir_url(endereco_series)
        except: html_source = ''
        items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
        if items != '':
                try:
                        FILMEN = re.compile('FILME(.+?)FILME').findall(FILMN)
                        FILMEN = FILMEN[0]
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

                        genr = re.compile("NERO:.+?/b>(.+?)<br/>").findall(items[0])
                        if genr: genero = genr[0]
                        else: genero = ''
                                        
                        ano = re.compile("<b>ANO:.+?/b>(.+?)<br/>").findall(items[0])
                        if ano: ano_filme = ano[0].replace(' ','')
                        else: ano_filme = ''

                        thumbnail = re.compile('src="(.+?)"').findall(items[0])
                        if thumbnail: thumb = thumbnail[0].replace('s72-c','s320')
                        else: thumb = ''

                        nome_pesquisa = nome_series
                        tv_id, sinopse = thetvdb_api_IMDB()._id(nome_pesquisa,imdbcode)
                        if tv_id != '':
                                fanart = 'http://thetvdb.com/banners/fanart/original/' + tv_id + '-1.jpg'
                                try:
                                        urllib2.urlopen(fanart)
                                except urllib2.HTTPError, e:
                                        fanart = 'http://thetvdb.com/banners/fanart/original/' + tv_id + '-2.jpg'
                                if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + tv_id + '-1.jpg'
                        else:
                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme+'|'+imdbcode)
                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                if ftart:  
                                        fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                        if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                if snpse and sinopse == '': sinopse = snpse[0]
                        if sinopse == '' or sinopse == '---':
                                nome_pesquisa = nome_series
                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme.replace('(','').replace(')',''))
                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                if snpse: sinopse = snpse[0]
                                                
                        ano_filme = '('+ano_filme+')'
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '': fanart = '---'
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'

                        try:
                                nome_final = '[B][COLOR green]' + nome_series+ '[/COLOR][/B][COLOR yellow] ' +ano_filme + '[/COLOR]'
                                filmes.append('NOME|'+str(nome_final)+'|IMDBCODE|'+'IMDB'+str(imdbcode)+'IMDB'+'|'+str(endereco_series)+'|THUMB|'+str(thumb)+'|ANO|'+str(ano_filme.replace('(','').replace(')',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|ONOME|'+str(nome_series)+'|SINOPSE|'+str(sinopse)+'|END|\n')
                        except: pass
                except: pass	
        else: pass
        filmes.sort()


	
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


