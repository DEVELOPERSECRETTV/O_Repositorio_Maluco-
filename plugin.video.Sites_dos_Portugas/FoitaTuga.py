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



import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'


#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#



def FTT_MenuPrincipal(artfolder):
        addDir1('[B][COLOR green]FOIT[/COLOR][COLOR yellow]A[/COLOR][COLOR red]TUGA[/COLOR][/B]','url',1002,'',False,'')
        addDir1('','url',1002,artfolder,False,'')
        addDir('- Pesquisar','http://www.tuga-filmes.com/search?q=',1,artfolder + 'Ze-pesquisar2.png','nao','')
	addDir1('[COLOR blue]Filmes:[/COLOR]','url',1002,'',False,'')
	addDir('[COLOR yellow]- Todos[/COLOR]','http://foitatugacinemaonline.blogspot.pt/',602,'','nao','')
	addDir('[COLOR yellow]- Animação[/COLOR]','http://foitatugacinemaonline.blogspot.pt/search/label/ANIMA%C3%87%C3%83O',602,'','nao','')
	addDir('[COLOR yellow]- Categorias[/COLOR]','url',606,'','nao','')
	addDir('[COLOR yellow]- Por Ano[/COLOR]','url',606,'','nao','')
	addDir('[COLOR yellow]- Top + Vistos[/COLOR]','url',608,'','nao','')

def ANTIGA_FTT_Menu_Filmes_Por_Categorias(artfolder):
        url_categorias = 'http://foitatugacinemaonline.blogspot.pt/'
        html_categorias_source = FTT_abrir_url(url_categorias)
        addDir1('[B][COLOR blue]Categorias[/COLOR][/B]','url',1002,'',False,'')
        addDir1('','url',1002,artfolder,False,'')
	if name == '[COLOR yellow]- Categorias[/COLOR]': html_items_categorias = re.findall("CATEGORIAS(.*?)FILMES POR ANO", html_categorias_source, re.DOTALL)
	if name == '[COLOR yellow]- Por Ano[/COLOR]': html_items_categorias = re.findall("FILMES POR ANO(.*?)<!-- end .menu -->", html_categorias_source, re.DOTALL)
	html_items_categorias = re.findall("<li>(.*?)</li>", html_items_categorias[0], re.DOTALL)
	#addDir1(str(len(html_items_categorias)),'url',1002,artfolder,False,'')
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<a class='trigger' href='(.+?)'>\n(.+?)\n").findall(item_categorias)
                #addDir1(str(len(filmes_por_categoria)),'url',1002,artfolder,False,'')
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        addDir('[COLOR yellow]' + nome_categoria.replace(' ','') + '[/COLOR]',endereco_categoria,602,'','nao','')

