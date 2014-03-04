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



def ARM_MenuPrincipal():
        addLink('teste','http://www.video.tt/player/player.swf?v=5SyAdRgZr','')
        addDir1('[B][COLOR yellow]ARMAGEDOM[/COLOR][COLOR green]FILMES[/COLOR][/B]','','','',False,'')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
	addDir('[COLOR blue]Menu Filmes[/COLOR]','url',337,artfolder + 'ze-TFV1.png','nao','')
	addDir('[COLOR blue]Menu Séries[/COLOR]','url',340,artfolder + 'ze-TFV1.png','nao','')	
	addDir('[COLOR blue]Filmes Animação[/COLOR]','http://www.armagedomfilmes.biz/?cat=3228',332,artfolder + 'ze-TFV1.png','nao','')
        #addDir('[COLOR blue]Recentes[/COLOR]','url',248,artfolder + 'ze-TFV1.png','nao','')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
	addDir('Pesquisar','url',1,artfolder + 'Ze-pesquisar1.png','nao','')
	#addDir('[COLOR brown]ChangeLog[/COLOR]','http://o-repositorio-maluco.googlecode.com/svn/trunk/changelogs/changelog_TugaFilmesTV.txt',56,artfolder + 'ze-TFV1.png','nao','')
 
def ARM_Menu_Filmes():
        addDir1('[B][COLOR yellow]Menu Filmes[/COLOR][/B]','','',artfolder + 'ze-TFV1.png',False,'')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
	addDir('[COLOR blue]Ver Todos[/COLOR]','http://www.armagedomfilmes.biz/?s=legendado',332,artfolder + 'ze-TFV1.png','nao','')
        addDir('[COLOR blue]Ver por Ano[/COLOR]','url',339,artfolder + 'ze-TFV1.png','nao','')
	addDir('[COLOR blue]Categorias[/COLOR]','url',338,artfolder + 'ze-TFV1.png','nao','')
	#addDir('[COLOR blue]Top 5 da Semana[/COLOR]','url',248,artfolder + 'ze-TFV1.png','nao','')
	if selfAddon.getSetting('hide-porno') == "false":
			addDir('[B][COLOR red]M+18[/B][/COLOR]','url',332,artfolder + 'ze-TFV1.png','nao','')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
	addDir('Pesquisar','url',1,artfolder + 'Ze-pesquisar1.png','nao','')

def ARM_Menu_Series():
        addDir1('[B][COLOR yellow]Menu Séries[/COLOR][/B]','','',artfolder + 'ze-TFV1.png',False,'')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
	addDir('[COLOR blue]A a Z[/COLOR]','url',341,artfolder + 'ze-TFV1.png','nao','')
        addDir('[COLOR blue]Recentes[/COLOR]','url',332,artfolder + 'ze-TFV1.png','nao','')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
	addDir('Pesquisar','http://www.tuga-filmes.tv/search?q=',1,artfolder + 'Ze-pesquisar1.png','nao','')

def ARM_Menu_Posts_Recentes():
        url_recentes = 'http://toppt.net/'
        recentes_source = ARM_abrir_url(url_recentes)
        addDir1('[B][COLOR yellow]Recentes[/COLOR][/B]','','',artfolder + 'ze-TFV1.png',False,'')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
        posts_recentes = re.compile('<a href="(.+?)">.+?</a>\n</li>\n<li>\n').findall(recentes_source)
        for endereco_recentes in posts_recentes:                
                #ARM_encontrar_fontes_filmes(endereco_recentes,artfolder)
                try:
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('(PT-PT)',"")
                        nome = nome.replace('(PT/PT)',"")
                        nome = nome.replace('[PT-PT]',"")
                        nome = nome.replace('[PT/PT]',"")
                        addDir('[B][COLOR green]' + nome + '[/COLOR][/B]',endereco_recentes,333,'','','')
                        #addDir('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR blue](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR]',urletitulo[0][0],num_mode,thumbnail[0].replace('s72-c','s320'),'','')
                except: pass


