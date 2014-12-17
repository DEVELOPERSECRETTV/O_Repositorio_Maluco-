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



import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,time,os,threading
from Funcoes import thetvdb_api, themoviedb_api, themoviedb_api_tv, theomapi_api, themoviedb_api_IMDB, themoviedb_api_IMDB_episodios, themoviedb_api_TMDB
from Funcoes import thetvdb_api_tvdbid, thetvdb_api_episodes, themoviedb_api_search_imdbcode, themoviedb_api_pagina, themoviedb_api_IMDB1, theomapi_api_nome
from Funcoes import addDir, addDir1, addDir2, addLink, addLink1, addDir_teste, addDir_trailer, addDir_episode
from Funcoes import get_params,abrir_url

num_f = 0
num_s = 0
num_f_TFV = []
num_s_TFV = []
num_f_TFC = []
num_s_TFC = []
num_f_MVT = []
num_s_MVT = []
num_f_TPT = []
num_s_TPT = []
num_f_FTT = []
num_s_FTT = []
num_f_CMT = []
num_s_CMT = []
num_f_CME = []
num_s_CME = []
num_f_CMC = []
num_s_CMC = []

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
	
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def pesquisar():
        
        if name == '[B][COLOR green]PRO[/COLOR][COLOR yellow]C[/COLOR][COLOR red]URAR[/COLOR][/B] (Filmes/Séries)' or name == '- Procurar':
                FS = 'FS'
        if name == '[B][COLOR green]PRO[/COLOR][COLOR yellow]C[/COLOR][COLOR red]URAR[/COLOR][/B] (Filmes)':
                FS = 'F'
        if name == '[B][COLOR green]PRO[/COLOR][COLOR yellow]C[/COLOR][COLOR red]URAR[/COLOR][/B] (Séries)':
                FS = 'S'
	keyb = xbmc.Keyboard('', 'Escreva o parâmetro de pesquisa')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		pesquisou = search
                #nome_pesquisa = nome_pesquisa.replace("'",'')
                a_q = re.compile('\w+')
                qq_aa = a_q.findall(search)
                search = ''
                conta = 0
                for q_a_q_a in qq_aa:
                        if len(q_a_q_a) > 0 or q_a_q_a == '1' or q_a_q_a == '2' or q_a_q_a == '3' or q_a_q_a == '4'or q_a_q_a == '5' or q_a_q_a == '6':
                        #if len(q_a_q_a) > 2:
                                if conta == 0:
                                        search = q_a_q_a
                                        conta = 1
                                else: search = search + '+' + q_a_q_a
		encode=urllib.quote(search)
		progress = xbmcgui.DialogProgress()
		a = 1
