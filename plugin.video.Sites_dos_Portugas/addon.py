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




import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,urlparse,time,os
import MovieTuga,TugaFilmesTV,TugaFilmesCom,M18,Pesquisar,Play,TopPt,FilmesAnima,Mashup,Armagedom,FoitaTuga,Cinematuga
from array import array
from string import capwords
from Mashup import thetvdb_api,themoviedb_api,themoviedb_api_tv,theomapi_api,theomapi_api_nome

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENU    ------------------------------------------------------------------#

def MAIN_MENU():
        if selfAddon.getSetting("AvisoFanart") == "true":
                SdPpath = selfAddon.getAddonInfo('path')
                d = AvisoFanart("AvisoFanart.xml" , SdPpath, "Default")
                d.doModal()
                del d
                selfAddon.setSetting('AvisoFanart',value='false')
        #return
        #####################################
        url_TPT = 'http://toppt.net/'
        url_TFV = 'http://www.tuga-filmes.us/'
        url_TFC = 'http://www.tuga-filmes.info/'
        url_MVT = 'http://www.movie-tuga.blogspot.pt'
        url_FTT = 'http://foitatugacinemaonline.blogspot.pt/'
        url_CMT = 'http://www.tugafilmes.org'#'http://www.tugafilmes.org/'
        try:
		html_source = abrir_url(url_TFV)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []: TFV_ONOFF = '[COLOR green] | UP[/COLOR]'
	else: TFV_ONOFF = '[COLOR red] | DOWN[/COLOR]'
	try:
		html_source = abrir_url(url_TFC)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
	if items != []: TFC_ONOFF = '[COLOR green] | UP[/COLOR]'
	else: TFC_ONOFF = '[COLOR red] | DOWN[/COLOR]'
	try:
		html_source = abrir_url(url_MVT)
	except: html_source = ''
	items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
	if items != []: MVT_ONOFF = '[COLOR green] | UP[/COLOR]'
	else: MVT_ONOFF = '[COLOR red] | DOWN[/COLOR]'
	try:
		html_source = abrir_url(url_TPT)
	except: html_source = ''
	items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	if items != []: TPT_ONOFF = '[COLOR green] | UP[/COLOR]'
	else: TPT_ONOFF = '[COLOR red] | DOWN[/COLOR]'
	try:
		html_source = abrir_url(url_FTT)
	except: html_source = ''
	items = re.findall("<div class='post-body entry-content'>(.+?)<div class='post-outer'>", html_source, re.DOTALL)
	if items != []: FTT_ONOFF = '[COLOR green] | UP[/COLOR]'
	else: FTT_ONOFF = '[COLOR red] | DOWN[/COLOR]'
	try:
		html_source = abrir_url(url_CMT)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []: CMT_ONOFF = '[COLOR green] | UP[/COLOR]'
	else: CMT_ONOFF = '[COLOR red] | DOWN[/COLOR]'
	#########################################
        addDir('[B][COLOR green]SÉ[/COLOR][COLOR yellow]R[/COLOR][COLOR red]IES[/COLOR][/B]','http://direct',3003,artfolder + 'SERIES1.png','nao','')
        addDir('[B][COLOR green]FI[/COLOR][COLOR yellow]L[/COLOR][COLOR red]MES[/COLOR][/B]','http://direct',3004,artfolder + 'FILMES1.png','nao','')
        addDir('[B][COLOR green]PRO[/COLOR][COLOR yellow]C[/COLOR][COLOR red]URAR[/COLOR][/B] (Filmes/Séries)','http://www.tuga-filmes.us/search?q=',1,artfolder + 'P1.png','nao','')
        addDir1('','url',1004,artfolder,False,'')
        addDir('[COLOR orange]FTT | [/COLOR][B][COLOR green]FOIT[/COLOR][COLOR yellow]A[/COLOR][COLOR red]TUGA[/COLOR][/B] (Filmes)'+FTT_ONOFF,'http://direct',601,artfolder + 'FTT1.png','nao','')
        addDir('[COLOR orange]TPT | [/COLOR][B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B] (Filmes/Séries)'+TPT_ONOFF,'http://direct',231,artfolder + 'TPT1.png','nao','')
        addDir('[COLOR orange]MVT | [/COLOR][B][COLOR green]MOV[/COLOR][COLOR yellow]I[/COLOR][COLOR red]ETUGA[/COLOR][/B] (Filmes)'+MVT_ONOFF,'http://direct',101,artfolder + 'MVT1.png','nao','')
        addDir('[COLOR orange]CMT | [/COLOR][B][COLOR green]CINE[/COLOR][COLOR yellow]M[/COLOR][COLOR red]ATUGA.net[/COLOR][/B] (Filmes)'+CMT_ONOFF,'http://direct',701,artfolder + 'CMT1.png','nao','')
        addDir('[COLOR orange]TFV | [/COLOR][B][COLOR green]TUGA-[/COLOR][COLOR yellow]F[/COLOR][COLOR red]ILMES.tv[/COLOR][/B] (Filmes/Séries)'+TFV_ONOFF,'http://direct',31,artfolder + 'TFV1.png','nao','')
        addDir('[COLOR orange]TFC | [/COLOR][B][COLOR green]TUGA-[/COLOR][COLOR yellow]F[/COLOR][COLOR red]ILMES.com[/COLOR][/B] (Filmes)'+TFC_ONOFF,'http://direct',71,artfolder + 'TFC1.png','nao','')
        addDir('[B][COLOR yellow]SITES[/COLOR][COLOR blue]dos[/COLOR][COLOR green]BRAZUCAS[/COLOR][/B] (Filmes/Séries)','url',331,artfolder + 'SDB.png','nao','')
        addDir1('','url',1004,artfolder,False,'')
        addDir('[B][COLOR green]DEFI[/COLOR][COLOR yellow]N[/COLOR][COLOR red]IÇÕES[/COLOR][/B] (ADDON)','url',1000,artfolder + 'DEF1.png','nao','')#'ze-icon3.png'

class AvisoFanart(xbmcgui.WindowXMLDialog):

    def __init__( self, *args, **kwargs ):
          xbmcgui.WindowXML.__init__(self)

    def onInit(self):
        pass
          
    def onClick(self,controlId):
        if controlId == 2001: self.close()

def FILMES_MENU():
        url_toppt = 'http://toppt.net/'
        url_TFV = 'http://www.tuga-filmes.us/search/label/Filmes'
        url_TFC = 'http://www.tuga-filmes.info/'
        url_MVT = 'http://www.movie-tuga.blogspot.pt'
        url_FTT = 'http://foitatugacinemaonline.blogspot.pt/'
        url_CMT = 'http://www.tugafilmes.org/search/label/Filmes'#'http://www.tugafilmes.org/search/label/Filmes'
        try:
                toppt_source = abrir_url(url_toppt)
        except: toppt_source = ''
        saber_url_todos = re.compile('<a href="(.+?)">filmes</a></li>').findall(toppt_source)
        if saber_url_todos: url_TPT = saber_url_todos[0]
        else: url_TPT = 'http://toppt.net/'
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "url_FTT": url_FTT, "url_CMT": url_CMT, "fim": 'fim',"xpto":'xpto'}
        url_filmes_filmes = urllib.urlencode(parameters)
        addDir('[B][COLOR green]TO[/COLOR][COLOR yellow]D[/COLOR][COLOR red]OS[/COLOR][/B]',url_filmes_filmes,507,artfolder + 'FT.png','nao','')
        url_TFV = 'http://www.tuga-filmes.us/search/label/Anima%C3%A7%C3%A3o'
        url_TFC = 'http://www.tuga-filmes.info/search/label/Anima%C3%A7%C3%A3o?max-results=20'
        url_MVT = 'http://movie-tuga.blogspot.pt/search/label/animacao'
        url_FTT = 'http://foitatugacinemaonline.blogspot.pt/search/label/ANIMA%C3%87%C3%83O'
        url_CMT = 'http://www.tugafilmes.org/search/label/Anima%C3%A7%C3%A3o'
        saber_url_animacao = re.compile('<a href="(.+?)">Animacao</a></li>').findall(toppt_source)
        if saber_url_animacao: url_TPT = saber_url_animacao[0]
        else: url_TPT = 'http://toppt.net/'
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "url_FTT": url_FTT, "url_CMT": url_CMT, "fim": 'fim',"xpto":'xpto'}
        url_filmes_animacao = urllib.urlencode(parameters)                                                          #6
        addDir('[B][COLOR green]ANI[/COLOR][COLOR yellow]M[/COLOR][COLOR red]AÇÃO[/COLOR][/B]',url_filmes_animacao,507,artfolder + 'FA.png','nao','')
        addDir('[B][COLOR green]NOS[/COLOR][COLOR yellow] C[/COLOR][COLOR red]INEMAS[/COLOR][/B] (TMDB)','http://www.themoviedb.org/movie/now-playing',3002,artfolder + 'NC.png','nao','')
        addDir('[B][COLOR green]MAIS[/COLOR][COLOR yellow] V[/COLOR][COLOR red]OTADOS[/COLOR][/B] (TMDB)','http://www.themoviedb.org/movie/top-rated',3001,artfolder + 'FMV.png','nao','')
        addDir('[B][COLOR green]MAIS P[/COLOR][COLOR yellow]O[/COLOR][COLOR red]PULARES[/COLOR][/B] (TMDB)','http://www.themoviedb.org/movie',3000,artfolder + 'MP.png','nao','')
        addDir('[B][COLOR green]PRO[/COLOR][COLOR yellow]C[/COLOR][COLOR red]URAR[/COLOR][/B] (Filmes)','http://www.tuga-filmes.us/search?q=',1,artfolder + 'P1.png','nao','')