def FTT_Menu_Filmes_Por_Categorias(artfolder):
        url_categorias = 'http://foitatugacinemaonline.blogspot.pt/'
        html_categorias_source = FTT_abrir_url(url_categorias)
	if name == '[COLOR yellow]- Categorias[/COLOR]': html_items_categorias = re.findall("'http://foitatugacinemaonline.blogspot.pt/search/label/2014'>2014(.*?)<div id='searchbarright'>", html_categorias_source, re.DOTALL)
	if name == '[COLOR yellow]- Por Ano[/COLOR]': html_items_categorias = re.findall("<option>ESCOLHA A CATEGORIA</option>(.*?)='http://foitatugacinemaonline.blogspot.pt/search/label/ANIMA%C3%87%C3%83O'", html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        #addDir1(str(len(html_items_categorias)),'url',1002,artfolder,False,'')
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<option value='(.+?)'>(.+?)\n.+?[(](.+?)[)]\n.+?</option>").findall(item_categorias)
                #addDir1(str(len(filmes_por_categoria)),'url',1002,artfolder,False,'')
                for endereco_categoria,nome_categoria,total_categoria in filmes_por_categoria:
                        addDir('[COLOR yellow]' + nome_categoria + '[/COLOR] ('+total_categoria+')',endereco_categoria,602,'','nao','')


def FTT_Top_Vistos(artfolder):
        url_categorias = 'http://foitatugacinemaonline.blogspot.pt/'
        html_categorias_source = FTT_abrir_url(url_categorias)
        html_items_categorias = re.findall("<div class='widget-content popular-posts'>(.*?)<div class='clear'>", html_categorias_source, re.DOTALL)
        html_items_categorias = re.findall("<div class='item-thumbnail-only'>(.*?)<div style='clear: both;'>", html_items_categorias[0], re.DOTALL)
        print len(html_items_categorias)
        #addDir1(str(len(html_items_categorias)),'url',1002,artfolder,False,'')
        for item_categorias in html_items_categorias:
                url_titulo = re.compile("<a href='(.+?)'>(.+?)</a>").findall(item_categorias)
                thumb_f = re.compile("src='(.+?)'").findall(item_categorias)
                nome_f = url_titulo[0][1]
                nome_f = nome_f.replace('&#8217;',"'")
                nome_f = nome_f.replace('&#8211;',"-")
                nome_f = nome_f.replace('&#39;',"'")
                nome_f = nome_f.replace('&amp;','&')
                nome_f = nome_f.replace('(Pedido)',"")
                addDir('[COLOR yellow]' + nome_f + '[/COLOR]',url_titulo[0][0],603,thumb_f[0].replace('s72-c','s320'),'nao','')



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
	items = re.findall("<div class='post hentry'>(.+?)<div class='post-outer'>", html_source, re.DOTALL)
	#addDir1(str(len(items)),'url',1002,artfolder,False,'')
	if items != []:
		print len(items)
		num = len(items) + 0.0
		for item in items:
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(len(items))
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(len(items))
                        if selfAddon.getSetting('movie-fanart-MVT') == "false": xbmc.sleep( 50 )
                        if progress.iscanceled():
                                break
                        
                        thumb = ''
                        fanart = ''
                        anofilme= ''
                        qualidade_filme = ''

                        urletitulo = re.compile("<a href='(.+?)'>(.+?)</a>").findall(item)
                        if urletitulo:
                                urlvideo = urletitulo[0][0]
                                nome = urletitulo[0][1]
                        else:
                                urlvideo = ''
                                nome = ''
                                
                        ano = re.compile('<strong>Lan\xc3\xa7amento:</strong>(.+?)</div>').findall(item)
                        if ano: anofilme = ano[0]
                        else: anofilme = ''
                        
                        #thumbnail = re.compile('<a href="(.+?)" imageanchor="1"').findall(item)
                        thumbnail = re.compile('document.write[(]bp_thumbnail_resize[(]"(.+?)",".+?"[)]').findall(item)
                        if thumbnail: thumb = thumbnail[0].replace('s72-c','s320').replace('s1600','s320')
                        else: thumb = ''
                        
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('(Pedido)',"")
                        
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        anofilme = str(q_a_q_a)
                                        tirar_ano = '- ' + str(q_a_q_a)
                                        nome = nome.replace(tirar_ano,'--')
                                        tirar_ano = '-' + str(q_a_q_a)
                                        nome = nome.replace(tirar_ano,'--')
                                        tirar_ano = str(q_a_q_a)
                                        nome = nome.replace(tirar_ano,'--')

                        qualidade = re.compile("--(.*)").findall(nome)
                        if qualidade:
                                qualidade_filme = qualidade[0]
                                nome = nome.replace('--','')
                                nome = nome.replace(qualidade_filme,'')
                        else:
                                qualidade_filme = ''
                                nome = nome.replace('--','')

                        if 'PT/PT' in nome:
                                qualidade_filme = 'PT/PT'
                                nome = nome.replace('-'+qualidade_filme,'')
                                nome = nome.replace('- '+qualidade_filme,'')
                                nome = nome.replace(qualidade_filme,'')
                        if 'PT-PT' in nome:
                                qualidade_filme = 'PT-PT'
                                nome = nome.replace('-'+qualidade_filme,'')
                                nome = nome.replace('- '+qualidade_filme,'')
                                nome = nome.replace(qualidade_filme,'')
                        if 'PT/BR' in nome:
                                qualidade_filme = 'PT/BR'
                                nome = nome.replace('-'+qualidade_filme,'')
                                nome = nome.replace('- '+qualidade_filme,'')
                                nome = nome.replace(qualidade_filme,'')
                        if 'PT-BR' in nome:
                                qualidade_filme = 'PT-BR'
                                nome = nome.replace('-'+qualidade_filme,'')
                                nome = nome.replace('- '+qualidade_filme,'')
                                nome = nome.replace(qualidade_filme,'')

                        nome = nome.replace('((','(')
                        nome = nome.replace('))',')')
                        nome = nome.replace('()','(')
                                        
                        #fanart = artfolder + 'flag.jpg'
                        if fanart == '':
                                nome_pesquisa = nome
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
                                if 'Temporada' in urletitulo[0][1]: url_pesquisa = 'http://www.themoviedb.org/search/tv?query=' + nome_pesquisa
                                else: url_pesquisa = 'http://www.themoviedb.org/search/movie?query=' + nome_pesquisa
                                if thumb == '':# or 's1600' in thumb:
                                        try:
                                                html_pesquisa = FTT_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail: thumb = thumbnail[0].replace('w92','w600')
                                if selfAddon.getSetting('movie-fanart-MVT') == "true":
                                        try:
                                                html_pesquisa = FTT_abrir_url(url_pesquisa)
                                        except: html_pesquisa = ''
                                        items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                        if items_pesquisa != []:
                                                url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(items_pesquisa[0])
                                                if url_filme_pesquisa:
                                                        url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                        try:
                                                                html_pesquisa = FTT_abrir_url(url_pesquisa)
                                                        except: html_pesquisa = ''
                                                        url_fan = re.findall('<div id="backdrops" class="image_carousel">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                                        if url_fan:
                                                                for urls_fanart in url_fan:
                                                                        url_fanart = re.compile('src="(.+?)"').findall(urls_fanart)
                                                                        if url_fanart:
                                                                                fanart = url_fanart[0].replace('w300','w1280')
                                                                        else:
                                                                                fanart = thumb
                                        else: fanart = thumb
                        if selfAddon.getSetting('movie-fanart-MVT') == "true":
                                if fanart == '': fanart = thumb
                        try:
                                addDir_teste('[B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',urlvideo,603,thumb,'',fanart,anofilme,'')
                        except: pass
                        #---------------------------------------------------------------
                        i = i + 1
                        #---------------------------------------------------------------
	proxima = re.compile("<a class='blog-pager-older-link' href='(.+?)' id='Blog1_blog-pager-older-link'").findall(html_source)	
	try:
                proxima_p = proxima[0]#.replace('%3A',':').replace('%2B','+')
		addDir("[B]Página Seguinte >>[/B]",proxima_p.replace('&amp;','&'),602,'','','')
	except: pass



#----------------------------------------------------------------------------------------------------------------------------------------------#

def FTT_encontrar_videos_filmes(name,url):
        colecao = 'nao'
        addDir1(name,'url',1002,iconimage,False,'')
        addDir1('','url',1002,artfolder,False,'')
        conta_id_video = 0
        try:
                fonte_video = FTT_abrir_url(url)
        except: fonte_video = ''
        fontes_video = re.findall("<div class='post hentry'>(.*?)<div style='clear: both;'>", fonte_video, re.DOTALL)
        numero_de_fontes = len(fontes_video)
        for fonte_e_url in fontes_video:
                match1 = re.compile('<script src="(.+?)" type="text/javascript"></script>').findall(fonte_e_url)
                #addDir1(str(len(match1)),'url',1002,artfolder,False,'')
                for fonte_id in match1:
                        if 'videomega' in fonte_id:
                                #addDir1(str(len(match1)),'url',1002,artfolder,False,'')
                                try:  
                                        if 'hashkey' in fonte_id:
                                                conta_id_video = conta_id_video + 1
                                                try:
                                                        urlvideomega = FTT_abrir_url(fonte_id)
                                                except: urlvideomega = ''
                                                if urlvideomega != '':
                                                        urlvidlink = re.compile('ref="(.+?)"').findall(urlvideomega)
                                                        if urlvidlink: url = 'http://videomega.tv/iframe.php?ref=' + urlvidlink[0] + '///' + name
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'','')
                                        if 'iframe.js' in fonte_id:
                                                refvideo = re.compile('<script type="text/javascript">ref="(.+?)".+?</script>').findall(fonte_e_url)
                                                if not refvideo: refvideo = re.compile(">ref='(.+?)'.+?</script>").findall(fonte_e_url)
                                                url = 'http://videomega.tv/iframe.php?ref=' + refvideo[0] + '///' + name
                                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'','')
                                except:pass
                match2 = re.compile('<iframe.+?src="(.+?)".+?></iframe>').findall(fonte_e_url)
                for fonte_id in match2:
                        if 'videomega' in fonte_id:
                                try:
                                        conta_id_video = conta_id_video + 1
                                        url = fonte_id + '///' + name
                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'','')
                                except:pass
                        if 'dropvideo' in fonte_id:
                                try:
                                        conta_id_video = conta_id_video + 1
                                        url = fonte_id + '///' + name
                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Dropvideo)[/COLOR][/B]',url,30,iconimage,'','')
                                except:pass
                        if 'vidto.me' in fonte_id:
                                try:
                                        conta_id_video = conta_id_video + 1
                                        fonte_id = fonte_id.replace('embed-','')
                                        refvideo = re.compile('http://vidto.me/embed-(.+?).html').findall(fonte_id)
                                        if refvideo: url = 'http://vidto.me/' + refvideo[0] + '.html' + '///' + name
                                        else: url = fonte_id + '///' + name
                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'','')
                                except:pass

