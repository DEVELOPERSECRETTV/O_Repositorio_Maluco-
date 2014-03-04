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



import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,urlresolver,urlparse
import MovieTuga,TugaFilmesTV,TugaFilmesCom,M18,Pesquisar,Play,TextBoxes,TopPt,FilmesAnima,Filmes,Series,Mashup,Armagedom
from array import array
from string import capwords
import xbmcvfs


addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

arr_series1 = [['' for i in range(87)] for j in range(1)]
arr_series = ['' for i in range(100)]
arr_filmes = ['' for i in range(100)]
arrai_filmes = ['' for i in range(100)]
thumb_filmes = ['' for i in range(100)]
arr_filmes[4] = '6'
i=arr_filmes[4]


arr_filmes_animacao = ['' for i in range(100)]
arrai_filmes_animacao  = ['' for i in range(100)]
thumb_filmes_animacao  = ['' for i in range(100)]




mensagemok = xbmcgui.Dialog().ok


#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENU    ------------------------------------------------------------------#

def MAIN_MENU():
        #xbmc.executebuiltin("Container.SetViewMode(503)")
        url_TFV = 'http://www.tuga-filmes.tv/search/label/Filmes'
        url_TFC = 'http://www.tuga-filmes.com'
        url_MVT = 'http://www.movie-tuga.blogspot.pt'
        url_TPT = 'http://toppt.net/?cat=68'
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "fim": 'fim',"xpto":'xpto'}
        url_filmes_filmes = urllib.urlencode(parameters)
        addDir1('[B][COLOR blue]Menu Principal[/COLOR][/B]','',31,artfolder + 'MPrin.png',False,'')
        addDir1('','','',artfolder + 'ze-icon3.png',False,'')
        addDir('[B][COLOR green]Fi[/COLOR][COLOR yellow]l[/COLOR][COLOR red]mes[/COLOR][/B]',url_filmes_filmes,507,'','nao','')
        addDir('[B][COLOR green]Sé[/COLOR][COLOR yellow]r[/COLOR][COLOR red]ies[/COLOR][/B]','http://www.tuga-filmes.tv',26,'','nao','')
        url_TFV = 'http://www.tuga-filmes.tv/search/label/Anima%C3%A7%C3%A3o'
        url_TFC = 'http://www.tuga-filmes.com/search/label/Anima%C3%A7%C3%A3o?max-results=20'
        url_MVT = 'http://movie-tuga.blogspot.pt/search/label/animacao'
        url_TPT = 'http://toppt.net/?cat=24'
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "fim": 'fim',"xpto":'xpto'}
        url_filmes_animacao = urllib.urlencode(parameters)
        addDir('[B][COLOR green]Ani[/COLOR][COLOR yellow]m[/COLOR][COLOR red]ação[/COLOR][/B]',url_filmes_animacao,6,'','nao','')
        #addDir('[B][COLOR cyan]IMDB[/COLOR][/B]','url',500,'','nao','')
        addDir1('','','',artfolder + 'ze-icon3.png',False,'')
        addDir('[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv','http://direct',31,artfolder + 'Ze-tv1.png','nao','')
        addDir('[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].com','http://direct',71,artfolder + 'Ze-tc1.png','nao','')
        addDir('[B][COLOR green]MOVIE[/COLOR][COLOR yellow]-[/COLOR][COLOR red]TUGA[/COLOR][/B]','http://direct',101,artfolder + 'Ze-mv1.png','nao','')
        addDir('[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.com[/COLOR][/B]','http://direct',231,'','nao','')
        #addDir1('','','',artfolder + 'ze-icon3.png',False,'')
        addDir('[B][COLOR yellow]SITES[/COLOR][COLOR blue]dos[/COLOR][COLOR green]BRAZUCAS[/COLOR][/B]','url',331,'','nao','')
        addDir1('','','',artfolder + 'ze-icon3.png',False,'')
        addDir('Pesquisar','http://www.tuga-filmes.tv/search?q=',1,artfolder + 'Ze-pesquisar1.png','nao','')


def Menu_IMDB():        
        addDir('[B][COLOR green]Fi[/COLOR][COLOR yellow]l[/COLOR][COLOR red]mes[/COLOR][/B]','url',25,'','nao','')
        addDir('[B][COLOR green]Sé[/COLOR][COLOR yellow]r[/COLOR][COLOR red]ies[/COLOR][/B]','url',26,'','nao','')
        addDir('[B][COLOR green]Ani[/COLOR][COLOR yellow]m[/COLOR][COLOR red]ação[/COLOR][/B]','url',501,'','nao','')



