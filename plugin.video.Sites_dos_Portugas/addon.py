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




import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,urlparse,time,os,threading
import MovieTuga,TugaFilmesTV,TugaFilmesCom,M18,Pesquisar,Play,TopPt,FilmesAnima,Mashup,Armagedom,FoitaTuga,Cinematuga,CinematugaEu,CinemaEmCasa,Funcoes
import PesquisaExterna
from array import array
from string import capwords
from Funcoes import thetvdb_api, themoviedb_api, themoviedb_api_tv, theomapi_api, themoviedb_api_IMDB, themoviedb_api_IMDB_episodios, themoviedb_api_TMDB
from Funcoes import thetvdb_api_tvdbid, thetvdb_api_episodes, themoviedb_api_search_imdbcode, themoviedb_api_pagina, themoviedb_api_IMDB1, theomapi_api_nome
from Funcoes import addDir, addDir1, addDir2, addLink, addLink1, addDir_teste, addDir_trailer, addDir_episode, addDir_trailer1, addDir_episode1
from Funcoes import addDir_trailer1_filmes, addDir_trailer_filmes
from Funcoes import get_params,abrir_url

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
perfil = xbmc.translatePath(selfAddon.getAddonInfo('profile'))

progress = xbmcgui.DialogProgress()

TPT_ONOFF = []
TFV_ONOFF = []
TFC_ONOFF = []
MVT_ONOFF = []
FTT_ONOFF = []
CMC_ONOFF = []
CME_ONOFF = []
CMT_ONOFF = []

results = []
resultos = []

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENU    ------------------------------------------------------------------#

def MAIN_MENU():
##        if selfAddon.getSetting("AvisoFanart") == "true":
##                SdPpath = selfAddon.getAddonInfo('path')
##                d = AvisoFanart("AvisoFanart.xml" , SdPpath, "Default")
##                d.doModal()
##                del d
##                selfAddon.setSetting('AvisoFanart',value='false')
##        addDir('[B][COLOR green]T[/COLOR][COLOR yellow]M[/COLOR][COLOR red]DB[/COLOR][/B]','http://direct',3003,artfolder + 'SERIES1.png','nao','')
##        addDir('[B][COLOR green]I[/COLOR][COLOR yellow]M[/COLOR][COLOR red]DB[/COLOR][/B]','http://direct',3003,artfolder + 'SERIES1.png','nao','')
        addDir('[B][COLOR green]SÉ[/COLOR][COLOR yellow]R[/COLOR][COLOR red]IES[/COLOR][/B] (TMDB)','http://direct',3003,artfolder + 'SERIES1.png','nao','')
        addDir('[B][COLOR green]PRO[/COLOR][COLOR yellow]C[/COLOR][COLOR red]URAR[/COLOR] [COLOR green]SÉ[/COLOR][COLOR yellow]R[/COLOR][COLOR red]IES[/COLOR][/B] (TMDB)','1',3011,artfolder + 'P1.png','nao','')
        addDir('[B][COLOR green]FI[/COLOR][COLOR yellow]L[/COLOR][COLOR red]MES[/COLOR][/B] (TMDB)','http://direct',3004,artfolder + 'FILMES1.png','nao','')
        addDir('[B][COLOR green]PRO[/COLOR][COLOR yellow]C[/COLOR][COLOR red]URAR[/COLOR] [COLOR green]FI[/COLOR][COLOR yellow]L[/COLOR][COLOR red]MES[/COLOR][/B] (TMDB)','1',2998,artfolder + 'P1.png','nao','')
        addDir('[B][COLOR green]SÉ[/COLOR][COLOR yellow]R[/COLOR][COLOR red]IES[/COLOR][/B] (A/Z)','urlTODAS',26,artfolder + 'ST.png','nao','')                
        url_TFC = 'http://www.tuga-filmes.info/'
        url_MVT = 'http://www.movie-tuga.blogspot.pt'
        url_TFV = 'http://www.tuga-filmes.us/search/label/S%C3%A9ries'
        url_TPT = 'http://toppt.net/category/series/'
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "fim": 'fim',"xpto":'xpto'}
        url_ultimos_episodios = urllib.urlencode(parameters)
        addDir('[B][COLOR green]ÚLTIMO[/COLOR][COLOR yellow]S [/COLOR][COLOR red]EPISÓDIOS[/COLOR][/B]',url_ultimos_episodios,508,artfolder + 'UEP.png','nao','')
        #----------------------------
        url_toppt = 'http://toppt.net/'
        url_TFV = 'http://www.tuga-filmes.us/search/label/Filmes'
        url_TFC = 'http://www.tuga-filmes.info/'
        url_MVT = 'http://www.movie-tuga.blogspot.pt'
        url_FTT = 'http://foitatugacinemaonline.blogspot.pt/'
        url_CMT = 'http://www.cinematuga.net/search/label/Filmes'#'http://www.tugafilmes.org/search/label/Filmes'
        url_CME = 'http://www.cinematuga.eu/search/label/Filmes'
        url_CMC = 'http://www.cinemaemcasa.pt/'
        try:
                toppt_source = abrir_url(url_toppt)
        except: toppt_source = ''
        saber_url_todos = re.compile('<a href="(.+?)">filmes</a></li>').findall(toppt_source)
        if saber_url_todos: url_TPT = saber_url_todos[0]
        else: url_TPT = 'http://toppt.net/'
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "url_FTT": url_FTT, "url_CMT": url_CMT, "url_CME": url_CME, "url_CMC": url_CMC, "fim": 'fim',"xpto":'xpto'}
        url_filmes_filmes = urllib.urlencode(parameters)                                                     #507
        addDir('[B][COLOR green]ÚLTIM[/COLOR][COLOR yellow]O[/COLOR][COLOR red]S FILMES[/COLOR][/B]',url_filmes_filmes,10001,artfolder + 'UF.png','nao','')
        #----------------------------
        url_TFV = 'http://www.tuga-filmes.us/search/label/Anima%C3%A7%C3%A3o'
        url_TFC = 'http://www.tuga-filmes.info/search/label/Anima%C3%A7%C3%A3o?max-results=20'
        url_MVT = 'http://movie-tuga.blogspot.pt/search/label/animacao'
        url_FTT = 'http://foitatugacinemaonline.blogspot.pt/search/label/ANIMA%C3%87%C3%83O'
        url_CMT = 'http://www.cinematuga.net/search/label/Anima%C3%A7%C3%A3o'
        url_CME = 'http://www.cinematuga.eu/search/label/Anima%C3%A7%C3%A3o'
        url_CMC = 'http://www.cinemaemcasa.pt/search/label/Anima%C3%A7%C3%A3o'
        saber_url_animacao = re.compile('<a href="(.+?)">Animacao</a></li>').findall(toppt_source)
        if saber_url_animacao: url_TPT = saber_url_animacao[0]
        else: url_TPT = 'http://toppt.net/'
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "url_FTT": url_FTT, "url_CMT": url_CMT, "url_CME": url_CME, "url_CMC": url_CMC, "fim": 'fim',"xpto":'xpto'}
        url_filmes_animacao = urllib.urlencode(parameters)                                                          #6 #507
        addDir('[B][COLOR green]ÚLTIMO[/COLOR][COLOR yellow]S [/COLOR][COLOR red]ANIMAÇÃO[/COLOR][/B]',url_filmes_animacao,10001,artfolder + 'FA.png','nao','')
        #----------------------------
        #----------------------------------
        #addDir('[B][COLOR green]PRO[/COLOR][COLOR yellow]C[/COLOR][COLOR red]URAR[/COLOR][/B] (Filmes/Séries)','http://www.tuga-filmes.us/search?q=',1,artfolder + 'P1.png','nao','')
        addDir('[B][COLOR green]PRO[/COLOR][COLOR yellow]C[/COLOR][COLOR red]URAR[/COLOR][/B] (SITESdosPORTUGAS)','url',7500,artfolder + 'P1.png','nao','')
        
        addDir1('','url',1004,artfolder,False,'')
        addDir('[B][COLOR green]RA[/COLOR][COLOR yellow]T[/COLOR][COLOR red]OTV[/COLOR][/B] (Filmes/Séries)[COLOR blue] NOVO[/COLOR] W.I.P.','url',20001,artfolder,'nao','')        
        addDir('[B][COLOR green]SITES[/COLOR][COLOR yellow]dos[/COLOR][COLOR red]PORTUGAS[/COLOR][/B] (Filmes/Séries)','url',10000,artfolder + 'SDPI.png','nao','')
        addDir('[B][COLOR yellow]SITES[/COLOR][COLOR blue]dos[/COLOR][COLOR green]BRAZUCAS[/COLOR][/B] (Filmes/Séries)','url',331,artfolder + 'SDB.png','nao','')
        #addDir1('','url',1004,artfolder,False,'')
        #addDir('[B][COLOR green]DEFI[/COLOR][COLOR yellow]N[/COLOR][COLOR red]IÇÕES[/COLOR][/B] (ADDON)','url',1000,artfolder + 'DEF1.png','nao','')#'ze-icon3.png'
        
def ProcurarFilmesSeries():
        addDir('[B][COLOR green]PRO[/COLOR][COLOR yellow]C[/COLOR][COLOR red]URAR[/COLOR][/B] (Filmes)','http://www.tuga-filmes.us/search?q=',1,artfolder + 'P1.png','nao','')
        addDir('[B][COLOR green]PRO[/COLOR][COLOR yellow]C[/COLOR][COLOR red]URAR[/COLOR][/B] (Séries)','http://www.tuga-filmes.us/search?q=',1,artfolder + 'P1.png','nao','')
        addDir('[B][COLOR green]PRO[/COLOR][COLOR yellow]C[/COLOR][COLOR red]URAR[/COLOR][/B] (Filmes/Séries)','http://www.tuga-filmes.us/search?q=',1,artfolder + 'P1.png','nao','')


def SITESdosPORTUGAS():
        #####################################
        url_TPT = 'http://toppt.net/'
        url_TFV = 'http://www.tuga-filmes.us/'
        url_TFC = 'http://www.tuga-filmes.info/'
        url_MVT = 'http://www.movie-tuga.blogspot.pt'
        url_FTT = 'http://foitatugacinemaonline.blogspot.pt/'
        url_CMT = 'http://www.cinematuga.net/'#'http://www.tugafilmes.org'#'http://www.cinematuga.net/'
        url_CME = 'http://www.cinematuga.eu/'
        url_CMC = 'http://www.cinemaemcasa.pt/'

        threads = []

        TPT = threading.Thread(name='TPT', target=TPTONOFF , args=(url_TPT,))
        threads.append(TPT)

        CME = threading.Thread(name='CME', target=CMEONOFF , args=(url_CME,))
        threads.append(CME)

        TFC = threading.Thread(name='TFC', target=TFCONOFF , args=(url_TFC,))
        threads.append(TFC)
        
        FTT = threading.Thread(name='FTT', target=FTTONOFF , args=(url_FTT,))
        threads.append(FTT)
        
        TFV = threading.Thread(name='TFV', target=TFVONOFF , args=(url_TFV,))
        threads.append(TFV)
        
        MVT = threading.Thread(name='MVT', target=MVTONOFF , args=(url_MVT,))
        threads.append(MVT)
        
        CMT = threading.Thread(name='CMT', target=CMTONOFF , args=(url_CMT,))
        threads.append(CMT)

        CMC = threading.Thread(name='CMC', target=CMCONOFF , args=(url_CMC,))
        threads.append(CMC)

        [i.start() for i in threads]
        [i.join() for i in threads]

        addDir('[COLOR orange]FTT | [/COLOR][B][COLOR green]FOIT[/COLOR][COLOR yellow]A[/COLOR][COLOR red]TUGA[/COLOR][/B] (Filmes)'+FTT_ONOFF[0],'http://direct',601,artfolder + 'FTT1.png','nao','')
        addDir('[COLOR orange]TPT | [/COLOR][B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B] (Filmes/Séries)'+TPT_ONOFF[0],'http://direct',231,artfolder + 'TPT1.png','nao','')
        addDir('[COLOR orange]MVT | [/COLOR][B][COLOR green]MOV[/COLOR][COLOR yellow]I[/COLOR][COLOR red]ETUGA[/COLOR][/B] (Filmes)'+MVT_ONOFF[0],'http://direct',101,artfolder + 'MVT1.png','nao','')
        addDir('[COLOR orange]CMT | [/COLOR][B][COLOR green]CINE[/COLOR][COLOR yellow]M[/COLOR][COLOR red]ATUGA.net[/COLOR][/B] (Filmes)'+CMT_ONOFF[0],'http://direct',701,artfolder + 'CMT1.png','nao','')
        addDir('[COLOR orange]TFV | [/COLOR][B][COLOR green]TUGA-[/COLOR][COLOR yellow]F[/COLOR][COLOR red]ILMES.tv[/COLOR][/B] (Filmes/Séries)'+TFV_ONOFF[0],'http://direct',31,artfolder + 'TFV1.png','nao','')
        addDir('[COLOR orange]TFC | [/COLOR][B][COLOR green]TUGA-[/COLOR][COLOR yellow]F[/COLOR][COLOR red]ILMES.com[/COLOR][/B] (Filmes)'+TFC_ONOFF[0],'http://direct',71,artfolder + 'TFC1.png','nao','')
        addDir('[COLOR orange]CME | [/COLOR][B][COLOR green]CINE[/COLOR][COLOR yellow]M[/COLOR][COLOR red]ATUGA.eu[/COLOR][/B] (Filmes)'+CME_ONOFF[0],'http://direct',801,artfolder + 'CME1.png','nao','')
        addDir('[COLOR orange]CMC | [/COLOR][B][COLOR green]CINEM[/COLOR][COLOR yellow]A[/COLOR][COLOR red]EMCASA[/COLOR][/B] (Filmes)'+CMC_ONOFF[0],'http://direct',901,artfolder + 'CMC1.png','nao','')


def TFVONOFF(url_TFV):
        try:
		html_source = abrir_url(url_TFV)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []: TFV_ONOFF.append('[COLOR green] | UP[/COLOR]')
	else: TFV_ONOFF.append('[COLOR red] | DOWN[/COLOR]')
