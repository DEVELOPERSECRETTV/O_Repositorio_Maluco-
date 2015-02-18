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


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,time,os,threading,FilmesAnima,Mashup,Funcoes,Play
from array import array
from string import capwords
from Funcoes import thetvdb_api, themoviedb_api, themoviedb_api_tv, theomapi_api, themoviedb_api_IMDB, themoviedb_api_IMDB_episodios, themoviedb_api_TMDB, thetvdb_api_IMDB
from Funcoes import thetvdb_api_tvdbid, thetvdb_api_episodes, themoviedb_api_search_imdbcode, themoviedb_api_pagina, themoviedb_api_IMDB1, theomapi_api_nome
from Funcoes import addDir, addDir1, addDir2, addLink, addLink1, addDir_teste, addDir_trailer, addDir_episode, addDir_trailer1, addDir_episode1, addDir_episode1_true
from Funcoes import get_params,abrir_url

arr_series = ['' for i in range(500)]
arrai_series = ['' for i in range(500)]
_series_ = []
_seriesALL_ = []
_series = []
_s_ = []
sri = []
filmes = []
filmesTPT = []

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
perfil = xbmc.translatePath(selfAddon.getAddonInfo('profile'))

progress = xbmcgui.DialogProgress()

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#

def TPT_MenuPrincipal(artfolder):
        try:
                url_toppt = 'http://toppt.net/'
                toppt_source = abrir_url(url_toppt)
                saber_url_todos = re.compile('<a href="(.+?)">filmes</a></li>').findall(toppt_source)
                saber_url_M18 = re.compile('<a href="(.+?)">m18</a></li>').findall(toppt_source)
                saber_url_animacao = re.compile('<a href="(.+?)">Animacao</a></li>').findall(toppt_source)
                saber_url_series = re.compile('<a href="(.+?)">Series</a></li>').findall(toppt_source)
                if not saber_url_series: saber_url_series = re.compile('<a href="(.+?)">SERIES</a></li>').findall(toppt_source)
                addDir('- Procurar','url',1,artfolder + 'P1.png','nao','')
                addDir1('[COLOR blue]Filmes:[/COLOR]','url',1001,artfolder + 'TPT1.png',False,'')
                addDir('[COLOR yellow]- Todos[/COLOR]',saber_url_todos[0],232,artfolder + 'FT.png','nao','')
                addDir('[COLOR yellow]- Animação[/COLOR]',saber_url_animacao[0],232,artfolder + 'FA.png','nao','')
                addDir('[COLOR yellow]- Por Ano[/COLOR]','url',239,artfolder + 'ANO.png','nao','')
                addDir('[COLOR yellow]- Categorias[/COLOR]','url',238,artfolder + 'CT.png','nao','')
                addDir('[COLOR yellow]- Top Filmes[/COLOR]','http://toppt.net/',232,artfolder + 'TPF.png','nao','')#258
                if selfAddon.getSetting('hide-porno') == "false":
                        addDir('[B][COLOR red]M+18[/B][/COLOR]',saber_url_M18[0],232,artfolder + 'TPT1.png','nao','')		
                addDir1('[COLOR blue]Séries:[/COLOR]','url',1001,artfolder + 'TPT1.png',False,'')
                addDir('[COLOR yellow]- A a Z[/COLOR]','urlTPT',241,artfolder + 'SAZ1.png','nao','')#241
                addDir('[COLOR yellow]- Últimos Episódios[/COLOR]',saber_url_series[0],260,artfolder + 'UE.png','nao','')#232
                addDir('[COLOR yellow]- Top Séries[/COLOR]','http://toppt.net/',232,artfolder + 'TPS.png','nao','')#259
        except:pass

def TPT_Menu_Filmes_Por_Ano(artfolder):
        ano = 2015
        for x in range(46):
                categoria_endereco = 'http://toppt.net/category/' + str(ano) + '/'
                addDir('[COLOR yellow]' + str(ano) + '[/COLOR]',categoria_endereco,232,artfolder + 'TPT1.png','nao','')
                ano = ano - 1

def TPT_Menu_Filmes_Por_Categorias(artfolder):
        conta_os_items = 0
        url_categorias = 'http://toppt.net/'
        html_categorias_source = abrir_url(url_categorias)
	html_items_categorias = re.findall('id="menu-item-15291"(.*?)id="menu-item-15290"', html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile('<a href="(.+?)">(.+?)</a>').findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        if nome_categoria != 'm18' and nome_categoria != 'FILMES':
                                nome_categoria = nome_categoria.replace('filmes ','')
                                nome_categoria = nome_categoria.lower()
                                nome_categoria = nome_categoria.title()
                                conta_os_items = conta_os_items + 1
                                addDir('[COLOR yellow]' + nome_categoria + '[/COLOR] ',endereco_categoria,232,artfolder + 'TPT1.png','nao','')


def TPT_Menu_Top_Filmes(item):
        if item != '':
                try:
                        try:
                                html_source = abrir_url(item)
                        except: html_source = ''
                        items = re.findall('<div id="content">(.*?)<span id="more', html_source, re.DOTALL)
                        if items != []:
                                urletitulo = re.compile('class="title">(.+?)<').findall(items[0])
                        try:
                                genero = ''
                                sinopse = ''
                                fanart = ''
                                thumb = ''
                                qualidade = ''
                                imdbcode = ''
                                audio_filme = ''
                                nome = urletitulo[0]
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
                                ano = re.compile("<b>ANO:.+?/b>(.+?)<br").findall(items[0])
                                imdbcode = ''
                                anofilme = ''

                                thumbnail = re.compile('src="(.+?)"').findall(items[0])
                                if thumbnail: thumb = thumbnail[0].replace('s72-c','s320')

                                imdb = re.compile('imdb.com/title/(.+?)/').findall(items[0])
                                if imdb: imdbcode = imdb[0]
                                else: imdbcode = ''
                                if ano:
                                        ano_filme = ano[0].replace(' ','')
                                        a_q = re.compile('\d+')
                                        qq_aa = a_q.findall(nome)
                                        for q_a_q_a in qq_aa:
                                                if len(q_a_q_a) == 4:
                                                        tirar_ano = '(' + str(q_a_q_a) + ')'
                                                        nome = nome.replace(tirar_ano,'')
                        
                                nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?)[:] ').findall(nome)
                                if nnnn: nome_pesquisa = nnnn[0]
                                else: nome_pesquisa = nome
                                try:
                                        fanart,tmdb_id,thu = themoviedb_api().fanart_and_id(nome_pesquisa,'')
                                        if imdbcode != '': sinopse = theomapi_api().sinopse(imdbcode)
                                except: pass

                                if genero == '':
                                        genre = '---'
                                        genero = '---'
                                if sinopse == '':
                                        plot = '---'
                                        sinopse = '---'
                                if fanart == '---': fanart = ''
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
                                #if tph == '': tph = '---'
                                addDir_trailer('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano_filme + ')[/COLOR]',item+'IMDB'+imdbcode+'IMDB',233,thumb,sinopse,fanart,ano_filme,genero,nome,item)
                                #addDir('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano_filme + ')[/COLOR]',tpe+'IMDB'+imdbcode+'IMDB',233,tph,'nao','')

                        except: pass
                except: pass


def TPT_Menu_Top_Series(item):

        if item != '':

                try:
                        try:
                                html_source = abrir_url(item)
                        except: html_source = ''
                        items = re.findall('<div id="content">(.*?)<span id="more', html_source, re.DOTALL)
                        if items != []:
                                imdb = re.compile('imdb.com/title/(.+?)/').findall(items[0])
                                if imdb: imdbcode = imdb[0]
                                else: imdbcode = ''
                                urletitulo = re.compile('class="title">(.+?)<').findall(items[0])
                                ano = re.compile("<b>ANO:.+?/b>(.+?)<br").findall(items[0])
                                if ano: ano_filme = ano[0].replace(' ','')
                                thumbnail = re.compile('src="(.+?)"').findall(items[0])
                                if thumbnail: thumb = thumbnail[0].replace('s72-c','s320')
                        try:
                                genero = ''
                                sinopse = ''
                                fanart = ''
                                thumb = ''
                                qualidade = ''
                                imdbcode = ''
                                audio_filme = ''
                                nome = urletitulo[0]
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
                                
                                n = re.compile('(.+?)[[].+?[]]').findall(nome)
                                if n: nome_pesquisa = n[0]
                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme)
                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                if ftart:
                                        fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                        if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                if snpse: sinopse = snpse[0]
##                                fanart,tmdb_id,thumb = themoviedb_api_tv().fanart_and_id(nome_pesquisa,ano_filme)
##                                thp = thumb
                                if imdbcode == '': imdbcode = themoviedb_api_search_imdbcode().fanart_and_id(nome_pesquisa,ano_filme)
                                if genero == '':
                                        genre = '---'
                                        genero = '---'
                                if sinopse == '':
                                        plot = '---'
                                        sinopse = '---'
                                if fanart == '---': fanart = ''
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
                                addDir_trailer('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano_filme + ')[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',item+'IMDB'+imdbcode+'IMDB',233,thumb,sinopse,fanart,ano_filme.replace('(','').replace(')',''),genero,nome_pesquisa,item)
                        except: pass
                except: pass



def TPT_Menu_Series_A_a_Z(artfolder,url):
        
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
                
                try: Filmes_Fi = open(folder + 'SeriesTPT1.txt', 'r')
                except:
                        Filmes_File = open(folder + 'SeriesTPT1.txt', 'a')
                        Filmes_File.close()
                        Filmes_Fi = open(folder + 'SeriesTPT1.txt', 'r')
                read_Filmes_File = ''
                for line in Filmes_Fi:
                        read_Filmes_File = read_Filmes_File + line
                        if line!='':filmes.append(line)

                if read_Filmes_File != '':
                        try: xbmcgui.Dialog().notification('A Procurar Séries (A/Z).', 'Por favor aguarde...', artfolder + 'TPT1.png', 2000, sound=False)
                        except: xbmc.executebuiltin("Notification(%s,%s, 2000, %s)" % ('A Procurar Séries (A/Z).', 'Por favor aguarde...', artfolder + 'TPT1.png'))
                else:
                        try: xbmcgui.Dialog().notification('A Procurar Séries (A/Z).', 'Por favor aguarde...', artfolder + 'TPT1.png', 12000, sound=False)
                        except: xbmc.executebuiltin("Notification(%s,%s, 12000, %s)" % ('A Procurar Séries (A/Z).', 'Por favor aguarde...', artfolder + 'TPT1.png'))

                try:
                        html_source = abrir_url('http://toppt.net/')
                except: html_source = ''
                html_items_series = re.findall('<a href="http://toppt.net/category/series/">SÈRIES NOVAS</a>(.*?)<div class="clearfix">', html_source, re.DOTALL)
                for item_series in html_items_series:
                        series = re.compile('<a href="(.+?)">(.+?)</a>').findall(item_series)
                        for endereco_series,nome_series in series:
                                if endereco_series not in read_Filmes_File:
                                        nome_series = nome_series.replace('&amp;','&')
                                        nome_series = nome_series.replace('&#39;',"'")
                                        nome_series = nome_series.replace('&#8217;',"'")
                                        nome_series = nome_series.replace('&#8230;',"...")
                                        nome_series = nome_series.replace('&#8211;',"-")
                                        nome_series = nome_series.replace('Da Vincis Demons',"Da Vinci'S Demons")
                                        nome_series = nome_series.replace('NCIS Los Angeles',"NCIS: Los Angeles")
                                        nome_series = nome_series.lower()
                                        nome_series = nome_series.title()
                                        _series.append(endereco_series)
                                        i = i + 1
                                        a = str(i)
                                        if i < 10: a = '00'+a
                                        if i < 100 and i > 9: a = '0'+a
                                        TPT = threading.Thread(name='TPT'+str(i), target=Series_TPT, args=('FILME'+str(a)+'FILME',endereco_series,nome_series,))
                                        threads.append(TPT)
                html_items_series = re.findall('href="http://toppt.net/category/series/">SÉRIES</a>(.*?)<div id="main">', html_source, re.DOTALL)
                for item_series in html_items_series:
                        series = re.compile('<a href="(.+?)">(.+?)</a>').findall(item_series)
                        for endereco_series,nome_series in series:
                                if endereco_series not in read_Filmes_File and endereco_series not in _series:
                                        nome_series = nome_series.replace('&amp;','&')
                                        nome_series = nome_series.replace('&#39;',"'")
                                        nome_series = nome_series.replace('&#8217;',"'")
                                        nome_series = nome_series.replace('&#8230;',"...")
                                        nome_series = nome_series.replace('&#8211;',"-")
                                        nome_series = nome_series.replace('Da Vincis Demons',"Da Vinci'S Demons")
                                        nome_series = nome_series.replace('NCIS Los Angeles',"NCIS: Los Angeles")
                                        nome_series = nome_series.lower()
                                        nome_series = nome_series.title()
                                        _series.append(endereco_series)
                                        i = i + 1
                                        a = str(i)
                                        if i < 10: a = '00'+a
                                        if i < 100 and i > 9: a = '0'+a
                                        TPT = threading.Thread(name='TPT'+str(i), target=Series_TPT, args=('FILME'+str(a)+'FILME',endereco_series,nome_series,))
                                        threads.append(TPT)
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
        Filmes_File = open(folder + 'SeriesTPT1.txt', 'w')
        for x in range(len(filmes)):
                if filmes[x] != '':
                        Filmes_File.write(str(filmes[x]))
        Filmes_File.close()

        try:
                _sites_ = ['SeriesTPT1.txt']
                folder = perfil
                num_filmes = 0
                
                for site in _sites_:
                        _filmes_ = []
                        Filmes_Fi = open(folder + site, 'r')
                        read_Filmes_File = ''
                        for line in Filmes_Fi:
                                read_Filmes_File = read_Filmes_File + line
                                if line!='':_filmes_.append(line)
                        num_filmes = len(_filmes_)
                        for x in range(len(_filmes_)):
                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_filmes_[x])
                                if _n: nome = _n[0]
                                else: nome = '---'
                                _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_filmes_[x])
                                if _i: imdbcode = _i[0]
                                else: imdbcode = '---'
                                urltrailer = re.compile('IMDB.+?MDB[|](.+?)[|]THUMB[|]').findall(imdbcode)
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
                                        #num_filmes = num_filmes + 1
                                        addDir_trailer1(nome,imdbcode,num_mode,thumb,sinopse,fanart,ano_filme,genero,O_Nome,urltrailer,'TVshows',num_filmes)
                                xbmc.sleep(20)
                        Filmes_Fi.close()

