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


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,time,os,threading,FilmesAnima,Mashup,Play
from Funcoes import thetvdb_api, themoviedb_api, themoviedb_api_tv, theomapi_api, themoviedb_api_IMDB, themoviedb_api_IMDB_episodios, themoviedb_api_TMDB, thetvdb_api_IMDB
from Funcoes import thetvdb_api_tvdbid, thetvdb_api_episodes, themoviedb_api_search_imdbcode, themoviedb_api_pagina, themoviedb_api_IMDB1, theomapi_api_nome
from Funcoes import addDir, addDir1, addDir2, addLink, addLink1, addDir_teste, addDir_trailer, addDir_episode, addDir_trailer1, addDir_episode1, addDir_episode1_false
from Funcoes import get_params,abrir_url

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
perfil = xbmc.translatePath(selfAddon.getAddonInfo('profile'))

#fanart = artfolder + 'FAN3.jpg'

arr_series = ['' for i in range(500)]
arrai_series = ['' for i in range(500)]
_series_ = []
_seriesALL_ = []
Anos = ['' for i in range(100)]
filmes = []
filmesTFV = []
fanfan = []
fanfan1 = []
episoding = []
episthreads = []
episthr = []


progress = xbmcgui.DialogProgress()


#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#



def TFV_MenuPrincipal(artfolder):
        fanart = artfolder + 'FAN3.jpg'
        addDir('- Procurar','http://www.tuga-filmes.us/search?q=',1,artfolder + 'P1.png','nao','')
        addDir('[COLOR yellow]- Últimos[/COLOR] (Filmes/Séries)','http://www.tuga-filmes.us',32,artfolder + 'UFS.png','nao','')
        addDir('[COLOR yellow]- Top Semanal[/COLOR]','http://www.tuga-filmes.us',32,artfolder + 'TPSE.png','nao','')#48
	addDir1('[COLOR blue]Filmes:[/COLOR]','url',1004,artfolder + 'TFV1.png',False,fanart)
	addDir('[COLOR yellow]- Todos[/COLOR]','http://www.tuga-filmes.us/search/label/Filmes',32,artfolder + 'FT.png','nao','')
	addDir('[COLOR yellow]- Animação[/COLOR]','http://www.tuga-filmes.us/search/label/Anima%C3%A7%C3%A3o',32,artfolder + 'FA.png','nao',fanart)
        addDir('[COLOR yellow]- Por Ano[/COLOR]','url',39,artfolder + 'ANO.png','nao','')
	addDir('[COLOR yellow]- Categorias[/COLOR]','url',38,artfolder + 'CT.png','nao','')
		
	#if selfAddon.getSetting('hide-porno') == "false":
			#addDir('[B][COLOR red]M+18[/B][/COLOR]','url',49,artfolder + 'TFV1.png','nao','')
	addDir1('[COLOR blue]Séries:[/COLOR]','url',1004,artfolder + 'TFV1.png',False,fanart)
	addDir('[COLOR yellow]- A a Z[/COLOR]','urlTFV',41,artfolder + 'SAZ1.png','nao','')
        addDir('[COLOR yellow]- Últimos Episódios[/COLOR]','http://www.tuga-filmes.us/search/label/Séries',58,artfolder + 'UE.png','nao','')#32#44

def TFV_Menu_Filmes_Top_5(endereco_top_5):
##        i = 1
##        percent = 0
##        message = ''
##        progress.create('Progresso', 'A Pesquisar:')
##        progress.update( percent, "", message, "" )
##        url_top_5 = 'http://www.tuga-filmes.us'
##        top_5_source = abrir_url(url_top_5)
##        filmes_top_5 = re.compile("<img alt=\'.+?\' height=\'50\' src=\'.+?\' width=\'50\'/>\n<a href=\'(.+?)\'").findall(top_5_source)
##	for endereco_top_5 in filmes_top_5:
        if endereco_top_5 != '':
                try:
                        html_source = abrir_url(endereco_top_5)
                except: html_source = ''
                items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
                if items != []:
                        #try:
                        for item in items:

                                imdbcode = ''
                                fanart = ''
                                sinopse = ''
                                thumb = ''
                                genero = ''

                                imdb = re.compile('"http://www.imdb.com/title/(.+?)/"').findall(item)
                                if imdb: imdbcode = imdb[0]
                                else: imdbcode = ''
                                
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
                                urletitulo = re.compile("<h1>(.+?)\n</h1>").findall(item)
                                if ttp and not tto: nome = ttp[0]
                                elif not ttp and tto: nome = tto[0]
                                elif ttp and tto:
                                        ttocomp = '['+ tto[0]
                                        ttpcomp = '['+ ttp[0]
                                        if ttpcomp.replace('[ ','') != ttocomp.replace('[ ',''): nome = ttp[0] +' ['+ tto[0] +']'
                                        else: nome = ttp[0]
                                elif not ttp and not tto: nome = urletitulo[0]
                                nome = nome.replace('[ ',"[")

                                resumo = re.compile("<b>Resumo</b>:(.+?)<br />").findall(item)
                                if resumo: sinopse = resumo[0]
                                else: sinopse = ''

                                genero = re.compile("nero</b>:(.+?)<br />").findall(item)
                                if genero: genero = genero[0]
                                else: genero = ''

                                qualidade = re.compile("<b>Qualidade</b>: (.+?)<br />").findall(item)
                                ano = re.compile("<b>Ano</b>: (.+?)<br />").findall(item)
                                thumbnail = re.compile('src="(.+?)"').findall(item)
                                
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
                                print urletitulo,thumbnail
                                if ano: ano_filme = ano[0]
                                else : ano_filme = ''

                                if 'Temporada' in urletitulo[0] or 'Season' in urletitulo[0] or 'Mini-Série' in urletitulo[0] or 'Mini-Serie' in urletitulo[0]:
                                        nome = urletitulo[0]
                                        nnnn = re.compile('(.+?)[(].+?[)]').findall(nome)
                                        if not nnnn: nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                                        if nnnn : nome_pesquisa = nnnn[0]
                                        else: nome_pesquisa = nome
                                        thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme.replace('(','').replace(')',''))
                                        ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                        if ftart:
                                                fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
        ##                                        for nt in range(20):
        ##                                                try:
        ##                                                        thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-'+str(nt)+'.jpg'
        ##                                                        f = urllib2.urlopen(urllib2.Request(thumb))
        ##                                                        deadLinkFound = False
        ##                                                except: deadLinkFound = True
        ##                                                if deadLinkFound == False: break                                        
                                        snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                        if snpse and sinopse == '': sinopse = snpse[0]
                                else:
                                        nnnn = re.compile('.+?[(](.+?)[)]').findall(nome)
                                        if not nnnn: nnnn = re.compile('.+?[[](.+?)[]]').findall(nome)
                                        if nnnn : nome_pesquisa = nnnn[0]
                                        else: nome_pesquisa = nome
                                        fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano_filme)
                                        if thumb == '': thumb = poster


                                
                                try:
                                        if "Temporada" in urletitulo[0] or 'Season' in urletitulo[0]:
                                                num_mode = 42
                                        else:
                                                num_mode = 33
                                        addDir_trailer('[B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + ano[0] + ')[/COLOR][COLOR red] (' + qualidade[0] + ')[/COLOR]',endereco_top_5+'IMDB'+imdbcode+'IMDB',num_mode,thumbnail[0].replace('s72-c','s320'),sinopse,fanart,ano_filme,genero,nome_pesquisa,endereco_top_5)
                                except: pass
                        #except: pass

def TFV_Menu_Filmes_Por_Ano(artfolder):
        i = 0
        url_ano = 'http://www.tuga-filmes.us'
        ano_source = abrir_url(url_ano)
        filmes_por_ano = re.compile("<a dir=\'ltr\' href=\'(.+?)\'>Filmes (.+?)</a>").findall(ano_source)
	for endereco_ano,nome_ano in filmes_por_ano:
		#addDir('[COLOR yellow]' + nome_ano + '[/COLOR] ',endereco_ano,32,artfolder + 'TFV1.png','nao','')
		Anos[i] = nome_ano+'|'+endereco_ano
                i = i + 1
        Anos.sort()
        Anos.reverse()
        for x in range(len(Anos)):
                if Anos[x] != '':
                        A = re.compile('(.+?)[|](.*)').findall(Anos[x])
                        if A:
                                addDir('[COLOR yellow]' + A[0][0].replace('  ','').replace(' ','') + '[/COLOR]',A[0][1],32,artfolder + 'TFV1.png','nao','')

