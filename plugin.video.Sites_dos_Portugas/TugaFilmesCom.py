#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2014 OMaluco
#
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


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,os,threading
import Play,Pesquisar,Mashup,TugaFilmesTV,TopPt,MovieTuga,Armagedom,FilmesAnima
from Funcoes import thetvdb_api, themoviedb_api, themoviedb_api_tv, theomapi_api, themoviedb_api_IMDB, themoviedb_api_IMDB_episodios, themoviedb_api_TMDB
from Funcoes import thetvdb_api_tvdbid, thetvdb_api_episodes, themoviedb_api_search_imdbcode, themoviedb_api_pagina, themoviedb_api_IMDB1, theomapi_api_nome
from Funcoes import addDir, addDir1, addDir2, addLink, addLink1, addDir_teste, addDir_trailer, addDir_episode, addDir_trailer1, addDir_episode1
from Funcoes import get_params,abrir_url
from array import array
from string import capwords

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
perfil = xbmc.translatePath(selfAddon.getAddonInfo('profile'))

filmes = []
itemstotal = []
itemsindividuais = []

progress = xbmcgui.DialogProgress()

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#

def TFC_MenuPrincipal(artfolder):
        addDir('- Procurar','http://www.tuga-filmes.info/search?q=',1,artfolder + 'P1.png','nao','')
	addDir1('[COLOR blue]Filmes:[/COLOR]','url',1003,artfolder + 'TFC1.png',False,'')
	#addDir('[COLOR yellow]- Todos[/COLOR]','http://www.tuga-filmes.info/',72,artfolder + 'FT.png','nao','')
	addDir('[COLOR yellow]- Todos[/COLOR]','http://www.tuga-filmes.com/page/1/',72,artfolder + 'FT.png','nao','')
	#addDir('[COLOR yellow]- Animação[/COLOR]','http://www.tuga-filmes.info/search/label/Anima%C3%A7%C3%A3o?max-results=20',72,artfolder + 'FA.png','nao','')
	addDir('[COLOR yellow]- Animação[/COLOR]','http://www.tuga-filmes.com/category/animacao/',72,artfolder + 'FA.png','nao','')
	addDir('[COLOR yellow]- Categorias[/COLOR]','url',78,artfolder + 'CT.png','nao','')
	addDir('[COLOR yellow]- Por Ano[/COLOR]','http://www.tuga-filmes.info/search/label/-%20Filmes%202013',90,artfolder + 'ANO.png','nao','')
	#addDir('[COLOR yellow]- Destaques[/COLOR]','http://www.tuga-filmes.info/search/label/destaque',72,artfolder + 'DTS.png','nao','')
	addDir('[COLOR yellow]- Destaques[/COLOR]','http://www.tuga-filmes.com/category/destaque/',72,artfolder + 'DTS.png','nao','')
        #addDir('[COLOR yellow]- Top Filmes[/COLOR]','http://www.tuga-filmes.info/',72,artfolder + 'TPF.png','nao','')
	#if selfAddon.getSetting('hide-porno') == "false":                        #79
                #addDir('[B][COLOR red]M+18[/B][/COLOR]','url',86,artfolder + 'TFC1.png','nao','')	

