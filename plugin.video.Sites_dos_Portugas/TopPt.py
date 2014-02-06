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


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,urlresolver
from array import array
from string import capwords


arrai_nome_series = ['' for i in range(50)]
arrai_endereco_series = ['' for i in range(50)]
arrai_series = [['' for i in range(50)] for j in range(2)]

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#



def TPT_MenuPrincipal(artfolder):
        url_toppt = 'http://toppt.net/'
        toppt_source = TPT_abrir_url(url_toppt)
        saber_url_animacao = re.compile('<a href="(.+?)">Animacao</a></li>').findall(toppt_source)
        addDir1('[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.com[/COLOR][/B]','','',artfolder + 'ze-TFV1.png',False,'')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
	addDir('[COLOR yellow]Menu Filmes[/COLOR]','url',237,artfolder + 'ze-TFV1.png','nao','')
	addDir('[COLOR yellow]Menu Séries[/COLOR]','url',240,artfolder + 'ze-TFV1.png','nao','')	
	addDir('[COLOR yellow]Filmes Animação[/COLOR]',saber_url_animacao[0],232,artfolder + 'ze-TFV1.png','nao','')
        #addDir('[COLOR yellow]Recentes[/COLOR]','url',248,artfolder + 'ze-TFV1.png','nao','')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
	addDir('Pesquisar','url',1,artfolder + 'Ze-pesquisar1.png','nao','')
	#addDir('[COLOR brown]ChangeLog[/COLOR]','http://o-repositorio-maluco.googlecode.com/svn/trunk/changelogs/changelog_TugaFilmesTV.txt',56,artfolder + 'ze-TFV1.png','nao','')
 
def TPT_Menu_Filmes(artfolder):
        url_toppt = 'http://toppt.net/'
        toppt_source = TPT_abrir_url(url_toppt)
        saber_url_todos = re.compile('<a href="(.+?)">filmes</a></li>').findall(toppt_source)
        saber_url_M18 = re.compile('<option class="level-0" value="92">m18</option>').findall(toppt_source)
        addDir1('[B][COLOR blue]Menu Filmes[/COLOR][/B]','','',artfolder + 'ze-TFV1.png',False,'')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
	addDir('[COLOR yellow]Ver Todos[/COLOR]',saber_url_todos[0],232,artfolder + 'ze-TFV1.png','nao','')
        addDir('[COLOR yellow]Ver por Ano[/COLOR]','url',239,artfolder + 'ze-TFV1.png','nao','')
	addDir('[COLOR yellow]Categorias[/COLOR]','url',238,artfolder + 'ze-TFV1.png','nao','')
	#addDir('[COLOR yellow]Top 5 da Semana[/COLOR]','url',248,artfolder + 'ze-TFV1.png','nao','')
	if selfAddon.getSetting('hide-porno') == "false":
			addDir('[B][COLOR red]M+18[/B][/COLOR]','http://toppt.net/?cat=' + saber_url_M18[0],232,artfolder + 'ze-TFV1.png','nao','')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
	addDir('Pesquisar','url',1,artfolder + 'Ze-pesquisar1.png','nao','')

def TPT_Menu_Series(artfolder):
        url_toppt = 'http://toppt.net/'
        toppt_source = TPT_abrir_url(url_toppt)
        saber_url_series = re.compile('<a href="(.+?)">Series</a></li>').findall(toppt_source)
        addDir1('[B][COLOR blue]Menu Séries[/COLOR][/B]','','',artfolder + 'ze-TFV1.png',False,'')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
	addDir('[COLOR yellow]A a Z[/COLOR]','url',241,artfolder + 'ze-TFV1.png','nao','')
        addDir('[COLOR yellow]Recentes[/COLOR]',saber_url_series[0],232,artfolder + 'ze-TFV1.png','nao','')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
	addDir('Pesquisar','http://www.tuga-filmes.tv/search?q=',1,artfolder + 'Ze-pesquisar1.png','nao','')

def TPT_Menu_Posts_Recentes(artfolder):
        url_recentes = 'http://toppt.net/'
        recentes_source = TPT_abrir_url(url_recentes)
        addDir1('[B][COLOR blue]Recentes[/COLOR][/B]','','',artfolder + 'ze-TFV1.png',False,'')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
        posts_recentes = re.compile('<a href="(.+?)">.+?</a>\n</li>\n<li>\n').findall(recentes_source)
        for endereco_recentes in posts_recentes:                
                #TPT_encontrar_fontes_filmes(endereco_recentes,artfolder)
                try:
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('(PT-PT)',"")
                        nome = nome.replace('(PT/PT)',"")
                        nome = nome.replace('[PT-PT]',"")
                        nome = nome.replace('[PT/PT]',"")
                        addDir('[B][COLOR green]' + nome + '[/COLOR][/B]',endereco_recentes,233,'','','')
                        #addDir('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR]',urletitulo[0][0],num_mode,thumbnail[0].replace('s72-c','s320'),'','')
                except: pass