def TFV_Menu_Filmes_Por_Categorias(artfolder):
        url_categorias = 'http://www.tuga-filmes.us'
        html_categorias_source = abrir_url(url_categorias)
	html_items_categorias = re.findall("<div class=\'widget Label\' id=\'Label1\'>(.*?)<div class=\'clear\'>", html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<a dir=\'ltr\' href=\'(.+?)\'>(.+?)</a>").findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        addDir('[COLOR yellow]' + nome_categoria + '[/COLOR] ',endereco_categoria,32,artfolder + 'TFV1.png','nao','')

def TFV_Menu_Series_A_a_Z(artfolder,url):

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
                
                try: Filmes_Fi = open(folder + 'SeriesTFV1.txt', 'r')
                except:
                        Filmes_File = open(folder + 'SeriesTFV1.txt', 'a')
                        Filmes_File.close()
                        Filmes_Fi = open(folder + 'SeriesTFV1.txt', 'r')
                read_Filmes_File = ''
                for line in Filmes_Fi:
                        read_Filmes_File = read_Filmes_File + line
                        if line!='':filmes.append(line)

                if read_Filmes_File != '':
                        try: xbmcgui.Dialog().notification('A Procurar Séries (A/Z).', 'Por favor aguarde...', artfolder + 'TFV1.png', 2000, sound=False)
                        except: xbmc.executebuiltin("Notification(%s,%s, 2000, %s)" % ('A Procurar Séries (A/Z).', 'Por favor aguarde...', artfolder + 'TFV1.png'))
                else:
                        try: xbmcgui.Dialog().notification('A Procurar Séries (A/Z).', 'Por favor aguarde...', artfolder + 'TFV1.png', 12000, sound=False)
                        except: xbmc.executebuiltin("Notification(%s,%s, 12000, %s)" % ('A Procurar Séries (A/Z).', 'Por favor aguarde...', artfolder + 'TFV1.png'))

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
                                if endereco_series not in read_Filmes_File:
                                        nome_series = nome_series.replace('&amp;','&')
                                        nome_series = nome_series.replace('&#39;',"'")
                                        nome_series = nome_series.replace('&#8217;',"'")
                                        nome_series = nome_series.replace('&#8230;',"...")
                                        nome_series = nome_series.replace('&#8211;',"-")
                                        nome_series = nome_series.lower()
                                        nome_series = nome_series.title()
                                        nome_series = nome_series.replace('Agents Of S.H.I.E.L.D',"Agents Of S.H.I.E.L.D.")
                                        i = i + 1
                                        a = str(i)
                                        if i < 10: a = '00'+a
                                        if i < 100 and i > 9: a = '0'+a
                                        TFV = threading.Thread(name='TFV'+str(i), target=Series_TFV, args=('FILME'+str(a)+'FILME',endereco_series,nome_series,))
                                        threads.append(TFV)
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

        for i in range(int(2*(len(threads)/3)),int(3*(len(threads)/3))):
                threads[i].start()
        for i in range(int(2*(len(threads)/3)),int(3*(len(threads)/3))):
                threads[i].join()

        for i in range(int(3*(len(threads)/3)),len(threads)):
                threads[i].start()
        for i in range(int(3*(len(threads)/3)),len(threads)):
                threads[i].join()

##        [i.start() for i in threads]
##
##        [i.join() for i in threads]

        filmes.sort()
        
        folder = perfil 
        Filmes_File = open(folder + 'SeriesTFV1.txt', 'w')
        for x in range(len(filmes)):
                if filmes[x] != '':
                        Filmes_File.write(str(filmes[x]))
        Filmes_File.close()

        try:
                _sites_ = ['SeriesTFV1.txt']
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
                                urltrailer = re.compile('IMDB.+?MDB[|](.*)').findall(imdbcode)
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
                                xbmc.sleep(12)
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


#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#


def TFV_encontrar_fontes_filmes(url):


        #try: xbmcgui.Dialog().notification('Movie Trailers', 'Finding Nemo download finished.', self.addonArt('icon.png'), 5000, sound=False)
        #except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % ('sim', '77', self.addonArt('icon.png')))
        #msg = ' (%s)' % timeout_msg if timeout_msg else ''
        
        
##        percent = 0
##        message = 'Por favor aguarde.'
##        progress.create('Progresso', 'A Procurar')
        
        if name == '[COLOR yellow]- Top Semanal[/COLOR]' or name == '[COLOR yellow]- Últimos[/COLOR] (Filmes/Séries)' or name == '[B]Página Seguinte>>>[/B]':
                #progress.update( percent, 'A Procurar ...', message, "" )
##                builtin = 'XBMC.Notification(%s,%s, 3000, %s)'
##                log = xbmc.executebuiltin(builtin % ('A Procurar.', 'Por favor aguarde...',artfolder + 'TFV1.png'))
                try: xbmcgui.Dialog().notification('A Procurar.', 'Por favor aguarde...', artfolder + 'TFV1.png', 3000, sound=False)
                except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % ('A Procurar.', 'Por favor aguarde...', artfolder + 'TFV1.png'))
                
        if name == '[COLOR yellow]- Últimos Episódios[/COLOR]' or name == '[B]Página Seguinte>>[/B]':
                #progress.update( percent, 'A Procurar Últimos Episódios ...', message, "" )
##                builtin = 'XBMC.Notification(%s,%s, 3000, %s)'
##                log = xbmc.executebuiltin(builtin % ('A Procurar Últimos Episódios.', 'Por favor aguarde...',artfolder + 'TFV1.png'))
                try: xbmcgui.Dialog().notification('A Procurar Últimos Episódios.', 'Por favor aguarde...', artfolder + 'TFV1.png', 3000, sound=False)
                except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % ('A Procurar Últimos Episódios.', 'Por favor aguarde...', artfolder + 'TFV1.png'))
                
        if name != '[COLOR yellow]- Top Semanal[/COLOR]' and name != '[COLOR yellow]- Últimos Episódios[/COLOR]' and name != '[B]Página Seguinte>>[/B]' and name != '[COLOR yellow]- Últimos[/COLOR] (Filmes/Séries)' and name != '[B]Página Seguinte>>>[/B]':
                #progress.update( percent, 'A Procurar Filmes ...', message, "" )
##                builtin = 'XBMC.Notification(%s,%s, 3000, %s)'
##                log = xbmc.executebuiltin(builtin % ('A Procurar Filmes.', 'Por favor aguarde...',artfolder + 'TFV1.png'))
                try: xbmcgui.Dialog().notification('A Procurar Filmes.', 'Por favor aguarde...', artfolder + 'TFV1.png', 3000, sound=False)
                except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % ('A Procurar Filmes.', 'Por favor aguarde...', artfolder + 'TFV1.png'))
        
        try:
		html_source = abrir_url(url)
	except: html_source = ''
	if name != '[COLOR yellow]- Top Semanal[/COLOR]':
                items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
        if name == '[COLOR yellow]- Top Semanal[/COLOR]':
                items = re.findall("<img alt=\'.+?\' height=\'50\' src=\'.+?\' width=\'50\'/>\n<a href=\'(.+?)\'", html_source, re.DOTALL)

        threads = []
        i = 0
        for item in items:
                if name != '[COLOR yellow]- Top Semanal[/COLOR]':
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        Filmes_TFV = threading.Thread(name='Filmes_TFV'+str(i), target=Fontes_Filmes_TFV , args=('FILME'+str(a)+'FILME'+item,))
                if name == '[COLOR yellow]- Top Semanal[/COLOR]':
                        Filmes_TFV = threading.Thread(name='Filmes_TFV'+str(i), target=TFV_Menu_Filmes_Top_5 , args=(item,))
                threads.append(Filmes_TFV)

        [i.start() for i in threads]

        [i.join() for i in threads]

        if name != '[COLOR yellow]- Top Semanal[/COLOR]':
                _sites_ = ['filmesTFV.txt']
                folder = perfil
                num_filmes = 0
                
                for site in _sites_:
                        _filmes_ = []
                        Filmes_Fi = open(folder + site, 'r')
                        read_Filmes_File = ''
                        for line in Filmes_Fi:
                                read_Filmes_File = read_Filmes_File + line
                                if line!='':_filmes_.append(line)
                        totalitems = len(_filmes_)
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
       
                                if "Temporada" in nome or 'Season' in nome or 'Mini-Série' in nome:
                                        num_mode = 42
                                else:
                                        num_mode = 33
                                
                                if nome != '---':
                                        num_filmes = num_filmes + 1
                                        #addDir_trailer(nome,imdbcode,num_mode,thumb,sinopse,fanart,ano_filme,genero,O_Nome,urltrailer)
                                        addDir_trailer1(nome,imdbcode,num_mode,thumb,sinopse,fanart,ano_filme,genero,O_Nome,urltrailer,'movie',totalitems)

                        Filmes_Fi.close()