def TFC_Menu_Filmes_Top_10(endereco_top_10):
##        progress = xbmcgui.DialogProgress()
##        i = 1
##        percent = 0
##        message = ''
##        progress.create('Progresso', 'A Pesquisar:')
##        progress.update( percent, "", message, "" )
##        url_top_10 = 'http://www.tuga-filmes.info/'
##        top_10_source = abrir_url(url_top_10)
##        filmes_top_10 = re.compile("<img alt=\'\' border=\'0\' height=\'72\' src=\'.+?\' width=\'72\'/>\n</a>\n</div>\n<div class=\'item-title\'><a href=\'(.+?)\'>.+?</a></div>\n</div>\n<div style=\'clear: both;\'>").findall(top_10_source)
##        num = len(filmes_top_10) + 0.0
##	for endereco_top_10 in filmes_top_10:
##                percent = int( ( i / num ) * 100)
##                message = str(i) + " de " + str(int(num))
##                progress.update( percent, "", message, "" )
##                print str(i) + " de " + str(int(num))
##                if progress.iscanceled():
##                        break
        if endereco_top_10 != '':
                try:
                        html_source = abrir_url(endereco_top_10)
                except: html_source = ''
                items = re.findall("<div id='title1'>(.*?)<div class='postmeta'>", html_source, re.DOTALL)
                #addLink(str(len(items)),'','')
                #return
                if items != []:
                        for item in items:
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
                                urletitulo = re.compile("<a href='(.+?)'>(.+?)</a>").findall(item)
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
                                #if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                                #if not nnnn: nnnn = re.compile('(.+?)[:] ').findall(nome)
                                if nnnn: nome_pesquisa = nnnn[0]
                                else: nome_pesquisa = nome
                                fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano)
                                if thumb == '': thumb = poster

                                if genero == '': genero = '---'
                                if sinopse == '': sinopse = '---'
                                if fanart == '---': fanart = ''
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
                                if qualidade == '': qualidade = '---'
                                try:
                                        if 'ASSISTIR O FILME' in item: addDir_trailer('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR][COLOR red] (' + qualidade + ')[/COLOR]' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',73,thumb.replace('s1600','s320').replace('.gif','.jpg'),sinopse,fanart,ano,qualidade,nome,urletitulo[0][0])
                                except: pass
##                #---------------------------------------------------------------
##                i = i + 1
##                #---------------------------------------------------------------
##	progress.close()

def TFC_Menu_Filmes_Por_Categorias(artfolder):
        url_categorias = 'http://www.tuga-filmes.info/'
        html_categorias_source = abrir_url(url_categorias)
	html_items_categorias = re.findall("<div id=\'nav-cat\'>(.*?)</div>", html_categorias_source, re.DOTALL)
	if not html_items_categorias: html_items_categorias = re.findall("<div id=\'nav-cat\'>(.*?)</div>", html_categorias_source, re.DOTALL)
	if not html_items_categorias: html_items_categorias = re.findall('<li id="menu-item-2238"(.*?)<li id="menu-item-2236"', html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<a href=\'/(.+?)\'>(.+?)</a>").findall(item_categorias)
                if not filmes_por_categoria: filmes_por_categoria = re.compile('<a href="(.+?)">(.+?)</a>').findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        categoria_endereco = endereco_categoria
                        addDir('[COLOR yellow]' + nome_categoria + '[/COLOR]',categoria_endereco,72,artfolder + 'TFC1.png','nao','')

def TFC_Menu_Filmes_Por_Ano(artfolder):
        ano = 2015
        for x in range(46):
                categoria_endereco = 'http://www.tuga-filmes.com/category/filmes-' + str(ano) + '/'
                addDir('[COLOR yellow]' + str(ano) + '[/COLOR]',categoria_endereco,72,artfolder + 'TFC1.png','nao','')
                ano = ano - 1
        


#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#

def cleanTitle(title):
	title = title.replace('&#8211;',"-").replace('&#8230;',"...").replace('&#8217;',"'").replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#39;", "'").replace("&quot;", "\"").replace("&ndash;", "-").replace('"',"").replace("â€™","'")
	title = title.strip()
	return title

def clean(text):
      command={'\r':'','\n':'','\t':'','\xC0':'À','\xC1':'Á','\xC2':'Â','\xC3':'Ã','\xC7':'Ç','\xC8':'È','\xC9':'É','\xCA':'Ê','\xCC':'Ì','\xCD':'Í','\xCE':'Î','\xD2':'Ò','\xD3':'Ó','\xD4':'Ô','\xDA':'Ú','\xDB':'Û','\xE0':'à','\xE1':'á','\xE2':'â','\xE3':'ã','\xE7':'ç','\xE8':'è','\xE9':'é','\xEA':'ê','\xEC':'ì','\xED':'í','\xEE':'î','\xF3':'ó','\xF5':'õ','\xFA':'ú'}
      regex = re.compile("|".join(map(re.escape, command.keys())))
      return regex.sub(lambda mo: command[mo.group(0)], text)

def IFilmes_TFC(ordem,urle,titulo,itemsindividuais):
        #itemsindividuais = []
        try:
		html_source = abrir_url(urle)
	except: html_source = ''
	ano = ''
	thumb = ''
	versao = ''
	nome = cleanTitle(titulo)
	imdb = re.compile('imdb.com/title/(.+?)/').findall(html_source)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = '---'
	pt_en_f = re.compile('<iframe (.+?)</iframe>').findall(html_source)
        if ('---------------------------------------' in html_source or '&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;' in html_source) and len(pt_en_f) > 1: versao = '[COLOR blue] 2 VERSÕES[/COLOR]'
        assist = re.findall(">ASSISTIR.+?", html_source, re.DOTALL)
        if len(assist) > 1: versao = '[COLOR blue] 2 VERSÕES[/COLOR]'
	item=re.findall('<div class="post-heading">(.*?)ASSISTIR O FILME', html_source, re.DOTALL)[0]
	try:sinopse = cleanTitle(re.compile('<b>SINOPSE.+?</b>(.+?)<').findall(html_source)[0].replace('</span>','').replace('<span style="font-size: x-small;">',''))
	except:
                try:sinopse = cleanTitle(re.compile('<b>Sinopse.+?</b>(.+?)<').findall(html_source)[0].replace('</span>','').replace('<span style="font-size: x-small;">',''))
                except:
                        try:sinopse = cleanTitle(re.compile('<b>Sinopse.+?</b>(.+?)\n').findall(html_source)[0].replace('</span>','').replace('<span style="font-size: x-small;">',''))
                        except:sinopse='---'
	try:
                try:qualidade = cleanTitle(re.compile('<b>VERS\xc3\x83O.+?</b>(.+?)<').findall(html_source)[0].replace('</span>','').replace('<span style="font-size: x-small;">',''))
                except:
                        try:qualidade = cleanTitle(re.compile('<b>Vers\xc3\x83.+?</b>(.+?)<').findall(html_source)[0].replace('</span>','').replace('<span style="font-size: x-small;">',''))
                        except:
                                try:qualidade = cleanTitle(re.compile('<b>Versão.+?</b>(.+?)<').findall(html_source)[0].replace('</span>','').replace('<span style="font-size: x-small;">',''))
                                except: qualidade = ''
                #if 'Versão' in html_source: addLink(qualidade+nome,'','','')
                tn = re.compile('\w+')
                tt = tn.findall(nome)
                for tt_tt in tt:
                        tira_nome=tt_tt
                qualidade = re.compile(tira_nome+'(.*)').findall(qualidade.replace('.',' '))[0]	
                a_q = re.compile('\d+')
                qq_aa = a_q.findall(qualidade)
                for q_a_q_a in qq_aa:
                        if len(q_a_q_a) == 4:
                                ano = q_a_q_a
                                break
                        else: ano = ''
                qualidade = qualidade.replace(ano,'').replace('  ','')
        except: qualidade = '---'
        
        if ano == '':
                #addLink('sim'+nome,'','','')
                try:ano = re.compile('<b>Estreia em Portugal.+?</b>.+?[-].+?[-](.+?)</p>').findall(html_source)[0].replace('</span>','').replace('<span style="font-size: x-small;">','').replace(' ','')
                except:
                        try:ano = re.compile('<b>Ano.+?</b>(.+?)<').findall(html_source)[0].replace('</span>','').replace('<span style="font-size: x-small;">','').replace(' ','')
                        except:pass
	
	try:thumb = re.compile('<img.+?src="(.+?)"').findall(item)[0]
	except:thumb=''

	nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
        #if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
        #if not nnnn: nnnn = re.compile('(.+?)[:] ').findall(nome)
        if nnnn: nome_pesquisa = nnnn[0]
        else: nome_pesquisa = nome
        try:fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano)
        except: fanart = '';tmdb_id='';poster=''
        if thumb == '':thumb = poster
	if ano == '': ano = ''

	#addLink(nome+'-'+ano+'-'+qualidade+'-'+sinopse,'',poster,fanart)
	#itemsindividuais.append(str(ordem)+'|'+urle+'|'+titulo+'|'+str(item))
	nome_final = '[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR][COLOR red] (' + qualidade + ')[/COLOR]'+ versao
        itemsindividuais.append(str(ordem)+'NOME|'+str(nome_final)+'|IMDBCODE|'+str(urle)+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb.replace('s1600','s320').replace('.gif','.jpg'))+'|ANO|'+str(ano.replace('(','').replace(')',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(qualidade)+'|ONOME|'+str(nome_pesquisa)+'|SINOPSE|'+str(sinopse)+'|END|\n')


def TFC_encontrar_fontes_filmes(url):

        itemstotal = []
        itemsindividuais = []

        if name != '[COLOR yellow]- Top Filmes[/COLOR]':
                try: xbmcgui.Dialog().notification('A Procurar Filmes.', 'Por favor aguarde...', artfolder + 'TFC1.png', 3000, sound=False)
                except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % ('A Procurar Filmes.', 'Por favor aguarde...', artfolder + 'TFC1.png'))

        if name == '[COLOR yellow]- Top Filmes[/COLOR]':
                try: xbmcgui.Dialog().notification('A Procurar.', 'Por favor aguarde...', artfolder + 'TFC1.png', 3000, sound=False)
                except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % ('A Procurar.', 'Por favor aguarde...', artfolder + 'TFC1.png'))
        
        #addLink(url,'','','')
        try:
		html_source = abrir_url(url)
	except: html_source = ''
	if name != '[COLOR yellow]- Top Filmes[/COLOR]':
                items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
                if not items: items = re.findall("<article(.*?)</article>", html_source, re.DOTALL)
        if name == '[COLOR yellow]- Top Filmes[/COLOR]':
                items = re.compile("<img alt=\'\' border=\'0\' height=\'72\' src=\'.+?\' width=\'72\'/>\n</a>\n</div>\n<div class=\'item-title\'><a href=\'(.+?)\'>.+?</a></div>\n</div>\n<div style=\'clear: both;\'>").findall(html_source)

        for item in items:
                urletitulo = re.compile('<a href="(.+?)" class="thumbnail-wrapper" title="(.+?)">').findall(item)
                itemstotal.append(urletitulo[0][0]+'|'+urletitulo[0][1])

        threads = []
        i = 0
        for it in itemstotal:
                dads = re.compile('(.+?)[|](.*)').findall(it)
                i = i + 1
                a = str(i)
                if i < 10: a = '0'+a
                Filmes_TFC = threading.Thread(name='Filmes_TFC'+str(i), target=IFilmes_TFC , args=(str(a),dads[0][0],dads[0][1],itemsindividuais,))
                threads.append(Filmes_TFC)
        [i.start() for i in threads]
        [i.join() for i in threads]

        itemsindividuais.sort()
        #addLink(str(len(itemsindividuais))+str(len(threads)),'','','')