##                percent = 0
##                message = ''
##                site = ''
##                progress.create('Progresso', 'A Procurar')
##                progress.update( percent, 'A Procurar...', 'Por favor aguarde.', "" )
		try: xbmcgui.Dialog().notification('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png', 10000, sound=False)
                except: xbmc.executebuiltin("Notification(%s,%s, 10000, %s)" % ('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png'))

                addDir1('[COLOR yellow]PROCUROU POR:[/COLOR] '+str(encode).replace('%2B',' '),'url',1004,artfolder + 'SDPI.png',False,'')
           
                if FS == 'FS' or FS == 'F':
                        
                        threads = []
                        
                        addDir1('[B][COLOR blue]Filmes:[/COLOR][/B]','url',1004,artfolder + 'FILMES1.png',False,'')
                        FSS = 'F'

                        url_pesquisa = 'http://www.tuga-filmes.us/search?q=' + str(encode)
                        try:
                                html_source = abrir_url(url_pesquisa)
                        except: html_source = ''
                        i=0
                        items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
                        for item in items:
                                i = i + 1
                                a = str(i)
                                if i < 10: a = '0'+a
                                TFV = threading.Thread(name='TFV'+str(i), target=encontrar_fontes_pesquisa_TFV , args=(url_pesquisa,pesquisou,FSS,item,))
                                threads.append(TFV)
                        #num_f_TFV,num_s_TFV = encontrar_fontes_pesquisa_TFV(url_pesquisa,pesquisou,FSS)
                        
                        url_pesquisa = 'http://www.tuga-filmes.info/search?q=' + str(encode)
                        try:
                                html_source = abrir_url(url_pesquisa)
                        except: html_source = ''
                        i=0
                        items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
                        for item in items:
                                i = i + 1
                                a = str(i)
                                if i < 10: a = '0'+a
                                TFC = threading.Thread(name='TFC'+str(i), target=encontrar_fontes_filmes_TFC , args=(url_pesquisa,pesquisou,FSS,item,))
                                threads.append(TFC)
                        #num_f_TFC,num_s_TFC = encontrar_fontes_filmes_TFC(url_pesquisa,pesquisou,FSS)
                        
                        url_pesquisa = 'http://www.movie-tuga.blogspot.pt/search?q=' + str(encode)
                        try:
                                html_source = abrir_url(url_pesquisa)
                        except: html_source = ''
                        i=0
                        items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
                        for item in items:
                                i = i + 1
                                a = str(i)
                                if i < 10: a = '0'+a
                                MVT = threading.Thread(name='MVT'+str(i), target=encontrar_fontes_pesquisa_MVT , args=(url_pesquisa,pesquisou,FSS,item,))
                                threads.append(MVT)
                        #num_f_MVT,num_s_MVT = encontrar_fontes_pesquisa_MVT(url_pesquisa,pesquisou,FSS)
                        
                        url_pesquisa = 'http://toppt.net/?s=' + str(encode)
                        try:
                                html_source = abrir_url(url_pesquisa)
                        except: html_source = ''
                        i=0
                        items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
                        for item in items:
                                i = i + 1
                                a = str(i)
                                if i < 10: a = '0'+a
                                TPT = threading.Thread(name='TPT'+str(i), target=encontrar_fontes_filmes_TPT , args=(url_pesquisa,pesquisou,FSS,item,))
                                threads.append(TPT)
                        #num_f_TPT,num_s_TPT = encontrar_fontes_filmes_TPT(url_pesquisa,pesquisou,FSS)
                        
                        url_pesquisa = 'http://foitatugacinemaonline.blogspot.pt/search?q=' + str(encode) + '&submit=Buscar'
                        try:
                                html_source = abrir_url(url_pesquisa)
                        except: html_source = ''
                        i=0
                        items = re.findall("<a class='comment-link'(.+?)<div class='post-footer'>", html_source, re.DOTALL)
                        for item in items:
                                i = i + 1
                                a = str(i)
                                if i < 10: a = '0'+a
                                FTT = threading.Thread(name='FTT'+str(i), target=encontrar_fontes_pesquisa_FTT , args=(url_pesquisa,pesquisou,FSS,item,))
                                threads.append(FTT)
                        #num_f_FTT,num_s_FTT = encontrar_fontes_pesquisa_FTT(url_pesquisa,pesquisou,FSS)

                        url_pesquisa = 'http://www.cinematuga.net/search?q=' + str(encode)
                        try:
                                html_source = abrir_url(url_pesquisa)
                        except: html_source = ''
                        i=0
                        items = re.findall("<h3 class='post-title entry-title'(.*?)<span class='post-location'>", html_source, re.DOTALL)
                        for item in items:
                                i = i + 1
                                a = str(i)
                                if i < 10: a = '0'+a
                                CMT = threading.Thread(name='CMT'+str(i), target=encontrar_fontes_pesquisa_CMT , args=(url_pesquisa,pesquisou,FSS,item,))
                                threads.append(CMT)
                        #num_f_CMT,num_s_CMT = encontrar_fontes_pesquisa_CMT(url_pesquisa,pesquisou,FSS)

                        url_pesquisa = 'http://www.cinematuga.eu/search?q=' + str(encode)
                        try:
                                html_source = abrir_url(url_pesquisa)
                        except: html_source = ''
                        i = 0
                        items = re.findall("<h3 class='post-title entry-title'(.+?)<div class='post-footer'>", html_source, re.DOTALL)
                        for item in items:
                                i = i + 1
                                a = str(i)
                                if i < 10: a = '0'+a
                                CME = threading.Thread(name='CME'+str(i), target=encontrar_fontes_pesquisa_CME , args=(url_pesquisa,pesquisou,FSS,item,))
                                threads.append(CME)
                        #num_f_CME,num_s_CME = encontrar_fontes_pesquisa_CME(url_pesquisa,pesquisou,FSS)

                        url_pesquisa = 'http://www.cinemaemcasa.pt/search?q=' + str(encode)
                        try:
                                html_source = abrir_url(url_pesquisa)
                        except: html_source = ''
                        i = 0
                        items = re.findall("<h2 class='post-title entry-title'>(.+?)<div class='post-footer'>", html_source, re.DOTALL)
                        for item in items:
                                i = i + 1
                                a = str(i)
                                if i < 10: a = '0'+a
                                CMC = threading.Thread(name='CMC'+str(i), target=encontrar_fontes_pesquisa_CMC , args=(url_pesquisa,pesquisou,FSS,item,))
                                threads.append(CMC)
                        #num_f_CMC,num_s_CMC = encontrar_fontes_pesquisa_CMC(url_pesquisa,pesquisou,FSS)

                        [i.start() for i in threads]

                        [i.join() for i in threads]
                        
                        if num_f_TFV == []: num_f_TFV.append(0)
                        if num_f_TFC == []: num_f_TFC.append(0)
                        if num_f_TPT == []: num_f_TPT.append(0)
                        if num_f_MVT == []: num_f_MVT.append(0)
                        if num_f_CME == []: num_f_CME.append(0)
                        if num_f_FTT == []: num_f_FTT.append(0)
                        if num_f_CMT == []: num_f_CMT.append(0)
                        if num_f_CMC == []: num_f_CMC.append(0)
                        num_f = num_f_TFV[0] + num_f_TPT[0] + num_f_TFC[0] + num_f_FTT[0] + num_f_MVT[0] + num_f_CMT[0] + num_f_CME[0] + num_f_CMC[0]
                        if num_f == 0: addDir1('-----','url',1004,artfolder,False,'')
       
                if FS == 'FS' or FS == 'S':
                        threads = []
                        addDir1('[B][COLOR blue]Séries:[/COLOR][/B]','url',1004,artfolder + 'SERIES1.png',False,'')
                        FSS = 'S'

                        url_pesquisa = 'http://toppt.net/?s=' + str(encode)
                        try:
                                html_source = abrir_url(url_pesquisa)
                        except: html_source = ''
                        i=0
                        items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
                        for item in items:
                                i = i + 1
                                a = str(i)
                                if i < 10: a = '0'+a
                                TPT = threading.Thread(name='TPT'+str(i), target=encontrar_fontes_filmes_TPT , args=(url_pesquisa,pesquisou,FSS,item,))
                                threads.append(TPT)
                        #num_f_TPT,num_s_TPT = encontrar_fontes_filmes_TPT(url_pesquisa,pesquisou,FSS)

                        url_pesquisa = 'http://www.tuga-filmes.us/search?q=' + str(encode)
                        try:
                                html_source = abrir_url(url_pesquisa)
                        except: html_source = ''
                        i=0
                        items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
                        for item in items:
                                i = i + 1
                                a = str(i)
                                if i < 10: a = '0'+a
                                TFV = threading.Thread(name='TFV'+str(i), target=encontrar_fontes_pesquisa_TFV , args=(url_pesquisa,pesquisou,FSS,item,))
                                threads.append(TFV)
                        #num_f_TFV,num_s_TFV = encontrar_fontes_pesquisa_TFV(url_pesquisa,pesquisou,FSS)

                        [i.start() for i in threads]

                        [i.join() for i in threads]

                        if num_s_TFV == []: num_s_TFV.append(0)
                        if num_s_TPT == []: num_s_TPT.append(0)
                        num_s = num_s_TFV[0] + num_s_TPT[0]
                        if num_s == 0: addDir1('-----','url',1004,artfolder,False,'')