def TFCONOFF(url_TFC):	
	try:
		html_source = abrir_url(url_TFC)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
	if items != []: TFC_ONOFF.append('[COLOR green] | UP[/COLOR]')
	else: TFC_ONOFF.append('[COLOR red] | DOWN[/COLOR]')
def MVTONOFF(url_MVT):
	try:
		html_source = abrir_url(url_MVT)
	except: html_source = ''
	items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
	if items != []: MVT_ONOFF.append('[COLOR green] | UP[/COLOR]')
	else: MVT_ONOFF.append('[COLOR red] | DOWN[/COLOR]')
def TPTONOFF(url_TPT):
	try:
		html_source = abrir_url(url_TPT)
	except: html_source = ''
	items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	if items != []: TPT_ONOFF.append('[COLOR green] | UP[/COLOR]')
	else: TPT_ONOFF.append('[COLOR red] | DOWN[/COLOR]')
def FTTONOFF(url_FTT):
	try:
		html_source = abrir_url(url_FTT)
	except: html_source = ''
	items = re.findall("<div class='post-body entry-content'>(.+?)<div class='post-outer'>", html_source, re.DOTALL)
	if not items: items = re.findall("<div class='video-item'>(.*?)<div class='clear'>", html_source, re.DOTALL)
	if items != []: FTT_ONOFF.append('[COLOR green] | UP[/COLOR]')
	else: FTT_ONOFF.append('[COLOR red] | DOWN[/COLOR]')
def CMTONOFF(url_CMT):
	try:
		html_source = abrir_url(url_CMT)
	except: html_source = ''
	items = re.findall("<h3 class='post-title entry-title'(.*?)<span class='post-location'>", html_source, re.DOTALL)
	if not items: items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []: CMT_ONOFF.append('[COLOR green] | UP[/COLOR]')
	else: CMT_ONOFF.append('[COLOR red] | DOWN[/COLOR]')
def CMEONOFF(url_CME):
	try:
		html_source = abrir_url(url_CME)
	except: html_source = ''
	items = re.findall("<h3 class='post-title entry-title'(.+?)<div class='post-outer'>", html_source, re.DOTALL)
	if items != []: CME_ONOFF.append('[COLOR green] | UP[/COLOR]')
	else: CME_ONOFF.append('[COLOR red] | DOWN[/COLOR]')
def CMCONOFF(url_CMC):
	try:
		html_source = abrir_url(url_CMC)
	except: html_source = ''
	items = re.findall("<h2 class='post-title entry-title'>(.+?)<div class='post-footer'>", html_source, re.DOTALL)
	if items != []: CMC_ONOFF.append('[COLOR green] | UP[/COLOR]')
	else: CMC_ONOFF.append('[COLOR red] | DOWN[/COLOR]')
	#########################################
        
class AvisoFanart(xbmcgui.WindowXMLDialog):

    def __init__( self, *args, **kwargs ):
          xbmcgui.WindowXML.__init__(self)

    def onInit(self):
        pass
          
    def onClick(self,controlId):
        if controlId == 2001: self.close()

def FILMES_MENU():
##        url_toppt = 'http://toppt.net/'
##        url_TFV = 'http://www.tuga-filmes.us/search/label/Filmes'
##        url_TFC = 'http://www.tuga-filmes.info/'
##        url_MVT = 'http://www.movie-tuga.blogspot.pt'
##        url_FTT = 'http://foitatugacinemaonline.blogspot.pt/'
##        url_CMT = 'http://www.cinematuga.net/search/label/Filmes'#'http://www.tugafilmes.org/search/label/Filmes'
##        url_CME = 'http://www.cinematuga.eu/search/label/Filmes'
##        url_CMC = 'http://www.cinemaemcasa.pt/'
##        try:
##                toppt_source = abrir_url(url_toppt)
##        except: toppt_source = ''
##        saber_url_todos = re.compile('<a href="(.+?)">filmes</a></li>').findall(toppt_source)
##        if saber_url_todos: url_TPT = saber_url_todos[0]
##        else: url_TPT = 'http://toppt.net/'
##        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "url_FTT": url_FTT, "url_CMT": url_CMT, "url_CME": url_CME, "url_CMC": url_CMC, "fim": 'fim',"xpto":'xpto'}
##        url_filmes_filmes = urllib.urlencode(parameters)                                                     #507
##        addDir('[B][COLOR green]TO[/COLOR][COLOR yellow]D[/COLOR][COLOR red]OS[/COLOR][/B]',url_filmes_filmes,10001,artfolder + 'FT.png','nao','')
##        #----------------------------
##        url_TFV = 'http://www.tuga-filmes.us/search/label/Anima%C3%A7%C3%A3o'
##        url_TFC = 'http://www.tuga-filmes.info/search/label/Anima%C3%A7%C3%A3o?max-results=20'
##        url_MVT = 'http://movie-tuga.blogspot.pt/search/label/animacao'
##        url_FTT = 'http://foitatugacinemaonline.blogspot.pt/search/label/ANIMA%C3%87%C3%83O'
##        url_CMT = 'http://www.cinematuga.net/search/label/Anima%C3%A7%C3%A3o'
##        url_CME = 'http://www.cinematuga.eu/search/label/Anima%C3%A7%C3%A3o'
##        url_CMC = 'http://www.cinemaemcasa.pt/search/label/Anima%C3%A7%C3%A3o'
##        saber_url_animacao = re.compile('<a href="(.+?)">Animacao</a></li>').findall(toppt_source)
##        if saber_url_animacao: url_TPT = saber_url_animacao[0]
##        else: url_TPT = 'http://toppt.net/'
##        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "url_FTT": url_FTT, "url_CMT": url_CMT, "url_CME": url_CME, "url_CMC": url_CMC, "fim": 'fim',"xpto":'xpto'}
##        url_filmes_animacao = urllib.urlencode(parameters)                                                          #6 #507
##        addDir('[B][COLOR green]ANI[/COLOR][COLOR yellow]M[/COLOR][COLOR red]AÇÃO[/COLOR][/B]',url_filmes_animacao,10001,artfolder + 'FA.png','nao','')
        #----------------------------
        addDir('[B][COLOR green]NOS[/COLOR][COLOR yellow] C[/COLOR][COLOR red]INEMAS[/COLOR][/B] (Filmes)','1',3002,artfolder + 'NC.png','nao','')
        addDir('[B][COLOR green]MAIS[/COLOR][COLOR yellow] V[/COLOR][COLOR red]OTADOS[/COLOR][/B] (Filmes)','1',3001,artfolder + 'FMV.png','nao','')
        addDir('[B][COLOR green]MAIS P[/COLOR][COLOR yellow]O[/COLOR][COLOR red]PULARES[/COLOR][/B] (Filmes)','1',3000,artfolder + 'MP.png','nao','')
        addDir('[B][COLOR green]BREV[/COLOR][COLOR yellow]E[/COLOR][COLOR red]MENTE[/COLOR][/B] (Filmes)','1',2999,artfolder,'nao','')
        addDir('[B][COLOR green]PRO[/COLOR][COLOR yellow]C[/COLOR][COLOR red]URAR[/COLOR][/B] (Filmes)','1',2998,artfolder + 'P1.png','nao','')

def dirtodos(url):
        try: xbmcgui.Dialog().notification('A Procurar Últimos Filmes.', 'Por favor aguarde...', artfolder + 'SDPI.png', 10000, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, 10000, %s)" % ('A Procurar Últimos Filmes.', 'Por favor aguarde...', artfolder + 'SDPI.png'))

        urlss = urllib.unquote(url)
        print urlss
        #addLink(urlss,'','','')
        #return
        urls=re.compile('url_TFC=(.+?)&url_CMT=(.+?)&url_FTT=(.+?)&url_TFV=(.+?)&url_CMC=(.+?)&url_MVT=(.+?)&xpto=xpto&url_CME=(.+?)&url_TPT=(.+?)&fim=fim').findall(urlss)
        url_TFV = urls[0][3]
        url_TFC = urls[0][0]
        url_MVT = urls[0][5]
        url_TPT = urls[0][7]
        url_FTT = urls[0][2]
        url_CMT = urls[0][1]
        url_CME = urls[0][6]
        url_CMC = urls[0][4]
        
##        percent = 0
##        message = 'Por favor aguarde.'
##        progress.create('Progresso', 'A Procurar')
##        progress.update( percent, 'A Procurar Filmes...', message, "" )

        threads = []
        i = 0
        try:
                try:
                        html_source = abrir_url(url_TPT)
                except: html_source = ''
                itemsTPT = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
                if itemsTPT != []:
                        proxima_TPT = re.compile('</span><a class="nextpostslink" rel="next" href="(.+?)">&raquo;</a><a class="last"').findall(html_source)
                        try:
                                url_TPT = proxima_TPT[0].replace('#038;','').replace('&amp;','&')
                        except: pass
                else: url_TPT = 'http:'

                for item in itemsTPT:
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        TPT = threading.Thread(name='TPT'+str(i), target=Mashup.TPTMASHUP , args=('FILME'+str(a)+'FILME'+item,))
                        threads.append(TPT)
        except: pass
        i = 0
        try:
                try:
                        html_source = abrir_url(url_TFV)
                except: html_source = ''
                itemsTFV = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
                if itemsTFV != []:
                        try:
                                proxima_TFV = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
                                url_TFV = proxima_TFV[0].replace('&amp;','&')
                        except: pass
                else: url_TFV = 'http:'

                for item in itemsTFV:
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        TFV = threading.Thread(name='TFV'+str(i), target=Mashup.TFVMASHUP , args=('FILME'+str(a)+'FILME'+item,))
                        threads.append(TFV)
        except: pass
        i = 0
        try:
                try:
                        html_source = abrir_url(url_CME)
                except: html_source = ''
                itemsCME = re.findall("<h3 class='post-title entry-title'(.+?)<div class='post-outer'>", html_source, re.DOTALL)
                if itemsCME != []:
                        proxima_CME = re.compile("<a class='blog-pager-older-link' href='(.+?)' id='Blog1_blog-pager-older-link'").findall(html_source)	
                        try:
                                url_CME = proxima_CME[0].replace('&amp;','&')
                        except: pass
                else: url_CME = 'http:'

                for item in itemsCME:
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        CME = threading.Thread(name='CME'+str(i), target=Mashup.CMEMASHUP , args=('FILME'+str(a)+'FILME'+item,))
                        threads.append(CME)
        except: pass
        i = 0
        try:
                try:
                        html_source = abrir_url(url_TFC)
                except: html_source = ''
                itemsTFC = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
                if itemsTFC != []:
                        try:
                                proxima_TFC = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
                                url_TFC = proxima_TFC[0].replace('&amp;','&')
                        except: pass
                else: url_TFC = 'http:'

                for item in itemsTFC:
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        TFC = threading.Thread(name='TFC'+str(i), target=Mashup.TFCMASHUP , args=('FILME'+str(a)+'FILME'+item,))
                        threads.append(TFC)
        except: pass
        i = 0
        try:
                try:
                        html_source = abrir_url(url_MVT)
                except: html_source = ''
                itemsMVT = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
                if itemsMVT != []:
                        proxima_MVT = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
                        try:
                                url_MVT = proxima_MVT[0].replace('%3A',':')
                                url_MVT = proxima_MVT[0].replace('&amp;','&')
                        except: pass
                else: url_MVT = 'http:'

                for item in itemsMVT:
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        MVT = threading.Thread(name='MVT'+str(i), target=Mashup.MVTMASHUP , args=('FILME'+str(a)+'FILME'+item,))
                        threads.append(MVT)
        except: pass
        i = 0
        try:
                try:
                        html_source = abrir_url(url_FTT)
                except: html_source = ''
                itemsFTT = re.findall("<a class='comment-link'(.+?)<div class='post-outer'>", html_source, re.DOTALL)
                if not itemsFTT: itemsFTT = re.findall("<div class='video-item'>(.*?)<div class='clear'>", html_source, re.DOTALL)
                if itemsFTT != []:
                        try:
                                proxima = re.compile("<a class='blog-pager-older-link' href='(.+?)' id='Blog1_blog-pager-older-link'").findall(html_source)
                                proxima_p = proxima[0]
                                url_FTT = proxima_p.replace('&amp;','&')
                        except: pass
                else: url_FTT = 'http:'

                for item in itemsFTT:
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        FTT = threading.Thread(name='FTT'+str(i), target=Mashup.FTTMASHUP , args=('FILME'+str(a)+'FILME'+item,))
                        threads.append(FTT)
        except: pass
        i = 0
        try:
                try:
                        html_source = abrir_url(url_CMT)
                except: html_source = ''
                itemsCMT = re.findall("<h3 class='post-title entry-title'(.*?)<span class='post-location'>", html_source, re.DOTALL)
                if not itemsCMT: itemsCMT = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
                if itemsCMT != []:
                        try:
                                proxima = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
                                url_CMT = proxima[0].replace('&amp;','&')
                        except: pass
                else: url_CMT = 'http:'

                for item in itemsCMT:
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        CMT = threading.Thread(name='CMT'+str(i), target=Mashup.CMTMASHUP , args=('FILME'+str(a)+'FILME'+item,))
                        threads.append(CMT)
        except: pass
        i = 0
        try:
                try:
                        html_source = abrir_url(url_CMC)
                except: html_source = ''
                itemsCMC = re.findall("<h2 class='post-title entry-title'>(.+?)<div class='post-footer'>", html_source, re.DOTALL)
                if itemsCMC != []:
                        proxima_CMC = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
                        try:
                                url_CMC = proxima_CMC[0].replace('&amp;','&').replace('%3A',':')
                        except: pass
                else: url_CMC = 'http:'

                for item in itemsCMC:
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        CMC = threading.Thread(name='CMC'+str(i), target=Mashup.CMCMASHUP , args=('FILME'+str(a)+'FILME'+item,))
                        threads.append(CMC)
        except: pass

        [i.start() for i in threads]

        [i.join() for i in threads]
        
        #######################################################################################
        
        _sites_ = ['filmesTPT.txt','filmesCME.txt','filmesFTT.txt','filmesTFC.txt','filmesMVT.txt','filmesCMTnet.txt','filmesCMC.txt','filmesTFV.txt']
        folder = perfil
        num_filmes = 0
        num_filmes = len(threads)
        for site in _sites_:
                _filmes_ = []
                try:
                        Filmes_Fi = open(folder + site, 'r')
                        read_Filmes_File = ''
                        for line in Filmes_Fi:
                                read_Filmes_File = read_Filmes_File + line
                                if line!='':_filmes_.append(line)

                        for x in range(len(_filmes_)):
                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_filmes_[x])
                                if _n: nome = _n[0]
                                else: nome = '---'
                                _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_filmes_[x])
                                if _i: imdbcode = _i[0]
                                else: imdbcode = '---'
                                urltrailer = re.compile('(.+?)IMDB.+?MDB').findall(imdbcode)
                                if urltrailer: urltrailer = urltrailer[0]
                                else: urltrailer = '---'
                                _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_filmes_[x])
                                if _t: thumb = _t[0]
                                else: thumb = '---'
                                _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_filmes_[x])
                                if _a: ano_filme = _a[0]
                                else: ano_filme = '---'
                                _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_filmes_[x])
                                if _f: fanart = _f[0]
                                else: fanart = ''
                                if fanart == '---': fanart = ''
                                _g = re.compile('[|]GENERO[|](.+?)[|]ONOME[|]').findall(_filmes_[x])
                                if _g: genero = _g[0]
                                else: genero = '---'
                                _o = re.compile('[|]ONOME[|](.+?)[|]SINOPSE[|]').findall(_filmes_[x])
                                if _o: O_Nome = _o[0]
                                else: O_Nome = '---'
                                _p = re.compile('PAGINA[|](.+?)[|]PAGINA').findall(_filmes_[x])
                                if _p: P_url = _p[0]
                                else: P_url = '---'
                                _s = re.compile('[|]SINOPSE[|](.*)').findall(_filmes_[x])
                                if _s: s = _s[0]
                                if '|END|' in s: sinopse = s.replace('|END|','')
                                else:
                                        si = re.compile('SINOPSE[|](.+?)\n(.+?)[|]END[|]').findall(_filmes_[x])
                                        if si: sinopse = si[0][0] + ' ' + si[0][1]
                                        else: sinopse = '---'
                                if 'toppt.net'         in imdbcode:
                                        num_mode = 233
                                        site = 'TPT'
                                if 'tuga-filmes.info'  in imdbcode:
                                        num_mode = 73
                                        site = 'TFC'
                                if 'tuga-filmes.us'    in imdbcode:
                                        num_mode = 33
                                        site = 'TFV'
                                if 'cinematuga.eu'     in imdbcode:
                                        num_mode = 803
                                        site = 'CME'
                                if 'cinematuga.net'    in imdbcode:
                                        num_mode = 703
                                        site = 'CMT'
                                if 'foitatuga'         in imdbcode:
                                        num_mode = 603
                                        site = 'FTT'
                                if 'cinemaemcasa.pt'   in imdbcode:
                                        num_mode = 903
                                        site = 'CMC'
                                if 'movietuga'         in imdbcode:
                                        num_mode = 103
                                        site = 'MVT'
                                if nome != '---':
                                        num_mode = 9004
                                        #addDir_trailer1_filmes(nome,imdbcode,num_mode,thumb,sinopse,fanart,ano_filme,genero,O_Nome,urltrailer,'Movies'+site,num_filmes)
                                        addDir_trailer1(nome,imdbcode,num_mode,thumb,sinopse,fanart,ano_filme,genero,O_Nome,urltrailer,'Movies'+site,num_filmes)
                                        #addDir_trailer1_filmes(nome,imdbcode,7,thumb,sinopse,fanart,ano_filme,genero,O_Nome,urltrailer,'Movies',num_filmes)
                                else:
                                        if 'toppt.net'         in P_url: url_TPT = P_url
                                        if 'tuga-filmes.info'  in P_url: url_TFC = P_url
                                        if 'tuga-filmes.us'    in P_url: url_TFV = P_url
                                        if 'cinematuga.eu'     in P_url: url_CME = P_url
                                        if 'cinematuga.net'    in P_url: url_CMT = P_url
                                        if 'foitatuga'         in P_url: url_FTT = P_url
                                        if 'cinemaemcasa.pt'   in P_url: url_CMC = P_url
                                        if 'movie-tuga'        in P_url: url_MVT = P_url
                                xbmc.sleep(12)
                        Filmes_Fi.close()
                except: pass

        #################################################################################

