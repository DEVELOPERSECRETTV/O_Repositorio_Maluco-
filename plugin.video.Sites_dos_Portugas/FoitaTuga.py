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


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,os,FilmesAnima,Play,threading
from Funcoes import thetvdb_api, themoviedb_api, themoviedb_api_tv, theomapi_api, themoviedb_api_IMDB, themoviedb_api_IMDB_episodios, themoviedb_api_TMDB
from Funcoes import thetvdb_api_tvdbid, thetvdb_api_episodes, themoviedb_api_search_imdbcode, themoviedb_api_pagina, themoviedb_api_IMDB1, theomapi_api_nome
from Funcoes import addDir, addDir1, addDir2, addLink, addLink1, addDir_teste, addDir_trailer, addDir_episode, addDir_trailer1, addDir_episode1
from Funcoes import get_params,abrir_url
from array import array

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
perfil = xbmc.translatePath(selfAddon.getAddonInfo('profile'))

progress = xbmcgui.DialogProgress()

Anos = ['' for i in range(100)]
filmes = []

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#



def FTT_MenuPrincipal(artfolder):
        addDir('- Procurar','http://www.tuga-filmes.com/search?q=',1,artfolder + 'P1.png','nao','')
	addDir1('[COLOR blue]Filmes:[/COLOR]','url',1002,artfolder + 'FTT1.png',False,'')
	addDir('[COLOR yellow]- Todos[/COLOR]','http://foitatugadownload.blogspot.pt/',602,artfolder + 'FT.png','nao','')
	addDir('[COLOR yellow]- Animação[/COLOR]','http://foitatugadownload.blogspot.pt/search/label/Anima%C3%A7%C3%A3o',602,artfolder + 'FA.png','nao','')
	addDir('[COLOR yellow]- Categorias[/COLOR]','url',606,artfolder + 'CT.png','nao','')
	addDir('[COLOR yellow]- Por Ano[/COLOR]','url',606,artfolder + 'ANO.png','nao','')          #608
	addDir('[COLOR yellow]- Top + Vistos[/COLOR]','http://foitatugadownload.blogspot.pt/',602,artfolder + 'T10V.png','nao','')

def FTT_Menu_Filmes_Por_Categorias(artfolder):
        i = 0
        url_categorias = 'http://foitatugadownload.blogspot.pt/'
        html_categorias_source = abrir_url(url_categorias)
	if name == '[COLOR yellow]- Categorias[/COLOR]':
                html_items_categorias = re.findall("'http://foitatugadownload.blogspot.pt/search/label/2014'>2014(.*?)<div id='searchbarright'>", html_categorias_source, re.DOTALL)
                if not html_items_categorias: html_items_categorias = re.findall(">CATEGORIAS</a>(.*?)<div id='searchbarright'>", html_categorias_source, re.DOTALL)
                if not html_items_categorias: html_items_categorias = re.findall(">FILMES</a>(.*?)<div style='clear:both;'>", html_categorias_source, re.DOTALL)
                if not html_items_categorias: html_items_categorias = re.findall("<h2>CATEGORIAS</h2>(.*?)<div class='clear'>", html_categorias_source, re.DOTALL)
                print len(html_items_categorias)
                for item_categorias in html_items_categorias:
                        filmes_por_categoria = re.compile("<option value='(.+?)'>(.+?)\n.+?[(](.+?)[)]\n.+?</option>").findall(item_categorias)
                        if not filmes_por_categoria: filmes_por_categoria = re.compile("<a dir='ltr' href='(.+?)'>(.+?)</a>").findall(item_categorias)
                        if not filmes_por_categoria: filmes_por_categoria = re.compile("<option value='(.+?)'>(.+?)\n</option>").findall(item_categorias)
                        if not filmes_por_categoria: filmes_por_categoria = re.compile("<li><a href='(.+?)'>(.+?)</a></li>").findall(item_categorias)
##                        for endereco_categoria,nome_categoria,total_categoria in filmes_por_categoria:
##                                addDir('[COLOR yellow]' + nome_categoria + '[/COLOR] ('+total_categoria+')',endereco_categoria,602,artfolder + 'FTT1.png','nao','')
                        for endereco_categoria,nome_categoria in filmes_por_categoria:
                                if 'ANO' not in nome_categoria: addDir('[COLOR yellow]' + nome_categoria + '[/COLOR]',endereco_categoria,602,artfolder + 'FTT1.png','nao','')
	if name == '[COLOR yellow]- Por Ano[/COLOR]':
                ano = 2015
                for x in range(46):
                        categoria_endereco = 'http://foitatugadownload.blogspot.pt/search/label/' + str(ano) #+ '#_'
                        addDir('[COLOR yellow]' + str(ano) + '[/COLOR]',categoria_endereco,602,artfolder + 'FTT1.png','nao','')
                        ano = ano - 1