##        threads = []
##        i = 0
##        for itemi in itemsindividuais:
##                if name != '[COLOR yellow]- Top Filmes[/COLOR]':
##                        item=re.compile('.+?[|](.+?)[|](.+?)[|](.*)').findall(itemi)
##                        #addLink(item[0][0],'','','')
##                        #addLink(item[0][1],'','','')
##                        i = i + 1
##                        a = str(i)
##                        if i < 10: a = '0'+a
##                        Filmes_TFC = threading.Thread(name='Filmes_TFC'+str(i), target=Fontes_Filmes_TFC , args=(item[0][0],item[0][1],'FILME'+str(a)+'FILME'+item[0][2],))
##                if name == '[COLOR yellow]- Top Filmes[/COLOR]':
##                        Filmes_TFC = threading.Thread(name='Filmes_TFC'+str(i), target=TFC_Menu_Filmes_Top_10 , args=(item,))
##                threads.append(Filmes_TFC)
##
##        [i.start() for i in threads]
##
##        [i.join() for i in threads]
        
        if name != '[COLOR yellow]- Top Filmes[/COLOR]':
                _sites_ = ['filmesTFC.txt']
                folder = perfil
                num_filmes = 0
                num_filmes = len(threads)
                for site in _sites_:
                        _filmes_ = []