##        num_total = num_filmes + 0.0
##        progress.create('[B][COLOR green]SITES[/COLOR][COLOR yellow]dos[/COLOR][COLOR red]PORTUGAS[/COLOR][/B]', '')
##        for a in range(num_filmes):
##                percent = int( ( a / num_total ) * 100)
##                message = str(a+1) + " de " + str(num_filmes)
##                progress.update( percent, 'A Finalizar ...', message, "" )
##                xbmc.sleep(12)
                
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "url_FTT": url_FTT, "url_CMT": url_CMT, "url_CME": url_CME, "url_CMC": url_CMC, "fim": 'fim',"xpto":'xpto'}
        url_filmes_filmes = urllib.urlencode(parameters)
        #progress.close()
        addDir('[B]Página Seguinte >>[/B]',url_filmes_filmes,10001,artfolder + 'PAGS1.png','','')
        
        #addLink(str(CME)+str(threading.active_count()),'','','')
        xbmcplugin.setContent(int(sys.argv[1]), 'livetv')#movies
        xbmc.executebuiltin("Container.SetViewMode(560)")#503
        #xbmcplugin.endOfDirectory(int(sys.argv[1]))

def procurarOnde(mvoutv, namet, url, year, urltrailer, name, iconimage):
        mv = mvoutv
        nmt = namet
        ur = url
        ye = year
        utr = urltrailer
        nm = name
        ico = iconimage
        _nomeproc_ = []
        _nomeproc_.append('[B][COLOR white]GENESIS[/COLOR][/B]')
        _nomeproc_.append('[B][COLOR white]SITESdosPORTUGAS[/COLOR][/B] | TODOS')
        _nomeproc_.append('[B][COLOR white]SITESdosPORTUGAS[/COLOR][/B] | TOPPT.NET')
        _nomeproc_.append('[B][COLOR white]SITESdosPORTUGAS[/COLOR][/B] | TUGA-FILMES.COM')
        _nomeproc_.append('[B][COLOR white]SITESdosPORTUGAS[/COLOR][/B] | TUGA-FILMES.TV')
        _nomeproc_.append('[B][COLOR white]SITESdosPORTUGAS[/COLOR][/B] | CINEMATUGA.EU')
        _nomeproc_.append('[B][COLOR white]SITESdosPORTUGAS[/COLOR][/B] | CINEMATUGA.NET')
        _nomeproc_.append('[B][COLOR white]SITESdosPORTUGAS[/COLOR][/B] | FOITATUGA')
        _nomeproc_.append('[B][COLOR white]SITESdosPORTUGAS[/COLOR][/B] | CINEMAEMCASA')
        _nomeproc_.append('[B][COLOR white]SITESdosPORTUGAS[/COLOR][/B] | MOVIETUGA')
        _nummode_ = [0,1,233,73,33,803,703,603,903,103]

        indexservidores = xbmcgui.Dialog().select
        index = indexservidores('Procurar streams em:', _nomeproc_)
        if index > -1:
                if 'GENESIS' in _nomeproc_[index]: Funcoes.playparser(namet, url, year, urltrailer)
                elif 'TODOS' in _nomeproc_[index]:                        
                        if mvoutv == 'MoviesTPT':
                                mvoutv = 'Movies'
                                TopPt.TPT_encontrar_videos_filmes(name,url,iconimage,mvoutv)
                        elif mvoutv == 'MoviesTFC':
                                mvoutv = 'Movies'
                                TugaFilmesCom.TFC_encontrar_videos_filmes(name,url,mvoutv)
                        elif mvoutv == 'MoviesTFV':
                                mvoutv = 'Movies'
                                TugaFilmesTV.TFV_encontrar_videos_filmes(name,url,mvoutv)
                        elif mvoutv == 'MoviesCME':
                                mvoutv = 'Movies'
                                CinematugaEu.CME_encontrar_videos_filmes(name,url,mvoutv)
                        elif mvoutv == 'MoviesCMT':
                                mvoutv = 'Movies'
                                Cinematuga.CMT_encontrar_videos_filmes(name,url,mvoutv)
                        elif mvoutv == 'MoviesFTT':
                                mvoutv = 'Movies'
                                FoitaTuga.FTT_encontrar_videos_filmes(name,url,mvoutv)
                        elif mvoutv == 'MoviesCMC':
                                mvoutv = 'Movies'
                                CinemaEmCasa.CMC_encontrar_videos_filmes(name,url,mvoutv)
                        elif mvoutv == 'MoviesMVT':
                                mvoutv = 'Movies'
                                MovieTuga.MVT_encontrar_videos_filmes(name,url,mvoutv)
                        elif mvoutv == 'MoviesRTV':
                                FilmesAnima.FILMES_ANIMACAO_pesquisar(namet,'',url)
                elif 'TOPPT.NET' in _nomeproc_[index]:
                        if mvoutv != 'MoviesTPT':
                                if mvoutv=='MoviesTFC':
                                        strstr,url = TFCmovies(name,url)
                                elif mvoutv=='MoviesFTT':
                                        strstr,url = FTTmovies(name,url)
                                elif mvoutv=='MoviesTFV':
                                        strstr,url = TFVmovies(name,url)
                                elif mvoutv=='MoviesMVT':
                                        strstr,url = MVTmovies(name,url)
                                elif mvoutv=='MoviesCME':
                                        strstr,url = CMEmovies(name,url)
                                elif mvoutv=='MoviesCMT':
                                        strstr,url = CMTmovies(name,url)
                                elif mvoutv=='MoviesCMC':
                                        strstr,url = CMCmovies(name,url)
                                elif mvoutv=='MoviesRTV':
                                        strstr,url = RTVmovies(namet,url)
                                FilmesAnima.FILMES_ANIMACAO_pesquisar(strstr,'siteTPT',url)     
                        else: TopPt.TPT_encontrar_videos_filmes(name,url,iconimage,mvoutv)
                elif 'TUGA-FILMES.COM' in _nomeproc_[index]:
                        if mvoutv != 'MoviesTFC':
                                if mvoutv=='MoviesTPT':
                                        strstr,url = TPTmovies(name,url,iconimage)
                                elif mvoutv=='MoviesFTT':
                                        strstr,url = FTTmovies(name,url)
                                elif mvoutv=='MoviesTFV':
                                        strstr,url = TFVmovies(name,url)
                                elif mvoutv=='MoviesMVT':
                                        strstr,url = MVTmovies(name,url)
                                elif mvoutv=='MoviesCME':
                                        strstr,url = CMEmovies(name,url)
                                elif mvoutv=='MoviesCMT':
                                        strstr,url = CMTmovies(name,url)
                                elif mvoutv=='MoviesCMC':
                                        strstr,url = CMCmovies(name,url)
                                elif mvoutv=='MoviesRTV':
                                        strstr,url = RTVmovies(namet,url)
                                FilmesAnima.FILMES_ANIMACAO_pesquisar(strstr,'siteTFC',url)
                        else: TugaFilmesCom.TFC_encontrar_videos_filmes(name,url,mvoutv)
                elif 'TUGA-FILMES.TV' in _nomeproc_[index]:
                        if mvoutv != 'MoviesTFV':
                                if mvoutv=='MoviesTPT':
                                        strstr,url = TPTmovies(name,url,iconimage)
                                elif mvoutv=='MoviesFTT':
                                        strstr,url = FTTmovies(name,url)
                                elif mvoutv=='MoviesTFC':
                                        strstr,url = TFCmovies(name,url)
                                elif mvoutv=='MoviesMVT':
                                        strstr,url = MVTmovies(name,url)
                                elif mvoutv=='MoviesCME':
                                        strstr,url = CMEmovies(name,url)
                                elif mvoutv=='MoviesCMT':
                                        strstr,url = CMTmovies(name,url)
                                elif mvoutv=='MoviesCMC':
                                        strstr,url = CMCmovies(name,url)
                                elif mvoutv=='MoviesRTV':
                                        strstr,url = RTVmovies(namet,url)
                                FilmesAnima.FILMES_ANIMACAO_pesquisar(strstr,'siteTFV',url)
                        else: TugaFilmesTV.TFV_encontrar_videos_filmes(name,url,mvoutv)
                elif 'CINEMATUGA.EU' in _nomeproc_[index]:
                        if mvoutv != 'MoviesCME':
                                if mvoutv=='MoviesTPT':
                                        strstr,url = TPTmovies(name,url,iconimage)
                                elif mvoutv=='MoviesFTT':
                                        strstr,url = FTTmovies(name,url)
                                elif mvoutv=='MoviesTFV':
                                        strstr,url = TFVmovies(name,url)
                                elif mvoutv=='MoviesMVT':
                                        strstr,url = MVTmovies(name,url)
                                elif mvoutv=='MoviesTFC':
                                        strstr,url = TFCmovies(name,url)
                                elif mvoutv=='MoviesCMT':
                                        strstr,url = CMTmovies(name,url)
                                elif mvoutv=='MoviesCMC':
                                        strstr,url = CMCmovies(name,url)
                                elif mvoutv=='MoviesRTV':
                                        strstr,url = RTVmovies(namet,url)
                                FilmesAnima.FILMES_ANIMACAO_pesquisar(strstr,'siteCME',url)
                        else: CinematugaEu.CME_encontrar_videos_filmes(name,url,mvoutv)
                elif 'CINEMATUGA.NET' in _nomeproc_[index]:
                        if mvoutv != 'MoviesCMT':
                                if mvoutv=='MoviesTPT':
                                        strstr,url = TPTmovies(name,url,iconimage)
                                elif mvoutv=='MoviesFTT':
                                        strstr,url = FTTmovies(name,url)
                                elif mvoutv=='MoviesTFV':
                                        strstr,url = TFVmovies(name,url)
                                elif mvoutv=='MoviesMVT':
                                        strstr,url = MVTmovies(name,url)
                                elif mvoutv=='MoviesCME':
                                        strstr,url = CMEmovies(name,url)
                                elif mvoutv=='MoviesTFC':
                                        strstr,url = TFCmovies(name,url)
                                elif mvoutv=='MoviesCMC':
                                        strstr,url = CMCmovies(name,url)
                                elif mvoutv=='MoviesRTV':
                                        strstr,url = RTVmovies(namet,url)
                                FilmesAnima.FILMES_ANIMACAO_pesquisar(strstr,'siteCMT',url)
                        else: Cinematuga.CMT_encontrar_videos_filmes(name,url,mvoutv)
                elif 'FOITATUGA' in _nomeproc_[index]:
                        if mvoutv != 'MoviesFTT':
                                if mvoutv=='MoviesTPT':
                                        strstr,url = TPTmovies(name,url,iconimage)
                                elif mvoutv=='MoviesTFC':
                                        strstr,url = FTTmovies(name,url)
                                elif mvoutv=='MoviesTFV':
                                        strstr,url = TFVmovies(name,url)
                                elif mvoutv=='MoviesMVT':
                                        strstr,url = TFCmovies(name,url)
                                elif mvoutv=='MoviesCME':
                                        strstr,url = CMEmovies(name,url)
                                elif mvoutv=='MoviesCMT':
                                        strstr,url = CMTmovies(name,url)
                                elif mvoutv=='MoviesCMC':
                                        strstr,url = CMCmovies(name,url)
                                elif mvoutv=='MoviesRTV':
                                        strstr,url = RTVmovies(namet,url)
                                FilmesAnima.FILMES_ANIMACAO_pesquisar(strstr,'siteFTT',url)
                        else: FoitaTuga.FTT_encontrar_videos_filmes(name,url,mvoutv)
                elif 'CINEMAEMCASA' in _nomeproc_[index]:
                        if mvoutv != 'MoviesCMC':
                                if mvoutv=='MoviesTPT':
                                        strstr,url = TPTmovies(name,url,iconimage)
                                elif mvoutv=='MoviesFTT':
                                        strstr,url = FTTmovies(name,url)
                                elif mvoutv=='MoviesTFV':
                                        strstr,url = TFVmovies(name,url)
                                elif mvoutv=='MoviesMVT':
                                        strstr,url = MVTmovies(name,url)
                                elif mvoutv=='MoviesCME':
                                        strstr,url = CMEmovies(name,url)
                                elif mvoutv=='MoviesCMT':
                                        strstr,url = CMTmovies(name,url)
                                elif mvoutv=='MoviesTFC':
                                        strstr,url = TFCmovies(name,url)
                                elif mvoutv=='MoviesRTV':
                                        strstr,url = RTVmovies(namet,url)
                                FilmesAnima.FILMES_ANIMACAO_pesquisar(strstr,'siteCMC',url)
                        else: CinemaEmCasa.CMC_encontrar_videos_filmes(name,url,mvoutv)
                elif 'MOVIETUGA' in _nomeproc_[index]:
                        if mvoutv != 'MoviesMVT':
                                if mvoutv=='MoviesTPT':
                                        strstr,url = TPTmovies(name,url,iconimage)
                                elif mvoutv=='MoviesFTT':
                                        strstr,url = FTTmovies(name,url)
                                elif mvoutv=='MoviesTFV':
                                        strstr,url = TFVmovies(name,url)
                                elif mvoutv=='MoviesTFC':
                                        strstr,url = MVTmovies(name,url)
                                elif mvoutv=='MoviesCME':
                                        strstr,url = CMEmovies(name,url)
                                elif mvoutv=='MoviesCMT':
                                        strstr,url = CMTmovies(name,url)
                                elif mvoutv=='MoviesCMC':
                                        strstr,url = CMCmovies(name,url)
                                elif mvoutv=='MoviesRTV':
                                        strstr,url = RTVmovies(namet,url)
                                FilmesAnima.FILMES_ANIMACAO_pesquisar(strstr,'siteMVT',url)
                        else: MovieTuga.MVT_encontrar_videos_filmes(name,url,mvoutv)
        #if 'PROCUROU' in name or 'PROCURAR' in name:
       # addLink(name,'','','')
        #procurarOnde(mv, nmt, ur, ye, utr, nm, ico)