def SERIES_MENU():
        addDir('[B][COLOR green]TO[/COLOR][COLOR yellow]D[/COLOR][COLOR red]AS[/COLOR][/B] (A/Z)','urlTODAS',26,artfolder + 'ST.png','nao','')
        url_TFC = 'http://www.tuga-filmes.info/'
        url_MVT = 'http://www.movie-tuga.blogspot.pt'
        url_TFV = 'http://www.tuga-filmes.us/search/label/S%C3%A9ries'
        url_TPT = 'http://toppt.net/category/series/'
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "fim": 'fim',"xpto":'xpto'}
        url_ultimos_episodios = urllib.urlencode(parameters)
        addDir('[B][COLOR green]ÚLTIMO[/COLOR][COLOR yellow]S [/COLOR][COLOR red]EPISÓDIOS[/COLOR][/B]',url_ultimos_episodios,508,artfolder + 'UEP.png','nao','')
        addDir('[B][COLOR green]EM E[/COLOR][COLOR yellow]X[/COLOR][COLOR red]IBIÇÃO[/COLOR][/B] (TMDB)','http://www.themoviedb.org/tv/on-the-air',3002,artfolder + 'EE.png','nao','')
        addDir('[B][COLOR green]MAIS[/COLOR][COLOR yellow] V[/COLOR][COLOR red]OTADAS[/COLOR][/B] (TMDB)','http://www.themoviedb.org/tv/top-rated',3001,artfolder + 'SMV.png','nao','')
        addDir('[B][COLOR green]MAIS P[/COLOR][COLOR yellow]O[/COLOR][COLOR red]PULARES[/COLOR][/B] (TMDB)','http://www.themoviedb.org/tv',3000,artfolder + 'MP.png','nao','')
        addDir('[B][COLOR green]PRO[/COLOR][COLOR yellow]C[/COLOR][COLOR red]URAR[/COLOR][/B] (Séries)','http://www.tuga-filmes.us/search?q=',1,artfolder + 'P1.png','nao','')
     

def passar_nome_pesquisa_animacao(name):
        nome_pesquisa = str(name)
        nome_pesquisa = nome_pesquisa.replace('[COLOR yellow]PROCURAR POR: [/COLOR]','')
        nome_pp = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]][[]COLOR yellow[]].+?[[]/COLOR[]]').findall(nome_pesquisa)
        if nome_pp: nome_pesquisa = nome_pp[0]
        conta = 0
        nome_pesquisa = nome_pesquisa.replace('é','e')
        nome_pesquisa = nome_pesquisa.replace('ê','e')
        nome_pesquisa = nome_pesquisa.replace('á','a')
        nome_pesquisa = nome_pesquisa.replace('à','a')
        nome_pesquisa = nome_pesquisa.replace('ã','a')
        nome_pesquisa = nome_pesquisa.replace('è','e')
        nome_pesquisa = nome_pesquisa.replace('í','i')
        nome_pesquisa = nome_pesquisa.replace('ó','o')
        nome_pesquisa = nome_pesquisa.replace('ô','o')
        nome_pesquisa = nome_pesquisa.replace('õ','o')
        nome_pesquisa = nome_pesquisa.replace('ú','u')
        nome_pesquisa = nome_pesquisa.replace('Ú','U')
        nome_pesquisa = nome_pesquisa.replace('ç','c')
        nome_pesquisa = nome_pesquisa.replace('ç','c')
        a_q = re.compile('\w+')
        qq_aa = a_q.findall(nome_pesquisa)
        nome_p = ''
        for q_a_q_a in qq_aa:
                if conta == 0:
                        nome_p = q_a_q_a
                        conta = 1
                else:
                        nome_p = nome_p + '+' + q_a_q_a
        url_imdb = 'http://www.imdb.com/find?ref_=nv_sr_fn&q=' + nome_p + '&s=all#tt'
        html_imdbcode = abrir_url(url_imdb)
        filmes_imdb = re.findall('<div class="findSection">(.*?)<div class="findMoreMatches">', html_imdbcode, re.DOTALL)
        imdbc = re.compile('/title/(.+?)/[?]ref').findall(filmes_imdb[0])
        if imdbc: imdbcode = imdbc[0]
        url = 'IMDB'+imdbcode+'IMDB'
        FilmesAnima.FILMES_ANIMACAO_pesquisar(str(nome_pesquisa),'',url)

def passar_nome_pesquisa_filmes(name):
        nome_pesquisa = str(name)
        #Filmes.FILMES_pesquisar(str(nome_pesquisa))
        
def passar_nome_pesquisa_series(name):
        nome_pesquisa = str(name)
        nome_pesquisa = nome_pesquisa.replace('[COLOR yellow]PROCURAR POR: [/COLOR]','')
        Series.SERIES_pesquisar(str(nome_pesquisa))

def passar_nome_SERIES(name):
        nome_pesquisa = str(name)
        nome_pesquisa = nome_pesquisa.replace('[COLOR yellow]PROCURAR POR: [/COLOR]','')
        nome_pp = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]][[]COLOR yellow[]].+?[[]/COLOR[]]').findall(nome_pesquisa)
        if nome_pp: nome_pesquisa = nome_pp[0]
        numpontos=re.compile('[.](.+?)').findall(nome_pesquisa)
        pontos = len(numpontos)
        if pontos > 1: nome_pesquisa = nome_pesquisa.replace('.','')
        conta = 0
        nome_pesquisa = nome_pesquisa.replace('é','e')
        nome_pesquisa = nome_pesquisa.replace('ê','e')
        nome_pesquisa = nome_pesquisa.replace('á','a')
        nome_pesquisa = nome_pesquisa.replace('à','a')
        nome_pesquisa = nome_pesquisa.replace('ã','a')
        nome_pesquisa = nome_pesquisa.replace('è','e')
        nome_pesquisa = nome_pesquisa.replace('í','i')
        nome_pesquisa = nome_pesquisa.replace('ó','o')
        nome_pesquisa = nome_pesquisa.replace('ô','o')
        nome_pesquisa = nome_pesquisa.replace('õ','o')
        nome_pesquisa = nome_pesquisa.replace('ú','u')
        nome_pesquisa = nome_pesquisa.replace('Ú','U')
        nome_pesquisa = nome_pesquisa.replace('ç','c')
        nome_pesquisa = nome_pesquisa.replace('ç','c')
        a_q = re.compile('\w+')
        qq_aa = a_q.findall(nome_pesquisa)
        nome_p = ''
        for q_a_q_a in qq_aa:
                if conta == 0:
                        nome_p = q_a_q_a
                        conta = 1
                else:
                        nome_p = nome_p + '+' + q_a_q_a
        url_imdb = 'http://www.imdb.com/find?ref_=nv_sr_fn&q=' + nome_p + '&s=all#tt'
        html_imdbcode = abrir_url(url_imdb)
        filmes_imdb = re.findall('<div class="findSection">(.*?)<div class="findMoreMatches">', html_imdbcode, re.DOTALL)
        imdbc = re.compile('/title/(.+?)/[?]ref').findall(filmes_imdb[0])
        if imdbc: imdbcode = imdbc[0]
        url = 'IMDB'+imdbcode+'IMDB'
        pesquisar_SERIES(str(nome_pesquisa),url)

