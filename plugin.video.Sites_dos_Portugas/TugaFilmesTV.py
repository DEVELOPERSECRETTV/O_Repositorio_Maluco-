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
from Mashup import thetvdb_api,themoviedb_api,themoviedb_api_tv

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

progress = xbmcgui.DialogProgress()

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#



def TFV_MenuPrincipal(artfolder):
        fanart = artfolder + 'FAN3.jpg'
        addDir('- Procurar','http://www.tuga-filmes.us/search?q=',1,artfolder + 'P1.png','nao','')
        addDir('[COLOR yellow]- Últimos[/COLOR] (Filmes/Séries)','http://www.tuga-filmes.us',32,artfolder + 'UFS.png','nao','')
        addDir('[COLOR yellow]- Top Semanal[/COLOR]','url',48,artfolder + 'TPSE.png','nao','')
	addDir1('[COLOR blue]Filmes:[/COLOR]','url',1004,artfolder + 'TFV1.png',False,fanart)
	addDir('[COLOR yellow]- Todos[/COLOR]','http://www.tuga-filmes.us/search/label/Filmes',32,artfolder + 'FT.png','nao','')
	addDir('[COLOR yellow]- Animação[/COLOR]','http://www.tuga-filmes.us/search/label/Anima%C3%A7%C3%A3o',32,artfolder + 'FA.png','nao',fanart)
        addDir('[COLOR yellow]- Por Ano[/COLOR]','url',39,artfolder + 'ANO.png','nao','')
	addDir('[COLOR yellow]- Categorias[/COLOR]','url',38,artfolder + 'CT.png','nao','')
		
	#if selfAddon.getSetting('hide-porno') == "false":
			#addDir('[B][COLOR red]M+18[/B][/COLOR]','url',49,artfolder + 'TFV1.png','nao','')
	addDir1('[COLOR blue]Séries:[/COLOR]','url',1004,artfolder + 'TFV1.png',False,fanart)
	addDir('[COLOR yellow]- A a Z[/COLOR]','urlTFV',41,artfolder + 'SAZ1.png','nao','')
        addDir('[COLOR yellow]- Últimos Episódios[/COLOR]','http://www.tuga-filmes.us/search/label/Séries',44,artfolder + 'UE.png','nao','')

def TFV_Menu_Filmes_Top_5(artfolder):
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
        url_top_5 = 'http://www.tuga-filmes.us'
        top_5_source = TFV_abrir_url(url_top_5)
        filmes_top_5 = re.compile("<img alt=\'.+?\' height=\'50\' src=\'.+?\' width=\'50\'/>\n<a href=\'(.+?)\'").findall(top_5_source)
	for endereco_top_5 in filmes_top_5:
                try:
                        html_source = TFV_abrir_url(endereco_top_5)
                except: html_source = ''
                items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
                if items != []:
                        print len(items)
                        for item in items:
                                percent = int( ( i / 5.0 ) * 100)
                                message = str(i) + " de " + '5'
                                progress.update( percent, "", message, "" )
                                print str(i) + " de " + '5'
                                if progress.iscanceled():
                                        break

                                imdbcode = ''
                                fanart = ''
                                sinopse = ''
                                thumb = ''

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

                                if 'Temporada' in urletitulo[0] or 'Season' in urletitulo[0] or 'Mini-Série' in urletitulo[0]:
                                        nome = urletitulo[0]
                                        nnnn = re.compile('(.+?)[(].+?[)]').findall(nome)
                                        if not nnnn: nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                                        if nnnn : nome_pesquisa = nnnn[0]
                                        else: nome_pesquisa = nome
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
                                        addDir('[B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + ano[0] + ')[/COLOR][COLOR red] (' + qualidade[0] + ')[/COLOR]',endereco_top_5+'IMDB'+imdbcode+'IMDB',num_mode,thumbnail[0].replace('s72-c','s320'),sinopse,fanart)
                                except: pass
                                i = i + 1