##                progress.close()
                #msg = ' (%s)' % timeout_msg if timeout_msg else ''
                #builtin = 'XBMC.Notification(%s,No Useable Sources Found%s, 5000, %s)'
                #xbmc.executebuiltin(builtin % ('teste', 'testado', ''))
                xbmcplugin.setContent(int(sys.argv[1]), 'livetv')#movies
                xbmc.executebuiltin("Container.SetViewMode(560)")#502
                xbmcplugin.endOfDirectory(int(sys.argv[1]))


#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def encontrar_fontes_pesquisa_TFV(url,pesquisou,FS,item):

        if item != '':
                try:
                        thumb = ''
                        fanart = ''
                        versao = ''
                        audio_filme = ''
                        imdbcode = ''
                        tirar_ano = ''
                        genre = ''

                        imdb = re.compile('"http://www.imdb.com/title/(.+?)/"').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
                        if 'Portug' and 'Legendado' in item: versao = '[COLOR blue]2 VERSÕES[/COLOR]'
                        genero = re.compile("nero</b>:(.+?)<br />").findall(item)
                        if genero: genre = genero[0]
                        else: genre = ''
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
                        #nome = urletitulo[0][1]
                        nometitulo = urletitulo[0][1].replace('&#8217;',"'").replace('&amp;','&').replace('&#39;',"'").replace('&#8211;',"-")
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

                        if ano: anofilme = ano[0]
                        else: anofilme = ''
                        if 'Temporada' in urletitulo[0][1] or 'Season' in urletitulo[0][1] or 'Mini-Série' in urletitulo[0][1]:
                                nome = urletitulo[0][1]
                                nnnn = re.compile('(.+?)[(].+?[)]').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                                if nnnn : nome_pesquisa = nnnn[0]
                                else: nome_pesquisa = nome
                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,anofilme.replace(' ',''))
                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                if ftart:
                                        fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                        if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
        ##                                        for nt in range(20):
        ##                                                try:
        ##                                                        thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-'+str(nt)+'.jpg'
        ##                                                        f = urllib2.urlopen(urllib2.Request(thumb))
        ##                                                        deadLinkFound = False
        ##                                                except: deadLinkFound = True
        ##                                                if deadLinkFound == False: break                                        
                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                if snpse: sinopse = snpse[0]
                        else:
                                #nome = urletitulo[0][1]
                                nnnn = re.compile('.+?[(](.+?)[)]').findall(nome)
                                if not nnnn: nnnn = re.compile('.+?[[](.+?)[]]').findall(nome)
                                if nnnn : nome_pesquisa = nnnn[0]
                                else: nome_pesquisa = nome
                                if imdbcode != '':
                                        try:
                                                fanart,tmdb_id,poster,sin = themoviedb_api_IMDB().fanart_and_id(str(imdbcode),ano[0].replace(' ',''))
                                                if sinopse == '': sinopse = sin
                                                if fanart == '': fanart,tmb,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano[0].replace(' ',''))
                                                if thumb == '' or 's1600' in thumb: thumb = poster
                                        except:pass
                                else:
                                        try:
                                                fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano[0].replace(' ',''))
                                                if thumb == '' or 's1600' in thumb: thumb = poster
                                        except:pass
                                
                        #return
                        
                        if qualidade:
                                qualidade = qualidade[0]
                        else:
                                qualidade = ''
                        if genre == '': genre = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'

                        try:
                                if "Temporada" in urletitulo[0][1] or 'Season' in urletitulo[0][1]:
                                        num_mode = 42
                                else:
                                        num_mode = 33
                                if anofilme != '---' and sinopse != '---' and imdbcode != '---' and genre != '---':
                                        if ("Temporada" not in urletitulo[0][1] and FS == 'FS') or ("Temporada" not in urletitulo[0][1] and FS == 'F'):
                                                addDir_trailer('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + anofilme.replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',num_mode,thumb.replace('s72-c','s320'),sinopse,fanart,anofilme,genre,nome_pesquisa,urletitulo[0][0])
                                                num_f_TFV.append(1)
                                        if ("Temporada" in urletitulo[0][1] and FS == 'FS') or ("Temporada" in urletitulo[0][1] and FS == 'S'):
                                                addDir_trailer('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + nometitulo.replace(tirar_ano,'') + '[/COLOR][/B][COLOR yellow](' + anofilme.replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',num_mode,thumb.replace('s72-c','s320'),sinopse,fanart,anofilme,genre,nome_pesquisa,urletitulo[0][0])
                                                num_s_TFV.append(1)
                        except: pass
                                        #addDir('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0] + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',num_mode,thumbnail[0].replace('s72-c','s320'),'','')
                                        #addDir('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0] + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',num_mode,thumbnail[0].replace('s72-c','s320'),'','')				
                except: pass
        else: return #num_f_TFV,num_s_TFV
	return# num_f_TFV,num_s_TFV

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def encontrar_fontes_filmes_TFC(url,pesquisou,FS,item):
        pt_en = 0

        if item != '':
                try:
                        fanart = ''
                        thumb = ''
                        versao = ''
                        sinopse = ''
                        imdbcode = ''
                        genero = ''
                        qualidade = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
                        pt_en_f = re.compile('<iframe (.+?)</iframe>').findall(item)
                        if '---------------------------------------' in item and len(pt_en_f) > 1: versao = '[COLOR blue] 2 VERSÕES[/COLOR]'
                        assist = re.findall(">ASSISTIR.+?", item, re.DOTALL)
                        if len(assist) > 1: versao = '[COLOR blue] 2 VERSÕES[/COLOR]'
			urletitulo = re.compile("<a href=\'(.+?)\' title=\'(.+?)\'>").findall(item)
			qualidade_ano = re.compile('<b>VERS\xc3\x83O:.+?</b><span style="font-size: x-small;">(.+?)<').findall(item)
			snpse = re.compile('<b>SINOPSE:.+?</b><span style="font-size: x-small;">(.+?)<').findall(item)
			if snpse: sinopse = snpse[0]
			else: sinopse = ''
			thumbnail = re.compile('<img alt="" border="0" src="(.+?)"').findall(item)
			if thumbnail: thumb = thumbnail[0]
			print urletitulo,thumbnail
			ano = ''
			qualidade = ''
			e_qua = 'nao'
			calid = ''
			if qualidade_ano != []:
                                for q_a in qualidade_ano:
                                        a_q = re.compile('\d+')
                                        qq_aa = a_q.findall(q_a)
                                        for q_a_q_a in qq_aa:
                                                if len(q_a_q_a) == 4:
                                                        ano = q_a_q_a
                                quali = re.compile('\w+')
                                qualid = quali.findall(q_a)
                                for qua_qua in qualid:
                                        if len(qua_qua) == 4 and qua_qua == ano:
                                                e_qua = 'sim'
                                                qua_qua = ''
                                                espaco = ''
                                                espa = 0
                                        if e_qua == 'sim' and espa < 2:
                                                espa = espa + 1
                                        if e_qua == 'sim' and espa == 2:
                                                qualidade = qualidade + espaco + qua_qua
                                                espaco = ' '
                                if len(ano) < 4:
                                        ano = ''
                                if qualidade == 'PT PT':
                                        qualidade = 'PT-PT'
                                if qualidade == '':
                                        quali_titi = urletitulo[0][1].replace('á','a')
                                        quali_titi = urletitulo[0][1].replace('é','e')
                                        quali_titi = urletitulo[0][1].replace('í','i')
                                        quali_titi = urletitulo[0][1].replace('ó','o')
                                        quali_titi = urletitulo[0][1].replace('ú','u')
                                        quali = re.compile('\w+')
                                        qualid = quali.findall(q_a)
                                        for qua_qua in qualid:
                                                qua_qua = str.capitalize(qua_qua)
                                                calid = calid + ' ' + qua_qua
                                        tita = re.compile('\w+')
                                        titalo = tita.findall(quali_titi)
                                        for tt in titalo:
                                                tt = str.capitalize(tt)
                                                if tt in calid:
                                                        qualidade = re.sub(tt,'',calid)
                                                        calid = re.sub(tt,'',calid)
                                        qqqq = re.compile('\w+')
                                        qqqqq = qqqq.findall(qualidade)
                                        for qqq in qqqqq:
                                                if qqq in quali_titi:
                                                        qualidade = qualidade.replace(qqq,'')
                                        nnnn = re.compile('\d+')
                                        nnnnn = nnnn.findall(qualidade)
                                        for nnn in nnnnn:
                                                if nnn in ano:
                                                        qualidade = qualidade.replace(nnn,'')
                                        quatit = re.compile('\s+')
                                        qualititulo = quatit.findall(qualidade)
                                        for q_t in qualititulo:
                                                if len(q_t)>1:
                                                        qualidade = qualidade.replace(q_t,'')
                                        if qualidade == 'Pt Pt':
                                                qualidade = 'PT-PT'
                        else:
                                qualidade = ''
                        if 'Pt Pt' in qualidade:
                                qualidade = qualidade.replace('Pt Pt','PT-PT')
                        if 'PT PT' in qualidade:
                                qualidade = qualidade.replace('PT PT','PT-PT')
                        nome = urletitulo[0][1]
                        nome = nome.replace('&#8216;',"'")
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&amp;','&')
                        sinopse = sinopse.replace('&#8216;',"'")
                        sinopse = sinopse.replace('&#8217;',"'")
                        sinopse = sinopse.replace('&#8211;',"-")
                        sinopse = sinopse.replace('&#39;',"'")
                        sinopse = sinopse.replace('&amp;','&')
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        tirar_ano = '(' + str(q_a_q_a) + ')'
                                        nome = nome.replace(tirar_ano,'')
                                        
                        nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                        if not nnnn: nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                        if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                        if not nnnn: nnnn = re.compile('(.+?)[:] ').findall(nome)
                        if nnnn: nome_pesquisa = nnnn[0]
                        else: nome_pesquisa = nome
                        try:
                                fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano)
                                if thumb == '': thumb = poster
                        except: pass

                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        if qualidade == '': qualidade = '---'
                                        
                        try:

                                if 'BREVEMENTE' not in item:
                                        if 'ASSISTIR O FILME' in item:
                                                addDir_trailer('[COLOR orange]TFC | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR][COLOR red] (' + qualidade + ')[/COLOR]' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',73,thumb.replace('s1600','s320').replace('.gif','.jpg'),sinopse,fanart,ano,qualidade,nome,urletitulo[0][0])
                                                num_f_TFC.append(1)
                                        #addDir('[COLOR orange]TFC | [/COLOR][B][COLOR green]' + urletitulo[0][1].replace('&#39;',"'") + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR][COLOR red] (' + qualidade + ')[/COLOR]' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',73,thumbnail[0].replace('s1600','s320').replace('.gif','.jpg'),'','')
                                        
                        except: pass
                except: pass
        else: return #num_f_TFC,num_s_TFC
	return# num_f_TFC,num_s_TFC

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def encontrar_fontes_pesquisa_MVT(url,pesquisou,FS,item):

        if item != '':
                try:
                        thumb = ''
                        fanart = ''
                        sinopse = ''
                        genero = ''
                        imdbcode = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
                        url = re.compile('<div class="btns"><a href="(.+?)" target="Player">').findall(item)
                        #url = re.compile("<a href='(.+?)'><div align=").findall(item)
                        if 'http' not in url[0]:
                                url[0] = 'http:' + url[0]

                        snpse = re.compile("<div id='imgsinopse'>(.+?)</div>").findall(item)
                        if snpse: sinopse = snpse[0]
                        sinopse = sinopse.replace('&#8216;',"'")
                        sinopse = sinopse.replace('&#8217;',"'")
                        sinopse = sinopse.replace('&#8211;',"-")
                        sinopse = sinopse.replace('&#8220;',"'")
                        sinopse = sinopse.replace('&#8221;',"'")
                        sinopse = sinopse.replace('&#39;',"'")
                        sinopse = sinopse.replace('&amp;','&')
                        
                        gen = re.compile("nero:</strong>(.+?)</div>").findall(item)
                        if gen: genero = gen[0]
                        
                        if 'Qualidade:' in item:
                                qualidade = re.compile("<strong>Qualidade:</strong>(.+?)</div>").findall(item)
                                qualidade_filme = qualidade[0].replace('&#8211;',"-")
                        else:
                                qualidade_filme = ''
                                
                        ano = re.compile('<strong>Lan\xc3\xa7amento:</strong>(.+?)</div>').findall(item)
                        if ano: ano_filme = ano[0].replace('20013','2013').replace(' ','')
                        else: ano_filme = ''
                        
                        thumbnail = re.compile('src="(.+?)"').findall(item)
                        if 'http' not in thumbnail[0]: thumbnail[0] = 'http:' + thumbnail[0]
                        if thumbnail: thumb = thumbnail[0].replace('s72-c','s320')
                        
                        titulo = re.compile("<strong>T\xc3\xadtulo original:</strong>(.+?)</div>").findall(item)
                        titulo[0] = titulo[0].replace('&#8217;',"'")
                        titulo[0] = titulo[0].replace('&#8211;',"-")
                        if 'Dear John' in titulo[0] and ano[0] == '2013': titulo[0] = titulo[0].replace('Dear John','12 Anos Escravo')
                        nome = titulo[0]
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('PT',"")
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        tirar_ano = '(' + str(q_a_q_a) + ')'
                                        nome = nome.replace(tirar_ano,'')
                        
                        nome_pesquisa = nome
                        if imdbcode != '':
                                try:
                                        fanart,tmdb_id,poster,sin = themoviedb_api_IMDB().fanart_and_id(str(imdbcode),ano_filme)
                                        if sinopse == '': sinopse = sin
                                        if fanart == '': fanart,tmb,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano_filme)
                                except:pass
                        else:
                                try:
                                        fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano_filme)
                                except:pass
                        
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'

                        try:
                                addDir_trailer('[COLOR orange]MVT | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',url[0].replace(' ','%20')+'IMDB'+imdbcode+'IMDB',103,thumb.replace(' ','%20'),sinopse,fanart,ano_filme,genero,nome,url[0].replace(' ','%20'))
                                num_f_MVT.append(1)
                        except: pass
                except: pass
        else: return# num_f_MVT,num_s_MVT
	return #num_f_MVT,num_s_MVT

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#


