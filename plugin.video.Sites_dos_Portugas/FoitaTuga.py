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



import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,FilmesAnima

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

Anos = ['' for i in range(100)]

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#



def FTT_MenuPrincipal(artfolder):
        addDir('- Procurar','http://www.tuga-filmes.com/search?q=',1,artfolder + 'P1.png','nao','')
	addDir1('[COLOR blue]Filmes:[/COLOR]','url',1002,artfolder + 'FTT1.png',False,'')
	addDir('[COLOR yellow]- Todos[/COLOR]','http://foitatugacinemaonline.blogspot.pt/',602,artfolder + 'FT.png','nao','')
	addDir('[COLOR yellow]- Animação[/COLOR]','http://foitatugacinemaonline.blogspot.pt/search/label/ANIMA%C3%87%C3%83O',602,artfolder + 'FA.png','nao','')
	addDir('[COLOR yellow]- Categorias[/COLOR]','url',606,artfolder + 'CT.png','nao','')
	addDir('[COLOR yellow]- Por Ano[/COLOR]','url',606,artfolder + 'ANO.png','nao','')
	addDir('[COLOR yellow]- Top 10 + Vistos[/COLOR]','url',608,artfolder + 'T10V.png','nao','')

def FTT_Menu_Filmes_Por_Categorias(artfolder):
        i = 0
        url_categorias = 'http://foitatugacinemaonline.blogspot.pt/'
        html_categorias_source = FTT_abrir_url(url_categorias)
	if name == '[COLOR yellow]- Categorias[/COLOR]':
                html_items_categorias = re.findall("'http://foitatugacinemaonline.blogspot.pt/search/label/2014'>2014(.*?)<div id='searchbarright'>", html_categorias_source, re.DOTALL)
                if not html_items_categorias: html_items_categorias = re.findall("<h2>CATEGORIAS</h2>(.*?)<div class='clear'>", html_categorias_source, re.DOTALL)
                print len(html_items_categorias)
                for item_categorias in html_items_categorias:
                        filmes_por_categoria = re.compile("<option value='(.+?)'>(.+?)\n.+?[(](.+?)[)]\n.+?</option>").findall(item_categorias)
                        if not filmes_por_categoria: filmes_por_categoria = re.compile("<a dir='ltr' href='(.+?)'>(.+?)</a>").findall(item_categorias)
##                        for endereco_categoria,nome_categoria,total_categoria in filmes_por_categoria:
##                                addDir('[COLOR yellow]' + nome_categoria + '[/COLOR] ('+total_categoria+')',endereco_categoria,602,artfolder + 'FTT1.png','nao','')
                        for endereco_categoria,nome_categoria in filmes_por_categoria:
                                addDir('[COLOR yellow]' + nome_categoria + '[/COLOR]',endereco_categoria,602,artfolder + 'FTT1.png','nao','')
	if name == '[COLOR yellow]- Por Ano[/COLOR]':
                html_items_categorias = re.findall("<option>ESCOLHA A CATEGORIA</option>(.*?)='http://foitatugacinemaonline.blogspot.pt/search/label/ANIMA%C3%87%C3%83O'", html_categorias_source, re.DOTALL)
                if not html_items_categorias: html_items_categorias = re.findall("<h2>FILMES POR ANO</h2>(.*?)<div class='clear'>", html_categorias_source, re.DOTALL)
                print len(html_items_categorias)
                for item_categorias in html_items_categorias:
                        filmes_por_categoria = re.compile("<option value='(.+?)'>(.+?)\n.+?[(](.+?)[)]\n.+?</option>").findall(item_categorias)
                        if not filmes_por_categoria: filmes_por_categoria = re.compile("<a dir='ltr' href='(.+?)'>(.+?)</a>").findall(item_categorias)
                        for endereco_categoria,nome_categoria in filmes_por_categoria:
                                Anos[i] = nome_categoria+'|'+endereco_categoria+'|'
                                i = i + 1