##                html_items_categorias = re.findall("<option>ESCOLHA A CATEGORIA</option>(.*?)='http://foitatugacinemaonline.blogspot.pt/search/label/ANIMA%C3%87%C3%83O'", html_categorias_source, re.DOTALL)
##                if not html_items_categorias: html_items_categorias = re.findall("<h2>FILMES POR ANO</h2>(.*?)<div class='clear'>", html_categorias_source, re.DOTALL)
##                print len(html_items_categorias)
##                for item_categorias in html_items_categorias:
##                        filmes_por_categoria = re.compile("<option value='(.+?)'>(.+?)\n.+?[(](.+?)[)]\n.+?</option>").findall(item_categorias)
##                        if not filmes_por_categoria: filmes_por_categoria = re.compile("<a dir='ltr' href='(.+?)'>(.+?)</a>").findall(item_categorias)
##                        if not filmes_por_categoria: filmes_por_categoria = re.compile("<option value='(.+?)'>(.+?)\n</option>").findall(item_categorias)
##                        for endereco_categoria,nome_categoria in filmes_por_categoria:
##                                Anos[i] = nome_categoria+'|'+endereco_categoria+'|'
##                                i = i + 1
####                        for endereco_categoria,nome_categoria,total_categoria in filmes_por_categoria:
####                                Anos[i] = nome_categoria+'|'+endereco_categoria+'|'+total_categoria
####                                i = i + 1
##                Anos.sort()
##                Anos.reverse()
##                for x in range(len(Anos)):
##                        if Anos[x] != '':
##                                A = re.compile('(.+?)[|](.+?)[|]').findall(Anos[x])
##                                if A:
##                                        addDir('[COLOR yellow]' + A[0][0] + '[/COLOR]',A[0][1],602,artfolder + 'FTT1.png','nao','')
####                                A = re.compile('(.+?)[|](.+?)[|](.*)').findall(Anos[x])
####                                if A:
####                                        addDir('[COLOR yellow]' + A[0][0] + '[/COLOR] ('+A[0][2]+')',A[0][1],602,artfolder + 'FTT1.png','nao','')