##                num_total = num_filmes + 0.0
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

                        genr = re.compile("NERO:.+?/b>(.+?)<br").findall(items[0])
                        if genr: genero = genr[0]
                        else: genero = ''
                                        
                        ano = re.compile("<b>ANO:.+?/b>(.+?)<br").findall(items[0])
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
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#

def TPT_encontrar_fontes_filmes(url):
        
##        percent = 0
##        message = 'Por favor aguarde.'
##        progress.create('Progresso', 'A Procurar')
        if name == '[COLOR yellow]- Top Séries[/COLOR]' or name == '[COLOR yellow]- Top Filmes[/COLOR]':
                try: xbmcgui.Dialog().notification('A Procurar.', 'Por favor aguarde...', artfolder + 'TPT1.png', 2000, sound=False)
                except: xbmc.executebuiltin("Notification(%s,%s, 2000, %s)" % ('A Procurar.', 'Por favor aguarde...', artfolder + 'TPT1.png'))
##                progress.update( percent, 'A Procurar ...', message, "" )
        if name == '[COLOR yellow]- Últimos Episódios[/COLOR]' or name == '[B]Página Seguinte>>[/B]':
                try: xbmcgui.Dialog().notification('A Procurar Últimos Episódios.', 'Por favor aguarde...', artfolder + 'TPT1.png', 2000, sound=False)
                except: xbmc.executebuiltin("Notification(%s,%s, 2000, %s)" % ('A Procurar Últimos Episódios.', 'Por favor aguarde...', artfolder + 'TPT1.png'))
##                progress.update( percent, 'A Procurar Últimos Episódios ...', message, "" )
        if name != '[COLOR yellow]- Top Séries[/COLOR]' and name != '[COLOR yellow]- Top Filmes[/COLOR]' and name != '[COLOR yellow]- Últimos Episódios[/COLOR]' and name != '[B]Página Seguinte>>[/B]':
                try: xbmcgui.Dialog().notification('A Procurar Filmes.', 'Por favor aguarde...', artfolder + 'TPT1.png', 2000, sound=False)
                except: xbmc.executebuiltin("Notification(%s,%s, 2000, %s)" % ('A Procurar Filmes.', 'Por favor aguarde...', artfolder + 'TPT1.png'))
##                progress.update( percent, 'A Procurar Filmes ...', message, "" )
        
        try:
		html_source = abrir_url(url)
	except: html_source = ''
	if name != '[COLOR yellow]- Top Séries[/COLOR]' and name != '[COLOR yellow]- Top Filmes[/COLOR]':
                items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
        if name == '[COLOR yellow]- Top Séries[/COLOR]':
                tp_series = re.findall('<h3 class="widgettitle">TOP SÉRIES</h3>(.+?)<ul class="widget-container">', html_source, re.DOTALL)
                items = re.compile('<a href="(.+?)".+?<img.+?src=".+?"').findall(tp_series[0])
        if name == '[COLOR yellow]- Top Filmes[/COLOR]':
                tp_filmes = re.findall('<h3 class="widgettitle">TOP FILMES</h3>(.+?)<ul class="widget-container">', html_source, re.DOTALL)
                items = re.compile('<a href="(.+?)".+?<img.+?src=".+?"').findall(tp_filmes[0])

        threads = []
        i = 0
        for item in items:
                if name != '[COLOR yellow]- Top Séries[/COLOR]' and name != '[COLOR yellow]- Top Filmes[/COLOR]':
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        Filmes_TPT = threading.Thread(name='Filmes_TPT'+str(i), target=Fontes_Filmes_TPT , args=('FILME'+str(a)+'FILME'+item,))
                if name == '[COLOR yellow]- Top Séries[/COLOR]':
                        Filmes_TPT = threading.Thread(name='Filmes_TPT'+str(i), target=TPT_Menu_Top_Series , args=(item,))
                if name == '[COLOR yellow]- Top Filmes[/COLOR]':
                        Filmes_TPT = threading.Thread(name='Filmes_TPT'+str(i), target=TPT_Menu_Top_Filmes , args=(item,))
                threads.append(Filmes_TPT)

        [i.start() for i in threads]

        [i.join() for i in threads]

        if name != '[COLOR yellow]- Top Séries[/COLOR]' and name != '[COLOR yellow]- Top Filmes[/COLOR]':
                _sites_ = ['filmesTPT.txt']
                folder = perfil
                num_filmes = 0
                num_filmes = len(threads)
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
                                urltrailer = re.compile('(.+?)IMDB.+?MDB').findall(imdbcode)
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
                                        
                                if 'toppt.net'         in imdbcode: num_mode = 233
                                
                                if nome != '---':
                                        #num_filmes = num_filmes + 1
                                        addDir_trailer1(nome,imdbcode,num_mode,thumb,sinopse,fanart,ano_filme,genero,O_Nome,urltrailer,'Movies',num_filmes)
                                xbmc.sleep(20)
                        Filmes_Fi.close()

##                num_total = num_filmes + 0.0
##                for a in range(num_filmes):
##                        percent = int( ( a / num_total ) * 100)
##                        message = str(a+1) + " de " + str(num_filmes)
##                        progress.update( percent, 'A Finalizar ...', message, "" )
##                        xbmc.sleep(20)

                proxima = re.compile('</span><a class="nextpostslink" rel="next" href="(.+?)">&raquo;</a><a class="last"').findall(html_source)
                try:
                        if name == '[COLOR yellow]- Últimos Episódios[/COLOR]' or name == '[B]Página Seguinte>>[/B]':
                                addDir("Página Seguinte>>",proxima[0].replace('#038;','').replace('&amp;','&'),232,artfolder + 'PAGS1.png','','')
                        else:
                                addDir("Página Seguinte >>",proxima[0].replace('#038;','').replace('&amp;','&'),232,artfolder + 'PAGS1.png','','')
                except:pass

##	progress.close()

def Fontes_Filmes_TPT(item):

        series = 0
        folder = perfil
        Filmes_File = open(folder + 'filmesTPT.txt', 'w')
        
        if item != '':
                try:
                        FILMEN = re.compile('FILME(.+?)FILME').findall(item)
                        FILMEN = FILMEN[0]
                        sinopse = ''
                        fanart = ''
                        thumb = ''
                        genero = ''
                        qualidade = ''
                        audio_filme = ''
                        imdbcode = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
                        urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(item)
                        if 'title=' in urletitulo[0][0]: urletitulo = re.compile('<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>').findall(item)
                        
                        qualid = re.compile("<b>QUALIDADE:.+?/b>(.+?)<br/>").findall(item)
                        if not qualid: qualid = re.compile("<b>VERSÃO:.+?</b>(.+?)<br").findall(item)
                        if qualid:
                                qualidade = qualid[0]
                                qualidade = qualidade.replace('[',' - ')
                                qualidade = qualidade.replace(']','')
                        else:
                                qualid = re.compile("\nQUALIDADE:\xc2\xa0(.+?)<br").findall(item)
                                if qualid:
                                        qualidade = qualid[0]
                                        qualidade = qualidade.replace('[',' - ')
                                        qualidade = qualidade.replace(']','')
                                else:
                                        qualid = re.compile("<b>VERS.+?</b>(.+?)<br").findall(item)
                                        if qualid:
                                                qualidade = qualid[0]
                                                qualidade = qualidade.replace('[',' - ')
                                                qualidade = qualidade.replace(']','')
                                        else:
                                                qualidade = ''
                                        
                        genr = re.compile("NERO:.+?/b>(.+?)<br/>").findall(item)
                        if genr: genero = genr[0]
                        
                        ano = re.compile("<b>ANO:.+?/b>(.+?)<br").findall(item)
                        audio = re.compile("<b>AUDIO:.+?/b>(.+?)<br").findall(item)
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
                                        
                        ###############################
                                        
                        if 'Temporada' in nome or 'Season' in nome or 'Mini-Série' in nome  or 'Mini-Serie' in nome:
                                n = re.compile('(.+?)[[].+?[]]').findall(nome)
                                if n: nome_pesquisa = n[0]
                                try:
                                        thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme)
                                        ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                        if ftart:
                                                fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'                                       
                                        snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                        if snpse: sinopse = snpse[0]
                                except: pass
                        else:
                                nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?)[:] ').findall(nome)
                                if nnnn: nome_pesquisa = nnnn[0]
                                else: nome_pesquisa = nome
                                try:
                                        fanart,tmdb_id,poster,sinopse = themoviedb_api_IMDB().fanart_and_id(str(imdbcode),ano_filme)
##                                fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano_filme)
                                        if thumb == '': thumb = poster
                                except: pass
                        #################################

                        ano_filme = '('+ano_filme+')'
                        qualidade = '('+qualidade
                        audio_filme = audio_filme+')'
                        if series == 1:
                                n = re.compile('[[](.+?)[]][[](.+?)[]]').findall(nome)
                                if not n: n = re.compile('[[](.+?)[]] [[](.+?)[]]').findall(nome)
                                if n: nome = n[0][0]+' - '+n[0][1]
                                else:
                                        n = re.compile('[(](.+?)[)][(](.+?)[)]').findall(nome)
                                        if not n: n = re.compile('[(](.+?)[)] [(](.+?)[)]').findall(nome)
                                        if n: nome = n[0][0]+' - '+n[0][1]
                                        else:
                                                n = re.compile('[[](.+?)[]]').findall(nome)
                                                if n: nome = n[0]
                                                else:
                                                        n = re.compile('[(](.+?)[)]').findall(nome)
                                                        if n: nome = n[0]
                                qualidade = ''
                                ano_filme = ''
                                audio_filme = ''
                        #addLink(nome,'','','')        
                        try:
                                if genero == '':
                                        genre = '---'
                                        genero = '---'
                                if sinopse == '':
                                        plot = '---'
                                        sinopse = '---'
                                if fanart == '---': fanart = ''
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
                                nome_final = '[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' +ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]'
                                filmes.append(FILMEN+'NOME|'+str(nome_final)+'|IMDBCODE|'+str(urletitulo[0][0])+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb)+'|ANO|'+str(ano_filme.replace('(','').replace(')',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|ONOME|'+str(nome_pesquisa)+'|SINOPSE|'+str(sinopse)+'|END|\n')
##                                addDir_trailer('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',233,thumb,sinopse,fanart,ano_filme.replace('(','').replace(')',''),genero,nome_pesquisa,urletitulo[0][0])
                                #addDir_teste('[B][COLOR green]' + n1 + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]'+'[COLOR nnn]'+n2+'[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',233,thumb,sinopse,fanart,ano_filme.replace('(','').replace(')',''),genero)
                        except: pass
                except: pass	
        else: pass
        filmes.sort()
        for x in range(len(filmes)):
                Filmes_File.write(str(filmes[x]))
	Filmes_File.close()



#----------------------------------------------------------------------------------------------------------------------------------------------#
                
def TPT_encontrar_videos_filmes(name,url,iconimage,mvoutv):
##        addLink(mvoutv,'','','')
##        return
        if 'Season' in name or 'Temporada' in name or 'Mini-Série' in name or 'Mini-serie' in name or 'Minisérie' in name or 'Miniserie' in name:
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
                if temporada == '':
                        temporada = '0'
                        temporadat = '0'
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

                tvdbid = thetvdb_api_tvdbid()._id(n_pesquisa,anne)
                #addLink(temporadat+'-'+anne+'-'+n_pesquisa,'','')
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
        #return
        if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                num = 0
                percent = 0
                message = ''
                progress.create('Progresso', 'A Procurar episódios...')
                progress.update( percent, "", message, "" )
        else:
                if mvoutv == 'MoviesTPT':
                        try: xbmcgui.Dialog().notification('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png', 3000, sound=False)
                        except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % ('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png'))
                else:
                        try: xbmcgui.Dialog().notification('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png', 10000, sound=False)
                        except: xbmc.executebuiltin("Notification(%s,%s, 10000, %s)" % ('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png'))
##                site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
##                message = 'Por favor aguarde.'
##                percent = 0
##                progress.create('Progresso', 'A Procurar...')
##                progress.update(percent, 'A Procurar em '+site, message, "")
        i = 1
        conta_id_video = 0
        contaultimo = 0
        ##############################################
        n1 = ''
        n2 = ''

        if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo and 'Mini-serie' not in nometitulo and 'Minisérie' not in nometitulo and 'Miniserie' not in nometitulo:
                nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(nomeescolha)
                nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
                nnnn = re.compile('(.+?)[(](.+?)[)]').findall(nnn[0])
                if nnnn:
                        n2 = nnnn[0][0]
                        n1 = nnnn[0][1]
                if not nnnn:
                        nnnn = re.compile('(.+?)[[](.+?)[]]').findall(nnn[0])
                        if nnnn:
                                n2 = nnnn[0][0]
                                n1 = nnnn[0][1]        
                if not nnnn:
                        nnnn = re.compile('(.+?) [-] ').findall(nnn[0])
                        if nnnn:
                                n2 = nnnn[0]
                if not nnnn:
                        nnnn = re.compile('(.+?)[:] ').findall(nnn[0])
                        if nnnn:
                                n2 = nnnn[0]
                if not nnnn : n2 = nnn[0]

        ###############################################
        if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo and 'Mini-serie' not in nometitulo and 'Minisérie' not in nometitulo and 'Miniserie' not in nometitulo:
                if n1 != '' and n2 != '':
                        addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n2,'url',1004,iconimage,False,fanart)
                        addDir('[COLOR yellow]PROCURAR POR: [/COLOR]'+n1,'IMDB'+imdbcode+'IMDB',7,iconimage,'',fanart)
                else:
                        addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n2,'url',1004,iconimage,False,fanart)
       
        if 'Season' not in name and 'Temporada' not in name and 'Mini-Série' not in name and 'Mini-Serie' not in name and 'Minisérie' not in name and 'Miniserie' not in name:
                addDir1(name,'url',1004,iconimage,False,fanart)
        #addDir(name+url,'url',9999,iconimage,'',fanart)
        l= 0
	try:
		link2=abrir_url(url)
	except: link2 = ''
	if link2:
                if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo and 'Mini-serie' not in nometitulo and 'Minisérie' not in nometitulo and 'Miniserie' not in nometitulo and imdbcode == '':
                        items = re.findall('<div class="postmeta-primary">(.*?)<div id="sidebar-primary">', link2, re.DOTALL)
                        if items != []:
                                imdb = re.compile('imdb.com/title/(.+?)/').findall(items[0])
                                if imdb: imdbcode = imdb[0]
                                else: imdbcode = ''
                if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo and 'Mini-serie' not in nometitulo and 'Minisérie' not in nometitulo and 'Miniserie' not in nometitulo:
                        newmatch = re.findall('<span id=.+?DOWNLOAD POR',link2,re.DOTALL)
                        if not newmatch: newmatch = re.findall('<span id=.+?BAIXAR',link2,re.DOTALL)
                        l=1
                else:
                        #newmatch = re.findall('<span id=.+?<img style="height: 40px; width: 465px;"',link2,re.DOTALL)
                        newmatch1 = re.findall('<span id=.+?DOWNLOAD POR',link2,re.DOTALL)
                        if not newmatch1: newmatch1 = re.findall('<span id=.+?BAIXAR',link2,re.DOTALL)
                        newmatch = re.findall('<img style="height: 90px; width: 200px;".+?DOWNLOAD POR',link2,re.DOTALL)
                        if not newmatch: newmatch = re.findall('<img style="height: 90px; width: 200px;".+?BAIXAR',link2,re.DOTALL)
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
                #if not newmatch:addDir1(str(l),'url',1001,iconimage,False,'')
                if not newmatch:
                        if newmatch1 != [] and 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                lin = re.findall('.+?EPIS',newmatch1[0],re.DOTALL)
                                #addDir1(str(l),'url',1001,iconimage,False,'')
                                num = len(lin) + 0.0 - 1
                                #linkseriesssss = re.findall('</span>CLIQUE AQUI PARA VER O (.+?)</div>(.+?)</div></div><',newmatch1[0],re.DOTALL)
                                linkseriesssss = re.findall('<span class="su-spoiler-icon"></span>(.+?)</div>(.+?)BAIXAR',link2,re.DOTALL)