##                        for endereco_categoria,nome_categoria,total_categoria in filmes_por_categoria:
##                                Anos[i] = nome_categoria+'|'+endereco_categoria+'|'+total_categoria
##                                i = i + 1
                Anos.sort()
                Anos.reverse()
                for x in range(len(Anos)):
                        if Anos[x] != '':
                                A = re.compile('(.+?)[|](.+?)[|]').findall(Anos[x])
                                if A:
                                        addDir('[COLOR yellow]' + A[0][0] + '[/COLOR]',A[0][1],602,artfolder + 'FTT1.png','nao','')
##                                A = re.compile('(.+?)[|](.+?)[|](.*)').findall(Anos[x])
##                                if A:
##                                        addDir('[COLOR yellow]' + A[0][0] + '[/COLOR] ('+A[0][2]+')',A[0][1],602,artfolder + 'FTT1.png','nao','')


def FTT_Top_Vistos(artfolder):
        progress = xbmcgui.DialogProgress()
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
        url_categorias = 'http://foitatugacinemaonline.blogspot.pt/'
        html_categorias_source = FTT_abrir_url(url_categorias)
        html_items_categorias = re.findall("<div class='widget-content popular-posts'>(.*?)<div class='clear'>", html_categorias_source, re.DOTALL)
        html_items_categorias = re.findall("<div class='item-thumbnail'>(.*?)<div style='clear: both;'>", html_items_categorias[0], re.DOTALL)
        num = len(html_items_categorias) + 0.0
        for item_categorias in html_items_categorias:
                percent = int( ( i / num ) * 100)
                message = str(i) + " de " + str(int(num))
                progress.update( percent, "", message, "" )
                print str(i) + " de " + str(int(num))
                if progress.iscanceled():
                        break
                anofilme = ''
                imdbcode = ''
                fanart = ''

                imdb = re.compile('imdb.com/title/(.+?)/').findall(item_categorias)
                if imdb: imdbcode = imdb[0]
                else: imdbcode = ''
                url_titulo = re.compile("<a href='(.+?)'>(.+?)</a>").findall(item_categorias)
                thumb_f = re.compile("src='(.+?)'").findall(item_categorias)
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
                sinopse = ''
                fanart = ''
                if fanart == '':
                        try:
                                nnnn = re.compile('.+?[(](.+?)[)]').findall(nome_f)
                                if not nnnn: nnnn = re.compile('.+?[[](.+?)[]]').findall(nome_f)
                                if not nnnn: nnnn = re.compile('(.+?) - ').findall(nome_f)
