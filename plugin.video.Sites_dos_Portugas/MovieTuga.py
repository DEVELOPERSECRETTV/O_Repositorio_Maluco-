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



import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,threading,FilmesAnima,Play
from Funcoes import thetvdb_api, themoviedb_api, themoviedb_api_tv, theomapi_api, themoviedb_api_IMDB, themoviedb_api_IMDB_episodios, themoviedb_api_TMDB
from Funcoes import thetvdb_api_tvdbid, thetvdb_api_episodes, themoviedb_api_search_imdbcode, themoviedb_api_pagina, themoviedb_api_IMDB1, theomapi_api_nome
from Funcoes import addDir, addDir1, addDir2, addLink, addLink1, addDir_teste, addDir_trailer, addDir_episode
from Funcoes import get_params,abrir_url
from array import array

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
perfil = xbmc.translatePath(selfAddon.getAddonInfo('profile'))

progress = xbmcgui.DialogProgress()
filmes = []
#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#



def MVT_MenuPrincipal(artfolder):
        addDir('- Procurar','http://www.tuga-filmes.com/search?q=',1,artfolder + 'P1.png','nao','')
	addDir1('[COLOR blue]Filmes:[/COLOR]','url',1002,artfolder + 'MVT1.png',False,'')
	addDir('[COLOR yellow]- Todos[/COLOR]','http://movie-tuga.blogspot.pt/',102,artfolder + 'FT.png','nao','')
	addDir('[COLOR yellow]- Animação[/COLOR]','http://movie-tuga.blogspot.pt/search/label/animacao',102,artfolder + 'FA.png','nao','')
	addDir('[COLOR yellow]- Categorias[/COLOR]','url',106,artfolder + 'CT.png','nao','')
	

def MVT_Menu_Filmes_Por_Categorias(artfolder):
        url_categorias = 'http://www.movie-tuga.blogspot.pt/'
        html_categorias_source = abrir_url(url_categorias)
	html_items_categorias = re.findall("<div id=\'menu-categorias\'>(.*?)</div>", html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<a href=\'(.+?)\' title=\'.+?\'>(.+?)</a>").findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        addDir('[COLOR yellow]' + nome_categoria + '[/COLOR]',endereco_categoria + '?&max-results=15',102,artfolder + 'MVT1.png','nao','')



#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#

		

def MVT_encontrar_fontes_filmes(url):
        
        percent = 0
        message = 'Por favor aguarde.'
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar Filmes ...', message, "" )
        
        try:
		html_source = abrir_url(url)
	except: html_source = ''
	if name != '':
                items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)

        threads = []
        i = 0
        for item in items:
                if name != '':
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        Filmes_MVT = threading.Thread(name='Filmes_MVT'+str(i), target=Fontes_Filmes_MVT , args=('FILME'+str(a)+'FILME'+item,))
                threads.append(Filmes_MVT)

        [i.start() for i in threads]

        [i.join() for i in threads]

        if name != '':
                _sites_ = ['filmesMVT.txt']
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
        ##                        _nfil = re.compile('(.+?)NOME[|]').findall(_filmes_[x])
        ##                        if _nfil: nfilme = _nfil[0]
        ##                        else: nfilme = '---'
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
                                else: fanart = '---'
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
                                        
                                if 'movietuga'         in imdbcode: num_mode = 103
                                
                                if nome != '---':
                                        num_filmes = num_filmes + 1
                                        addDir_trailer(nome,imdbcode,num_mode,thumb,sinopse,fanart,ano_filme,genero,O_Nome,urltrailer)

                        Filmes_Fi.close()

                num_total = num_filmes + 0.0
                for a in range(num_filmes):
                        percent = int( ( a / num_total ) * 100)
                        message = str(a+1) + " de " + str(num_filmes)
                        progress.update( percent, 'A Finalizar ...', message, "" )
                        xbmc.sleep(20)

                proxima = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
                try:
                        proxima_p = proxima[0].replace('%3A',':')
                        addDir("[B]Página Seguinte >>[/B]",proxima_p.replace('&amp;','&'),102,artfolder + 'PAGS1.png','','')
                except: pass
	progress.close()