def TFV_Menu_Filmes_Por_Ano(artfolder):
        i = 0
        url_ano = 'http://www.tuga-filmes.us'
        ano_source = TFV_abrir_url(url_ano)
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
        html_categorias_source = TFV_abrir_url(url_categorias)
	html_items_categorias = re.findall("<div class=\'widget Label\' id=\'Label1\'>(.*?)<div class=\'clear\'>", html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<a dir=\'ltr\' href=\'(.+?)\'>(.+?)</a>").findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        addDir('[COLOR yellow]' + nome_categoria + '[/COLOR] ',endereco_categoria,32,artfolder + 'TFV1.png','nao','')

def TFV_Menu_Series_A_a_Z(artfolder,url):
        i = 1
        
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )

##        Mashup.Series_Series(url)

        folder = perfil
        Series_File = open(folder + 'seriesTFV.txt', 'a') 
        Series_Fi = open(folder + 'seriesTFV.txt', 'r')
        read_Series_File = ''
        for line in Series_Fi:
                read_Series_File = read_Series_File + line
                if line!='':_series_.append(line)

        Series_File_ALL = open(folder + 'series.txt', 'r')
        read_Series_File_ALL = ''
        for linha in Series_File_ALL:
                read_Series_File_ALL = read_Series_File_ALL + linha
                if linha!='':_seriesALL_.append(linha)
                
        url_series = 'http://www.tuga-filmes.us'
	html_series_source = TFV_abrir_url(url_series)
	html_items_series = re.findall("<div class=\'widget Label\' id=\'Label3\'>(.*?)<div class=\'clear\'>", html_series_source, re.DOTALL)
        num_series = re.compile("<a dir=\'ltr\' href=\'(.+?)\'>(.+?)</a>").findall(html_items_series[0])
        print len(html_items_series)
        num = len(num_series) + 0.0
        for item_series in html_items_series:
                series = re.compile("<a dir=\'ltr\' href=\'(.+?)\'>(.+?)</a>").findall(item_series)
                for endereco_series,nome_series in series:
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(len(num_series))
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(len(num_series))
                        #xbmc.sleep( 50 )
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
                                                                        #thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                                                                        snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                                        if sinopse == '---':
                                                                                if snpse: sinopse = snpse[0]
                                                                
                                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|THUMB|'+thumb.replace('s72-c','s320')+'|ANO|'+ano_filme.replace('  ','').replace(' ','')+'|FANART|'+fanart+'|GENERO|'+genre+'|SINOPSE|'+sinopse+'|END|'
                                                        arr_series[i] = nome_series
                        elif nome_series in read_Series_File_ALL:
                                for x in range(len(_seriesALL_)):
                                        if nome_series in _seriesALL_[x]:
                                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_seriesALL_[x])
                                                if _n: nome = _n[0]
                                                else: nome = '---'
                                                if nome_series in nome:
                                                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_seriesALL_[x])
                                                        if _i: imdbcode = _i[0]
                                                        else: imdbcode = '---'
                                                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_seriesALL_[x])
                                                        if _t: thumb = _t[0]
                                                        else: thumb = '---'
                                                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_seriesALL_[x])
                                                        if _a: ano_filme = _a[0]
                                                        else: ano_filme = '---'
                                                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_seriesALL_[x])
                                                        if _f: fanart = _f[0]
                                                        else: fanart = '---'
                                                        _g = re.compile('[|]GENERO[|](.+?)[|]SINOPSE[|]').findall(_seriesALL_[x])
                                                        if _g: genre = _g[0]
                                                        else: genre = '---'
                                                        _s = re.compile('[|]SINOPSE[|](.*)').findall(_seriesALL_[x])
                                                        if _s: s = _s[0]
                                                        if '|END|' in s: sinopse = s.replace('|END|','')
                                                        else:
                                                                si = re.compile('SINOPSE[|](.+?)\n(.+?)[|]END[|]').findall(_seriesALL_[x])
                                                                if si: sinopse = si[0][0] + ' ' + si[0][1]
                                                                else: sinopse = '---'
                                                        if fanart == '' or fanart == '---':
                                                                if selfAddon.getSetting('Fanart') == "true":
                                                                        nome_pesquisa = nome_series
                                                                        thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme.replace('(','').replace(')',''))
                                                                        ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                                                        if ftart: fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                                        #thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                                                                        snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                                        if sinopse == '---':
                                                                                if snpse: sinopse = snpse[0]
                                                                
                                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|THUMB|'+thumb.replace('s72-c','s320')+'|ANO|'+ano_filme.replace('  ','').replace(' ','')+'|FANART|'+fanart+'|GENERO|'+genre+'|SINOPSE|'+sinopse+'|END|'
                                                        arr_series[i] = nome_series                        
                        else:
                                try:
                                        html_source = TFV_abrir_url(endereco_series)
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
                                        else: ano_filme = ''
                                        
                                        if selfAddon.getSetting('Fanart') == "true":
                                                nome_pesquisa = nome_series
                                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme.replace('(','').replace(')',''))
                                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                                if ftart: fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                if sinopse == '---':
                                                        if snpse: sinopse = snpse[0]
                                                
                                        if qualidade:
                                                qualidade = qualidade[0]
                                        else:
                                                qualidade = ''
                                        if ano: ano_filme = ano[0]
                                        else: ano_filme = '---'
                                        if genre == '': genre = '---'
                                        if sinopse == '': sinopse = '---'
                                        if fanart == '': fanart = '---'
                                        if imdbcode == '': imdbcode = '---'
                                        if thumb == '': thumb = '---'
                                        #Series_File.write('NOME|'+nome_series+'|SINOPSE|'+sinopse+'|END|\n')
                                        Series_File.write('NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb.replace('s72-c','s320')+'|ANO|'+ano_filme.replace('  ','').replace(' ','')+'|FANART|'+fanart+'|GENERO|'+genre+'|SINOPSE|'+sinopse+'|END|\n')
                                except: pass
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
                                                #thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                if sinopse == '---':
                                                        if snpse: sinopse = snpse[0]
                                arr_series[i] = nome_series
                                if 'IMDB' in imdbcode:
                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|'+endereco_series+'|THUMB|'+thumb.replace('s72-c','s320')+'|ANO|'+ano_filme.replace('  ','').replace(' ','')+'|FANART|'+fanart+'|GENERO|'+genre+'|SINOPSE|'+sinopse+'|END|'
                                else:
                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb.replace('s72-c','s320')+'|ANO|'+ano_filme.replace('  ','').replace(' ','')+'|FANART|'+fanart+'|GENERO|'+genre+'|SINOPSE|'+sinopse+'|END|'
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
                        addDir_teste('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR]',imdbcode,3007,thumb,sinopse,fanart,ano,genero)
        SeriesFile = open(folder + 'seriesTFV.txt', 'w')
        for x in range(len(arrai_series)):
                if arrai_series[x] != '': SeriesFile.write(arrai_series[x]+'\n')
        Series_Fi.close()
        Series_Fi.close()
        Series_File.close()
        Series_File_ALL.close()
        progress.close()

        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(515)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        

#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#


def TFV_encontrar_fontes_filmes(url,artfolder):
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
	try:
		html_source = TFV_abrir_url(url)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	conta_items = 0
	if items != []:
		print len(items)
		num = len(items) + 0.0
		for item in items:
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(len(items))
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(len(items))
                        #if selfAddon.getSetting('movie-fanart-TFV') == "false": xbmc.sleep( 50 )
                        if progress.iscanceled():
                                break
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
                                if snpse: sinopse = snpse[0]
                        else:
                                #nome = urletitulo[0][1]
                                nnnn = re.compile('.+?[(](.+?)[)]').findall(nome)
                                if not nnnn: nnnn = re.compile('.+?[[](.+?)[]]').findall(nome)
                                if nnnn : nome_pesquisa = nnnn[0]
                                else: nome_pesquisa = nome
                                fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano[0].replace(' ',''))
                                if thumb == '': thumb = poster

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
                                if "Temporada" in urletitulo[0][1] or 'Season' in urletitulo[0][1]:
                                        num_mode = 42
                                else:
                                        num_mode = 33
                                addDir_teste('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',num_mode,thumb.replace('s72-c','s320'),sinopse,fanart,ano[0],genre)
                        except: pass
                        #---------------------------------------------------------------
                        i = i + 1
                        #---------------------------------------------------------------
	else:
		items = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(html_source)
		for endereco,nome in items:
                        try:
                                if "Temporada" in nome:
                                        num_mode = 42
                                else:
                                        num_mode = 33
                                addDir(nome,endereco,num_mode,'','','')
                        except:pass
	proxima = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
	if proxima[0] != '':
                try:
                        addDir("[B]Página Seguinte >>[/B]",proxima[0].replace('&amp;','&'),32,artfolder + 'PAGS1.png','','')
                except:pass
        
        