def MenuFilmesRato():
        addDir('[B][COLOR green]T[/COLOR][COLOR yellow]O[/COLOR][COLOR red]DOS[/COLOR][/B] (Filmes)','http://www.ratotv.net/movies/page/1/',20000,artfolder + 'FT.png','nao','')
        addDir('[B][COLOR green]MAIS[/COLOR][COLOR yellow] V[/COLOR][COLOR red]OTADOS[/COLOR][/B] (Filmes)','http://www.ratotv.net/',20002,artfolder + 'FMV.png','nao','')
        addDir('[B][COLOR green]MAIS[/COLOR][COLOR yellow] P[/COLOR][COLOR red]OPULARES[/COLOR][/B] (Filmes)','http://www.ratotv.net/',20002,artfolder + 'MP.png','nao','')
        addDir('[B][COLOR green]MAIS[/COLOR][COLOR yellow] R[/COLOR][COLOR red]ECENTES[/COLOR][/B] (Filmes)','http://www.ratotv.net/',20002,artfolder,'nao','')
        addDir('[B][COLOR green]MAIS[/COLOR][COLOR yellow] V[/COLOR][COLOR red]ISTOS[/COLOR][/B] (Filmes)','http://www.ratotv.net/',20002,artfolder,'nao','')
        #addDir('[B][COLOR green]PRO[/COLOR][COLOR yellow]C[/COLOR][COLOR red]URAR[/COLOR][/B] (Filmes)','1',2998,artfolder + 'P1.png','nao','')
        addDir1('','url',1004,artfolder,False,'')
        addDir('[B][COLOR green]T[/COLOR][COLOR yellow]O[/COLOR][COLOR red]DAS[/COLOR][/B] (Séries)','http://www.ratotv.net/tvshows/page/1/',20003,artfolder + 'FT.png','nao','')
        addDir('[B][COLOR green]MAIS[/COLOR][COLOR yellow] V[/COLOR][COLOR red]OTADAS[/COLOR][/B] (Séries)','http://www.ratotv.net/',20002,artfolder + 'FMV.png','nao','')
        addDir('[B][COLOR green]MAIS[/COLOR][COLOR yellow] P[/COLOR][COLOR red]OPULARES[/COLOR][/B] (Séries)','http://www.ratotv.net/',20002,artfolder + 'MP.png','nao','')
        addDir('[B][COLOR green]MAIS[/COLOR][COLOR yellow] R[/COLOR][COLOR red]ECENTES[/COLOR][/B] (Séries)','http://www.ratotv.net/',20002,artfolder,'nao','')
        addDir('[B][COLOR green]MAIS[/COLOR][COLOR yellow] V[/COLOR][COLOR red]ISTAS[/COLOR][/B] (Séries)','http://www.ratotv.net/',20002,artfolder,'nao','')
        #addDir('[B][COLOR green]PRO[/COLOR][COLOR yellow]C[/COLOR][COLOR red]URAR[/COLOR][/B] (Séries)','1',2998,artfolder + 'P1.png','nao','')

def tvoumv(name,url):
        try: xbmcgui.Dialog().notification('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png', 3000, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % ('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png'))
        
        i=0
        _fs_ =[]
        resultos=[]
        results=[]
        threads=[]
        
        if 'Filmes' in name:
                FilmesOuSeries = 'Filmes'
        elif 'Séries' in name:
                FilmesOuSeries = 'Séries'
                
        try: html_source = abrir_url(url)
	except: html_source = ''
	
        name = name.replace('[COLOR yellow]','').replace('[COLOR red]','').replace('[/COLOR]','')
	if 'Filmes' in name and 'VISTOS' in name:
		pasta = False
		mode = 3
		html_source_trunk = re.findall('<div id="viewed">(.*?)<div id="rated">', html_source, re.DOTALL)
	elif 'Filmes' in name and 'POPULARES' in name:
		pasta = False
		mode = 3
		html_source_trunk = re.findall('<div id="popular">(.*?)<div id="viewed">', html_source, re.DOTALL)
	elif 'Filmes' in name and 'RECENTES' in name:
		pasta = False
		mode = 3
		html_source_trunk = re.findall('<div id="new"(.*?)<div id="popular">', html_source, re.DOTALL)
	elif 'Filmes' in name and 'VOTADOS' in name:
		pasta = False
		mode = 3
		html_source_trunk = re.findall('<div id="rated">(.*?)</div></div>', html_source, re.DOTALL)
	elif 'Séries' in name and 'VISTAS' in name:
		pasta = True
		mode = 10
		html_source_trunk = re.findall('<div id="viewed2">(.*?)<div id="rated2">', html_source, re.DOTALL)
	elif 'Séries' in name and 'POPULARES' in name:
		pasta = True
		mode = 10
		html_source_trunk = re.findall('<div id="popular2">(.*?)<div id="viewed2">', html_source, re.DOTALL)
	elif 'Séries' in name and 'RECENTES' in name:
		pasta = True
		mode = 10
		html_source_trunk = re.findall('<div id="new2">(.*?)<div id="popular2">', html_source, re.DOTALL)
	elif 'Séries' in name and 'VOTADAS' in name:
		pasta = True
		mode = 10
		html_source_trunk = re.findall('<div id="rated2">(.*?)</div></div>', html_source, re.DOTALL)
	
	if html_source:
		items = re.compile('<img src="(.+?)" alt=".+?"/><span>(.+?)</span><a href="(.+?)"').findall(html_source_trunk[0])
		for img,titulo,url in items:
                        i = i + 1
                        a = str(i)
                        if i < 10: a = '0'+a
                        DA = threading.Thread(name='DA'+str(i), target=ratoTV1 , args=(url, resultos, ))
                        threads.append(DA)


        [i.start() for i in threads]
        [i.join() for i in threads]

        i = 0
        x = 0
        threads = []
        for r in range(len(resultos)):
                dads = re.compile('(.+?)[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|]END[|]').findall(resultos[r])
                title = dads[0][0]
                Otitle = dads[0][1]
                url = dads[0][2]
                year = dads[0][3]
                imdbcode = dads[0][4]                
                sinopse = dads[0][5]
                i = i + 1
                a = str(i)
                if i < 10: a = '0'+a
                if FilmesOuSeries == 'Filmes':
                        DADOS = threading.Thread(name='DADOS'+str(i), target=dadosImdbcode , args=(title, Otitle, url, year, str(a), results, imdbcode, sinopse, ))
                elif FilmesOuSeries == 'Séries':
                        DADOS = threading.Thread(name='DADOS'+str(i), target=thetvdbIMDB , args=(title, Otitle, url, year, str(a), results, imdbcode, sinopse, ))
                threads.append(DADOS)
                x = x + 1
                
        [i.start() for i in threads]
        [i.join() for i in threads]
        
        num_filmes = len(results)
        results.sort()
        for x in range(len(results)):
                name = ''
                imdbcode = ''
                iconimage = ''
                fanart = ''
                url = ''
                year = ''
                Otitle = ''
                sinopse = ''
                genero = ''
                dads = re.compile('(.+?)[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|]END[|]').findall(results[x])
                order = dads[0][0]
                name = dads[0][1]
                imdbcode = dads[0][2]
                iconimage = dads[0][3]
                fanart = dads[0][4]
                url = dads[0][5]
                year = dads[0][6]
                Otitle = dads[0][7]
                sinopse = dads[0][8]
                if FilmesOuSeries == 'Filmes':                                                                                                          #7
                        addDir_trailer1('[B][COLOR green]' + Otitle + '[/COLOR][/B][COLOR yellow] (' + year + ')[/COLOR]',url+'IMDB'+imdbcode+'IMDB',9004,iconimage,sinopse,fanart,year,'',Otitle,url,'MoviesRTV',num_filmes)
                elif FilmesOuSeries == 'Séries':
                        addDir_trailer1('[B][COLOR green]' + Otitle + '[/COLOR][/B][COLOR yellow] (' + year + ')[/COLOR]',url+'IMDB'+imdbcode+'IMDB',3007,iconimage,sinopse,fanart,year,'',Otitle,url,'MoviesRTV',num_filmes)
                xbmc.sleep(12)                                                                                                                  

        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(515)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def ratoTV1(url,resultos):

        #resultos = []
        
        try:
                html_source = abrir_url(url)
        except: html_source = ''

        items = re.findall('<div class="posthead">(.+?)<div class="full-post">', html_source, re.DOTALL)

        for item in items:
                Otitle = re.compile('tulo Original.+?/strong>(.+?)</li>\n').findall(item)

                title = re.compile('tulo Portugu.+?/strong>(.+?)</li>\n').findall(item)
                
                #link = re.compile('<h1> <a href="(.+?)">.+?</a></h1>').findall(item)
                        
                anos = re.compile('<li><strong>Ano: </strong><a .+?>(.+?)</a></li>\n').findall(item)

                sins = re.compile('style="display:inline;">(.+?)\n').findall(item)
                        
                imdb = re.compile('"http://www.imdb.com/title/(.+?)/"').findall(item)

                resultos.append(title[0]+'|'+Otitle[0]+'|'+url+'|'+anos[0]+'|'+imdb[0]+'|'+sins[0]+'|END|')