def Fontes_Filmes_MVT(item):        
##        progress = xbmcgui.DialogProgress()
##        i = 1
##        percent = 0
##        message = ''
##        progress.create('Progresso', 'A Pesquisar:')
##        progress.update( percent, "", message, "" )
##        try:
##		html_source = abrir_url(url)
##	except: html_source = ''
##	items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
##	if items != []:
##		print len(items)
##		num = len(items) + 0.0
##		for item in items:
##                        percent = int( ( i / num ) * 100)
##                        message = str(i) + " de " + str(len(items))
##                        progress.update( percent, "", message, "" )
##                        print str(i) + " de " + str(len(items))
##                        if progress.iscanceled():
##                                break

        folder = perfil
        Filmes_File = open(folder + 'filmesMVT.txt', 'w')
        
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
                        
                        url = re.compile('<div class="btns"><a href="(.+?)" target="Player">').findall(item)
                        #url = re.compile("<a href='(.+?)'><div align=").findall(item)
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
                        if ano: ano_filme = ano[0].replace(' ','').replace('20013','2013')
                        else: ano_filme = ''
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
                                        
                        
##                        nnnn = re.compile('.+?[(](.+?)[)]').findall(nome)
##                        if not nnnn: nnnn = re.compile('.+?[[](.+?)[]]').findall(nome)
##                        if not nnnn: nnnn = re.compile('(.+?)[:]').findall(nome)
##                        if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
##                        if nnnn : nome_pesquisa = nnnn[0]
##                        else: nome_pesquisa = nome
                        nome_pesquisa = nome
                        #if imdbcode == '': imdbcode = themoviedb_api_search_imdbcode().fanart_and_id(nome_pesquisa,ano_filme)
                        
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
                                nome_final = '[B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]'
                                filmes.append(FILMEN+'NOME|'+str(nome_final)+'|IMDBCODE|'+url[0].replace(' ','%20')+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb.replace(' ','%20'))+'|ANO|'+str(ano_filme)+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|ONOME|'+str(nome)+'|SINOPSE|'+str(sinopse)+'|END|\n')
                                #addDir_trailer('[B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',url[0].replace(' ','%20')+'IMDB'+imdbcode+'IMDB',103,thumb.replace(' ','%20'),sinopse,fanart,ano_filme,genero,nome,url[0])
                        except: pass
                except: pass
        else: pass
        filmes.sort()
        for x in range(len(filmes)):
                Filmes_File.write(str(filmes[x]))
	Filmes_File.close()



#----------------------------------------------------------------------------------------------------------------------------------------------#

def MVT_encontrar_videos_filmes(name,url):
        site = '[B][COLOR green]MOVIE[/COLOR][COLOR yellow]-[/COLOR][COLOR red]TUGA[/COLOR][/B]'
        message = 'Por favor aguarde.'
        percent = 0
        progress.create('Progresso', 'A Procurar...')
        progress.update(percent, 'A Procurar em '+site, message, "")
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]
        if 'MVT' not in name: name = '[COLOR orange]MVT | [/COLOR]' + name
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
##        nn = nomeescolha.replace('[B][COLOR green]','--').replace('[/COLOR][/B]','--').replace('[COLOR orange]','').replace('MVT | ','')
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
        
        fontes_video = re.findall("<body>(.+?)</body>", fonte_video, re.DOTALL)
        if imdbcode == '':
                imdb = re.compile('imdb.com/title/(.+?)/').findall(fonte_video)
                if imdb: imdbcode = imdb[0]
                else: imdbcode = ''
        numero_de_fontes = len(fontes_video)
        for fonte_e_url in fontes_video:
                match = re.compile('<option value=(.+?)>(.+?)<').findall(fonte_e_url)
                if '<option' in fonte_e_url:
                        for url_video_url_id,cd in match:
                                if url_video_url_id == '""':
                                        if 'CD' in cd:
                                                conta_id_video = 0
                                                cd = cd.replace('Filme Aqui','')
                                                addDir1('[COLOR blue]' + cd + '[/COLOR]','','',iconimage,False,fanart)
                                        if 'Cole' in cd:
                                                conta_id_video = 0
                                                colecao = 'sim'
                                else:
                                        url_video_url_id = url_video_url_id.replace('"','')
                                if colecao == 'sim' and (('Breve' or 'breve') not in cd):
                                        if 'Cole' not in cd:
                                                conta_id_video = 0
                                                addDir1('[COLOR blue]' + cd + ':[/COLOR]','','',iconimage,False,fanart)
                                if 'http:' not in url_video_url_id:
                                        url_video = 'http:' + url_video_url_id
                                else:
                                        url_video = url_video_url_id
                                try:
                                        fonte = abrir_url(url_video)
                                except: fonte = ''
                                fontes = re.findall("<body>(.+?)</body>", fonte, re.DOTALL)
                                for fonte_id in fontes:
                                        if 'videomega' in fonte_id:
                                                try:
                                                        match = re.compile("<script type=\'text/javascript\'>ref=\'(.+?)\'").findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        id_video = match[0]
                                                        url = 'http://videomega.tv/iframe.php?ref=' + id_video + '///' + name
                                                        fonte_serv = '(Videomega)'
                                                        Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_serv+'[/COLOR][/B]',iconimage,'',fanart)
                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,100,iconimage,'',fanart)
                                                except:pass
                                        if 'vidto' in fonte_id:
                                                try:
                                                        match = re.compile('<iframe .+? src=".+?//vidto.me/embed-(.+?)" .+?</iframe>').findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        if match: match = re.compile('(.+?)-').findall(match[0])
                                                        id_video = match[0]
                                                        url = 'http://vidto.me/' + id_video + '.html' + '///' + name
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,100,iconimage,'',fanart)
                                                except:pass
                else:
 	                if fonte_video:
 		                for fonte_id in fontes_video:
                                        if 'videomega' in fonte_id:
                                                try:
                                                        match = re.compile("<script type=\'text/javascript\'>ref=\'(.+?)\'").findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        id_video = match[0]
                                                        url = 'http://videomega.tv/iframe.php?ref=' + id_video + '///' + name
                                                        fonte_serv = '(Videomega)'
                                                        Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_serv+'[/COLOR][/B]',iconimage,'',fanart)
                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,100,iconimage,'',fanart)
                                                except:pass
                                        if 'vidto' in fonte_id:
                                                try:
                                                        match = re.compile('<iframe .+? src=".+?//vidto.me/embed-(.+?)" .+?</iframe>').findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        if match: match = re.compile('(.+?)-').findall(match[0])
                                                        id_video = match[0]
                                                        url = 'http://vidto.me/' + id_video + '.html' + '///' + name
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,100,iconimage,'',fanart)
                                                except:pass
