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



def TBOX_TextBoxes_ChangeLog(url):
        texto = ''
        try:
                texto_url = TBOX_abrir_url(url)
        except: texto_url = ''
        texto_items = re.compile('>(.+?)<').findall(texto_url)
        if texto_items != []:
                for linhas in texto_items:
                        texto = texto + linhas + '\n'
        texto = texto.replace('bbbbb','\n')
	texto = texto.replace('\xe7','ç')
	texto = texto.replace('\xf5','õ')	
	texto = texto.replace('\xe3','ã')		
	class TextBox():
		"""Thanks to BSTRDMKR for this code:)"""
		# constants
		WINDOW = 10147		
		CONTROL_LABEL = 1
		CONTROL_TEXTBOX = 5
		
		def __init__( self, *args, **kwargs):
			# activate the text viewer window
			xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
			# get window
			self.win = xbmcgui.Window( self.WINDOW )
			# give window time to initialize
			xbmc.sleep( 500 )
			self.setControls()

		def setControls( self ):
			# set heading
			self.win.getControl( self.CONTROL_LABEL ).setLabel('[COLOR brown]ChangeLog: [/COLOR][B][COLOR green]MOVIE[/COLOR][COLOR yellow]-[/COLOR][COLOR red]TUGA[/COLOR][/B]')
			self.win.getControl( self.CONTROL_TEXTBOX ).setText(texto)
			return
	TextBox()


def TBOX_TextBoxes_Sinopse(url):
        unquote_texto = urllib.unquote(url)
        print unquote_texto
        url_e_label = re.compile('url=(.+?)&nome_texto=[[].+?[]][[].+?[]](.+?)[[].+?[]][[].+?[]][[].+?[]](.+?)[[].+?[]][[].+?[]](.+?)[[].+?[]]').findall(unquote_texto)
        url_sinopse = url_e_label[0][0]
        label = '[B][COLOR green]' + url_e_label[0][1].replace('+',' ') + '[/COLOR][/B][COLOR yellow]' + url_e_label[0][2].replace('+',' ') + '[/COLOR][COLOR red]' + url_e_label[0][3].replace('+',' ') + '[/COLOR]'
        try:
                Sinopse_url = TBOX_abrir_url(url_sinopse)
        except: Sinopse_url = ''
        addDir1(url_e_label[0][0],'','',iconimage,False,'')
        if 'Resumo' in Sinopse_url: resumo = re.compile('<b>Resumo</b>:(.+?)<br />').findall(Sinopse_url)
        #if 'imgsinopse' in Sinopse_url: resumo = re.compile("<div id=\'imgsinopse\'>(.+?)</div>").findall(Sinopse_url)
        if resumo:
                texto = resumo[0]
                texto = texto.replace('&#8220;','"')
                texto = texto.replace('&#8221;','"')
                texto = texto.replace('&#8211;','-')	
                #texto = texto.replace('\xe3','ã')
        else:
                return
	class TextBox():
		"""Thanks to BSTRDMKR for this code:)"""
		# constants
		WINDOW = 10147		
		CONTROL_LABEL = 1
		CONTROL_TEXTBOX = 5
		
		def __init__( self, *args, **kwargs):
			# activate the text viewer window
			xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
			# get window
			self.win = xbmcgui.Window( self.WINDOW )
			# give window time to initialize
			xbmc.sleep( 500 )
			self.setControls()

		def setControls( self ):
			# set heading
			self.win.getControl( self.CONTROL_LABEL ).setLabel(label)
			self.win.getControl( self.CONTROL_TEXTBOX ).setText('\n\n\n\n[B][COLOR blue]Sinopse: [/COLOR][/B]' + texto)
			return
	TextBox()




#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#


	
def TBOX_abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

#----------------------------------------------------------------------------------------------------------------------------------------------#
              
def TBOX_get_params():
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
	liz.setProperty('fanart_image',artfolder + 'Wall.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir1(name,url,mode,iconimage,folder,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'Wall.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
        return ok



#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#


          
params=TBOX_get_params()
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