def FTT_encontrar_videos_filmesllllllllllllllllllllllllllllll(name,url):
        colecao = 'nao'
        addDir1(name,'url',1002,iconimage,False,'')
        addDir1('','url',1002,artfolder,False,'')
        conta_id_video = 0
        try:
                fonte_video = FTT_abrir_url(url)
        except: fonte_video = ''
        fontes_video = re.findall("<body>(.+?)</body>", fonte_video, re.DOTALL)
        numero_de_fontes = len(fontes_video)
        for fonte_e_url in fontes_video:
                match = re.compile('<option value=(.+?)>(.+?)<').findall(fonte_e_url)
                if '<option' in fonte_e_url:
                        for url_video_url_id,cd in match:
                                if url_video_url_id == '""':
                                        if 'CD' in cd:
                                                conta_id_video = 0
                                                cd = cd.replace('Filme Aqui','')
                                                addDir1('[COLOR blue]' + cd + '[/COLOR]','','',iconimage,False,'')
                                        if 'Cole' in cd:
                                                conta_id_video = 0
                                                colecao = 'sim'
                                else:
                                        url_video_url_id = url_video_url_id.replace('"','')
                                if colecao == 'sim' and (('Breve' or 'breve') not in cd):
                                        if 'Cole' not in cd:
                                                conta_id_video = 0
                                                addDir1('[COLOR blue]' + cd + ':[/COLOR]','','',iconimage,False,'')
                                if 'http:' not in url_video_url_id:
                                        url_video = 'http:' + url_video_url_id
                                else:
                                        url_video = url_video_url_id
                                try:
                                        fonte = FTT_abrir_url(url_video)
                                except: fonte = ''
                                fontes = re.findall("<body>(.+?)</body>", fonte, re.DOTALL)
                                for fonte_id in fontes:
                                        if 'videomega' in fonte_id:
                                                try:
                                                        match = re.compile("<script type=\'text/javascript\'>ref=\'(.+?)\'").findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        id_video = match[0]
                                                        url = 'http://videomega.tv/iframe.php?ref=' + id_video + '///' + name
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,100,iconimage,'','')
                                                except:pass
                                        if 'vidto' in fonte_id:
                                                try:
                                                        match = re.compile('<iframe .+? src=".+?//vidto.me/embed-(.+?)" .+?</iframe>').findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        if match: match = re.compile('(.+?)-').findall(match[0])
                                                        id_video = match[0]
                                                        url = 'http://vidto.me/' + id_video + '.html' + '///' + name
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,100,iconimage,'','')
                                                except:pass
                else:
                        #addDir1(url+name,'url',1002,iconimage,False,'')
 	                if fonte_video:
 		                for fonte_id in fontes_video:
                                        if 'videomega' in fonte_id:
                                                try:
                                                        #addDir1(url+name,'url',1002,iconimage,False,'')
                                                        match = re.compile("<script type=\'text/javascript\'>ref=\'(.+?)\'").findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        id_video = match[0]
                                                        url = 'http://videomega.tv/iframe.php?ref=' + id_video + '///' + name
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,100,iconimage,'','')
                                                except:pass
                                        if 'vidto' in fonte_id:
                                                try:
                                                        #addDir1(url+name,'url',1002,iconimage,False,'')
                                                        match = re.compile('<iframe .+? src=".+?//vidto.me/embed-(.+?)" .+?</iframe>').findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        if match: match = re.compile('(.+?)-').findall(match[0])
                                                        id_video = match[0]
                                                        url = 'http://vidto.me/' + id_video + '.html' + '///' + name
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,100,iconimage,'','')
                                                except:pass



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
	liz.setProperty('fanart_image',artfolder + 'Wall.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addLink1(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'Wall.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,checker,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&checker="+urllib.quote_plus(checker)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'flag.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir1(name,url,mode,iconimage,folder,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'flag.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
        return ok

def addDir_teste(name,url,mode,iconimage,plot,fanart,year,genre):
        if fanart == '': fanart = artfolder + 'flag.jpg'
        #text = checker
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&plot="+urllib.quote_plus(plot)+"&year="+urllib.quote_plus(year)+"&genre="+urllib.quote_plus(genre)+"&iconimage="+urllib.quote_plus(iconimage)
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