def ratoTV(url):

        try: xbmcgui.Dialog().notification('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png', 3000, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % ('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png'))

        threads = []
        results = []
        
        try:
                html_source = abrir_url(url)
        except: html_source = ''
        i = 0
        x = 0
        items = re.findall('<div class="posthead">(.+?)<span class="more-btn">', html_source, re.DOTALL)
        for item in items:
                Otitle = re.compile('tulo Original.+?/strong>(.+?)</li>\n').findall(item)

                title = re.compile('tulo Portugu.+?/strong>(.+?)</li>\n').findall(item)
                
                link = re.compile('<h1> <a href="(.+?)">.+?</a></h1>').findall(item)
                        
                anos = re.compile('<li><strong>Ano: </strong>(.+?)</li>').findall(item)

                sins = re.compile('style="display:inline;">(.+?)\n').findall(item)
                        
                imdb = re.compile('"http://www.imdb.com/title/(.+?)/"').findall(item)
              
                i = i + 1
                a = str(i)
                if i < 10: a = '0'+a
                DADOS = threading.Thread(name='DADOS'+str(i), target=dadosImdbcode , args=(title[0], Otitle[0], link[0], anos[0], str(a), results, imdb[0], sins[0], ))
                threads.append(DADOS)
                x = x + 1

        [i.start() for i in threads]
        [i.join() for i in threads]

        num_filmes = len(results)
        results.sort()
        for x in range(len(results)):
                name = ''
                imdbcode = ''
                iconimage = ''
                fanart = ''
                url = ''
                year = ''
                Otitle = ''
                sinopse = ''
                genero = ''
                dads = re.compile('(.+?)[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|]END[|]').findall(results[x])
                order = dads[0][0]
                name = dads[0][1]
                imdbcode = dads[0][2]
                iconimage = dads[0][3]
                fanart = dads[0][4]
                url = dads[0][5]
                year = dads[0][6]
                Otitle = dads[0][7]
                sinopse = dads[0][8]
                #addDir_trailer1(nome,imdbcode,num_mode,thumb,sinopse,fanart,ano_filme,genero,O_Nome,urltrailer,'Movies',num_filmes)
                addDir_trailer1('[B][COLOR green]' + Otitle + '[/COLOR][/B][COLOR yellow] (' + year + ')[/COLOR]',url+'IMDB'+imdbcode+'IMDB',9004,iconimage,sinopse,fanart,year,'',Otitle,url,'MoviesRTV',num_filmes)
                #addLink('|'+name+'|'+imdbcode+'|'+iconimage+'|'+fanart+'|'+url+'|'+year+'|'+sinopse,'',iconimage,fanart)
                xbmc.sleep(12)

        pseg = re.compile('<div class="next"><a href="(.+?)"><img').findall(html_source)
        addDir("[COLOR blue]Página Seguinte >>[/COLOR]",pseg[0],20000,artfolder + 'PAGS1.png','','')

        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")#503
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
#http://api.themoviedb.org/3/movie/tt1174954?language=pt&api_key=3e7807c4a01f18298f64662b257d7059
def dadosImdbcode(title, Otitle, url, year, ordem, results, imdbcode, sinopse):
        api_key = '3e7807c4a01f18298f64662b257d7059'
        tmdb_base_url = 'http://d3gtl9l2a4fn1j.cloudfront.net/t/p/w1280'
        
        try:
                url_tmdb = 'http://api.themoviedb.org/3/movie/'+urllib.quote_plus(imdbcode)+'?language=pt&api_key=' + api_key 
                try: data = Funcoes.json_get(url_tmdb)
                except: data = ''

##                try: name = data[u'title']
##                except:name = ''
##                try: name = data[u'original_title']
##                except: name = ''

##                try: sinopse = data[u'overview']
##                except: sinopse = '---'
                        
                try: fanart = tmdb_base_url + data[u'backdrop_path']
                except: fanart = ''
                        
                try: thumb = tmdb_base_url.replace('w1280','w600') + data[u'poster_path']
                except: thumb =''
                        
                try: id_tmdb = data[u'id']
                except: id_tmdb=''
        except: pass

        if fanart == '':
                try:
                        url_tmdb = 'http://api.themoviedb.org/3/movie/'+urllib.quote_plus(imdbcode)+'?language=en&api_key=' + api_key 
                        try: data = Funcoes.json_get(url_tmdb)
                        except: data = ''

##                        try: name = data[u'title']
##                        except:name = ''
##                        try: name = data[u'original_title']
##                        except: name = ''

##                        try: sinopse = data[u'overview']
##                        except: sinopse = '--'
                                
                        try: fanart = tmdb_base_url + data[u'backdrop_path']
                        except: fanart = ''
                                
                        try: thumb = tmdb_base_url.replace('w1280','w600') + data[u'poster_path']
                        except: thumb =''
                                
                        try: id_tmdb = data[u'id']
                        except: id_tmdb=''
                except: pass
        results.append(str(ordem)+'|'+str(title)+'|'+str(imdbcode)+'|'+str(thumb)+'|'+str(fanart)+'|'+str(url)+'|'+str(year)+'|'+str(Otitle)+'|'+str(sinopse)+'|END|')                       
        #return fanart,str(id_tmdb),thumb

def ratoTVTV(url):

        try: xbmcgui.Dialog().notification('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png', 3000, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % ('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png'))

        threads = []
        results = []
        
        try:
                html_source = abrir_url(url)
        except: html_source = ''
        i = 0
        x = 0
        items = re.findall('<div class="posthead">(.+?)<span class="more-btn">', html_source, re.DOTALL)
        for item in items:
                Otitle = re.compile('tulo Original.+?/strong>(.+?)</li>\n').findall(item)

                title = re.compile('tulo Portugu.+?/strong>(.+?)</li>\n').findall(item)
                
                link = re.compile('<h1> <a href="(.+?)">.+?</a></h1>').findall(item)
                        
                anos = re.compile('<li><strong>Ano: </strong>(.+?)</li>').findall(item)

                sins = re.compile('style="display:inline;">(.+?)\n').findall(item)
                        
                imdb = re.compile('"http://www.imdb.com/title/(.+?)/"').findall(item)
              
                i = i + 1
                a = str(i)
                if i < 10: a = '0'+a
                DADOS = threading.Thread(name='DADOS'+str(i), target=thetvdbIMDB , args=(title[0], Otitle[0], link[0], anos[0], str(a), results, imdb[0], sins[0], ))
                threads.append(DADOS)
                x = x + 1

        [i.start() for i in threads]
        [i.join() for i in threads]

        num_filmes = len(results)
        results.sort()
        for x in range(len(results)):
                name = ''
                imdbcode = ''
                iconimage = ''
                fanart = ''
                url = ''
                year = ''
                Otitle = ''
                sinopse = ''
                genero = ''
                dads = re.compile('(.+?)[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|]END[|]').findall(results[x])
                order = dads[0][0]
                name = dads[0][1]
                imdbcode = dads[0][2]
                iconimage = dads[0][3]
                fanart = dads[0][4]
                url = dads[0][5]
                year = dads[0][6]
                Otitle = dads[0][7]
                sinopse = dads[0][8]
                #addDir_trailer1(nome,imdbcode,num_mode,thumb,sinopse,fanart,ano_filme,genero,O_Nome,urltrailer,'Movies',num_filmes)
                addDir_trailer1('[B][COLOR green]' + Otitle + '[/COLOR][/B][COLOR yellow] (' + year + ')[/COLOR]',url+'IMDB'+imdbcode+'IMDB',3007,iconimage,sinopse,fanart,year,'',Otitle,url,'MoviesRTV',num_filmes)
                #addLink('|'+name+'|'+imdbcode+'|'+iconimage+'|'+fanart+'|'+url+'|'+year+'|'+sinopse,'',iconimage,fanart)
                xbmc.sleep(12)

        pseg = re.compile('<div class="next"><a href="(.+?)"><img').findall(html_source)
        addDir("[COLOR blue]Página Seguinte >>[/COLOR]",pseg[0],20000,artfolder + 'PAGS1.png','','')

        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")#503
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def thetvdbIMDB(title, Otitle, url, year, ordem, results, imdbcode, sinopse):
                
	sin = ''
	idserie = ''

	try:
		url = 'http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=' + urllib.quote(imdbcode)+'&language=pt'
		html_source = abrir_url(url)
	except: html_source = ''
		
        sid = re.compile('<seriesid>(.+?)</seriesid>').findall(html_source)
        overview = re.compile('<Overview>(.+?)</Overview>').findall(html_source)
        imdbcode = re.compile('<IMDB_ID>(.+?)</IMDB_ID>').findall(html_source)
        aired = re.compile('<FirstAired>(.+?)-.+?-.+?</FirstAired>').findall(html_source)
        bann = re.compile('<banner>(.+?)</banner>').findall(html_source)

        if overview: sinopse = overview[0]
        #else: sin = '---'
        if sid: idserie = sid[0]
        else: idserie = ''

        #thumb = 'http://thetvdb.com/banners/'+bann[0]
        thumb = 'http://thetvdb.com/banners/posters/' + idserie + '-1.jpg'
        fanart = 'http://thetvdb.com/banners/fanart/original/' + idserie + '-1.jpg'
                                                
        results.append(str(ordem)+'|'+str(title)+'|'+str(imdbcode)+'|'+str(thumb)+'|'+str(fanart)+'|'+str(url)+'|'+str(year)+'|'+str(Otitle)+'|'+str(sinopse)+'|END|')                       
        
def RTVmovies(namet,url):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+namet,'url',1004,iconimage,False,fanart)
        url = 'IMDB'+imdbcode+'IMDB'

        return namet,url

def TPTmovies(name,url,iconimage):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        n1 = ''
        n2 = ''
        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(name)
        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
        nnnn = re.compile('(.+?)[(](.+?)[)]').findall(nnn[0])
        if nnnn:
                n2 = nnnn[0][0]
                n1 = nnnn[0][1]
        if not nnnn:
                nnnn = re.compile('(.+?)[[](.+?)[]]').findall(nnn[0])
                if nnnn:
                        n2 = nnnn[0][0]
                        n1 = nnnn[0][1]        
        if not nnnn:
                nnnn = re.compile('(.+?) [-] ').findall(nnn[0])
                if nnnn:
                        n2 = nnnn[0]
        if not nnnn:
                nnnn = re.compile('(.+?)[:] ').findall(nnn[0])
                if nnnn:
                        n2 = nnnn[0]
        if not nnnn : n2 = nnn[0]
        if n1 != '' and n2 != '':
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n2,'url',1004,iconimage,False,fanart)
                addDir('[COLOR yellow]PROCURAR POR: [/COLOR]'+n1,'IMDB'+imdbcode+'IMDB',7,iconimage,'',fanart)
        else:
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n2,'url',1004,iconimage,False,fanart)
        url = 'IMDB'+imdbcode+'IMDB'
        #addLink(name,'','','')
        return str(n2),url

def FTTmovies(name,url):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        n1 = ''
        n2 = ''
        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(name)
        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
        nnnn = re.compile('(.+?)[(](.+?)[)]').findall(nnn[0])
        if nnnn:
                n2 = nnnn[0][0]
                n1 = nnnn[0][1]
        if not nnnn:
                nnnn = re.compile('(.+?)[[](.+?)[]]').findall(nnn[0])
                if nnnn:
                        n2 = nnnn[0][0]
                        n1 = nnnn[0][1]        
        if not nnnn:
                nnnn = re.compile('(.+?) [-] ').findall(nnn[0])
                if nnnn:
                        n1 = nnnn[0]
        if not nnnn:
                nnnn = re.compile('(.+?)[:] ').findall(nnn[0])
                if nnnn:
                        n1 = nnnn[0]
        if not nnnn : n1 = nnn[0]

        if imdbcode == '' or imdbcode == '---':
                conta = 0
                nome_pesquisa = n1
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
                imdbcode = imdbc[0]

        if n1 != '' and n2 != '':
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
                addDir('[COLOR yellow]PROCURAR POR: [/COLOR]'+n2,'IMDB'+imdbcode+'IMDB',7,iconimage,'',fanart)
        else:
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
        url = 'IMDB'+imdbcode+'IMDB'
        return str(n1),url

def TFCmovies(name,url):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        n1 = ''
        n2 = ''
        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(name)
        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
        nnnn = re.compile('(.+?)[(](.+?)[)]').findall(nnn[0])
        if nnnn:
                n2 = nnnn[0][0]
                n1 = nnnn[0][1]
        if not nnnn:
                nnnn = re.compile('(.+?)[[](.+?)[]]').findall(nnn[0])
                if nnnn:
                        n2 = nnnn[0][0]
                        n1 = nnnn[0][1]        
        if not nnnn:
                nnnn = re.compile('(.+?) [-] ').findall(nnn[0])
                if nnnn:
                        n1 = nnnn[0]
        if not nnnn:
                nnnn = re.compile('(.+?)[:] ').findall(nnn[0])
                if nnnn:
                        n1 = nnnn[0]
        if not nnnn : n1 = nnn[0]

        if imdbcode == '' or '---' in imdbcode:                
                conta = 0
                ano_pp = re.compile('[[]COLOR yellow[]](.+?)[[]/COLOR[]]').findall(name)
                if ano_pp: ano_pesquisa = ano_pp[0].replace('(','').replace(')','').replace(' ','')
                else: ano_pesquisa = ''
                #addLink(imdbcode+'sim'+n1+'-'+ano_pesquisa,'','','')
                nome_pesquisa = n1 + ' ' + ano_pesquisa
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
                else: imdbcode = ''
                #addLink(imdbcode+'sim'+n1+'-'+ano_pesquisa,'','','')

        if n1 != '' and n2 != '':
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
                addDir('[COLOR yellow]PROCURAR POR: [/COLOR]'+n2,'IMDB'+imdbcode+'IMDB',7,iconimage,'',fanart)
        else:
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
        url = 'IMDB'+imdbcode+'IMDB'
        return str(n1),url

def CMTmovies(name,url):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        n1 = ''
        n2 = ''
        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(name)
        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
        nnnn = re.compile('(.+?)[(](.+?)[)]').findall(nnn[0])
        if nnnn:
                n2 = nnnn[0][0]
                n1 = nnnn[0][1]
        if not nnnn:
                nnnn = re.compile('(.+?)[[](.+?)[]]').findall(nnn[0])
                if nnnn:
                        n2 = nnnn[0][0]
                        n1 = nnnn[0][1]        
        if not nnnn:
                nnnn = re.compile('(.+?) [-] ').findall(nnn[0])
                if nnnn:
                        n1 = nnnn[0]
        if not nnnn:
                nnnn = re.compile('(.+?)[:] ').findall(nnn[0])
                if nnnn:
                        n1 = nnnn[0]
        if not nnnn : n1 = nnn[0]
                        
        if n1 != '' and n2 != '':
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
                addDir('[COLOR yellow]PROCURAR POR: [/COLOR]'+n2,'IMDB'+imdbcode+'IMDB',7,iconimage,'',fanart)
        else:
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
        url = 'IMDB'+imdbcode+'IMDB'
        return str(n1),url

