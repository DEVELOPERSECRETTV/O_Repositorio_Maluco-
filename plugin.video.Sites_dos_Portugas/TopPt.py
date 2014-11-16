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


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,time,os,FilmesAnima,Mashup
from array import array
from string import capwords
from Mashup import thetvdb_api,themoviedb_api,themoviedb_api_tv,theomapi_api

arr_series = ['' for i in range(500)]
arrai_series = ['' for i in range(500)]
_series_ = []
_series = []
_s_ = []
sri = []

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
                toppt_source = TPT_abrir_url(url_toppt)
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
                addDir('[COLOR yellow]- Top Filmes[/COLOR]','http://toppt.net/',258,artfolder + 'TPF.png','nao','')
                if selfAddon.getSetting('hide-porno') == "false":
                                addDir('[B][COLOR red]M+18[/B][/COLOR]',saber_url_M18[0],232,artfolder + 'TPT1.png','nao','')		
                addDir1('[COLOR blue]Séries:[/COLOR]','url',1001,artfolder + 'TPT1.png',False,'')
                addDir('[COLOR yellow]- A a Z[/COLOR]','urlTPT',241,artfolder + 'SAZ1.png','nao','')#241
                addDir('[COLOR yellow]- Últimos Episódios[/COLOR]',saber_url_series[0],232,artfolder + 'UE.png','nao','')
                addDir('[COLOR yellow]- Top Séries[/COLOR]','http://toppt.net/',259,artfolder + 'TPS.png','nao','')
        except:pass

def TPT_Menu_Posts_Recentes(artfolder):
        url_recentes = 'http://toppt.net/'
        recentes_source = TPT_abrir_url(url_recentes)
        posts_recentes = re.compile('<a href="(.+?)">.+?</a>\n</li>\n<li>\n').findall(recentes_source)
        for endereco_recentes in posts_recentes:                
                try:
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('(PT-PT)',"")
                        nome = nome.replace('(PT/PT)',"")
                        nome = nome.replace('[PT-PT]',"")
                        nome = nome.replace('[PT/PT]',"")
                        addDir('[B][COLOR green]' + nome + '[/COLOR][/B]',endereco_recentes,233,'','','')
                except: pass

def antiga_TPT_Menu_Filmes_Por_Ano(artfolder): #antiga
        url_ano = 'http://toppt.net/'
        ano_source = TPT_abrir_url(url_ano)
        filmes_por_ano = re.compile('<option class="level-0" value="(.+?)">(.+?)</option>').findall(ano_source)
	for num_cat,nome_ano in filmes_por_ano:
                endereco_ano = 'http://toppt.net/?cat=' + str(num_cat)
		addDir('[COLOR yellow]' + nome_ano + '[/COLOR] ',endereco_ano,232,artfolder + 'TPT1.png','nao','')
		if str(nome_ano) == '2014': break

def TPT_Menu_Filmes_Por_Ano(artfolder):
        ano = 2014
        for x in range(46):
                categoria_endereco = 'http://toppt.net/category/' + str(ano) + '/'
                addDir('[COLOR yellow]' + str(ano) + '[/COLOR]',categoria_endereco,232,artfolder + 'TPT1.png','nao','')
                ano = ano - 1

def TPT_Menu_Top_Filmes(artfolder):
        i = 1
        num = 22.0
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
        url_ano = 'http://toppt.net/'
        top_source = TPT_abrir_url(url_ano)
        filmes_por_ano = re.findall('<h3 class="widgettitle">TOP FILMES</h3>(.+?)<ul class="widget-container">', top_source, re.DOTALL)
	for tp_filmes in filmes_por_ano:
                endereco_tf = re.compile('<a href="(.+?)".+?<img.+?src="(.+?)"').findall(tp_filmes)
                for tpe,tph in endereco_tf:
                        #addLink(tpe,'','')
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(int(num))
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        try:
                                html_source = TPT_abrir_url(tpe)
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
                                ano = re.compile("<b>ANO:.+?/b>(.+?)<br/>").findall(items[0])
                                imdbcode = ''
                                anofilme = ''

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
                                fanart,tmdb_id,thumb = themoviedb_api().fanart_and_id(nome_pesquisa,'')
                                if imdbcode != '': sinopse = theomapi_api().sinopse(imdbcode)

                                if genero == '':
                                        genre = '---'
                                        genero = '---'
                                if sinopse == '':
                                        plot = '---'
                                        sinopse = '---'
                                if fanart == '---': fanart = ''
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
                                if tph == '': tph = '---'
                                addDir_teste('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano_filme + ')[/COLOR]',tpe+'IMDB'+imdbcode+'IMDB',233,tph,sinopse,fanart,ano_filme,genero)
                                #addDir('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano_filme + ')[/COLOR]',tpe+'IMDB'+imdbcode+'IMDB',233,tph,'nao','')

                        except: pass        
                        i = i + 1
        progress.close()