##                                if not linkseriesssss: linkseriesssss = re.findall('<h2>(.+?)</h2>\n(.+?)DOWNLOAD POR',newmatch1[0],re.DOTALL)
##                                if not linkseriesssss: linkseriesssss = re.findall('<h2>(.+?)</h2>(.+?)BAIXAR',newmatch1[0],re.DOTALL)
                                for parte1,parte2 in linkseriesssss:                                        
                                        
                                        try:
                                                episodio = re.compile('(\d+)').findall(parte1)
                                                if episodio:
                                                        episodiot = episodio[0]
                                                        episodio = episodio[0]
                                                a_q = re.compile('\d+')
                                                qq_aa = a_q.findall(episodio)
                                                for q_a_q_a in qq_aa:
                                                        if len(q_a_q_a) == 1:
                                                                episodiot = '%02d' % int(episodio)#'0'+episodio
                                        except: pass
                                        
                                                
                                        try:
                                                epi_nome,air,sin,th = thetvdb_api_episodes()._id(str(tvdbid),str(temporada),str(episodio))
                                                iconimage = th
                                        except: pass
                                        conta_id_video = 0
                                        
##                                        match = re.compile('<span class="su-lightbox" data-mfp-src="(.+?)" data-mfp-type="iframe">').findall(parte2)
##                                        for url in match:
##                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
##                                                        conta_id_video = conta_id_video + 1
##                                                        conta_os_items = conta_os_items + 1
##                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
##                                                        if f_id == '': f_id = fonte_id
##                                                        else: f_id = f_id + '|' + fonte_id
                                        match = re.compile('src="(.+?)"').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                        if f_id == '': f_id = fonte_id
                                                        else: f_id = f_id + '|' + fonte_id
                                        
                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                        if f_id == '': f_id = fonte_id
                                                        else: f_id = f_id + '|' + fonte_id
                                        match = re.compile('SRC="(.+?)"').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                        if f_id == '': f_id = fonte_id
                                                        else: f_id = f_id + '|' + fonte_id
                                        try:
                                                if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                        percent = int( ( i / num ) * 100)
                                                        message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]'
                                                        progress.update( percent, "", message, "" )
                                                        print str(i) + " de " + str(int(num))
                                                        
                                                        if progress.iscanceled():
                                                                break
                                                #episod = episodiot
                                                #label = temporada + 'x' + '%02d' % int(episodiot) + ' . ' + epi_nome
                                                mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                        except:
                                                if 'EPI' not in parte1 and 'Epi' not in parte1: parte1 = parte1+'ºEPISÓDIO'
                                                if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                        percent = int( ( i / num ) * 100)
                                                        message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]'
                                                        progress.update( percent, "", message, "" )
                                                        print str(i) + " de " + str(int(num))
                                                        
                                                        if progress.iscanceled():
                                                                break
                                                mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)

                                        f_id = ''
                                        i = i + 1
        
                                linkseriesssss = re.findall('<h2></h2>.+?<h2>(.+?)EPIS.+?</h2>\n(.+?)DOWNLOAD POR',link2,re.DOTALL)
                                
                                for parte1,parte2 in linkseriesssss:                                        
                                        
                                        try:
                                                episodio = re.compile('(\d+)').findall(parte1)
                                                if episodio:
                                                        episodiot = episodio[0]
                                                        episodio = episodio[0]
                                                a_q = re.compile('\d+')
                                                qq_aa = a_q.findall(episodio)
                                                for q_a_q_a in qq_aa:
                                                        if len(q_a_q_a) == 1:
                                                                episodiot = '%02d' % int(episodio)#'0'+episodio
                                        except: pass
                                        #addLink(parte1,'','','')
                                                
                                        try:
                                                epi_nome,air,sin,th = thetvdb_api_episodes()._id(str(tvdbid),str(temporada),str(episodio))
                                                iconimage = th
                                        except: pass
                                        conta_id_video = 0
                                        
##                                        match = re.compile('<span class="su-lightbox" data-mfp-src="(.+?)" data-mfp-type="iframe">').findall(parte2)
##                                        for url in match:
##                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
##                                                        conta_id_video = conta_id_video + 1
##                                                        conta_os_items = conta_os_items + 1
##                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
##                                                        if f_id == '': f_id = fonte_id
##                                                        else: f_id = f_id + '|' + fonte_id
                                        match = re.compile('src="(.+?)"').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                        if f_id == '': f_id = fonte_id
                                                        else: f_id = f_id + '|' + fonte_id
                                        
                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                        if f_id == '': f_id = fonte_id
                                                        else: f_id = f_id + '|' + fonte_id
                                        match = re.compile('SRC="(.+?)"').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                        if f_id == '': f_id = fonte_id
                                                        else: f_id = f_id + '|' + fonte_id
                                        try:
                                                if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                        percent = int( ( i / num ) * 100)
                                                        message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]'
                                                        progress.update( percent, "", message, "" )
                                                        print str(i) + " de " + str(int(num))
                                                        
                                                        if progress.iscanceled():
                                                                break
                                                #episod = episodiot
                                                #label = temporada + 'x' + '%02d' % int(episodiot) + ' . ' + epi_nome
                                                mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                        except:
                                                if 'EPI' not in parte1 and 'Epi' not in parte1: parte1 = parte1+'ºEPISÓDIO'
                                                if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                        percent = int( ( i / num ) * 100)
                                                        message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]'
                                                        progress.update( percent, "", message, "" )
                                                        print str(i) + " de " + str(int(num))
                                                        
                                                        if progress.iscanceled():
                                                                break
                                                mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)

                                        f_id = ''
                                        i = i + 1
                                #linkseriesssss = re.findall('</span>CLIQUE AQUI PARA VER O (.+?)</div>(.+?)</div></div><',newmatch1[0],re.DOTALL)
                                #linkseriesssss = re.findall('<span class="su-spoiler-icon"></span>(.+?)</div>(.+?)BAIXAR',newmatch1[0],re.DOTALL)
                                #linkseriesssss = re.findall('<h2>(.+?)</h2>\n(.+?)DOWNLOAD POR',newmatch1[0],re.DOTALL)
                                linkseriesssss = re.findall('<h2>(.+?)</h2>(.+?)BAIXAR',link2,re.DOTALL)
                                for parte1,parte2 in linkseriesssss:                                        
                                        
                                        try:
                                                episodio = re.compile('(\d+)').findall(parte1)
                                                if episodio:
                                                        episodiot = episodio[0]
                                                        episodio = episodio[0]
                                                a_q = re.compile('\d+')
                                                qq_aa = a_q.findall(episodio)
                                                for q_a_q_a in qq_aa:
                                                        if len(q_a_q_a) == 1:
                                                                episodiot = '%02d' % int(episodio)#'0'+episodio
                                        except: pass
                                        
                                                
                                        try:
                                                epi_nome,air,sin,th = thetvdb_api_episodes()._id(str(tvdbid),str(temporada),str(episodio))
                                                iconimage = th
                                        except: pass
                                        conta_id_video = 0
                                        
##                                        match = re.compile('<span class="su-lightbox" data-mfp-src="(.+?)" data-mfp-type="iframe">').findall(parte2)
##                                        for url in match:
##                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
##                                                        conta_id_video = conta_id_video + 1
##                                                        conta_os_items = conta_os_items + 1
##                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
##                                                        if f_id == '': f_id = fonte_id
##                                                        else: f_id = f_id + '|' + fonte_id
                                        match = re.compile('src="(.+?)"').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                        if f_id == '': f_id = fonte_id
                                                        else: f_id = f_id + '|' + fonte_id
                                        
                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                        if f_id == '': f_id = fonte_id
                                                        else: f_id = f_id + '|' + fonte_id
                                        match = re.compile('SRC="(.+?)"').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                        if f_id == '': f_id = fonte_id
                                                        else: f_id = f_id + '|' + fonte_id
                                        try:
                                                if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                        percent = int( ( i / num ) * 100)
                                                        message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]'
                                                        progress.update( percent, "", message, "" )
                                                        print str(i) + " de " + str(int(num))
                                                        
                                                        if progress.iscanceled():
                                                                break
                                                #episod = episodiot
                                                #label = temporada + 'x' + '%02d' % int(episodiot) + ' . ' + epi_nome
                                                mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                        except:
                                                if 'EPI' not in parte1 and 'Epi' not in parte1: parte1 = parte1+'ºEPISÓDIO'
                                                if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                        percent = int( ( i / num ) * 100)
                                                        message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]'
                                                        progress.update( percent, "", message, "" )
                                                        print str(i) + " de " + str(int(num))
                                                        
                                                        if progress.iscanceled():
                                                                break
                                                mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)

                                        f_id = ''
                                        i = i + 1
                                linkseriesssss = re.findall('</span>CLIQUE AQUI PARA VER O (.+?)</div>(.+?)</div></div><',link2,re.DOTALL)
                                #linkseriesssss = re.findall('<span class="su-spoiler-icon"></span>(.+?)</div>(.+?)BAIXAR',newmatch1[0],re.DOTALL)
                                #linkseriesssss = re.findall('<h2>(.+?)</h2>\n(.+?)DOWNLOAD POR',newmatch1[0],re.DOTALL)
                                #linkseriesssss = re.findall('<h2>(.+?)</h2>(.+?)BAIXAR',newmatch1[0],re.DOTALL)
                                for parte1,parte2 in linkseriesssss:                                        
                                        
                                        try:
                                                episodio = re.compile('(\d+)').findall(parte1)
                                                if episodio:
                                                        episodiot = episodio[0]
                                                        episodio = episodio[0]
                                                a_q = re.compile('\d+')
                                                qq_aa = a_q.findall(episodio)
                                                for q_a_q_a in qq_aa:
                                                        if len(q_a_q_a) == 1:
                                                                episodiot = '%02d' % int(episodio)#'0'+episodio
                                        except: pass
                                        
                                                
                                        try:
                                                epi_nome,air,sin,th = thetvdb_api_episodes()._id(str(tvdbid),str(temporada),str(episodio))
                                                iconimage = th
                                        except: pass
                                        conta_id_video = 0
                                        