##                                        nomes = '|'+nome.replace(' - ','|')
##                                        nnnn = re.compile('[|](.+?)[|].+?').findall(nomes)
                                if nnnn : nome_pesquisa = nnnn[0]
                                else: nome_pesquisa = nome_f
                                nome_pesquisa = nome_pesquisa.replace('é','e')
                                nome_pesquisa = nome_pesquisa.replace('ê','e')
                                nome_pesquisa = nome_pesquisa.replace('á','a')
                                nome_pesquisa = nome_pesquisa.replace('ã','a')
                                nome_pesquisa = nome_pesquisa.replace('è','e')
                                nome_pesquisa = nome_pesquisa.replace('í','i')
                                nome_pesquisa = nome_pesquisa.replace('ó','o')
                                nome_pesquisa = nome_pesquisa.replace('ô','o')
                                nome_pesquisa = nome_pesquisa.replace('õ','o')
                                nome_pesquisa = nome_pesquisa.replace('ú','u')
                                nome_pesquisa = nome_pesquisa.replace('Ú','U')
                                nome_pesquisa = nome_pesquisa.replace('ç','c')
                                nome_pesquisa = nome_pesquisa.replace('&#189;','½')
                                nome_pesquisa = nome_pesquisa.replace('.',"")
                                a_q = re.compile('\w+')
                                qq_aa = a_q.findall(nome_pesquisa)
                                nome_pesquisa = ''
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) > 1 or q_a_q_a == '1' or q_a_q_a == '2' or q_a_q_a == '3' or q_a_q_a == '4'or q_a_q_a == '5' or q_a_q_a == '6':
                                                nome_pesquisa = nome_pesquisa + '+' + q_a_q_a
                                url_pesquisa = 'http://www.themoviedb.org/search/movie?query=' + nome_pesquisa
                                if fanart == '':
                                        try:
                                                html_pesquisa = FTT_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.compile('<a href="(.+?)" title=".+?"><img class="right_shadow"').findall(html_pesquisa)
                                        if items_pesquisa: url_pesquisa = 'http://www.themoviedb.org' + items_pesquisa[0] + '?language=pt'
                                        try:
                                                html_pesquisa = FTT_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        if 'There are no backdrops added to this movie.' not in html_pesquisa:
                                                url_fan = re.compile('<meta name="twitter:image" content="(.+?)" />').findall(html_pesquisa)
                                                if url_fan: fanart = url_fan[0].replace('w780','w1280')
                                                else: fanart = '---'
                                        else: fanart = '---'
                                        snpse = re.compile('<p id="overview" itemprop="description">(.+?)</p>').findall(html_pesquisa)
                                        if not snpse: snpse = re.compile('<h3>Overview</h3>\n<p>(.+?)</p>').findall(html_pesquisa)
                                        if snpse: sinopse = snpse[0]
                                        else:
                                                if items_pesquisa: url_pesquisa = 'http://www.themoviedb.org' + items_pesquisa[0] + '?language=en'
                                                try:
                                                        html_pesquisa = FTT_abrir_url(url_pesquisa)
                                                except: html_pesquisa = ''
                                                snpse = re.compile('<p id="overview" itemprop="description">(.+?)</p>').findall(html_pesquisa)
                                                if not snpse: snpse = re.compile('<h3>Overview</h3>\n<p>(.+?)</p>').findall(html_pesquisa)
                                                if snpse: sinopse = snpse[0]
                        except: pass
                if sinopse == '': sinopse = '---'
                if fanart == '---': fanart = ''
                if imdbcode == '': imdbcode = '---'
                addDir('[B][COLOR green]' + nome_f + '[/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR]',url_titulo[0][0]+'IMDB'+imdbcode+'IMDB',603,thumb_f[0].replace('s72-c','s320'),sinopse,fanart)
                i = i + 1
        progress.close()                



#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#

		

def FTT_encontrar_fontes_filmes(url):
        progress = xbmcgui.DialogProgress()
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
        try:
		html_source = FTT_abrir_url(url)
	except: html_source = ''
	items = re.findall("<a class='comment-link'(.+?)<div class='post-footer'>", html_source, re.DOTALL)
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

                        urletitulo = re.compile("<a href='(.+?)' title='(.+?)'>").findall(item)
                        if not urletitulo: urletitulo = re.compile("<a href='(.+?)'>(.+?)</a>").findall(item)
                        if urletitulo:
                                urlvideo = urletitulo[0][0]
                                nome = urletitulo[0][1]
                        else:
                                urlvideo = ''
                                nome = ''

                        try:
                                fonte_video = FTT_abrir_url(urlvideo)
                        except: fonte_video = ''
                        fontes_video = re.findall("<div class='post-body entry-content'>(.*?)<div style='clear: both;'>", fonte_video, re.DOTALL)
                        if fontes_video != []:
                                qualid = re.compile('ASSISTIR ONLINE LEGENDADO(.+?)\n').findall(fontes_video[0])
                                if qualid: qualidade_filme = qualid[0].replace('/ ','').replace('</b>','').replace('</span>','')
                                else:
                                        qualid = re.compile('[[]</span><span style=".+?"><span style=".+?">(.+?)</span><span style=".+?">[]]').findall(fontes_video[0])
                                        if qualid: qualidade_filme = qualid[0].replace('/ ','').replace('</b>','').replace('</span>','')

                                
                        snpse = re.compile('Sinopse.png"></a></div>\n(.+?)\n').findall(item)
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

                        if audio_filme != '': qualidade_filme = qualidade_filme + ' - ' + audio_filme

                        nome = nome.replace('((','(')
                        nome = nome.replace('))',')')
                        nome = nome.replace('()','(')
                        nome = nome.replace('  ','')
                        nome = nome.replace(' - []','')