def passar_nome_SERIES_IMDB(name):         
        nome_pesquisa = str(name).replace("Marvel's",'')
        #addLink(nome_pesquisa,'','')
        nome_pesquisa = nome_pesquisa.replace('[COLOR yellow]PROCURAR POR: [/COLOR]','')
        nome_pp = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]][[]COLOR yellow[]].+?[[]/COLOR[]]').findall(nome_pesquisa)
        if nome_pp: nome_pesquisa = nome_pp[0]
        numpontos=re.compile('[.](.+?)').findall(nome_pesquisa)
        pontos = len(numpontos)
        if pontos > 1: nome_pesquisa = nome_pesquisa.replace('.','')
        conta = 0
        nome_pesquisa = nome_pesquisa.replace('é','e')
        nome_pesquisa = nome_pesquisa.replace('ê','e')
        nome_pesquisa = nome_pesquisa.replace('á','a')
        nome_pesquisa = nome_pesquisa.replace('à','a')
        nome_pesquisa = nome_pesquisa.replace('ã','a')
        nome_pesquisa = nome_pesquisa.replace('è','e')
        nome_pesquisa = nome_pesquisa.replace('í','i')
        nome_pesquisa = nome_pesquisa.replace('ó','o')
        nome_pesquisa = nome_pesquisa.replace('ô','o')
        nome_pesquisa = nome_pesquisa.replace('õ','o')
        nome_pesquisa = nome_pesquisa.replace('ú','u')
        nome_pesquisa = nome_pesquisa.replace('Ú','U')
        nome_pesquisa = nome_pesquisa.replace('ç','c')
        nome_pesquisa = nome_pesquisa.replace('ç','c')
        a_q = re.compile('\w+')
        qq_aa = a_q.findall(nome_pesquisa)
        nome_p = ''
        for q_a_q_a in qq_aa:
                if conta == 0:
                        nome_p = q_a_q_a
                        conta = 1
                else:
                        nome_p = nome_p + '+' + q_a_q_a
        url_imdb = 'http://www.imdb.com/find?ref_=nv_sr_fn&q=' + nome_p + '&s=all#tt'
        html_imdbcode = abrir_url(url_imdb)
        filmes_imdb = re.findall('<div class="findSection">(.*?)<div class="findMoreMatches">', html_imdbcode, re.DOTALL)
        imdbc = re.compile('/title/(.+?)/[?]ref').findall(filmes_imdb[0])
        if imdbc: imdbcode = imdbc[0]
        url = 'IMDB'+imdbcode+'IMDB'
        pesquisar_SERIES_IMDB(str(nome_pesquisa),url)
        
def MPOPULARES():
        progress = xbmcgui.DialogProgress()
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
        html_pop_source = abrir_url(url)
        conta = 0
        num_mode = 7
	html_pop = re.findall("<h3>Popular Movies</h3>(.*?)<h3>Latest movies", html_pop_source, re.DOTALL)
	if not html_pop:
                html_pop = re.findall("<h3>Popular TV Shows</h3>(.*?)<h3>Latest TV shows", html_pop_source, re.DOTALL)
                num_mode = 3007
        for items_pop in html_pop:
                filmes_pop = re.findall('<li class="w480">(.*?)<ul class="icons left_padding">', items_pop, re.DOTALL)
                num = len(filmes_pop) + 0.0
                for pop_filmes in filmes_pop:
                        imdbcode = ''
                        sinopse = ''
                        fanart = ''
                        genero = ''
                        thumb = ''
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(int(num))
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        nome_ano = re.compile('<h4><a href="(.+?)">(.+?)</a> <span class="date">(.+?)</span></h4>').findall(pop_filmes)
                        thumb_pop = re.compile('<img class="shadow" src="(.+?)" width="92" />').findall(pop_filmes)
                        #############
                        if num_mode == 7:
                                fanart,tmdb_id,thumb = themoviedb_api().fanart_and_id(nome_ano[0][1],nome_ano[0][2].replace('(','').replace(')',''))
                                sinopse = theomapi_api_nome().sinopse(nome_ano[0][1])
                                url_pesquisa = 'http://www.themoviedb.org' + nome_ano[0][0]# + '?language=pt'
                        if num_mode == 3007:
                                thetvdb_id = thetvdb_api()._id(nome_ano[0][1],nome_ano[0][2].replace('(','').replace(')',''))
                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                if ftart:
                                        fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                        if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'                                       
                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                if snpse: sinopse = snpse[0]
                                #fanart,tmdb_id,thumb = themoviedb_api_tv().fanart_and_id(nome_ano[0][1],nome_ano[0][2].replace('(','').replace(')',''))
                                #url_pesquisa = 'http://www.themoviedb.org' + nome_ano[0][0]
##                        try:
##                                html_source = abrir_url(url_pesquisa)
##                        except: html_source = ''
##                        if html_source == '':
##                                if num_mode == 7: url_pesquisa = 'http://www.themoviedb.org' + nome_ano[0][0] + '?language=en'
##                                if num_mode == 3007: url_pesquisa = 'http://www.themoviedb.org' + nome_ano[0][0] + '?language=en'
##                                try:
##                                        html_source = abrir_url(url_pesquisa)
##                                except: html_source = ''
##                        snpse = re.compile('<p id="overview" itemprop="description">(.+?)</p>').findall(html_source)
##                        if not snpse: snpse = re.compile('<h3>Overview</h3>\n<p>(.+?)</p>').findall(html_source)
##                        if snpse: sinopse = snpse[0]
##                        if 'There are no backdrops added to this' not in html_source:
##                                url_fan = re.compile('<meta name="twitter:image" content="(.+?)" />').findall(html_source)
##                                if url_fan: fanart = url_fan[0].replace('w780','w1280')
##                        else: fanart = ''
##                        genre = re.compile('<span itemprop="genre">(.+?)</span></a>').findall(html_source)
##                        conta = 0
##                        for gen in genre:
##                                if conta == 0:
##                                        genero = gen
##                                        conta = 1
##                                else:
##                                        genero = genero + ' ' + gen
                        ##############
                        addDir_teste('[B][COLOR green]' + nome_ano[0][1] + '[/COLOR][/B][COLOR yellow] ' + nome_ano[0][2] + '[/COLOR]','IMDB'+imdbcode+'IMDB',num_mode,thumb_pop[0].replace('w92','w396'),sinopse,fanart,nome_ano[0][2].replace('(','').replace(')',''),genero)
                        #addDir('[B][COLOR green]' + nome_ano[0][1] + '[/COLOR][/B][COLOR yellow] ' + nome_ano[0][2] + '[/COLOR]','IMDB'+imdbcode+'IMDB',num_mode,thumb_pop[0].replace('w92','w396'),'nao','')
                        i = i + 1
        npag = re.compile('<p class="left">Currently on page: (.+?)</p>').findall(html_pop[0])
        numpag = '('+npag[0].replace(' of ','/')+')'
        npagseg = re.compile('<p class="left">Currently on page: (\d+) of .+?</p>').findall(html_pop[0])
        npseg = int(npagseg[0]) + 1
        proxima = re.compile('Previous</a> [|] <a href="(.+?)">Next').findall(html_pop[0])
        if not proxima: proxima = re.compile('<a href="(.+?)">Next').findall(html_pop[0])
	try:
                proximap = 'http://www.themoviedb.org' + proxima[0]
		addDir('[B][COLOR blue]'+numpag+'[/COLOR] Seguinte > [COLOR blue]'+str(npseg)+'[/COLOR][/B]',proximap,3000,artfolder + 'PAGS1.png','','')
	except: pass
        progress.close()

def MVOTADOS():
        progress = xbmcgui.DialogProgress()
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
        html_pop_source = abrir_url(url)
        conta = 0
        num_mode = 7
	html_pop = re.findall('<h3>Top Rated Movies</h3>(.*?)<div id="footer">', html_pop_source, re.DOTALL)
	if not html_pop:
                html_pop = re.findall('<h3>Top Rated TV Shows</h3>(.*?)<div id="footer">', html_pop_source, re.DOTALL)
                num_mode = 3007
        for items_pop in html_pop:
                filmes_pop = re.findall('<li class="w480">(.*?)<ul class="icons left_padding">', items_pop, re.DOTALL)
                num = len(filmes_pop) + 0.0
                for pop_filmes in filmes_pop:
                        imdbcode = ''
                        sinopse = ''
                        fanart = ''
                        genero = ''
                        thumb = ''
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(int(num))
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        nome_ano = re.compile('<h4><a href="(.+?)">(.+?)</a> <span class="date">(.+?)</span></h4>').findall(pop_filmes)
                        thumb_pop = re.compile('<img class="shadow" src="(.+?)" width="92" />').findall(pop_filmes)
                        #############
                        if num_mode == 7:
                                fanart,tmdb_id,thumb = themoviedb_api().fanart_and_id(nome_ano[0][1],nome_ano[0][2].replace('(','').replace(')',''))
                                sinopse = theomapi_api_nome().sinopse(nome_ano[0][1])
                                #url_pesquisa = 'http://www.themoviedb.org' + nome_ano[0][0] + '?language=pt'
                        if num_mode == 3007:
                                thetvdb_id = thetvdb_api()._id(nome_ano[0][1],nome_ano[0][2].replace('(','').replace(')',''))
                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                if ftart:
                                        fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                        if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'                                       
                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                if snpse: sinopse = snpse[0]
                                #fanart,tmdb_id,thumb = themoviedb_api_tv().fanart_and_id(nome_ano[0][1],nome_ano[0][2].replace('(','').replace(')',''))
                                #url_pesquisa = 'http://www.themoviedb.org' + nome_ano[0][0] + '?language=pt'