#----------------------------------------------------------------------------------------------------------------------------------------------#	


def TFV_encontrar_videos_filmes(name,url):
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

        #addDir1('','url',1004,artfolder,False,'')     
	try:
		link2=TFV_abrir_url(url)
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
        if 'Parte 1' and 'Parte 2' not in link2:
                num_leg = 1
                num_ptpt = 1
                matchvid = re.findall("Assistir(.+?)Clique aqui para ver", link2, re.DOTALL)
                if not matchvid: matchvid = re.findall("Assistir(.+?)</p>", link2, re.DOTALL)
                if not matchvid: matchvid = re.findall("Assistir(.+?)\n</p>", link2, re.DOTALL)
                if matchvid:
                        for matchsvids in matchvid:
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
                                                        TFV_resolve_not_videomega_filmes(name,url,id_video,conta_id_video)
                                        except:pass
                else:
                        videomeg = re.compile('<iframe frameborder="0" height="400" scrolling="no" src="(.+?)"').findall(link2)
                        if videomeg:
                                conta_id_video = conta_id_video + 1
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',videomeg[0],30,iconimage,'',fanart)

        if 'Parte 1' and 'Parte 2' in link2:
                matchvid = re.findall("Assistir(.+?)Clique aqui para ver", link2, re.DOTALL)
                if not matchvid: matchvid = re.findall("Assistir(.+?)</p>", link2, re.DOTALL)
                if not matchvid: matchvid = re.findall("Assistir(.+?)\n</p>", link2, re.DOTALL)
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
                                if "videomega" in url:
                                        try:
                                                url = url + '///' + name
                                                addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                        except: pass
                                else:
                                        req = urllib2.Request(url)
                                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                                        response = urllib2.urlopen(req)
                                        link4=response.read()
                                        response.close()
                                        match = re.compile('<iframe src="(.+?)".+?></iframe></center>').findall(link4)
                                        url=match[0]
                                        if "videomega" in url:
                                                try:
                                                        url = 'http://videomega.tv/iframe.php?ref=' + id_video + '///' + name
                                                        print url
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except: pass
                                        if "vidto.me" in url:
                                                try:
                                                        url = 'http://vidto.me/' + id_video + '.html' + '///' + name
                                                        print url
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except: pass
                                        if "dropvideo" in url:
                                                try:
                                                        url = 'http://dropvideo.com/embed/' + id_video + '///' + name
                                                        print url
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if "streamin.to" in url:
                                                try:
                                                        url = 'http://streamin.to/embed-' + id_video + '.html' + '///' + name
                                                        print url
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,30,iconimage,'',fanart)
                                                except:pass                        
                                        if "putlocker" in url:
                                                try:
                                                        url = 'http://www.putlocker.com/embed/' + id_video + '///' + name
                                                        print url
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Putlocker)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if "nowvideo" in url:
                                                try:
                                                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video + '///' + name
                                                        print url
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if "videowood" in url:
                                                try:
                                                        if '/video/' in url: url = url.replace('/video/','/embed/')
                                                        url = 'http://www.videowood.tv/embed/' + id_video + '///' + name
                                                        print url
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](VideoWood)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if "firedrive" in url:
                                                try:
                                                        url = 'http://www.firedrive.com/file/' + id_video + '///' + name
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
##        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(nomeescolha)
##        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
##        nn = nomeescolha.replace('[B][COLOR green]','--').replace('[/COLOR][/B]','--').replace('[COLOR orange]','').replace('[/COLOR]','').replace('[','---').replace(']','---').replace('TPT | ','')
##        #addDir1('','url',1004,artfolder,False,'')

        url = 'IMDB'+imdbcode+'IMDB'
        FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n1),'TFV',url)
        
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

