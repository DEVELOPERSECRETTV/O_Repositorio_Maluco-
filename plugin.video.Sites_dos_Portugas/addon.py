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



import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,urlresolver
import MovieTuga,TugaFilmesTV,TugaFilmesCom,M18,Pesquisar,Play,TextBoxes


addon_id = 'plugin.video.Filmes_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

 
mensagemok = xbmcgui.Dialog().ok


#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENU    ------------------------------------------------------------------#

def MAIN_MENU():
        addDir1('[B][COLOR blue]Menu Principal[/COLOR][/B]','',31,artfolder + 'MPrin.png',False,'')
        addDir1('','','',artfolder + 'ze-icon3.png',False,'')
        addDir('[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv','http://direct',31,artfolder + 'Ze-tv1.png','nao','')
        addDir('[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].com','http://direct',71,artfolder + 'Ze-tc1.png','nao','')
        addDir('[B][COLOR green]MOVIE[/COLOR][COLOR yellow]-[/COLOR][COLOR red]TUGA[/COLOR][/B]','http://direct',101,artfolder + 'Ze-mv1.png','nao','')		
        addDir1('','','',artfolder + 'ze-icon3.png',False,'')
	addDir('Pesquisar','http://www.tuga-filmes.tv/search?q=',1,artfolder + 'Ze-pesquisar1.png','nao','')
	


def get_params():
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
#----------------------------------------------------------------------------------------------------------------------------------------------#

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def addLink(name,url,iconimage):
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
        
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
          
params=get_params()
url=None
name=None
mode=None
checker=None
iconimage=None
fanart=None

try: url=urllib.unquote_plus(params["url"])
except: pass

try: name=urllib.unquote_plus(params["name"])
except: pass

try: mode=int(params["mode"])
except: pass

try: checker=urllib.unquote_plus(params["checker"])
except: pass

try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

try: fanart=urllib.unquote_plus(params["fanart"])
except: pass

#print "Mode: "+str(mode)
#print "URL: "+str(url)
#print "Name: "+str(name)
#print "Checker: "+str(checker)
#print "Iconimage: "+str(iconimage)