##                        Filmes_Fi = open(folder + site, 'r')
##                        read_Filmes_File = ''
##                        for line in Filmes_Fi:
##                                read_Filmes_File = read_Filmes_File + line
##                                if line!='':_filmes_.append(line)
                        _filmes_=itemsindividuais
##                        addLink(str(len(_filmes_)),'','','')
                        
                        for x in range(len(_filmes_)):
        ##                        _nfil = re.compile('(.+?)NOME[|]').findall(_filmes_[x])
        ##                        if _nfil: nfilme = _nfil[0]
        ##                        else: nfilme = '---'
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
                                if 'tuga-filmes.info' in imdbcode or 'tuga-filmes.com' in imdbcode: num_mode = 73
                                if nome != '---':
                                        #num_filmes = num_filmes + 1
                                        addDir_trailer1(nome,imdbcode,num_mode,thumb,sinopse,fanart,ano_filme,genero,O_Nome,urltrailer,'Movies',num_filmes)
                                xbmc.sleep(20)
##                        Filmes_Fi.close()

                proxima = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
                if not proxima: proxima = re.compile('<a class="nextpostslink" rel="next" href="(.+?)">').findall(html_source)
                try:
                        addDir("[B]Página Seguinte >>[/B]",proxima[0].replace('&amp;','&'),72,artfolder + 'PAGS1.png','','')
                except: pass
                