def encontrar_fontes_filmes_TPT(url,pesquisou,FS,item):
        
        series = 0

        if item != '':
                try:
                        sinopse = ''
                        fanart = ''
                        thumb = ''
                        genero = ''
                        qualidade = ''
                        audio_filme = ''
                        imdbcode = ''

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
                                        
                        if 'Temporada' in nome or 'Season' in nome or 'Mini-Série' in nome:
                                n = re.compile('(.+?)[[].+?[]]').findall(nome)
                                if n: nome_pesquisa = n[0]
                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme)
                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                if ftart:
                                        fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                        if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'                                       
                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                if snpse: sinopse = snpse[0]
                        else:
                                nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?)[:] ').findall(nome)
                                if nnnn: nome_pesquisa = nnnn[0]
                                else: nome_pesquisa = nome
                                if imdbcode != '':
                                        try:
                                                fanart,tmdb_id,poster,sin = themoviedb_api_IMDB().fanart_and_id(str(imdbcode),ano_filme)
                                                if sinopse == '': sinopse = sin
                                                if fanart == '': fanart,tmb,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano_filme)
                                                if thumb == '': thumb = poster
                                        except:pass
                                else:
                                        try:
                                                fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano_filme)
                                                if thumb == '': thumb = poster
                                        except: pass

                        ano_filme = '('+ano_filme+')'
                        qualidade = '('+qualidade
                        audio_filme = audio_filme+')'
                        if series == 1:
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

                                qualidade = ''
                                ano_filme = ''
                                audio_filme = ''                  

                        if genero == '':
                                genre = '---'
                                genero = '---'
                        if sinopse == '':
                                plot = '---'
                                sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'

                        try:
                                if ano and genr and audio:
                                        if (("Season" in nome or 'Mini-Série' in nome or 'Mini-Serie' in nome) and FS == 'FS') or (("Season" in nome or 'Mini-Série' in nome or 'Mini-Serie' in nome) and FS == 'S'):
                                                addDir_trailer('[COLOR orange]TPT | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',233,thumb,sinopse,fanart,ano_filme.replace('(','').replace(')',''),genero,nome_pesquisa,urletitulo[0][0])
                                                num_s_TPT.append(1)
                                        if ("Season" not in nome and 'Mini-Série' not in nome and 'Mini-Serie' not in nome and FS == 'FS') or ("Season" not in nome and 'Mini-Série' not in nome and 'Mini-Serie' not in nome and FS == 'F'):
                                                addDir_trailer('[COLOR orange]TPT | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',233,thumb,sinopse,fanart,ano_filme.replace('(','').replace(')',''),genero,nome_pesquisa,urletitulo[0][0])
                                                num_f_TPT.append(1)
                        except: pass
                except: pass
        else: return #num_f_TPT,num_s_TPT
	return# num_f_TPT,num_s_TPT

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def encontrar_fontes_pesquisa_FTT(url,pesquisou,FS,item):
        

        if item != '':
                try:
                        thumb = ''
                        genero = ''
                        sinopse = ''
                        fanart = ''
                        anofilme= ''
                        qualidade_filme = ''
                        imdbcode = ''
                        audio_filme = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''

                        urletitulo = re.compile("<a href='(.+?)' title='(.+?)'>").findall(item)
                        if not urletitulo: urletitulo = re.compile("<a href='(.+?)'>(.+?)</a>").findall(item)
                        if urletitulo:
                                urlvideo = urletitulo[0][0]
                                nome = urletitulo[0][1]
                        else:
                                urlvideo = ''
                                nome = ''

                        try:
                                fonte_video = abrir_url(urlvideo)
                        except: fonte_video = ''
                        fontes_video = re.findall("<div class='post-body entry-content'>(.*?)<div style='clear: both;'>", fonte_video, re.DOTALL)
                        if fontes_video != []:
                                qualid = re.compile('ASSISTIR ONLINE (.*)\n').findall(fontes_video[0])
                                if qualid: qualidade_filme = qualid[0].replace('/ ',' ').replace('</b>','').replace('</span>','').replace('LEGENDADO','')
                                else:
                                        qualid = re.compile('[[]</span><span style=".+?"><span style=".+?">(.+?)</span><span style=".+?">[]]').findall(fontes_video[0])
                                        if qualid: qualidade_filme = qualid[0].replace('/ ','').replace('</b>','').replace('</span>','')

                                
                        snpse = re.compile('Sinopse.png"></a></div>\n(.+?)\n').findall(item)
                        if snpse: sinopse = snpse[0]
                        sinopse = sinopse.replace('&#8216;',"'")
                        sinopse = sinopse.replace('&#8217;',"'")
                        sinopse = sinopse.replace('&#8220;',"'")
                        sinopse = sinopse.replace('&#8221;',"'")
                        sinopse = sinopse.replace('&#8211;',"-")
                        sinopse = sinopse.replace('&#39;',"'")
                        sinopse = sinopse.replace('&amp;','&')
                                
                        ano = re.compile('<strong>Lan\xc3\xa7amento:</strong>(.+?)</div>').findall(item)
                        if ano: anofilme = ano[0]
                        else: anofilme = ''

                        generos = re.compile("rel='tag'>(.+?)</a>").findall(item)
                        conta = 0
                        for gener in generos:
                                if conta == 0:
                                        if gener.replace(' ','') != anofilme.replace(' ',''):
                                                genero = gener
                                                conta = conta + 1
                                else:
                                        if gener.replace(' ','') != anofilme.replace(' ',''):
                                                genero = genero +'  '+ gener
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(genero)
                        conta = 0
                        for q_a_q_a in qq_aa:
                                genero = genero.replace(str(q_a_q_a)+'  ','')
                        
                        thumbnail = re.compile('<img height=".+?" src="(.+?)" width=".+?"').findall(item)
                        if thumbnail: thumb = thumbnail[0].replace('s72-c','s320').replace('s1600','s320')
                        else:         
                                #thumbnail = re.compile('<a href="(.+?)" imageanchor="1"').findall(item)        
                                thumbnail = re.compile('document.write[(]bp_thumbnail_resize[(]"(.+?)",".+?"[)]').findall(item)
                                if thumbnail: thumb = thumbnail[0].replace('s72-c','s320').replace('s1600','s320')
                                else:
                                        #if not thumbnail: thumbnail = re.compile("<meta content='(.+?)' itemprop='image_url'/>").findall(item)
                                        thumbnail = re.compile('<a href="(.+?)" imageanchor="1"').findall(item)
                                        if thumbnail: thumb = thumbnail[0].replace('s72-c','s320').replace('s1600','s320')
                                        else:
                                                thumbnail = re.compile('<img alt="image" height=".+?" src="(.+?)" width=".+?"').findall(item)
                                                if thumbnail: thumb = thumbnail[0].replace('s72-c','s320').replace('s1600','s320')
                                                else:
                                                        thumbnail = re.compile('<img src="(.+?)" height=".+?" width=".+?"').findall(item)
                                                        if thumbnail: thumb = thumbnail[0].replace('s72-c','s320').replace('s1600','s320')
                        if 'container' in thumb:
                                thumbnail = re.compile('url=(.+?)blogspot(.+?)&amp;container').findall(thumb)
                                if thumbnail: thumb = thumbnail[0][0].replace('%3A',':').replace('%2F','/')+'blogspot'+thumbnail[0][1].replace('%3A',':').replace('%2F','/')

                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('(Pedido)',"").replace('[Pedido]','')
                        
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        anofilme = str(q_a_q_a)
                                        tirar_ano = '- ' + str(q_a_q_a)
                                        nome = nome.replace(tirar_ano,'')
                                        tirar_ano = '-' + str(q_a_q_a)
                                        nome = nome.replace(tirar_ano,'')
                                        tirar_ano = str(q_a_q_a)
                                        nome = nome.replace(tirar_ano,'')

                        if '[PT/PT]' in nome:
                                audio_filme = 'PT/PT'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')
                        if '[PT-PT]' in nome:
                                audio_filme = 'PT-PT'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')
                        if '[PT/BR]' in nome:
                                audio_filme = 'PT/BR'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')
                        if '[PT-BR]' in nome:
                                audio_filme = 'PT-BR'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')
                        if 'PT/PT' in nome:
                                audio_filme = 'PT/PT'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')
                        if 'PT-PT' in nome:
                                audio_filme = 'PT-PT'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')
                        if 'PT/BR' in nome:
                                audio_filme = 'PT/BR'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')
                        if 'PT-BR' in nome:
                                audio_filme = 'PT-BR'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')

                        nome = nome.replace('-- ',"")
                        nome = nome.replace(' --',"")
                        nome = nome.replace('--',"")

                        if audio_filme != '': qualidade_filme = qualidade_filme #+ ' - ' + audio_filme

                        nome = nome.replace('((','(')
                        nome = nome.replace('))',')')
                        nome = nome.replace('()','(')
                        nome = nome.replace('  ','')
                        nome = nome.replace(' - []','')
                        
                        nnnn = re.compile('.+?[(](.+?)[)]').findall(nome)
                        if not nnnn: nnnn = re.compile('.+?[[](.+?)[]]').findall(nome)
                        if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                        if not nnnn: nnnn = re.compile('(.+?)[:] ').findall(nome)
                        if nnnn : nome_pesquisa = nnnn[0]
                        else: nome_pesquisa = nome
                        if imdbcode != '':
                                try:
                                        fanart,tmdb_id,poster,sin = themoviedb_api_IMDB().fanart_and_id(str(imdbcode),anofilme)
                                        if sinopse == '': sinopse = sin
                                        if fanart == '': fanart,tmb,poster = themoviedb_api().fanart_and_id(nome_pesquisa,anofilme)
                                        if thumb == ''  or 'IMDb.png' in thumb or 'Sinopse' in thumb: thumb = poster
                                except:pass
                        else:
                                try:
                                        fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,anofilme)
                                        if thumb == ''  or 'IMDb.png' in thumb or 'Sinopse' in thumb: thumb = poster
                                except: pass
                        
                        
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        try:
                                addDir_trailer('[COLOR orange]FTT | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme.replace('</div>','') + ')[/COLOR]',urlvideo+'IMDB'+imdbcode+'IMDB',603,thumb,sinopse,fanart,anofilme,genero,nome,urlvideo)
                                num_f_FTT.append(1)
                        except: pass
                except: pass
        else: return #num_f_FTT,num_s_FTT
	return #num_f_FTT,num_s_FTT

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def encontrar_fontes_pesquisa_CMT(url,pesquisou,FS,item):
        

        if item != '':
                try:
                        thumb = ''
                        fanart = ''
                        versao = ''
                        audio_filme = ''
                        imdbcode = ''
                        ano_filme = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
                        #if 'Portug' and 'Legendado' in item: versao = '[COLOR blue]2 VERSÕES[/COLOR]'
                        genero = re.compile("nero</b>:(.+?)<br />").findall(item)
                        if genero: genre = genero[0]
                        else: genre = ''
                        resumo = re.compile("<b>Resumo</b>:(.+?)<br />").findall(item)
                        if resumo: sinopse = resumo[0]
                        else: sinopse = ''
                        titulooriginal = re.compile("tulo Original:</b>(.+?)<br />").findall(item)
                        if titulooriginal:
                                nome_original = titulooriginal[0]
                                #addDir1(nome_original,'','','',False,'')
                        else:
                                titulooriginal = re.compile("<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>(.+?)<br />").findall(item)
                                if titulooriginal:
                                        nome_original = titulooriginal[0]
                                else: nome_original = ''
                                #addDir1(nome_original,'','','',False,'')
                        ################urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)
                        urletitulo = re.compile("<a href='(.+?)'>(.+?)</a>").findall(item)
                        qualidade = re.compile("<b>Qualidade</b>: (.+?)<br />").findall(item)
                        if not qualidade: qualidade = re.compile("Ass.+?tir online .+?[(](.+?)[)]").findall(item)
                        ano = re.compile("<b>Ano</b>: (.+?)<br />").findall(item)
                        if ano: ano_filme = ano[0]
                        else: ano_filme = ''
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
                        nome = nome.replace('&#183;',"-")
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
                                        if ano_filme == '': ano_filme = str(q_a_q_a)
                                        
                        nnnn = re.compile('(.+?): ').findall(nome)
                        if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                        if nnnn : nome_pesquisa = nnnn[0]
                        else: nome_pesquisa = nome
                        if imdbcode != '':
                                try:
                                        fanart,tmdb_id,poster,sin = themoviedb_api_IMDB().fanart_and_id(str(imdbcode),ano_filme.replace(' ',''))
                                        if sinopse == '': sinopse = sin
                                        if fanart == '': fanart,tmb,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano_filme.replace(' ',''))
                                except:
                                        fanart = '---'
                                        tmdb_id = '---'
                                        poster = ''
                        else:
                                try:
                                        fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano_filme.replace(' ',''))
                                except: 
                                        fanart = '---'
                                        tmdb_id = '---'
                                        poster = ''

                        if qualidade:
                                qualidade = qualidade[0].replace('<b>','').replace('</b>','')
                        else:
                                qualidade = ''
                        if genre == '': genre = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        try:
##                                if ("Temporada" in urletitulo[0][1] and FS == 'FS') or ("Temporada" in urletitulo[0][1] and FS == 'S'):
##                                        num_mode = 712
##                                        addDir_teste('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',num_mode,thumb.replace('s72-c','s320'),sinopse,fanart,ano[0],genre)
                                if ("Temporada" not in urletitulo[0][1] and FS == 'FS') or ("Temporada" not in urletitulo[0][1] and FS == 'F'):
                                        num_mode = 703
                                        addDir_trailer('[COLOR orange]CMT | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow](' + ano_filme.replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',num_mode,thumb.replace('s72-c','s320'),sinopse,fanart,ano_filme.replace(' ',''),genre,nome,urletitulo[0][0])
                                        num_f_CMT.append(1)
                        except: pass
                except: pass
        else: return# num_f_CMT,num_s_CMT
	return #num_f_CMT,num_s_CMT

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def encontrar_fontes_pesquisa_CME(url,pesquisou,FS,item):
        

        if item != '':
                try:
                        
                        thumb = ''
                        genero = ''
                        sinopse = ''
                        fanart = ''
                        anofilme= ''
                        qualidade_filme = ''
                        imdbcode = ''
                        audio_filme = ''

                        imdb = re.compile('imdb.com/title/(.+?)"').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''

                        urletitulo = re.compile("<a href='(.+?)' title='(.+?)'>").findall(item)
                        if not urletitulo: urletitulo = re.compile("<a href='(.+?)'>(.+?)</a>").findall(item)
                        if urletitulo:
                                urlvideo = urletitulo[0][0].replace('#more','')
                                nome = urletitulo[0][1]
                        else:
                                urlvideo = ''
                                nome = ''
                                
                        snpse = re.compile('<b>sinopse</b><br>\n(.+?)<br>\n').findall(item)
                        if snpse: sinopse = snpse[0]
                        sinopse = sinopse.replace('&#8216;',"'")
                        sinopse = sinopse.replace('&#8217;',"'")
                        sinopse = sinopse.replace('&#8220;',"'")
                        sinopse = sinopse.replace('&#8221;',"'")
                        sinopse = sinopse.replace('&#8211;',"-")
                        sinopse = sinopse.replace('&#39;',"'")
                        sinopse = sinopse.replace('&amp;','&')
                                
                        ano = re.compile('<strong>Lan\xc3\xa7amento:</strong>(.+?)</div>').findall(item)
                        if ano: anofilme = ano[0]
                        else: anofilme = ''

                        generos = re.compile("rel='tag'>(.+?)</a>").findall(item)
                        conta = 0
                        for gener in generos:
                                if conta == 0:
                                        if gener.replace(' ','') != anofilme.replace(' ',''):
                                                genero = gener
                                                conta = conta + 1
                                else:
                                        if gener.replace(' ','') != anofilme.replace(' ',''):
                                                genero = genero +'  '+ gener
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(genero)
                        conta = 0
                        for q_a_q_a in qq_aa:
                                genero = genero.replace(str(q_a_q_a)+'  ','')

                        thumbnail = re.compile("<meta content='(.+?)' itemprop='image_url'/>").findall(item)
                        if not thumbnail: thumbnail = re.compile('<img class="alignleft" src="(.+?)">').findall(item)
                        if thumbnail: thumb = thumbnail[0].replace('s72-c','s320').replace('s1600','s320')
                        else: thumb = ''
               
                                

                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('(Pedido)',"").replace('[Pedido]','')
                        
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        anofilme = str(q_a_q_a)
                                        tirar_ano = '('+str(q_a_q_a)+')'
                                        nome = nome.replace(tirar_ano,'')

                        if audio_filme != '': qualidade_filme = qualidade_filme# + ' - ' + audio_filme
                        
                        nnnn = re.compile('.+?[(](.+?)[)]').findall(nome)
                        if not nnnn: nnnn = re.compile('.+?[[](.+?)[]]').findall(nome)
                        if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                        if not nnnn: nnnn = re.compile('(.+?)[:] ').findall(nome) 
                        if nnnn :
                                if 'Trilogia' in nnnn[0]: nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                                nome_pesquisa = nnnn[0]
                        else: nome_pesquisa = nome
                        if imdbcode != '':
                                try:
                                        fanart,tmdb_id,poster,sin = themoviedb_api_IMDB().fanart_and_id(str(imdbcode),anofilme)
                                        if sinopse == '': sinopse = sin
                                        if fanart == '': fanart,tmb,poster = themoviedb_api().fanart_and_id(nome_pesquisa,anofilme)
                                        if thumb == ''  or 'IMDb.png' in thumb or 'Sinopse' in thumb: thumb = poster
                                except:pass
                        else:
                                try:
                                        fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,anofilme)
                                        if thumb == ''  or 'IMDb.png' in thumb or 'Sinopse' in thumb: thumb = poster
                                except: pass
                        

                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        try:
                                addDir_trailer('[COLOR orange]CME | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme.replace('</div>','') + ')[/COLOR]',urlvideo+'IMDB'+imdbcode+'IMDB',803,thumb,sinopse,fanart,anofilme,genero,nome,urlvideo)
                                num_f_CME.append(1)
                        except: pass
                except: pass
	else: return #num_f_CME,num_s_CME
	return #num_f_CME,num_s_CME