##                        nnn = re.compile('[(](.+?)[)]').findall(nome)
##                        if nnn: nome = nnn[0]
##                        nnn = re.compile('[[](.+?)[]]').findall(nome)
##                        if nnn: nome = nnn[0]

                        #if selfAddon.getSetting('movie-fanart-FTT') == "true" and fanart == '':
                        if fanart == '':
                                nnnn = re.compile('.+?[(](.+?)[)]').findall(nome)
                                if not nnnn: nnnn = re.compile('.+?[[](.+?)[]]').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
##                                        nomes = '|'+nome.replace(' - ','|')
##                                        nnnn = re.compile('[|](.+?)[|].+?').findall(nomes)
                                if nnnn : nome_pesquisa = nnnn[0]
                                else: nome_pesquisa = nome
                                nome_pesquisa = nome_pesquisa.replace('é','e')
                                nome_pesquisa = nome_pesquisa.replace('ê','e')
                                nome_pesquisa = nome_pesquisa.replace('á','a')
                                nome_pesquisa = nome_pesquisa.replace('ã','a')
                                nome_pesquisa = nome_pesquisa.replace('è','e')
                                nome_pesquisa = nome_pesquisa.replace('í','i')
                                nome_pesquisa = nome_pesquisa.replace('ó','o')
                                nome_pesquisa = nome_pesquisa.replace('ô','o')
                                nome_pesquisa = nome_pesquisa.replace('õ','o')
                                nome_pesquisa = nome_pesquisa.replace('ú','u')
                                nome_pesquisa = nome_pesquisa.replace('Ú','U')
                                nome_pesquisa = nome_pesquisa.replace('ç','c')
                                nome_pesquisa = nome_pesquisa.replace('&#189;','½')
                                a_q = re.compile('\w+')
                                qq_aa = a_q.findall(nome_pesquisa)
                                nome_pesquisa = ''
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) > 1 or q_a_q_a == '1' or q_a_q_a == '2' or q_a_q_a == '3' or q_a_q_a == '4'or q_a_q_a == '5' or q_a_q_a == '6':
                                                nome_pesquisa = nome_pesquisa + '+' + q_a_q_a
                                url_pesquisa = 'http://www.themoviedb.org/search/movie?query=' + nome_pesquisa
                                if thumb == '':
                                        try:
                                                html_pesquisa = FTT_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail: thumb = thumbnail[0].replace('w92','w600')
                                #if selfAddon.getSetting('series-fanart-FTT') == "true":
                                if fanart == '':
                                        try:
                                                html_pesquisa = FTT_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.compile('<a href="(.+?)" title=".+?"><img class="right_shadow"').findall(html_pesquisa)
                                        if items_pesquisa: url_pesquisa = 'http://www.themoviedb.org' + items_pesquisa[0]
                                        try:
                                                html_pesquisa = FTT_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        if 'There are no backdrops added to this movie.' not in html_pesquisa:
                                                url_fan = re.compile('<meta name="twitter:image" content="(.+?)" />').findall(html_pesquisa)
                                                if url_fan: fanart = url_fan[0].replace('w780','w1280').replace('w500','w1280')
                                                else: fanart = '---'
                                        else: fanart = '---'

                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        try:
                                addDir_teste('[B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',urlvideo+'IMDB'+imdbcode+'IMDB',603,thumb,sinopse,fanart,anofilme,genero)
                        except: pass
                        #---------------------------------------------------------------
                        i = i + 1
                        #---------------------------------------------------------------
	proxima = re.compile("<a class='blog-pager-older-link' href='(.+?)' id='Blog1_blog-pager-older-link'").findall(html_source)	
	try:
                proxima_p = proxima[0]#.replace('%3A',':').replace('%2B','+')
		addDir("[B]Página Seguinte >>[/B]",proxima_p.replace('&amp;','&'),602,artfolder + 'PAGS1.png','','')
	except: pass