def TPT_Menu_Top_Series(artfolder):
        i = 1
        num = 10.0
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
        url_ano = 'http://toppt.net/'
        top_source = TPT_abrir_url(url_ano)
        filmes_por_ano = re.findall('<h3 class="widgettitle">TOP SÉRIES</h3>(.+?)<ul class="widget-container">', top_source, re.DOTALL)
	for tp_filmes in filmes_por_ano:
                endereco_tf = re.compile('<a href="(.+?)".+?<img.+?src="(.+?)"').findall(tp_filmes)
                for tpe,tph in endereco_tf:
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(int(num))
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        try:
                                html_source = TPT_abrir_url(tpe)
                        except: html_source = ''
                        items = re.findall('<div id="content">(.*?)<span id="more', html_source, re.DOTALL)
                        if items != []:
                                urletitulo = re.compile('class="title">(.+?)<').findall(items[0])
                                ano = re.compile("<b>ANO:.+?/b>(.+?)<br/>").findall(items[0])
                                if ano: ano_filme = ano[0].replace(' ','')
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
                                #if fanart == '':
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
       
                                if genero == '':
                                        genre = '---'
                                        genero = '---'
                                if sinopse == '':
                                        plot = '---'
                                        sinopse = '---'
                                if fanart == '---': fanart = ''
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
                                addDir_teste('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano_filme + ')[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',233,thumb,sinopse,fanart,ano_filme.replace('(','').replace(')',''),genero)

                                #addDir('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano_filme + ')[/COLOR]',tpe,233,tph,sinopse,fanart)
                        except: pass
                        i = i + 1
        progress.close()

def TPT_Menu_Filmes_Por_Categorias(artfolder):
        conta_os_items = 0
        url_categorias = 'http://toppt.net/'
        html_categorias_source = TPT_abrir_url(url_categorias)
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

def TPT_Menu_Series_A_a_Z(artfolder,url):
        conta_os_items = 0
        i = 1
        s = 0
        num = 0
        conta = 0
        conta_items = 1
        
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )

##        try:
##                Series_Fi = open(folder + 'series.txt', 'r')
##                Series_Fi.close()
##                Mashup.Series_Series(url)
##        except: pass
                

        folder = perfil
        Series_File = open(folder + 'series.txt', 'a')
        Series_Fi = open(folder + 'series.txt', 'r')
        read_Series_File = ''
        for line in Series_Fi:
                read_Series_File = read_Series_File + line
                if line!='':_series_.append(line)
        urltpt = 'http://toppt.net/'
        
        try:
                html_series_source = TPT_abrir_url(urltpt)
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
	#return
        num = s + 0.0
        url = 'http://toppt.net/'
        site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
        try:
                html_series_source = TPT_abrir_url(url)
        except: html_series_source = ''
	html_items_series = re.findall('<a href="http://toppt.net/category/series/">SÈRIES NOVAS</a>(.*?)<div class="clearfix">', html_series_source, re.DOTALL)
        print len(html_items_series)
        for item_series in html_items_series:
                series = re.compile('<a href="(.+?)">(.+?)</a>').findall(item_series)
                for endereco_series,nome_series in series:
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
                                percent = int( ( i / num ) * 100)
                                message = str(i) + " de " + str(int(num))
                                progress.update( percent, 'A Procurar Séries em '+site, message, "" )
                                print str(i) + " de " + str(int(num))
                                if progress.iscanceled():
                                        break
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

                                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                                        arr_series[i] = nome_series
                        else:
                                try:
                                        html_source = TPT_abrir_url(endereco_series)
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
                                        
