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



def FILMES3D_MenuPrincipal(artfolder):
        addDir1('[B][COLOR green]Filmes[/COLOR][COLOR yellow]3D[/COLOR][COLOR red]cinema[/COLOR][/B]','','',artfolder + 'ze-MVT1.png',False,'')
        addDir1('','','',artfolder + 'ze-MVT1.png',False,'')
	addDir('[COLOR yellow]Menu Filmes[/COLOR]','url',405,artfolder + 'ze-MVT1.png','nao','')
	addDir('[COLOR yellow]Animação[/COLOR]','http://filmes3dcinema.blogspot.pt/search/label/Anima%C3%A7%C3%A3o',402,artfolder + 'ze-MVT1.png','nao','')
        addDir1('','','',artfolder + 'ze-MVT1.png',False,'')
	addDir('Pesquisar','http://filmes3dcinema.blogspot.pt/search?q=',1,artfolder + 'Ze-pesquisar1.png','nao','')
	#addDir('[COLOR brown]ChangeLog[/COLOR]','http://o-repositorio-maluco.googlecode.com/svn/trunk/changelogs/changelog_MovieTuga.txt',108,artfolder + 'ze-MVT1.png','nao','')

def FILMES3D_Menu_Filmes(artfolder):
        addDir1('[B][COLOR blue]Menu Filmes[/COLOR][/B]','','',artfolder + 'ze-MVT1.png',False,'')
        addDir1('','','',artfolder + 'ze-MVT1.png',False,'')
	addDir('[COLOR yellow]Recentes[/COLOR]','http://filmes3dcinema.blogspot.pt/',402,artfolder + 'ze-MVT1.png','nao','')
	addDir('[COLOR yellow]Categorias[/COLOR]','url',406,artfolder + 'ze-MVT1.png','nao','')
        addDir1('','','',artfolder + 'ze-MVT1.png',False,'')
	addDir('Pesquisar','http://www.tuga-filmes.com/search?q=',1,artfolder + 'Ze-pesquisar1.png','nao','')

def FILMES3D_Menu_Filmes_Por_Categorias(artfolder):
        url_categorias = 'http://www.movie-tuga.blogspot.pt/'
        html_categorias_source = FILMES3D_abrir_url(url_categorias)
        addDir1('[B][COLOR blue]Categorias[/COLOR][/B]','','',artfolder + 'ze-MVT1.png',False,'')
        addDir1('','','',artfolder + 'ze-MVT11.png',False,'')
	html_items_categorias = re.findall("<div id=\'menu-categorias\'>(.*?)</div>", html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<a href=\'(.+?)\' title=\'.+?\'>(.+?)</a>").findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        addDir('[COLOR yellow]' + nome_categoria + '[/COLOR]',endereco_categoria + '?&max-results=15',402,artfolder + 'ze-MVT1.png','nao','')



#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#

		

def FILMES3D_encontrar_fontes_filmes(url):
        try:
		html_source = FILMES3D_abrir_url(url)
	except: html_source = ''
	items = re.findall("<div class=\'post hentry\'>(.*?)<div class=\'summary\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        linkvideo = re.compile("<a href=\'(.+?)\'>(.+?)</a>").findall(item)
                        titulo = linkvideo[0][1]
                        linkv = linkvideo[0][0]
                        thumbnail = re.compile('sompret_image_creator[(]"(.+?)",').findall(item)
                        print linkv,thumbnail
                        titulo = titulo.replace('&#8217;',"'")
                        titulo = titulo.replace('&#8211;',"-")
                        try:
                                addDir('[B][COLOR green]' + titulo + ' [/COLOR][/B]',linkv,403,thumbnail[0].replace('s72-c','w260'),'','')
                        except: pass
	proxima = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
	try:
                proxima_p = proxima[0].replace('%3A',':')
                addDir1('','','','',False,'')
		addDir("[B]Página Seguinte >>[/B]",proxima_p.replace('&amp;','&'),402,"",'','')
	except: pass



#----------------------------------------------------------------------------------------------------------------------------------------------#

def FILMES3D_encontrar_videos_filmes(name,url):
        addDir1(name,'','',iconimage,False,'')
        addDir1('','','',iconimage,False,'')
        num_fonte = 0
        try:
                fonte_video = FILMES3D_abrir_url(url)
        except: fonte_video = ''
        fontes_video = re.findall("<iframe(.+?)</iframe>", fonte_video, re.DOTALL)
        addDir(str(len(fontes_video)),url,1,iconimage,'','')
        #<iframe height="385" src="https://docs.google.com/file/d/0B6fdYHGIUr6pcEd5ZjYtNG1WQXM/preview" width="500"></iframe>
        for fonte_e_url in fontes_video:
                matchvideo = re.compile('src="(.+?)"').findall(fonte_e_url)
                if matchvideo: url = matchvideo[0]
                if 'docs.google' in url:                        
                        try:
                                num_fonte = num_fonte + 1
                                url = url + '///' + name
                                addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](VK)[/COLOR][/B]',url,30,iconimage,'','')
                        except: pass



#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#


	
def FILMES3D_abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

#----------------------------------------------------------------------------------------------------------------------------------------------#
              
def FILMES3D_get_params():
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


          
params=FILMES3D_get_params()
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