def FTT_Top_Vistos(item_categorias):

        if item_categorias != '':
                
                anofilme = ''
                imdbcode = ''
                fanart = ''
                thumb = ''
                sinopse = ''
                genero = ''

                
                url_titulo = re.compile("<a href='(.+?)'>(.+?)</a>").findall(item_categorias)
                thumb_f = re.compile("src='(.+?)'").findall(item_categorias)
                if thumb_f: thumb = thumb_f[0]
                nome_f = url_titulo[0][1]
                a_q = re.compile('\d+')
                qq_aa = a_q.findall(nome_f)
                for q_a_q_a in qq_aa:
                        if len(q_a_q_a) == 4:
                                anofilme = str(q_a_q_a)
                                tirar_ano = '- ' + str(q_a_q_a)
                                nome_f = nome_f.replace(tirar_ano,'')
                                tirar_ano = '-' + str(q_a_q_a)
                                nome_f = nome_f.replace(tirar_ano,'')
                                tirar_ano = str(q_a_q_a)
                                nome_f = nome_f.replace(tirar_ano,'')

                try:
                        fonte_video = abrir_url(url_titulo[0][0])
                except: fonte_video = ''
                fontes_video = re.findall("<h3 class='post-title entry-title'>(.*?)<div class='post-footer'>", fonte_video, re.DOTALL)
                if not fontes_video: fontes_video = re.findall("<div class='post-body entry-content'(.*?)<div style='clear: both;'>", fonte_video, re.DOTALL)
                if not fontes_video: fontes_video = re.findall("<div class='video-item'>(.*?)<div class='clear'>", fonte_video, re.DOTALL)
                if fontes_video != []:
                        snpse = re.compile('Sinopse.png"></a></div>\n(.+?)\n').findall(fontes_video[0])
                        if not snpse: snpse = re.compile('Sinopse.png" /></a></div>\n(.+?)\n').findall(fontes_video[0])
                        if not snpse: snpse = re.compile('<div class="separator" style="clear: both; text-align: center;">\n(.+?)\n</div>\n<div class="separator" style="clear: both; text-align: center;">').findall(fontes_video[0])
                        if snpse: sinopse = snpse[0]
                        sinopse = sinopse.replace('&#8216;',"'")
                        sinopse = sinopse.replace('&#8217;',"'")
                        sinopse = sinopse.replace('&#8220;',"'")
                        sinopse = sinopse.replace('&#8221;',"'")
                        sinopse = sinopse.replace('&#8211;',"-")
                        sinopse = sinopse.replace('&#39;',"'")
                        sinopse = sinopse.replace('&amp;','&')
                        imdb = re.compile('imdb.com/title/(.+?)/').findall(fontes_video[0])
                        if imdb:
                                imdbcode = imdb[0]
                                #addLink(imdbcode,'','','')
                        else: imdbcode = ''
                        
                nome_f = nome_f.replace('&#8217;',"'")
                nome_f = nome_f.replace('&#8211;',"-")
                
                nome_f = nome_f.replace('&#39;',"'")
                nome_f = nome_f.replace('&amp;','&')
                nome_f = nome_f.replace('(Pedido)',"").replace('[Pedido]','')
                nome_f = nome_f.replace('[PT/PT]','')
                nome_f = nome_f.replace('[PT-PT]','')
                nome_f = nome_f.replace('[PT/BR]','')
                nome_f = nome_f.replace('[PT-BR]','')
                nome_f = nome_f.replace('PT/PT','')
                nome_f = nome_f.replace('PT-PT','')
                nome_f = nome_f.replace('PT/BR','')
                nome_f = nome_f.replace('PT-BR','')
                nome_f = nome_f.replace(' - ','')
                nome_f = nome_f.replace('&#;',"-")

                nnnn = re.compile('.+?[(](.+?)[)]').findall(nome_f)
                if not nnnn: nnnn = re.compile('.+?[[](.+?)[]]').findall(nome_f)
                if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome_f)
                if not nnnn: nnnn = re.compile('(.+?)[:] ').findall(nome_f)
                if nnnn : nome_pesquisa = nnnn[0]
                else: nome_pesquisa = nome_f
                if imdbcode != '':
                        try:
                                fanart,tmdb_id,poster,sin = themoviedb_api_IMDB().fanart_and_id(str(imdbcode),anofilme)
                                if sinopse == '' or 'style' in sinopse: sinopse = sin
                                if fanart == '': fanart,tmb,pter = themoviedb_api().fanart_and_id(nome_pesquisa,anofilme)
                                if thumb == ''  or 'IMDb.png' in thumb or 'Sinopse' in thumb: thumb = poster
                        except:pass
                else:
                        try:
                                fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,anofilme)
                                if thumb == ''  or 'IMDb.png' in thumb or 'Sinopse' in thumb: thumb = poster
                        except: pass
                
                if sinopse == '': sinopse = '---'
                if fanart == '---': fanart = ''
                if imdbcode == '': imdbcode = '---'
                try:
                        if 'Temporada' not in nome_f and 'temporada' not in nome_f and 'Season' not in nome_f and 'season' not in nome_f:
                                addDir_trailer('[B][COLOR green]' + nome_f + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR]',url_titulo[0][0]+'IMDB'+imdbcode+'IMDB',603,thumb.replace('s72-c','s320'),sinopse,fanart,anofilme,genero,nome_f,url_titulo[0][0])
                except: pass       


#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#
        
def FTT_encontrar_fontes_filmes(url):
        