##        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(nomeescolha)
##        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
##        nn = nomeescolha.replace('[B][COLOR green]','--').replace('[/COLOR][/B]','--').replace('[COLOR orange]','').replace('MVT | ','')
##        n = re.compile('--(.+?)--').findall(nn)
##        url = 'IMDB'+imdbcode+'IMDB'
##        FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n[0]),'MVT',url)
        #addLink(imdbcode,'','')
        url = 'IMDB'+imdbcode+'IMDB'
        FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n1),'MVT',url)


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
        if imdbcode == '':
                imdb = re.compile('imdb.com/title/(.+?)/').findall(fonte_video)
                if imdb: imdbcode = imdb[0]
                else: imdbcode = ''
        numero_de_fontes = len(fontes_video)
        for fonte_e_url in fontes_video:
                match = re.compile('<option value=(.+?)>(.+?)<').findall(fonte_e_url)
                if '<option' in fonte_e_url:
                        for url_video_url_id,cd in match:
                                if url_video_url_id == '""':
                                        if 'CD' in cd:
                                                conta_id_video = 0
                                                cd = cd.replace('Filme Aqui','')
                                                addDir1('[COLOR blue]' + cd + '[/COLOR]','','',iconimage,False,fanart)
                                        if 'Cole' in cd:
                                                conta_id_video = 0
                                                colecao = 'sim'
                                else:
                                        url_video_url_id = url_video_url_id.replace('"','')
                                if colecao == 'sim' and (('Breve' or 'breve') not in cd):
                                        if 'Cole' not in cd:
                                                conta_id_video = 0
                                                addDir1('[COLOR blue]' + cd + ':[/COLOR]','','',iconimage,False,fanart)
                                if 'http:' not in url_video_url_id:
                                        url_video = 'http:' + url_video_url_id
                                else:
                                        url_video = url_video_url_id
                                try:
                                        fonte = abrir_url(url_video)
                                except: fonte = ''
                                fontes = re.findall("<body>(.+?)</body>", fonte, re.DOTALL)
                                for fonte_id in fontes:
                                        if 'videomega' in fonte_id:
                                                try:
                                                        match = re.compile("<script type=\'text/javascript\'>ref=\'(.+?)\'").findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        id_video = match[0]
                                                        url = 'http://videomega.tv/iframe.php?ref=' + id_video + '///' + name
                                                        fonte_serv = '(Videomega)'
                                                        Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_serv+'[/COLOR][/B]',iconimage,'',fanart)
                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,100,iconimage,'',fanart)
                                                except:pass
                                        if 'vidto' in fonte_id:
                                                try:
                                                        match = re.compile('<iframe .+? src=".+?//vidto.me/embed-(.+?)" .+?</iframe>').findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        if match: match = re.compile('(.+?)-').findall(match[0])
                                                        id_video = match[0]
                                                        url = 'http://vidto.me/' + id_video + '.html' + '///' + name
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,100,iconimage,'',fanart)
                                                except:pass
                else:
 	                if fonte_video:
 		                for fonte_id in fontes_video:
                                        if 'videomega' in fonte_id:
                                                try:
                                                        match = re.compile("<script type=\'text/javascript\'>ref=\'(.+?)\'").findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        id_video = match[0]
                                                        url = 'http://videomega.tv/iframe.php?ref=' + id_video + '///' + name
                                                        fonte_serv = '(Videomega)'
                                                        Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_serv+'[/COLOR][/B]',iconimage,'',fanart)
                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,100,iconimage,'',fanart)
                                                except:pass
                                        if 'vidto' in fonte_id:
                                                try:
                                                        match = re.compile('<iframe .+? src=".+?//vidto.me/embed-(.+?)" .+?</iframe>').findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        if match: match = re.compile('(.+?)-').findall(match[0])
                                                        id_video = match[0]
                                                        url = 'http://vidto.me/' + id_video + '.html' + '///' + name
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,100,iconimage,'',fanart)
                                                except:pass



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