##                                        match = re.compile('<span class="su-lightbox" data-mfp-src="(.+?)" data-mfp-type="iframe">').findall(parte2)
##                                        for url in match:
##                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
##                                                        conta_id_video = conta_id_video + 1
##                                                        conta_os_items = conta_os_items + 1
##                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
##                                                        if f_id == '': f_id = fonte_id
##                                                        else: f_id = f_id + '|' + fonte_id
                                        match = re.compile('src="(.+?)"').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                        if f_id == '': f_id = fonte_id
                                                        else: f_id = f_id + '|' + fonte_id
                                        
                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                        if f_id == '': f_id = fonte_id
                                                        else: f_id = f_id + '|' + fonte_id
                                        match = re.compile('SRC="(.+?)"').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                        if f_id == '': f_id = fonte_id
                                                        else: f_id = f_id + '|' + fonte_id
                                        try:
                                                if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                        percent = int( ( i / num ) * 100)
                                                        message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]'
                                                        progress.update( percent, "", message, "" )
                                                        print str(i) + " de " + str(int(num))
                                                        
                                                        if progress.iscanceled():
                                                                break
                                                #episod = episodiot
                                                #label = temporada + 'x' + '%02d' % int(episodiot) + ' . ' + epi_nome
                                                mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                        except:
                                                if 'EPI' not in parte1 and 'Epi' not in parte1: parte1 = parte1+'ºEPISÓDIO'
                                                if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                        percent = int( ( i / num ) * 100)
                                                        message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]'
                                                        progress.update( percent, "", message, "" )
                                                        print str(i) + " de " + str(int(num))
                                                        
                                                        if progress.iscanceled():
                                                                break
                                                mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)

                                        f_id = ''
                                        i = i + 1
                                
                if newmatch:
                        if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo and 'Mini-serie' not in nometitulo and 'Minisérie' not in nometitulo and 'Miniserie' not in nometitulo:
                                match = re.compile('<span class="su-lightbox" data-mfp-src="(.+?)" data-mfp-type="iframe">').findall(newmatch[0])
                                if not match: match = re.compile('src="(.+?)"').findall(newmatch[0])
                                #addLink(str(len(match)),'','','')
                                for url in match:
                                        #addLink(url,'','','')
                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                        
                                        try:
                                                episodio = re.compile('(\d+)').findall(parte1)
                                                if episodio:
                                                        episodiot = episodio[0]
                                                        episodio = episodio[0]
                                                a_q = re.compile('\d+')
                                                qq_aa = a_q.findall(episodio)
                                                for q_a_q_a in qq_aa:
                                                        if len(q_a_q_a) == 1:
                                                                episodiot = '0'+episodio
                                        except: pass
                                                
                                        #addLink(temporada+'-'+episodio+'-'+imdbcode+'-'+tmdbcode,'','')
                                        
                                        try:
                                                epi_nome,air,sin,th = thetvdb_api_episodes()._id(str(tvdbid),str(temporada),str(episodio))
                                                iconimage = th
                                        except: pass
                                        
                                        conta_id_video = 0
                                        #addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]','','',iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                        match = re.compile('<span class="su-lightbox" data-mfp-src="(.+?)" data-mfp-type="iframe">').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                        if f_id == '': f_id = fonte_id
                                                        else: f_id = f_id + '|' + fonte_id
                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                        if f_id == '': f_id = fonte_id
                                                        else: f_id = f_id + '|' + fonte_id
                                        try:
                                                if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                        percent = int( ( i / num ) * 100)
                                                        message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]'
                                                        progress.update( percent, "", message, "" )
                                                        print str(i) + " de " + str(int(num))
                                                        
                                                        if progress.iscanceled():
                                                                break
                                                mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                        except:
                                                if 'EPI' not in parte1 and 'Epi' not in parte1: parte1 = parte1+'ºEPISÓDIO'
                                                if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                        percent = int( ( i / num ) * 100)
                                                        message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]'
                                                        progress.update( percent, "", message, "" )
                                                        print str(i) + " de " + str(int(num))
                                                        
                                                        if progress.iscanceled():
                                                                break
                                                mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                        f_id = ''
                                        i = i + 1
			linksseccaopartes = re.findall('.+?PARTE',newmatch[0],re.DOTALL)
			if linksseccaopartes:
                                if len(linksseccaopartes) > 1:
                                        linksseccao = re.findall('RTE(.+?)<.+?>\n(.+?)>PA',newmatch[0],re.DOTALL)
                                        for parte1,parte2 in linksseccao:
                                                conta_id_video = 0
                                                conta_os_items = conta_os_items + 1
                                                addDir1('[COLOR blue] Parte '+parte1+'[/COLOR]','','',iconimage,False,fanart)					
                                                match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                addDir1('[COLOR blue] Parte '+parte1+'[/COLOR]','','',iconimage,False,fanart)					
                                                match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                #addDir1('sim'+str(l),'url',1001,artfolder,False,'')
                                                conta_id_video = 0
                                                conta_os_items = conta_os_items + 1
                                                addDir1('[COLOR blue] Parte '+parte1+'[/COLOR]','','',iconimage,False,fanart)					
                                                match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                addDir1('[COLOR blue] Parte '+parte1+'[/COLOR]','','',iconimage,False,fanart)					
                                                match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
						try:
                                                        episodio = re.compile('(\d+)').findall(parte1)
                                                        if episodio:
                                                                episodiot = episodio[0]
                                                                episodio = episodio[0]
                                                        a_q = re.compile('\d+')
                                                        qq_aa = a_q.findall(episodio)
                                                        for q_a_q_a in qq_aa:
                                                                if len(q_a_q_a) == 1:
                                                                        episodiot = '0'+episodio
                                                except: pass
                                                #addLink(temporada+'-'+episodio+'-'+imdbcode+'-'+tmdbcode,'','')
                                                #return
                                                try:
                                                        epi_nome,air,sin,th = thetvdb_api_episodes()._id(str(tvdbid),str(temporada),str(episodio))
                                                        iconimage = th
                                                except: pass
                                                #addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]','','',iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)					
						match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
						for url in match:
                                                        conta_id_video = conta_id_video + 1
							conta_os_items = conta_os_items + 1
                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                        if f_id == '': f_id = fonte_id
                                                        else: f_id = f_id + '|' + fonte_id
						match = re.compile('<a href="(.+?)" target="_blank">').findall(parte2)
						if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
						for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                conta_os_items = conta_os_items + 1
                                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                if f_id == '': f_id = fonte_id
                                                                else: f_id = f_id + '|' + fonte_id
						match = re.compile('"window.open(.+?)"').findall(parte2)
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        conta_os_items = conta_os_items + 1
                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                        if f_id == '': f_id = fonte_id
                                                        else: f_id = f_id + '|' + fonte_id
                                                try:
                                                        if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                                percent = int( ( i / num ) * 100)
                                                                message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]'
                                                                progress.update( percent, "", message, "" )
                                                                print str(i) + " de " + str(int(num))
                                                                
                                                                if progress.iscanceled():
                                                                        break
                                                        mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                        addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                                except:
                                                        if 'EPI' not in parte1 and 'Epi' not in parte1: parte1 = parte1+'ºEPISÓDIO'
                                                        if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                                percent = int( ( i / num ) * 100)
                                                                message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]'
                                                                progress.update( percent, "", message, "" )
                                                                print str(i) + " de " + str(int(num))
                                                                
                                                                if progress.iscanceled():
                                                                        break
                                                        mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                        addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                                f_id = ''
                                                #return
				else:
					linksseccao = re.findall('<span style="color:.+?"><strong>(.+?)</strong></span><br.+?>(.+?)Ver Aqui</a></p>',newmatch[0],re.DOTALL)
                                        if linksseccao:
                                                for parte1,parte2 in linksseccao:
                                                        parte1=parte1.replace('[','(').replace(']',')').replace('<strong>','').replace('</strong>','')
                                                        conta_id_video = 0
                                                        conta_os_items = conta_os_items + 1
                                                        try:
                                                                episodio = re.compile('(\d+)').findall(parte1)
                                                                if episodio:
                                                                        episodiot = episodio[0]
                                                                        episodio = episodio[0]
                                                                a_q = re.compile('\d+')
                                                                qq_aa = a_q.findall(episodio)
                                                                for q_a_q_a in qq_aa:
                                                                        if len(q_a_q_a) == 1:
                                                                                episodiot = '0'+episodio
                                                        except: pass
                                                        #addLink(temporada+'-'+episodio+'-'+imdbcode+'-'+tmdbcode,'','')
                                                        #return              
                                                        try:
                                                                epi_nome,air,sin,th = thetvdb_api_episodes()._id(str(tvdbid),str(temporada),str(episodio))
                                                                iconimage = th
                                                        except: pass
                                                        #addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]','','',iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)						
                                                        match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                        if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                        for url in match:
                                                                conta_id_video = conta_id_video + 1
                                                                conta_os_items = conta_os_items + 1
                                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                if f_id == '': f_id = fonte_id
                                                                else: f_id = f_id + '|' + fonte_id
                                                        match = re.compile('<a href="(.+?)" target="_blank">').findall(parte2)
                                                        if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                        for url in match:
                                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                        conta_id_video = conta_id_video + 1
                                                                        conta_os_items = conta_os_items + 1
                                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        if f_id == '': f_id = fonte_id
                                                                        else: f_id = f_id + '|' + fonte_id
                                                        match = re.compile('"window.open(.+?)"').findall(parte2)
                                                        for url in match:
                                                                conta_id_video = conta_id_video + 1
                                                                url = url.replace("'","").replace("(","").replace(")","")
                                                                conta_os_items = conta_os_items + 1
                                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                if f_id == '': f_id = fonte_id
                                                                else: f_id = f_id + '|' + fonte_id
                                                        try:
                                                                if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                                        percent = int( ( i / num ) * 100)
                                                                        message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]'
                                                                        progress.update( percent, "", message, "" )
                                                                        print str(i) + " de " + str(int(num))
                                                                        
                                                                        if progress.iscanceled():
                                                                                break
                                                                mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                                addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                                        except:
                                                                if 'EPI' not in parte1 and 'Epi' not in parte1: parte1 = parte1+'ºEPISÓDIO'
                                                                if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                                        percent = int( ( i / num ) * 100)
                                                                        message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]'
                                                                        progress.update( percent, "", message, "" )
                                                                        print str(i) + " de " + str(int(num))
                                                                        
                                                                        if progress.iscanceled():
                                                                                break
                                                                mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                                addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                                        f_id = ''
                                                        #return
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
                                                                        try:
                                                                                episodio = re.compile('(\d+)').findall(parte1)
                                                                                if episodio:
                                                                                        episodiot = episodio[0]
                                                                                        episodio = episodio[0]
                                                                                a_q = re.compile('\d+')
                                                                                qq_aa = a_q.findall(episodio)
                                                                                for q_a_q_a in qq_aa:
                                                                                        if len(q_a_q_a) == 1:
                                                                                                episodiot = '0'+episodio
                                                                        except: pass
                                                                        #addLink(temporada+'-'+episodio+'-'+imdbcode+'-'+tmdbcode,'','')
                                                                        #return
                                                                        try:
                                                                                epi_nome,air,sin,th = thetvdb_api_episodes()._id(str(tvdbid),str(temporada),str(episodio))
                                                                                iconimage = th
                                                                        except: pass
                                                                        #addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]','','',iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)						
                                                                        match = re.compile('<iframe src="(.+?)"').findall(parte2)	
                                                                        for url in match:
                                                                                conta_id_video = conta_id_video + 1
                                                                                conta_os_items = conta_os_items + 1
                                                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                if f_id == '': f_id = fonte_id
                                                                                else: f_id = f_id + '|' + fonte_id
                                                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                                        if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                                        for url in match:
                                                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                        if f_id == '': f_id = fonte_id
                                                                                        else: f_id = f_id + '|' + fonte_id
                                                                        match = re.compile('"window.open(.+?)"').findall(parte2)
                                                                        for url in match:
                                                                                conta_id_video = conta_id_video + 1
                                                                                url = url.replace("'","").replace("(","").replace(")","")
                                                                                conta_os_items = conta_os_items + 1
                                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                if f_id == '': f_id = fonte_id
                                                                                else: f_id = f_id + '|' + fonte_id
                                                                        try:
                                                                                if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                                                        percent = int( ( i / num ) * 100)
                                                                                        message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]'
                                                                                        progress.update( percent, "", message, "" )
                                                                                        print str(i) + " de " + str(int(num))
                                                                                        
                                                                                        if progress.iscanceled():
                                                                                                break
                                                                                mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                                                addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                                                        except:
                                                                                if 'EPI' not in parte1 and 'Epi' not in parte1: parte1 = parte1+'ºEPISÓDIO'
                                                                                if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                                                        percent = int( ( i / num ) * 100)
                                                                                        message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]'
                                                                                        progress.update( percent, "", message, "" )
                                                                                        print str(i) + " de " + str(int(num))
                                                                                        
                                                                                        if progress.iscanceled():
                                                                                                break
                                                                                mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                                                addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                                                        f_id = ''
                                                                        #return
                                                else:
                                                        lin = re.findall('.+?EPIS',newmatch[0],re.DOTALL)
                                                        if len(lin) == 1: linksseccao = re.findall('ODIO (.+?)<.+?>(.+?)<img',newmatch[0],re.DOTALL)
                                                        else: linksseccao = re.findall('ODIO (.+?)<.+?>\n(.+?)EPIS',newmatch[0],re.DOTALL)
                                                        linksseccaoultimo = re.findall('ODIO (.+?)<.+?>\n(.+?)</p>',newmatch[0],re.DOTALL)
                                                        if i == 1: num = len(lin) + 0.0
                                                        if linksseccao:
                                                                ultima_parte = ''
                                                                fonte_id = ''
                                                                for parte1,parte2 in linksseccao:                
                                                                        conta_id_video = 0
                                                                        try:
                                                                                episodio = re.compile('(\d+)').findall(parte1)
                                                                                if episodio:
                                                                                        episodiot = episodio[0]
                                                                                        episodio = episodio[0]
                                                                                a_q = re.compile('\d+')
                                                                                qq_aa = a_q.findall(episodio)
                                                                                for q_a_q_a in qq_aa:
                                                                                        if len(q_a_q_a) == 1:
                                                                                                episodiot = '0'+episodio
                                                                        except: pass
                                                                        #addLink(parte1+'-'+temporada+'-'+episodio+'-'+imdbcode+'-'+tmdbcode,'','')
                                                                        
                                                                        try:
                                                                                epi_nome,air,sin,th = thetvdb_api_episodes()._id(str(tvdbid),str(temporada),str(episodio))
                                                                                iconimage = th
                                                                                
                                                                        except: pass
                                                                       
                                                                        if parte1 != ultima_parte:
                                                                                conta_os_items = conta_os_items + 1                                                                                
                                                                        
                                                                        if 'e' in parte1: ultepi = 'e'
                                                                        else: ultepi = int(parte1)
                                                                        match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                                        if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                                        for url in match:
                                                                                conta_id_video = conta_id_video + 1
                                                                                conta_os_items = conta_os_items + 1
                                                                                
                                                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                if f_id == '': f_id = fonte_id
                                                                                else: f_id = f_id + '|' + fonte_id
                                                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                                        if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                                        for url in match:
                                                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        
                                                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                       
                                                                                        if f_id == '': f_id = fonte_id
                                                                                        else: f_id = f_id + '|' + fonte_id
                                                                        match = re.compile('"window.open(.+?)"').findall(parte2)
                                                                        for url in match:
                                                                                if 'LINK' not in url:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        
                                                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                        if f_id == '': f_id = fonte_id
                                                                                        else: f_id = f_id + '|' + fonte_id
                                                                        if parte1 != ultima_parte:
                                                                                try:
                                                                                        if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                                                                percent = int( ( i / num ) * 100)
                                                                                                message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]'
                                                                                                progress.update( percent, "", message, "" )
                                                                                                print str(i) + " de " + str(int(num))
                                                                                                
                                                                                                if progress.iscanceled():
                                                                                                        break
                                                                                        mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                                                        addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                                                                except:
                                                                                        if 'EPI' not in parte1 and 'Epi' not in parte1: parte1 = parte1+'ºEPISÓDIO'
                                                                                        if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                                                                percent = int( ( i / num ) * 100)
                                                                                                message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]'
                                                                                                progress.update( percent, "", message, "" )
                                                                                                print str(i) + " de " + str(int(num))
                                                                                                
                                                                                                if progress.iscanceled():
                                                                                                        break
                                                                                        mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                                                        addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                              
                                                                        f_id = ''       
                                                                        i = i + 1
       
                                                                conta_id_video = 0
                                                                v_id = re.compile('=(.*)').findall(url)
                                                                if not v_id: v_id = re.compile('//(.*)').findall(url)
                                                                #return
                                                                nmatch = re.findall(v_id[0]+'.+?DOWNLOAD',link2,re.DOTALL)
                                                                if not nmatch: nmatch = re.findall(v_id[0]+'.+?<nav class="navigation post-navigation"',link2,re.DOTALL)
                                                                linksseccao = re.findall('ODIO (.+?)</p>\n<p><b>(.+?)EPIS',nmatch[0],re.DOTALL)
                                                                if linksseccao:
                                                                        for parte1,parte2 in linksseccao:
                                                                                
                                                                                conta_os_items = conta_os_items + 1
                                                                                try:
                                                                                        episodio = re.compile('(\d+)').findall(parte1)
                                                                                        if episodio:
                                                                                                episodiot = episodio[0]
                                                                                                episodio = episodio[0]
                                                                                        a_q = re.compile('\d+')
                                                                                        qq_aa = a_q.findall(episodio)
                                                                                        for q_a_q_a in qq_aa:
                                                                                                if len(q_a_q_a) == 1:
                                                                                                        episodiot = '0'+episodio
                                                                                except: pass
                                                                                #addLink(temporada+'-'+episodio+'-'+imdbcode+'-'+tmdbcode,'','')
                                                                                try:
                                                                                        epi_nome,air,sin,th = thetvdb_api_episodes()._id(str(tvdbid),str(temporada),str(episodio))
                                                                                        iconimage = th
                                                                                except: pass
                                                                                #addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]','','',iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                                                                match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                                                for url in match:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                        if f_id == '': f_id = fonte_id
                                                                                        else: f_id = f_id + '|' + fonte_id
                                                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                                                for url in match:
                                                                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                                conta_id_video = conta_id_video + 1
                                                                                                conta_os_items = conta_os_items + 1
                                                                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                                if f_id == '': f_id = fonte_id
                                                                                                else: f_id = f_id + '|' + fonte_id
                                                                                match = re.compile('"window.open(.+?)"').findall(parte2)
                                                                                for url in match:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                        if f_id == '': f_id = fonte_id
                                                                                        else: f_id = f_id + '|' + fonte_id
                                                                                try:
                                                                                        if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                                                                percent = int( ( i / num ) * 100)
                                                                                                message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]'
                                                                                                progress.update( percent, "", message, "" )
                                                                                                print str(i) + " de " + str(int(num))
                                                                                                
                                                                                                if progress.iscanceled():
                                                                                                        break
                                                                                        mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                                                        addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                                                                except:
                                                                                        if 'EPI' not in parte1 and 'Epi' not in parte1: parte1 = parte1+'ºEPISÓDIO'
                                                                                        if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                                                                percent = int( ( i / num ) * 100)
                                                                                                message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]'
                                                                                                progress.update( percent, "", message, "" )
                                                                                                print str(i) + " de " + str(int(num))
                                                                                                
                                                                                                if progress.iscanceled():
                                                                                                        break
                                                                                        mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                                                        addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                                                                f_id = ''
                                                                                i = i + 1
                                                                conta_id_video = 0
                                                                v_id = re.compile('=(.*)').findall(url)
                                                                if not v_id: v_id = re.compile('//(.*)').findall(url)
                                                                contamatch = re.findall('ODIO (.+?)</p>\n<p><b>',newmatch[0],re.DOTALL)
                                                                #return
                                                                linksseccao = re.findall(v_id[0]+'(.+?)<img',newmatch[0],re.DOTALL)
                                                                if linksseccao:
                                                                        match = re.compile('ODIO (.+?)<br').findall(linksseccao[0])
                                                                        if not match: match = re.compile('ODIO (.+?)</p>').findall(linksseccao[0])
                                                                        if match:
                                                                                parte1 = match[0]
                                                                                conta_os_items = conta_os_items + 1
                                                                                try:
                                                                                        episodio = re.compile('(\d+)').findall(parte1)
                                                                                        if episodio:
                                                                                                episodiot = episodio[0]
                                                                                                episodio = episodio[0]
                                                                                        a_q = re.compile('\d+')
                                                                                        qq_aa = a_q.findall(episodio)
                                                                                        for q_a_q_a in qq_aa:
                                                                                                if len(q_a_q_a) == 1:
                                                                                                        episodiot = '0'+episodio
                                                                                except: pass
                                                                                #addLink(temporada+'-'+episodio+'-'+imdbcode+'-'+tmdbcode,'','')
                                                                                try:
                                                                                        epi_nome,air,sin,th = thetvdb_api_episodes()._id(str(tvdbid),str(temporada),str(episodio))
                                                                                        iconimage = th
                                                                                except: pass
                                                                                #addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]','','',iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                                                        match = re.compile('<iframe.+?src="(.+?)"').findall(linksseccao[0])
                                                                        if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(linksseccao[0])	
                                                                        for url in match:
                                                                                conta_id_video = conta_id_video + 1
                                                                                conta_os_items = conta_os_items + 1
                                                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                if f_id == '': f_id = fonte_id
                                                                                else: f_id = f_id + '|' + fonte_id
                                                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(linksseccao[0])
                                                                        if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(linksseccao[0])
                                                                        for url in match:
                                                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                        if f_id == '': f_id = fonte_id
                                                                                        else: f_id = f_id + '|' + fonte_id
                                                                        match = re.compile('"window.open(.+?)"').findall(linksseccao[0])
                                                                        for url in match:
                                                                                conta_id_video = conta_id_video + 1
                                                                                url = url.replace("'","").replace("(","").replace(")","")
                                                                                conta_os_items = conta_os_items + 1
                                                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                if f_id == '': f_id = fonte_id
                                                                                else: f_id = f_id + '|' + fonte_id
                                                                        try:
                                                                                if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                                                        percent = int( ( i / num ) * 100)
                                                                                        message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]'
                                                                                        progress.update( percent, "", message, "" )
                                                                                        print str(i) + " de " + str(int(num))
                                                                                        
                                                                                        #if progress.iscanceled():
                                                                                                #break
                                                                                mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                                                addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                                                        except:
                                                                                if 'EPI' not in parte1 and 'Epi' not in parte1: parte1 = parte1+'ºEPISÓDIO'
                                                                                if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                                                        percent = int( ( i / num ) * 100)
                                                                                        message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]'
                                                                                        progress.update( percent, "", message, "" )
                                                                                        print str(i) + " de " + str(int(num))
                                                                                        
                                                                                        #if progress.iscanceled():
                                                                                                #break
                                                                                mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                                                addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                                                        f_id = ''
                                                                ####################################################################
                                                        else:
                                                                linksseccao = re.findall('<p>(.+?)EPISODIO<br/>(.+?)</iframe>',newmatch[0],re.DOTALL)
                                                                if linksseccao:
                                                                        #addDir1('sim1','url',1001,artfolder,False,'')
                                                                        for parte1,parte2 in linksseccao:
                                                                               
                                                                                conta_id_video = 0
                                                                                conta_os_items = conta_os_items + 1
                                                                                try:
                                                                                        episodio = re.compile('(\d+)').findall(parte1)
                                                                                        if episodio:
                                                                                                episodiot = episodio[0]
                                                                                                episodio = episodio[0]
                                                                                        a_q = re.compile('\d+')
                                                                                        qq_aa = a_q.findall(episodio)
                                                                                        for q_a_q_a in qq_aa:
                                                                                                if len(q_a_q_a) == 1:
                                                                                                        episodiot = '0'+episodio
                                                                                except: pass
                                                                                #addLink(temporada+'-'+episodio+'-'+imdbcode+'-'+tmdbcode,'','')
                                                                                try:
                                                                                        epi_nome,air,sin,th = thetvdb_api_episodes()._id(str(tvdbid),str(temporada),str(episodio))
                                                                                        iconimage = th
                                                                                except: pass
                                                                                #addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]','','',iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)					
                                                                                match = re.compile('<iframe src="(.+?)"').findall(parte2)	
                                                                                for url in match:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                        if f_id == '': f_id = fonte_id
                                                                                        else: f_id = f_id + '|' + fonte_id
                                                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                                                for url in match:
                                                                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                                conta_id_video = conta_id_video + 1
                                                                                                conta_os_items = conta_os_items + 1
                                                                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                                if f_id == '': f_id = fonte_id
                                                                                                else: f_id = f_id + '|' + fonte_id
                                                                                match = re.compile('"window.open(.+?)"').findall(parte2)
                                                                                for url in match:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                        if f_id == '': f_id = fonte_id
                                                                                        else: f_id = f_id + '|' + fonte_id
                                                                                try:
                                                                                        if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                                                                percent = int( ( i / num ) * 100)
                                                                                                message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]'
                                                                                                progress.update( percent, "", message, "" )
                                                                                                print str(i) + " de " + str(int(num))
                                                                                                
                                                                                                if progress.iscanceled():
                                                                                                        break
                                                                                        mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                                                        addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                                                                except:
                                                                                        if 'EPI' not in parte1 and 'Epi' not in parte1: parte1 = parte1+'ºEPISÓDIO'
                                                                                        if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                                                                percent = int( ( i / num ) * 100)
                                                                                                message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]'
                                                                                                progress.update( percent, "", message, "" )
                                                                                                print str(i) + " de " + str(int(num))
                                                                                                
                                                                                                if progress.iscanceled():
                                                                                                        break
                                                                                        mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                                                        addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                                                                f_id = ''
                                                                                i = i + 1
                                                                        conta_id_video = 0
                                                                        v_id = re.compile('=(.*)').findall(url)
                                                                        if not v_id: v_id = re.compile('//(.*)').findall(url)
                                                                        nmatch = re.findall(v_id[0]+'(.+?)<img',newmatch[0],re.DOTALL)
                                                                        linksseccao = re.findall('<p>(.+?)EPISODIO<br/>(.+?)</iframe>',nmatch[0],re.DOTALL)
                                                                        for parte1,parte2 in linksseccao:
                          
                                                                                conta_id_video = 0
                                                                                conta_os_items = conta_os_items + 1
                                                                                try:
                                                                                        episodio = re.compile('(\d+)').findall(parte1)
                                                                                        if episodio:
                                                                                                episodiot = episodio[0]
                                                                                                episodio = episodio[0]
                                                                                        a_q = re.compile('\d+')
                                                                                        qq_aa = a_q.findall(episodio)
                                                                                        for q_a_q_a in qq_aa:
                                                                                                if len(q_a_q_a) == 1:
                                                                                                        episodiot = '0'+episodio
                                                                                except: pass
                                                                                #addLink(temporada+'-'+episodio+'-'+imdbcode+'-'+tmdbcode,'','')
                                                                                try:
                                                                                        epi_nome,air,sin,th = thetvdb_api_episodes()._id(str(tvdbid),str(temporada),str(episodio))
                                                                                        iconimage = th
                                                                                except: pass
                                                                                #addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]','','',iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)					
                                                                                match = re.compile('<iframe src="(.+?)"').findall(parte2)	
                                                                                for url in match:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                        if f_id == '': f_id = fonte_id
                                                                                        else: f_id = f_id + '|' + fonte_id
                                                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                                                for url in match:
                                                                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                                conta_id_video = conta_id_video + 1
                                                                                                conta_os_items = conta_os_items + 1
                                                                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                                if f_id == '': f_id = fonte_id
                                                                                                else: f_id = f_id + '|' + fonte_id
                                                                                match = re.compile('"window.open(.+?)"').findall(parte2)
                                                                                for url in match:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                        if f_id == '': f_id = fonte_id
                                                                                        else: f_id = f_id + '|' + fonte_id
                                                                                try:
                                                                                        if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                                                                percent = int( ( i / num ) * 100)
                                                                                                message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]'
                                                                                                progress.update( percent, "", message, "" )
                                                                                                print str(i) + " de " + str(int(num))
                                                                                                
                                                                                                if progress.iscanceled():
                                                                                                        break
                                                                                        mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                                                        addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                                                                except:
                                                                                        if 'EPI' not in parte1 and 'Epi' not in parte1: parte1 = parte1+'ºEPISÓDIO'
                                                                                        if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                                                                percent = int( ( i / num ) * 100)
                                                                                                message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]'
                                                                                                progress.update( percent, "", message, "" )
                                                                                                print str(i) + " de " + str(int(num))
                                                                                                
                                                                                                if progress.iscanceled():
                                                                                                        break
                                                                                        mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                                                        addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                                                                f_id = ''
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
                                                                                        try:
                                                                                                episodio = re.compile('(\d+)').findall(parte1)
                                                                                                if episodio:
                                                                                                        episodiot = episodio[0]
                                                                                                        episodio = episodio[0]
                                                                                                a_q = re.compile('\d+')
                                                                                                qq_aa = a_q.findall(episodio)
                                                                                                for q_a_q_a in qq_aa:
                                                                                                        if len(q_a_q_a) == 1:
                                                                                                                episodiot = '0'+episodio
                                                                                        except: pass
                                                                                        #addLink(temporada+'-'+episodio+'-'+imdbcode+'-'+tmdbcode,'','')
                                                                                        try:
                                                                                                epi_nome,air,sin,th = thetvdb_api_episodes()._id(str(tvdbid),str(temporada),str(episodio))
                                                                                                iconimage = th
                                                                                        except:pass
                                                                                        #addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]','','',iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)					
                                                                                        match = re.compile('<iframe src="(.+?)"').findall(parte2)	
                                                                                        for url in match:
                                                                                                conta_id_video = conta_id_video + 1
                                                                                                conta_os_items = conta_os_items + 1
                                                                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                                if f_id == '': f_id = fonte_id
                                                                                                else: f_id = f_id + '|' + fonte_id
                                                                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                                                        if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                                                        for url in match:
                                                                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                                        conta_id_video = conta_id_video + 1
                                                                                                        conta_os_items = conta_os_items + 1
                                                                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                                        if f_id == '': f_id = fonte_id
                                                                                                        else: f_id = f_id + '|' + fonte_id
                                                                                        match = re.compile('"window.open(.+?)"').findall(parte2)
                                                                                        for url in match:
                                                                                                conta_id_video = conta_id_video + 1
                                                                                                url = url.replace("'","").replace("(","").replace(")","")
                                                                                                conta_os_items = conta_os_items + 1
                                                                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                                if f_id == '': f_id = fonte_id
                                                                                                else: f_id = f_id + '|' + fonte_id
                                                                                        try:
                                                                                                if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                                                                        percent = int( ( i / num ) * 100)
                                                                                                        message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]'
                                                                                                        progress.update( percent, "", message, "" )
                                                                                                        print str(i) + " de " + str(int(num))
                                                                                                        
                                                                                                        if progress.iscanceled():
                                                                                                                break
                                                                                                mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                                                                addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                                                                        except:
                                                                                                if 'EPI' not in parte1 and 'Epi' not in parte1: parte1 = parte1+'ºEPISÓDIO'
                                                                                                if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                                                                        percent = int( ( i / num ) * 100)
                                                                                                        message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]'
                                                                                                        progress.update( percent, "", message, "" )
                                                                                                        print str(i) + " de " + str(int(num))
                                                                                                        
                                                                                                        if progress.iscanceled():
                                                                                                                break
                                                                                                mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                                                                addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                                                                        f_id = ''
                                                                                        i = i + 1
                                                                else:
                                                                        match = re.compile('<iframe.+?src="(.+?)"').findall(newmatch[0])
                                                                        if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(newmatch[0])
                                                                        for url in match:
                                                                                conta_id_video = conta_id_video + 1
                                                                                conta_os_items = conta_os_items + 1
                                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        match = re.compile('<IFRAME.+?SRC="(.+?)"').findall(newmatch[0])
                                                                        for url in match:
                                                                                conta_id_video = conta_id_video + 1
                                                                                conta_os_items = conta_os_items + 1
                                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(newmatch[0])
                                                                        if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(newmatch[0])
                                                                        for url in match:
                                                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
						addDir1('[COLOR blue] Parte '+parte1+'[/COLOR]',urlfinal,'',iconimage,False,'')					
						match = re.compile('<iframe src="(.+?)"').findall(parte2)	
						for url in match:
                                                        conta_id_video = conta_id_video + 1
							conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('<IFRAME SRC="(.+?)"').findall(parte2)	
						for url in match:
                                                        conta_id_video = conta_id_video + 1
							conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
						match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
						if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
						for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                                try:
                                                                        episodio = re.compile('(\d+)').findall(parte1)
                                                                        if episodio:
                                                                                episodiot = episodio[0]
                                                                                episodio = episodio[0]
                                                                        a_q = re.compile('\d+')
                                                                        qq_aa = a_q.findall(episodio)
                                                                        for q_a_q_a in qq_aa:
                                                                                if len(q_a_q_a) == 1:
                                                                                        episodiot = '0'+episodio
                                                                except: pass
                                                                #addLink(temporada+'-'+episodio+'-'+imdbcode+'-'+tmdbcode,'','')
                                                                try:
                                                                        epi_nome,air,sin,th = thetvdb_api_episodes()._id(str(tvdbid),str(temporada),str(episodio))
                                                                        iconimage = th
                                                                except:pass
                                                                #addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]','','',iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
							ultima_parte = parte1
							match = re.compile('<iframe src="(.+?)"').findall(parte2)	
							for url in match:
                                                                conta_id_video = conta_id_video + 1
								conta_os_items = conta_os_items + 1
                                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                if f_id == '': f_id = fonte_id
                                                                else: f_id = f_id + '|' + fonte_id
							match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
							match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
							match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
							for url in match:
                                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                        conta_id_video = conta_id_video + 1
                                                                        conta_os_items = conta_os_items + 1
                                                                        fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        if f_id == '': f_id = fonte_id
                                                                        else: f_id = f_id + '|' + fonte_id
							match = re.compile('"window.open(.+?)"').findall(parte2)
                                                        for url in match:
                                                                conta_id_video = conta_id_video + 1
                                                                url = url.replace("'","").replace("(","").replace(")","")
                                                                conta_os_items = conta_os_items + 1
                                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                if f_id == '': f_id = fonte_id
                                                                else: f_id = f_id + '|' + fonte_id
                                                        try:
                                                                if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                                        percent = int( ( i / num ) * 100)
                                                                        message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]'
                                                                        progress.update( percent, "", message, "" )
                                                                        print str(i) + " de " + str(int(num))
                                                                        
                                                                        if progress.iscanceled():
                                                                                break
                                                                mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                                addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                                        except:
                                                                if 'EPI' not in parte1 and 'Epi' not in parte1: parte1 = parte1+'ºEPISÓDIO'
                                                                if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                                                        percent = int( ( i / num ) * 100)
                                                                        message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]'
                                                                        progress.update( percent, "", message, "" )
                                                                        print str(i) + " de " + str(int(num))
                                                                        
                                                                        if progress.iscanceled():
                                                                                break
                                                                mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                                                addDir_episode1_true('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                                        f_id = ''
					else:
                                                
						match = re.compile('<iframe src="(.+?)"').findall(newmatch[0])	
						for url in match:
                                                        conta_id_video = conta_id_video + 1
							conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('<IFRAME SRC="(.+?)"').findall(newmatch[0])	
						for url in match:
                                                        conta_id_video = conta_id_video + 1
							conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
						match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(newmatch[0])
                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(newmatch[0])
						for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                conta_os_items = conta_os_items + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
						match = re.compile('"window.open(.+?)"').findall(newmatch[0])
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
        if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                percent = int( ( 100 / 100.0 ) * 100)
                progress.update( percent, "", message, "" )
        if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo and 'Mini-serie' not in nometitulo and 'Minisérie' not in nometitulo and 'Miniserie' not in nometitulo:
                url = 'IMDB'+imdbcode+'IMDB'
                if mvoutv != 'MoviesTPT': FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n2),'TPT',url)