##                                        snpse = re.compile("<b>SINOPSE:.+?/b>(.+?)<br/>").findall(items[0])
##                                        if not snpse: snpse = re.compile("<b>SINOPSE:.+?</b>(.+?)<br/>").findall(items[0])
##                                        if snpse: sinopse = snpse[0]
##                                        else:
##                                                try:
##                                                        fonte_video = TPT_abrir_url(urletitulo[0][0])
##                                                except: fonte_video = ''
##                                                fontes_video = re.findall('<div class="postmeta-primary">(.*?)<div id="sidebar-primary">', fonte_video, re.DOTALL)
##                                                if fontes_video != []:
##                                                        snpse = re.compile('Sinopse.png".+?/><br/>\n(.+?)</p>').findall(fontes_video[0])
##                                                        if snpse: sinopse = snpse[0]
##                                                        else: sinopse = ''
##                                        sinopse = sinopse.replace('&#8216;',"'")
##                                        sinopse = sinopse.replace('&#8217;',"'")
##                                        sinopse = sinopse.replace('&#8211;',"-")
##                                        sinopse = sinopse.replace('&#8220;',"'")
##                                        sinopse = sinopse.replace('&#8221;',"'")
##                                        sinopse = sinopse.replace('&#39;',"'")
##                                        sinopse = sinopse.replace('&amp;','&')

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
                                                if snpse: sinopse = snpse[0]
                                                
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
                        if nome_series in arr_series:
                                _imdb = re.compile('[|]IMDBCODE[|](.+?)[|](.+?)[|](.+?)[|]THUMB[|]').findall(arrai_series[arr_series.index(nome_series)])
                                if not _imdb:
                                        _imdb = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(arrai_series[arr_series.index(nome_series)])
                                        if _imdb:
                                                if 'toppt' not in _imdb[0]:
                                                        imdb = _imdb[0]
                                                        arrai_series[arr_series.index(nome_series)]=arrai_series[arr_series.index(nome_series)].replace(imdb,imdb+'|'+endereco_series)
                        if nome_series not in arr_series:
                                percent = int( ( i / num ) * 100)
                                message = str(i) + " de " + str(int(num))
                                progress.update( percent, 'A Procurar Séries em '+site, message, "" )
                                print str(i) + " de " + str(int(num))
                                if progress.iscanceled():
                                        break
                                arr_series[i] = nome_series
                                if 'IMDB' in imdbcode:
                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                else:
                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                        i = i + 1
        html_items_series = re.findall('href="http://toppt.net/category/series/">SÉRIES</a>(.*?)<div id="main">', html_series_source, re.DOTALL)
        print len(html_items_series)
        for item_series in html_items_series:
                series = re.compile('<a href="(.+?)">(.+?)</a>').findall(item_series)
                for endereco_series,nome_series in series:
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
                                percent = int( ( i / num ) * 100)
                                message = str(i) + " de " + str(int(num))
                                progress.update( percent, 'A Procurar Séries em '+site, message, "" )
                                print str(i) + " de " + str(int(num))
                                if progress.iscanceled():
                                        break
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
                                                        
                                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                                        arr_series[i] = nome_series

                        else:
                                try:
                                        html_source = TPT_abrir_url(endereco_series)
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
                                        