def Fontes_Filmes_TFC(urlen,titulo,item):        

        folder = perfil
        Filmes_File = open(folder + 'filmesTFC.txt', 'w')
        
        if item != '':
                try:
                        FILMEN = re.compile('FILME(.+?)FILME').findall(item)
                        FILMEN = FILMEN[0]
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
			if not urletitulo:
                                nome = titulo
			qualidade_ano = re.compile('<b>VERS\xc3\x83O.+?</b><span style="font-size: x-small;">(.+?)<').findall(item)
			snpse = re.compile('<b>SINOPSE:.+?</b><span style="font-size: x-small;">(.+?)<').findall(item)
			if not snpse: snpse = re.compile('<b>SINOPSE:.+?</b><span style="font-size: x-small;">(.+?)</span></p>').findall(item)
			if snpse: sinopse = snpse[0]
			else: sinopse = ''
			thumbnail = re.compile('<img alt="" border="0" src="(.+?)"').findall(item)
			if not thumbnail: thumbnail = re.compile('src="(.+?)"').findall(item)
			if thumbnail: thumb = thumbnail[0]
			#print urletitulo,thumbnail
			ano = 'Ano'
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
                                        quali_titi = nome.replace('á','a')
                                        quali_titi = nome.replace('é','e')
                                        quali_titi = nome.replace('í','i')
                                        quali_titi = nome.replace('ó','o')
                                        quali_titi = nome.replace('ú','u')
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
                        #if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                        #if not nnnn: nnnn = re.compile('(.+?)[:] ').findall(nome)
                        if nnnn: nome_pesquisa = nnnn[0]
                        else: nome_pesquisa = nome
                        fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano)
                        if thumb == '': thumb = poster

                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        if qualidade == '': qualidade = '---'
			try:
				if 'ASSISTIR O FILME' not in item:
                                        addLink(FILMEN,'',thumb,fanart)
                                        addLink(urlen,'','','')
                                        addLink(nome,'','','')
                                        addLink(ano,'','','')
                                        addLink(qualidade,'','','')
                                        addLink(thumb,'','','')
                                        addLink(versao,'','','')
                                        addLink(fanart,'','','')
                                        addLink(sinopse,'','','')
                                        addLink(genero,'','','')
                                        addLink('------------------','','','')
                                        nome_final = '[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR][COLOR red] (' + qualidade + ')[/COLOR]' + versao
                                        filmes.append(FILMEN+'NOME|'+str(nome_final)+'|IMDBCODE|'+str(urlen)+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb.replace('s1600','s320').replace('.gif','.jpg'))+'|ANO|'+str(ano.replace('(','').replace(')',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(qualidade)+'|ONOME|'+str(nome_pesquisa)+'|SINOPSE|'+str(sinopse)+'|END|\n')
			except: pass
		except: pass
	else: pass
	filmes.sort()
	for x in range(len(filmes)):
                Filmes_File.write(str(filmes[x]))
	Filmes_File.close()

	

#----------------------------------------------------------------------------------------------------------------------------------------------#
	
def TFC_resolve_not_videomega_filmesll(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart):
        if 'videomega' in url: vidv = url
        url = url + '///' + name
        if "videomega" in url:
		try:
                        if 'hashkey' in url:
                                try:
                                        urlvideomega = abrir_url(vidv)
                                except: urlvideomega = ''
                                if urlvideomega != '':
                                        urlvidlink = re.compile('ref="(.+?)"').findall(urlvideomega)
                                        if urlvidlink: url = 'http://videomega.tv/iframe.php?ref=' + urlvidlink[0] + '///' + name
                        fonte_id = '(Videomega)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,30,iconimage,'',fanart)
		except: pass
        if "vidto.me" in url:
		try:
                        print url
                        fonte_id = '(Vidto.me)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,70,iconimage,'',fanart)
		except: pass
        if "dropvideo" in url:
		try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        fonte_id = '(DropVideo)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B]',url,70,iconimage,'',fanart)
		except:pass
	if "streamin.to" in url:
                try:
			print url
			fonte_id = '(Streamin)'
			#addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B]',url,70,iconimage,'',fanart)
                except:pass                        
        if "putlocker" in url:
                try:
                        print url
                        fonte_id = '(Putlocker)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Putlocker)[/COLOR][/B]',url,70,iconimage,'',fanart)
    		except:pass
    	if "nowvideo" in url:
                try:
                        print url
                        fonte_id = '(Nowvideo)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,70,iconimage,'',fanart)
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(VideoWood)'
                        #addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoWood)[/COLOR][/B]',url,70,iconimage,'',fanart)
    		except:pass
    	if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url:# and 'iiiiiiiiii' in url:
                Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',iconimage,'',fanart)
    	return

def TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart):
        if 'videomega' in url: vidv = url
        url = url + '///' + name
        #addLink(urltrailer,'','','')
        if "videomega" in url:
		try:
                        if 'hashkey' in url:
                                try:
                                        urlvideomega = abrir_url(vidv)
                                except: urlvideomega = ''
                                if urlvideomega != '':
                                        urlvidlink = re.compile('ref="(.+?)"').findall(urlvideomega)
                                        if urlvidlink: url = 'http://videomega.tv/iframe.php?ref=' + urlvidlink[0] + '///' + name
                        fonte_id = '(Videomega)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',urltrailer + '///' + name,30,iconimage,'',fanart)
		except: pass
        if "vidto.me" in url:
		try:
                        print url
                        fonte_id = '(Vidto.me)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,70,iconimage,'',fanart)
		except: pass
        if "dropvideo" in url:
		try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        fonte_id = '(DropVideo)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B]',url,70,iconimage,'',fanart)
		except:pass
	if "streamin.to" in url:
                try:
			print url
			fonte_id = '(Streamin)'
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B]',url,70,iconimage,'',fanart)
                except:pass                        
        if "putlocker" in url:
                try:
                        print url
                        fonte_id = '(Putlocker)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Putlocker)[/COLOR][/B]',url,70,iconimage,'',fanart)
    		except:pass
    	if "nowvideo" in url:
                try:
                        print url
                        fonte_id = '(Nowvideo)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,70,iconimage,'',fanart)
    		except:pass
    	if "videowood" in url:
                try:
                        if '/video/' in url: url = url.replace('/video/','/embed/')
                        print url
                        fonte_id = '(VideoWood)'
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](VideoWood)[/COLOR][/B]',url,70,iconimage,'',fanart)
    		except:pass
##    	if 'vk.com' not in url and 'video.mail.ru' not in url and 'videoapi.my.mail' not in url and 'vidzi.tv' not in url and 'playfreehd' not in url  and 'thevideo.me' not in url and 'vidto.me' not in url:# and 'iiiiiiiiii' in url:
##                Play.PLAY_movie_url(url,'[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow]'+fonte_id+'[/COLOR][/B]',iconimage,'',fanart)
    	return
#----------------------------------------------------------------------------------------------------------------------------------------------#