#----------------------------------------------------------------------------------------------------------------------------------------------#

def encontrar_fontes_pesquisa_CMC(url,pesquisou,FS,item):

        if item != '':
                try:
                        
                        thumb = ''
                        fanart = ''
                        sinopse = ''
                        genero = ''
                        imdbcode = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
                        urltitulo = re.compile("<a href='(.+?)'>\n(.+?)\n</a>").findall(item)
                        if urltitulo:
                                urlfilme = urltitulo[0][0]
                                nome = urltitulo[0][1]
                        else:
                                urlfilme = ''
                                nome = ''

                        snpse = re.compile("<div id='imgsinopse'>(.+?)</div>").findall(item)
                        if snpse: sinopse = snpse[0]
                        sinopse = sinopse.replace('&#8216;',"'")
                        sinopse = sinopse.replace('&#8217;',"'")
                        sinopse = sinopse.replace('&#8211;',"-")
                        sinopse = sinopse.replace('&#8220;',"'")
                        sinopse = sinopse.replace('&#8221;',"'")
                        sinopse = sinopse.replace('&#39;',"'")
                        sinopse = sinopse.replace('&amp;','&')
                        
                        gen = re.compile('nero: </span><span style="color: white;">(.+?)</span></b></span>').findall(item)
                        if gen: genero = gen[0]
                        
                        qualidade = re.compile("<strong>Qualidade:</strong>(.+?)</div>").findall(item)
                        if qualidade: qualidade_filme = qualidade[0].replace('&#8211;',"-")
                        else: qualidade_filme = ''

                        audio = re.compile('Audio: </span><span style="color: white;">(.+?)</span></b></span>').findall(item)
                        if audio and qualidade_filme == '': qualidade_filme = audio[0]
                                
                        ano = re.compile('>Ano: </span><span style="color: white;">(.+?)</span></b></span>').findall(item)
                        if ano: ano_filme = ano[0]
                        else: ano_filme = ''
                        
                        thumbnail = re.compile('<a href="(.+?)" imageanchor="1"').findall(item)
                        if thumbnail: thumb = thumbnail[0].replace('s72-c','s320')
                        else: thumb = ''

                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&amp;','&')
                        nome = nome.replace('PT',"")
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        tirar_ano = '(' + str(q_a_q_a) + ')'
                                        nome = nome.replace(tirar_ano,'')
                                        
                        
                        nnnn = re.compile('.+?[(](.+?)[)]').findall(nome)
                        if not nnnn: nnnn = re.compile('.+?[[](.+?)[]]').findall(nome)
                        if not nnnn: nnnn = re.compile('(.+?)[:]').findall(nome)
                        if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                        if nnnn : nome_pesquisa = nnnn[0]
                        else: nome_pesquisa = nome
                        #nome_pesquisa = nome
                        #addLink(imdbcode,'','')
                        if imdbcode != '':
                                try:
                                        fanart,tmdb_id,poster,sin = themoviedb_api_IMDB().fanart_and_id(str(imdbcode),ano_filme)
                                        if sinopse == '': sinopse = sin
                                        if fanart == '': fanart,tmb,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano_filme)
                                        if thumb == '': thumb = poster
                                except:pass
                        else:
                                try:
                                        fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano_filme)
                                        if thumb == '': thumb = poster
                                except:pass
                        
                        
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'

                        try:
                                if 'Temporada' not in nome:                                            
                                        addDir_trailer('[COLOR orange]CMC | [/COLOR][B][COLOR green]' + nome + ' [/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',urlfilme.replace(' ','%20')+'IMDB'+imdbcode+'IMDB',903,thumb.replace(' ','%20'),sinopse,fanart,ano_filme,genero,nome,urlfilme)
                                        num_f_CMC.append(1)
                        except: pass
                except: pass
	else: return #num_f_CMC,num_s_CMC
	return #num_f_CMC,num_s_CMC
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
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