##                        try:
##                                html_source = abrir_url(url_pesquisa)
##                        except: html_source = ''
##                        if html_source == '':
##                                if num_mode == 7: url_pesquisa = 'http://www.themoviedb.org' + nome_ano[0][0] + '?language=en'
##                                if num_mode == 3007: url_pesquisa = 'http://www.themoviedb.org' + nome_ano[0][0] + '?language=en'
##                                try:
##                                        html_source = abrir_url(url_pesquisa)
##                                except: html_source = ''
##                        snpse = re.compile('<p id="overview" itemprop="description">(.+?)</p>').findall(html_source)
##                        if not snpse: snpse = re.compile('<h3>Overview</h3>\n<p>(.+?)</p>').findall(html_source)
##                        if snpse: sinopse = snpse[0]
##                        if 'There are no backdrops added to this' not in html_source:
##                                url_fan = re.compile('<meta name="twitter:image" content="(.+?)" />').findall(html_source)
##                                if url_fan: fanart = url_fan[0].replace('w780','w1280')
##                        else: fanart = ''
##                        genre = re.compile('<span itemprop="genre">(.+?)</span></a>').findall(html_source)
##                        conta = 0
##                        for gen in genre:
##                                if conta == 0:
##                                        genero = gen
##                                        conta = 1
##                                else:
##                                        genero = genero + ' ' + gen
                        ##############
                        addDir_teste('[B][COLOR green]' + nome_ano[0][1] + '[/COLOR][/B][COLOR yellow] ' + nome_ano[0][2] + '[/COLOR]','IMDB'+imdbcode+'IMDB',num_mode,thumb,sinopse,fanart,nome_ano[0][2].replace('(','').replace(')',''),genero)
                        #addDir('[B][COLOR green]' + nome_ano[0][0] + '[/COLOR][/B][COLOR yellow] ' + nome_ano[0][1] + '[/COLOR]','IMDB'+imdbcode+'IMDB',num_mode,thumb_pop[0].replace('w92','w396'),'nao','')
                        i = i + 1
        npag = re.compile('<p class="left">Currently on page: (.+?)</p>').findall(html_pop[0])
        numpag = '('+npag[0].replace(' of ','/')+')'
        npagseg = re.compile('<p class="left">Currently on page: (\d+) of .+?</p>').findall(html_pop[0])
        npseg = int(npagseg[0]) + 1
        proxima = re.compile('Previous</a> [|] <a href="(.+?)">Next').findall(html_pop[0])
        if not proxima: proxima = re.compile('<a href="(.+?)">Next').findall(html_pop[0])
	try:
                proximap = 'http://www.themoviedb.org' + proxima[0]
		addDir('[B][COLOR blue]'+numpag+'[/COLOR] Seguinte > [COLOR blue]'+str(npseg)+'[/COLOR][/B]',proximap,3001,artfolder + 'PAGS1.png','','')
	except: pass
        progress.close()

def NCINEMAS():
        progress = xbmcgui.DialogProgress()
        i = 1
        percent = 0
        message = ''
        progress.create('Progresso', 'A Pesquisar:')
        progress.update( percent, "", message, "" )
        html_pop_source = abrir_url(url)
        conta = 0
        num_mode = 7
	html_pop = re.findall('<h3>Now Playing Movies</h3>(.*?)<div id="footer">', html_pop_source, re.DOTALL)
	if not html_pop:
                html_pop = re.findall('<h3>Currently Airing TV Shows</h3>(.*?)<div id="footer">', html_pop_source, re.DOTALL)
                num_mode = 3007
        for items_pop in html_pop:
                filmes_pop = re.findall('<li class="w480">(.*?)<ul class="icons left_padding">', items_pop, re.DOTALL)
                num = len(filmes_pop) + 0.0
                for pop_filmes in filmes_pop:
                        imdbcode = ''
                        sinopse = ''
                        fanart = ''
                        genero = ''
                        thumb = ''
                        percent = int( ( i / num ) * 100)
                        message = str(i) + " de " + str(int(num))
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        nome_ano = re.compile('<h4><a href="(.+?)">(.+?)</a> <span class="date">(.+?)</span></h4>').findall(pop_filmes)
                        thumb_pop = re.compile('<img class="shadow" src="(.+?)" width="92" />').findall(pop_filmes)
                        #############
                        if num_mode == 7:
                                fanart,tmdb_id,thumb = themoviedb_api().fanart_and_id(nome_ano[0][1],nome_ano[0][2].replace('(','').replace(')',''))
                                sinopse = theomapi_api_nome().sinopse(nome_ano[0][1])
                                #url_pesquisa = 'http://www.themoviedb.org' + nome_ano[0][0]# + '?language=pt'
                        if num_mode == 3007:
                                thetvdb_id = thetvdb_api()._id(nome_ano[0][1],nome_ano[0][2].replace('(','').replace(')',''))
                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                if ftart:
                                        fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                        if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'                                       
                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                if snpse: sinopse = snpse[0]
                                #fanart,tmdb_id,thumb = themoviedb_api_tv().fanart_and_id(nome_ano[0][1],nome_ano[0][2].replace('(','').replace(')',''))
                                #url_pesquisa = 'http://www.themoviedb.org' + nome_ano[0][0]
