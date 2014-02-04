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
import MovieTuga,TugaFilmesTV,TugaFilmesCom,M18,Pesquisar,Play,TextBoxes,TopPt,FilmesAnima,Filmes,Series
from array import array
from string import capwords


addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

arr_series1 = [['' for i in range(87)] for j in range(1)]
arr_series = ['' for i in range(87)]
 
mensagemok = xbmcgui.Dialog().ok


#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENU    ------------------------------------------------------------------#

def MAIN_MENU():
        addDir1('[B][COLOR blue]Menu Principal[/COLOR][/B]','',31,artfolder + 'MPrin.png',False,'')
        addDir1('','','',artfolder + 'ze-icon3.png',False,'')
        addDir('[B][COLOR green]Fi[/COLOR][COLOR yellow]l[/COLOR][COLOR red]mes[/COLOR][/B]','http://www.tuga-filmes.com/',25,'','nao','')
        addDir('[B][COLOR green]Sé[/COLOR][COLOR yellow]r[/COLOR][COLOR red]ies[/COLOR][/B]','http://www.tuga-filmes.tv',26,'','nao','')
        addDir('[B][COLOR green]Ani[/COLOR][COLOR yellow]m[/COLOR][COLOR red]ação[/COLOR][/B]','http://www.tuga-filmes.com/search/label/Anima%C3%A7%C3%A3o?max-results=20',6,'','nao','')
        #addDir('[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.com[/COLOR][/B]','http://direct',231,artfolder + 'Ze-mv1.png','nao','')	
        addDir1('','','',artfolder + 'ze-icon3.png',False,'')
        addDir('[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv','http://direct',31,artfolder + 'Ze-tv1.png','nao','')
        addDir('[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].com','http://direct',71,artfolder + 'Ze-tc1.png','nao','')
        addDir('[B][COLOR green]MOVIE[/COLOR][COLOR yellow]-[/COLOR][COLOR red]TUGA[/COLOR][/B]','http://direct',101,artfolder + 'Ze-mv1.png','nao','')
        addDir('[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.com[/COLOR][/B]','http://direct',231,'','nao','')
        addDir1('','','',artfolder + 'ze-icon3.png',False,'')
	addDir('Pesquisar','url',1,artfolder + 'Ze-pesquisar1.png','nao','')
	