##                num_total = num_filmes + 0.0
##                progress.create('Progresso', '')
##                for a in range(num_filmes):
##                        percent = int( ( a / num_total ) * 100)
##                        message = str(a+1) + " de " + str(num_filmes)
##                        progress.update( percent, 'A Finalizar ...', message, "" )
##                        xbmc.sleep(20)

                proxima = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
                try:
                        if name == '[COLOR yellow]- Últimos Episódios[/COLOR]' or name == '[B]Página Seguinte>>[/B]':
                                addDir("[B]Página Seguinte>>[/B]",proxima[0].replace('&amp;','&'),32,artfolder + 'PAGS1.png','','')
                        elif name == '[COLOR yellow]- Últimos[/COLOR] (Filmes/Séries)' or name == '[B]Página Seguinte>>>[/B]':
                                addDir("[B]Página Seguinte>>>[/B]",proxima[0].replace('&amp;','&'),32,artfolder + 'PAGS1.png','','')
                        else:
                                addDir("[B]Página Seguinte >>[/B]",proxima[0].replace('&amp;','&'),32,artfolder + 'PAGS1.png','','')
                except:pass
	progress.close()
	#log.close()
	


def Fontes_Filmes_TFV(item):        

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

                        imdb = re.compile('"http://www.imdb.com/title/(.+?)/"').findall(item)
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
                                #addDir1(nome_original,'','',artfolder + 'PAGS1.png',False,'')
                        else:
                                titulooriginal = re.compile("<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>(.+?)<br />").findall(item)
                                if titulooriginal:
                                        nome_original = titulooriginal[0]
                                else: nome_original = ''
                                #addDir1(nome_original,'','',artfolder + 'PAGS1.png',False,'')
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

                        if 'Temporada' in urletitulo[0][1] or 'Season' in urletitulo[0][1] or 'Mini-Série' in urletitulo[0][1]:
                                nome = urletitulo[0][1]
                                nnnn = re.compile('(.+?)[(].+?[)]').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                                if nnnn : nome_pesquisa = nnnn[0]
                                else: nome_pesquisa = nome
                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano[0].replace(' ',''))
                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                if ftart:
                                        fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                        if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
        ##                                        for nt in range(20):
        ##                                                try:
        ##                                                        thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-'+str(nt)+'.jpg'
        ##                                                        f = urllib2.urlopen(urllib2.Request(thumb))
        ##                                                        deadLinkFound = False
        ##                                                except: deadLinkFound = True
        ##                                                if deadLinkFound == False: break                                        
                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                if snpse and sinopse == '': sinopse = snpse[0]
                        else:
                                #nome = urletitulo[0][1]
                                nnnn = re.compile('.+?[(](.+?)[)]').findall(nome)
                                if not nnnn: nnnn = re.compile('.+?[[](.+?)[]]').findall(nome)
                                if nnnn : nome_pesquisa = nnnn[0]
                                else: nome_pesquisa = nome
                                fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano[0].replace(' ',''))
                                if thumb == '': thumb = poster

                        sinopse = sinopse.replace('&#8216;',"'")
                        sinopse = sinopse.replace('&#8217;',"'")
                        sinopse = sinopse.replace('&#8211;',"-")
                        sinopse = sinopse.replace('&#8220;',"'")
                        sinopse = sinopse.replace('&#8221;',"'")
                        sinopse = sinopse.replace('&#39;',"'")
                        sinopse = sinopse.replace('&amp;','&')

                        if qualidade:
                                qualidade = qualidade[0]
                        else:
                                qualidade = ''
                        if genre == '': genre = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        try:
                                if "Temporada" in urletitulo[0][1] or 'Season' in urletitulo[0][1] or 'Mini-Série' in urletitulo[0][1]:
                                        num_mode = 42
                                else:
                                        num_mode = 33
                                #addLink(nome,'','','')
                                nome_final = '[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao
                                filmes.append(FILMEN+'NOME|'+str(nome_final)+'|IMDBCODE|'+urletitulo[0][0]+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb.replace('s72-c','s320'))+'|ANO|'+str(ano[0].replace(' ',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(genre)+'|ONOME|'+str(nome_pesquisa)+'|SINOPSE|'+str(sinopse)+'|END|\n')
                                #addDir_trailer('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',num_mode,thumb.replace('s72-c','s320'),sinopse,fanart,ano[0],genre,nome_pesquisa,urletitulo[0][0])
                        except: pass
                except: pass	
        else: pass
        filmes.sort()
        for x in range(len(filmes)):
                Filmes_File.write(str(filmes[x]))
	Filmes_File.close()
	
        
        
#----------------------------------------------------------------------------------------------------------------------------------------------#	


def TFV_encontrar_videos_filmes(name,url,mvoutv):
        if mvoutv == 'MoviesTFV':
                try: xbmcgui.Dialog().notification('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png', 3000, sound=False)
                except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % ('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png'))
        else:
                try: xbmcgui.Dialog().notification('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png', 10000, sound=False)
                except: xbmc.executebuiltin("Notification(%s,%s, 10000, %s)" % ('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png'))
        site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv'
##        message = 'Por favor aguarde.'
##        percent = 0
##        progress.create('Progresso', 'A Procurar...')
##        progress.update(percent, 'A Procurar em '+site, message, "")
        nomeescolha = name
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]
        if 'TFV' not in name: name = '[COLOR orange]TFV | [/COLOR]' + name
        #########################################
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

        if n1 != '' and n2 != '':
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
                addDir('[COLOR yellow]PROCURAR POR: [/COLOR]'+n2,'IMDB'+imdbcode+'IMDB',7,iconimage,'',fanart)
        else:
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
      
##        nn = nomeescolha.replace('[B][COLOR green]','--').replace('[/COLOR][/B]','--').replace('[COLOR orange]','').replace('[/COLOR]','').replace('[','---').replace(']','---').replace('TPT | ','')
##        if '---' in nn:
##                n = re.compile('---(.+?)---').findall(nn)
##                n1 = re.compile('--(.+?)--').findall(nn)
##                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1[0],'url',1004,iconimage,False,fanart)
##                addDir('[COLOR yellow]PROCURAR POR: [/COLOR]'+n[0],'IMDB'+imdbcode+'IMDB',7,iconimage,'',fanart)
##        else:
##                n1 = re.compile('--(.+?)--').findall(nn)
##                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1[0],'url',1004,iconimage,False,fanart)
        ##########################################
        conta_id_video = 0
	addDir1(name,'url',1004,iconimage,False,fanart)

        #addDir1(url,'url',1004,artfolder,False,'')     
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
        items = re.findall('<div class=\'video-item\'>(.*?)<div class=\'clear\'>', link2, re.DOTALL)
        #addLink(str(len(items)),'','','')
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

                #addLink(str(len(matchvid)),'','','')
                if matchvid:
                        for servidor,matchsvids in matchvid:
                                if 'Legendado' in matchsvids and num_leg == 1:
                                        num_leg = 0
                                        if num_ptpt == 0: conta_id_video = 0
                                        addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,'')
                                if 'Portug' in matchsvids or 'PT-PT' in matchsvids:
                                        if num_ptpt == 1:
                                                num_ptpt = 0
                                                if num_leg == 0: conta_id_video = 0
                                                addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,'')
                                if '</iframe>' in matchsvids:
                                        videomeg = re.compile('<iframe frameborder="0" height="400" scrolling="no" src="(.+?)"').findall(matchsvids)
                                        if videomeg:
                                                conta_id_video = conta_id_video + 1
                                                fonte_id = '(Videomega)'
                                                Play.PLAY_movie_url(videomeg[0],'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',iconimage,'',fanart)
                                                #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',videomeg[0],30,iconimage,'',fanart)
                                match = re.compile('href="(.+?)"').findall(matchsvids)
                                url = match[0] 
                                if url != '':
                                        try:
                                                for url in match:
                                                        identifica_video = re.compile('=(.*)').findall(url)
                                                        id_video = identifica_video[0]
                                                        conta_id_video = conta_id_video + 1
                                                        #addLink(servidor,'','')
                                                        if "ep" in servidor: url = 'videomega'
                                                        if "vw" in servidor: url = 'videowood'
                                                        if "dv" in servidor: url = 'dropvideo'
                                                        if "vt" in servidor: url = 'vidto.me'
                                                        if "nv" in servidor: url = 'nowvideo'
                                                        #addLink(url+id_video,'','','')
                                                        TFV_resolve_not_videomega_filmes(name,url,id_video,conta_id_video)
                                        except:pass
                else:
                        videomeg = re.compile('<iframe frameborder="0" height="400" scrolling="no" src="(.+?)"').findall(link2)
                        if videomeg:
                                conta_id_video = conta_id_video + 1
                                fonte_id = '(Videomega)'
                                Play.PLAY_movie_url(videomeg[0],'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',iconimage,'',fanart)
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
                        for servidor,parte in matchvideo:
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
                                                        #addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except: pass
                                        if "vidto.me" in url:
                                                try:
                                                        url = 'http://vidto.me/' + id_video + '.html' + '///' + name
                                                        print url
                                                        fonte_id = '(Vidto.me)'
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except: pass
                                        if "dropvideo" in url:
                                                try:
                                                        url = 'http://dropvideo.com/embed/' + id_video #+ '///' + name
                                                        print url
                                                        fonte_id = '(Dropvideo)'
                                                        #addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if "streamin.to" in url:
                                                try:
                                                        url = 'http://streamin.to/embed-' + id_video + '.html' #+ '///' + name
                                                        print url
                                                        fonte_id = '(Streamin)'
                                                        #addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,30,iconimage,'',fanart)
                                                except:pass                        
                                        if "putlocker" in url:
                                                try:
                                                        url = 'http://www.putlocker.com/embed/' + id_video# + '///' + name
                                                        print url
                                                        fonte_id = '(Putlocker)'
                                                        #addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Putlocker)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if "nowvideo" in url:
                                                try:
                                                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video #+ '///' + name
                                                        print url
                                                        fonte_id = '(Nowvideo)'
                                                        #addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if "videowood" in url:
                                                try:
                                                        if '/video/' in url: url = url.replace('/video/','/embed/')
                                                        url = 'http://www.videowood.tv/embed/' + id_video #+ '///' + name
                                                        print url
                                                        fonte_id = '(Videowood)'
                                                        #addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](VideoWood)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if "firedrive" in url:
                                                try:
                                                        url = 'http://www.firedrive.com/file/' + id_video #+ '///' + name
                                                        fonte_id = '(Firedrive)'
                                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url:# and 'iiiiiiiiii' in url:
                                                Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',iconimage,'',fanart)