def CMEmovies(name,url):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        n1 = ''
        n2 = ''
        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(name)
        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
        nnnn = re.compile('(.+?)[(](.+?)[)]').findall(nnn[0])
        if nnnn:
                n2 = nnnn[0][0]
                n1 = nnnn[0][1]
        if not nnnn:
                nnnn = re.compile('(.+?)[[](.+?)[]]').findall(nnn[0])
                if nnnn:
                        n2 = nnnn[0][0]
                        n1 = nnnn[0][1]        
        if not nnnn:
                nnnn = re.compile('(.+?) [-] ').findall(nnn[0])
                if nnnn:
                        n1 = nnnn[0]
        if not nnnn:
                nnnn = re.compile('(.+?)[:] ').findall(nnn[0])
                if nnnn:
                        n1 = nnnn[0]
        if not nnnn : n1 = nnn[0]

        if imdbcode == '' or imdbcode == '---':
                conta = 0
                nome_pesquisa = n1
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
                imdbcode = imdbc[0]

        if n1 != '' and n2 != '':
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
                addDir('[COLOR yellow]PROCURAR POR: [/COLOR]'+n2,'IMDB'+imdbcode+'IMDB',7,iconimage,'',fanart)
        else:
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
        url = 'IMDB'+imdbcode+'IMDB'
        return str(n1),url

def TFVmovies(name,url):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        n1 = ''
        n2 = ''
        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(name)
        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
        nnnn = re.compile('(.+?)[(](.+?)[)]').findall(nnn[0])
        if nnnn:
                n2 = nnnn[0][0]
                n1 = nnnn[0][1]
        if not nnnn:
                nnnn = re.compile('(.+?)[[](.+?)[]]').findall(nnn[0])
                if nnnn:
                        n2 = nnnn[0][0]
                        n1 = nnnn[0][1]        
        if not nnnn:
                nnnn = re.compile('(.+?) [-] ').findall(nnn[0])
                if nnnn:
                        n1 = nnnn[0]
        if not nnnn:
                nnnn = re.compile('(.+?)[:] ').findall(nnn[0])
                if nnnn:
                        n1 = nnnn[0]
        if not nnnn : n1 = nnn[0]

        if n1 != '' and n2 != '':
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
                addDir('[COLOR yellow]PROCURAR POR: [/COLOR]'+n2,'IMDB'+imdbcode+'IMDB',7,iconimage,'',fanart)
        else:
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
        url = 'IMDB'+imdbcode+'IMDB'
        return str(n1),url

def MVTmovies(name,url):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        n1 = ''
        n2 = ''
        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(name)
        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
        nnnn = re.compile('(.+?)[(](.+?)[)]').findall(nnn[0])
        if nnnn:
                n2 = nnnn[0][0]
                n1 = nnnn[0][1]
        if not nnnn:
                nnnn = re.compile('(.+?)[[](.+?)[]]').findall(nnn[0])
                if nnnn:
                        n2 = nnnn[0][0]
                        n1 = nnnn[0][1]        
        if not nnnn:
                nnnn = re.compile('(.+?) [-] ').findall(nnn[0])
                if nnnn:
                        n1 = nnnn[0]
        if not nnnn:
                nnnn = re.compile('(.+?)[:] ').findall(nnn[0])
                if nnnn:
                        n1 = nnnn[0]
        if not nnnn : n1 = nnn[0]

        if imdbcode == '' or '---' in imdbcode:
                ano_pp = re.compile('[[]COLOR yellow[]](.+?)[[]/COLOR[]]').findall(name)
                if ano_pp: ano_pesquisa = ano_pp[0].replace('(','').replace(')','')
                else: ano_pesquisa = ''
                conta = 0
##                nome_pesquisa = n[0] + ' ' + ano_pesquisa
                nome_pesquisa = n1 + '+' + ano_pesquisa
                nome_pesquisa = nome_pesquisa.replace('é','e').replace(' 1 ',' ')
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
                try: html_imdbcode = abrir_url(url_imdb)
                except: html_imdbcode = ''
                filmes_imdb = re.findall('<div class="findSection">(.*?)<div class="findMoreMatches">', html_imdbcode, re.DOTALL)
                if filmes_imdb:
                        imdbc = re.compile('/title/(.+?)/[?]ref').findall(filmes_imdb[0])
                        if imdbc: imdbcode = imdbc[0]
        
        if n1 != '' and n2 != '':
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
                addDir('[COLOR yellow]PROCURAR POR: [/COLOR]'+n2,'IMDB'+imdbcode+'IMDB',7,iconimage,'',fanart)
        else:
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
        url = 'IMDB'+imdbcode+'IMDB'
        return str(n1),url

def CMCmovies(name,url):
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        n1 = ''
        n2 = ''
        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(name)
        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
        nnnn = re.compile('(.+?)[(](.+?)[)]').findall(nnn[0])
        if nnnn:
                n2 = nnnn[0][0]
                n1 = nnnn[0][1]
        if not nnnn:
                nnnn = re.compile('(.+?)[[](.+?)[]]').findall(nnn[0])
                if nnnn:
                        n2 = nnnn[0][0]
                        n1 = nnnn[0][1]        
        if not nnnn:
                nnnn = re.compile('(.+?) [-] ').findall(nnn[0])
                if nnnn:
                        n1 = nnnn[0]
        if not nnnn:
                nnnn = re.compile('(.+?)[:] ').findall(nnn[0])
                if nnnn:
                        n1 = nnnn[0]
        if not nnnn : n1 = nnn[0]

        if imdbcode == '' or '---' in imdbcode:
                ano_pp = re.compile('[[]COLOR yellow[]](.+?)[[]/COLOR[]]').findall(name)
                if ano_pp: ano_pesquisa = ano_pp[0].replace('(','').replace(')','')
                else: ano_pesquisa = ''
                conta = 0
##                nome_pesquisa = n[0] + ' ' + ano_pesquisa
                nome_pesquisa = n1 + ' ' + ano_pesquisa
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

        if n1 != '' and n2 != '':
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
                addDir('[COLOR yellow]PROCURAR POR: [/COLOR]'+n2,'IMDB'+imdbcode+'IMDB',7,iconimage,'',fanart)
        else:
                addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n1,'url',1004,iconimage,False,fanart)
        url = 'IMDB'+imdbcode+'IMDB'
        return str(n1),url
        
def SERIES_MENU():
##        addDir('[B][COLOR green]TO[/COLOR][COLOR yellow]D[/COLOR][COLOR red]AS[/COLOR][/B] (A/Z)','urlTODAS',26,artfolder + 'ST.png','nao','')
##        url_TFC = 'http://www.tuga-filmes.info/'
##        url_MVT = 'http://www.movie-tuga.blogspot.pt'
##        url_TFV = 'http://www.tuga-filmes.us/search/label/S%C3%A9ries'
##        url_TPT = 'http://toppt.net/category/series/'
##        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "fim": 'fim',"xpto":'xpto'}
##        url_ultimos_episodios = urllib.urlencode(parameters)
##        addDir('[B][COLOR green]ÚLTIMO[/COLOR][COLOR yellow]S [/COLOR][COLOR red]EPISÓDIOS[/COLOR][/B]',url_ultimos_episodios,508,artfolder + 'UEP.png','nao','')
        addDir('[B][COLOR green]EM E[/COLOR][COLOR yellow]X[/COLOR][COLOR red]IBIÇÃO[/COLOR][/B] (Séries)','1',3008,artfolder + 'EE.png','nao','')
        addDir('[B][COLOR green]MAIS[/COLOR][COLOR yellow] V[/COLOR][COLOR red]OTADAS[/COLOR][/B] (Séries)','1',3009,artfolder + 'SMV.png','nao','')
        addDir('[B][COLOR green]MAIS P[/COLOR][COLOR yellow]O[/COLOR][COLOR red]PULARES[/COLOR][/B] (Séries)','1',3010,artfolder + 'MP.png','nao','')
        addDir('[B][COLOR green]PRO[/COLOR][COLOR yellow]C[/COLOR][COLOR red]URAR[/COLOR][/B] (Séries)','1',3011,artfolder + 'P1.png','nao','')
     

def passar_nome_pesquisa_animacao(name,url,year):
        try: xbmcgui.Dialog().notification('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png', 10000, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, 10000, %s)" % ('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png'))
        
        imdbcode = re.compile('IMDB(.+?)IMDB').findall(url)
        if imdbcode: imdbcode = imdbcode[0]
        else: imdbcode = ''
        
        nome_pesquisa = str(name)       
        nome_pesquisa = nome_pesquisa.replace('[COLOR yellow]PROCURAR POR: [/COLOR]','')
        nome_pp = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]][[]COLOR yellow[]].+?[[]/COLOR[]]').findall(nome_pesquisa)
        if nome_pp: nome_pesquisa = nome_pp[0]
        
        conta = 0        
        if imdbcode == '' or imdbcode == '---':
                nome_pesquisa = nome_pesquisa.replace(' 1 ','') + '+' + year
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
                try: html_imdbcode = abrir_url(url_imdb)
                except: html_imdbcode = ''
                if html_imdbcode != '':
                        filmes_imdb = re.findall('<div class="findSection">(.*?)<div class="findMoreMatches">', html_imdbcode, re.DOTALL)
                        if filmes_imdb:
                                imdbc = re.compile('/title/(.+?)/[?]ref').findall(filmes_imdb[0])
                                if imdbc: imdbcode = imdbc[0]
                
        url = 'IMDB'+imdbcode+'IMDB'
##        addLink(name+url+year,'','','')
##        return
        FilmesAnima.FILMES_ANIMACAO_pesquisar(str(nome_pesquisa),'',url)
        #PesquisaExterna.pesquisar(str(nome_pesquisa),url)
##        item = xbmcgui.ListItem(path=url)
##	item.setProperty("IsPlayable", "true")
##        xbmc.Player().play('plugin://plugin.video.Sites_dos_Portugas/?url='+url+'&mode=9000&name='+str(nome_pesquisa)+'&automatico=', item)

def passar_nome_pesquisa_externa(name,url):

        imdbcode = re.compile('IMDB(.+?)IMDB').findall(url)
        if imdbcode: imdbcode = imdbcode[0]
        else: imdbcode = ''
        
        nome_pesquisa = str(name)       
        nome_pesquisa = nome_pesquisa.replace('[COLOR yellow]PROCURAR POR: [/COLOR]','')
        nome_pp = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]][[]COLOR yellow[]].+?[[]/COLOR[]]').findall(nome_pesquisa)
        if nome_pp: nome_pesquisa = nome_pp[0]
        conta = 0
        
        if imdbcode == '':
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
        PesquisaExterna.pesquisar(str(nome_pesquisa),url)

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
        
###############################   FILMES TMDB
        
def MPOPULARES():
        num_pag = urllib.quote(url)
        conta = 0
        num_mode = 7
        if num_mode == 7: noscinemas = themoviedb_api_pagina().fanart_and_id('movie','7','popular',str(num_pag))
        npag = urllib.quote(url)
        numpag = '('+str(npag)+'/22)'
        npseg = int(npag) + 1
	addDir('[B][COLOR blue]'+numpag+'[/COLOR] Seguinte > [COLOR blue]'+str(npseg)+'[/COLOR][/B]',str(npseg),3000,artfolder + 'PAGS1.png','','')

def MVOTADOS():
        num_pag = urllib.quote(url)
        conta = 0
        num_mode = 7
        if num_mode == 7: noscinemas = themoviedb_api_pagina().fanart_and_id('movie','7','top_rated',str(num_pag))
        npag = urllib.quote(url)
        numpag = '('+str(npag)+'/22)'
        npseg = int(npag) + 1
	addDir('[B][COLOR blue]'+numpag+'[/COLOR] Seguinte > [COLOR blue]'+str(npseg)+'[/COLOR][/B]',str(npseg),3001,artfolder + 'PAGS1.png','','')

def NCINEMAS():
        num_pag = urllib.quote(url)
        conta = 0
        num_mode = 7
        if num_mode == 7: noscinemas = themoviedb_api_pagina().fanart_and_id('movie','7','now_playing',str(num_pag))
        npag = urllib.quote(url)
        numpag = '('+str(npag)+'/22)'
        npseg = int(npag) + 1
	addDir('[B][COLOR blue]'+numpag+'[/COLOR] Seguinte > [COLOR blue]'+str(npseg)+'[/COLOR][/B]',str(npseg),3002,artfolder + 'PAGS1.png','','')

def BREVEMFILMES():
        num_pag = urllib.quote(url)
        conta = 0
        num_mode = 7
        if num_mode == 7: noscinemas = themoviedb_api_pagina().fanart_and_id('movie','7','upcoming',str(num_pag))
        npag = urllib.quote(url)
        numpag = '('+str(npag)+'/22)'
        npseg = int(npag) + 1
	addDir('[B][COLOR blue]'+numpag+'[/COLOR] Seguinte > [COLOR blue]'+str(npseg)+'[/COLOR][/B]',str(npseg),2999,artfolder + 'PAGS1.png','','')

def SEARCHTMDBMOVIES():
        keyb = xbmc.Keyboard('', 'Escreva o parâmetro de pesquisa')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		pesquisou = search
		encode=urllib.quote(search)
                num_mode = 7
                if num_mode == 7: noscinemas = themoviedb_api_pagina().fanart_and_id('movie','7','search',str(encode))


###############################   SÉRIES TMDB

def EMEXIBICAO():
        num_pag = urllib.quote(url)
        conta = 0
        num_mode = 3007
        if num_mode == 3007: emexibicao = themoviedb_api_pagina().fanart_and_id('tv','3007','on_the_air',str(num_pag))
        npag = urllib.quote(url)
        numpag = '('+str(npag)+'/22)'
        npseg = int(npag) + 1
	addDir('[B][COLOR blue]'+numpag+'[/COLOR] Seguinte > [COLOR blue]'+str(npseg)+'[/COLOR][/B]',str(npseg),3008,artfolder + 'PAGS1.png','','')