def ARM_Menu_Filmes_Por_Ano():
        url_ano = 'http://toppt.net/'
        ano_source = ARM_abrir_url(url_ano)
        filmes_por_ano = re.compile('<option class="level-0" value="(.+?)">(.+?)</option>').findall(ano_source)
	for num_cat,nome_ano in filmes_por_ano:
                endereco_ano = 'http://toppt.net/?cat=' + str(num_cat)
		addDir('[COLOR blue]' + nome_ano + '[/COLOR] ',endereco_ano,332,artfolder + 'ze-TFV1.png','nao','')
		if str(nome_ano) == '2014': break

def ARM_Menu_Filmes_Por_Categorias():
        url_categorias = 'http://toppt.net/'
        html_categorias_source = ARM_abrir_url(url_categorias)
	html_items_categorias = re.findall('<h1 class="widget-title">FILMES</h1>(.*?)<h1 class="widget-title">MUSICAS</h1>', html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile('<a href="(.+?)">(.+?)</a>').findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        if nome_categoria != '2011' and nome_categoria != '2012' and nome_categoria != '2013' and nome_categoria != '2014':
                                addDir('[COLOR blue]' + nome_categoria + '[/COLOR] ',endereco_categoria,332,artfolder + 'ze-TFV1.png','nao','')

def ARM_Menu_Series_A_a_Z():
        conta = 0
        url_series = 'http://toppt.net/'
	html_series_source = ARM_abrir_url(url_series)
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
                        addDir('[COLOR blue]' + nome_series + '[/COLOR]',endereco_series,332,artfolder + 'ze-TFV1.png','nao','')



#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#

		

def ARM_encontrar_fontes_filmes():        
        if 'Seguinte' not in name:
                addDir1(name + ':','','',iconimage,False,'')
                addDir1('','','',iconimage,False,'')
	try:
		html_source = ARM_abrir_url(url)
	except: html_source = ''
	items = re.findall('<div class="titulo-post-us">(.*?)<div class="div-us">', html_source, re.DOTALL)
	addDir1(str(len(items)),'','',iconimage,False,'')
	if items != []:
		print len(items)
		for item in items:
                        urletitulo = re.compile('<a href="(.+?)" title="(.+?)">').findall(item)
                        thumbnail = re.compile('src="(.+?)"').findall(item)
                        if thumbnail: thumb = thumbnail[0]
                        else: thumb = ''
                        urlfilme = urletitulo[0][0]
                        nome = urletitulo[0][1].replace('Assistir ','')
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        if qq_aa:
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) == 4:
                                                ano = str(q_a_q_a)
                                                nome = nome.replace(' '+ano,'')
                        else: ano = ''
                        if ' Dublado ou Legendado' in nome: nome = nome.replace(' Dublado ou Legendado','')
                        if ' Dublado e Legendado &#8211;' in nome: nome = nome.replace(' Dublado e Legendado &#8211;','')
                        if ' Dublado e Legendado' in nome: nome = nome.replace(' Dublado e Legendado','')
                        if ' Online' in nome: nome = nome.replace(' Online','')
                        if ' Dublado' in nome: nome = nome.replace(' Dublado','')
                        if ' Legendado' in nome: nome = nome.replace(' Legendado','')
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8230;',"...")
                        nome = nome.replace('&#8211;',"-")
                        try:
                                addDir('[B][COLOR yellow]' + nome + '[/COLOR][COLOR green] (' + ano + ')[/COLOR][/B]',urlfilme,333,thumb,'nao','')
                        except: pass
	proxima = re.compile('<link rel="next" href="(.+?)"/>').findall(html_source)		
	try:
		addDir("Página Seguinte >>",proxima[0].replace('#038;',''),332,artfolder + 'ze-TFV1.png','nao','')
        except:pass


#----------------------------------------------------------------------------------------------------------------------------------------------#