##                                        snpse = re.compile("<b>SINOPSE:.+?/b>(.+?)<br/>").findall(items[0])
##                                        if not snpse: snpse = re.compile("<b>SINOPSE:.+?</b>(.+?)<br/>").findall(items[0])
##                                        if snpse: sinopse = snpse[0]
##                                        else:
##                                                try:
##                                                        fonte_video = TPT_abrir_url(urletitulo[0][0])
##                                                except: fonte_video = ''
##                                                fontes_video = re.findall('<div class="postmeta-primary">(.*?)<div id="sidebar-primary">', fonte_video, re.DOTALL)
##                                                if fontes_video != []:
##                                                        snpse = re.compile('Sinopse.png".+?/><br/>\n(.+?)</p>').findall(fontes_video[0])
##                                                        if snpse: sinopse = snpse[0]
##                                                        else: sinopse = ''
##                                        sinopse = sinopse.replace('&#8216;',"'")
##                                        sinopse = sinopse.replace('&#8217;',"'")
##                                        sinopse = sinopse.replace('&#8211;',"-")
##                                        sinopse = sinopse.replace('&#8220;',"'")
##                                        sinopse = sinopse.replace('&#8221;',"'")
##                                        sinopse = sinopse.replace('&#39;',"'")
##                                        sinopse = sinopse.replace('&amp;','&')

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
                                                if snpse: sinopse = snpse[0]
                                                
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
                        if nome_series in arr_series:
                                _imdb = re.compile('[|]IMDBCODE[|](.+?)[|](.+?)[|](.+?)[|]THUMB[|]').findall(arrai_series[arr_series.index(nome_series)])
                                if not _imdb:
                                        _imdb = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(arrai_series[arr_series.index(nome_series)])
                                        if _imdb:
                                                if 'toppt' not in _imdb[0]:
                                                        imdb = _imdb[0]
                                                        arrai_series[arr_series.index(nome_series)]=arrai_series[arr_series.index(nome_series)].replace(imdb,imdb+'|'+endereco_series)
                        if nome_series not in arr_series:
                                percent = int( ( i / num ) * 100)
                                message = str(i) + " de " + str(int(num))
                                progress.update( percent, 'A Procurar Séries em '+site, message, "" )
                                print str(i) + " de " + str(int(num))
                                if progress.iscanceled():
                                        break
                                arr_series[i] = nome_series
                                if 'IMDB' in imdbcode:
                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                else:
                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                        i = i + 1
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
                        if _f: fanart = _f[0]
                        else: fanart = '---'
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
                        if fanart == '---': fanart = ''
                        addDir_teste('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR]',imdbcode,3006,thumb,sinopse,fanart,ano,genero)
        Series_File = open(folder + 'series.txt', 'w')
        for x in range(len(_series_)):
                if _series_[x] != '': Series_File.write(_series_[x])
        #Series_File.write
        Series_Fi.close()
        Series_File.close()
        progress.close()

        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(515)")
        #xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#

def TPT_encontrar_fontes_filmes(url,artfolder):
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
        i = 1
        n_name = name.replace('[COLOR yellow]','')
        n_name = n_name.replace('[/COLOR]','')
        series = 0
	try:
		html_source = TPT_abrir_url(url)
	except: html_source = ''
	items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		num = len(items) + 0.0
		for item in items:
                        sinopse = ''
                        fanart = ''
                        thumb = ''
                        genero = ''
                        qualidade = ''
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(len(items))
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(len(items))
                        #if fan == 'nao': xbmc.sleep( 200 )
                        if progress.iscanceled():
                                break
                        audio_filme = ''

                        imdbcode = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
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
                        