def MVOTADAS():
        num_pag = urllib.quote(url)
        conta = 0
        num_mode = 3007
        if num_mode == 3007: emexibicao = themoviedb_api_pagina().fanart_and_id('tv','3007','top_rated',str(num_pag))
        npag = urllib.quote(url)
        numpag = '('+str(npag)+'/22)'
        npseg = int(npag) + 1
	addDir('[B][COLOR blue]'+numpag+'[/COLOR] Seguinte > [COLOR blue]'+str(npseg)+'[/COLOR][/B]',str(npseg),3009,artfolder + 'PAGS1.png','','')

def MPOPULARESTV():
        num_pag = urllib.quote(url)
        conta = 0
        num_mode = 3007
        if num_mode == 3007: emexibicao = themoviedb_api_pagina().fanart_and_id('tv','3007','popular',str(num_pag))
        npag = urllib.quote(url)
        numpag = '('+str(npag)+'/22)'
        npseg = int(npag) + 1
	addDir('[B][COLOR blue]'+numpag+'[/COLOR] Seguinte > [COLOR blue]'+str(npseg)+'[/COLOR][/B]',str(npseg),3010,artfolder + 'PAGS1.png','','')

def SEARCHTMDBTV():
        keyb = xbmc.Keyboard('', 'Escreva o parâmetro de pesquisa')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		pesquisou = search
		encode=urllib.quote(search)
                num_mode = 3007
                if num_mode == 3007: noscinemas = themoviedb_api_pagina().fanart_and_id('tv','3007','search',str(encode))
        
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
##        if '-' in nome_pesquisa:
##                nome_p = re.compile('.+?[-](.+?)').findall(nome_pesquisa)
##                if len(nome_p[0])>2:
##                        nome_pesquisa = nome_p[0]
##        else:
##                if ':' in nome_pesquisa:
##                        nome_p = re.compile('(.+?)[:].+?').findall(nome_pesquisa)
##                        nome_pesquisa = nome_p[0]
##
##        nome_pesquisa = nome_pesquisa.replace('é','e')
        nome_pesquisa = nome_pesquisa.replace("'s",'')
        nome_pesquisa = nome_pesquisa.replace("&",'')
        nome_pesquisa = nome_pesquisa.replace(":",'')
##        nome_pesquisa = nome_pesquisa.replace('ê','e')
##        nome_pesquisa = nome_pesquisa.replace('á','a')
##        nome_pesquisa = nome_pesquisa.replace('à','a')
##        nome_pesquisa = nome_pesquisa.replace('ã','a')
##        nome_pesquisa = nome_pesquisa.replace('è','e')
##        nome_pesquisa = nome_pesquisa.replace('í','i')
##        nome_pesquisa = nome_pesquisa.replace('ó','o')
##        nome_pesquisa = nome_pesquisa.replace('ô','o')
##        nome_pesquisa = nome_pesquisa.replace('õ','o')
##        nome_pesquisa = nome_pesquisa.replace('ú','u')
##        nome_pesquisa = nome_pesquisa.replace('Ú','U')
##        nome_pesquisa = nome_pesquisa.replace('ç','c')
##        nome_pesquisa = nome_pesquisa.replace('ç','c')
##
##        nome_pesquisa = nome_pesquisa.lower()
        pesquisou = nome_pesquisa
        nome_pesquisa = urllib.quote_plus(nome_pesquisa)
##        numpontos=re.compile('[.](.+?)').findall(nome_pesquisa)
##        pontos = len(numpontos)
##        if pontos > 1: nome_pesquisa = nome_pesquisa.replace('.','')
##
##        conta = 0
##        a_q = re.compile('\w+')
##        qq_aa = a_q.findall(nome_pesquisa)
##        nome_pesquisa = ''
##        for q_a_q_a in qq_aa:
##                if len(q_a_q_a) > 0 or q_a_q_a == '1' or q_a_q_a == '2' or q_a_q_a == '3' or q_a_q_a == '4'or q_a_q_a == '5' or q_a_q_a == '6':
##                #if len(q_a_q_a) > 1:
##                        if conta == 0:
##                                nome_pesquisa = q_a_q_a
##                                conta = 1
##                        else:
##                                nome_pesquisa = nome_pesquisa + '+' + q_a_q_a
##
##        nome_pesquisa = nome_pesquisa.lower()
##        nome_pesquisa = nome_pesquisa.replace('  ','')
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

        nome_pesquisa = urllib.quote_plus(nome_pesquisa)
        encode = urllib.quote(nome_pesquisa)
        
        a = 0
        site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv'
        percent = int( ( a / 2.0 ) * 100)
        message = ''
        progress.update(percent, 'A Procurar em '+site, message, "")
        print str(a) + " de " + str(int(a))
        if url_TFV == '': url_TFV = 'http://www.tuga-filmes.us/search?q=' + str(encode)
	encontrar_fontes_SERIES_TFV(url_TFV + 'IMDB'+imdbcode+'IMDB',pesquisou)
	
	a = 1
	site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
	percent = int( ( a / 2.0 ) * 100)
        message = ''
        progress.update(percent, 'A Procurar em '+site, message, "")
        print str(a) + " de " + str(int(a))
        if url_TPT == '': url_TPT = 'http://toppt.net/?s=' + str(encode)
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
                        #imdb_code = re.compile('<b>Mais INFO</b>: <a href="http://www.imdb.com/title/(.+?)/" target="_blank">IMDb</a>').findall(item)
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
                        ###########################
                        season = re.compile('Temporada(.+?)[-].+?[(]').findall(nome)
                        if season: season = season[0]
                        else:
                                season = re.compile('Temporada(.+?)[(]').findall(nome)
                                if season: season = season[0]
                                else:
                                        season = re.compile('[(](.+?)[-].+?[)]').findall(nome)
                                        if season: season = season[0]
                                        else:
                                                season = re.compile('[(](.+?)[)]').findall(nome)
                                                if season: season = season[0]
                                                else: season = ''
                                        
                                        
                        temporada = re.compile('(\d+)').findall(season)
                        if temporada:
                                temporada = temporada[0]
                        else:
                                temporada = ''
                        thumbl=''
                        ###############################
                        n = re.compile('(.+?)[(].+?[)]').findall(nome)
                        if n: nome_pesquisa = n[0]
                        else: nome_pesquisa = nome      
                        try:
                                #addLink(nome +'-'+ imdbcode +'-'+ imdbcode_passado + '-'+imdbc,'','')
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
                                                                #thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                                                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                                if snpse and sinopse == '': sinopse = snpse[0]
##                                                        if temporada!= '':
##                                                                thumbl = 'http://thetvdb.com/banners/seasons/' + ftart[0] + '-' + temporada + '.jpg'
##                                                                try:
##                                                                        thml=abrir_url(thumbl)
##                                                                        if thml: thumb = 'http://thetvdb.com/banners/seasons/' + ftart[0] + '-' + temporada + '.jpg'
##                                                                except: pass
                                                        if temporada!= '':
                                                                try:
                                                                        thumbl = buscathumb(ftart[0],str(temporada))
                                                                        if thumbl != '': thumb = thumbl
                                                                except: pass
                                                        n = re.compile('[(](.+?)[)]').findall(nome)
                                                        if n: nome = n[0]
                                                        #addDir('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR]',urletitulo[0][0],num_mode,thumbnail[0].replace('s72-c','s320'),'',fanart)
                                                        addDir_trailer('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB'+nome_pesquisa,num_mode,thumb.replace('s72-c','s320'),sinopse,fanart,ano[0],genero,nome_pesquisa,urletitulo[0][0])
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
                                                        #if thumb == '' or 's1600' in thumb: thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                                                        #addLink(thumb,'','')
##                                                        if temporada!= '':
##                                                                thumbl = 'http://thetvdb.com/banners/seasons/' + ftart[0] + '-' + temporada + '.jpg'
##                                                                try:
##                                                                        thml=abrir_url(thumbl)
##                                                                        if thml: thumb = 'http://thetvdb.com/banners/seasons/' + ftart[0] + '-' + temporada + '.jpg'
##                                                                except: pass
                                                        snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                        if snpse and sinopse == '': sinopse = snpse[0]
                                                if temporada!= '':
                                                        try:
                                                                thumbl = buscathumb(ftart[0],str(temporada))
                                                                if thumbl != '': thumb = thumbl
                                                        except: pass
                                                n = re.compile('[(](.+?)[)]').findall(nome)
                                                if n: nome = n[0]
                                                #addDir('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR]',urletitulo[0][0],num_mode,thumbnail[0].replace('s72-c','s320'),'',fanart)
                                                addDir_trailer('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB'+nome_pesquisa,num_mode,thumb.replace('s72-c','s320'),sinopse,fanart,ano[0],genero,nome_pesquisa,urletitulo[0][0])
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
                                        
                        n = re.compile('(.+?)[[].+?[]].+?[]]').findall(nome)                                                        
                        if n: nome_pesquisa = n[0]
                        else: nome_pesquisa = nome

                        ###########################
                        season = re.compile('[[]Season(.+?)[]].+?[]]').findall(nome)
                        if season: season = season[0]
                        else:
                                season = re.compile('[[]Temporada(.+?)[]].+?[]]').findall(nome)
                                if season: season = season[0]
                                else:
                                        season = re.compile('Season(.+?)[(]').findall(nome)
                                        if season: season = season[0]
                                        else:
                                                season = re.compile('[(](.+?)[-].+?[)]').findall(nome)
                                                if season: season = season[0]
                                                else:
                                                        season = re.compile('[(](.+?)[)]').findall(nome)
                                                        if season: season = season[0]
                                                        else: season = ''

                        temporada = re.compile('(\d+)').findall(season)
                        if temporada:
                                temporada = temporada[0]
                        else:
                                temporada = ''
                        thumbl=''
                        ###############################
                        #addLink(temporada+'-','','','')
                        try:
                                if genero == '': genero = '---'
                                if sinopse == '': sinopse = '---'
                                if fanart == '': fanart = '---'
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
                                #addLink(nome +'-'+ imdbcode +'-'+ imdbcode_passado + '-'+imdbc,'','')
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
                                                        #if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                                                        snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                        if snpse and sinopse == '---': sinopse = snpse[0]
##                                                if temporada!= '':
##                                                        thumbl = 'http://thetvdb.com/banners/seasons/' + ftart[0] + '-' + temporada + '.jpg'
##                                                        try:
##                                                                thml=abrir_url(thumbl)
##                                                                if thml: thumb = 'http://thetvdb.com/banners/seasons/' + ftart[0] + '-' + temporada + '.jpg'
##                                                        except: pass
                                                if temporada!= '':
                                                        try:
                                                                thumbl = buscathumb(ftart[0],str(temporada))
                                                                if thumbl != '': thumb = thumbl
                                                        except: pass
                                                #addLink(ftart[0],'','',fanart)
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
                                                addDir_trailer('[COLOR orange]TPT | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB'+nome_pesquisa,233,thumb,sinopse,fanart,ano_filme.replace('(','').replace(')',''),genero,nome_pesquisa,urletitulo[0][0])
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
                                                #if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                if snpse and sinopse == '---': sinopse = snpse[0]
##                                        if temporada!= '':
##                                                thumbl = 'http://thetvdb.com/banners/seasons/' + ftart[0] + '-' + temporada + '.jpg'
##                                                try:
##                                                        thml=abrir_url(thumbl)
##                                                        if thml: thumb = 'http://thetvdb.com/banners/seasons/' + ftart[0] + '-' + temporada + '.jpg'
##                                                except: pass
                                        if temporada!= '':
                                                try:
                                                        thumbl = buscathumb(ftart[0],str(temporada))
                                                        if thumbl != '': thumb = thumbl
                                                except: pass
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
                                        addDir_trailer('[COLOR orange]TPT | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB'+nome_pesquisa,233,thumb,sinopse,fanart,ano_filme.replace('(','').replace(')',''),genero,nome_pesquisa,urletitulo[0][0])
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

def buscathumb(tvdbid,temporada):
        seasonBanner = ''
        if tvdbid!='':
                try:
                        url = 'http://thetvdb.com/api/23B3F3D91B980C9F/series/'+urllib.quote(tvdbid)+'/banners.xml'
                        html_source = abrir_url(url)
                except: html_source = ''
                info = re.findall('<Banner>(.+?)</Banner>', html_source, re.DOTALL)
                for infos in info:
                        try:
                                season = re.compile('<Season>(.+?)</Season>').findall(infos)
                                bannertype = re.compile('<BannerType>(.+?)</BannerType>').findall(infos)
                                bannertype2 = re.compile('<BannerType2>(.+?)</BannerType2>').findall(infos)
                                language = re.compile('<Language>(.+?)</Language>').findall(infos)
                                if season and bannertype and bannertype2 and language:
                                        #addLink(season[0],'','','')
                                        if season[0] == str(temporada) and bannertype[0] == 'season' and bannertype2[0] == 'season' and language[0] == 'en':
                                                seasonB =re.compile('<BannerPath>(.+?)</BannerPath>').findall(infos)
                                                try: seasonBanner = 'http://thetvdb.com/banners/'+seasonB[0]
                                                except: seasonBanner = ''
                                                break
                                                
                        except: seasonBanner = ''
                return str(seasonBanner)
        else: return str(seasonBanner)

def INDEX(url,name):
        
        #nepi = re.compile('[[].+?[]].+?[[].+?[]][[].+?[]].+?[[].+?[]](.*)').findall(name)
        #if nepi: name = nepi[0].replace('[/B] | ','').replace('[COLOR blue]','').replace('[COLOR grey]','').replace('[/COLOR]','')
        #addLink(name,'','','')
        i = 1
        _nomeservidor_ = []
        _linkservidor_ = []

        nomeepi = re.compile('[[]COLOR grey[]](.*)').findall(url)
        if nomeepi: nomeepisodio = '[COLOR grey]'+nomeepi[0]

        checker = ''
        n = re.compile('[(](.+?)[)](.+?)[|]').findall(url.replace('//[COLOR grey]','|[COLOR grey]'))
        for n1,n2 in n:
                _nomeservidor_.append('Fonte '+str(i)+': [COLOR yellow]'+n1+'[/COLOR]')
                _linkservidor_.append(n2+'///'+nomeepisodio)
                i = i + 1
        indexservidores = xbmcgui.Dialog().select
        index = indexservidores('Escolha o Stream', _nomeservidor_)
        if index > -1: Play.PLAY_episodes(_linkservidor_[index],name,iconimage,'',fanart)