def TFC_encontrar_videos_filmes(name,url,mvoutv):
        if mvoutv == 'MoviesTFC':
                try: xbmcgui.Dialog().notification('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png', 3000, sound=False)
                except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % ('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png'))
        else:
                try: xbmcgui.Dialog().notification('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png', 10000, sound=False)
                except: xbmc.executebuiltin("Notification(%s,%s, 10000, %s)" % ('A Procurar.', 'Por favor aguarde...', artfolder + 'SDPI.png'))
        site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].com'
##        message = 'Por favor aguarde.'
##        percent = 0
##        progress.create('Progresso', 'A Procurar...')
##        progress.update(percent, 'A Procurar em '+site, message, "")
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]
        if 'TFC' not in name: name = '[COLOR orange]TFC | [/COLOR]' + name
        nomeescolha = name
        conta_os_items = 0
        conta_os_items = conta_os_items + 1
        n1 = ''
        n2 = ''
        ################################################
        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(nomeescolha)
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
##        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(nomeescolha)
##        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
##        nn = nomeescolha.replace('[B][COLOR green]','--').replace('[/COLOR][/B]','--').replace('[COLOR orange]','').replace('TFC | ','')
##        n = re.compile('--(.+?)--').findall(nn)
##        addDir1('[COLOR blue]PROCUROU POR: [/COLOR]'+n[0],'url',1004,iconimage,False,fanart)
        ############################################

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
        
        conta_id_video = 0
	addDir1(name,'url',1003,iconimage,False,fanart)
        try:
                fonte = abrir_url(url)
        except: fonte = ''
        items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", fonte, re.DOTALL)
        if not items: items = re.findall("<div id='postagem'>(.*?)<div class='postmeta'>", fonte, re.DOTALL)

        assist = re.findall(">ASSISTIR.+?", fonte, re.DOTALL)
        fontes = re.findall("Ver Aqui.+?", fonte, re.DOTALL)
        numero_de_fontes = len(fontes)
       # addLink(str(len(assist)),'','','')
        #fonte = 
        #return
	if fonte:
                if len(assist) > 1:
                        #addDir1('1','url',1003,artfolder,False,'')
                        #return
                        assistir_fontes = re.findall('>ASSISTIR(.*?)------------------------------', fonte, re.DOTALL)
                        if not assistir_fontes: assistir_fontes = re.findall('>ASSISTIR(.*?)&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;', fonte, re.DOTALL)
                        #addLink(str(len(assistir_fontes)),'','','')
                        #return
                        if assistir_fontes:
                                for ass_fon in assistir_fontes:
                                        match = re.compile('<iframe .+? src="(.+?)"').findall(ass_fon)
                                        assis = re.compile('ONLINE(.+?)</span>').findall(ass_fon)
                                        if not assis: assis = re.compile('ONLINE(.+?)</b><br').findall(ass_fon)
                                        conta_video = len(match)
                                        if assis:
                                                if 'LEGENDADO' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,fanart)
                                                if 'PT/PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                                elif 'PT-PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        match = re.compile('<a href="(.+?)" target=".+?">Ver Aqui</a>').findall(ass_fon)
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        matchi = re.compile('<script type="text/javascript" src="(.+?)"></script><script').findall(ass_fon)
                                        if matchi:
                                                for url in matchi:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        conta_os_items = conta_os_items + 1
                                assistir_fontes = re.findall("------------------------------<br />(.*?)='postmeta'>", fonte, re.DOTALL)
                                if not assistir_fontes: assistir_fontes = re.findall('&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;(.*?)<div class="views">', fonte, re.DOTALL)
                                if not assistir_fontes: assistir_fontes = re.findall('&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;(.*?)<div class="clear">', fonte, re.DOTALL)
                                #assistir_fontes = re.findall(">ASSISTIR(.*?)<div class", assistir_fontes[0], re.DOTALL)
                                conta_id_video = 0
                                for ass_fon in assistir_fontes:
                                        match = re.compile('<iframe .+? src="(.+?)"').findall(ass_fon)
                                        assis = re.compile('ONLINE(.+?)</span>').findall(ass_fon)
                                        if not assis: assis = re.compile('ONLINE(.+?)</b><br').findall(ass_fon)
                                        conta_video = len(match)
                                        if assis:
                                                if 'LEGENDADO' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,fanart)
                                                if 'PT/PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                                elif 'PT-PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        match = re.compile('<a href="(.+?)" target=".+?">Ver Aqui</a>').findall(ass_fon)
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        matchi = re.compile('<script type="text/javascript" src="(.+?)"></script><script').findall(ass_fon)
                                        if matchi:
                                                for url in matchi:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        conta_os_items = conta_os_items + 1
                        else:
                                assistir_fontes = re.findall('>ASSISTIR(.*?)</iframe>', fonte, re.DOTALL)
                                if not assistir_fontes: assistir_fontes = re.findall('>ASSISTIR(.*?)<div class="views">', fonte, re.DOTALL)
                                if not assistir_fontes: assistir_fontes = re.findall('>ASSISTIR(.*?)<div class="clear">', fonte, re.DOTALL)
                                conta_id_video = 0
                                for ass_fon in assistir_fontes:
                                        match = re.compile('<iframe .+? src="(.+?)"').findall(ass_fon)
                                        assis = re.compile('ONLINE(.+?)</span>').findall(ass_fon)
                                        if not assis: assis = re.compile('ONLINE(.+?)</b><br').findall(ass_fon)
                                        conta_video = len(match)
                                        if assis:
                                                if 'LEGENDADO' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,fanart)
                                                if 'PT/PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                                elif 'PT-PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        match = re.compile('<a href="(.+?)" target=".+?">Ver Aqui</a>').findall(ass_fon)
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        matchi = re.compile('<script type="text/javascript" src="(.+?)"></script><script').findall(ass_fon)
                                        if matchi:
                                                for url in matchi:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        conta_os_items = conta_os_items + 1
                else:
                        assistir_fontes = re.findall('>ASSISTIR(.*?)<div class="views">', fonte, re.DOTALL)
                        if not assistir_fontes: assistir_fontes = re.findall('>ASSISTIR(.*?)<div class="clear">', fonte, re.DOTALL)
                        match = re.compile('www.videowood(.+?)" target="_blank">.+?[(]Online').findall(fonte)
                        #if not match: match = re.compile('www.videowood(.+?)" target="_blank">.+?[(]Online').findall(fonte)
                        if not match: match = re.compile('<a href="(.+?)" target="_blank">.+?[(]Online').findall(fonte)
                        for url in match:
                                url = 'http://www.videowood'+url
                                id_video = ''
                                conta_id_video = conta_id_video + 1
                                TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                conta_os_items = conta_os_items + 1
                        #return
                        match = re.compile('<iframe .+? src="(.+?)"').findall(fonte)
                        if match:
                                
                                conta_video = len(match)
                                for url in match:
                                        id_video = ''
                                        conta_id_video = conta_id_video + 1
                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        conta_os_items = conta_os_items + 1
                        else:
                                
                                match = re.compile("<script type='text/javascript' src='(.+?)'></script>").findall(assistir_fontes[0])
                                if not match: match = re.compile('<script type="text/javascript" src="(.+?)"></script>').findall(assistir_fontes[0])
                                conta_video = len(match)
                                #addLink(str(conta_video),'','','')
                                for url in match:
                                        if 'hashkey' in url:
                                                id_video = ''
                                                conta_id_video = conta_id_video + 1
                                                TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                                conta_os_items = conta_os_items + 1
                        if numero_de_fontes > 0:
                                conta_video = 0
                                match = re.compile('<a href="(.+?)" target=".+?">Ver Aqui</a>').findall(fonte)
                                url = match[0]
                                if url != '':
                                        try:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                                        conta_os_items = conta_os_items + 1
                                        except:pass