def TFV_resolve_not_videomega_filmes(name,url,id_video,conta_id_video):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link4=response.read()
        response.close()
        match = re.compile('<iframe src="(.+?)".+?></iframe></center>').findall(link4)
        url=match[0]
        if "videomega" in url:
		try:
                        url = 'http://videomega.tv/iframe.php?ref=' + id_video + '///' + name
                        print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
        if "vidto.me" in url:
		try:
                        url = 'http://vidto.me/' + id_video + '.html' + '///' + name
                        print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
        if "dropvideo" in url:
		try:
                        url = 'http://dropvideo.com/embed/' + id_video + '///' + name
			print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "streamin.to" in url:
                try:
                        url = 'http://streamin.to/embed-' + id_video + '.html' + '///' + name
			print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,30,iconimage,'',fanart)
                except:pass                        
        if "putlocker" in url:
                try:
                        url = 'http://www.putlocker.com/embed/' + id_video + '///' + name
                        print url
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Putlocker)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "nowvideo" in url:
                try:
                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video + '///' + name
                        print url
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        url = 'http://www.videowood.tv/embed/' + id_video + '///' + name
                        print url
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoWood)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "firedrive" in url:
                try:
                        url = 'http://www.firedrive.com/file/' + id_video + '///' + name
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                except:pass
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
		link2=TFV_abrir_url(url)
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
        if 'Parte 1' and 'Parte 2' not in link2:
                num_leg = 1
                num_ptpt = 1
                matchvid = re.findall("Assistir(.+?)Clique aqui para ver", link2, re.DOTALL)
                if not matchvid: matchvid = re.findall("Assistir(.+?)</p>", link2, re.DOTALL)
                if not matchvid: matchvid = re.findall("Assistir(.+?)\n</p>", link2, re.DOTALL)
                if matchvid:
                        for matchsvids in matchvid:
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
                                                  ##################      
                                                        req = urllib2.Request(url)
                                                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                                                        response = urllib2.urlopen(req)
                                                        link4=response.read()
                                                        response.close()
                                                        matchs = re.compile('<iframe src="(.+?)".+?></iframe></center>').findall(link4)
                                                        url=matchs[0]
                                                        if "videomega" in url:
                                                                try:
                                                                        url = 'http://videomega.tv/iframe.php?ref=' + id_video + '///' + name
                                                                        print url
                                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                                except: pass
                                                        if "vidto.me" in url:
                                                                try:
                                                                        url = 'http://vidto.me/' + id_video + '.html' + '///' + name
                                                                        print url
                                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                                except: pass
                                                        if "dropvideo" in url:
                                                                try:
                                                                        url = 'http://dropvideo.com/embed/' + id_video + '///' + name
                                                                        print url
                                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                                except:pass
                                                        if "streamin.to" in url:
                                                                try:
                                                                        url = 'http://streamin.to/embed-' + id_video + '.html' + '///' + name
                                                                        print url
                                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,30,iconimage,'',fanart)
                                                                except:pass                        
                                                        if "putlocker" in url:
                                                                try:
                                                                        url = 'http://www.putlocker.com/embed/' + id_video + '///' + name
                                                                        print url
                                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Putlocker)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                                except:pass
                                                        if "nowvideo" in url:
                                                                try:
                                                                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video + '///' + name
                                                                        print url
                                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                                except:pass
                                                        if "videowood" in url:
                                                                try:
                                                                        if '/video/' in url: url = url.replace('/video/','/embed/')
                                                                        url = 'http://www.videowood.tv/embed/' + id_video + '///' + name
                                                                        print url
                                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoWood)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                                except:pass
                                                        if "firedrive" in url:
                                                                try:
                                                                        url = 'http://www.firedrive.com/file/' + id_video + '///' + name
                                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                                except:pass
                                                        ##################        
                                                        #TFV_resolve_not_videomega_filmes(name,url,id_video,conta_id_video)
                                        except:pass
                else:
                        videomeg = re.compile('<iframe frameborder="0" height="400" scrolling="no" src="(.+?)"').findall(link2)
                        if videomeg:
                                conta_id_video = conta_id_video + 1
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',videomeg[0],30,iconimage,'',fanart)

        if 'Parte 1' and 'Parte 2' in link2:
                matchvid = re.findall("Assistir(.+?)Clique aqui para ver", link2, re.DOTALL)
                if not matchvid: matchvid = re.findall("Assistir(.+?)</p>", link2, re.DOTALL)
                if not matchvid: matchvid = re.findall("Assistir(.+?)\n</p>", link2, re.DOTALL)
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
                                if "videomega" in url:
                                        try:
                                                url = url + '///' + name
                                                addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                        except: pass
                                else:
                                        req = urllib2.Request(url)
                                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                                        response = urllib2.urlopen(req)
                                        link4=response.read()
                                        response.close()
                                        match = re.compile('<iframe src="(.+?)".+?></iframe></center>').findall(link4)
                                        url=match[0]
                                        if "videomega" in url:
                                                try:
                                                        url = 'http://videomega.tv/iframe.php?ref=' + id_video + '///' + name
                                                        print url
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except: pass
                                        if "vidto.me" in url:
                                                try:
                                                        url = 'http://vidto.me/' + id_video + '.html' + '///' + name
                                                        print url
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except: pass
                                        if "dropvideo" in url:
                                                try:
                                                        url = 'http://dropvideo.com/embed/' + id_video + '///' + name
                                                        print url
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if "streamin.to" in url:
                                                try:
                                                        url = 'http://streamin.to/embed-' + id_video + '.html' + '///' + name
                                                        print url
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,30,iconimage,'',fanart)
                                                except:pass                        
                                        if "putlocker" in url:
                                                try:
                                                        url = 'http://www.putlocker.com/embed/' + id_video + '///' + name
                                                        print url
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Putlocker)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if "nowvideo" in url:
                                                try:
                                                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video + '///' + name
                                                        print url
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if "videowood" in url:
                                                try:
                                                        if '/video/' in url: url = url.replace('/video/','/embed/')
                                                        url = 'http://www.videowood.tv/embed/' + id_video + '///' + name
                                                        print url
                                                        addDir('[B][COLOR blue]'+nome+'[/COLOR] - Fonte : [COLOR yellow](VideoWood)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if "firedrive" in url:
                                                try:
                                                        url = 'http://www.firedrive.com/file/' + id_video + '///' + name
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass



#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Séries  -----------------------------------------------------------------#


                                
def TFV_encontrar_fontes_series_recentes(url):
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
	try:
		html_source = TFV_abrir_url(url)
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
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(len(items))
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(len(items))
                        #if selfAddon.getSetting('series-fanart-TFV') == "false": xbmc.sleep( 50 )
                        if progress.iscanceled():
                                break
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
				addDir_teste('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano + '[/COLOR][COLOR red] ' + qualidade + '[/COLOR]',urletitulo[0][0],42,thumb.replace('s72-c','s320'),sinopse,fanart,ano,genero)
			except: pass
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

def TFV_encontrar_videos_series(name,url):
        urlseries = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlseries: url = url.replace('IMDBIMDB','')
        else: url = urlseries[0]
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
        conta_id_video = 0
	try:
		link_series=TFV_abrir_url(url)
	except: link_series = ''
        addDir1(name,'url',1004,iconimage,False,fanart)
	if link_series:
                try:
                        items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", link_series, re.DOTALL)
                        items_series = re.findall('<div class=(.+?)</a>', items[0], re.DOTALL)
                        if not items_series: items_series = re.findall("<div class=(.+?)</p>", items[0], re.DOTALL)
                        n_items = len(items_series)
                        if 'calendar_title' in items[0]: n_items = n_items - 1
                        divide = n_items + 0.0
                        for item_vid_series in items_series:
                                try:
##                                        if 'div class=' in item_vid_series:
##                                                ivs = re.compile('class=.+?>(.*)').findall(item_vid_series)
##                                                if ivs: item_vid_series = ivs[0]
                                        if 'videomega' in item_vid_series:
                                                try:
                                                        if 'div class=' in item_vid_series: videomega_video_nome = re.compile('class=.+?>(.+?)</div></h3>').findall(item_vid_series)
                                                        videomega_video_nome = re.compile('>(.+?)</div></h3><p>').findall(item_vid_series)
                                                        if not videomega_video_nome: videomega_video_nome = re.compile('>(.+?)</div></h3><a').findall(item_vid_series)
                                                        if 'div class=' in videomega_video_nome[0]: videomega_video_nome = re.compile('div class=.+?>(.*)').findall(videomega_video_nome[0])
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
                                                        not_videomega_video_nome = re.compile('>(.+?)</div></h3><p>').findall(item_vid_series)
                                                        if not not_videomega_video_nome: not_videomega_video_nome = re.compile('>(.+?)</div></h3><a').findall(item_vid_series)
                                                        if 'div class=' in not_videomega_video_nome[0]: not_videomega_video_nome = re.compile('div class=.+?>(.*)').findall(not_videomega_video_nome[0])
                                                        nome_cada_episodio = not_videomega_video_nome[0]
                                                        url = not_videomega_video_url[0]
                                                        identifica_video = re.compile('=(.*)').findall(not_videomega_video_url[0])                                                        
                                                        id_video = identifica_video[0]
                                                        src_href = 'src'
                                                        nome_cada_episodio = nome_cada_episodio.replace('&#8217;',"'")
                                                        nome_cada_episodio = nome_cada_episodio.replace('&#8211;',"-")
                                                        nome_cada_episodio = nome_cada_episodio.replace('&#39;',"'")
                                                        nome_cada_episodio = nome_cada_episodio.replace('&amp;','&')
                                                        TFV_resolve_not_videomega_series(name,url,id_video,nome_cada_episodio,src_href)
                                                except:pass
                                        if 'href' and 'Clique' in item_vid_series:
                                                try:
                                                        not_videomega_video_url = re.compile('<a href="(.+?)"').findall(item_vid_series)
                                                        if not not_videomega_video_url: not_videomega_video_url = re.compile('<a class=".+?" href="(.+?)"').findall(item_vid_series)
                                                        
                                                        not_videomega_video_nome = re.compile('>(.+?)</div></h3><p>').findall(item_vid_series)
                                                        if not not_videomega_video_nome: not_videomega_video_nome = re.compile('>(.+?)</div></h3><a').findall(item_vid_series)
                                                        if 'div class=' in not_videomega_video_nome[0]: not_videomega_video_nome = re.compile('div class=.+?>(.*)').findall(not_videomega_video_nome[0])
                                                        
                                                        nome_cada_episodio = not_videomega_video_nome[0]
                                                        url = not_videomega_video_url[0]
                                                        identifica_video = re.compile('=(.*)').findall(not_videomega_video_url[0])                                                        
                                                        id_video = identifica_video[0]
                                                        src_href = 'href'
                                                        nome_cada_episodio = nome_cada_episodio.replace('&#8217;',"'")
                                                        nome_cada_episodio = nome_cada_episodio.replace('&#8211;',"-")
                                                        nome_cada_episodio = nome_cada_episodio.replace('&#39;',"'")
                                                        nome_cada_episodio = nome_cada_episodio.replace('&amp;','&')
                                                        TFV_resolve_not_videomega_series(name,url,id_video,nome_cada_episodio,src_href)
                                                except:pass
                                        #if 'calendar_title' not in item_vid_series:
                                        percent = int( ( i / divide ) * 100)
                                        message = str(i) + " de " + str(int(divide)) + ' Links'
                                        progress.update( percent, "", message, "" )
                                        print str(i) + " de " + str(int(divide)) + ' Links'
                                        xbmc.sleep(50)
                                        if progress.iscanceled():
                                                break
                                        if i != int(divide): i = i + 1
                                except:pass
                except:pass
        
#----------------------------------------------------------------------------------------------------------------------------------------------#
	
def TFV_resolve_not_videomega_series(name,url,id_video,nome_cada_episodio,src_href):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link4=response.read()
        response.close()
        if src_href == 'href':
                match = re.compile('<iframe src="(.+?)".+?></iframe>').findall(link4)
        if src_href == 'src':
                match = re.compile('<iframe .+? src="(.+?)" .+?></iframe>').findall(link4)
        url=match[0]        
        if "videomega" in url:
		try:
                        url = 'http://videomega.tv/iframe.php?ref=' + id_video + '///' + name
                        print url
			addDir('[COLOR blue]' + nome_cada_episodio + '[/COLOR][B] - Fonte : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
        if "vidto.me" in url:
		try:
                        url = 'http://vidto.me/' + id_video + '.html' + '///' + name
                        print url
			addDir('[COLOR blue]' + nome_cada_episodio + '[/COLOR][B] - Fonte : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
        if "dropvideo" in url:
		try:
                        url = 'http://dropvideo.com/embed/' + id_video + '///' + name
			print url
			addDir('[COLOR blue]' + nome_cada_episodio + '[/COLOR][B] - Fonte : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except:pass
	if "streamin.to" in url:
                try:
                        url = 'http://streamin.to/embed-' + id_video + '.html' + '///' + name
			print url
			addDir('[COLOR blue]' + nome_cada_episodio + '[/COLOR][B] - Fonte : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,30,iconimage,'',fanart)
                except:pass                        
        if "putlocker" in url:
                try:
                        url = 'http://www.putlocker.com/embed/' + id_video + '///' + name
                        print url
                        addDir('[COLOR blue]' + nome_cada_episodio + '[/COLOR][B] - Fonte : [COLOR yellow](Putlocker)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "nowvideo" in url:
                try:
                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video + '///' + name
                        print url
                        addDir('[COLOR blue]' + nome_cada_episodio + '[/COLOR][B] - Fonte : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        url = 'http://www.videowood.tv/embed/' + id_video + '///' + name
                        print url
                        addDir('[COLOR blue]' + nome_cada_episodio + '[/COLOR][B] - Fonte : [COLOR yellow](VideoWood)[/COLOR][/B]',url,70,iconimage,'',fanart)
    		except:pass
    	return
                


#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#


	
def TFV_abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

#----------------------------------------------------------------------------------------------------------------------------------------------#
              
def TFV_get_params():
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
        #text = checker
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&checker="+urllib.quote_plus(checker)+"&fanart="+urllib.quote_plus(fanart)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',fanart)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
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
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
        return ok

def addDir_vazio(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	#liz.setProperty('fanart_image',fanart)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addDir_teste(name,url,mode,iconimage,plot,fanart,year,genre):
        if fanart == '': fanart = artfolder + 'FAN3.jpg'
        #text = checker
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)+"&plot="+urllib.quote_plus(plot)+"&year="+urllib.quote_plus(year)+"&genre="+urllib.quote_plus(genre)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',fanart)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Year": year, "Genre": genre } )
        #cm = []
	#cm.append(('Sinopse', 'XBMC.Action(Info)'))
	#liz.addContextMenuItems(cm, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


#----------------------------------------------------------------------------------------------------------------------------------------------#
	
params=TFV_get_params()
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


