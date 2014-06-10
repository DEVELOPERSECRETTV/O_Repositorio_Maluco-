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

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#

def TFC_MenuPrincipal(artfolder):
        addDir1('[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].com','','',artfolder + 'ze-TFC1.png',False,'')
        addDir1('','','',artfolder + 'ze-TFC1.png',False,'')
        addDir('- Pesquisar','http://www.tuga-filmes.info/search?q=',1,artfolder + 'Ze-pesquisar2.png','nao','')
	addDir1('[COLOR blue]Filmes:[/COLOR]','','',artfolder + 'ze-TFC1.png',False,'')
	addDir('[COLOR yellow]- Todos[/COLOR]','http://www.tuga-filmes.info/',72,artfolder + 'ze-TFC1.png','nao','')
	addDir('[COLOR yellow]- Destaques[/COLOR]','http://www.tuga-filmes.info/search/label/destaque',72,artfolder + 'ze-TFC1.png','nao','')
	addDir('[COLOR yellow]- 2013[/COLOR]','http://www.tuga-filmes.info/search/label/-%20Filmes%202013',72,artfolder + 'ze-TFC1.png','nao','')
        addDir('[COLOR yellow]- Top Filmes[/COLOR]','url',79,artfolder + 'ze-TFC1.png','nao','')
	addDir('[COLOR yellow]- Categorias[/COLOR]','url',78,artfolder + 'ze-TFC1.png','nao','')
	addDir('[COLOR yellow]- Animação[/COLOR]','http://www.tuga-filmes.info/search/label/Anima%C3%A7%C3%A3o?max-results=20',72,artfolder + 'ze-TFC1.png','nao','')
	if selfAddon.getSetting('hide-porno') == "false":
                addDir('[B][COLOR red]M+18[/B][/COLOR]','url',86,artfolder + 'ze-TFC1.png','nao','')	

def TFC_Menu_Filmes_Top_10(artfolder):
        url_top_10 = 'http://www.tuga-filmes.info/'
        top_10_source = TFC_abrir_url(url_top_10)
        if selfAddon.getSetting('movies-view') == "0":
                addDir1('[B][COLOR blue]TOP 10[/COLOR][/B]','','',artfolder + 'ze-TFC1.png',False,'')
                addDir1('','','',artfolder + 'ze-TFC1.png',False,'')
        filmes_top_10 = re.compile("<img alt=\'\' border=\'0\' height=\'72\' src=\'(.+?)\' width=\'72\'/>\n</a>\n</div>\n<div class=\'item-title\'><a href=\'(.+?)\'>(.+?)</a></div>\n</div>\n<div style=\'clear: both;\'>").findall(top_10_source)
	for iconimage_filmes_top_10,endereco_top_10,nome_top_10 in filmes_top_10:
		addDir(nome_top_10,endereco_top_10,73,iconimage_filmes_top_10.replace('s72-c','s320').replace('.gif','.jpg'),'nao','')

def TFC_Menu_Filmes_Por_Categorias(artfolder):
        url_categorias = 'http://www.tuga-filmes.info/'
        html_categorias_source = TFC_abrir_url(url_categorias)
        addDir1('[B][COLOR blue]Categorias[/COLOR][/B]','','',artfolder + 'ze-TFC1.png',False,'')
        addDir1('','','',artfolder + 'ze-TFC1.png',False,'')
	html_items_categorias = re.findall("<div id=\'nav-cat\'>(.*?)</div>", html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<a href=\'/(.+?)\'>(.+?)</a>").findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        categoria_endereco = url_categorias + endereco_categoria
                        addDir('[COLOR yellow]' + nome_categoria + '[/COLOR]',categoria_endereco,72,artfolder + 'ze-TFC1.png','nao','')
        


#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#

		

def TFC_encontrar_fontes_filmes(url):
        pt_en = 0
        conta_items = 1
        if conta_items == 1:      
                mensagemprogresso = xbmcgui.DialogProgress()
                mensagemprogresso.create('Tuga-Filmes.com', 'A Pesquisar','Por favor aguarde...')
                mensagemprogresso.update(0)
	try:
		html_source = TFC_abrir_url(url)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        fanart = ''
                        thumb = ''
                        versao = ''
                        pt_en_f = re.compile('<iframe (.+?)</iframe>').findall(item)
                        if '---------------------------------------' in item and len(pt_en_f) > 1: versao = '[COLOR blue] 2 VERSÕES[/COLOR]'
                        assist = re.findall(">ASSISTIR.+?", item, re.DOTALL)
                        if len(assist) > 1: versao = '[COLOR blue] 2 VERSÕES[/COLOR]'
			urletitulo = re.compile("<a href=\'(.+?)\' title=\'(.+?)\'>").findall(item)
			qualidade_ano = re.compile('<b>VERS\xc3\x83O:.+?</b><span style="font-size: x-small;">(.+?)<').findall(item)
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
                                        ano = 'Ano'
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
                                try:
                                        html_pesquisa = TFC_abrir_url(url_pesquisa)
                                except: html_pesquisa = ''
                                items_pesquisa = re.findall('<div class="poster">(.*?)<div style="clear: both;">', html_pesquisa, re.DOTALL)
                                if items_pesquisa != []:
                                        if thumb == '':
                                                thumbnail = re.compile('<img class="right_shadow" src="(.+?)" width=').findall(items_pesquisa[0])
                                                if thumbnail: thumb = thumbnail[0].replace('w92','w600')
                                        url_filme_pesquisa = re.compile('href="(.+?)" title=".+?"><img').findall(items_pesquisa[0])
                                        if url_filme_pesquisa:
                                                url_pesquisa = 'http://www.themoviedb.org' + url_filme_pesquisa[0]
                                                try:
                                                        html_pesquisa = TFC_abrir_url(url_pesquisa)
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
                        if fanart == '': fanart = thumb
			try:
				if 'ASSISTIR O FILME' in item: addDir_teste('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR][COLOR red] (' + qualidade + ')[/COLOR]' + versao,urletitulo[0][0],73,thumb.replace('s1600','s320').replace('.gif','.jpg'),'',fanart,ano,'')
			except: pass
			#---------------------------------------------------------------
                        conta_items = conta_items + 1   
                        if conta_items == 2:      
                                mensagemprogresso.update(10)
                        if conta_items == 4:
                                mensagemprogresso.update(20)
                        if conta_items == 6:
                                mensagemprogresso.update(30)
                        if conta_items == 8:      
                                mensagemprogresso.update(40)
                        if conta_items == 10:
                                mensagemprogresso.update(50)
                        if conta_items == 12:
                                mensagemprogresso.update(60)
                        if conta_items == 14:      
                                mensagemprogresso.update(70)
                        if conta_items == 16:
                                mensagemprogresso.update(80)
                        if conta_items == 17:
                                mensagemprogresso.update(90)
                        if conta_items == len(items):
                                mensagemprogresso.update(100)
                                mensagemprogresso.close()
                        #---------------------------------------------------------------
	else:
		items = re.compile("<a href=\'(.+?)\' title=.+?>Assistir Online - </div>(.+?)<div id=\'player\'>").findall(html_source)
		for endereco,nome in items:
			addDir(nome.replace('&#8217;',"'"),endereco,73,'','','')
	proxima = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
	try:
		addDir("[B]Página Seguinte >>[/B]",proxima[0].replace('&amp;','&'),72,artfolder + 'ze-TFC1.png','','')
	except: pass

#----------------------------------------------------------------------------------------------------------------------------------------------#
	
def TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video):
        url = url + '///' + name
        if "videomega" in url:
		try:
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "vidto.me" in url:
		try:
                        print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,70,iconimage,'','')
		except: pass
        if "dropvideo" in url:
		try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B]',url,70,iconimage,'','')
		except:pass
	if "streamin.to" in url:
                try:
			print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,70,iconimage,'','')
                except:pass                        
        if "putlocker" in url:
                try:
                        print url
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Putlocker)[/COLOR][/B]',url,70,iconimage,'','')
    		except:pass
    	if "nowvideo" in url:
                try:
                        print url
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,70,iconimage,'','')
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoWood)[/COLOR][/B]',url,70,iconimage,'','')
    		except:pass
    	return