##                nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(nomeescolha)
##                nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
##                nn = nomeescolha.replace('[B][COLOR green]','--').replace('[/COLOR][/B]','--').replace('[COLOR orange]','').replace('[/COLOR]','').replace('[','---').replace(']','---').replace('TPT | ','')
##                if '---' in nn:
##                        n = re.compile('---(.+?)---').findall(nn)
##                        n1 = re.compile('--(.+?)--').findall(nn)
##                        url = 'IMDB'+imdbcode+'IMDB'
##                        FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n1[0]),'TPT',url)
##                else:
##                        n1 = re.compile('--(.+?)--').findall(nn)
##                        url = 'IMDB'+imdbcode+'IMDB'
##                        FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n1[0]),'TPT',url)
        if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                progress.close()
                
                xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
                xbmc.executebuiltin("Container.SetViewMode(504)")
                xbmcplugin.endOfDirectory(int(sys.argv[1]))

		
#----------------------------------------------------------------------------------------------------------------------------------------------#

def TPT_resolve_not_videomega_filmes11(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart):
        conta_id_video = int(conta_id_video)
        conta_os_items = int(conta_os_items)
        #addLink('vai','','','')
        
        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                url = url + '///' + nomeescolha
        
        if "videomega" in url:
		try:
                        fonte_id = '(Videomega)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
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
			if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id1.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
        if "dropvideo" in url:
		try:
                        url = url.replace('/video/','/embed/')
                        fonte_id = '(DropVideo)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "vidzi.tv" in url:
                try:
                        fonte_id = '(Vidzi.tv)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "vodlocker" in url:
		try:
                        fonte_id = '(Vodlocker)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "played.to" in url:
                try:
                        fonte_id = '(Played.to)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "cloudzilla" in url:
                try:
                        fonte_id = '(Cloudzilla)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "divxstage" in url:
                try:
                        fonte_id = '(Divxstage)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "vidzen" in url:
                try:
                        fonte_id = '(Vidzen)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
	if "streamin.to" in url:
                try:
                        fonte_id = '(Streamin)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass                        
    	if "nowvideo" in url:
                try:
                        fonte_id = '(Nowvideo)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "primeshare" in url:
                try:
                        fonte_id = '(Primeshare)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videoslasher" in url:
                try:
                        fonte_id = '(VideoSlasher)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "sockshare" in url:
                try:
                        fonte_id = '(Sockshare)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "putlocker" in url:
                try:
                        url = url.replace('putlocker.com/embed/','firedrive.com/file/')
                        fonte_id = '(Firedrive)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	else:
                if "firedrive" in url:
                        try:
                                fonte_id = '(Firedrive)'+url
                                if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
                        except:pass
    	if "movshare" in url:
                try:
                        fonte_id = '(Movshare)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
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
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:                     
                                url = url + '///' + nomeescolha
                        fonte_id = '(Video.tt)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                #addDir('1[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(VideoWood)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "video.pw" in url:
                try:
                        print url
                        fonte_id = '(Video.pw)'+url
                        #if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "thevideo.me" in url:
                try:
                        #if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(Thevideo.me)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	#addLink(url,'','','')
        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url and 'sockshare' not in url and 'firedrive' not in url and 'movshare' not in url and 'nowvideo' not in url and 'putlocker' not in url:# and 'iiiiiiiiii' in url:
                        Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'').replace(url+'///'+nomeescolha,'')+'[/COLOR][/B]',iconimage,'',fanart)
    	return fonte_id
   
	
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
        streams = []
	try:
		link2=abrir_url(url)
	except: link2 = ''
	if link2:
                if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo and 'Mini-Serie' not in nometitulo and 'Minisérie' not in nometitulo and 'Miniserie' not in nometitulo and imdbcode == '':
                        items = re.findall('<div class="postmeta-primary">(.*?)<div id="sidebar-primary">', link2, re.DOTALL)
                        if items != []:
                                imdb = re.compile('imdb.com/title/(.+?)/').findall(items[0])
                                if imdb: imdbcode = imdb[0]
                                else: imdbcode = ''
                if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo and 'Mini-serie' not in nometitulo and 'Minisérie' not in nometitulo and 'Miniserie' not in nometitulo:
                        newmatch = re.findall('<span id=.+?DOWNLOAD POR',link2,re.DOTALL)
                        if not newmatch: newmatch = re.findall('<span id=.+?BAIXAR',link2,re.DOTALL)
                        l=1
                else:
                        #newmatch = re.findall('<span id=.+?<img style="height: 40px; width: 465px;"',link2,re.DOTALL)
                        newmatch1 = re.findall('<span id=.+?DOWNLOAD POR',link2,re.DOTALL)
                        if not newmatch1: newmatch1 = re.findall('<span id=.+?BAIXAR',link2,re.DOTALL)
                        newmatch = re.findall('<img style="height: 90px; width: 200px;".+?DOWNLOAD POR',link2,re.DOTALL)
                        if not newmatch: newmatch = re.findall('<img style="height: 90px; width: 200px;".+?BAIXAR',link2,re.DOTALL)
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
                        if newmatch1 != [] and 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo or 'Mini-serie' in nometitulo or 'Minisérie' in nometitulo or 'Miniserie' in nometitulo:
                                lin = re.findall('.+?EPIS',newmatch1[0],re.DOTALL)
                                num = len(lin) + 0.0 - 1
                                linkseriesssss = re.findall('</span>CLIQUE AQUI PARA VER O (.+?)</div>(.+?)</div></div><',newmatch1[0],re.DOTALL)
                                for parte1,parte2 in linkseriesssss:
                                        conta_id_video = 0
                                        addDir1('[COLOR blue]'+parte1+'[/COLOR]','','',iconimage,False,fanart)
                                        match = re.compile('<span class="su-lightbox" data-mfp-src="(.+?)" data-mfp-type="iframe">').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                        i = i + 1
                if newmatch:
                        if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo and 'Mini-serie' not in nometitulo and 'Minisérie' not in nometitulo and 'Miniserie' not in nometitulo:
                                match = re.compile('<span class="su-lightbox" data-mfp-src="(.+?)" data-mfp-type="iframe">').findall(newmatch[0])
                                if not match: match = re.compile('src="(.+?)"').findall(newmatch[0])
                                for url in match:
                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                conta_id_video = conta_id_video + 1
                                                conta_os_items = conta_os_items + 1
                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
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
                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                        i = i + 1
			linksseccaopartes = re.findall('.+?PARTE',newmatch[0],re.DOTALL)
			if linksseccaopartes:
                                if len(linksseccaopartes) > 1:
                                        linksseccao = re.findall('RTE(.+?)<.+?>\n(.+?)>PA',newmatch[0],re.DOTALL)
                                        for parte1,parte2 in linksseccao:
                                                conta_id_video = 0
                                                conta_os_items = conta_os_items + 1
                                                addDir1('[COLOR blue] Parte '+parte1+'[/COLOR]','','',iconimage,False,fanart)					
                                                match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                conta_os_items = conta_os_items + 1
                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('"window.open(.+?)"').findall(parte2)
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        conta_os_items = conta_os_items + 1
                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                        v_id = re.compile('=(.*)').findall(url)
                                        if not v_id: v_id = re.compile('//(.*)').findall(url)
                                        nmatch = re.findall(v_id[0]+'.+?DOWNLOAD',link2,re.DOTALL)
                                        if not nmatch: nmatch = re.findall(v_id[0]+'.+?<nav class="navigation post-navigation"',link2,re.DOTALL)
                                        linksseccao = re.findall('PARTE(.+?)<.+?>\n(.+?)<p>&nbsp;</p>',nmatch[0],re.DOTALL)
                                        for parte1,parte2 in linksseccao:
                                                conta_id_video = 0
                                                conta_os_items = conta_os_items + 1
                                                addDir1('[COLOR blue] Parte '+parte1+'[/COLOR]','','',iconimage,False,fanart)					
                                                match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                conta_os_items = conta_os_items + 1
                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('"window.open(.+?)"').findall(parte2)
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        conta_os_items = conta_os_items + 1
                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                if len(linksseccaopartes) == 1:
                                        linksseccao = re.findall('<p>PARTE(.+?)<.+?>\n(.+?)<p>&nbsp;</p>',newmatch[0],re.DOTALL)
                                        for parte1,parte2 in linksseccao:
                                                conta_id_video = 0
                                                conta_os_items = conta_os_items + 1
                                                addDir1('[COLOR blue] Parte '+parte1+'[/COLOR]','','',iconimage,False,fanart)					
                                                match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                conta_os_items = conta_os_items + 1
                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('"window.open(.+?)"').findall(parte2)
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        conta_os_items = conta_os_items + 1
                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                        linksseccao = re.findall('<p>PARTE(\d+)</p>\n(.+?)<p>&nbsp;</p>',newmatch[0],re.DOTALL)
                                        for parte1,parte2 in linksseccao:
                                                conta_id_video = 0
                                                conta_os_items = conta_os_items + 1
                                                addDir1('[COLOR blue] Parte '+parte1+'[/COLOR]','','',iconimage,False,fanart)					
                                                match = re.compile('<iframe.+?src="(.+?)"').findall(parte2)
                                                if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(parte2)	
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                conta_os_items = conta_os_items + 1
                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                match = re.compile('"window.open(.+?)"').findall(parte2)
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        conta_os_items = conta_os_items + 1
                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
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
							streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
						match = re.compile('<a href="(.+?)" target="_blank">').findall(parte2)
						if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
						for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                conta_os_items = conta_os_items + 1
                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
						match = re.compile('"window.open(.+?)"').findall(parte2)
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        conta_os_items = conta_os_items + 1
                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
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
                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                        match = re.compile('<a href="(.+?)" target="_blank">').findall(parte2)
                                                        if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                        for url in match:
                                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                        conta_id_video = conta_id_video + 1
                                                                        conta_os_items = conta_os_items + 1
                                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                        match = re.compile('"window.open(.+?)"').findall(parte2)
                                                        for url in match:
                                                                conta_id_video = conta_id_video + 1
                                                                url = url.replace("'","").replace("(","").replace(")","")
                                                                conta_os_items = conta_os_items + 1
                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
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
                                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                                        if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                                        for url in match:
                                                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        match = re.compile('"window.open(.+?)"').findall(parte2)
                                                                        for url in match:
                                                                                conta_id_video = conta_id_video + 1
                                                                                url = url.replace("'","").replace("(","").replace(")","")
                                                                                conta_os_items = conta_os_items + 1
                                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
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
                                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                                        if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                                        for url in match:
                                                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        match = re.compile('"window.open(.+?)"').findall(parte2)
                                                                        for url in match:
                                                                                if 'LINK' not in url:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
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
                                                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                                                for url in match:
                                                                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                                conta_id_video = conta_id_video + 1
                                                                                                conta_os_items = conta_os_items + 1
                                                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                match = re.compile('"window.open(.+?)"').findall(parte2)
                                                                                for url in match:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
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
                                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(linksseccao[0])
                                                                        if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(linksseccao[0])
                                                                        for url in match:
                                                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        match = re.compile('"window.open(.+?)"').findall(linksseccao[0])
                                                                        for url in match:
                                                                                conta_id_video = conta_id_video + 1
                                                                                url = url.replace("'","").replace("(","").replace(")","")
                                                                                conta_os_items = conta_os_items + 1
                                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
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
                                                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                                                for url in match:
                                                                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                                conta_id_video = conta_id_video + 1
                                                                                                conta_os_items = conta_os_items + 1
                                                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                match = re.compile('"window.open(.+?)"').findall(parte2)
                                                                                for url in match:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
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
                                                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                                                for url in match:
                                                                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                                conta_id_video = conta_id_video + 1
                                                                                                conta_os_items = conta_os_items + 1
                                                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                match = re.compile('"window.open(.+?)"').findall(parte2)
                                                                                for url in match:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
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
                                                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                                                                        if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
                                                                                        for url in match:
                                                                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                                        conta_id_video = conta_id_video + 1
                                                                                                        conta_os_items = conta_os_items + 1
                                                                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                        match = re.compile('"window.open(.+?)"').findall(parte2)
                                                                                        for url in match:
                                                                                                conta_id_video = conta_id_video + 1
                                                                                                url = url.replace("'","").replace("(","").replace(")","")
                                                                                                conta_os_items = conta_os_items + 1
                                                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                                        i = i + 1
                                                                else:
                                                                        match = re.compile('<iframe.+?src="(.+?)"').findall(newmatch[0])
                                                                        if not match: match = re.compile("<iframe.+?src='(.+?)'").findall(newmatch[0])
                                                                        for url in match:
                                                                                conta_id_video = conta_id_video + 1
                                                                                conta_os_items = conta_os_items + 1
                                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        match = re.compile('<IFRAME.+?SRC="(.+?)"').findall(newmatch[0])
                                                                        if not match: match = re.compile("<IFRAME.+?SRC='(.+?)'").findall(newmatch[0])
                                                                        for url in match:
                                                                                conta_id_video = conta_id_video + 1
                                                                                conta_os_items = conta_os_items + 1
                                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(newmatch[0])
                                                                        if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(newmatch[0])
                                                                        for url in match:
                                                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                                        conta_id_video = conta_id_video + 1
                                                                                        conta_os_items = conta_os_items + 1
                                                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                                        match = re.compile('"window.open(.+?)"').findall(newmatch[0])
                                                                        for url in match:
                                                                                conta_id_video = conta_id_video + 1
                                                                                url = url.replace("'","").replace("(","").replace(")","")
                                                                                conta_os_items = conta_os_items + 1
                                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
		else:
			newmatch = re.findall('EM PT/PT:.+?<nav class="navigation post-navigation"',link2,re.DOTALL)
			if newmatch:
				linksseccao = re.findall('<p>PARTE (\d+)<br.+?\n(.+?)</p>',newmatch[0],re.DOTALL)
				if linksseccao:
					for parte1,parte2 in linksseccao:
                                                conta_id_video = 0
                                                conta_os_items = conta_os_items + 1
						addDir1('[COLOR blue] Parte '+parte1+'[/COLOR]',urlfinal,'',iconimage,False,'')					
						match = re.compile('<iframe src="(.+?)"').findall(parte2)	
						for url in match:
                                                        conta_id_video = conta_id_video + 1
							conta_os_items = conta_os_items + 1
							streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
						match = re.compile('<IFRAME SRC="(.+?)"').findall(parte2)	
						for url in match:
                                                        conta_id_video = conta_id_video + 1
							conta_os_items = conta_os_items + 1
							streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
						match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
						if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
						for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                conta_os_items = conta_os_items + 1
                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
						match = re.compile('"window.open(.+?)"').findall(parte2)
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        conta_os_items = conta_os_items + 1
                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
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
								streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
							match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
							match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
							match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
							for url in match:
                                                                if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                        conta_id_video = conta_id_video + 1
                                                                        conta_os_items = conta_os_items + 1
                                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
							match = re.compile('"window.open(.+?)"').findall(parte2)
                                                        for url in match:
                                                                conta_id_video = conta_id_video + 1
                                                                url = url.replace("'","").replace("(","").replace(")","")
                                                                conta_os_items = conta_os_items + 1
                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
					else:
						match = re.compile('<iframe src="(.+?)"').findall(newmatch[0])	
						for url in match:
                                                        conta_id_video = conta_id_video + 1
							conta_os_items = conta_os_items + 1
							streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
						match = re.compile('<IFRAME SRC="(.+?)"').findall(newmatch[0])	
						for url in match:
                                                        conta_id_video = conta_id_video + 1
							conta_os_items = conta_os_items + 1
							streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
						match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(newmatch[0])
                                                if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(newmatch[0])
						for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                conta_os_items = conta_os_items + 1
                                                                streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                                #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
						match = re.compile('"window.open(.+?)"').findall(newmatch[0])
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        conta_os_items = conta_os_items + 1
                                                        streams.append(url+'|'+str(conta_id_video)+'|'+str(conta_os_items)+'|'+nomeescolha+'|'+iconimage+'|'+fanart)
                                                        #TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
        i = 0
        threads = []
        #addLink(str(len(streams)),'','','')
        for stream in streams:
                dados = re.compile('(.+?)[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|](.*)').findall(stream)
                url = dados[0][0]
                conta_id_vi = dados[0][1]
                conta_id_video = int(conta_id_vi)
                conta_os_it = dados[0][2]
                conta_os_items = int(conta_os_it)
                nomeescolha = dados[0][3]
                iconimage = dados[0][4]
                fanart = dados[0][5]
                i = i + 1
                a = str(i)
                if i < 10: a = '0'+a
                TPT = threading.Thread(name='TPT'+str(i), target=TPT_resolve_not_videomega_filmes , args=(url,conta_id_video,conta_os_items,str(nomeescolha),str(iconimage),str(fanart),))
                threads.append(TPT)

        [i.start() for i in threads]
        [i.join() for i in threads]

def TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart):
        conta_id_video = int(conta_id_video)
        conta_os_items = int(conta_os_items)
        #addLink('vai','','','')
        
        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                url = url + '///' + nomeescolha
        
        if "videomega" in url:
		try:
                        fonte_id = '(Videomega)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',urltrailer,30,iconimage,'',fanart)
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
			if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id1.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
        if "dropvideo" in url:
		try:
                        url = url.replace('/video/','/embed/')
                        fonte_id = '(DropVideo)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "vidzi.tv" in url:
                try:
                        fonte_id = '(Vidzi.tv)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "vodlocker" in url:
		try:
                        fonte_id = '(Vodlocker)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "played.to" in url:
                try:
                        fonte_id = '(Played.to)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "cloudzilla" in url:
                try:
                        fonte_id = '(Cloudzilla)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "divxstage" in url:
                try:
                        fonte_id = '(Divxstage)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "vidzen" in url:
                try:
                        fonte_id = '(Vidzen)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
	if "streamin.to" in url:
                try:
                        fonte_id = '(Streamin)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass                        
    	if "nowvideo" in url:
                try:
                        fonte_id = '(Nowvideo)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "primeshare" in url:
                try:
                        fonte_id = '(Primeshare)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videoslasher" in url:
                try:
                        fonte_id = '(VideoSlasher)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "sockshare" in url:
                try:
                        fonte_id = '(Sockshare)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "putlocker" in url:
                try:
                        url = url.replace('putlocker.com/embed/','firedrive.com/file/')
                        fonte_id = '(Firedrive)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	else:
                if "firedrive" in url:
                        try:
                                fonte_id = '(Firedrive)'+url
                                if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
                        except:pass
    	if "movshare" in url:
                try:
                        fonte_id = '(Movshare)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
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
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:                     
                                url = url + '///' + nomeescolha
                        fonte_id = '(Video.tt)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(VideoWood)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "video.pw" in url:
                try:
                        print url
                        fonte_id = '(Video.pw)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "thevideo.me" in url:
                try:
                        #if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(Thevideo.me)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	#addLink(url,'','','')
