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

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'


#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#



def MVT_MenuPrincipal(artfolder):
        addDir1('[B][COLOR green]MOVIE[/COLOR][COLOR yellow]-[/COLOR][COLOR red]TUGA[/COLOR][/B]','','',artfolder + 'ze-MVT1.png',False,'')
        addDir1('','','',artfolder + 'ze-MVT1.png',False,'')
	addDir('[COLOR yellow]Menu Filmes[/COLOR]','url',105,artfolder + 'ze-MVT1.png','nao','')
	addDir('[COLOR yellow]Animação[/COLOR]','http://movie-tuga.blogspot.pt/search/label/animacao',102,artfolder + 'ze-MVT1.png','nao','')
        addDir1('','','',artfolder + 'ze-MVT1.png',False,'')
	addDir('Pesquisar','http://www.tuga-filmes.com/search?q=',1,artfolder + 'Ze-pesquisar1.png','nao','')
	#addDir('[COLOR brown]ChangeLog[/COLOR]','http://o-repositorio-maluco.googlecode.com/svn/trunk/changelogs/changelog_MovieTuga.txt',108,artfolder + 'ze-MVT1.png','nao','')

def MVT_Menu_Filmes(artfolder):
        addDir1('[B][COLOR blue]Menu Filmes[/COLOR][/B]','','',artfolder + 'ze-MVT1.png',False,'')
        addDir1('','','',artfolder + 'ze-MVT1.png',False,'')
	addDir('[COLOR yellow]Ver Todos[/COLOR]','http://movie-tuga.blogspot.pt/',102,artfolder + 'ze-MVT1.png','nao','')
	addDir('[COLOR yellow]Categorias[/COLOR]','url',106,artfolder + 'ze-MVT1.png','nao','')
        addDir1('','','',artfolder + 'ze-MVT1.png',False,'')
	addDir('Pesquisar','http://www.tuga-filmes.com/search?q=',1,artfolder + 'Ze-pesquisar1.png','nao','')

def MVT_Menu_Filmes_Por_Categorias(artfolder):
        url_categorias = 'http://www.movie-tuga.blogspot.pt/'
        html_categorias_source = MVT_abrir_url(url_categorias)
        addDir1('[B][COLOR blue]Categorias[/COLOR][/B]','','',artfolder + 'ze-MVT1.png',False,'')
        addDir1('','','',artfolder + 'ze-MVT11.png',False,'')
	html_items_categorias = re.findall("<div id=\'menu-categorias\'>(.*?)</div>", html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<a href=\'(.+?)\' title=\'.+?\'>(.+?)</a>").findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        addDir('[COLOR yellow]' + nome_categoria + '[/COLOR]',endereco_categoria + '?&max-results=15',102,artfolder + 'ze-MVT1.png','nao','')



#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#

		

def MVT_encontrar_fontes_filmes(url):
        try:
		html_source = MVT_abrir_url(url)
	except: html_source = ''
	items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        url = re.compile('<div class="btns"><a href="(.+?)" target="Player">').findall(item)
                        if 'http' not in url[0]:
                                url[0] = 'http:' + url[0] 
                        titulo = re.compile("<strong>T\xc3\xadtulo original:</strong>(.+?)</div>").findall(item)
                        if 'Qualidade:' in item:
                                qualidade = re.compile("<strong>Qualidade:</strong>(.+?)</div>").findall(item)
                                qualidade_filme = qualidade[0].replace('&#8211;',"-")
                        else:
                                qualidade_filme = ''
                        ano = re.compile('<strong>Lan\xc3\xa7amento:</strong>(.+?)</div>').findall(item)
                        thumbnail = re.compile('src="(.+?)"').findall(item)
                        print url,thumbnail
                        if 'http' not in thumbnail[0]: thumbnail[0] = 'http:' + thumbnail[0]
                        titulo[0] = titulo[0].replace('&#8217;',"'")
                        titulo[0] = titulo[0].replace('&#8211;',"-")
                        if 'Dear John' in titulo[0] and ano[0] == '2013': titulo[0] = titulo[0].replace('Dear John','12 Anos Escravo')
                        try:
                                addDir('[B][COLOR green]' + titulo[0] + ' [/COLOR][/B][COLOR yellow](' + ano[0] + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',url[0],103,thumbnail[0].replace('s72-c','s320'),'','')
                        except: pass
	proxima = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
	try:
                proxima_p = proxima[0].replace('%3A',':')
                addDir1('','','','',False,'')
		addDir("[B]Página Seguinte >>[/B]",proxima_p.replace('&amp;','&'),102,"",'','')
	except: pass



#----------------------------------------------------------------------------------------------------------------------------------------------#

def MVT_encontrar_videos_filmes(name,url):
        colecao = 'nao'
        addDir1(name,'','',iconimage,False,'')
        addDir1('','','',iconimage,False,'')
        conta_id_video = 0
        try:
                fonte_video = MVT_abrir_url(url)
        except: fonte_video = ''
        fontes_video = re.findall("<body>(.+?)</body>", fonte_video, re.DOTALL)
        #addDir(fontes_video[0],url,1,iconimage,'','')
        numero_de_fontes = len(fontes_video)
        for fonte_e_url in fontes_video:
                #parameters = {"nome_texto" : name, "url": url, "addonid": 'MVT'}
                #nome_textbox = urllib.urlencode(parameters)
                #addDir('[COLOR blue]Sinopse[/COLOR]'+url,nome_textbox,109,iconimage,'nao','')
                #addDir(str(len(fontes_video)),url,1,iconimage,'','')
                match = re.compile('<option value=(.+?)>(.+?)<').findall(fonte_e_url)
                #addDir(str(len(match)),url,1,iconimage,'','')
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
                                                #addDir1('[COLOR blue]' + cd + '[/COLOR]','','',iconimage,False,'')
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
                                #addDir(url_video,url,1,iconimage,'','')
                                try:
                                        fonte = MVT_abrir_url(url_video)
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
                                                        match = re.compile('<iframe .+? src="//vidto.me/embed-(.+?)-755x390.html" .+?</iframe>').findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        id_video = match[0]
                                                        url = 'http://vidto.me/' + id_video + '.html' + '///' + name
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,100,iconimage,'','')
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
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,100,iconimage,'','')
                                                except:pass
                                        if 'vidto' in fonte_id:
                                                try:
                                                        match = re.compile('<iframe .+? src="//vidto.me/embed-(.+?)-755x390.html" .+?</iframe>').findall(fonte_id)
                                                        conta_id_video = conta_id_video + 1
                                                        id_video = match[0]
                                                        url = 'http://vidto.me/' + id_video + '.html' + '///' + name
                                                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,100,iconimage,'','')
                                                except:pass



#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#


	
def MVT_abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

#----------------------------------------------------------------------------------------------------------------------------------------------#
              
def MVT_get_params():
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
        


#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#


          
params=MVT_get_params()
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