def ARM_encontrar_videos_filmes(name,url):
        num_fonte = 0
	addDir1(name,'','',iconimage,False,'')
        addDir1('','','',iconimage,False,'')
	try:
		link2=ARM_abrir_url(url)
	except: link2 = '' 
	if link2:
                matchvideo = re.findall('\n \n \n<div(.*?)</div>\n \n \n', link2, re.DOTALL)
                #addDir1(str(len(matchvideo)),'','',iconimage,False,'')
                if 'ASSISTIR: LEGENDADO' in link2: addDir1('[COLOR orange]Dublado:[/COLOR]','','',iconimage,False,'')
                for match in matchvideo:
                        urls_video = re.compile('src="(.+?)"').findall(match)
                        if urls_video:
                                for url_video in urls_video:
                                        id_video = re.compile('id=(.*)').findall(url_video)
                                        if id_video: id_video = id_video[0]
                                        else: id_video = ''
                                        num_fonte = num_fonte + 1
                                        #addDir1(url_video+id_video[0],'','',iconimage,False,'')
                                        #id_video = id_video[0]
                                        ARM_resolve_not_videomega_filmes(url_video,id_video,num_fonte)
                        urls_video = re.compile('SRC="(.+?)"').findall(match)
                        if urls_video:
                                for url_video in urls_video:
                                        id_video = re.compile('id=(.*)').findall(url_video)
                                        if id_video: id_video = id_video[0]
                                        else: id_video = ''
                                        num_fonte = num_fonte + 1
                                        #addDir1(url_video+id_video[0],'','',iconimage,False,'')
                                        #id_video = id_video[0]
                                        ARM_resolve_not_videomega_filmes(url_video,id_video,num_fonte)
                if 'ASSISTIR: LEGENDADO' in link2:
                        num_fonte = 0
                        addDir1('[COLOR orange]Legendado:[/COLOR]','','',iconimage,False,'')
                        matchvideo = re.findall('<p style="text-align: center;">(.*?)target="_blank">OP', link2, re.DOTALL)
                        for match in matchvideo:
                                urls_video = re.compile('href="(.+?)"').findall(match)
                                if urls_video:
                                        for url_video in urls_video:
                                                id_video = re.compile('id=(.*)').findall(url_video)
                                                if id_video: id_video = id_video[0]
                                                else: id_video = ''
                                                num_fonte = num_fonte + 1
                                                #addDir1(url_video+id_video[0],'','',iconimage,False,'')
                                                #id_video = id_video[0]
                                                ARM_resolve_not_videomega_filmes(url_video,id_video,num_fonte)
                #if 'Temporada' in link2 or 'TEMPORADA' in link2:
                        #matchvideo = re.findall('<p style="text-align: center;">(.*?)target="_blank">OP', link2, re.DOTALL)
                        
				
#----------------------------------------------------------------------------------------------------------------------------------------------#

def ARM_resolve_not_videomega_filmes(url,id_video,num_fonte):
        if "videomega" in url:
		try:
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Videomega)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "vidto.me" in url:
		try:
                        match = re.compile('http://vidto.me/embed-(.+?).html').findall(url)
			if match:
				id_video = match[0]
				url = 'http://vidto.me/' + id_video + '.html'
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Vidto.me)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "dropvideo" in url or 'drop' in url:
		try:
                        url = 'http://dropvideo.com/embed/' + id_video
			print url
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](DropVideo)[/COLOR][/B]',url,30,iconimage,'','')
		except:pass
	if "streamin.to" in url:
                try:
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,30,iconimage,'','')
                except:pass                        
        if "putlocker" in url or 'armage.php' in url:
                try:
                        url = 'http://www.putlocker.com/embed/' + id_video
                        print url
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Putlocker)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "nowvideo" in url:
                try:
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Nowvideo)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "primeshare" in url:
                try:
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Primeshare.tv)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "videoslasher" in url:
                try:
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](VideoSlasher)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "sockshare" in url:
                try:
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Sockshare)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "flashx.tv" in url:
                try:
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](FlashX.tv)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "flashxtv" in url:
                try:
                        url = 'http://flashx.tv/video/' + id_video
                        print url
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](FlashX.tv)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "video.tt" in url:
                try:
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Video.tt)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	return

   
	
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

	
def ARM_abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

#----------------------------------------------------------------------------------------------------------------------------------------------#
              
def ARM_get_params():
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
	
params=ARM_get_params()
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