##                        snpse = re.compile("<b>SINOPSE:.+?/b>(.+?)<br/>").findall(item)
##                        if not snpse: snpse = re.compile("<b>SINOPSE:.+?</b>(.+?)<br/>").findall(item)
##                        if snpse: sinopse = snpse[0]
##                        else:
##                                try:
##                                        fonte_video = TPT_abrir_url(urletitulo[0][0])
##                                except: fonte_video = ''
##                                fontes_video = re.findall('<div class="postmeta-primary">(.*?)<div id="sidebar-primary">', fonte_video, re.DOTALL)
##                                if fontes_video != []:
##                                        snpse = re.compile('Sinopse.png".+?/><br/>\n(.+?)</p>').findall(fontes_video[0])
##                                        if snpse: sinopse = snpse[0]
##                                        else: sinopse = ''
##                        sinopse = sinopse.replace('&#8216;',"'")
##                        sinopse = sinopse.replace('&#8217;',"'")
##                        sinopse = sinopse.replace('&#8211;',"-")
##                        sinopse = sinopse.replace('&#8220;',"'")
##                        sinopse = sinopse.replace('&#8221;',"'")
##                        sinopse = sinopse.replace('&#39;',"'")
##                        sinopse = sinopse.replace('&amp;','&')
                                        
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
                                        
                        ###############################
                                        
                        if 'Temporada' in nome or 'Season' in nome or 'Mini-Série' in nome:
                                n = re.compile('(.+?)[[].+?[]]').findall(nome)
                                if n: nome_pesquisa = n[0]
                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme)
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
                                if snpse: sinopse = snpse[0]
                        else:
                                nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?)[:] ').findall(nome)
                                if nnnn: nome_pesquisa = nnnn[0]
                                else: nome_pesquisa = nome
                                fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano_filme)
                                if thumb == '': thumb = poster
                                if imdbcode != '': sinopse = theomapi_api().sinopse(imdbcode)

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
                                #n1 = nome
                                #n2 = ''
                                qualidade = ''
                                ano_filme = ''
                                audio_filme = ''
                        #elif 'Season' not in nome and 'Temporada' not in nome:
                                #n = re.compile('[[](.+?)[]][[](.+?)[]]').findall(nome)
                                #if not n: n = re.compile('[[](.+?)[]] [[](.+?)[]]').findall(nome)
                                #if n:
                                        #n1 = n[0][0]
                                        #n2 = n[0][1]
                                #else:
                                        #n = re.compile('[(](.+?)[)][(](.+?)[)]').findall(nome)
                                        #if not n: n = re.compile('[(](.+?)[)] [(](.+?)[)]').findall(nome)
                                        #if n:
                                                #n1 = n[0][0]
                                                #n2 = n[0][1]
                                        #else:
                                                #n = re.compile('[[](.+?)[]]').findall(nome)
                                                #if n:
                                                        #n1 = n[0]
                                                        #n2 = ''
                                                #else:
                                                        #n = re.compile('[(](.+?)[)]').findall(nome)
                                                        #if n:
                                                                #n1 = n[0]
                                                                #n2 = ''
                                                        #else:
                                                                #n1 = nome
                                                                #n2 = ''
                        #else:
                                #n1 = nome
                                #n2 = ''
                                
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
                                addDir_teste('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',233,thumb,sinopse,fanart,ano_filme.replace('(','').replace(')',''),genero)
                                #addDir_teste('[B][COLOR green]' + n1 + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]'+'[COLOR nnn]'+n2+'[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',233,thumb,sinopse,fanart,ano_filme.replace('(','').replace(')',''),genero)
                        except: pass
                        i = i + 1
                        
	else:
		items = re.compile('<h1 class="entry-title"><a href="(.+?)" .+?>(.+?)</a>').findall(html_source)
		for endereco,nome in items:
                        try:
                                addDir(nome,endereco,233,'','','')
                        except:pass
	proxima = re.compile('</span><a class="nextpostslink" rel="next" href="(.+?)">&raquo;</a><a class="last"').findall(html_source)
	try:
                if n_name == '- Recentes' or name == 'Seguinte >>':
                        addDir("Seguinte >>",proxima[0].replace('#038;','').replace('&amp;','&'),232,artfolder + 'PAGS1.png','','')
                else:
                        addDir("Página Seguinte >>",proxima[0].replace('#038;','').replace('&amp;','&'),232,artfolder + 'PAGS1.png','','')
        except:pass
        progress.close()


#----------------------------------------------------------------------------------------------------------------------------------------------#
                