def TPT_Menu_Filmes_Por_Ano(artfolder):
        url_ano = 'http://toppt.net/'
        ano_source = TPT_abrir_url(url_ano)
        filmes_por_ano = re.compile('<option class="level-0" value="(.+?)">(.+?)</option>').findall(ano_source)
	for num_cat,nome_ano in filmes_por_ano:
                endereco_ano = 'http://toppt.net/?cat=' + str(num_cat)
		addDir('[COLOR yellow]' + nome_ano + '[/COLOR] ',endereco_ano,232,artfolder + 'ze-TFV1.png','nao','')
		if str(nome_ano) == '2014': break

def TPT_Menu_Filmes_Por_Categorias(artfolder):
        url_categorias = 'http://toppt.net/'
        html_categorias_source = TPT_abrir_url(url_categorias)
	html_items_categorias = re.findall('<h1 class="widget-title">FILMES</h1>(.*?)<h1 class="widget-title">MUSICAS</h1>', html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile('<a href="(.+?)">(.+?)</a>').findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        if nome_categoria != '2011' and nome_categoria != '2012' and nome_categoria != '2013' and nome_categoria != '2014':
                                addDir('[COLOR yellow]' + nome_categoria + '[/COLOR] ',endereco_categoria,232,artfolder + 'ze-TFV1.png','nao','')

def TPT_Menu_Series_A_a_Z(artfolder):
        conta = 0
        url_series = 'http://toppt.net/'
	html_series_source = TPT_abrir_url(url_series)
	html_items_series = re.findall('<h1 class="widget-title">SERIES</h1>(.*?)</ul></div></aside>', html_series_source, re.DOTALL)	
        print len(html_items_series)
        for item_series in html_items_series:
                series = re.compile('<a href="(.+?)">(.+?)</a>').findall(item_series)
                for endereco_series,nome_series in series:
                        if conta == 0:
                                addDir1('[B][COLOR blue]Séries[/COLOR][/B] (' + str(len(series)) + ')','','',artfolder + 'ze-TFV1.png',False,'')
                                addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
                                conta = 1
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        nome_series = nome_series.replace('&#8217;',"'")
                        nome_series = nome_series.replace('&#8230;',"...")
                        addDir('[COLOR yellow]' + nome_series + '[/COLOR]',endereco_series,232,artfolder + 'ze-TFV1.png','nao','')



#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#

		

def TPT_encontrar_fontes_filmes(url,artfolder):        
        if 'Seguinte' not in name:
                addDir1(name + ':','','',iconimage,False,'')
                addDir1('','','',iconimage,False,'')
	try:
		html_source = TPT_abrir_url(url)
	except: html_source = ''
	items = re.findall('<h1 class="entry-title">(.*?)</article>', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        audio_filme = ''
                        urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(item)
                        qualidade = re.compile("<b>QUALIDADE:.+?/b>(.+?)<br/>").findall(item)
                        ano = re.compile("<b>ANO:.+?/b>(.+?)<br/>").findall(item)
                        audio = re.compile("<b>AUDIO:.+?/b>(.+?)<br/>").findall(item)
                        thumbnail = re.compile('src="(.+?)"').findall(item)
                        print urletitulo,thumbnail
                        nome = urletitulo[0][1]
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('(PT-PT)',"")
                        nome = nome.replace('(PT/PT)',"")
                        nome = nome.replace('[PT-PT]',"")
                        nome = nome.replace('[PT/PT]',"")
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
                                        ano_filme = ': ' + ano[0]
                                else:
                                        ano_filme = ''     
                        if ano:
                                ano_filme = ano[0]
                                a_q = re.compile('\d+')
                                qq_aa = a_q.findall(nome)
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) == 4:
                                                tirar_ano = '(' + str(q_a_q_a) + ')'
                                                nome = nome.replace(tirar_ano,'')
                        if qualidade:
                                qualidade = qualidade[0]
                                qualidade = qualidade.replace('[',' - ')
                                qualidade = qualidade.replace(']','')
                        else:
                                qualidade = re.compile("\nQUALIDADE:\xc2\xa0(.+?)<br/>").findall(item)
                                if qualidade:
                                        qualidade = qualidade[0]
                                        qualidade = qualidade.replace('[',' - ')
                                        qualidade = qualidade.replace(']','')
                                else:
                                        qualidade = ''
                        try:
                                #addDir('[B][COLOR green]' + nome + '[/COLOR][/B]',urletitulo[0][0],num_mode,thumbnail[0].replace('s72-c','s320'),'','')
                                addDir('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR]',urletitulo[0][0],233,thumbnail[0].replace('s72-c','s320'),'','')
                        except: pass
	else:
		items = re.compile('<h1 class="entry-title"><a href="(.+?)" .+?>(.+?)</a>').findall(html_source)
		for endereco,nome in items:
                        try:
                                addDir(nome,endereco,233,'','','')
                        except:pass
	proxima = re.compile('.*href="(.+?)">Next &rarr;</a>').findall(html_source)		
	try:
		addDir("Página Seguinte >>",proxima[0].replace('#038;',''),232,artfolder + 'ze-TFV1.png','','')
        except:pass


#----------------------------------------------------------------------------------------------------------------------------------------------#

def TPT_encontrar_videos_filmes(name,url):
        conta_id_video = 0
	addDir1(name,'','',iconimage,False,'')
        addDir1('','','',iconimage,False,'')
        #try:
                #fonte = TPT_abrir_url(url)
        #except: fonte = ''
        #fontes = re.findall("Ver Aqui(.+?)", fonte, re.DOTALL)
        #numero_de_fontes = len(fontes)
	try:
		link2=TPT_abrir_url(url)
	except: link2 = ''
	if link2:
                newmatch = re.findall('<span id=.+?<nav class="navigation post-navigation"',link2,re.DOTALL)
                #parameters = {"nome_texto" : name, "url": url, "addonid": 'TFV'}
                #nome_textbox = urllib.urlencode(parameters)
                #addDir('[COLOR blue]Sinopse[/COLOR]',nome_textbox,57,iconimage,'nao','')
                #trailer = re.compile('<b>Trailer</b>: <a href="(.+?)" target="_blank">').findall(link2)
                #if trailer: addDir('[COLOR blue]Trailer[/COLOR]',trailer[0],30,iconimage,'nao','')
                #-------------------- Videomega
                if newmatch:
			linksseccao = re.findall('<p>PARTE (\d+)<br/>\n(.+?)</p>',newmatch[0],re.DOTALL)
			if linksseccao:			
				for parte1,parte2 in linksseccao:
                                        conta_id_video = 0
					addDir1('[COLOR blue] Parte '+parte1+'[/COLOR]','','',iconimage,False,'')					
					match = re.compile('<iframe src="(.+?)"').findall(parte2)	
					for url in match:
                                                conta_id_video = conta_id_video + 1
						TPT_resolve_not_videomega_filmes(url,conta_id_video)
					match = re.compile('<a href="(.+?)" target="_blank">Ver Aqui</a>').findall(parte2)
					for url in match:
                                                conta_id_video = conta_id_video + 1
						TPT_resolve_not_videomega_filmes(url,conta_id_video)
			else:
                                linksseccao = re.findall('<span style="color:.+?"><strong>(.+?)</strong></span><br/>(.+?)Ver Aqui</a></p>',newmatch[0],re.DOTALL)
				if linksseccao:			
					for parte1,parte2 in linksseccao:
                                                parte1=parte1.replace('[','(').replace(']',')')
                                                conta_id_video = 0
						addDir1('[COLOR blue]'+parte1+'[/COLOR]','','',iconimage,False,'')					
						match = re.compile('<iframe src="(.+?)"').findall(parte2)	
						for url in match:
                                                        conta_id_video = conta_id_video + 1
							TPT_resolve_not_videomega_filmes(url,conta_id_video)
						match = re.compile('<a href="(.+?)" target="_blank">').findall(parte2)
						for url in match:
                                                        conta_id_video = conta_id_video + 1
							TPT_resolve_not_videomega_filmes(url,conta_id_video)
				else:
                                        linksseccao = re.findall('<p>EPISODIO (.+?)<br/>\n(.+?)</p>',newmatch[0],re.DOTALL)
                                        if linksseccao:			
                                                for parte1,parte2 in linksseccao:
                                                        conta_id_video = 0
                                                        addDir1('[COLOR blue] Episódio '+parte1+'[/COLOR]','','',iconimage,False,'')					
                                                        match = re.compile('<iframe src="(.+?)"').findall(parte2)	
                                                        for url in match:
                                                                conta_id_video = conta_id_video + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                                        match = re.compile('<a href="(.+?)" target="_blank">Ver Aqui</a>').findall(parte2)
                                                        for url in match:
                                                                conta_id_video = conta_id_video + 1
                                                                TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                        else:
                                                match = re.compile('<iframe src="(.+?)"').findall(newmatch[0])	
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                                match = re.compile('</b><a href="(.+?)" target="_blank">Ver Aqui</a>').findall(newmatch[0])
                                                for url in match:
                                                        conta_id_video = conta_id_video + 1
                                                        TPT_resolve_not_videomega_filmes(url,conta_id_video)
		else:
			newmatch = re.findall('EM PT/PT:.+?<nav class="navigation post-navigation"',link2,re.DOTALL)
			if newmatch:
				linksseccao = re.findall('<p>PARTE (\d+)<br/>\n(.+?)</p>',newmatch[0],re.DOTALL)
				if linksseccao:
					for parte1,parte2 in linksseccao:
                                                conta_id_video = 0
						addDir1('[COLOR bue] Parte '+parte1+'[/COLOR]',urlfinal,'',iconimage,False,'')					
						match = re.compile('<iframe src="(.+?)"').findall(parte2)	
						for url in match:
                                                        conta_id_video = conta_id_video + 1
							TPT_resolve_not_videomega_filmes(url,conta_id_video)
						match = re.compile('<a href="(.+?)" target="_blank">Ver Aqui</a>').findall(parte2)
						for url in match:
                                                        conta_id_video = conta_id_video + 1
							TPT_resolve_not_videomega_filmes(url,conta_id_video)
                                else:
					linksseccao = re.findall('<p>EPISODIO (.+?)<br/>\n(.+?)</p>',newmatch[0],re.DOTALL)
					if linksseccao:			
						for parte1,parte2 in linksseccao:
                                                        conta_id_video = 0
							addDir('[COLOR yellow] Episódio '+parte1+'[/COLOR]',urlfinal,'',iconimage,False,'')					
							match = re.compile('<iframe src="(.+?)"').findall(parte2)	
							for url in match:
                                                                conta_id_video = conta_id_video + 1
								TPT_resolve_not_videomega_filmes(url,conta_id_video)
							match = re.compile('<a href="(.+?)" target="_blank">Ver Aqui</a>').findall(parte2)
							match = re.compile('<a href="(.+?)" target="_blank">Ver Aqui</a>').findall(parte2)
							match = re.compile('<a href="(.+?)" target="_blank">Ver Aqui</a>').findall(parte2)
							for url in match:
                                                                conta_id_video = conta_id_video + 1
								TPT_resolve_not_videomega_filmes(url,conta_id_video)				
					else:
						match = re.compile('<iframe src="(.+?)"').findall(newmatch[0])	
						for url in match:
                                                        conta_id_video = conta_id_video + 1
							TPT_resolve_not_videomega_filmes(url,conta_id_video)
						match = re.compile('</b><a href="(.+?)" target="_blank">Ver Aqui</a>').findall(newmatch[0])
						for url in match:
                                                        conta_id_video = conta_id_video + 1
							TPT_resolve_not_videomega_filmes(url,conta_id_video)
				
#----------------------------------------------------------------------------------------------------------------------------------------------#

def TPT_resolve_not_videomega_filmes(url,conta_id_video):
        if "videomega" in url:
		try:
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "vidto.me" in url:
		try:
                        match = re.compile('http://vidto.me/embed-(.+?).html').findall(url)
			if match:
				id_video = match[0]
				url = 'http://vidto.me/' + id_video + '.html'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "dropvideo" in url:
		try:
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B]',url,30,iconimage,'','')
		except:pass
	if "streamin.to" in url:
                try:
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,30,iconimage,'','')
                except:pass                        
        if "putlocker" in url:
                try:
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Putlocker)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "nowvideo" in url:
                try:
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "primeshare" in url:
                try:
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Primeshare.tv)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "videoslasher" in url:
                try:
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoSlasher)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "sockshare" in url:
                try:
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Sockshare)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	return

   
	
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

def addDir(name,url,mode,iconimage,checker,fanart):
        text = 'nnnnnn'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&checker="+urllib.quote_plus(checker)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'flag.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": text } )
        #cm = []
	#cm.append(('Sinopse', 'XBMC.Action(Info)'))
	#liz.addContextMenuItems(cm, replaceItems=True)
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


#----------------------------------------------------------------------------------------------------------------------------------------------#
	
params=TPT_get_params()
url=None
name=None
mode=None
checker=None
iconimage=None
fanart=None

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

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Checker: "+str(checker)
print "Iconimage: "+str(iconimage)


