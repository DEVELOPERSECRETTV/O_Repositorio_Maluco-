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
from Mashup import thetvdb_api,themoviedb_api,themoviedb_api_tv,themoviedb_api_search_imdbcode

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'


#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#



def CMC_MenuPrincipal(artfolder):
        addDir('- Procurar','http://www.tuga-filmes.com/search?q=',1,artfolder + 'P1.png','nao','')
	addDir1('[COLOR blue]Filmes:[/COLOR]','url',1002,artfolder + 'CMC1.png',False,'')
	#addDir('[COLOR yellow]- Todos[/COLOR]','http://movie-tuga.blogspot.pt/',102,artfolder + 'FT.png','nao','')
	addDir('[COLOR yellow]- Animação[/COLOR]','http://www.cinemaemcasa.pt/search/label/Anima%C3%A7%C3%A3o',902,artfolder + 'FA.png','nao','')
	addDir('[COLOR yellow]- Categorias[/COLOR]','url',906,artfolder + 'CT.png','nao','')
	

def CMC_Menu_Filmes_Por_Categorias(artfolder):
        url_categorias = 'http://www.cinemaemcasa.pt/'
        html_categorias_source = CMC_abrir_url(url_categorias)
	html_items_categorias = re.findall("<div class='widget-content list-label-widget-content'>(.*?)<div class='clear'></div>", html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<a dir='ltr' href='(.+?)'>\n(.+?)\n</a>").findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        addDir('[COLOR yellow]' + nome_categoria + '[/COLOR]',endereco_categoria + '?&max-results=15',902,artfolder + 'CMC1.png','nao','')



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
		html_source = CMC_abrir_url(url)
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
                                        
                        
##                        nnnn = re.compile('.+?[(](.+?)[)]').findall(nome)
##                        if not nnnn: nnnn = re.compile('.+?[[](.+?)[]]').findall(nome)
##                        if not nnnn: nnnn = re.compile('(.+?)[:]').findall(nome)
##                        if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
##                        if nnnn : nome_pesquisa = nnnn[0]
##                        else: nome_pesquisa = nome
                        nome_pesquisa = nome
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

                        try:                                                                                                                                                                                                      #903                                              
                                addDir_teste('[B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',urlfilme.replace(' ','%20')+'IMDB'+imdbcode+'IMDB','',thumb.replace(' ','%20'),sinopse,fanart,ano_filme,genero) 
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

def CMC_encontrar_videos_filmes(name,url):
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
                html_imdbcode = CMC_abrir_url(url_imdb)
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
                fonte_video = CMC_abrir_url(url)
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
                                        fonte = CMC_abrir_url(url_video)
                                except: fonte = ''
                                fontes = re.findall("<body>(.+?)</body>", fonte, re.DOTALL)
                                for fonte_id in fontes:
                                        if 'videomega' in fonte_id:
                                                try:
                                                        match = re.compile("<script type=\'text/javascript\'>ref=\'(.+?)\'").findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        id_video = match[0]
                                                        url = 'http://videomega.tv/iframe.php?ref=' + id_video + '///' + name
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if 'vidto' in fonte_id:
                                                try:
                                                        match = re.compile('<iframe .+? src=".+?//vidto.me/embed-(.+?)" .+?</iframe>').findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        if match: match = re.compile('(.+?)-').findall(match[0])
                                                        id_video = match[0]
                                                        url = 'http://vidto.me/' + id_video + '.html' + '///' + name
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'',fanart)
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
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
                                        if 'vidto' in fonte_id:
                                                try:
                                                        match = re.compile('<iframe .+? src=".+?//vidto.me/embed-(.+?)" .+?</iframe>').findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        if match: match = re.compile('(.+?)-').findall(match[0])
                                                        id_video = match[0]
                                                        url = 'http://vidto.me/' + id_video + '.html' + '///' + name
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'',fanart)
                                                except:pass
##        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(nomeescolha)
##        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
##        nn = nomeescolha.replace('[B][COLOR green]','--').replace('[/COLOR][/B]','--').replace('[COLOR orange]','').replace('CMC | ','')
##        n = re.compile('--(.+?)--').findall(nn)
##        url = 'IMDB'+imdbcode+'IMDB'
##        FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n[0]),'CMC',url)
        #addLink(imdbcode,'','')
        url = 'IMDB'+imdbcode+'IMDB'
        FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n1),'CMC',url)


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
        try:
                fonte_video = CMC_abrir_url(url)
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
                                        fonte = CMC_abrir_url(url_video)
                                except: fonte = ''
                                fontes = re.findall("<body>(.+?)</body>", fonte, re.DOTALL)
                                for fonte_id in fontes:
                                        if 'videomega' in fonte_id:
                                                try:
                                                        match = re.compile("<script type=\'text/javascript\'>ref=\'(.+?)\'").findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        id_video = match[0]
                                                        url = 'http://videomega.tv/iframe.php?ref=' + id_video + '///' + name
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,100,iconimage,'',fanart)
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
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,100,iconimage,'',fanart)
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


	
def CMC_abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

#----------------------------------------------------------------------------------------------------------------------------------------------#
              
def CMC_get_params():
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
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&checker="+urllib.quote_plus(checker)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
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
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&year="+urllib.quote_plus(year)+"&genre="+urllib.quote_plus(genre)+"&iconimage="+urllib.quote_plus(iconimage)
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


          
params=CMC_get_params()
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