##        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-serie' not in nomeescolha and 'Minisérie' not in nomeescolha and 'Miniserie' not in nomeescolha:
##                if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url and 'sockshare' not in url and 'firedrive' not in url and 'movshare' not in url and 'nowvideo' not in url and 'putlocker' not in url:# and 'iiiiiiiiii' in url:
##                        Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'').replace(url+'///'+nomeescolha,'')+'[/COLOR][/B]',iconimage,'',fanart)
    	return fonte_id

def ultimos_episodios_TPT_ultimos(url):

        try: xbmcgui.Dialog().notification('A Procurar Últimos Episódios.', 'Por favor aguarde...', artfolder + 'TPT1.png', 2000, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, 2000, %s)" % ('A Procurar Últimos Episódios.', 'Por favor aguarde...', artfolder + 'TPT1.png'))

        
##        percent = 0
##        message = 'Por favor aguarde.'
##        progress.create('Progresso', 'A Procurar')
##        progress.update( percent, 'A Procurar Últimos Episódios...', message, "" )

        #----------------------------------------------------------------------------------------------------
        threads = []
        
        i = 0
        try:
                try:
                        html_source = abrir_url(url)
                except: html_source = ''
                itemsTPT = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
                #addLink(str(len(itemsTPT)),'','','')
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
        except: pass

        [i.start() for i in threads]

        [i.join() for i in threads]
        
