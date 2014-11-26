#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2014 OMaluco
#
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


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket
import Play,Pesquisar,Mashup,TugaFilmesTV,TopPt,MovieTuga,Armagedom,FilmesAnima
from Mashup import thetvdb_api,themoviedb_api,themoviedb_api_tv

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

progress = xbmcgui.DialogProgress()

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#

def TFC_MenuPrincipal(artfolder):
        addDir('- Procurar','http://www.tuga-filmes.info/search?q=',1,artfolder + 'P1.png','nao','')
	addDir1('[COLOR blue]Filmes:[/COLOR]','url',1003,artfolder + 'TFC1.png',False,'')
	addDir('[COLOR yellow]- Todos[/COLOR]','http://www.tuga-filmes.info/',72,artfolder + 'FT.png','nao','')
	addDir('[COLOR yellow]- Animação[/COLOR]','http://www.tuga-filmes.info/search/label/Anima%C3%A7%C3%A3o?max-results=20',72,artfolder + 'FA.png','nao','')
	addDir('[COLOR yellow]- Categorias[/COLOR]','url',78,artfolder + 'CT.png','nao','')
	addDir('[COLOR yellow]- Por Ano[/COLOR]','http://www.tuga-filmes.info/search/label/-%20Filmes%202013',90,artfolder + 'ANO.png','nao','')
	addDir('[COLOR yellow]- Destaques[/COLOR]','http://www.tuga-filmes.info/search/label/destaque',72,artfolder + 'DTS.png','nao','')
        addDir('[COLOR yellow]- Top Filmes[/COLOR]','url',79,artfolder + 'TPF.png','nao','')
	#if selfAddon.getSetting('hide-porno') == "false":
                #addDir('[B][COLOR red]M+18[/B][/COLOR]','url',86,artfolder + 'TFC1.png','nao','')	