##                        try:
##                                html_source = abrir_url(url_pesquisa)
##                        except: html_source = ''
##                        snpse = re.compile('<p id="overview" itemprop="description">(.+?)</p>').findall(html_source)
##                        if not snpse: snpse = re.compile('<h3>Overview</h3>\n<p>(.+?)</p>').findall(html_source)
##                        if snpse: sinopse = snpse[0]
####                        else:
####                                if num_mode == 7: url_pesquisa = 'http://www.themoviedb.org' + nome_ano[0][0]
####                                if num_mode == 3005: url_pesquisa = 'http://www.themoviedb.org' + nome_ano[0][0]
####                                try:
####                                        html_source = abrir_url(url_pesquisa)
####                                except: html_source = ''
####                                snpse = re.compile('<p id="overview" itemprop="description">(.+?)</p>').findall(html_source)
####                                if not snpse: snpse = re.compile('<h3>Overview</h3>\n<p>(.+?)</p>').findall(html_source)
####                                if snpse: sinopse = snpse[0]
##                        if 'There are no backdrops added to this' not in html_source:
##                                url_fan = re.compile('<meta name="twitter:image" content="(.+?)" />').findall(html_source)
##                                if url_fan: fanart = url_fan[0].replace('w780','w1280')
##                        else: fanart = ''
##                        genre = re.compile('<span itemprop="genre">(.+?)</span></a>').findall(html_source)
##                        conta = 0
##                        for gen in genre:
##                                if conta == 0:
##                                        genero = gen
##                                        conta = 1
##                                else:
##                                        genero = genero + ' ' + gen
                        ##############
                        addDir_teste('[B][COLOR green]' + nome_ano[0][1] + '[/COLOR][/B][COLOR yellow] ' + nome_ano[0][2] + '[/COLOR]','IMDB'+imdbcode+'IMDB',num_mode,thumb_pop[0].replace('w92','w396'),sinopse,fanart,nome_ano[0][2].replace('(','').replace(')',''),genero)
                        #addDir('[B][COLOR green]' + nome_ano[0][0] + '[/COLOR][/B][COLOR yellow] ' + nome_ano[0][1] + '[/COLOR]','IMDB'+imdbcode+'IMDB',num_mode,thumb_pop[0].replace('w92','w396'),'nao','')
                        i = i + 1
        npag = re.compile('<p class="left">Currently on page: (.+?)</p>').findall(html_pop[0])
        numpag = '('+npag[0].replace(' of ','/')+')'
        npagseg = re.compile('<p class="left">Currently on page: (\d+) of .+?</p>').findall(html_pop[0])
        npseg = int(npagseg[0]) + 1
        proxima = re.compile('Previous</a> [|] <a href="(.+?)">Next').findall(html_pop[0])
        if not proxima: proxima = re.compile('<a href="(.+?)">Next').findall(html_pop[0])
	try:
                proximap = 'http://www.themoviedb.org' + proxima[0]
		addDir('[B][COLOR blue]'+numpag+'[/COLOR] Seguinte > [COLOR blue]'+str(npseg)+'[/COLOR][/B]',proximap,3002,artfolder + 'PAGS1.png','','')
	except: pass
        progress.close()

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def pesquisar_SERIES_IMDB(nome_pesquisa,url):
        nome_pp = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]][[]COLOR yellow[]].+?[[]/COLOR[]]').findall(nome_pesquisa)
        if nome_pp: nome_pesquisa = nome_pp[0]
        imdb = re.compile('IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        pp = nome_pesquisa
        
        progress = xbmcgui.DialogProgress()
        percent = 0
        message = ''
        site = ''
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar...'+site, message, "" )
        pesquisou = nome_pesquisa
        if '-' in nome_pesquisa:
                nome_p = re.compile('.+?[-](.+?)').findall(nome_pesquisa)
                if len(nome_p[0])>2:
                        nome_pesquisa = nome_p[0]
        else:
                if ':' in nome_pesquisa:
                        nome_p = re.compile('(.+?)[:].+?').findall(nome_pesquisa)
                        nome_pesquisa = nome_p[0]

        nome_pesquisa = nome_pesquisa.replace('é','e')
        nome_pesquisa = nome_pesquisa.replace('ê','e')
        nome_pesquisa = nome_pesquisa.replace('á','a')
        nome_pesquisa = nome_pesquisa.replace('à','a')
        nome_pesquisa = nome_pesquisa.replace('ã','a')
        nome_pesquisa = nome_pesquisa.replace('è','e')
        nome_pesquisa = nome_pesquisa.replace('í','i')
        nome_pesquisa = nome_pesquisa.replace('ó','o')
        nome_pesquisa = nome_pesquisa.replace('ô','o')
        nome_pesquisa = nome_pesquisa.replace('õ','o')
        nome_pesquisa = nome_pesquisa.replace('ú','u')
        nome_pesquisa = nome_pesquisa.replace('Ú','U')
        nome_pesquisa = nome_pesquisa.replace('ç','c')
        nome_pesquisa = nome_pesquisa.replace('ç','c')

        nome_pesquisa = nome_pesquisa.lower()
        pesquisou = nome_pesquisa

        numpontos=re.compile('[.](.+?)').findall(nome_pesquisa)
        pontos = len(numpontos)
        if pontos > 1: nome_pesquisa = nome_pesquisa.replace('.','')

        conta = 0
        a_q = re.compile('\w+')
        qq_aa = a_q.findall(nome_pesquisa)
        nome_pesquisa = ''
        for q_a_q_a in qq_aa:
                if len(q_a_q_a) > 0 or q_a_q_a == '1' or q_a_q_a == '2' or q_a_q_a == '3' or q_a_q_a == '4'or q_a_q_a == '5' or q_a_q_a == '6':
                #if len(q_a_q_a) > 1:
                        if conta == 0:
                                nome_pesquisa = q_a_q_a
                                conta = 1
                        else:
                                nome_pesquisa = nome_pesquisa + '+' + q_a_q_a

        nome_pesquisa = nome_pesquisa.lower()
        nome_pesquisa = nome_pesquisa.replace('  ','')
        encode=urllib.quote(nome_pesquisa)

        a = 0
        site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv'
        percent = int( ( a / 2.0 ) * 100)
        message = ''
        progress.update(percent, 'A Procurar em '+site, message, "")
        print str(a) + " de " + str(int(a))
        #xbmc.sleep( 200 )
	url_pesquisa = 'http://www.tuga-filmes.us/search?q=' + str(encode) + 'IMDB'+imdbcode+'IMDB'
	encontrar_fontes_SERIES_TFV(url_pesquisa,pesquisou)
	
	a = 1
	site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
	percent = int( ( a / 2.0 ) * 100)
        message = ''
        progress.update(percent, 'A Procurar em '+site, message, "")
        print str(a) + " de " + str(int(a))
        #xbmc.sleep( 100 )
	url_pesquisa = 'http://toppt.net/?s=' + str(encode) + 'IMDB'+imdbcode+'IMDB'
	encontrar_fontes_SERIES_TPT(url_pesquisa,pesquisou)
	
        a = 2
	site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
	percent = int( ( a / 2.0 ) * 100)
        message = ''
        progress.update(percent, 'A Procurar em '+site, message, "")
        print str(a) + " de " + str(int(a))
        #xbmc.sleep( 100 )

        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(500)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def pesquisar_SERIES(nome_pesquisa,url):

        nome_pp = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]][[]COLOR yellow[]].+?[[]/COLOR[]]').findall(nome_pesquisa)
        if nome_pp: nome_pesquisa = nome_pp[0]
        imdb = re.compile('IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        

        progress = xbmcgui.DialogProgress()
        percent = 0
        message = ''
        site = ''
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar...'+site, message, "" )
        pesquisou = nome_pesquisa

        _url = re.compile('IMDB[|](.+?)[|](.*)').findall(url)
        if _url:
                url_TFV = _url[0][0]
                url_TPT = _url[0][1]
        else:
                _url = re.compile('IMDB[|](.*)').findall(url)
                if _url:
                        url = _url[0]
                        if 'tuga-filmes' in url:
                                url_TPT = ''
                                url_TFV = url
                        if 'toppt' in url:
                                url_TFV = ''
                                url_TPT = url
        #addLink(url_TPT,'','')
        #addLink(url_TFV,'','')
        a = 0
        site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv'
        percent = int( ( a / 2.0 ) * 100)
        message = ''
        progress.update(percent, 'A Procurar em '+site, message, "")
        print str(a) + " de " + str(int(a))
	encontrar_fontes_SERIES_TFV(url_TFV + 'IMDB'+imdbcode+'IMDB',pesquisou)
	
	a = 1
	site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
	percent = int( ( a / 2.0 ) * 100)
        message = ''
        progress.update(percent, 'A Procurar em '+site, message, "")
        print str(a) + " de " + str(int(a))
	encontrar_fontes_SERIES_TPT(url_TPT + 'IMDB'+imdbcode+'IMDB',pesquisou)
	
        a = 2
	site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
	percent = int( ( a / 2.0 ) * 100)
        message = ''
        progress.update(percent, 'A Procurar em '+site, message, "")
        print str(a) + " de " + str(int(a))
        
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        xbmc.executebuiltin("Container.SetViewMode(500)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def encontrar_fontes_SERIES_TFV(url,pesquisou):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbc = imdb[0].replace('IMDB','')
        else: imdbc = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','').replace('IMDB','')
        else: url = urlimdb[0].replace('IMDBIMDB','').replace('IMDB','')
        imdbcode_passado = ''
        num_mode = 42

	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
                num_f = 0
		print len(items)
		fanart = ''
		for item in items:
                        #if fanart == '':
                        thumb = ''
                        #fanart = ''
                        versao = ''
                        audio_filme = ''
                        imdbcode = ''
                        genero = ''
                        sinopse = ''
                        versao = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        if 'Portug' and 'Legendado' in item: versao = '[COLOR blue]2 VERSÕES[/COLOR]'
                        gener = re.compile("nero</b>:(.+?)<br />").findall(item)
                        if gener: genero = gener[0]
                        else: genero = ''
                        resumo = re.compile("<b>Resumo</b>:(.+?)<br />").findall(item)
                        if resumo: sinopse = resumo[0]
                        else: sinopse = ''
                        titulooriginal = re.compile("tulo Original:</b>(.+?)<br />").findall(item)
                        if titulooriginal:
                                nome_original = titulooriginal[0]
                                #addDir1(nome_original,'','',artfolder + 'PAGS1.png',False,'')
                        else:
                                titulooriginal = re.compile("<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>(.+?)<br />").findall(item)
                                if titulooriginal:
                                        nome_original = titulooriginal[0]
                                else: nome_original = ''
                                #addDir1(nome_original,'','',artfolder + 'PAGS1.png',False,'')
                        urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)

                        tto=re.compile('tulo Original:</b>:(.+?)<br').findall(item)
                        if tto: ttor = tto[0]
                        else:
                                tto=re.compile('tulo Original:</b>(.+?)<br').findall(item)
                                if tto: ttor = tto[0]
                        ttp=re.compile('<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>:(.+?)<br').findall(item)
                        if ttp: ttpo = ttp[0]
                        else:
                                ttp=re.compile('<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>(.+?)<br').findall(item)
                                if ttp: ttpo = ttp[0]
                        #urletitulo = re.compile("<h1>(.+?)\n</h1>").findall(item)
                        if ttp and not tto: nome = ttp[0]
                        elif not ttp and tto: nome = tto[0]
                        elif ttp and tto:
                                ttocomp = '['+ tto[0]
                                ttpcomp = '['+ ttp[0]
                                if ttpcomp.replace('[ ','') != ttocomp.replace('[ ',''): nome = ttp[0] +' ['+ tto[0] +']'
                                else: nome = ttp[0]
                        elif not ttp and not tto: nome = urletitulo[0][1]
                        nome = nome.replace('[ ',"[")
                                
                        qualidade = re.compile("<b>Qualidade</b>: (.+?)<br />").findall(item)
                        ano = re.compile("<b>Ano</b>: (.+?)<br />").findall(item)
                        audio = re.compile("<b>.+?udio</b>(.+?)<br />").findall(item)
                        imdb_code = re.compile('<b>Mais INFO</b>: <a href="http://www.imdb.com/title/(.+?)/" target="_blank">IMDb</a>').findall(item)
                        if audio != []:
                                if 'Portug' in audio[0]:
                                        audio_filme = ': PT-PT'
                                else:
                                        audio_filme = audio[0]
                        thumbnail = re.compile('src="(.+?)"').findall(item)
                        if thumbnail: thumb = thumbnail[0]
                        else: thumb = ''
                        print urletitulo,thumb
                        nome = urletitulo[0][1]
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('(PT-PT)',"")
                        nome = nome.replace('(PT/PT)',"")
                        nome = nome.replace('[PT-PT]',"")
                        nome = nome.replace('[PT/PT]',"")
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        tirar_ano = '(' + str(q_a_q_a) + ')'
                                        nome = nome.replace(tirar_ano,'')			

                        if qualidade:
                                qualidade = qualidade[0]
                        else:
                                qualidade = ''
                        try:
                                #addLink(nome,'','')
                                
                                if 'Temporada' in nome or 'Season' in nome:
                                        if imdbc != '' and imdbcode != '':
                                                if imdbcode == imdbc:
                                                        #addLink(thumb,'','')
                                                        if imdbcode_passado != imdbcode:
                                                                imdbcode_passado = imdbcode
                                                                n = re.compile('(.+?)[(].+?[)]').findall(nome)
                                                                if n: nome_pesquisa = n[0]
                                                                else: nome_pesquisa = nome
                                                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano[0])
                                                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                                                if ftart: fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                                if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                                                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                                if snpse: sinopse = snpse[0]
                                                        n = re.compile('[(](.+?)[)]').findall(nome)
                                                        if n: nome = n[0]
                                                        #addDir('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR]',urletitulo[0][0],num_mode,thumbnail[0].replace('s72-c','s320'),'',fanart)
                                                        addDir_teste('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0],num_mode,thumb.replace('s72-c','s320'),sinopse,fanart,ano[0],genero)
                                                        num_f = num_f + 1
                                        else:
                                                if imdbcode_passado != imdbcode:
                                                        imdbcode_passado = imdbcode
                                                        n = re.compile('(.+?)[(].+?[)]').findall(nome)
                                                        if n: nome_pesquisa = n[0]
                                                        else: nome_pesquisa = nome
                                                        thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano[0])
                                                        ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                                        if ftart: fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                        if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                                                        snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                        if snpse: sinopse = snpse[0]
                                                n = re.compile('[(](.+?)[)]').findall(nome)
                                                if n: nome = n[0]
                                                #addDir('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR]',urletitulo[0][0],num_mode,thumbnail[0].replace('s72-c','s320'),'',fanart)
                                                addDir_teste('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0],num_mode,thumb.replace('s72-c','s320'),sinopse,fanart,ano[0],genero)
                                                num_f = num_f + 1
                        except: pass
##                        addLink(str(len(items)),'','')
##                        addLink(nome,'','')
##                        addLink(nome_original,'','')
##                        addLink(thumb,'','')
##                        addLink(versao,'','')
##                        addLink(qualidade,'','')
##                        addLink(genero,'','')
##                        addLink(ano[0],'','')
##                        addLink(sinopse,'','')
##                        addLink(fanart,'','')
##                        addLink(imdbcode,'','')
                        #except: pass
                                
        else: return
	return

def encontrar_fontes_SERIES_TPT(url,pesquisou):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbc = imdb[0].replace('IMDB','')
        else: imdbc = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','').replace('IMDB','')
        else: url = urlimdb[0].replace('IMDBIMDB','').replace('IMDB','')
        imdbcode_passado = ''

	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	if items != []:
                num_f = 0
		print len(items)
		fanart = ''
		for item in items:
                        audio_filme = ''
                        sinopse = ''
                        #fanart = ''
                        thumb = ''
                        genero = ''
                        qualidade = ''
                        #nome_pesquisa = ''
                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(item)
                        if 'title=' in urletitulo[0][0]: urletitulo = re.compile('<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>').findall(item)
                        
                        qualid = re.compile("<b>QUALIDADE:.+?/b>(.+?)<br/>").findall(item)
                        if not qualid: qualid = re.compile("<b>VERSÃO:.+?</b>(.+?)<br/>").findall(item)
                        if qualid:
                                qualidade = qualid[0]
                                qualidade = qualidade.replace('[',' - ')
                                qualidade = qualidade.replace(']','')
                        else:
                                qualid = re.compile("\nQUALIDADE:\xc2\xa0(.+?)<br/>").findall(item)
                                if qualid:
                                        qualidade = qualid[0]
                                        qualidade = qualidade.replace('[',' - ')
                                        qualidade = qualidade.replace(']','')
                                else:
                                        qualid = re.compile("<b>VERS.+?</b>(.+?)<br/>").findall(item)
                                        if qualid:
                                                qualidade = qualid[0]
                                                qualidade = qualidade.replace('[',' - ')
                                                qualidade = qualidade.replace(']','')
                                        else:
                                                qualidade = ''
                        
##                        snpse = re.compile("<b>SINOPSE:.+?/b>(.+?)<br/>").findall(item)
##                        if not snpse: snpse = re.compile("<b>SINOPSE:.+?</b>(.+?)<br/>").findall(item)
##                        if snpse: sinopse = snpse[0]
##                        else:
##                                try:
##                                        fonte_video = abrir_url(urletitulo[0][0])
##                                except: fonte_video = ''
##                                fontes_video = re.findall('<div class="postmeta-primary">(.*?)<div id="sidebar-primary">', fonte_video, re.DOTALL)
##                                if fontes_video != []:
##                                        snpse = re.compile('Sinopse.png".+?/><br/>\n(.+?)</p>').findall(fontes_video[0])
##                                        if snpse: sinopse = snpse[0]
##                                        else: sinopse = ''
##                        sinopse = sinopse.replace('&#8216;',"'")
##                        sinopse = sinopse.replace('&#8217;',"'")
##                        sinopse = sinopse.replace('&#8211;',"-")
##                        sinopse = sinopse.replace('&#8220;',"'")
##                        sinopse = sinopse.replace('&#8221;',"'")
##                        sinopse = sinopse.replace('&#39;',"'")
##                        sinopse = sinopse.replace('&amp;','&')
                                        
                        genr = re.compile("NERO:.+?/b>(.+?)<br/>").findall(item)
                        if genr: genero = genr[0]
                        
                        ano = re.compile("<b>ANO:.+?/b>(.+?)<br/>").findall(item)
                        audio = re.compile("<b>AUDIO:.+?/b>(.+?)<br/>").findall(item)
                        thumbnail = re.compile('src="(.+?)"').findall(item)
                        if thumbnail: thumb = thumbnail[0].replace('s72-c','s320')
                        print urletitulo,thumbnail
                        nome = urletitulo[0][1]
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#038;',"&")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('(PT-PT)',"")
                        nome = nome.replace('(PT/PT)',"")
                        nome = nome.replace('[PT-PT]',"")
                        nome = nome.replace('[PT/PT]',"")
                        nome = nome.replace('[PT-BR]',"")
                        nome = nome.replace('[PT/BR]',"")
                        nome = nome.replace(' (PT-PT)',"")
                        nome = nome.replace(' (PT/PT)',"")
                        nome = nome.replace(' [PT-PT]',"")
                        nome = nome.replace(' [PT/PT]',"")
                        nome = nome.replace(' [PT-BR]',"")
                        nome = nome.replace(' [PT/BR]',"")
                        nome = nome.replace('  '," ")
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
                                                        audio = re.compile('<b>AUDIO:.+?<strong>(.+?)</strong>').findall(item)
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
                                        ano_filme = ': ' + ano[0].replace(' ','')
                                else:
                                        ano_filme = ''     
                        if ano:
                                ano_filme = ano[0].replace(' ','')
                                a_q = re.compile('\d+')
                                qq_aa = a_q.findall(nome)
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) == 4:
                                                tirar_ano = '(' + str(q_a_q_a) + ')'
                                                nome = nome.replace(tirar_ano,'')
                        
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        tirar_ano = '(' + str(q_a_q_a) + ')'
                                        nome = nome.replace(tirar_ano,'')
                        
                        try:
                                if genero == '': genero = '---'
                                if sinopse == '': sinopse = '---'
                                if fanart == '': fanart = '---'
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
                                if imdbc != '' and imdbcode != '':
                                        if imdbcode == imdbc:
                                                #addLink(imdbcode_passado+'-'+imdbcode,'','')
                                                if imdbcode_passado != imdbcode:
                                                        imdbcode_passado = imdbcode
                                                        n = re.compile('(.+?)[[].+?[]]').findall(nome)
                                                        if n: nome_pesquisa = n[0]
                                                        else: nome_pesquisa = nome
                                                        thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme.replace('(','').replace(')',''))
                                                        ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                                        if ftart: fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                        if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                                                        snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                        if snpse: sinopse = snpse[0]
                                                n = re.compile('[[](.+?)[]][[](.+?)[]]').findall(nome)
                                                if not n: n = re.compile('[[](.+?)[]] [[](.+?)[]]').findall(nome)
                                                if n: nome = n[0][0]+' - '+n[0][1]
                                                else:
                                                        n = re.compile('[(](.+?)[)][(](.+?)[)]').findall(nome)
                                                        if not n: n = re.compile('[(](.+?)[)] [(](.+?)[)]').findall(nome)
                                                        if n: nome = n[0][0]+' - '+n[0][1]
                                                        else:
                                                                n = re.compile('[[](.+?)[]]').findall(nome)
                                                                if n: nome = n[0]
                                                                else:
                                                                        n = re.compile('[(](.+?)[)]').findall(nome)
                                                                        if n: nome = n[0]
                                                addDir_teste('[COLOR orange]TPT | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',233,thumb,sinopse,fanart,ano_filme.replace('(','').replace(')',''),genero)
                                                num_f = num_f + 1
                                else:
                                        if imdbcode_passado != imdbcode:
                                                imdbcode_passado = imdbcode
                                                n = re.compile('(.+?)[[].+?[]]').findall(nome)
                                                if n: nome_pesquisa = n[0]
                                                else: nome_pesquisa = nome
                                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme.replace('(','').replace(')',''))
                                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                                if ftart: fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                if snpse: sinopse = snpse[0]
                                        n = re.compile('[[](.+?)[]][[](.+?)[]]').findall(nome)
                                        if not n: n = re.compile('[[](.+?)[]] [[](.+?)[]]').findall(nome)
                                        if n: nome = n[0][0]+' - '+n[0][1]
                                        else:
                                                n = re.compile('[(](.+?)[)][(](.+?)[)]').findall(nome)
                                                if not n: n = re.compile('[(](.+?)[)] [(](.+?)[)]').findall(nome)
                                                if n: nome = n[0][0]+' - '+n[0][1]
                                                else:
                                                        n = re.compile('[[](.+?)[]]').findall(nome)
                                                        if n: nome = n[0]
                                                        else:
                                                                n = re.compile('[(](.+?)[)]').findall(nome)
                                                                if n: nome = n[0]
                                        addDir_teste('[COLOR orange]TPT | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',233,thumb,sinopse,fanart,ano_filme.replace('(','').replace(')',''),genero)
                                        num_f = num_f + 1
                        except: pass