if mode==None or url==None or len(url)<1: MAIN_MENU()
elif mode ==  1: Pesquisar.pesquisar()
elif mode ==  2: Pesquisar.encontrar_fontes_pesquisa_TFV(url,pesquisou)
elif mode ==  3: Pesquisar.encontrar_fontes_filmes_TFC(url_pesquisa)
elif mode ==  4: Pesquisar.encontrar_fontes_pesquisa_MVT(url)
#----------------------------------------------  Tuga-Filmes.tv  ----------------------------------------------------
elif mode == 30: print ""; Play.PLAY_movie(url,name,iconimage,checker,fanart)
elif mode == 31: TugaFilmesTV.TFV_MenuPrincipal(artfolder)
elif mode == 32: TugaFilmesTV.TFV_encontrar_fontes_filmes(url,artfolder)
elif mode == 33: TugaFilmesTV.TFV_encontrar_videos_filmes(name,url)
elif mode == 34: TugaFilmesTV.TFV_pesquisar()
elif mode == 35: TugaFilmesTV.TFV_resolve_videomega_filmes(url,conta_id_video)
elif mode == 36: TugaFilmesTV.TFV_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,nome_fonte_video)
elif mode == 37: TugaFilmesTV.TFV_Menu_Filmes(artfolder)
elif mode == 38: TugaFilmesTV.TFV_Menu_Filmes_Por_Categorias(artfolder)
elif mode == 39: TugaFilmesTV.TFV_Menu_Filmes_Por_Ano(artfolder)
elif mode == 40: TugaFilmesTV.TFV_Menu_Series(artfolder)
elif mode == 41: TugaFilmesTV.TFV_Menu_Series_A_a_Z(artfolder)
elif mode == 42: TugaFilmesTV.TFV_encontrar_videos_series(name,url)
elif mode == 43: TugaFilmesTV.TFV_resolve_not_videomega_series(name,url,id_video,nome_cada_episodio,src_href)
elif mode == 44: TugaFilmesTV.TFV_encontrar_fontes_series_recentes(url)
elif mode == 45: TugaFilmesTV.TFV_pesquisar_series()
elif mode == 46: TugaFilmesTV.TFV_encontrar_fontes_pesquisa(url,pesquisou)
elif mode == 47: TugaFilmesTV.TFV_encontrar_fontes_series_A_a_Z(url)
elif mode == 48: TugaFilmesTV.TFV_Menu_Filmes_Top_5(artfolder)
elif mode == 49: M18.M18_TFV_Menu_M18(artfolder)
elif mode == 50: M18.M18_TFV_Menu_M18_Categorias(artfolder)
elif mode == 51: M18.M18_TFV_Menu_M18_30_Recentes(artfolder)
elif mode == 52: M18.M18_TFV_encontrar_fontes_M18(url)
elif mode == 53: M18.M18_TFV_encontrar_videos_M18(name,url)
elif mode == 54: M18.M18_TFV_pesquisar_M18()
elif mode == 55: M18.M18_TFV_encontrar_fontes_pesquisa_M18(url,pesquisou)
elif mode == 56: TextBoxes.TBOX_TextBoxes_ChangeLog(url)
elif mode == 57: TextBoxes.TBOX_TextBoxes_Sinopse(url)
#----------------------------------------------  Tuga-Filmes.com  --------------------------------------------------
elif mode == 70: print "", Play.PLAY_movie(url,name,iconimage,checker,fanart)
elif mode == 71: TugaFilmesCom.TFC_MenuPrincipal(artfolder)
elif mode == 72: TugaFilmesCom.TFC_encontrar_fontes_filmes(url)
elif mode == 73: TugaFilmesCom.TFC_encontrar_videos_filmes(name,url)
elif mode == 74: TugaFilmesCom.TFC_pesquisar_filmes()
elif mode == 75: TugaFilmesCom.TFC_resolve_videomega_filmes(url,conta_id_video)
elif mode == 76: TugaFilmesCom.TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,nome_fonte_video)
elif mode == 77: TugaFilmesCom.TFC_Menu_Filmes(artfolder)
elif mode == 78: TugaFilmesCom.TFC_Menu_Filmes_Por_Categorias(artfolder)
elif mode == 79: TugaFilmesCom.TFC_Menu_Filmes_Top_10(artfolder)
elif mode == 80: TugaFilmesCom.TFC_Menu_Series(artfolder)
elif mode == 81: TugaFilmesCom.TFC_Menu_Filmes_Brevemente(artfolder)
elif mode == 82: M18.M18_TFC_encontrar_videos_M18(name,url)
elif mode == 83: M18.M18_TFC_resolve_not_videomega_M18(name,url,id_video,conta_id_video,nome_fonte_video)
elif mode == 84: M18.M18_TFC_encontrar_fontes_M18(url)
elif mode == 85: M18.M18_TFC_pesquisar_M18()
elif mode == 86: M18.M18_TFC_Link_M18(artfolder)
elif mode == 87: M18.M18_TFC_Menu_M18(url,artfolder)
elif mode == 88: TextBoxes.TBOX_TextBoxes_ChangeLog(url)
elif mode == 89: TextBoxes.TBOX_TextBoxes_Sinopse(url)
#----------------------------------------------  MOVIETUGA  -------------------------------------------------------
elif mode == 100: print ""; Play.PLAY_movie(url,name,iconimage,checker,fanart)
elif mode == 101: MovieTuga.MVT_MenuPrincipal(artfolder)
elif mode == 102: MovieTuga.MVT_encontrar_fontes_filmes(url)
elif mode == 103: MovieTuga.MVT_encontrar_videos_filmes(name,url)
elif mode == 104: MovieTuga.MVT_pesquisar_filmes()
elif mode == 105: MovieTuga.MVT_Menu_Filmes(artfolder)
elif mode == 106: MovieTuga.MVT_Menu_Filmes_Por_Categorias(artfolder)
elif mode == 107: MovieTuga.MVT_Menu_Filmes_Brevemente(artfolder)
elif mode == 108: TextBoxes.TBOX_TextBoxes_ChangeLog(url)
elif mode == 109: TextBoxes.TBOX_TextBoxes_Sinopse(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