##                item = xbmcgui.ListItem(path=_linkservidor_[index])
##                item.setProperty("IsPlayable", "true")
##                xbmc.Player().play('plugin://plugin.video.Sites_dos_Portugas/?url='+_linkservidor_[index]+'&mode=6000&name='+name+'&iconimage='+iconimage+'&checker='+checker+'&fanart='+fanart, item)

def xbmcxbmc(url,name):
##        addLink(url,'','','')
##        addLink(name,'','','')
        tt = 'tt2267998'
        n = 'gone girl'
        item = xbmcgui.ListItem(path=url)
	item.setProperty("IsPlayable", "true")
        #xbmc.Player().play('plugin://plugin.video.Sites_dos_Portugas/?mode=7000&url='+url, item)
        xbmc.Player().play('plugin://plugin.video.Sites_dos_Portugas/?url=IMDB'+tt+'IMDB&mode=9000&name='+n, item)

def playper(name, url, imdb_id, year, addon):
	item = xbmcgui.ListItem(path=url)
	item.setProperty("IsPlayable", "true")
	if 'genesis' in addon: xbmc.Player().play(links.link().genesis_play % (name,name,year,imdb_id,url), item)
	elif 'rato' in addon: xbmc.Player().play(links.link().rato_play % (url,name), item)
	#if 'portugas' in addon.lower():	xbmc.executebuiltin('activatewindow(video,'+links.link().sdp_search % (imdb_id,urllib.quote_plus(name.split("(")[0].strip()))+')')
	
	if 'portugas' in addon.lower():	xbmc.Player().play(links.link().sdp_search % (imdb_id,urllib.quote_plus(name.replace('('+year+')',''))), item)
	
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
          
params=get_params()
url=None
name=None
mode=None
checker=None
iconimage=None
fanart=None
year=None
plot=None
genre=None
episod=None
air=None
namet=None
urltrailer=None
mvoutv=None
automatico=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: urltrailer=urllib.unquote_plus(params["urltrailer"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: namet=urllib.unquote_plus(params["namet"])
except: pass
try: nome=urllib.unquote_plus(params["nome"])
except: pass
try: mode=int(params["mode"])
except: pass
try: checker=urllib.unquote_plus(params["checker"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: fanart=urllib.unquote_plus(params["fanart"])
except: pass
try: plot=urllib.unquote_plus(params["plot"])
except: pass
try: year=urllib.unquote_plus(params["year"])
except: pass
try: genre=urllib.unquote_plus(params["genre"])
except: pass
try: episod=urllib.unquote_plus(params["episod"])
except: pass
try: air=urllib.unquote_plus(params["air"])
except: pass
try: mvoutv=urllib.unquote_plus(params["mvoutv"])
except: pass
try: automatico=urllib.unquote_plus(params["automatico"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Checker: "+str(checker)
print "Iconimage: "+str(iconimage)
print "Plot: "+str(plot)
print "Year: "+str(year)
print "Genre: "+str(genre)
print "Fanart: "+str(fanart)
print "Episode: "+str(episod)
print "Namet: "+str(namet)
print "Urltrailer: "+str(urltrailer)
print "MvouTv: "+str(mvoutv)
print "Automatico: "+str(automatico)
######################################################################################

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
        passar_nome_pesquisa_animacao(name,url,year)

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
        TugaFilmesTV.TFV_encontrar_fontes_filmes(url)
        xbmcplugin.setContent(int(sys.argv[1]), 'livetv')#movies
        xbmc.executebuiltin("Container.SetViewMode(560)")#503
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 33: TugaFilmesTV.TFV_encontrar_videos_filmes(name,url,mvoutv)
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
elif mode == 42:
        TugaFilmesTV.TFV_encontrar_videos_series(name,url)

elif mode == 43:
        TugaFilmesTV.TFV_resolve_not_videomega_series(name,url,id_video,nome_cada_episodio,src_href)
elif mode == 44:
        TugaFilmesTV.TFV_encontrar_fontes_series_recentes(url)
        xbmcplugin.setContent(int(sys.argv[1]), 'livetv')#movies
        xbmc.executebuiltin("Container.SetViewMode(560)")#503
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
        xbmcplugin.setContent(int(sys.argv[1]), 'livetv')#movies
        xbmc.executebuiltin("Container.SetViewMode(560)")#503
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
elif mode == 58:
        TugaFilmesTV.ultimos_episodios_TFV_ultimos(url)
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmc.executebuiltin("Container.SetViewMode(504)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

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
        xbmcplugin.setContent(int(sys.argv[1]), 'livetv')#movies
        xbmc.executebuiltin("Container.SetViewMode(560)")#503
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 73: TugaFilmesCom.TFC_encontrar_videos_filmes(name,url,mvoutv)
elif mode == 74: TugaFilmesCom.TFC_pesquisar_filmes()
elif mode == 75: TugaFilmesCom.TFC_resolve_videomega_filmes(url,conta_id_video)
elif mode == 76: TugaFilmesCom.TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,nome_fonte_video)
elif mode == 77: TugaFilmesCom.TFC_Menu_Filmes(artfolder)
elif mode == 78: TugaFilmesCom.TFC_Menu_Filmes_Por_Categorias(artfolder)
elif mode == 79:
        TugaFilmesCom.TFC_Menu_Filmes_Top_10(artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'livetv')#movies
        xbmc.executebuiltin("Container.SetViewMode(560)")#503
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
        xbmcplugin.setContent(int(sys.argv[1]), 'livetv')#movies
        xbmc.executebuiltin("Container.SetViewMode(560)")#503
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 103: MovieTuga.MVT_encontrar_videos_filmes(name,url,mvoutv)
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
        TopPt.TPT_encontrar_fontes_filmes(url)
        xbmcplugin.setContent(int(sys.argv[1]), 'livetv')#movies
        xbmc.executebuiltin("Container.SetViewMode(560)")#503
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 233: TopPt.TPT_encontrar_videos_filmes(name,url,iconimage,mvoutv)
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
        xbmcplugin.setContent(int(sys.argv[1]), 'livetv')#movies
        xbmc.executebuiltin("Container.SetViewMode(560)")#503
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 259:
        TopPt.TPT_Menu_Top_Series(artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'livetv')#movies
        xbmc.executebuiltin("Container.SetViewMode(560)")#503
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 260:
        TopPt.ultimos_episodios_TPT_ultimos(url)
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmc.executebuiltin("Container.SetViewMode(504)")
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
        xbmcplugin.setContent(int(sys.argv[1]), 'livetv')
        xbmc.executebuiltin("Container.SetViewMode(560)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 508:
        Mashup.ultimos_episodios(url)
        #setViewMode_filmes()
##        xbmcplugin.setContent(int(sys.argv[1]), 'livetv')#movies
##        xbmc.executebuiltin("Container.SetViewMode(560)")#503
##        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmc.executebuiltin("Container.SetViewMode(504)")
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
        xbmcplugin.setContent(int(sys.argv[1]), 'livetv')#movies
        xbmc.executebuiltin("Container.SetViewMode(560)")#503
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 603: FoitaTuga.FTT_encontrar_videos_filmes(name,url,mvoutv)
elif mode == 604: FoitaTuga.FTT_pesquisar_filmes()
elif mode == 605: FoitaTuga.FTT_Menu_Filmes(artfolder)
elif mode == 606: FoitaTuga.FTT_Menu_Filmes_Por_Categorias(artfolder)
elif mode == 607: FoitaTuga.FTT_Menu_Filmes_Brevemente(artfolder)
elif mode == 608:
        FoitaTuga.FTT_Top_Vistos(artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'livetv')#movies
        xbmc.executebuiltin("Container.SetViewMode(560)")#503
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
#----------------------------------------------  CINEMATUGA.net  -------------------------------------------------------
elif mode == 700: print ""; Play.PLAY_movie(url,name,iconimage,checker,fanart)#,nomeAddon)
elif mode == 701:
        Cinematuga.CMT_MenuPrincipal(artfolder)
        #setViewMode_menuCMT()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 702:
        Cinematuga.CMT_encontrar_fontes_filmes(url,artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'livetv')#movies
        xbmc.executebuiltin("Container.SetViewMode(560)")#503
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 703: Cinematuga.CMT_encontrar_videos_filmes(name,url,mvoutv)
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
elif mode == 719:
        Cinematuga.CMT_Menu_Filmes_Por_Qualidade(artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------  CINEMATUGA.eu  -------------------------------------------------------
elif mode == 800: print ""; Play.PLAY_movie(url,name,iconimage,checker,fanart)
elif mode == 801:
        CinematugaEu.CME_MenuPrincipal(artfolder)
        #setViewMode_menuFTT()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 802:
        CinematugaEu.CME_encontrar_fontes_filmes(url)
        xbmcplugin.setContent(int(sys.argv[1]), 'livetv')#movies
        xbmc.executebuiltin("Container.SetViewMode(560)")#503
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 803: CinematugaEu.CME_encontrar_videos_filmes(name,url,mvoutv)
elif mode == 804: CinematugaEu.CME_pesquisar_filmes()
elif mode == 805: CinematugaEu.CME_Menu_Filmes(artfolder)
elif mode == 806: CinematugaEu.CME_Menu_Filmes_Por_Categorias(artfolder)
elif mode == 807: CinematugaEu.CME_Menu_Filmes_Brevemente(artfolder)
elif mode == 808:
        CinematugaEu.CME_Top_Vistos(artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(503)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
#----------------------------------------------  CINEMAEMCASA  -------------------------------------------------------
elif mode == 900: print ""; Play.PLAY_movie(url,name,iconimage,checker,fanart)
elif mode == 901:
        CinemaEmCasa.CMC_MenuPrincipal(artfolder)
        #setViewMode_menuMVT()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 902:
        CinemaEmCasa.CMC_encontrar_fontes_filmes(url)
        xbmcplugin.setContent(int(sys.argv[1]), 'livetv')
        xbmc.executebuiltin("Container.SetViewMode(560)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 903: CinemaEmCasa.CMC_encontrar_videos_filmes(name,url,mvoutv)
elif mode == 904: CinemaEmCasa.CMC_pesquisar_filmes()
elif mode == 905:
        CinemaEmCasa.CMC_Menu_Filmes_Top_Semanal(artfolder)
        xbmcplugin.setContent(int(sys.argv[1]), 'livetv')
        xbmc.executebuiltin("Container.SetViewMode(560)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 906: CinemaEmCasa.CMC_Menu_Filmes_Por_Categorias(artfolder)
elif mode == 907: CinemaEmCasa.CMC_Menu_Filmes_Por_Ano(artfolder)

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
        
elif mode == 2998:
        SEARCHTMDBMOVIES()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(515)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 2999:
        BREVEMFILMES()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(515)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
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
elif mode == 3008:
        EMEXIBICAO()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(515)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 3009:
        MVOTADAS()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(515)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 3010:
        MPOPULARESTV()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(515)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 3011:
        SEARCHTMDBTV()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(515)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
elif mode == 6000:
        Play.PLAY_episodes(url,name,iconimage,checker,fanart)

elif mode == 7000:
        INDEX(url,name)
elif mode == 7001:
        tt = 'tt2267998'
        n = 'gone girl'
        item = xbmcgui.ListItem(path=url)
	item.setProperty("IsPlayable", "true")
        #xbmc.Player().play('plugin://plugin.video.Sites_dos_Portugas/?mode=7000&url='+url, item)
        xbmc.Player().play('plugin://plugin.video.Sites_dos_Portugas/?url='+tt+'&mode=9000&name='+n, item)
        #xbmcxbmc(url,name)
        
elif mode == 7500:
        ProcurarFilmesSeries()
        
elif mode == 8000:
        Funcoes.trailer(namet,url)

elif mode == 9000:
        PesquisaExterna.pesquisar(name,url,automatico)
elif mode == 9001:
        passar_nome_pesquisa_externa(name,url)
elif mode == 9002:
        Funcoes.playparser(namet, url, year, urltrailer)
elif mode == 9003:
        ositems = re.compile('(.+?)[|](.+?)[|](.+?)[|](.+?)[|](.+?)[|](.*)').findall(mvoutv)
        porada = ositems[0][0]
        podio = ositems[0][1]
        show = ositems[0][2]
        idtv = ositems[0][3]
        idmdb = ositems[0][4].replace('tt','')
        anoano = ositems[0][5]
        item = xbmcgui.ListItem(path=url)
	item.setProperty("IsPlayable", "true")
        xbmc.Player().play('plugin://plugin.video.genesis/?action=play&name='+show+'&imdb='+idmdb+'&season='+porada+'&show='+show+'&tvdb='+idtv+'&year='+anoano+'&episode='+podio)
        #Funcoes.playparser(idmdb,porada,show,idtv,anoano,podio)
elif mode == 9004:
        procurarOnde(mvoutv, namet, url, year, urltrailer, name, iconimage)

elif mode == 9005:
       # item = xbmcgui.ListItem(path=url)
	#item.setProperty("IsPlayable", "false")
        #xbmc.Player().play('plugin://plugin.video.Sites_dos_Portugas/?mode=7000&url='+url, item)
        xbmc.Player().play('plugin://plugin.video.Sites_dos_Portugas/?url='+url+'&mode=9004&name='+name+'&namet='+namet+'&mvoutv='+mvoutv+'&year='+year+'&urltrailer='+urltrailer+'&iconimage='+iconimage)#, item)
        #xbmcxbmc(url,name)

elif mode == 10000:
        SITESdosPORTUGAS()
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin("Container.SetViewMode(502)")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 10001:
        dirtodos(url)

elif mode == 20000:
        ratoTV(url)
elif mode == 20001:
        MenuFilmesRato()
elif mode == 20002:
        tvoumv(name,url)
elif mode == 20003:
        ratoTVTV(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
