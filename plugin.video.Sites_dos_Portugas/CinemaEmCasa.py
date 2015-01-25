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



import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,FilmesAnima,Play
from Funcoes import thetvdb_api, themoviedb_api, themoviedb_api_tv, theomapi_api, themoviedb_api_IMDB, themoviedb_api_IMDB_episodios, themoviedb_api_TMDB
from Funcoes import thetvdb_api_tvdbid, thetvdb_api_episodes, themoviedb_api_search_imdbcode, themoviedb_api_pagina, themoviedb_api_IMDB1, theomapi_api_nome
from Funcoes import addDir, addDir1, addDir2, addLink, addLink1, addDir_teste, addDir_trailer, addDir_episode
from Funcoes import get_params,abrir_url

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

progress = xbmcgui.DialogProgress()

Anos = ['' for i in range(100)]
#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#



def CMC_MenuPrincipal(artfolder):
        addDir('- Procurar','http://www.tuga-filmes.com/search?q=',1,artfolder + 'P1.png','nao','')
	addDir1('[COLOR blue]Filmes:[/COLOR]','url',1002,artfolder + 'CMC1.png',False,'')
	addDir('[COLOR yellow]- Todos[/COLOR]','http://www.cinemaemcasa.pt/',902,artfolder + 'FT.png','nao','')
	addDir('[COLOR yellow]- Animação[/COLOR]','http://www.cinemaemcasa.pt/search/label/Anima%C3%A7%C3%A3o',902,artfolder + 'FA.png','nao','')
	addDir('[COLOR yellow]- Categorias[/COLOR]','url',906,artfolder + 'CT.png','nao','')
	addDir('[COLOR yellow]- Por Ano[/COLOR]','url',907,artfolder + 'ANO.png','nao','')
	addDir('[COLOR yellow]- Top Semanal[/COLOR]','http://www.cinemaemcasa.pt/',905,artfolder + 'TPSE.png','nao','')
	

