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


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,time,os,FilmesAnima,Play
from Funcoes import thetvdb_api, themoviedb_api, themoviedb_api_tv, theomapi_api, themoviedb_api_IMDB, themoviedb_api_IMDB_episodios, themoviedb_api_TMDB
from Funcoes import thetvdb_api_tvdbid, thetvdb_api_episodes, themoviedb_api_search_imdbcode, themoviedb_api_pagina, themoviedb_api_IMDB1, theomapi_api_nome
from Funcoes import addDir, addDir1, addDir2, addLink, addLink1, addDir_teste, addDir_trailer, addDir_episode
from Funcoes import get_params,abrir_url

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

fanart = artfolder + 'FAN3.jpg'

Anos = ['' for i in range(100)]

progress = xbmcgui.DialogProgress()

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#



def CMT_MenuPrincipal(artfolder):
        fanart = artfolder + 'FAN3.jpg'
        addDir('- Procurar','http://www.tuga-filmes.us/search?q=',1,artfolder + 'P1.png','nao','')
	addDir1('[COLOR blue]Filmes:[/COLOR]','url',1004,artfolder + 'CMT1.png',False,fanart)
	addDir('[COLOR yellow]- Todos[/COLOR]','http://www.cinematuga.net/search/label/Filmes',702,artfolder + 'FT.png','nao','')#'http://www.tugafilmes.org/search/label/Filmes'
	addDir('[COLOR yellow]- Animação[/COLOR]','http://www.cinematuga.net/search/label/Anima%C3%A7%C3%A3o',702,artfolder + 'FA.png','nao',fanart)
        addDir('[COLOR yellow]- Por Ano[/COLOR]','url',709,artfolder + 'ANO.png','nao','')
	addDir('[COLOR yellow]- Categorias[/COLOR]','url',708,artfolder + 'CT.png','nao','')
	#addDir('[COLOR yellow]- Top Semanal[/COLOR]','url',718,artfolder + 'TPSE.png','nao','')
	addDir('[COLOR yellow]- Qualidade[/COLOR]','url',719,artfolder,'nao','')

def CMT_Menu_Filmes_Top_5(artfolder):
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
        url_top_5 = 'http://www.cinematuga.net'#'http://www.tugafilmes.org'
        top_5_source = abrir_url(url_top_5)
                
        html_top5 = re.findall("<div class='item-thumbnail'>(.*?)<div style='clear: both;'>", top_5_source, re.DOTALL)
	for item in html_top5:
                percent = int( ( i / 5.0 ) * 100)
                message = str(i) + " de " + '5'
                progress.update( percent, "", message, "" )
                print str(i) + " de " + '5'
                if progress.iscanceled():
                        break
                urletitulo = re.compile("<div class='item-title'><a href='(.+?)'>(.+?)</a></div>").findall(item)
                try:
                        html_source = abrir_url(urletitulo[0][0])
                except: html_source = ''
                items = re.findall("<h3 class='post-title entry-title'(.*?)<span class='post-location'>", html_source, re.DOTALL)
                for item in items:
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
                                #addDir1(nome_original,'','','',False,'')
                        else:
                                titulooriginal = re.compile("<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>(.+?)<br />").findall(item)
                                if titulooriginal:
                                        nome_original = titulooriginal[0]
                                else: nome_original = ''
                                #addDir1(nome_original,'','','',False,'')
                        #urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)
                        qualidade = re.compile("<b>Qualidade</b>: (.+?)<br />").findall(item)
                        if not qualidade: qualidade = re.compile("Ass.+?tir online .+?[(](.+?)[)]").findall(item)
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
                                        
                        nnnn = re.compile('(.+?): ').findall(nome)
                        if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                        if nnnn : nome_pesquisa = nnnn[0]
                        else: nome_pesquisa = nome

                        if imdbcode != '':
                                try:
                                        fanart,tmdb_id,poster,sin = themoviedb_api_IMDB().fanart_and_id(str(imdbcode),ano_filme.replace(' ',''))
                                        if sinopse == '': sinopse = sin
                                        if fanart == '': fanart,tmb,pter = themoviedb_api().fanart_and_id(nome_pesquisa,ano_filme.replace(' ',''))
                                except:pass
                        else:
                                try:
                                        fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano_filme.replace(' ',''))
                                except: pass

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
                                if "Temporada" in urletitulo[0][1]:
                                        num_mode = 712
                                else:
                                        num_mode = 703
                                addDir_trailer('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano_filme.replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',num_mode,thumb.replace('s72-c','s320'),sinopse,fanart,ano_filme.replace(' ',''),genre,nome,urletitulo[0][0])
                        except: pass
                i = i + 1