def TPT_encontrar_videos_filmes(name,url,iconimage):
        iconimage = iconimage
        nomeescolha = name
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]
        if 'TPT' not in name: name = '[COLOR orange]TPT | [/COLOR]' + name
        if 'TPT' not in nomeescolha: nomeescolha = '[COLOR orange]TPT | [/COLOR]' + nomeescolha
        conta_os_items = 0
        nometitulo = nomeescolha
        #return
        if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo:
                num = 0
                percent = 0
                message = ''
                progress.create('Progresso', 'A Procurar streams...')
                progress.update( percent, "", message, "" )
        i = 1
        conta_id_video = 0
        contaultimo = 0
        ##############################################
        n1 = ''
        n2 = ''
        if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo:
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
##                nn = nomeescolha.replace('[B][COLOR green]','--').replace('[/COLOR][/B]','--').replace('[COLOR orange]','').replace('[/COLOR]','').replace('[','---').replace(']','---').replace('TPT | ','')
##                if '---' in nn:
##                        n = re.compile('---(.+?)---').findall(nn)
##                        n1 = re.compile('--(.+?)--').findall(nn)
##                        addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1[0],'url',1004,iconimage,False,fanart)
##                        addDir('[COLOR yellow]PROCURAR POR: [/COLOR]'+n[0],'IMDB'+imdbcode+'IMDB',7,iconimage,'',fanart)
##                else:
##                        n1 = re.compile('--(.+?)--').findall(nn)
##                        addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1[0],'url',1004,iconimage,False,fanart)
        ###############################################
        if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo:
                if n1 != '' and n2 != '':
                        addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n2,'url',1004,iconimage,False,fanart)
                        addDir('[COLOR yellow]PROCURAR POR: [/COLOR]'+n1,'IMDB'+imdbcode+'IMDB',7,iconimage,'',fanart)
                else:
                        addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n2,'url',1004,iconimage,False,fanart)
        
        addDir1(name,'url',9999,iconimage,False,fanart)
        l= 0
	try:
		link2=TPT_abrir_url(url)
	except: link2 = ''
	if link2:
                if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo and imdbcode == '':
                        items = re.findall('<div class="postmeta-primary">(.*?)<div id="sidebar-primary">', link2, re.DOTALL)
                        if items != []:
                                imdb = re.compile('imdb.com/title/(.+?)/').findall(items[0])
                                if imdb: imdbcode = imdb[0]
                                else: imdbcode = ''
                if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo:
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
                #addDir1(str(l),'url',1001,iconimage,False,'')
                if not newmatch:
                        if newmatch1 != [] and 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo:
                                lin = re.findall('.+?EPIS',newmatch1[0],re.DOTALL)
                                num = len(lin) + 0.0 - 1
                                linkseriesssss = re.findall('</span>CLIQUE AQUI PARA VER O (.+?)</div>(.+?)</div></div><',newmatch1[0],re.DOTALL)
                                for parte1,parte2 in linkseriesssss:
                                        if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo:
                                                percent = int( ( i / num ) * 100)
                                                message = str(i) + " de " + str(int(num))
                                                progress.update( percent, "", message, "" )
                                                print str(i) + " de " + str(int(num))
                                                xbmc.sleep( 50 )
                                                if progress.iscanceled():
                                                        break
                                        conta_id_video = 0
                                        addDir1('[COLOR blue]'+parte1+'[/COLOR]','','',iconimage,False,fanart)
                                        match = re.compile('<span class="su-lightbox" data-mfp-src="(.+?)" data-mfp-type="iframe">').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                        i = i + 1
                if newmatch:
                        if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo:
                                match = re.compile('<span class="su-lightbox" data-mfp-src="(.+?)" data-mfp-type="iframe">').findall(newmatch[0])
                                for url in match:
                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                        if 'Season' in nometitulo or 'Temporada' in nometitulo and 'Mini-Série' not in nometitulo:
                                                percent = int( ( i / num ) * 100)
                                                message = str(i) + " de " + str(int(num))
                                                progress.update( percent, "", message, "" )
                                                print str(i) + " de " + str(int(num))
                                                xbmc.sleep( 50 )
                                                if progress.iscanceled():
                                                        break
                                        conta_id_video = 0
                                        addDir1('[COLOR blue]'+parte1+'[/COLOR]','','',iconimage,False,fanart)
                                        match = re.compile('<span class="su-lightbox" data-mfp-src="(.+?)" data-mfp-type="iframe">').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                                        if 'Season' in nometitulo or 'Temporada' in nometitulo and 'Mini-Série' not in nometitulo:
                                                                                percent = int( ( i / num ) * 100)
                                                                                message = str(i) + " de " + str(int(num))
                                                                                progress.update( percent, "", message, "" )
                                                                                print str(i) + " de " + str(int(num))
                                                                                xbmc.sleep( 50 )
                                                                                if progress.iscanceled():
                                                                                        break
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
                                                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                                #return
                                                                nmatch = re.findall(v_id[0]+'.+?DOWNLOAD',link2,re.DOTALL)
                                                                if not nmatch: nmatch = re.findall(v_id[0]+'.+?<nav class="navigation post-navigation"',link2,re.DOTALL)
                                                                linksseccao = re.findall('ODIO (.+?)</p>\n<p><b>(.+?)EPIS',nmatch[0],re.DOTALL)
                                                                if linksseccao:
                                                                        for parte1,parte2 in linksseccao:
                                                                                if 'Season' in nometitulo or 'Temporada' in nometitulo and 'Mini-Série' not in nometitulo:
                                                                                        percent = int( ( i / num ) * 100)
                                                                                        message = str(i) + " de " + str(int(num))
                                                                                        progress.update( percent, "", message, "" )
                                                                                        print str(i) + " de " + str(int(num))
                                                                                        xbmc.sleep( 50 )
                                                                                        if progress.iscanceled():
                                                                                                break
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
                                                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                                #return
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
                                                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                                        #addDir1('sim1','url',1001,artfolder,False,'')
                                                                        for parte1,parte2 in linksseccao:
                                                                                if 'Season' in nometitulo or 'Temporada' in nometitulo and 'Mini-Série' not in nometitulo:
                                                                                        percent = int( ( i / num ) * 100)
                                                                                        message = str(i) + " de " + str(int(num))
                                                                                        progress.update( percent, "", message, "" )
                                                                                        print str(i) + " de " + str(int(num))
                                                                                        xbmc.sleep( 50 )
                                                                                        if progress.iscanceled():
                                                                                                break
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
                                                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                                                if 'Season' in nometitulo or 'Temporada' in nometitulo and 'Mini-Série' not in nometitulo:
                                                                                        percent = int( ( i / num ) * 100)
                                                                                        message = str(i) + " de " + str(int(num))
                                                                                        progress.update( percent, "", message, "" )
                                                                                        print str(i) + " de " + str(int(num))
                                                                                        xbmc.sleep( 50 )
                                                                                        if progress.iscanceled():
                                                                                                break
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
                                                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                                                        if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo:
                                                                                                percent = int( ( i / num ) * 100)
                                                                                                message = str(i) + " de " + str(int(num))
                                                                                                progress.update( percent, "", message, "" )
                                                                                                print str(i) + " de " + str(int(num))
                                                                                                xbmc.sleep( 50 )
                                                                                                if progress.iscanceled():
                                                                                                        break
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
                                                                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
						match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
						if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
						for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                conta_os_items = conta_os_items + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
						match = re.compile('"window.open(.+?)"').findall(newmatch[0])
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
        if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo:
                percent = int( ( 100 / 100.0 ) * 100)
                progress.update( percent, "", message, "" )
        if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo:
                url = 'IMDB'+imdbcode+'IMDB'
                FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n2),'TPT',url)
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
        if 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo: progress.close()


		