##        percent = 0
##        message = 'Por favor aguarde.'
##        progress.create('Progresso', 'A Procurar')
##        progress.update( percent, 'A Procurar Filmes ...', message, "" )
        
        if name != '[COLOR yellow]- Top + Vistos[/COLOR]':
                try: xbmcgui.Dialog().notification('A Procurar Filmes.', 'Por favor aguarde...', artfolder + 'FTT1.png', 3000, sound=False)
                except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % ('A Procurar Filmes.', 'Por favor aguarde...', artfolder + 'FTT1.png'))
        if name == '[COLOR yellow]- Top + Vistos[/COLOR]':
                try: xbmcgui.Dialog().notification('A Procurar.', 'Por favor aguarde...', artfolder + 'FTT1.png', 3000, sound=False)
                except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % ('A Procurar.', 'Por favor aguarde...', artfolder + 'FTT1.png'))
        
        try:
		html_source = abrir_url(url)
	except: html_source = ''
	if name != '[COLOR yellow]- Top + Vistos[/COLOR]':#'[COLOR yellow]- Todos[/COLOR]' or name == "[B]Página Seguinte >>[/B]":
                items = re.findall("<h3 class='post-title entry-title'(.*?)<div class='post-footer'>", html_source, re.DOTALL)
                if not items: items = re.findall("<a class='comment-link'(.*?)<div class='post-outer'>", html_source, re.DOTALL)
                if not items: items = re.findall("<div class='video-item'>(.*?)<div class='clear'>", html_source, re.DOTALL)
        if name == '[COLOR yellow]- Top + Vistos[/COLOR]':
                html_items_categorias = re.findall("<div class='widget-content popular-posts'>(.*?)<div class='clear'>", html_source, re.DOTALL)
                items = re.findall("<div class='item-thumbnail'>(.*?)<div style='clear: both;'>", html_items_categorias[0], re.DOTALL)

        threads = []
        i = 0
        for item in items:
                if name != '[COLOR yellow]- Top + Vistos[/COLOR]':
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        Filmes_FTT = threading.Thread(name='Filmes_FTT'+str(i), target=Fontes_Filmes_FTT , args=('FILME'+str(a)+'FILME'+item,))
                if name == '[COLOR yellow]- Top + Vistos[/COLOR]':
                        Filmes_FTT = threading.Thread(name='Filmes_FTT'+str(i), target=FTT_Top_Vistos , args=(item,))
                threads.append(Filmes_FTT)

        [i.start() for i in threads]

        [i.join() for i in threads]

        if name != '[COLOR yellow]- Top + Vistos[/COLOR]':
                _sites_ = ['filmesFTT.txt']
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
                                if 'foitatuga'         in imdbcode: num_mode = 603
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

                proxima = re.compile("<a class='blog-pager-older-link' href='(.+?)' id='Blog1_blog-pager-older-link'").findall(html_source)	
                try:
                        proxima_p = proxima[0]#.replace('%3A',':').replace('%2B','+')
                        addDir("[B]Página Seguinte >>[/B]",proxima_p.replace('&amp;','&'),602,artfolder + 'PAGS1.png','','')
                except: pass
##	progress.close()

def Fontes_Filmes_FTT(item):
        
        folder = perfil
        Filmes_File = open(folder + 'filmesFTT.txt', 'w')
        
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

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''

                        urletitulo = re.compile("<a href='(.+?)'>(.+?)</a>").findall(item)
                        if not urletitulo: urletitulo = re.compile("<a href='(.+?)' title='(.+?)'>Ler mais").findall(item)
                        if not urletitulo: urletitulo = re.compile("<a href='(.+?)' title='(.+?)'>").findall(item)
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