def CMC_Menu_Filmes_Por_Categorias(artfolder):
        url_categorias = 'http://www.cinemaemcasa.pt/'
        html_categorias_source = abrir_url(url_categorias)
	html_items_categorias = re.findall("<div class='widget-content list-label-widget-content'>(.*?)<div class='clear'></div>", html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<a dir='ltr' href='(.+?)'>\n(.+?)\n</a>").findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        addDir('[COLOR yellow]' + nome_categoria + '[/COLOR]',endereco_categoria,902,artfolder + 'CMC1.png','nao','')

def CMC_Menu_Filmes_Por_Ano(artfolder):
        i = 0
        url_categorias = 'http://www.cinemaemcasa.pt/'
        html_categorias_source = abrir_url(url_categorias)
	html_items_categorias = re.findall("<h2>Ano</h2>(.*?)<div class='clear'></div>", html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<a dir='ltr' href='(.+?)'>(\d+)</a>\n").findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        #addDir('[COLOR yellow]' + nome_categoria + '[/COLOR]',endereco_categoria,902,artfolder + 'CMC1.png','nao','')
                        Anos[i] = nome_categoria+'|'+endereco_categoria+'|'
                        i = i + 1
        Anos.sort()
        Anos.reverse()
        for x in range(len(Anos)):
                if Anos[x] != '':
                        A = re.compile('(.+?)[|](.+?)[|]').findall(Anos[x])
                        if A:
                                addDir('[COLOR yellow]' + A[0][0] + '[/COLOR]',A[0][1],902,artfolder + 'FTT1.png','nao','')

def CMC_Menu_Filmes_Top_Semanal(artfolder):
        progress = xbmcgui.DialogProgress()
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
        url = 'http://www.cinemaemcasa.pt/'
        try:
		html5_source = abrir_url(url)
	except: html5_source = ''
        items5 = re.findall("<div class='item-thumbnail'>(.+?)<div class='item-title'>", html5_source, re.DOTALL)
        print len(items5)
        num = len(items5) + 0.0
        #return
        for ites in items5:
                percent = int( ( i / num ) * 100)
                message = str(i) + " de " + str(int(num))
                progress.update( percent, "", message, "" )
                print str(i) + " de " + str(int(num))
                if progress.iscanceled():
                        break
                endereco = re.compile("<a href='(.+?)' target='_blank'>").findall(ites)
                try:
                        html_source = abrir_url(endereco[0])
                except: html_source = ''
                
                items = re.findall("<h1 class='post-title entry-title'>(.+?)<div class='post-footer'>", html_source, re.DOTALL)
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
                                                addDir_trailer('[B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',urlfilme.replace(' ','%20')+'IMDB'+imdbcode+'IMDB',903,thumb.replace(' ','%20'),sinopse,fanart,ano_filme,genero,nome,urlfilme) 
                                except: pass

                else: pass
                #---------------------------------------------------------------
                i = i + 1
                #---------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#

		

def CMC_encontrar_fontes_filmes(url):
        progress = xbmcgui.DialogProgress()
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
        try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall("<h2 class='post-title entry-title'>(.+?)<div class='post-footer'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		num = len(items) + 0.0
		for item in items:
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(len(items))
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(len(items))
                        if progress.iscanceled():
                                break
                        
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
                                        addDir_trailer('[B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',urlfilme.replace(' ','%20')+'IMDB'+imdbcode+'IMDB',903,thumb.replace(' ','%20'),sinopse,fanart,ano_filme,genero,nome,urlfilme) 
                        except: pass
                        #---------------------------------------------------------------
                        i = i + 1
                        #---------------------------------------------------------------
	proxima = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
	try:
                proxima_p = proxima[0].replace('%3A',':')
		addDir("[B]Página Seguinte >>[/B]",proxima_p.replace('&amp;','&'),902,artfolder + 'PAGS1.png','','')
	except: pass



#----------------------------------------------------------------------------------------------------------------------------------------------#

def CMC_encontrar_videos_filmes(name,url,mvoutv):
        if mvoutv == 'MoviesCMC':
                try: xbmcgui.Dialog().notification('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png', 3000, sound=False)
                except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % ('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png'))
        else:
                try: xbmcgui.Dialog().notification('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png', 10000, sound=False)
                except: xbmc.executebuiltin("Notification(%s,%s, 10000, %s)" % ('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png'))
        site = '[B][COLOR green]CINEM[/COLOR][COLOR yellow]A[/COLOR][COLOR red]EMCASA[/COLOR][/B]'
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
        if 'CMC' not in name: name = '[COLOR orange]CMC | [/COLOR]' + name
        nomeescolha = name
        colecao = 'nao'
        ########################################
        n1 = ''
        n2 = ''
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
##        nn = nomeescolha.replace('[B][COLOR green]','--').replace('[/COLOR][/B]','--').replace('[COLOR orange]','').replace('CMC | ','')
##        n = re.compile('--(.+?)--').findall(nn)
##        addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n[0],'url',1004,iconimage,False,fanart)
        ########################################
        if imdbcode == '' or '---' in imdbcode:
                ano_pp = re.compile('[[]COLOR yellow[]](.+?)[[]/COLOR[]]').findall(name)
                if ano_pp: ano_pesquisa = ano_pp[0].replace('(','').replace(')','')
                else: ano_pesquisa = ''
                conta = 0
##                nome_pesquisa = n[0] + ' ' + ano_pesquisa
                nome_pesquisa = n1 + ' ' + ano_pesquisa
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
                if imdbc: imdbcode = imdbc[0]

        if n1 != '' and n2 != '':
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
                addDir('[COLOR yellow]PROCURAR POR: [/COLOR]'+n2,'IMDB'+imdbcode+'IMDB',7,iconimage,'',fanart)
        else:
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
                
        addDir1(name,'url',1002,iconimage,False,fanart)
        conta_id_video = 0
        conta_os_items = 0
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

##        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(nomeescolha)
##        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
##        nn = nomeescolha.replace('[B][COLOR green]','--').replace('[/COLOR][/B]','--').replace('[COLOR orange]','').replace('CMC | ','')
##        n = re.compile('--(.+?)--').findall(nn)
##        url = 'IMDB'+imdbcode+'IMDB'
##        FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n[0]),'CMC',url)
        #addLink(imdbcode,'','')
        url = 'IMDB'+imdbcode+'IMDB'
        if mvoutv != 'MoviesCMC': FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n1),'CMC',url)

#-------------------------------------------------------------------------------------------------------------------------------

def CMC_resolve_not_videomega_filmesll(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart):
        
        
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
                        
                        fonte_id = '(Video.tt)'+url
                        url = url + '///' + nomeescolha
                        fonte_id1 = '(Video.tt)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id1.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
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
                        Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',iconimage,'',fanart)
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


def CMC_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart):
        
        
        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                url = url + '///' + nomeescolha
        
        if "videomega" in url:
		try:
                        fonte_id = '(Videomega)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
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
			if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id1.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
        if "dropvideo" in url:
		try:
                        url = url.replace('/video/','/embed/')
                        fonte_id = '(DropVideo)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
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
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "played.to" in url:
                try:
                        fonte_id = '(Played.to)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "cloudzilla" in url:
                try:
                        fonte_id = '(Cloudzilla)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "divxstage" in url:
                try:
                        fonte_id = '(Divxstage)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "vidzen" in url:
                try:
                        fonte_id = '(Vidzen)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
	if "streamin.to" in url:
                try:
                        fonte_id = '(Streamin)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
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
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videoslasher" in url:
                try:
                        fonte_id = '(VideoSlasher)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
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
                        
                        fonte_id = '(Video.tt)'+url
                        url = url + '///' + nomeescolha
                        fonte_id1 = '(Video.tt)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id1.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(VideoWood)'+url
                        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',url,30,iconimage,'',fanart)
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
##        if 'Season' not in nomeescolha and 'Temporada' not in nomeescolha and 'Mini-Série' not in nomeescolha and 'Mini-Serie' not in nomeescolha:
##                if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url and 'sockshare' not in url and 'firedrive' not in url and 'movshare' not in url and 'nowvideo' not in url and 'putlocker' not in url:# and 'iiiiiiiiii' in url:
##                        Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id.replace(url,'')+'[/COLOR][/B]',iconimage,'',fanart)
    	return fonte_id
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