def CMT_Menu_Filmes_Por_Ano(artfolder):
        i = 0
        url_ano = 'http://www.cinematuga.net'#'http://www.tugafilmes.org'
        html_categorias_source = abrir_url(url_ano)
	html_items_categorias = re.findall("<h2>Anos de La(.*?)<div class=\'clear\'>", html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<option value='(.+?)'>Filmes (\d+)\n</option>").findall(item_categorias)
                if not filmes_por_categoria: filmes_por_categoria = re.compile("<a dir='ltr' href='(.+?)'>Filmes (\d+)</a>").findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        Anos[i] = nome_categoria+'|'+endereco_categoria
                        i = i + 1
        Anos.sort()
        Anos.reverse()
        for x in range(len(Anos)):
                if Anos[x] != '':
                        A = re.compile('(.+?)[|](.*)').findall(Anos[x])
                        if A:
                                addDir('[COLOR yellow]' + A[0][0].replace('  ','').replace(' ','') + '[/COLOR]',A[0][1],702,artfolder + 'CMT1.png','nao','')

def CMT_Menu_Filmes_Por_Categorias(artfolder):
        url_categorias = 'http://www.cinematuga.net'#'http://www.tugafilmes.org'
        html_categorias_source = abrir_url(url_categorias)
	html_items_categorias = re.findall("<h2>Menu Filmes</h2>(.*?)<div class=\'clear\'>", html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<option value='(.+?)'>(.+?)\n</option>").findall(item_categorias)
                if not filmes_por_categoria: filmes_por_categoria = re.compile("<a dir='ltr' href='(.+?)'>(.+?)</a>").findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        addDir('[COLOR yellow]' + nome_categoria + '[/COLOR]',endereco_categoria,702,artfolder + 'CMT1.png','nao','')

def CMT_Menu_Filmes_Por_Qualidade(artfolder):
        url_categorias = 'http://www.cinematuga.net'#'http://www.tugafilmes.org'
        html_categorias_source = abrir_url(url_categorias)
	html_items_categorias = re.findall("<h2>Formatos</h2>(.*?)<div class=\'clear\'>", html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<option value='(.+?)'>(.+?)\n</option>").findall(item_categorias)
                if not filmes_por_categoria: filmes_por_categoria = re.compile("<a dir='ltr' href='(.+?)'>(.+?)</a>").findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        addDir('[COLOR yellow]' + nome_categoria + '[/COLOR]',endereco_categoria,702,artfolder + 'CMT1.png','nao','')

      

#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#


def CMT_encontrar_fontes_filmes(url,artfolder):
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	#items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	items = re.findall("<h3 class='post-title entry-title'(.*?)<span class='post-location'>", html_source, re.DOTALL)
	conta_items = 0
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
                        versao = ''
                        audio_filme = ''
                        imdbcode = ''
                        ano_filme = ''
                        qualidade = ''

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
                                #addDir1(nome_original,'','','',False,'')
                        else:
                                titulooriginal = re.compile("<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>(.+?)<br />").findall(item)
                                if titulooriginal:
                                        nome_original = titulooriginal[0]
                                else: nome_original = ''
                                #addDir1(nome_original,'','','',False,'')
                        ################urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)
                        urletitulo = re.compile("<a href='(.+?)'>(.+?)</a>").findall(item)
                        qualidade = re.compile("<b>Qualidade</b>: (.+?)<br />").findall(item)
                        if not qualidade: qualidade = re.compile("Ass.+?tir online .+?[(](.+?)[)]").findall(item)
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

                                        
                        nnnn = re.compile('(.+?): ').findall(nome)
                        if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                        if nnnn : nome_pesquisa = nnnn[0]
                        else: nome_pesquisa = nome
                        if imdbcode != '':
                                try:
                                        fanart,tmdb_id,poster,sin = themoviedb_api_IMDB().fanart_and_id(str(imdbcode),ano_filme.replace(' ',''))
                                        if sinopse == '': sinopse = sin
                                        if fanart == '': fanart,tmb,pter = themoviedb_api().fanart_and_id(nome_pesquisa,ano_filme.replace(' ',''))
                                except:pass
                        else:
                                try:
                                        fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano_filme.replace(' ',''))
                                except: pass

                        if qualidade: qualidade = qualidade[0].replace('<b>','').replace('</b>','')
                        else: qualidade = ''
                        #else:
##                        lur = urletitulo[0][0]
##                        addLink(str(lur),'','','')
##                        try:
##                                htm = abrir_url(lur)
##                        except: htm = ''
##                        if htm != '':
##                                quq = re.findall("<h3 class='post-title entry-title'(.*?)<span class='post-location'>", htm, re.DOTALL)
##                                if quq != '':
##                                        qualidade = re.compile('<b>Assitir online(.+?)</b>').findall(quq[0])
##                                        if qualidade:
##                                                qualidade = qualidade[0].replace('Legendado','')
##                                                qualidade = qualidade.replace('(','')
##                                                qualidade = qualidade.replace(')','')
##                                                qualidade = qualidade.replace(' ','')
##                                        else: qualidade = ''
                        if genre == '': genre = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        try:
                                if "Temporada" in urletitulo[0][1]:
                                        num_mode = 712
                                else:
                                        num_mode = 703
                                addDir_trailer('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano_filme.replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',num_mode,thumb.replace('s72-c','s320'),sinopse,fanart,ano_filme.replace(' ',''),genre,nome,urletitulo[0][0])
                        except: pass
                        #---------------------------------------------------------------
                        i = i + 1
                        #---------------------------------------------------------------
	else: return
	proxima = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
	if proxima[0] != '':
                try:
                        addDir("[B]Página Seguinte >>[/B]",proxima[0].replace('&amp;','&'),702,artfolder + 'PAGS1.png','','')
                except:pass
        
        
#----------------------------------------------------------------------------------------------------------------------------------------------#	


def CMT_encontrar_videos_filmes(name,url):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]
        if 'CMT' not in name: name = '[COLOR orange]CMT | [/COLOR]' + name
        nomeescolha = name
        conta_id_video = 0
        conta_os_items = 0

        ######################################
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
##        nn = nomeescolha.replace('[B][COLOR green]','--').replace('[/COLOR][/B]','--').replace('[COLOR orange]','').replace('CMT | ','')
##        n = re.compile('--(.+?)--').findall(nn)
##        addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n[0],'url',1004,iconimage,False,fanart)
        ######################################
	#addLink(imdbcode,'','')

	if imdbcode == '' or imdbcode == '---':
                try:
                        link2=abrir_url(url)
                except: link2 = ''
                if imdbcode == '':
                        items = re.findall("<div class='video-item'>(.+?)<div class='clear'>", link2, re.DOTALL)
                        if items != []:
                                imdb = re.compile('imdb.com/title/(.+?)/').findall(items[0])
                                if imdb: imdbcode = imdb[0]
                                else: imdbcode = ''
                        
        if n1 != '' and n2 != '':
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
                addDir('[COLOR yellow]PROCURAR POR: [/COLOR]'+n2,'IMDB'+imdbcode+'IMDB',7,iconimage,'',fanart)
        else:
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
        addDir1(name,'url',1004,iconimage,False,fanart)
        
        try:
                link2=abrir_url(url)
        except: link2 = ''
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
                        CMT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,fanart,iconimage)
                except: pass
##        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(nomeescolha)
##        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
##        nn = nomeescolha.replace('[B][COLOR green]','--').replace('[/COLOR][/B]','--').replace('[COLOR orange]','').replace('CMT | ','')
##        n = re.compile('--(.+?)--').findall(nn)
        url = 'IMDB'+imdbcode+'IMDB'
        FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n1),'CMT',url)


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
                        ##############################################
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
                                               # addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Firedrive)[/COLOR][/B]',url,30,iconimage,'',fanart)
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
                        if "videowood" in url:
                                try:
                                        if '/video/' in url: url = url.replace('/video/','/embed/')
                                        print url
                                        fonte_id = '(VideoWood)'
                                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoWood)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                        if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url and 'nowvideo' not in url:# and 'iiiiiiiiii' in url:
                                Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',iconimage,'',fanart)
                except: pass




#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def CMT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha,fanart,iconimage):
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
                       # addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Cloudzilla)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "divxstage" in url:
                try:
                        fonte_id = '(Divxstage)'
                       # addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Divxstage)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	if "vidzen" in url:
                try:
                        fonte_id = '(Vidzen)'
                       # addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidzen)[/COLOR][/B]',url,30,iconimage,'',fanart)
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