def Filmes_IMDB_antiga(url):
        sim='sim'
        #nome_filme_IMDB = 'croods'
	#Filmes.FILMES_pesquisar(nome_filme_IMDB)
        url = 'http://www.imdb.com/search/title?at=0&genres=animation&sort=moviemeter&title_type=feature'
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall('<td class="image">(.+?)<td class="title">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
			nomethumb_IMDB = re.compile('<a href=".+?" title="(.+?)"><img src="(.+?)"').findall(item)
			nome_filme_IMDB = nomethumb_IMDB[0][0]
			nome_filme_IMDB = nome_filme_IMDB.replace('&#xF4;','ô')
			nome_filme_IMDB = nome_filme_IMDB.replace('&#xE3;','ã')
			nome_filme_IMDB = nome_filme_IMDB.replace('&#xE7;','ç')
			nome_filme_IMDB = nome_filme_IMDB.replace('&#xF3;','ó')
			nome_filme_IMDB = nome_filme_IMDB.replace('&#xC0;','À')
			nome_filme_IMDB = nome_filme_IMDB.replace('&#xE1;','á')
			nome_filme_IMDB = nome_filme_IMDB.replace('&#xF5;','õ')
			nome_filme_IMDB = nome_filme_IMDB.replace('&#xF3;','ó')
			#passar_nome_pesquisa(nome_filme_IMDB)
			addDir(nome_filme_IMDB,'url',7,nomethumb_IMDB[0][1],'nao','')



def passar_nome_pesquisa_animacao(name):
        nome_pesquisa = str(name)
        FilmesAnima.FILMES_ANIMACAO_pesquisar(str(nome_pesquisa))

def passar_nome_pesquisa_filmes(name):
        nome_pesquisa = str(name)
        Filmes.FILMES_pesquisar(str(nome_pesquisa))

def passar_nome_pesquisa_series(name):
        nome_pesquisa = str(name)
        Series.SERIES_pesquisar(str(nome_pesquisa))
        



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
elif mode ==  5: Pesquisar.encontrar_fontes_filmes_TPT(url_pesquisa)
elif mode ==  6: Mashup.Filmes_Animacao(url)
elif mode ==  7: passar_nome_pesquisa_animacao(name)
elif mode ==  8: passar_nome_pesquisa_filmes(name)
elif mode ==  9: passar_nome_pesquisa_series(name)
elif mode == 10: FilmesAnima.FILMES_ANIMACAO_pesquisar(nome_pesquisa)
elif mode == 11: FilmesAnima.FILMES_ANIMACAO_fontes_pesquisa_TFV(url,pesquisou)
elif mode == 12: FilmesAnima.FILMES_ANIMACAO_fontes_filmes_TFC(url_pesquisa)
elif mode == 13: FilmesAnima.FILMES_ANIMACAO_fontes_pesquisa_MVT(url)
elif mode == 14: FilmesAnima.FILMES_ANIMACAO_fontes_filmes_TPT(url_pesquisa)
elif mode == 20: Filmes.FILMES_pesquisar(nome_pesquisa)
elif mode == 21: Filmes.FILMES_fontes_pesquisa_TFV(url,pesquisou)
elif mode == 22: Filmes.FILMES_fontes_filmes_TFC(url_pesquisa)
elif mode == 23: Filmes.FILMES_fontes_pesquisa_MVT(url)
elif mode == 24: Filmes.FILMES_fontes_filmes_TPT(url_pesquisa)
elif mode == 25: Filmes_Filmes()
elif mode == 26: Mashup.Series_Series(url)
elif mode == 27: Series.SERIES_pesquisar(nome_pesquisa)
elif mode == 28: Series.SERIES_fontes_pesquisa_TFV(url,pesquisou)
elif mode == 29: Series.SERIES_fontes_TPT(url_pesquisa)
#elif mode==5: toppt.listar_texto(name,url)
#elif mode==7: toppt.play_movie(url,name,iconimage,checker,fanart)
#elif mode==16: toppt.top_pt_encontrar_categorias(name,url,siteurl,pornID)
#elif mode==19: toppt.top_pt_mainmenu(siteurl,filmesID,seriesID,animacaoID,pornID)
#elif mode==20: toppt.top_pt_encontrar_fontes(url)
#elif mode==21: toppt.top_pt_encontrar_videos(name,url)
#elif mode==22: toppt.top_pt_pesquisa(siteurl)
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
#-----------------------------------------------  Top-Pt.com  ------------------------------------------------------
#elif mode == 230: print ""; Play.PLAY_movie(url,name,iconimage,checker,fanart)
elif mode == 231: TopPt.TPT_MenuPrincipal(artfolder)
elif mode == 232: TopPt.TPT_encontrar_fontes_filmes(url,artfolder)
elif mode == 233: TopPt.TPT_encontrar_videos_filmes(name,url)
elif mode == 234: TopPt.TPT_pesquisar()
elif mode == 235: TopPt.TPT_resolve_videomega_filmes(url,conta_id_video)
elif mode == 236: TopPt.TPT_resolve_not_videomega_filmes(name,conta_id_video)
elif mode == 237: TopPt.TPT_Menu_Filmes(artfolder)
elif mode == 238: TopPt.TPT_Menu_Filmes_Por_Categorias(artfolder)
elif mode == 239: TopPt.TPT_Menu_Filmes_Por_Ano(artfolder)
elif mode == 240: TopPt.TPT_Menu_Series(artfolder)
elif mode == 241: TopPt.TPT_Menu_Series_A_a_Z(artfolder)
elif mode == 242: TopPt.TPT_encontrar_videos_series(name,url)
elif mode == 243: TopPt.TPT_resolve_not_videomega_series(name,url,id_video,nome_cada_episodio,src_href)
elif mode == 244: TopPt.TPT_encontrar_fontes_series_recentes(url)
elif mode == 245: TopPt.TPT_pesquisar_series()
elif mode == 246: TopPt.TPT_encontrar_fontes_pesquisa(url,pesquisou)
elif mode == 247: TopPt.TPT_encontrar_fontes_series_A_a_Z(url)
elif mode == 248: TopPt.TPT_Menu_Posts_Recentes(artfolder)
#elif mode == 249: M18.M18_TPT_Menu_M18(artfolder)
#elif mode == 250: M18.M18_TPT_Menu_M18_Categorias(artfolder)
#elif mode == 251: M18.M18_TPT_Menu_M18_30_Recentes(artfolder)
#elif mode == 252: M18.M18_TPT_encontrar_fontes_M18(url)
#elif mode == 253: M18.M18_TPT_encontrar_videos_M18(name,url)
#elif mode == 254: M18.M18_TPT_pesquisar_M18()
#elif mode == 255: M18.M18_TPT_encontrar_fontes_pesquisa_M18(url,pesquisou)
elif mode == 256: TextBoxes.TBOX_TextBoxes_ChangeLog(url)
elif mode == 257: TextBoxes.TBOX_TextBoxes_Sinopse(url)
#----------------------------------------------------------------ARMAGEDOM--------------------------------------------------------------------#
elif mode == 331: Armagedom.ARM_MenuPrincipal()
elif mode == 332: Armagedom.ARM_encontrar_fontes_filmes()
elif mode == 333: Armagedom.ARM_encontrar_videos_filmes(name,url)
elif mode == 334: Armagedom.ARM_pesquisar()
elif mode == 335: Armagedom.ARM_resolve_videomega_filmes(url,conta_id_video)
elif mode == 336: Armagedom.ARM_resolve_not_videomega_filmes(url,id_video,num_fonte)
elif mode == 337: Armagedom.ARM_Menu_Filmes()
elif mode == 338: Armagedom.ARM_Menu_Filmes_Por_Categorias()
elif mode == 339: Armagedom.ARM_Menu_Filmes_Por_Ano()
elif mode == 340: Armagedom.ARM_Menu_Series()
elif mode == 341: Armagedom.ARM_Menu_Series_A_a_Z()
elif mode == 342: Armagedom.ARM_encontrar_videos_series(name,url)
elif mode == 343: Armagedom.ARM_resolve_not_videomega_series(name,url,id_video,nome_cada_episodio,src_href)
elif mode == 344: Armagedom.ARM_encontrar_fontes_series_recentes(url)
elif mode == 345: Armagedom.ARM_pesquisar_series()
elif mode == 346: Armagedom.ARM_encontrar_fontes_pesquisa(url,pesquisou)
elif mode == 347: Armagedom.ARM_encontrar_fontes_series_A_a_Z(url)
elif mode == 348: Armagedom.ARM_Menu_Posts_Recentes(artfolder)
elif mode == 349: Armagedom.ARM_encontrar_fontes_filmes_MEGA()
elif mode == 350: Armagedom.ARM_encontrar_fontes_filmes_M18()
elif mode == 351: Armagedom.ARM_encontrar_fontes_filmes_MEGA_net()
elif mode == 352: Armagedom.ARM_Menu_Filmes_Por_Categorias_MEGA_net()
elif mode == 353: Armagedom.ARM_encontrar_fontes_series_MEGA_net()
#----------------------------------------------------------------   IMDB   --------------------------------------------------------------------#
elif mode == 500: Menu_IMDB()
elif mode == 501: Filmes_IMDB_antiga(url)
elif mode == 502: Filmes_Filmes_TFV(i)
elif mode == 503: Filmes_Filmes_TFC(i)
elif mode == 504: Filmes_Filmes_MVT(i)
elif mode == 505: Filmes_Filmes_TPT(i)
elif mode == 506: declara_variaveis(url)
elif mode == 507: Mashup.Filmes_Filmes_Filmes(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