##                        try:
##                                fonte_video = abrir_url(urlvideo)
##                        except: fonte_video = ''
##                        fontes_video = re.findall("<div class='post-body entry-content'>(.*?)<div style='clear: both;'>", fonte_video, re.DOTALL)
##                        if not fontes_video: fontes_video = re.findall("<div class='video-item'>(.*?)<div class='clear'>", fonte_video, re.DOTALL)
##                        if fontes_video != []:
##                                qualid = re.compile('ASSISTIR ONLINE (.*)\n').findall(fontes_video[0])
##                                if qualid: qualidade_filme = qualid[0].replace('/ ',' ').replace('</b>','').replace('</span>','').replace('LEGENDADO','')+audio_filme
##                                else:
##                                        qualid = re.compile('[[]</span><span style=".+?"><span style=".+?">(.+?)</span><span style=".+?">[]]').findall(fontes_video[0])
##                                        if qualid: qualidade_filme = qualid[0].replace('/ ','').replace('</b>','').replace('</span>','')+audio_filme
                        qualid = re.compile('ASSISTIR ONLINE (.*)\n').findall(item)
                        if qualid: qualidade_filme = qualid[0].replace('/ ',' ').replace('</b>','').replace('</span>','').replace('LEGENDADO','') + audio_filme
                        else:
                                qualid = re.compile('[[]</span><span style=".+?"><span style=".+?">(.+?)</span><span style=".+?">[]]').findall(item)
                                if not qualid: qualid = re.compile('VERS.+?:(.+?)[[]').findall(item)
                                if qualid: qualidade_filme = qualid[0].replace('/ ','').replace('</b>','').replace('</span>','').replace(' ','') + audio_filme
                                else: qualidade_filme = '---'
                                
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
                                        if sinopse == '' or '<div class="separator" style="clear: both; text-align: center;">' in sinopse: sinopse = sin
                                        if fanart == '': fanart,tmb,pter = themoviedb_api().fanart_and_id(nome_pesquisa,anofilme)
                                        if thumb == ''  or 'IMDb.png' in thumb or 'Sinopse' in thumb: thumb = poster
                                except:pass
                        else:
                                try:
                                        fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,anofilme)
                                        if thumb == ''  or 'IMDb.png' in thumb or 'Sinopse' in thumb: thumb = poster
                                except: pass
                                                
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        try:
                                if 'Temporada' not in nome and 'temporada' not in nome and 'Season' not in nome and 'season' not in nome:
                                        nome_final = '[B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme.replace('</div>','') + ')[/COLOR]'
                                        filmes.append(FILMEN+'NOME|'+str(nome_final.replace('  ',' '))+'|IMDBCODE|'+str(urlvideo)+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb)+'|ANO|'+str(anofilme)+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|ONOME|'+str(nome_pesquisa)+'|SINOPSE|'+str(sinopse)+'|END|\n')
                        except: pass
                except: pass	
        else: pass
        filmes.sort()
        for x in range(len(filmes)):
                Filmes_File.write(str(filmes[x]))
	Filmes_File.close()




#----------------------------------------------------------------------------------------------------------------------------------------------#

def FTT_encontrar_videos_filmes(name,url,mvoutv):
        if mvoutv == 'MoviesFTT':
                try: xbmcgui.Dialog().notification('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png', 3000, sound=False)
                except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % ('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png'))
        else:
                try: xbmcgui.Dialog().notification('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png', 10000, sound=False)
                except: xbmc.executebuiltin("Notification(%s,%s, 10000, %s)" % ('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png'))
        site = '[B][COLOR green]FOIT[/COLOR][COLOR yellow]A[/COLOR][COLOR red]TUGA[/COLOR][/B]'
##        message = 'Por favor aguarde.'
##        percent = 0
##        progress.create('Progresso', 'A Procurar...')
##        progress.update(percent, 'A Procurar em '+site, message, "")
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]
        if 'FTT' not in name: name = '[COLOR orange]FTT | [/COLOR]' + name
        nomeescolha = name
        colecao = 'nao'
        n1 = ''
        n2 = ''
        ################################################
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
                        n1 = nnnn[0]
        if not nnnn:
                nnnn = re.compile('(.+?)[:] ').findall(nnn[0])
                if nnnn:
                        n1 = nnnn[0]
        if not nnnn : n1 = nnn[0]