#----------------------------------------------------------------------------------------------------------------------------------------------#

def TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart):
        #addLink
        url = url + '///' + nomeescolha
        
        if "videomega" in url:
		try:
                        fonte_id = '(Videomega)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
        if "vidto.me" in url:
		try:
                        match = re.compile('http://vidto.me/embed-(.+?).html').findall(url)
			if match:
				id_video = match[0]
				url = 'http://vidto.me/' + id_video + '.html' + '///' + nomeescolha
			fonte_id = '(Vidto.me)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
        if "dropvideo" in url:
		try:
                        url = url.replace('/video/','/embed/')
                        fonte_id = '(DropVideo)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "vidzi.tv" in url:
                try:
                        fonte_id = '(Vidzi.tv)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "vodlocker" in url:
		try:
                        fonte_id = '(Vodlocker)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "played.to" in url:
                try:
                        fonte_id = '(Played.to)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
        if "cloudzilla" in url:
                try:
                        fonte_id = '(Cloudzilla)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "divxstage" in url:
                try:
                        fonte_id = '(Divxstage)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "vidzen" in url:
                try:
                        fonte_id = '(Vidzen)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
	if "streamin.to" in url:
                try:
                        fonte_id = '(Streamin)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass                        
    	if "nowvideo" in url:
                try:
                        fonte_id = '(Nowvideo)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "primeshare" in url:
                try:
                        fonte_id = '(Primeshare)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videoslasher" in url:
                try:
                        fonte_id = '(VideoSlasher)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "sockshare" in url:
                try:
                        fonte_id = '(Sockshare)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "putlocker" in url:
                try:
                        url = url.replace('putlocker.com/embed/','firedrive.com/file/')
                        fonte_id = '(Firedrive)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	else:
                if "firedrive" in url:
                        try:
                                fonte_id = '(Firedrive)'
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',url,30,iconimage,'',fanart)
                        except:pass
    	if "movshare" in url:
                try:
                        fonte_id = '(Movshare)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',url,30,iconimage,'',fanart)
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
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(VideoWood)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	return
   
	
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
		link2=TPT_abrir_url(url)
	except: link2 = ''
	if link2:
                if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo and imdbcode == '':
                        items = re.findall('<div class="postmeta-primary">(.*?)<div id="sidebar-primary">', link2, re.DOTALL)
                        if items != []:
                                imdb = re.compile('imdb.com/title/(.+?)/').findall(items[0])
                                if imdb: imdbcode = imdb[0]
                                else: imdbcode = ''
                if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo:
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
                        if newmatch1 != [] and 'Season' in nometitulo or 'Temporada' in nometitulo or 'Mini-Série' in nometitulo:
                                lin = re.findall('.+?EPIS',newmatch1[0],re.DOTALL)
                                num = len(lin) + 0.0 - 1
                                linkseriesssss = re.findall('</span>CLIQUE AQUI PARA VER O (.+?)</div>(.+?)</div></div><',newmatch1[0],re.DOTALL)
                                for parte1,parte2 in linkseriesssss:
                                        conta_id_video = 0
                                        addDir1('[COLOR blue]'+parte1+'[/COLOR]','','',iconimage,False,fanart)
                                        match = re.compile('<span class="su-lightbox" data-mfp-src="(.+?)" data-mfp-type="iframe">').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                        i = i + 1
                if newmatch:
                        if 'Season' not in nometitulo and 'Temporada' not in nometitulo and 'Mini-Série' not in nometitulo:
                                match = re.compile('<span class="su-lightbox" data-mfp-src="(.+?)" data-mfp-type="iframe">').findall(newmatch[0])
                                for url in match:
                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                        conta_id_video = conta_id_video + 1
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
                                        match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
                                        for url in match:
                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
						match = re.compile('<a href="(.+?)" target="_blank">.+?</a>').findall(parte2)
						if not match: match = re.compile('O: </b><a href="(.+?)" target="_blank">').findall(parte2)
						for url in match:
                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                                if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
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
                                                        if "videomega" in url or "vidto.me" in url or "dropvideo" in url or "vodlocker" in url or "played.to" in url or "cloudzilla" in url or "vidzen" in url or "vidzi.tv" in url or "divxstage" in url or "streamin.to" in url or "putlocker" in url or "nowvideo" in url or "primeshare" in url or "videoslasher" in url or "sockshare" in url or "firedrive" in url or "movshare" in url or "video.tt" in url or "videowood" in url:
                                                                conta_id_video = conta_id_video + 1
                                                                conta_os_items = conta_os_items + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)
						match = re.compile('"window.open(.+?)"').findall(newmatch[0])
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        url = url.replace("'","").replace("(","").replace(")","")
                                                        conta_os_items = conta_os_items + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,iconimage,fanart)


		
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#	
def TPT_abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