##        nnn = re.compile('[[]B[]][[]COLOR green[]](.+?)[[]/COLOR[]][[]/B[]]').findall(nomeescolha)
##        nomeescolha = '[B][COLOR green]'+nnn[0]+'[/COLOR][/B]'
##        nn = nomeescolha.replace('[B][COLOR green]','--').replace('[/COLOR][/B]','--').replace('[COLOR orange]','').replace('TFC | ','')
##        n = re.compile('--(.+?)--').findall(nn)
        url = 'IMDB'+imdbcode+'IMDB'
        #addLink(url+'-'+str(n[0]),'','')
        if mvoutv != 'MoviesTFC': FilmesAnima.FILMES_ANIMACAO_pesquisar(str(n1),'TFC',url)


#----------------------------------------------------------------------------------------------------------------------------------------------#

def TFC_links(name,url,iconimage,fanart):
        iconimage = iconimage
        imdb = re.compile('.+?IMDB(.+?)IMDB').findall(url)
        if imdb: imdbcode = imdb[0]
        else: imdbcode = ''
        urlimdb = re.compile('(.+?)IMDB.+?IMDB').findall(url)
        if not urlimdb: url = url.replace('IMDBIMDB','')
        else: url = urlimdb[0]
                
        nomeescolha = name
        conta_os_items = 0
        conta_os_items = conta_os_items + 1
        conta_id_video = 0
        try:
                fonte = abrir_url(url)
        except: fonte = ''
        items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", fonte, re.DOTALL)
        if not items: items = re.findall("<div id='postagem'>(.*?)<div class='postmeta'>", fonte, re.DOTALL)