##        nn = nomeescolha.replace('[B][COLOR green]','--').replace('[COLOR orange]','').replace('[/COLOR][/B]','--').replace('[/COLOR]','').replace('[','---').replace(']','---')
##        nn = nn.replace('(','---').replace(')','---').replace('FTT | ','')
##        if '---' in nn:
##                n = re.compile('---(.+?)---').findall(nn)
##                n1 = re.compile('--(.+?)--').findall(nn)
##                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n[0],'url',1004,iconimage,False,fanart)
##                addDir('[COLOR yellow]PROCURAR POR: [/COLOR]'+n1[0],'IMDB'+imdbcode+'IMDB',7,iconimage,'',fanart)
##                nome_pesquisa = n1[0]
##        else:
##                n1 = re.compile('--(.+?)--').findall(nn)
##                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1[0],'url',1004,iconimage,False,fanart)
##                nome_pesquisa = n1[0]
        ################################################
        if imdbcode == '' or imdbcode == '---':
                conta = 0
                nome_pesquisa = n1
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
                imdbc = re.compile('/title/(.+?)/[?]ref').findall(filmes_imdb[0])
                imdbcode = imdbc[0]

        if n1 != '' and n2 != '':
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
                addDir('[COLOR yellow]PROCURAR POR: [/COLOR]'+n2,'IMDB'+imdbcode+'IMDB',7,iconimage,'',fanart)
        else:
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
                
            
        addDir1(name,'url',1002,iconimage,False,fanart)
        conta_id_video = 0
        try:
                fonte_video = abrir_url(url)
        except: fonte_video = ''
        fontes_video = re.findall("<h3 class='post-title entry-title'(.*?)<div class='post-footer'>", fonte_video, re.DOTALL)
        if not fontes_video: fontes_video = re.findall("<div class='post-body entry-content'>(.*?)<div style='clear: both;'>", fonte_video, re.DOTALL)
        if not fontes_video: fontes_video = re.findall("<div class='video-item'>(.*?)<div class='clear'>", fonte_video, re.DOTALL)
        numero_de_fontes = len(fontes_video)
        addLink(str(numero_de_fontes),'','','')
        #if 'BREVEMENTE ONLINE' in fonte_video: addDir1('[COLOR blue]BREVEMENTE ONLINE[/COLOR]','url',1004,artfolder,False,'')
        for fonte_e_url in fontes_video:
                if imdbcode == '':
                        imdb = re.compile('imdb.com/title/(.+?)/').findall(fonte_e_url)
                        if imdb: imdbcode = imdb[0]
                        #else: imdbcode = ''
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
                                                        #Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_serv+'[/COLOR][/B]',iconimage,'',fanart)
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',urltrailer,30,iconimage,'',fanart)
                                        if 'iframe.js' in fonte_id:
                                                conta_id_video = conta_id_video + 1
                                                refvideo = re.compile('<script type="text/javascript">ref="(.+?)".+?</script>').findall(fonte_e_url)
                                                if not refvideo: refvideo = re.compile(">ref='(.+?)'.+?</script>").findall(fonte_e_url)
                                                url = 'http://videomega.tv/iframe.php?ref=' + refvideo[0] + '///' + name
                                                fonte_serv = '(Videomega)'
                                                #Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_serv+'[/COLOR][/B]',iconimage,'',fanart)
                                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',urltrailer,30,iconimage,'',fanart)
                                except:pass
                match2 = re.compile('<iframe.+?src="(.+?)" .+?</iframe>').findall(fonte_e_url)
                if not match2: match2 = re.compile('<iframe.+?src="(.+?)".+?>').findall(fonte_e_url)
                if not match2: match2 = re.compile('<a href="(.+?)" target="_blank"><img border="0" src="http://1.bp.blogspot.com/-_yTINh6ZYdo/VNIWCpRm93I/AAAAAAAAAQk/akx68KoQ2VA/s1600/1.png"').findall(fonte_e_url)
                if not match2: match2 = re.compile('<a href="(.+?)" target="_blank"><img border="0" src=".+?VER%2BONLINE.jpg"').findall(fonte_e_url)

                for fonte_id in match2:
                        if 'videomega' in fonte_id:
                                try:
                                        conta_id_video = conta_id_video + 1
                                        url = fonte_id + '///' + name
                                        fonte_serv = '(Videomega)'
                                        #Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_serv+'[/COLOR][/B]',iconimage,'',fanart)
                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',urltrailer,30,iconimage,'',fanart)
                                except:pass
                        elif 'dropvideo' in fonte_id:
                                try:
                                        conta_id_video = conta_id_video + 1
                                        url = fonte_id + '///' + name
                                        fonte_serv = '(Dropvideo)'
                                        #Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_serv+'[/COLOR][/B]',iconimage,'',fanart)
                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Dropvideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                        elif 'vidto.me' in fonte_id:
                                try:
                                        conta_id_video = conta_id_video + 1
                                        fonte_id = fonte_id.replace('embed-','')
                                        refvideo = re.compile('http://vidto.me/embed-(.+?).html').findall(fonte_id)
                                        if refvideo: url = 'http://vidto.me/' + refvideo[0] + '.html' + '///' + name
                                        else: url = fonte_id + '///' + name
                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                        else:
                                conta_id_video = conta_id_video + 1
                                FTT_resolve_not_videomega_filmes(fonte_id,nomeescolha,conta_id_video,fanart,iconimage)