##        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(nomeescolha)
##        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
##        nn = nomeescolha.replace('[B][COLOR green]','--').replace('[/COLOR][/B]','--').replace('[COLOR orange]','').replace('[/COLOR]','').replace('[','---').replace(']','---').replace('TPT | ','')
##        #addDir1('','url',1004,artfolder,False,'')

        url = 'IMDB'+imdbcode+'IMDB'
        if mvoutv != 'MoviesTFV': FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n1),'TFV',url)
        
##        if '---' in nn:
##                n = re.compile('---(.+?)---').findall(nn)
##                n1 = re.compile('--(.+?)--').findall(nn)
##                url = 'IMDB'+imdbcode+'IMDB'
##                FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n1[0]),'TFV',url)
##        else:
##                n1 = re.compile('--(.+?)--').findall(nn)
##                url = 'IMDB'+imdbcode+'IMDB'
##                FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n1[0]),'TFV',url)


#----------------------------------------------------------------------------------------------------------------------------------------------#

def TFV_resolve_not_videomega_filmes11(name,url,id_video,conta_id_video):
##        req = urllib2.Request(url)
##        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
##        response = urllib2.urlopen(req)
##        link4=response.read()
##        response.close()
##        match = re.compile('<iframe src="(.+?)".+?></iframe></center>').findall(link4)
##        url=match[0]
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
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'',fanart)
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
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Putlocker)[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "nowvideo" in url:
                try:
                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video #+ '///' + name
                        print url
                        fonte_id = '(Nowvideo)'
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
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url:# and 'iiiiiiiiii' in url:
                Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',iconimage,'',fanart)
    	return

def TFV_resolve_not_videomega_filmes(name,url,id_video,conta_id_video):
##        req = urllib2.Request(url)
##        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
##        response = urllib2.urlopen(req)
##        link4=response.read()
##        response.close()
##        match = re.compile('<iframe src="(.+?)".+?></iframe></center>').findall(link4)
##        url=match[0]
        if "videomega" in url:
                try:
                        url = 'http://videomega.tv/iframe.php?ref=' + id_video + '///' + name
                        print url
                        fonte_id = '(Videomega)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                except: pass
        if "vidto.me" in url:
                try:
                        url = 'http://vidto.me/' + id_video + '.html' + '///' + name
                        print url
                        fonte_id = '(Vidto.me)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'',fanart)
                except: pass
        if "dropvideo" in url:
                try:
                        url = 'http://dropvideo.com/embed/' + id_video + '///' + name
                        print url
                        fonte_id = '(Dropvideo)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "streamin.to" in url:
                try:
                        url = 'http://streamin.to/embed-' + id_video + '.html' + '///' + name
                        print url
                        fonte_id = '(Streamin)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,30,iconimage,'',fanart)
                except:pass                        
        if "putlocker" in url:
                try:
                        url = 'http://www.putlocker.com/embed/' + id_video + '///' + name
                        print url
                        fonte_id = '(Putlocker)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Putlocker)[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "nowvideo" in url:
                try:
                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video + '///' + name
                        print url
                        fonte_id = '(Nowvideo)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        url = 'http://www.videowood.tv/embed/' + id_video + '///' + name
                        print url
                        fonte_id = '(Videowood)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoWood)[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "firedrive" in url:
                try:
                        url = 'http://www.firedrive.com/file/' + id_video + '///' + name
                        fonte_id = '(Firedrive)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
##        if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url:# and 'iiiiiiiiii' in url:
##                Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',iconimage,'',fanart)
    	return


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
                                        addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,'')
                                if 'Portug' in matchsvids or 'PT-PT' in matchsvids:
                                        if num_ptpt == 1:
                                                num_ptpt = 0
                                                if num_leg == 0: conta_id_video = 0
                                                addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,'')
                                if '</iframe>' in matchsvids:
                                        videomeg = re.compile('<iframe frameborder="0" height="400" scrolling="no" src="(.+?)"').findall(matchsvids)
                                        if videomeg:
                                                conta_id_video = conta_id_video + 1
                                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',videomeg[0],30,iconimage,'',fanart)
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
                                                        TFV_resolve_not_videomega_filmes(name,url,id_video,conta_id_video)    
                                                        #TFV_resolve_not_videomega_filmes(name,url,id_video,conta_id_video)
                                        except:pass
                else:
                        videomeg = re.compile('<iframe frameborder="0" height="400" scrolling="no" src="(.+?)"').findall(link2)
                        if videomeg:
                                conta_id_video = conta_id_video + 1
                                fonte_id = '(Videomega)'
                                #Play.PLAY_movie_url(videomeg[0],'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',iconimage,'',fanart)
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',videomeg[0],30,iconimage,'',fanart)

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
                                                        url = 'http://videomega.tv/iframe.php?ref=' + id_video + '///' + name
                                                        print url
                                                        fonte_id = '(Videomega)'
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except: pass
                                        if "vidto.me" in url:
                                                try:
                                                        url = 'http://vidto.me/' + id_video + '.html' + '///' + name
                                                        print url
                                                        fonte_id = '(Vidto.me)'
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except: pass
                                        if "dropvideo" in url:
                                                try:
                                                        url = 'http://dropvideo.com/embed/' + id_video + '///' + name
                                                        print url
                                                        fonte_id = '(Dropvideo)'
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if "streamin.to" in url:
                                                try:
                                                        url = 'http://streamin.to/embed-' + id_video + '.html' + '///' + name
                                                        print url
                                                        fonte_id = '(Streamin)'
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,30,iconimage,'',fanart)
                                                except:pass                        
                                        if "putlocker" in url:
                                                try:
                                                        url = 'http://www.putlocker.com/embed/' + id_video + '///' + name
                                                        print url
                                                        fonte_id = '(Putlocker)'
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Putlocker)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if "nowvideo" in url:
                                                try:
                                                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video + '///' + name
                                                        print url
                                                        fonte_id = '(Nowvideo)'
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if "videowood" in url:
                                                try:
                                                        if '/video/' in url: url = url.replace('/video/','/embed/')
                                                        url = 'http://www.videowood.tv/embed/' + id_video + '///' + name
                                                        print url
                                                        fonte_id = '(Videowood)'
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](VideoWood)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if "firedrive" in url:
                                                try:
                                                        url = 'http://www.firedrive.com/file/' + id_video + '///' + name
                                                        fonte_id = '(Firedrive)'
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
##                                        if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url:# and 'iiiiiiiiii' in url:
##                                                Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',iconimage,'',fanart)