def Filmes_IMDB_antiga(url):
        sim='sim'
        #nome_filme_IMDB = 'croods'
	#Filmes.FILMES_pesquisar(nome_filme_IMDB)
        url = 'http://www.imdb.com/genre/animation/?ref_=gnr_mn_an_mp'
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall('<td class="image">(.+?)<td class="title">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        
			nomethumb_IMDB = re.compile('<a href=".+?" title="(.+?)"><img src="(.+?)"').findall(item)
			nome_filme_IMDB = nomethumb_IMDB[0][0]
			#nome_filme_IMDB = 'croods'
			#passar_nome_pesquisa(nome_filme_IMDB)
			addDir(nome_filme_IMDB,'url',7,nomethumb_IMDB[0][1],'nao','')

def Filmes_Filmes(url):
        #url_toppt = 'http://toppt.net/'
        #toppt_source = abrir_url(url_toppt)
        #saber_url_animacao = re.compile('<a href="(.+?)">Animacao</a></li>').findall(toppt_source)
        #url = saber_url_animacao[0]
        #url = 'http://www.tuga-filmes.com/search/label/Anima%C3%A7%C3%A3o?max-results=20'
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        urletitulo = re.compile("<a href=\'(.+?)\' title=\'(.+?)\'>").findall(item)
                        thumbnail = re.compile('<img alt="" border="0" src="(.+?)"').findall(item)
                        qualidade_ano = re.compile('<b>VERS\xc3\x83O:.+?</b><span style="font-size: x-small;">(.+?)<').findall(item)
                        if qualidade_ano != []:
                                for q_a in qualidade_ano:
                                        #addDir1(q_a,'','','',False,'')
                                        a_q = re.compile('\d+')
                                        qq_aa = a_q.findall(q_a)
                                        for q_a_q_a in qq_aa:
                                                if len(q_a_q_a) == 4:
                                                        ano = ' ('+ q_a_q_a + ')'
                                                else: ano = ''
                        print urletitulo,thumbnail
                        nome = urletitulo[0][1] + ano
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('(PT-PT)',"")
                        nome = nome.replace('(PT/PT)',"")
                        nome = nome.replace('[PT-PT]',"")
                        nome = nome.replace('[PT/PT]',"")
                        nome = nome.replace('['," ")
                        nome = nome.replace(']'," ")
                        addDir(nome,'url',8,thumbnail[0],'nao','')
        else:
                return
        proxima = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
	try:
                addDir1('','','','',False,'')
		addDir("[COLOR yellow]Página Seguinte >>[/COLOR]",proxima[0].replace('&amp;','&'),25,"",'','')
	except: pass

def Series_Series(url):
	html_series_source = abrir_url(url)
	html_items_series = re.findall("<div class=\'widget Label\' id=\'Label3\'>\n<h2>S\xc3\xa9ries(.*?)<div class=\'clear\'>", html_series_source, re.DOTALL)
        print len(html_items_series)
        i=0
        for item_series in html_items_series:
                series = re.compile("<a dir=\'ltr\' href=\'(.+?)\'>(.+?)</a>").findall(item_series)
                for endereco_series,nome_series in series:
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        nome_series = nome_series.replace('&#8217;',"'")
                        nome_series = nome_series.replace('&#8230;',"...")
                        if nome_series != 'Agents of S.H.I.E.L.D': arr_series[i]=nome_series
                        #arr_series[6][1]=endereco_series
                        #addDir(nome_series,endereco_series,47,artfolder + 'ze-TFV1.png','nao','')
                        i=i+1
        url = 'http://toppt.net/'
        html_series_source = abrir_url(url)
	html_items_series = re.findall('<h1 class="widget-title">SERIES</h1>(.+?)</div></aside>', html_series_source, re.DOTALL)
        print len(html_items_series)
        for item_series in html_items_series:
                series = re.compile('<a href="(.+?)">(.+?)</a>').findall(item_series)
                for endereco_series,nome_series in series:
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        nome_series = nome_series.replace('&#8217;',"'")
                        nome_series = nome_series.replace('&#8230;',"...")
                        if nome_series not in arr_series:
                                arr_series.append(nome_series)
        arr_series.sort(key = lambda k : k.lower())
        addDir1('[B][COLOR blue]Séries[/COLOR][/B] (' + str(len(arr_series)) + ')','','',artfolder + 'ze-TFV1.png',False,'')
        addDir1('','','',artfolder + 'ze-TFV1.png',False,'')
        for x in range(len(arr_series)):
                if arr_series[x] != '': addDir(arr_series[x],'url',9,artfolder + 'ze-TFV1.png','nao','')
 


def Filmes_Animacao(url):
        #url_toppt = 'http://toppt.net/'
        #toppt_source = abrir_url(url_toppt)
        #saber_url_animacao = re.compile('<a href="(.+?)">Animacao</a></li>').findall(toppt_source)
        #url = saber_url_animacao[0]
        #url = 'http://www.tuga-filmes.com/search/label/Anima%C3%A7%C3%A3o?max-results=20'
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        urletitulo = re.compile("<a href=\'(.+?)\' title=\'(.+?)\'>").findall(item)
                        thumbnail = re.compile('<img alt="" border="0" src="(.+?)"').findall(item)
                        qualidade_ano = re.compile('<b>VERS\xc3\x83O:.+?</b><span style="font-size: x-small;">(.+?)<').findall(item)
                        if qualidade_ano != []:
                                for q_a in qualidade_ano:
                                        #addDir1(q_a,'','','',False,'')
                                        a_q = re.compile('\d+')
                                        qq_aa = a_q.findall(q_a)
                                        for q_a_q_a in qq_aa:
                                                if len(q_a_q_a) == 4:
                                                        ano = ' ('+ q_a_q_a + ')'
                                                else: ano = ''
                        print urletitulo,thumbnail
                        nome = urletitulo[0][1] + ano
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('(PT-PT)',"")
                        nome = nome.replace('(PT/PT)',"")
                        nome = nome.replace('[PT-PT]',"")
                        nome = nome.replace('[PT/PT]',"")
                        nome = nome.replace('['," ")
                        nome = nome.replace(']'," ")
                        addDir(nome,'url',7,thumbnail[0],'nao','')
        else:
                return
        proxima = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
	try:
                addDir1('','','','',False,'')
		addDir("[COLOR yellow]Página Seguinte >>[/COLOR]",proxima[0].replace('&amp;','&'),6,"",'','')
	except: pass



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
elif mode ==  6: Filmes_Animacao(url)
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
elif mode == 25: Filmes_Filmes(url)
elif mode == 26: Series_Series(url)
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
elif mode == 236: TopPt.TPT_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,nome_fonte_video)
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


xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