##        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(nomeescolha)
##        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
##        nn = nomeescolha.replace('[B][COLOR green]','--').replace('[COLOR orange]','').replace('[/COLOR][/B]','--').replace('[/COLOR]','').replace('[','---').replace(']','---')
##        nn = nn.replace('(','---').replace(')','---').replace('FTT | ','')
##
##        nnnn = re.compile('.+?[(](.+?)[)]').findall(nnn[0])
##        if not nnnn: nnnn = re.compile('.+?[[](.+?)[]]').findall(nnn[0])
##        if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nnn[0])
##        if not nnnn: nnnn = re.compile('(.+?)[:] ').findall(nnn[0])
##        if nnnn : nome_pesquisa = nnnn[0]
##        else: nome_pesquisa = nnn[0]
        #addLink(n1+imdbcode,'','')
        url = 'IMDB'+imdbcode+'IMDB'
        if mvoutv != 'MoviesFTT': FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n1),'FTT',url)
        
##        if '---' in nn:
##                n = re.compile('---(.+?)---').findall(nn)
##                n1 = re.compile('--(.+?)--').findall(nn)
##                url = 'IMDB'+imdbcode+'IMDB'
##                FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n[0]),'FTT',url)
##        else:
##                n1 = re.compile('--(.+?)--').findall(nn)
##                url = 'IMDB'+imdbcode+'IMDB'
##                FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n1[0]),'FTT',url)



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
        #addDir1(url+name,'url',1001,iconimage,False,fanart)
        fontes_video = re.findall("<h3 class='post-title entry-title'(.*?)<div class='post-footer'>", fonte_video, re.DOTALL)
        if not fontes_video: fontes_video = re.findall("<div class='post-body entry-content'>(.*?)<div style='clear: both;'>", fonte_video, re.DOTALL)
        if not fontes_video: fontes_video = re.findall("<div class='video-item'>(.*?)<div class='clear'>", fonte_video, re.DOTALL)
        numero_de_fontes = len(fontes_video)
        #if 'BREVEMENTE ONLINE' in fonte_video: addDir1('[COLOR blue]BREVEMENTE ONLINE[/COLOR]','url',1004,artfolder,False,'')
        for fonte_e_url in fontes_video:
                if imdbcode == '':
                        imdb = re.compile('imdb.com/title/(.+?)/').findall(fonte_e_url)
                        if imdb: imdbcode = imdb[0]
                        #else: imdbcode = ''
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
                                                        #Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_serv+'[/COLOR][/B]',iconimage,'',fanart)
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',urltrailer,30,iconimage,'',fanart)
                                        if 'iframe.js' in fonte_id:
                                                conta_id_video = conta_id_video + 1
                                                refvideo = re.compile('<script type="text/javascript">ref="(.+?)".+?</script>').findall(fonte_e_url)
                                                if not refvideo: refvideo = re.compile(">ref='(.+?)'.+?</script>").findall(fonte_e_url)
                                                url = 'http://videomega.tv/iframe.php?ref=' + refvideo[0] + '///' + name
                                                fonte_serv = '(Videomega)'
                                                #Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_serv+'[/COLOR][/B]',iconimage,'',fanart)
                                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',urltrailer,30,iconimage,'',fanart)
                                except:pass
                match2 = re.compile('<iframe.+?src="(.+?)".+?></iframe>').findall(fonte_e_url)
                if not match2: match2 = re.compile('<iframe.+?src="(.+?)".+?>').findall(fonte_e_url)
                if not match2: match2 = re.compile('<a href="(.+?)" target="_blank"><img border="0" src="http://1.bp.blogspot.com/-_yTINh6ZYdo/VNIWCpRm93I/AAAAAAAAAQk/akx68KoQ2VA/s1600/1.png"').findall(fonte_e_url)
                if not match2: match2 = re.compile('<a href="(.+?)" target="_blank"><img border="0" src=".+?VER%2BONLINE.jpg"').findall(fonte_e_url)

                for fonte_id in match2:
                        if 'videomega' in fonte_id:
                                try:
                                        conta_id_video = conta_id_video + 1
                                        url = fonte_id + '///' + name
                                        fonte_serv = '(Videomega)'
                                        #Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_serv+'[/COLOR][/B]',iconimage,'',fanart)
                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',urltrailer,30,iconimage,'',fanart)
                                except:pass
                        elif 'dropvideo' in fonte_id:
                                try:
                                        conta_id_video = conta_id_video + 1
                                        url = fonte_id + '///' + name
                                        fonte_serv = '(Dropvideo)'
                                        #Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_serv+'[/COLOR][/B]',iconimage,'',fanart)
                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Dropvideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                        elif 'vidto.me' in fonte_id:
                                try:
                                        conta_id_video = conta_id_video + 1
                                        fonte_id = fonte_id.replace('embed-','')
                                        refvideo = re.compile('http://vidto.me/embed-(.+?).html').findall(fonte_id)
                                        if refvideo: url = 'http://vidto.me/' + refvideo[0] + '.html' + '///' + name
                                        else: url = fonte_id + '///' + name
                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                        else:
                                conta_id_video = conta_id_video + 1
                                FTT_resolve_not_videomega_filmes(fonte_id,nomeescolha,conta_id_video,fanart,iconimage)