#----------------------------------------------------------------------------------------------------------------------------------------------#

def TFC_encontrar_videos_filmes(name,url):
        conta_id_video = 0
	addDir1(name,'','',iconimage,False,'')
        addDir1('','','',iconimage,False,'')
        try:
                fonte = TFC_abrir_url(url)
        except: fonte = ''
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
                                                        addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,'')
                                                if 'PT/PT' in assis[0]:
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,'')
                                                elif 'PT-PT' in assis[0]: addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,'')
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video)
                                        match = re.compile('<a href="(.+?)" target=".+?">Ver Aqui</a>').findall(ass_fon)
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video)
                                assistir_fontes = re.findall("------------------------------<br />(.*?)='postmeta'>", fonte, re.DOTALL)
                                assistir_fontes = re.findall(">ASSISTIR(.*?)<div class", assistir_fontes[0], re.DOTALL)
                                conta_id_video = 0
                                for ass_fon in assistir_fontes:
                                        match = re.compile('<iframe .+? src="(.+?)"').findall(ass_fon)
                                        assis = re.compile('ONLINE(.+?)</span>').findall(ass_fon)
                                        conta_video = len(match)
                                        if assis:
                                                if 'LEGENDADO' in assis[0]:
                                                        addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,'')
                                                if 'PT/PT' in assis[0]:
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,'')
                                                elif 'PT-PT' in assis[0]: addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,'')
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video)
                                        match = re.compile('<a href="(.+?)" target=".+?">Ver Aqui</a>').findall(ass_fon)
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video)
                        else:
                                assistir_fontes = re.findall('>ASSISTIR(.*?)</iframe>', fonte, re.DOTALL)
                                conta_id_video = 0
                                for ass_fon in assistir_fontes:
                                        match = re.compile('<iframe .+? src="(.+?)"').findall(ass_fon)
                                        assis = re.compile('ONLINE(.+?)</span>').findall(ass_fon)
                                        conta_video = len(match)
                                        if assis:
                                                if 'LEGENDADO' in assis[0]:
                                                        addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,'')
                                                if 'PT/PT' in assis[0]:
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,'')
                                                elif 'PT-PT' in assis[0]: addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,'')
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video)
                                        match = re.compile('<a href="(.+?)" target=".+?">Ver Aqui</a>').findall(ass_fon)
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video)
                else:
                        match = re.compile('<iframe .+? src="(.+?)"').findall(fonte)
                        conta_video = len(match)
                        for url in match:                                
                                id_video = ''
                                conta_id_video = conta_id_video + 1
                                TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video)
                        if numero_de_fontes > 0:
                                conta_video = 0
                                match = re.compile('<a href="(.+?)" target=".+?">Ver Aqui</a>').findall(fonte)
                                url = match[0]
                                if url != '':
                                        try:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video)
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
	liz.setProperty('fanart_image',artfolder + 'flag.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addLink1(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'flag.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addLink2(name,url,iconimage,checker):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&checker="+urllib.quote_plus(checker)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'flag.jpg')
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