##        _sites_ = ['filmesTPT.txt','filmesTFV.txt']
##        folder = perfil
##        num_filmes = 0
##        
##        for site in _sites_:
##                _filmes_ = []
##                Filmes_Fi = open(folder + site, 'r')
##                read_Filmes_File = ''
##                for line in Filmes_Fi:
##                        read_Filmes_File = read_Filmes_File + line
##                        if line!='':_filmes_.append(line)
##
##                for x in range(len(_filmes_)):
##                        _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_filmes_[x])
##                        if _n: nome = _n[0]
##                        else: nome = '---'
##                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_filmes_[x])
##                        if _i: imdbcode = _i[0]
##                        else: imdbcode = '---'
##                        urltrailer = re.compile('(.+?)IMDB.+?MDB').findall(imdbcode)
##                        if urltrailer: urltrailer = urltrailer[0]
##                        else: urltrailer = '---'
##                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_filmes_[x])
##                        if _t: thumb = _t[0]
##                        else: thumb = '---'
##                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_filmes_[x])
##                        if _a: ano_filme = _a[0]
##                        else: ano_filme = '---'
##                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_filmes_[x])
##                        if _f: fanart = _f[0]
##                        else: fanart = ''
##                        if fanart == '---': fanart = ''
##                        _g = re.compile('[|]GENERO[|](.+?)[|]ONOME[|]').findall(_filmes_[x])
##                        if _g: genero = _g[0]
##                        else: genero = '---'
##                        _o = re.compile('[|]ONOME[|](.+?)[|]SINOPSE[|]').findall(_filmes_[x])
##                        if _o: O_Nome = _o[0]
##                        else: O_Nome = '---'
##                        _p = re.compile('PAGINA[|](.+?)[|]PAGINA').findall(_filmes_[x])
##                        if _p: P_url = _p[0]
##                        else: P_url = '---'
##                        _s = re.compile('[|]SINOPSE[|](.*)').findall(_filmes_[x])
##                        if _s: s = _s[0]
##                        if '|END|' in s: sinopse = s.replace('|END|','')
##                        else:
##                                si = re.compile('SINOPSE[|](.+?)\n(.+?)[|]END[|]').findall(_filmes_[x])
##                                if si: sinopse = si[0][0] + ' ' + si[0][1]
##                                else: sinopse = '---'
##                        if 'toppt.net'         in imdbcode: num_mode = 233
##                        if 'tuga-filmes.us'    in imdbcode: num_mode = 42
##                        if nome != '---':
##                                num_filmes = num_filmes + 1
##                                addDir_trailer(nome,imdbcode,num_mode,thumb,sinopse,fanart,ano_filme,genero,O_Nome,urltrailer)
##                        else:
##                                if 'toppt.net'         in P_url: url_TPT = P_url
##                                if 'tuga-filmes.us'    in P_url: url_TFV = P_url
##
##                Filmes_Fi.close()
##
        _sites_ = ['filmesTPT.txt']
        folder = perfil
        num_filmes = 0
        for site in _sites_:
                _filmes_ = []
                Filmes_Fi = open(folder + site, 'r')
                read_Filmes_File = ''
                for line in Filmes_Fi:
                        read_Filmes_File = read_Filmes_File + line
                        if line!='':_filmes_.append(line)

                for x in range(len(_filmes_)):
                        num_filmes = num_filmes + 1
        Filmes_Fi.close()
        num_total = num_filmes + 0.0
        percent = 0
        progress.create('Progresso', 'A Procurar')
        for a in range(num_filmes):
                percent = int( ( a / num_total ) * 100)
                message = str(a+1) + " de " + str(num_filmes)
                progress.update( percent, 'A Finalizar ...', message, "" )
                xbmc.sleep(20)

        proxima = re.compile('</span><a class="nextpostslink" rel="next" href="(.+?)">&raquo;</a><a class="last"').findall(html_source)
        try:
                addDir("Página Seguinte >>",proxima[0].replace('#038;','').replace('&amp;','&'),260,artfolder + 'PAGS1.png','','')
        except:pass

        progress.close()

        
def ultimos_ep_TPT(item):

        folder = perfil
        Filmes_File = open(folder + 'filmesTPT.txt', 'w')
        
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
                        qualid = re.compile("<b>QUALIDADE:.+?/b>(.+?)<br").findall(item)
                        if not qualid: qualid = re.compile("<b>VERSÃO:.+?</b>(.+?)<br").findall(item)
                        if qualid:
                                qualidade = qualid[0]
                                qualidade = qualidade.replace('[',' - ')
                                qualidade = qualidade.replace(']','')
                        else:
                                qualid = re.compile("\nQUALIDADE:\xc2\xa0(.+?)<br").findall(item)
                                if qualid:
                                        qualidade = qualid[0]
                                        qualidade = qualidade.replace('[',' - ')
                                        qualidade = qualidade.replace(']','')
                                else:
                                        qualid = re.compile("<b>VERS.+?</b>(.+?)<br").findall(item)
                                        if qualid:
                                                qualidade = qualid[0]
                                                qualidade = qualidade.replace('[',' - ')
                                                qualidade = qualidade.replace(']','')
                                        else:
                                                qualidade = ''

                        genr = re.compile("NERO:.+?/b>(.+?)<br").findall(item)
                        if genr: genero = genr[0]

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
                        ano = re.compile("<b>ANO:.+?/b>(.+?)<br").findall(item)
                        audio = re.compile("<b>AUDIO:.+?/b>(.+?)<br").findall(item)
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
                                audio = re.compile("\nAUDIO:\xc2\xa0(.+?)<br").findall(item)
                                if audio:
                                        audio_filme = ': ' + audio[0]
                                else:
                                        audio_filme = ''
                        if not ano:
                                ano = re.compile("\nANO:\xc2\xa0(.+?)<br").findall(item)
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
                                TPT_Ultimos(nome_fi,urletitulo[0][0]+'IMDB'+str(imdbcode)+'IMDB',thumb,fanart,item)
                        except: pass
                except: pass
        else: pass
        
        filmesTPT.sort()
        for x in range(len(filmesTPT)):
                Filmes_File.write(str(filmesTPT[x]))
        #Filmes_File.write('PAGINA|'+url_TPT+'|PAGINA')
        Filmes_File.close()

        #----------------------------------------------------------------------------------------------------

def TPT_Ultimos(name,url,iconimage,fanart,item):
        #addLink(name,'',iconimage,fanart)
        if 'Season' in name or 'Temporada' in name or 'Mini-Série' in name or 'Mini-serie' in name or 'Minisérie' in name or 'Miniserie' in name:
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
                if temporada == '': temporada = '0'
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

                tvdbid = thetvdb_api_tvdbid()._id(n_pesquisa,anne)
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
	nome_antes = '[B][COLOR green]' + namet + '[/COLOR][/B] | '
	if link2:
                if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo and 'Mini-serie' not in nometitulo and 'Minisérie' not in nometitulo and 'Miniserie' not in nometitulo:
                        newmatch = re.findall('<span id=.+?DOWNLOAD',link2,re.DOTALL)
                        if not newmatch: newmatch = re.findall('<span id=.+?BAIXAR',link2,re.DOTALL)
                        l=1
                else:
                        #newmatch = re.findall('<span id=.+?<img style="height: 40px; width: 465px;"',link2,re.DOTALL)
                        newmatch1 = re.findall('<span id=.+?DOWNLOAD POR',link2,re.DOTALL)
                        if not newmatch1: newmatch1 = re.findall('<span id=.+?BAIXAR',link2,re.DOTALL)
                        newmatch = re.findall('<img style="height: 90px; width: 200px;".+?DOWNLOAD POR',link2,re.DOTALL)
                        if not newmatch: newmatch = re.findall('<img style="height: 90px; width: 200px;".+?BAIXAR',link2,re.DOTALL)
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
                        
                linkseries = re.findall('<span class="su-spoiler-icon"></span>(.+?)</div>(.+?)BAIXAR',link2,re.DOTALL)
                if not linkseries: linkseries = re.findall('<h2>(.+?)</h2>\n(.+?)DOWNLOAD POR',link2,re.DOTALL)
                #if linkseries: addLink(linkseries[0][1],'','','')
                if not linkseries: linkseries = re.findall('<h2>(.+?)</h2>(.+?)BAIXAR',link2,re.DOTALL)
                if not linkseries: linkseries = re.findall('</span>CLIQUE AQUI PARA VER O (.+?)</div>(.+?)</div></div>',link2,re.DOTALL)
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
                #addLink(str(l),'','','')
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
                                                
##                                match = re.compile('<span class="su-lightbox" data-mfp-src="(.+?)" data-mfp-type="iframe">').findall(linkseries[0][1])
##                                for url in match:
##                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
##                                                conta_id_video = conta_id_video + 1
##                                                conta_os_items = conta_os_items + 1
##                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
##                                                if "videomega" in url: fonte_id = '(Videomega)'+urltrailer
##                                                if f_id == '': f_id = fonte_id
##                                                else: f_id = f_id + '|' + fonte_id
                                match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(linkseries[0][1])
                                for url in match:
                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                conta_id_video = conta_id_video + 1
                                                conta_os_items = conta_os_items + 1
                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                if "videomega" in url: fonte_id = '(Videomega)'+urltrailer
                                                if f_id == '': f_id = fonte_id
                                                else: f_id = f_id + '|' + fonte_id
                                match = re.compile('"window.open(.+?)"').findall(linkseries[0][1])
                                for url in match:
                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                conta_id_video = conta_id_video + 1
                                                url = url.replace("'","").replace("(","").replace(")","")
                                                conta_os_items = conta_os_items + 1
                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                if "videomega" in url: fonte_id = '(Videomega)'+urltrailer
                                                if f_id == '': f_id = fonte_id
                                                else: f_id = f_id + '|' + fonte_id
                                match = re.compile('src="(.+?)"').findall(linkseries[0][1])
                                for url in match:
                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                conta_id_video = conta_id_video + 1
                                                url = url.replace("'","").replace("(","").replace(")","")
                                                conta_os_items = conta_os_items + 1
                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                if "videomega" in url: fonte_id = '(Videomega)'+urltrailer
                                                if f_id == '': f_id = fonte_id
                                                else: f_id = f_id + '|' + fonte_id
                                match = re.compile('SRC="(.+?)"').findall(linkseries[0][1])
                                #if match: addLink(str(l),'','','')
                                for url in match:
                                        if "videomega" in url or "vidto.me" in url or "video.pw" in url or "thevideo.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                conta_id_video = conta_id_video + 1
                                                url = url.replace("'","").replace("(","").replace(")","")
                                                conta_os_items = conta_os_items + 1
                                                fonte_id = TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                                if "videomega" in url: fonte_id = '(Videomega)'+urltrailer
                                                if f_id == '': f_id = fonte_id
                                                else: f_id = f_id + '|' + fonte_id
                                try:

                                        #label = temporada + 'x' + '%02d' % int(episodiot) + ' . ' + epi_nome
                                        mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                        addDir_episode1_true(nome_antes+'[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,iconimage,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)
                                except:
                                        if 'EPI' not in linkseries[0][0] and 'Epi' not in linkseries[0][0]: parte1 = linkseries[0][0]+'º EPISÓDIO'
                                        mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+anne
                                        addDir_episode1_true(nome_antes+'[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+parte1+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,0)

                                f_id = ''
                                i = i + 1
                        except: pass

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