#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Séries  -----------------------------------------------------------------#


                                
def TFV_encontrar_fontes_series_recentes(url):
        i = 1
        percent = 0
        message = ''
        progress.create( 'Progresso', 'A Procurar Últimos Episódios...' )
        progress.update( percent, "", message, "" )
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		num = len(items) + 0.0
		for item in items:
                        thumb = ''
                        fanart = ''
                        genero = ''
                        sinopse = ''
                        
                        imdb = re.compile('"http://www.imdb.com/title/(.+?)/"').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
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
                                        
                        nnnn = re.compile('(.+?)[(].+?[)]').findall(nome)
                        if not nnnn: nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                        if nnnn : nome_pesquisa = nnnn[0]
                        else: nome_pesquisa = nome
                        thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano)
                        ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                        if ftart:
                                fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'                                       
                        snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                        if snpse: sinopse = snpse[0]
          
			try:
				addDir_trailer('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano + '[/COLOR][COLOR red] ' + qualidade + '[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',42,thumb.replace('s72-c','s320'),sinopse,fanart,ano,genero,nome_pesquisa,urletitulo[0][0])
			except: pass
			percent = int( ( i / num ) * 100)
                        message = nome
                        progress.update( percent, "", message, "" )
                        if progress.iscanceled():
                                break
			i = i + 1
	else:
		items = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(html_source)
		for endereco,nome in items:
			addDir(nome,endereco,42,'','','')
	proxima = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
        try:
                addDir("Página Seguinte >>",proxima[0],44,artfolder + 'PAGS1.png','','')
        except: pass

#----------------------------------------------------------------------------------------------------------------------------------------------#                     
#----------------------------------------------------------------------------------------------------------------------------------------------#
	
def TFV_resolve_not_videomega_series(name,url,id_video,nome_cada_episodio,src_href):
##        req = urllib2.Request(url)
##        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
##        response = urllib2.urlopen(req)
##        link4=response.read()
##        response.close()
##        if src_href == 'href':
##                match = re.compile('<iframe src="(.+?)".+?></iframe>').findall(link4)
##        if src_href == 'src':
##                match = re.compile('<iframe .+? src="(.+?)" .+?></iframe>').findall(link4)
##        url=match[0]        
        if "videomega" in url:
		try:
                        url = 'http://videomega.tv/iframe.php?ref=' + id_video #+ '///' + name
                        fonte_id ='(Videomega)'+url
                        print url
			#addDir('[COLOR blue]' + nome_cada_episodio + '[/COLOR][B] - Fonte : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
        if "vidto.me" in url:
		try:
                        url = 'http://vidto.me/' + id_video + '.html'# + '///' + name
                        fonte_id ='(Vidto.me)'+url
                        print url
			#addDir('[COLOR blue]' + nome_cada_episodio + '[/COLOR][B] - Fonte : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
        if "dropvideo" in url:
		try:
                        url = 'http://dropvideo.com/embed/' + id_video# + '///' + name
                        fonte_id ='(Dropvideo)'+url
			print url
			#addDir('[COLOR blue]' + nome_cada_episodio + '[/COLOR][B] - Fonte : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "streamin.to" in url:
                try:
                        url = 'http://streamin.to/embed-' + id_video# + '.html' + '///' + name
                        fonte_id ='(streamin)'+url
			print url
			#addDir('[COLOR blue]' + nome_cada_episodio + '[/COLOR][B] - Fonte : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,30,iconimage,'',fanart)
                except:pass                        
        if "putlocker" in url:
                try:
                        url = 'http://www.putlocker.com/embed/' + id_video# + '///' + name
                        fonte_id ='(Putlocker)'+url
                        print url
                        #addDir('[COLOR blue]' + nome_cada_episodio + '[/COLOR][B] - Fonte : [COLOR yellow](Putlocker)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "nowvideo" in url:
                try:
                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video# + '///' + name
                        fonte_id ='(Nowvideo)'+url
                        print url
                        #addDir('[COLOR blue]' + nome_cada_episodio + '[/COLOR][B] - Fonte : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        url = 'http://www.videowood.tv/embed/' + id_video #+ '///' + name
                        fonte_id ='(VideoWood)'+url
                        print url
                        #addDir('[COLOR blue]' + nome_cada_episodio + '[/COLOR][B] - Fonte : [COLOR yellow](VideoWood)[/COLOR][/B]',url,70,iconimage,'',fanart)
    		except:pass
    	return fonte_id

#----------------------------------------------------------------------------------------------------------------------------------------------#                     
#----------------------------------------------------------------------------------------------------------------------------------------------#
def TFV_encontrar_videos_series(name,url):
        try: xbmcgui.Dialog().notification('A Procurar Episódios.', 'Por favor aguarde...', artfolder + 'TFV1.png', 3000, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % ('A Procurar Episódios.', 'Por favor aguarde...', artfolder + 'TFV1.png'))
        
        ####################
        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(name)
        if nnn: nnnn = re.compile('(.+?)[(].+?[)]').findall(nnn[0])
        if nnnn : n_pesquisa = nnnn[0]
        else:
                nnn = re.compile('IMDB.+?IMDB(.*)').findall(url)
                if nnn: n_pesquisa = nnn[0]
                else: n_pesquisa = ''

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

        tvdbid = thetvdb_api_tvdbid()._id(n_pesquisa,anne)
        #addLink(season+'-'+imdbcode+'-'+tvdbid+'-'+temporadat+'-'+anne+'-'+n_pesquisa+'-'+name,'','')
        #return
        #######################

        namett = re.compile('IMDB.+?IMDB(.*)').findall(url)
        if namett: namet = namett[0]
        else:
                namett = re.compile('IMDBIMDB(.*)').findall(url)
                if namett: namet = namett[0]
                #else: namet = ''
        
        urlseries = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlseries: url = url.replace('IMDBIMDB','')
        else: url = urlseries[0]

        urltrailer = url

        episodioanterior = ''
        episodio = ''
        episodiot = ''
        nomecadaantes = ''
        f_id = ''
        f_idantes = ''
        i = 0
        epis = []

        conta_id_video = 0

	try:
		link_series=abrir_url(url)
	except: link_series = ''
        #addDir1(name,'url',1004,iconimage,False,fanart)
	if link_series:
                try:
                        items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", link_series, re.DOTALL)
                        items_series = re.findall("<div class='id(.+?)</a>", items[0], re.DOTALL)
                        if not items_series: items_series = re.findall("<div class='id(.+?)</p>", items[0], re.DOTALL)
                        if not items_series: items_series = re.findall('<div class="id(.+?)</a>', items[0], re.DOTALL)
                        if not items_series: items_series = re.findall('<div class="id(.+?)</p>', items[0], re.DOTALL)

                        nomecadaantes = ''
                        n_items = 0
                        #addLink(str(len(items_series)),'','','')
                        for item_vid_series in items_series:
                                not_vi = re.compile('>(.+?)</div></h3>').findall(item_vid_series)
                                if not not_vi: not_vi = re.compile('>(.+?)</div></h3>').findall(item_vid_series)
                                if 'div class=' in not_vi[0]: not_vi = re.compile('>(.*)').findall(not_vi[0])
                                nomecadaepisodio = not_vi[0]
                                nomecadaepisodio = nomecadaepisodio.replace('&#8217;',"'")
                                nomecadaepisodio = nomecadaepisodio.replace('&#8211;',"-")
                                nomecadaepisodio = nomecadaepisodio.replace('&#39;',"'")
                                nomecadaepisodio = nomecadaepisodio.replace('&amp;','&')
##                                episodio = re.compile('(\d+) [-] ').findall(nomecadaepisodio)
##                                if episodio:
##                                        episodiot = episodio[0]
##                                        episodio = episodio[0]
##                                a_q = re.compile('\d+')
##                                qq_aa = a_q.findall(episodio)
##                                for q_a_q_a in qq_aa:
##                                        if len(q_a_q_a) == 1:
##                                                episodiot = '0'+episodio
                                #addLink(nomecadaepisodio+'--'+nomecadaantes,'','','')
##                                if nomecadaepisodio != nomecadaantes:
##                                        f_id = ''
                                        
                                try:
                                        #addLink(episodio+'-f-'+f_id,'','','')
                                        #addLink(episodio+'-'+episodioanterior+'-'+item_vid_series+'-'+str(i)+'-'+str(n_items)+'-'+temporadat,'','')                                 
         
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
                                                        
                                                        try:
                                                                fonte_id = TFV_resolve_not_videomega_series(name,url,id_video,nome_cada_episodio,src_href)
                                                        except: pass
                                                except:pass                        
                                except:pass
                                #addLink('-f-'+f_id,'','','')
                                if nomecadaepisodio != nomecadaantes and nomecadaantes != '':
                                        #addLink(episodio+'-f-'+f_id,'','','')
                                        
                                        n_items = n_items + 1
                                        #f_id = ''

                                        nomeepisodio = re.compile(' [-] (.*)').findall(nomecadaepisodio)
                                        if nomeepisodio: nomeepisodio = nomeepisodio[0]
                                        else: nomeepisodio = nomecadaepisodio

                                        #addLink(episodio+'-f-'+f_id,'','','')
                                        
                                        epis.append('episodio'+episodio+'episodiot'+episodiot+'nomeepisodio'+nomecadaantes+'f_id'+f_id+'|END')
                                        f_id = ''
                                        
                                nomecadaantes = nomecadaepisodio

                                episodio = re.compile('(\d+) [-] ').findall(nomecadaepisodio)
                                if episodio:
                                        episodiot = episodio[0]
                                        episodio = episodio[0]
                                a_q = re.compile('\d+')
                                qq_aa = a_q.findall(episodio)
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) == 1:
                                                episodiot = '0'+episodio                                        

                                if f_id == '': f_id = fonte_id
                                else: f_id = f_id + '|' + fonte_id
                                
                        #addLink('-f-'+f_id,'','','')
                        if nomecadaepisodio == nomecadaantes and nomecadaantes != '':
                                #addLink(episodio+'-f-'+f_id,'','','')
                                        
                                n_items = n_items + 1
                                #f_id = ''

                                nomeepisodio = re.compile(' [-] (.*)').findall(nomecadaepisodio)
                                if nomeepisodio: nomeepisodio = nomeepisodio[0]
                                else: nomeepisodio = nomecadaepisodio

                                #addLink(episodio+'-f-'+f_id,'','','')
                                        
                                epis.append('episodio'+episodio+'episodiot'+episodiot+'nomeepisodio'+nomecadaantes+'f_id'+f_id+'|END')
                                f_id = ''
                                        
                        nomecadaantes = nomecadaepisodio
                except:pass
                
                if 'calendar_title' in items[0]: n_items = n_items - 1
                threads = []
                for x in range(len(epis)):
                        #addLink(epis[x],'','','')
                        episo = re.compile('episodio(.+?)episodiot(.+?)nomeepisodio(.+?)f_id(.+?)[|]END').findall(epis[x])
                        for episodio,episodiot,nomeepisodio,f_id in episo:
                                TFVepi = threading.Thread(name='TFVepi'+str(x), target=vamosla , args=(episodio,episodiot,nomeepisodio,f_id,temporada,temporadat,urltrailer,fanart,namet,n_items,tvdbid,'---',imdbcode,year,))
                                threads.append(TFVepi)
                                
                [i.start() for i in threads]
                [i.join() for i in threads]

        episoding.sort()
        episoding.reverse()
        for x in range(len(episoding)):
                #episco = re.compile('TEMPT(.+?)EPT(.+?)FID(.+?)EPINOME(.+?)THUMB(.+?)SIN(.+?)AIR(.+?)NAMET(.+?)TEMPO(.+?)EPI(.+?)END').findall(episoding[x])
                temporadat = re.compile('TEMPADAT(.+?)EPISODT').findall(episoding[x])
                temporadat = temporadat[0]
                #addLink(temporadat,'','','')
                episodiot = re.compile('EPISODT(.+?)FIDID').findall(episoding[x])
                episodiot = episodiot[0]
                #addLink(episodiot,'','','')
                f_id = re.compile('FIDID(.+?)EPINOME').findall(episoding[x])
                f_id = f_id[0]
                #addLink(f_id,'','','')
                epi_nome = re.compile('EPINOME(.+?)THUMB').findall(episoding[x])
                epi_nome = epi_nome[0]
                #addLink(epi_nome,'','','')
                th = re.compile('THUMB(.+?)SINOPSE').findall(episoding[x])
                th = th[0]
                if th == '---': th = ''
                #addLink(th,'','','')
                sin = re.compile('SINOPSE(.+?)AIRDAY').findall(episoding[x])
                sin = sin[0]
                if sin == '---': sin = ''
                #addLink(sin,'','','')
                air = re.compile('AIRDAY(.+?)NAMET').findall(episoding[x])
                air = air[0]
                if air == '---': air = ''
                #addLink(air,'','','')
                namett = re.compile('NAMET(.+?)TEMPORDA').findall(episoding[x])
                try: namet = namett[0]
                except: namet = ''
                #addLink(namet,'','','')
                temporada = re.compile('TEMPORDA(.+?)EPISTIO').findall(episoding[x])
                temporada = temporada[0]
                #addLink(temporada,'','','')
                episodio = re.compile('EPISTIO(.+?)FANART').findall(episoding[x])
                episodio = episodio[0]
                #addLink(episodio,'','','')
                mvoutv = temporada+'|'+episodio+'|'+namet+'|'+tvdbid+'|'+imdbcode+'|'+year
                addDir_episode1_false('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,th,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,mvoutv,n_items)
                xbmc.sleep(12)
                
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmc.executebuiltin("Container.SetViewMode(504)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
                                
def vamosla(episodio,episodiot,nomeepisodio,f_id,temporada,temporadat,urltrailer,fanart,namet,n_items,tvdbid,nome_antes,imdbcode,anne):
        
        try:
                epi_nome,air,sin,th = thetvdb_api_episodes()._id(str(tvdbid),str(temporada),str(episodio))
                if sin == '': sin = '---'
                if th == '': th = '---'
                if air == '': air = '---'
                if epi_nome == '': epi_nome = nomeepisodio
                episoding.append('TEMPADAT'+temporadat+'EPISODT'+episodiot+'FIDID'+f_id+'EPINOME'+epi_nome+'THUMB'+th+'SINOPSE'+sin+'AIRDAY'+air+'NAMET'+namet+'TEMPORDA'+temporada+'EPISTIO'+episodio+'FANART'+fanart+'URLTRAILER'+urltrailer+'NMANTES'+nome_antes+'END'+tvdbid+'|'+imdbcode+'|'+anne)
                #addDir_episode1('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,th,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,'tvepisode',n_items)
        except:
                episoding.append('TEMPADAT'+temporadat+'EPISODT'+episodiot+'FIDID'+f_id+'EPINOME'+nomeepisodio+'THUMB'+fanart+'SINOPSE---AIRDAY---'+'NAMET'+namet+'TEMPORDA'+temporada+'EPISTIO'+episodio+'FANART'+fanart+'URLTRAILER'+urltrailer+'NMANTES'+nome_antes+'END'+tvdbid+'|'+imdbcode+'|'+anne)
                #addDir_episode1('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+nomeepisodio+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+nomeepisodio+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer,'tvepisode',n_items)
        

                                
                
def TFV_encontrar_videos_series1(name,url):

        ####################
        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(name)
        if nnn: nnnn = re.compile('(.+?)[(].+?[)]').findall(nnn[0])
        if nnnn : n_pesquisa = nnnn[0]
        else:
                nnn = re.compile('IMDB.+?IMDB(.*)').findall(url)
                if nnn: n_pesquisa = nnn[0]
                else: n_pesquisa = ''

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

        tvdbid = thetvdb_api_tvdbid()._id(n_pesquisa,anne)
        #addLink(season+'-'+imdbcode+'-'+tvdbid+'-'+temporadat+'-'+anne+'-'+n_pesquisa+'-'+name,'','')
        #return
        #######################
        
        urlseries = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlseries: url = url.replace('IMDBIMDB','')
        else: url = urlseries[0]

        urltrailer = url

        episodioanterior = ''
        episodio = ''
        episodiot = ''

        f_id = ''
        i = 0
##        percent = 0
##        message = ''
##        progress.create('Progresso', 'A Procurar Episódios...')
##        progress.update( percent, "", message, "" )
        conta_id_video = 0

	try:
		link_series=abrir_url(url)
	except: link_series = ''
        #addDir1(name,'url',1004,iconimage,False,fanart)
	if link_series:
                try:
                        items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", link_series, re.DOTALL)
                        items_series = re.findall("<div class='id(.+?)</a>", items[0], re.DOTALL)
                        if not items_series: items_series = re.findall("<div class='id(.+?)</p>", items[0], re.DOTALL)
##                        n_items = len(items_series)
##                        if 'calendar_title' in items[0]: n_items = n_items - 1
##                        divide = n_items + 0.0

                        nomecadaantes = ''
                        n_items = 0
                        for item_vid_series in items_series:
                                not_vi = re.compile('>(.+?)</div></h3>').findall(item_vid_series)
                                if not not_vi: not_vi = re.compile('>(.+?)</div></h3>').findall(item_vid_series)
                                if 'div class=' in not_vi[0]: not_vi = re.compile('>(.*)').findall(not_vi[0])
                                nomecada = not_vi[0]
                                if nomecada != nomecadaantes:
                                        nomecadaantes = nomecada
                                        n_items = n_items + 1
                                        
                        if 'calendar_title' in items[0]: n_items = n_items - 1
                        divide = n_items + 0.0
                        for item_vid_series in items_series:
                                
                                #addLink(item_vid_series,'','')
                                not_videomeganome = re.compile('>(.+?)</div></h3>').findall(item_vid_series)
                                if not not_videomeganome: not_videomeganome = re.compile('>(.+?)</div></h3>').findall(item_vid_series)
                                if 'div class=' in not_videomeganome[0]: not_videomeganome = re.compile('>(.*)').findall(not_videomeganome[0])
                                nomecadaepisodio = not_videomeganome[0]
                                episodioanterior = re.compile('(\d+) [-] ').findall(nomecadaepisodio)
                                if episodioanterior: episodioanterior = episodioanterior[0]

                                try:
##                                        if 'div class=' in item_vid_series:
##                                                ivs = re.compile('class=.+?>(.*)').findall(item_vid_series)
##                                                if ivs: item_vid_series = ivs[0]
                                        
                                        #addLink(episodio+'-'+episodioanterior+'-'+item_vid_series+'-'+str(i)+'-'+str(n_items)+'-'+temporadat,'','')                                        
         
                                        if 'videomega' in item_vid_series:
                                                try:
##                                                        videomega_video_nome = re.compile('>(.+?)</div></h3>').findall(item_vid_series)
##                                                        if not videomega_video_nome: videomega_video_nome = re.compile('>(.+?)</div></h3><p>').findall(item_vid_series)
##                                                        if not videomega_video_nome: videomega_video_nome = re.compile('>(.+?)</div></h3><a').findall(item_vid_series)
##                                                        if 'div class=' in videomega_video_nome[0]: videomega_video_nome = re.compile('>(.*)').findall(videomega_video_nome[0])
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
##                                                        not_videomega_video_nome = re.compile('>(.+?)</div></h3>').findall(item_vid_series)
##                                                        if not not_videomega_video_nome: not_videomega_video_nome = re.compile('>(.+?)</div></h3><p>').findall(item_vid_series)
##                                                        if not not_videomega_video_nome: not_videomega_video_nome = re.compile('>(.+?)</div></h3><a').findall(item_vid_series)
##                                                        if 'div class=' in not_videomega_video_nome[0]: not_videomega_video_nome = re.compile('>(.*)').findall(not_videomega_video_nome[0])
##                                                        nome_cada_episodio = not_videomega_video_nome[0]
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

##                                                        not_videomega_video_nome = re.compile('>(.+?)</div></h3>').findall(item_vid_series)
##                                                        if not not_videomega_video_nome: not_videomega_video_nome = re.compile('>(.+?)</div></h3>').findall(item_vid_series)
##                                                        if 'div class=' in not_videomega_video_nome[0]: not_videomega_video_nome = re.compile('>(.*)').findall(not_videomega_video_nome[0])
##                                                        if not_videomega_video_nome: nome_cada_episodio = not_videomega_video_nome[0]
##                                                        else: nome_cada_episodio = ''
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
                                
                                
                                try:
                                        epi_nome,air,sin,th = thetvdb_api_episodes()._id(str(tvdbid),str(temporada),str(episodio))
                                                        
                                        if episodioanterior != episodio and episodio != '':
                                                try:
                                                        #addDir_episode('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,th,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer)
                                                        addDir_episode1('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,th,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,'tvepisode',n_items)
                                                        #nomeepisodioanterior = nomeepisodio
                                                        f_id = ''
                                                except: pass
                                        #else: nomeepisodioanterior = nomeepisodio
                                except:
                                        #addLink(nomecadaepisodio,'','','')
                                        nomeepisodio = re.compile(' [-] (.*)').findall(nomecadaepisodio)
                                        if nomeepisodio: nomeepisodio = nomeepisodio[0]
                                        else: nomeepisodio = nomecadaepisodio
                                        
                                        #addLink(episodio+'-'+episodioanterior,'','')
                                        if episodioanterior != episodio and episodio != '':
                                                #addDir_episode('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+nomeepisodioanterior+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+nomeepisodioanterior+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer)
                                                addDir_episode1('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+nomeepisodioanterior+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+nomeepisodioanterior+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer,'tvepisode',n_items)
                                                nomeepisodioanterior = nomeepisodio
                                                f_id = ''
                                        else: nomeepisodioanterior = nomeepisodio

                                episodio = re.compile('(\d+) [-] ').findall(nomecadaepisodio)
                                if episodio:
                                        episodiot = episodio[0]
                                        episodio = episodio[0]
                                a_q = re.compile('\d+')
                                qq_aa = a_q.findall(episodio)
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) == 1:
                                                episodiot = '0'+episodio

                                if f_id == '': f_id = fonte_id
                                else: f_id = f_id + '|' + fonte_id

##                                percent = int( ( i / divide ) * 100)
##                                message = '[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+nomeepisodio+'[/COLOR]'
##                                progress.update( percent, "", message, "" )        
##                                if progress.iscanceled():
##                                        break

                                
                                if i != int(divide): i = i + 1
                                #addLink(str(i)+' == '+str(int(divide)),'','','')
                                
                        try:
                                #if i == int(divide):
                                if episodio != '':
                                        try:
                                                epi_nome,air,sin,th = thetvdb_api_episodes()._id(str(tvdbid),str(temporada),str(episodio))

                                                nomeepisodio = re.compile(' [-] (.*)').findall(nomecadaepisodio)
                                                if nomeepisodio: nomeepisodio = nomeepisodio[0]
                                                else: nomeepisodio = nomecadaepisodio
                                                
                                                if (episodioanterior == episodio and episodio != '') or 'calendar_title' in item_vid_series:
                                                        try:                                                                
                                                                #addDir_episode('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,th,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer)
                                                                addDir_episode1('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,th,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,'tvepisode',n_items)
                                                                f_id = ''
                                                        except: pass
                                        except:                                     
                                                nomeepisodio = re.compile(' [-] (.*)').findall(nomecadaepisodio)
                                                if nomeepisodio: nomeepisodio = nomeepisodio[0]
                                                else: nomeepisodio = nomecadaepisodio
                                                
                                                #addLink(episodio+'-'+episodioanterior,'','','')
                                                if episodioanterior == episodio and episodio != '':
                                                        #addDir_episode('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+nomeepisodio+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+nomeepisodio+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer)
                                                        addDir_episode1('[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+nomeepisodio+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+nomeepisodio+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer,'tvepisode',n_items)
                                                        f_id = ''
                                                        
                                
                        except:pass          
                except:pass
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmc.executebuiltin("Container.SetViewMode(504)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------------------------------------------------------------------------#                     
#----------------------------------------------------------------------------------------------------------------------------------------------#

def TFV_Ultimos(fanart,name,url,item,tvdbid,n_items):
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
        
	nome_antes = '[B][COLOR green]' + namet + '[/COLOR][/B] | '

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
                                        
                        nomeepisodio = re.compile(' [-] (.*)').findall(nomecadaepisodio)
                        if nomeepisodio: nomeepisodio = nomeepisodio[0]
                        else: nomeepisodio = nomecadaepisodio

                        episthr.append('episodio'+episodio+'episodiot'+episodiot+'nomeepisodio'+nomeepisodio+'f_id'+f_id+'|END')
##
##                        try:
##                                epi_nome,air,sin,th = thetvdb_api_episodes()._id(str(tvdbid),str(temporada),str(episodio))
##
##                                try:
##                                        #addDir_episode(nome_antes+' [COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,th,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer)
##                                        addDir_episode1(nome_antes+' [COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,th,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namet,urltrailer,'tvepisode',n_items)
##                                        f_id = ''
##                                except: pass
##                        except:                                     
##                                nomeepisodio = re.compile(' [-] (.*)').findall(nomecadaepisodio)
##                                if nomeepisodio: nomeepisodio = nomeepisodio[0]
##                                else: nomeepisodio = nomecadaepisodio
##
##                                addDir_episode(nome_antes+' [COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+nomeepisodio+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+nomeepisodio+'[/COLOR]',7000,fanart,'',fanart,episodiot,'',temporada+'x'+episodiot+' '+namet,urltrailer)
##                                f_id = ''
                                
                except:pass
                #episthreads = []
##                for x in range(len(episthr)):
##                        addLink(episthr[x],'','','')
##                        episo = re.compile('episodio(.+?)episodiot(.+?)nomeepisodio(.+?)f_id(.+?)[|]END').findall(episthr[x])
##                        for episodio,episodiot,nomeepisodio,f_id in episo:
##                                TFVepi = threading.Thread(name='TFVepi'+str(x), target=vamosla , args=(episodio,episodiot,nomeepisodio,f_id,temporada,temporadat,urltrailer,fanart,namet,n_items,tvdbid,))
##                                episthreads.append(TFVepi)


                TFVepi = threading.Thread(name='TFVepi'+FILMEN, target=vamosla , args=(episodio,episodiot,nomeepisodio,f_id,temporada,temporadat,urltrailer,fanart,namet,n_items,tvdbid,nome_antes,imdbcode,anne,))
                episthreads.append(TFVepi)
                TFVepi.start()
                TFVepi.join()
                                
##                [i.start() for i in threads]
##                [i.join() for i in threads]

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#


def ultimos_ep_TFV(item,passaurlimdbcode,nome_pesquisa,nome_fi,imdbcode,tv_id,n_items):
        
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
                        TFV3 = threading.Thread(name='TFV3'+FILMEN, target=TFV_Ultimos , args=(fanart,nome_fi,passaurlimdbcode,item,tv_id,n_items,))
                        fanfan1.append(TFV3)
                        TFV3.start()
                        TFV3.join()
		except: pass
        else: pass

def busca_tvid(item,passaurlimdbcode,nome_pesquisa,nome_fi,imdbcode,n_items):
        FILMEN = re.compile('FILME(.+?)FILME').findall(item)
        FILMEN = FILMEN[0]
        item = 'FILME'+FILMEN+'FILME'+item
        tv_id, sinopse = thetvdb_api_IMDB()._id(nome_pesquisa,imdbcode)
        #addLink(tv_id+passaurlimdbcode+nome_pesquisa+nome_fi+imdbcode,'','','')
        TFV2 = threading.Thread(name='TFV2'+FILMEN, target=ultimos_ep_TFV , args=(item,passaurlimdbcode,nome_pesquisa,nome_fi,imdbcode,tv_id,n_items,))
        fanfan.append(TFV2)
        TFV2.start()
        TFV2.join()
##        url = 'http://thetvdb.com/api/23B3F3D91B980C9F/series/'+str(tv_id)+'/pt.xml'
##        try: html_source = abrir_url(url)
##        except: html_source = ''
##        fan = re.compile('<fanart>(.+?)</fanart>').findall(html_source)#(fanart,name,url,item,tvdbid)
##        try: fanart = 'http://thetvdb.com/banners/'+fan[0]
##        except: fanart = ''
##        #addLink(tv_id+passaurlimdbcode+nome_pesquisa+nome_fi+imdbcode,'','',fanart)
##        TFV3 = threading.Thread(name='TFV3'+FILMEN, target=TFV_Ultimos , args=(fanart,nome_fi,passaurlimdbcode,item,tv_id,n_items,))
##        fanfan1.append(TFV3)
##        TFV3.start()
##        TFV3.join()

        
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def ultimos_episodios_TFV_ultimos(url):

        try: xbmcgui.Dialog().notification('A Procurar Últimos Episódios.', 'Por favor aguarde...', artfolder + 'TFV1.png', 6000, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, 6000, %s)" % ('A Procurar Últimos Episódios.', 'Por favor aguarde...', artfolder + 'TFV1.png'))
##                builtin = 'XBMC.Notification(%s,%s, 6000, %s)'
##                log = xbmc.executebuiltin(builtin % ('A Procurar Últimos Episódios.', 'Por favor aguarde...',artfolder + 'TFV1.png'))

        #----------------------------------------------------------------------------------------------------
        threads = []

        i = 0
        try:
                try:
                        html_source = abrir_url(url)
                except: html_source = ''
                itemsTFV = re.findall("<div class='video-item'>(.*?)<div class='clear'>", html_source, re.DOTALL)
                n_items = len(itemsTFV)
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
                        TFV1 = threading.Thread(name='TFV1'+str(i), target=busca_tvid , args=(item,passaurlimdbcode,nome_pesquisa,nome_fi,imdbcode,n_items,))
                        #TFV2 = threading.Thread(name='TFV2'+str(i), target=ultimos_ep_TFV , args=('FILME'+str(a)+'FILME'+item,nome_pesquisa,imdbcode,tv_id,))
                        threads.append(TFV1)

        except: pass

        [i.start() for i in threads]

        [i.join() for i in threads]

##        [i.start() for i in fanfan]
##
##        [i.join() for i in fanfan]

##        [i.start() for i in fanfan1]
##
##        [i.join() for i in fanfan1]

##        [i.start() for i in episthreads]
##
##        [i.join() for i in episthreads]

        num_filmes = 0

        for x in range(len(threads)):
                num_filmes = num_filmes + 1

        num_total = num_filmes# + 0.0
        episoding.sort()
        episoding.reverse()
        #addLink(str(len(threads))+str(num_total),'','','')
        #return
        for x in range(len(episoding)):
                #episco = re.compile('TEMPT(.+?)EPT(.+?)FID(.+?)EPINOME(.+?)THUMB(.+?)SIN(.+?)AIR(.+?)NAMET(.+?)TEMPO(.+?)EPI(.+?)END').findall(episoding[x])
                temporadat = re.compile('TEMPADAT(.+?)EPISODT').findall(episoding[x])
                try: temporadat = temporadat[0]
                except: temporadat = ''
                #addLink(temporadat,'','','')
                episodiot = re.compile('EPISODT(.+?)FIDID').findall(episoding[x])
                try: episodiot = episodiot[0]
                except: episodiot = ''
                #addLink(episodiot,'','','')
                f_id = re.compile('FIDID(.+?)EPINOME').findall(episoding[x])
                try: f_id = f_id[0]
                except: f_id = ''
                #addLink(f_id,'','','')
                epi_nome = re.compile('EPINOME(.+?)THUMB').findall(episoding[x])    
                try: epi_nome = epi_nome[0]
                except: epi_nome = ''
                #addLink(epi_nome,'','','')
                th = re.compile('THUMB(.+?)SINOPSE').findall(episoding[x])
                try: th = th[0]
                except: th = ''
                if th == '---': th = ''
                #addLink(th,'','','')
                sin = re.compile('SINOPSE(.+?)AIRDAY').findall(episoding[x])                
                try: sin = sin[0]
                except: sin = ''
                if sin == '---': sin = ''
                #addLink(sin,'','','')
                air = re.compile('AIRDAY(.+?)NAMET').findall(episoding[x])
                try: air = air[0]
                except: air = ''
                if air == '---': air = ''
                #addLink(air,'','','')
                namett = re.compile('NAMET(.+?)TEMPORDA').findall(episoding[x])
                try: namett = namett[0]
                except: namett = ''
                #addLink(namet,'','','')
                temporada = re.compile('TEMPORDA(.+?)EPISTIO').findall(episoding[x])
                try: temporada = temporada[0]
                except: temporada = ''
                #addLink(temporada,'','','')
                episodio = re.compile('EPISTIO(.+?)FANART').findall(episoding[x])
                try: episodio = episodio[0]
                except: episodio = ''
                #addLink(episodio,'','','')
                fanart = re.compile('FANART(.+?)URLTRAILER').findall(episoding[x])
                try: fanart = fanart[0]
                except: fanart = ''
                #addLink(fanart,'','','')
                urltrailer = re.compile('URLTRAILER(.+?)NMANTES').findall(episoding[x])
                try: urltrailer = urltrailer[0]
                except: urltrailer = ''
                #addLink(urltrailer,'','','')
                nome_antes = re.compile('NMANTES(.+?)END').findall(episoding[x])
                nome_antes = nome_antes[0]
                if nome_antes == '---': nome_antes = ''
                #addLink(urltrailer,'','','')
                tvdbidimdbyear = re.compile('END(.+?)[|](.+?)[|](.*)').findall(episoding[x])
                tvdbid = tvdbidimdbyear[0][0]
                imdbcode = tvdbidimdbyear[0][1]
                anne = tvdbidimdbyear[0][2]
                #sin = ''
                try:
                        mvoutv = temporada+'|'+episodio+'|'+namett+'|'+tvdbid+'|'+imdbcode+'|'+anne
                        addDir_episode1_false(nome_antes+'[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',f_id+'//[COLOR grey]S'+temporadat+' x E'+episodiot+' - [/COLOR][COLOR blue]'+epi_nome+'[/COLOR]',7000,th,str(sin),fanart,episodiot,air,temporada+'x'+episodiot+' '+namett,urltrailer,mvoutv,num_total)
                except: pass
                xbmc.sleep(20)
##        percent = 0
##        progress.create('[B][COLOR green]TUGA-[/COLOR][COLOR yellow]F[/COLOR][COLOR red]ILMES.tv[/COLOR][/B]', '')
##        for a in range(num_filmes):
##                percent = int( ( a / num_total ) * 100)
##                message = str(a+1) + " de " + str(num_filmes)
##                progress.update( percent, 'A Finalizar ...', message, "" )
##                xbmc.sleep(20)

        proxima = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
        try:
                addDir("[B]Página Seguinte >>[/B]",proxima[0].replace('&amp;','&'),58,artfolder + 'PAGS1.png','','')
        except:pass
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