def FTT_resolve_not_videomega_filmes(url,nomeescolha,conta_id_video,fanart,iconimage):
        url = url + '///' + nomeescolha
        if "videomega" in url:
		try:
                        fonte_id = '(Videomega)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',urltrailer,30,iconimage,'',fanart)
		except: pass
        if "vidto.me" in url:
		try:
                        match = re.compile('http://vidto.me/embed-(.+?).html').findall(url)
			if match:
				id_video = match[0]
				url = 'http://vidto.me/' + id_video + '.html' + '///' + nomeescolha
			fonte_id = '(Vidto.me)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
	if "thevideo.me" in url:
		try:
                        fonte_id = '(TheVideo.me)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](TheVideo.me)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
        if "dropvideo" in url:
		try:
                        url = url.replace('/video/','/embed/')
                        fonte_id = '(DropVideo)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "vidzi.tv" in url:
                try:
                        fonte_id = '(Vidzi.tv)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidzi.tv)[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "vodlocker" in url:
		try:
                        fonte_id = '(Vodlocker)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vodlocker)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "played.to" in url:
                try:
                        fonte_id = '(Played.to)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Played.to)[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "cloudzilla" in url:
                try:
                        fonte_id = '(Cloudzilla)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Cloudzilla)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "divxstage" in url:
                try:
                        fonte_id = '(Divxstage)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Divxstage)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "vidzen" in url:
                try:
                        fonte_id = '(Vidzen)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidzen)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
	if "streamin.to" in url:
                try:
                        fonte_id = '(Streamin)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass                        
    	if "nowvideo" in url:
                try:
                        fonte_id = '(Nowvideo)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "primeshare" in url:
                try:
                        fonte_id = '(Primeshare)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Primeshare.tv)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videoslasher" in url:
                try:
                        fonte_id = '(VideoSlasher)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoSlasher)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "sockshare" in url:
                try:
                        fonte_id = '(Sockshare)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Sockshare)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "putlocker" in url:
                try:
                        url = url.replace('putlocker.com/embed/','firedrive.com/file/')
                        fonte_id = '(Firedrive)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	else:
                if "firedrive" in url:
                        try:
                                fonte_id = '(Firedrive)'
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                        except:pass
    	if "movshare" in url:
                try:
                        fonte_id = '(Movshare)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Movshare)[/COLOR][/B]',url,30,iconimage,'',fanart)
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
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Video.tt)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "video.pw" in url:
                try:
                        print url
                        fonte_id = '(Video.pw)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Video.pw)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(VideoWood)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoWood)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
##    	if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url and 'nowvideo' not in url:# and 'iiiiiiiiii' in url:
##                Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',iconimage,'',fanart)
    	return

def FTT_resolve_not_videomega_filmesll(url,nomeescolha,conta_id_video,fanart,iconimage):
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
				url = 'http://vidto.me/' + id_video + '.html' + '///' + nomeescolha
			fonte_id = '(Vidto.me)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
	if "thevideo.me" in url:
		try:
                        fonte_id = '(TheVideo.me)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](TheVideo.me)[/COLOR][/B]',url,30,iconimage,'',fanart)
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
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidzi.tv)[/COLOR][/B]',url,30,iconimage,'',fanart)
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
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
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
    		except:pass
    	if "putlocker" in url:
                try:
                        url = url.replace('putlocker.com/embed/','firedrive.com/file/')
                        fonte_id = '(Firedrive)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	else:
                if "firedrive" in url:
                        try:
                                fonte_id = '(Firedrive)'
                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                        except:pass
    	if "movshare" in url:
                try:
                        fonte_id = '(Movshare)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Movshare)[/COLOR][/B]',url,30,iconimage,'',fanart)
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
    	if "video.pw" in url:
                try:
                        print url
                        fonte_id = '(Video.pw)'
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(VideoWood)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoWood)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url and 'nowvideo' not in url:# and 'iiiiiiiiii' in url:
                Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',iconimage,'',fanart)
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
mvoutv=None

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