#----------------------------------------------------------------------------------------------------------------------------------------------#

def FTT_encontrar_videos_filmes(name,url):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]
        if 'FTT' not in name: name = '[COLOR orange]FTT | [/COLOR]' + name
        nomeescolha = name
        colecao = 'nao'
        ################################################
        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(nomeescolha)
        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
        nn = nomeescolha.replace('[B][COLOR green]','--').replace('[COLOR orange]','').replace('[/COLOR][/B]','--').replace('[/COLOR]','').replace('[','---').replace(']','---')
        nn = nn.replace('(','---').replace(')','---').replace('FTT | ','')
        if '---' in nn:
                n = re.compile('---(.+?)---').findall(nn)
                n1 = re.compile('--(.+?)--').findall(nn)
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1[0],'url',1004,iconimage,False,fanart)
                addDir('[COLOR yellow]PROCURAR POR: [/COLOR]'+n[0],'IMDB'+imdbcode+'IMDB',7,iconimage,'',fanart)
                nome_pesquisa = n1[0]
        else:
                n1 = re.compile('--(.+?)--').findall(nn)
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1[0],'url',1004,iconimage,False,fanart)
                nome_pesquisa = n1[0]
        ################################################
        if imdbcode == '' or imdbcode == '---':
                conta = 0
                #nome_pesquisa = n[0]
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
                html_imdbcode = FTT_abrir_url(url_imdb)
                filmes_imdb = re.findall('<div class="findSection">(.*?)<div class="findMoreMatches">', html_imdbcode, re.DOTALL)
                imdbc = re.compile('/title/(.+?)/[?]ref').findall(filmes_imdb[0])
                imdbcode = imdbc[0]
            
        addDir1(name,'url',1002,iconimage,False,fanart)
        conta_id_video = 0
        try:
                fonte_video = FTT_abrir_url(url)
        except: fonte_video = ''
        fontes_video = re.findall("<div class='post-body entry-content'>(.*?)<div style='clear: both;'>", fonte_video, re.DOTALL)
        numero_de_fontes = len(fontes_video)
        if 'BREVEMENTE ONLINE' in fonte_video: addDir1('[COLOR blue]BREVEMENTE ONLINE[/COLOR]','url',1004,artfolder,False,'')
        for fonte_e_url in fontes_video:
                if imdbcode == '':
                        imdb = re.compile('imdb.com/title/(.+?)/').findall(fonte_e_url)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                #if 'BREVEMENTE ONLINE' in fontes_video: addDir1('[COLOR blue]BREVEMENTE ONLINE[/COLOR]','url',1004,artfolder,False,'')
                match1 = re.compile('<script src="(.+?)" type="text/javascript"></script>').findall(fonte_e_url)
                for fonte_id in match1: 
                        if 'videomega' in fonte_id:
                                try:  
                                        if 'hashkey' in fonte_id:
                                                conta_id_video = conta_id_video + 1
                                                try:
                                                        urlvideomega = FTT_abrir_url(fonte_id)
                                                except: urlvideomega = ''
                                                if urlvideomega != '':
                                                        urlvidlink = re.compile('ref="(.+?)"').findall(urlvideomega)
                                                        if urlvidlink: url = 'http://videomega.tv/iframe.php?ref=' + urlvidlink[0] + '///' + name
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                        if 'iframe.js' in fonte_id:
                                                conta_id_video = conta_id_video + 1
                                                refvideo = re.compile('<script type="text/javascript">ref="(.+?)".+?</script>').findall(fonte_e_url)
                                                if not refvideo: refvideo = re.compile(">ref='(.+?)'.+?</script>").findall(fonte_e_url)
                                                url = 'http://videomega.tv/iframe.php?ref=' + refvideo[0] + '///' + name
                                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                match2 = re.compile('<iframe.+?src="(.+?)" .+?</iframe>').findall(fonte_e_url)
                for fonte_id in match2:
                        if 'videomega' in fonte_id:
                                try:
                                        conta_id_video = conta_id_video + 1
                                        url = fonte_id + '///' + name
                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                        elif 'dropvideo' in fonte_id:
                                try:
                                        conta_id_video = conta_id_video + 1
                                        url = fonte_id + '///' + name
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
        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(nomeescolha)
        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
        nn = nomeescolha.replace('[B][COLOR green]','--').replace('[COLOR orange]','').replace('[/COLOR][/B]','--').replace('[/COLOR]','').replace('[','---').replace(']','---')
        nn = nn.replace('(','---').replace(')','---').replace('FTT | ','')
        if '---' in nn:
                n = re.compile('---(.+?)---').findall(nn)
                n1 = re.compile('--(.+?)--').findall(nn)
                url = 'IMDB'+imdbcode+'IMDB'
                FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n[0]),'FTT',url)
        else:
                n1 = re.compile('--(.+?)--').findall(nn)
                url = 'IMDB'+imdbcode+'IMDB'
                FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n1[0]),'FTT',url)



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
                fonte_video = FTT_abrir_url(url)
        except: fonte_video = ''
        fontes_video = re.findall("<div class='post-body entry-content'>(.*?)<div style='clear: both;'>", fonte_video, re.DOTALL)
        numero_de_fontes = len(fontes_video)
        if 'BREVEMENTE ONLINE' in fonte_video: addDir1('[COLOR blue]BREVEMENTE ONLINE[/COLOR]','url',1004,artfolder,False,'')
        for fonte_e_url in fontes_video:
                if imdbcode == '':
                        imdb = re.compile('imdb.com/title/(.+?)/').findall(fonte_e_url)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                #if 'BREVEMENTE ONLINE' in fontes_video: addDir1('[COLOR blue]BREVEMENTE ONLINE[/COLOR]','url',1004,artfolder,False,'')
                match1 = re.compile('<script src="(.+?)" type="text/javascript"></script>').findall(fonte_e_url)
                for fonte_id in match1: 
                        if 'videomega' in fonte_id:
                                try:  
                                        if 'hashkey' in fonte_id:
                                                conta_id_video = conta_id_video + 1
                                                try:
                                                        urlvideomega = FTT_abrir_url(fonte_id)
                                                except: urlvideomega = ''
                                                if urlvideomega != '':
                                                        urlvidlink = re.compile('ref="(.+?)"').findall(urlvideomega)
                                                        if urlvidlink: url = 'http://videomega.tv/iframe.php?ref=' + urlvidlink[0] + '///' + name
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                        if 'iframe.js' in fonte_id:
                                                conta_id_video = conta_id_video + 1
                                                refvideo = re.compile('<script type="text/javascript">ref="(.+?)".+?</script>').findall(fonte_e_url)
                                                if not refvideo: refvideo = re.compile(">ref='(.+?)'.+?</script>").findall(fonte_e_url)
                                                url = 'http://videomega.tv/iframe.php?ref=' + refvideo[0] + '///' + name
                                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                match2 = re.compile('<iframe.+?src="(.+?)".+?></iframe>').findall(fonte_e_url)
                for fonte_id in match2:
                        if 'videomega' in fonte_id:
                                try:
                                        conta_id_video = conta_id_video + 1
                                        url = fonte_id + '///' + name
                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                except:pass
                        elif 'dropvideo' in fonte_id:
                                try:
                                        conta_id_video = conta_id_video + 1
                                        url = fonte_id + '///' + name
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
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
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
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(VideoWood)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoWood)[/COLOR][/B]',url,30,iconimage,'',fanart)
    		except:pass
    	return



#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#


	
def FTT_abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

#----------------------------------------------------------------------------------------------------------------------------------------------#
              
def FTT_get_params():
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
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&checker="+urllib.quote_plus(checker)+"&fanart="+urllib.quote_plus(fanart)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',fanart)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
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


          
params=FTT_get_params()
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