##	if items != []:
##                imdb = re.compile('imdb.com/title/(.+?)/').findall(items[0])
##                if imdb: imdbcode = imdb[0]
##                else: imdbcode = ''
        assist = re.findall(">ASSISTIR.+?", fonte, re.DOTALL)
        fontes = re.findall("Ver Aqui.+?", fonte, re.DOTALL)
        numero_de_fontes = len(fontes)
        #addLink(str(len(assist)),'','','')
	if fonte:
                if len(assist) > 1:
                        assistir_fontes = re.findall('>ASSISTIR(.*?)------------------------------', fonte, re.DOTALL)
                        if not assistir_fontes: assistir_fontes = re.findall('>ASSISTIR(.*?)&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;', fonte, re.DOTALL)
                        if assistir_fontes:
                                for ass_fon in assistir_fontes:
                                        match = re.compile('<iframe .+? src="(.+?)"').findall(ass_fon)
                                        assis = re.compile('ONLINE(.+?)</span>').findall(ass_fon)
                                        if not assis: assis = re.compile('ONLINE(.+?)</b><br').findall(ass_fon)
                                        conta_video = len(match)
                                        if assis:
                                                if 'LEGENDADO' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,fanart)
                                                if 'PT/PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                                elif 'PT-PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        match = re.compile('<a href="(.+?)" target=".+?">Ver Aqui</a>').findall(ass_fon)
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        conta_os_items = conta_os_items + 1
                                assistir_fontes = re.findall("------------------------------<br />(.*?)='postmeta'>", fonte, re.DOTALL)
                                if not assistir_fontes: assistir_fontes = re.findall('&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;(.*?)<div class="views">', fonte, re.DOTALL)
                                if not assistir_fontes: assistir_fontes = re.findall('&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;(.*?)<div class="clear">', fonte, re.DOTALL)
                                #assistir_fontes = re.findall(">ASSISTIR(.*?)<div class", assistir_fontes[0], re.DOTALL)
                                conta_id_video = 0
                                for ass_fon in assistir_fontes:
                                        match = re.compile('<iframe .+? src="(.+?)"').findall(ass_fon)
                                        assis = re.compile('ONLINE(.+?)</span>').findall(ass_fon)
                                        if not assis: assis = re.compile('ONLINE(.+?)</b><br').findall(ass_fon)
                                        conta_video = len(match)
                                        if assis:
                                                if 'LEGENDADO' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,fanart)
                                                if 'PT/PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                                elif 'PT-PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        match = re.compile('<a href="(.+?)" target=".+?">Ver Aqui</a>').findall(ass_fon)
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        conta_os_items = conta_os_items + 1
                        else:
                                assistir_fontes = re.findall('>ASSISTIR(.*?)</iframe>', fonte, re.DOTALL)
                                if not assistir_fontes: assistir_fontes = re.findall('>ASSISTIR(.*?)<div class="views">', fonte, re.DOTALL)
                                if not assistir_fontes: assistir_fontes = re.findall('>ASSISTIR(.*?)<div class="clear">', fonte, re.DOTALL)
                                conta_id_video = 0
                                for ass_fon in assistir_fontes:
                                        match = re.compile('<iframe .+? src="(.+?)"').findall(ass_fon)
                                        assis = re.compile('ONLINE(.+?)</span>').findall(ass_fon)
                                        if not assis: assis = re.compile('ONLINE(.+?)</b><br').findall(ass_fon)
                                        conta_video = len(match)
                                        if assis:
                                                if 'LEGENDADO' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,fanart)
                                                if 'PT/PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                                elif 'PT-PT' in assis[0]:
                                                        conta_os_items = conta_os_items + 1
                                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,fanart)
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        match = re.compile('<a href="(.+?)" target=".+?">Ver Aqui</a>').findall(ass_fon)
                                        if match:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        conta_os_items = conta_os_items + 1
                else:
                        assistir_fontes = re.findall('>ASSISTIR(.*?)<div class="views">', fonte, re.DOTALL)
                        if not assistir_fontes: assistir_fontes = re.findall('>ASSISTIR(.*?)<div class="clear">', fonte, re.DOTALL)
                        match = re.compile('www.videowood(.+?)" target="_blank">.+?[(]Online').findall(fonte)
                        if not match: match = re.compile('<a href="(.+?)" target="_blank">.+?[(]Online').findall(fonte)
                        for url in match:
                                url = 'http://www.videowood'+url                                
                                id_video = ''
                                conta_id_video = conta_id_video + 1
                                TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                conta_os_items = conta_os_items + 1
                        match = re.compile('<iframe .+? src="(.+?)"').findall(fonte)
                        if match:
                                conta_video = len(match)
                                for url in match:
                                        id_video = ''
                                        conta_id_video = conta_id_video + 1
                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                        conta_os_items = conta_os_items + 1
                        else:
                                match = re.compile("<script type='text/javascript' src='(.+?)'></script>").findall(assistir_fontes[0])
                                if not match: match = re.compile('<script type="text/javascript" src="(.+?)"></script>').findall(assistir_fontes[0])
                                conta_video = len(match)
                                for url in match:
                                        if 'hashkey' in url:
                                                id_video = ''
                                                conta_id_video = conta_id_video + 1
                                                TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                                conta_os_items = conta_os_items + 1
                        if numero_de_fontes > 0:
                                conta_video = 0
                                match = re.compile('<a href="(.+?)" target=".+?">Ver Aqui</a>').findall(fonte)
                                url = match[0]
                                if url != '':
                                        try:
                                                for url in match:
                                                        id_video = ''
                                                        conta_id_video = conta_id_video + 1
                                                        TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,conta_os_items,iconimage,fanart)
                                                        conta_os_items = conta_os_items + 1
                                        except:pass



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