##                        addLink(str(len(items)),'','')
##                        addLink(nome,'','')
##                        #addLink(nome_original,'','')
##                        addLink(thumb,'','')
##                        addLink(audio_filme,'','')
##                        addLink(qualidade,'','')
##                        addLink(genero,'','')
##                        addLink(ano_filme,'','')
##                        addLink(sinopse,'','')
##                        addLink(fanart,'','')
##                        addLink(imdbcode,'','')
        return

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#




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
	liz.setProperty('fanart_image',artfolder + 'FAN3.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,checker,fanart):
        if fanart == '': fanart = artfolder + 'FAN3.jpg'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&checker="+urllib.quote_plus(checker)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',fanart)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir1(name,url,mode,iconimage,folder,fanart):
        if fanart == '': fanart = artfolder + 'FAN3.jpg'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',fanart)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
        return ok

def addDir_teste(name,url,mode,iconimage,plot,fanart,year,genre):
        if fanart == '': fanart = artfolder + 'FAN3.jpg'
        #text = plot
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&plot="+urllib.quote_plus(plot)+"&year="+urllib.quote_plus(year)+"&genre="+urllib.quote_plus(genre)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',fanart)
        #liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Year": year, "Genre": genre } )
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Year": year, "Genre": genre } )
        #cm = []
	#cm.append(('Sinopse', 'XBMC.Action(Info)'))
	#liz.addContextMenuItems(cm, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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
plot=None
year=None
genre=None

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
print "Fanart: "+str(fanart)

if mode==None or url==None or len(url)<1:
        #setViewMode_menuPrincipal()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        MAIN_MENU()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        #setViewMode_menuPrincipal()
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode ==  1:
        Pesquisar.pesquisar()

elif mode ==  2:
        Pesquisar.encontrar_fontes_pesquisa_TFV(url,pesquisou)

elif mode ==  3:
        Pesquisar.encontrar_fontes_filmes_TFC(url_pesquisa)

elif mode ==  4:
        Pesquisar.encontrar_fontes_pesquisa_MVT(url)

elif mode ==  5:
        Pesquisar.encontrar_fontes_filmes_TPT(url_pesquisa)

elif mode ==  6:
        Mashup.Filmes_Animacao(url)
        #setViewMode_filmesAnima()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode ==  7:
        passar_nome_pesquisa_animacao(name)

elif mode ==  8:
        passar_nome_pesquisa_filmes(name)

elif mode ==  9:
        passar_nome_pesquisa_series(name)

elif mode == 10:
        FilmesAnima.FILMES_ANIMACAO_pesquisar(nome_pesquisa)

elif mode == 11:
        FilmesAnima.FILMES_ANIMACAO_fontes_pesquisa_TFV(url,pesquisou)

elif mode == 12:
        FilmesAnima.FILMES_ANIMACAO_fontes_filmes_TFC(url_pesquisa)

elif mode == 13:
        FilmesAnima.FILMES_ANIMACAO_fontes_pesquisa_MVT(url)

elif mode == 14:
        FilmesAnima.FILMES_ANIMACAO_fontes_filmes_TPT(url_pesquisa,pesquisou)

#elif mode == 20:
#        Filmes.FILMES_pesquisar(nome_pesquisa)

#elif mode == 21:
#        Filmes.FILMES_fontes_pesquisa_TFV(url,pesquisou)

#elif mode == 22:
#        Filmes.FILMES_fontes_filmes_TFC(url_pesquisa)

#elif mode == 23:
#        Filmes.FILMES_fontes_pesquisa_MVT(url)

#elif mode == 24:
#        Filmes.FILMES_fontes_filmes_TPT(url_pesquisa)
        
elif mode == 25:
        Filmes_Filmes()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(500)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 26:
        Mashup.Series_Series(url)
        #setViewMode_series()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(515)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

        
elif mode == 27:
        Series.SERIES_pesquisar(nome_pesquisa)
        
elif mode == 28:
        Series.SERIES_fontes_pesquisa_TFV(url,pesquisou)

elif mode == 29:
        Series.SERIES_fontes_TPT(url_pesquisa)

#----------------------------------------------  Tuga-Filmes.tv  ----------------------------------------------------
elif mode == 30: print ""; Play.PLAY_movie(url,name,iconimage,checker,fanart)#,nomeAddon)
elif mode == 31:
        TugaFilmesTV.TFV_MenuPrincipal(artfolder)
        #setViewMode_menuTFV()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 32:
        TugaFilmesTV.TFV_encontrar_fontes_filmes(url,artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 33: TugaFilmesTV.TFV_encontrar_videos_filmes(name,url)
elif mode == 34: TugaFilmesTV.TFV_pesquisar()
elif mode == 35: TugaFilmesTV.TFV_resolve_videomega_filmes(url,conta_id_video)
elif mode == 36: TugaFilmesTV.TFV_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,nome_fonte_video)
elif mode == 37: TugaFilmesTV.TFV_Menu_Filmes(artfolder)
elif mode == 38:
        TugaFilmesTV.TFV_Menu_Filmes_Por_Categorias(artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 39:
        TugaFilmesTV.TFV_Menu_Filmes_Por_Ano(artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 40: TugaFilmesTV.TFV_Menu_Series(artfolder)
elif mode == 41:
        TugaFilmesTV.TFV_Menu_Series_A_a_Z(artfolder,url)
        #setViewMode_series_AZ_TFV()
        #xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 42: TugaFilmesTV.TFV_encontrar_videos_series(name,url)
elif mode == 43: TugaFilmesTV.TFV_resolve_not_videomega_series(name,url,id_video,nome_cada_episodio,src_href)
elif mode == 44:
        TugaFilmesTV.TFV_encontrar_fontes_series_recentes(url)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 45: TugaFilmesTV.TFV_pesquisar_series()
elif mode == 46:
        TugaFilmesTV.TFV_encontrar_fontes_pesquisa(url,pesquisou)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(500)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 47:
        TugaFilmesTV.TFV_encontrar_fontes_series_A_a_Z(url)
        #xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        #xbmc.executebuiltin("Container.SetViewMode(500)")
        #xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 48:
        TugaFilmesTV.TFV_Menu_Filmes_Top_5(artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
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
elif mode == 71:
        TugaFilmesCom.TFC_MenuPrincipal(artfolder)
        #setViewMode_menuTFC()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 72:
        TugaFilmesCom.TFC_encontrar_fontes_filmes(url)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 73: TugaFilmesCom.TFC_encontrar_videos_filmes(name,url)
elif mode == 74: TugaFilmesCom.TFC_pesquisar_filmes()
elif mode == 75: TugaFilmesCom.TFC_resolve_videomega_filmes(url,conta_id_video)
elif mode == 76: TugaFilmesCom.TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,nome_fonte_video)
elif mode == 77: TugaFilmesCom.TFC_Menu_Filmes(artfolder)
elif mode == 78: TugaFilmesCom.TFC_Menu_Filmes_Por_Categorias(artfolder)
elif mode == 79:
        TugaFilmesCom.TFC_Menu_Filmes_Top_10(artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
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
elif mode == 90: TugaFilmesCom.TFC_Menu_Filmes_Por_Ano(artfolder)
#----------------------------------------------  MOVIETUGA  -------------------------------------------------------
elif mode == 100: print ""; Play.PLAY_movie(url,name,iconimage,checker,fanart)
elif mode == 101:
        MovieTuga.MVT_MenuPrincipal(artfolder)
        #setViewMode_menuMVT()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 102:
        MovieTuga.MVT_encontrar_fontes_filmes(url)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 103: MovieTuga.MVT_encontrar_videos_filmes(name,url)
elif mode == 104: MovieTuga.MVT_pesquisar_filmes()
elif mode == 105: MovieTuga.MVT_Menu_Filmes(artfolder)
elif mode == 106: MovieTuga.MVT_Menu_Filmes_Por_Categorias(artfolder)
elif mode == 107: MovieTuga.MVT_Menu_Filmes_Brevemente(artfolder)
elif mode == 108: TextBoxes.TBOX_TextBoxes_ChangeLog(url)
elif mode == 109: TextBoxes.TBOX_TextBoxes_Sinopse(url)
#-----------------------------------------------  Top-Pt.com  ------------------------------------------------------
#elif mode == 230: print ""; Play.PLAY_movie(url,name,iconimage,checker,fanart)
elif mode == 231:
        TopPt.TPT_MenuPrincipal(artfolder)
        #setViewMode_menuTPT()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 232:
        TopPt.TPT_encontrar_fontes_filmes(url,artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 233: TopPt.TPT_encontrar_videos_filmes(name,url,iconimage)
elif mode == 234: TopPt.TPT_pesquisar()
elif mode == 235: TopPt.TPT_resolve_videomega_filmes(url,conta_id_video)
elif mode == 236: TopPt.TPT_resolve_not_videomega_filmes(name,conta_id_video)
elif mode == 237: TopPt.TPT_Menu_Filmes(artfolder)
elif mode == 238:
        TopPt.TPT_Menu_Filmes_Por_Categorias(artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 239:
        TopPt.TPT_Menu_Filmes_Por_Ano(artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 240: TopPt.TPT_Menu_Series(artfolder)
elif mode == 241:
        TopPt.TPT_Menu_Series_A_a_Z(artfolder,url)
        #setViewMode_series_AZ_TPT()
        #xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 242: TopPt.TPT_encontrar_videos_series(name,url)
elif mode == 243: TopPt.TPT_resolve_not_videomega_series(name,url,id_video,nome_cada_episodio,src_href)
elif mode == 244: TopPt.TPT_encontrar_fontes_series_recentes(url)
elif mode == 245: TopPt.TPT_pesquisar_series()
elif mode == 246: TopPt.TPT_encontrar_fontes_pesquisa(url,pesquisou)
elif mode == 247: TopPt.TPT_encontrar_fontes_series_A_a_Z(url)
elif mode == 248: TopPt.TPT_Menu_Posts_Recentes(artfolder)
elif mode == 249: TopPt.TPT_encontrar_videos_series(name,url)
elif mode == 256: TextBoxes.TBOX_TextBoxes_ChangeLog(url)
elif mode == 257: TextBoxes.TBOX_TextBoxes_Sinopse(url)
elif mode == 258:
        TopPt.TPT_Menu_Top_Filmes(artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 259:
        TopPt.TPT_Menu_Top_Series(artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
#----------------------------------------------------------------ARMAGEDOM--------------------------------------------------------------------#
elif mode == 331: Armagedom.ARM_MenuPrincipal()
elif mode == 332: Armagedom.ARM_encontrar_fontes_filmes(url)
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
elif mode == 349: Armagedom.ARM_encontrar_fontes_filmes_MEGA_tv(url)
elif mode == 350: Armagedom.ARM_encontrar_fontes_filmes_M18()
elif mode == 351: Armagedom.ARM_encontrar_fontes_filmes_MEGA_net(url)
elif mode == 352: Armagedom.ARM_Menu_Filmes_Por_Categorias_MEGA_net()
elif mode == 353: Armagedom.ARM_encontrar_fontes_series_MEGA_net(url)
elif mode == 354: Armagedom.ARM_encontrar_videos_filmes_MEGA_NET(name,url)
elif mode == 355: Armagedom.ARM_encontrar_fontes_filmes_pesquisa_MEGA_net(url,nome_pesquisa)
elif mode == 356: Armagedom.ARM_Menu_Filmes_Por_Categorias_MEGA_tv()
elif mode == 357: Armagedom.ARM_encontrar_fontes_filmes_MEGASERIESONLINEHD(url)
elif mode == 358: Armagedom.ARM_Menu_Series_MEGASERIESONLINEHD()
elif mode == 359: Armagedom.ARM_encontrar_videos_filmes_MEGASERIESONLINEHD(name,url)
elif mode == 360: Armagedom.ARM_Menu_Series_MEGA_net()
#---------------------------------------------------------------   Filmes3D   -----------------------------------------------------------------#
elif mode == 400: print ""; Play.PLAY_movie(url,name,iconimage,checker,fanart)
elif mode == 401: Filmes3D.FILMES3D_MenuPrincipal(artfolder)
elif mode == 402: Filmes3D.FILMES3D_encontrar_fontes_filmes(url)
elif mode == 403: Filmes3D.FILMES3D_encontrar_videos_filmes(name,url)
elif mode == 404: Filmes3D.FILMES3D_pesquisar_filmes()
elif mode == 405: Filmes3D.FILMES3D_Menu_Filmes(artfolder)
elif mode == 406: Filmes3D.FILMES3D_Menu_Filmes_Por_Categorias(artfolder)
elif mode == 407: Filmes3D.FILMES3D_Menu_Filmes_Brevemente(artfolder)
#----------------------------------------------------------------   IMDB   --------------------------------------------------------------------#
elif mode == 500: Menu_IMDB()
elif mode == 501: Filmes_IMDB_antiga(url)
elif mode == 502: Filmes_Filmes_TFV(i)
elif mode == 503: Filmes_Filmes_TFC(i)
elif mode == 504: Filmes_Filmes_MVT(i)
elif mode == 505: Filmes_Filmes_TPT(i)
elif mode == 506: declara_variaveis(url)
#----------------------------------------------------------------------------------------------------------------------------------------------
elif mode == 507:
        Mashup.Filmes_Filmes_Filmes(url)
        #setViewMode_filmes()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 508:
        Mashup.ultimos_episodios(url)
        #setViewMode_filmes()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
#----------------------------------------------  FOITATUGA  -------------------------------------------------------
elif mode == 600: print ""; Play.PLAY_movie(url,name,iconimage,checker,fanart)
elif mode == 601:
        FoitaTuga.FTT_MenuPrincipal(artfolder)
        #setViewMode_menuFTT()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 602:
        FoitaTuga.FTT_encontrar_fontes_filmes(url)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 603: FoitaTuga.FTT_encontrar_videos_filmes(name,url)
elif mode == 604: FoitaTuga.FTT_pesquisar_filmes()
elif mode == 605: FoitaTuga.FTT_Menu_Filmes(artfolder)
elif mode == 606: FoitaTuga.FTT_Menu_Filmes_Por_Categorias(artfolder)
elif mode == 607: FoitaTuga.FTT_Menu_Filmes_Brevemente(artfolder)
elif mode == 608:
        FoitaTuga.FTT_Top_Vistos(artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
#----------------------------------------------  CINEMATUGA  -------------------------------------------------------
elif mode == 700: print ""; Play.PLAY_movie(url,name,iconimage,checker,fanart)#,nomeAddon)
elif mode == 701:
        Cinematuga.CMT_MenuPrincipal(artfolder)
        #setViewMode_menuCMT()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 702:
        Cinematuga.CMT_encontrar_fontes_filmes(url,artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 703: Cinematuga.CMT_encontrar_videos_filmes(name,url)
elif mode == 704: Cinematuga.CMT_pesquisar()
elif mode == 705: Cinematuga.CMT_resolve_videomega_filmes(url,conta_id_video)
elif mode == 706: Cinematuga.CMT_resolve_not_videomega_filmes(url,conta_id_video,conta_os_items,nomeescolha)
elif mode == 707: Cinematuga.CMT_Menu_Filmes(artfolder)
elif mode == 708:
        Cinematuga.CMT_Menu_Filmes_Por_Categorias(artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 709:
        Cinematuga.CMT_Menu_Filmes_Por_Ano(artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 710: Cinematuga.CMT_Menu_Series(artfolder)
elif mode == 711:
        Cinematuga.CMT_Menu_Series_A_a_Z(artfolder)
        setViewMode_series_AZ_CMT()
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 712: Cinematuga.CMT_encontrar_videos_series(name,url)
elif mode == 713: Cinematuga.CMT_resolve_not_videomega_series(name,url,id_video,nome_cada_episodio,src_href)
elif mode == 714:
        Cinematuga.CMT_encontrar_fontes_series_recentes(url)
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        xbmc.executebuiltin("Container.SetViewMode(500)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 715: Cinematuga.CMT_pesquisar_series()
elif mode == 716:
        Cinematuga.CMT_encontrar_fontes_pesquisa(url,pesquisou)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(500)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 717:
        Cinematuga.CMT_encontrar_fontes_series_A_a_Z(url)
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        xbmc.executebuiltin("Container.SetViewMode(500)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 718:
        Cinematuga.CMT_Menu_Filmes_Top_5(artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
#-------------------------------------------------------------------------------------------------------------------------

elif mode == 1000:
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        #xbmcplugin.endOfDirectory(int(sys.argv[1]))
        selfAddon.openSettings()
        #setViewMode_menuPrincipal()
        MAIN_MENU()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        #setViewMode_menuPrincipal()
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode == 1001:
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1002:
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1003:
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1004:
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1005:
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")


elif mode == 3000:
        MPOPULARES()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(515)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 3001:
        MVOTADOS()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(515)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 3002:
        NCINEMAS()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(515)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 3003:
        SERIES_MENU()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 3004:
        FILMES_MENU()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 3005:
        passar_nome_SERIES(name)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(500)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 3006:
        pesquisar_SERIES(name,url)
        #xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        #xbmc.executebuiltin("Container.SetViewMode(500)")
        #xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 3007:
        passar_nome_SERIES_IMDB(name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