#----------------------------------------------------------------------------------------------------------------------------------------------#
              
def TPT_get_params():
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

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'FAN3.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addLink1(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'FAN3.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,checker,fanart):
        if fanart == '': fanart = artfolder + 'FAN3.jpg'
        #text = 'nnnnnn'
        text = ''
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)+"&checker="+urllib.quote_plus(checker)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',fanart)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": text } )
        #cm = []
	#cm.append(('Sinopse', 'XBMC.Action(Info)'))
	#liz.addContextMenuItems(cm, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir2(nome,url,mode,iconimage,checker,fanart):
        #text = 'nnnnnn'
        text = ''
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&nome="+urllib.quote_plus(nome)+"&checker="+urllib.quote_plus(checker)+"&fanart="+urllib.quote_plus(fanart)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(nome, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'FAN3.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": nome, "Plot": text } )
        #cm = []
	#cm.append(('Sinopse', 'XBMC.Action(Info)'))
	#liz.addContextMenuItems(cm, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir1(name,url,mode,iconimage,folder,fanart):
        if fanart == '': fanart = artfolder + 'FAN3.jpg'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',fanart)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
        return ok

def addDir_teste(name,url,mode,iconimage,plot,fanart,year,genre):
        if fanart == '': fanart = artfolder + 'FAN3.jpg'
        #text = plot
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&plot="+urllib.quote_plus(plot)+"&year="+urllib.quote_plus(year)+"&genre="+urllib.quote_plus(genre)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',fanart)
        #liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Year": year, "Genre": genre } )
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Year": year, "Genre": genre } )
        #cm = []
	#cm.append(('Sinopse', 'XBMC.Action(Info)'))
	#liz.addContextMenuItems(cm, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

#----------------------------------------------------------------------------------------------------------------------------------------------#
	
params=TPT_get_params()
url=None
name=None
mode=None
checker=None
iconimage=None
fanart=None
year=None
plot=None
genre=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        nome=urllib.unquote_plus(params["nome"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:        
        checker=urllib.unquote_plus(params["checker"])
except:
        pass
try:        
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        plot=urllib.unquote_plus(params["plot"])
except:
        pass
try:        
        year=urllib.unquote_plus(params["year"])
except:
        pass
try:        
        genre=urllib.unquote_plus(params["genre"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Checker: "+str(checker)
print "Iconimage: "+str(iconimage)
print "Plot: "+str(plot)
print "Year: "+str(year)
print "Genre: "+str(genre)
print "Fanart: "+str(fanart)