def TFC_Menu_Filmes_Top_10(artfolder):
        progress = xbmcgui.DialogProgress()
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
        url_top_10 = 'http://www.tuga-filmes.info/'
        top_10_source = TFC_abrir_url(url_top_10)
        filmes_top_10 = re.compile("<img alt=\'\' border=\'0\' height=\'72\' src=\'.+?\' width=\'72\'/>\n</a>\n</div>\n<div class=\'item-title\'><a href=\'(.+?)\'>.+?</a></div>\n</div>\n<div style=\'clear: both;\'>").findall(top_10_source)
        num = len(filmes_top_10) + 0.0
	for endereco_top_10 in filmes_top_10:
                percent = int( ( i / num ) * 100)
                message = str(i) + " de " + str(int(num))
                progress.update( percent, "", message, "" )
                print str(i) + " de " + str(int(num))
                if progress.iscanceled():
                        break
                try:
                        html_source = TFC_abrir_url(endereco_top_10)
                except: html_source = ''
                items = re.findall("<div id='title1'>(.*?)<div class='postmeta'>", html_source, re.DOTALL)
                #addLink(str(len(items)),'','')
                #return
                if items != []:
                        for item in items:
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
                                urletitulo = re.compile("<a href='(.+?)'>(.+?)</a>").findall(item)
                                qualidade_ano = re.compile('<b>VERS\xc3\x83O:.+?</b><span style="font-size: x-small;">(.+?)<').findall(item)
                                snpse = re.compile('<b>SINOPSE:.+?</b><span style="font-size: x-small;">(.+?)<').findall(item)
                                if snpse: sinopse = snpse[0]
                                else: sinopse = ''
                                thumbnail = re.compile('<img alt="" border="0" src="(.+?)"').findall(item)
                                if thumbnail: thumb = thumbnail[0]
                                print urletitulo,thumbnail
                                ano = ''
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
                                                
                                nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                                #if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                                #if not nnnn: nnnn = re.compile('(.+?)[:] ').findall(nome)
                                if nnnn: nome_pesquisa = nnnn[0]
                                else: nome_pesquisa = nome
                                fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano)
                                if thumb == '': thumb = poster

                                if genero == '': genero = '---'
                                if sinopse == '': sinopse = '---'
                                if fanart == '---': fanart = ''
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
                                if qualidade == '': qualidade = '---'
                                try:
                                        if 'ASSISTIR O FILME' in item: addDir_teste('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR][COLOR red] (' + qualidade + ')[/COLOR]' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',73,thumb.replace('s1600','s320').replace('.gif','.jpg'),sinopse,fanart,ano,qualidade)
                                except: pass
                #---------------------------------------------------------------
                i = i + 1
                #---------------------------------------------------------------
	progress.close()

def TFC_Menu_Filmes_Por_Categorias(artfolder):
        url_categorias = 'http://www.tuga-filmes.info/'
        html_categorias_source = TFC_abrir_url(url_categorias)
	html_items_categorias = re.findall("<div id=\'nav-cat\'>(.*?)</div>", html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<a href=\'/(.+?)\'>(.+?)</a>").findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        categoria_endereco = url_categorias + endereco_categoria
                        addDir('[COLOR yellow]' + nome_categoria + '[/COLOR]',categoria_endereco,72,artfolder + 'TFC1.png','nao','')

def TFC_Menu_Filmes_Por_Ano(artfolder):
        ano = 2014
        for x in range(46):
                categoria_endereco = 'http://www.tuga-filmes.info/search/label/-%20Filmes%20' + str(ano)
                addDir('[COLOR yellow]' + str(ano) + '[/COLOR]',categoria_endereco,72,artfolder + 'TFC1.png','nao','')
                ano = ano - 1
        


#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#

		

def TFC_encontrar_fontes_filmes(url):
        pt_en = 0
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
	try:
		html_source = TFC_abrir_url(url)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		num = len(items) + 0.0
		for item in items:
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(len(items))
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(len(items))
                        #if selfAddon.getSetting('movie-fanart-TFC') == "false": xbmc.sleep( 50 )
                        if progress.iscanceled():
                                break
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
                        nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                        #if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                        #if not nnnn: nnnn = re.compile('(.+?)[:] ').findall(nome)
                        if nnnn: nome_pesquisa = nnnn[0]
                        else: nome_pesquisa = nome
                        fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano)
                        if thumb == '': thumb = poster

                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        if qualidade == '': qualidade = '---'
			try:
				if 'ASSISTIR O FILME' in item: addDir_teste('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR][COLOR red] (' + qualidade + ')[/COLOR]' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',73,thumb.replace('s1600','s320').replace('.gif','.jpg'),sinopse,fanart,ano,qualidade)
			except: pass
			#---------------------------------------------------------------
                        i = i + 1
                        #---------------------------------------------------------------
	else:
		items = re.compile("<a href=\'(.+?)\' title=.+?>Assistir Online - </div>(.+?)<div id=\'player\'>").findall(html_source)
		for endereco,nome in items:
			addDir(nome.replace('&#8217;',"'"),endereco,73,'','','')
	proxima = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
	try:
		addDir("[B]Página Seguinte >>[/B]",proxima[0].replace('&amp;','&'),72,artfolder + 'PAGS1.png','','')
	except: pass

#----------------------------------------------------------------------------------------------------------------------------------------------#
	
def TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart):
        if 'videomega' in url: vidv = url
        url = url + '///' + name
        if "videomega" in url:
		try:
                        if 'hashkey' in url:
                                try:
                                        urlvideomega = TFC_abrir_url(vidv)
                                except: urlvideomega = ''
                                if urlvideomega != '':
                                        urlvidlink = re.compile('ref="(.+?)"').findall(urlvideomega)
                                        if urlvidlink: url = 'http://videomega.tv/iframe.php?ref=' + urlvidlink[0] + '///' + name
                        fonte_id = '(Videomega)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
        if "vidto.me" in url:
		try:
                        print url
                        fonte_id = '(Vidto.me)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,70,iconimage,'',fanart)
		except: pass
        if "dropvideo" in url:
		try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        fonte_id = '(DropVideo)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B]',url,70,iconimage,'',fanart)
		except:pass
	if "streamin.to" in url:
                try:
			print url
			fonte_id = '(Streamin)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B]',url,70,iconimage,'',fanart)
                except:pass                        
        if "putlocker" in url:
                try:
                        print url
                        fonte_id = '(Putlocker)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Putlocker)[/COLOR][/B]',url,70,iconimage,'',fanart)
    		except:pass
    	if "nowvideo" in url:
                try:
                        print url
                        fonte_id = '(Nowvideo)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,70,iconimage,'',fanart)
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(VideoWood)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoWood)[/COLOR][/B]',url,70,iconimage,'',fanart)
    		except:pass
    	return

#----------------------------------------------------------------------------------------------------------------------------------------------#

def TFC_encontrar_videos_filmes(name,url):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]
        if 'TFC' not in name: name = '[COLOR orange]TFC | [/COLOR]' + name
        nomeescolha = name
        conta_os_items = 0
        conta_os_items = conta_os_items + 1
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
##        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(nomeescolha)
##        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
##        nn = nomeescolha.replace('[B][COLOR green]','--').replace('[/COLOR][/B]','--').replace('[COLOR orange]','').replace('TFC | ','')
##        n = re.compile('--(.+?)--').findall(nn)
##        addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n[0],'url',1004,iconimage,False,fanart)
        ############################################

        if imdbcode == '' or '---' in imdbcode:
                conta = 0
                ano_pp = re.compile('[[]COLOR yellow[]](.+?)[[]/COLOR[]]').findall(name)
                if ano_pp: ano_pesquisa = ano_pp[0].replace('(','').replace(')','')
                else: ano_pesquisa = ''
                conta = 0
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
                html_imdbcode = TFC_abrir_url(url_imdb)
                filmes_imdb = re.findall('<div class="findSection">(.*?)<div class="findMoreMatches">', html_imdbcode, re.DOTALL)
                imdbc = re.compile('/title/(.+?)/[?]ref').findall(filmes_imdb[0])
                imdbcode = imdbc[0]

        if n1 != '' and n2 != '':
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
                addDir('[COLOR yellow]PROCURAR POR: [/COLOR]'+n2,'IMDB'+imdbcode+'IMDB',7,iconimage,'',fanart)
        else:
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
        
        conta_id_video = 0
	addDir1(name,'url',1003,iconimage,False,fanart)
        try:
                fonte = TFC_abrir_url(url)
        except: fonte = ''
        items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", fonte, re.DOTALL)
	if items != []:
                imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                if imdb: imdbcode = imdb[0]
                else: imdbcode = ''
        assist = re.findall(">ASSISTIR.+?", fonte, re.DOTALL)
        fontes = re.findall("Ver Aqui.+?", fonte, re.DOTALL)
        numero_de_fontes = len(fontes)
	if fonte:
                if len(assist) > 1:
                        #addDir1('1','url',1003,artfolder,False,'')
                        assistir_fontes = re.findall('>ASSISTIR(.*?)------------------------------', fonte, re.DOTALL)
                        if assistir_fontes:
                                for ass_fon in assistir_fontes:
                                        match = re.compile('<iframe .+? src="(.+?)"').findall(ass_fon)
                                        assis = re.compile('ONLINE(.+?)</span>').findall(ass_fon)
                                        conta_video = len(match)
                                        if assis:
                                                if 'LEGENDADO' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,fanart)
                                                if 'PT/PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                                elif 'PT-PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
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
                                                        addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,fanart)
                                                if 'PT/PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                                elif 'PT-PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
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
                                                        addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,fanart)
                                                if 'PT/PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                                elif 'PT-PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
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
                        match = re.compile('<a href="(.+?)" target="_blank">.+?[(]Online').findall(fonte)
                        for url in match:                                
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
##        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(nomeescolha)
##        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
##        nn = nomeescolha.replace('[B][COLOR green]','--').replace('[/COLOR][/B]','--').replace('[COLOR orange]','').replace('TFC | ','')
##        n = re.compile('--(.+?)--').findall(nn)
        url = 'IMDB'+imdbcode+'IMDB'
        #addLink(url+'-'+str(n[0]),'','')
        FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n1),'TFC',url)


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
                fonte = TFC_abrir_url(url)
        except: fonte = ''
        items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", fonte, re.DOTALL)
	if items != []:
                imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                if imdb: imdbcode = imdb[0]
                else: imdbcode = ''
        assist = re.findall(">ASSISTIR.+?", fonte, re.DOTALL)
        fontes = re.findall("Ver Aqui.+?", fonte, re.DOTALL)
        numero_de_fontes = len(fontes)
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
                                                        addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,fanart)
                                                if 'PT/PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                                elif 'PT-PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
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
                                                        addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,fanart)
                                                if 'PT/PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                                elif 'PT-PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
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
                                                        addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,fanart)
                                                if 'PT/PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                                elif 'PT-PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
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
                        match = re.compile('<a href="(.+?)" target="_blank">.+?[(]Online').findall(fonte)
                        for url in match:                                
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



#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

	
def TFC_abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

#----------------------------------------------------------------------------------------------------------------------------------------------#
              
def TFC_get_params():
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

def addLink2(name,url,iconimage,checker):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&checker="+urllib.quote_plus(checker)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'FAN3.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,plot,fanart):
        if fanart == '': fanart = artfolder + 'FAN3.jpg'#iconimage
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&plot="+urllib.quote_plus(plot)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',fanart)#artfolder + 'FAN3.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir1(name,url,mode,iconimage,folder,fanart):
        if fanart == '': fanart = artfolder + 'FAN3.jpg'#iconimage
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',fanart)#artfolder + 'FAN3.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
        return ok

def addDir_teste(name,url,mode,iconimage,plot,fanart,year,genre):
        if fanart == '': fanart = artfolder + 'FAN3.jpg'
        #text = checker
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&plot="+urllib.quote_plus(plot)+"&year="+urllib.quote_plus(year)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)+"&iconimage="+urllib.quote_plus(iconimage)
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
#----------------------------------------------------------------------------------------------------------------------------------------------#


          
params=TFC_get_params()
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
print "Fanart: "+str(fanart)
