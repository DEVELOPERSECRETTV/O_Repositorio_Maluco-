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



import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,time,os


addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

 
mensagemok = xbmcgui.Dialog().ok
	
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def pesquisar():
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
                        if len(q_a_q_a) > 2 or q_a_q_a == '1' or q_a_q_a == '2' or q_a_q_a == '3':
                        #if len(q_a_q_a) > 2:
                                if conta == 0:
                                        search = q_a_q_a
                                        conta = 1
                                if conta == 1:
                                        search = search + '+' + q_a_q_a
		encode=urllib.quote(search)
		mensagemprogresso = xbmcgui.DialogProgress()
                mensagemprogresso.create('Progresso', 'A Pesquisar','Por favor aguarde...')
                mensagemprogresso.update(0)
		url_pesquisa = 'http://www.tuga-filmes.us/search?q=' + str(encode)
		encontrar_fontes_pesquisa_TFV(url_pesquisa,pesquisou)
		mensagemprogresso.update(25)
		url_pesquisa = 'http://www.tuga-filmes.info/search?q=' + str(encode)
		encontrar_fontes_filmes_TFC(url_pesquisa)
		mensagemprogresso.update(50)
		url_pesquisa = 'http://www.movie-tuga.blogspot.pt/search?q=' + str(encode)
		encontrar_fontes_pesquisa_MVT(url_pesquisa)
		mensagemprogresso.update(75)
		url_pesquisa = 'http://toppt.net/?s=' + str(encode)
		encontrar_fontes_filmes_TPT(url_pesquisa)
		if selfAddon.getSetting('movies-view') == "0":
                        addDir1('','','',artfolder + 'banner.png',False,'')		
                        addDir('[COLOR yellow]Nova Pesquisa[/COLOR]','url',1,artfolder + 'banner.png','nao','')
                        addDir('[COLOR yellow]Menu Principal[/COLOR]','','',artfolder + 'banner.png','nao','')
                mensagemprogresso.update(100)


#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def encontrar_fontes_pesquisa_TFV(url,pesquisou):
        pesquisado = pesquisou.replace('%20',' ')
        if selfAddon.getSetting('movies-view') == "0":
                addDir1('[B][COLOR blue]Pesquisou : [/COLOR]( ' + pesquisado + ' )[/B]','','',artfolder + 'banner.png',False,'')
                addDir1('','','',artfolder + 'banner.png',False,'')
                addDir1('[B][COLOR yellow]----- [/COLOR][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv[B][COLOR yellow] -----[/COLOR][/B]','','','',False,'')
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
                num_f = 0
		print len(items)
		for item in items:
                        try:
                                audio_filme = ''
                                urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)
                                if "Temporada" in urletitulo[0][1]:
                                        urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)
                                        num_mode = 42
                                else:
                                        urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)
                                        num_mode = 33
                                qualidade = re.compile("<b>Qualidade</b>: (.+?)<br />").findall(item)
                                ano = re.compile("<b>Ano</b>: (.+?)<br />").findall(item)
                                audio = re.compile("<b>.+?udio</b>(.+?)<br />").findall(item)
                                if audio != []:
                                        if 'Portug' in audio[0]:
                                                audio_filme = ': PT-PT'
                                        else:
                                                audio_filme = audio[0]
                                thumbnail = re.compile('src="(.+?)"').findall(item)
                                print urletitulo,thumbnail
                                nome = urletitulo[0][1]
                                nome = nome.replace('&#8217;',"'")
                                nome = nome.replace('&#8211;',"-")
                                nome = nome.replace('(PT-PT)',"")
                                nome = nome.replace('(PT/PT)',"")
                                nome = nome.replace('[PT-PT]',"")
                                nome = nome.replace('[PT/PT]',"")
                                if ano:
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
                                        addDir('[B][COLOR green]- ' + nome + '[/COLOR][/B][COLOR yellow] (' + ano[0] + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR]',urletitulo[0][0],num_mode,thumbnail[0].replace('s72-c','s320'),'','')				
                                        num_f = num_f + 1
                                except: pass
                        except: pass
        else: num_f = 0
        if num_f == 0:
                if selfAddon.getSetting('movies-view') == "0": addDir1('- No Match Found -','','','',False,'')
	return

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def encontrar_fontes_filmes_TFC(url):
        if selfAddon.getSetting('movies-view') == "0":
                addDir1('[B][COLOR yellow]----- [/COLOR][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].com[B][COLOR yellow] -----[/COLOR][/B]','','','',False,'')
        pt_en = 0
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
	if items != []:
                num_f = 0
		print len(items)
		for item in items:
                        try:
                                versao = ''
                                pt_en_f = re.compile('<iframe (.+?)</iframe>').findall(item)
                                if '---------------------------------------' in item and len(pt_en_f) > 1: versao = '[COLOR blue] 2 VERSÕES[/COLOR]'
                                urletitulo = re.compile("<a href=\'(.+?)\' title=\'(.+?)\'>").findall(item)
                                qualidade_ano = re.compile('<b>VERS\xc3\x83O:.+?</b><span style="font-size: x-small;">(.+?)<').findall(item)
                                thumbnail = re.compile('<img alt="" border="0" src="(.+?)"').findall(item)
                                print urletitulo,thumbnail
                                ano = 'Ano'
                                qualidade = ''
                                e_qua = 'nao'
                                calid = ''
                                if qualidade_ano != []:
                                        for q_a in qualidade_ano:
                                                #addDir1(q_a,'','','',False,'')
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
                                                ano = 'Ano'
                                                #qualidade = q_a
                                        if qualidade == 'PT PT':
                                                qualidade = 'PT-PT'
                                        if qualidade == '':
                                                quali_titi = urletitulo[0][1].replace('á','a')
                                                quali_titi = urletitulo[0][1].replace('é','e')
                                                quali_titi = urletitulo[0][1].replace('í','i')
                                                quali_titi = urletitulo[0][1].replace('ó','o')
                                                quali_titi = urletitulo[0][1].replace('ú','u')
                                                #addDir1(quali_titi,'','','',False,'')
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
                                try:
                                        addDir('[B][COLOR green]- ' + urletitulo[0][1].replace('&#39;',"'") + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR][COLOR red] (' + qualidade + ')[/COLOR]' + versao,urletitulo[0][0],73,thumbnail[0].replace('s1600','s320').replace('.gif','.jpg'),'','')
                                        num_f = num_f + 1
                                except: pass
                        except: pass
        else: num_f = 0
	if num_f == 0:
                if selfAddon.getSetting('movies-view') == "0": addDir1('- No Match Found -','','','',False,'')
	return

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

def encontrar_fontes_pesquisa_MVT(url):
        if selfAddon.getSetting('movies-view') == "0":
                addDir1('[B][COLOR yellow]----- [/COLOR][COLOR green]MOVIE[/COLOR][COLOR yellow]-[/COLOR][COLOR red]TUGA[/COLOR][/B][B][COLOR yellow] -----[/COLOR][/B]','','','',False,'')
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
	if items != []:
                num_f = 0
		print len(items)
		for item in items:
                        try:
                                url = re.compile('<div class="btns"><a href="(.+?)" target="Player">').findall(item)
                                if 'http' not in url[0]:
                                        urllink = 'http:' + url[0]
                                else: urllink = url[0] 
                                titulo = re.compile("<strong>T\xc3\xadtulo original:</strong>(.+?)</div>").findall(item)
                                if 'Qualidade:' in item:
                                        qualidade = re.compile("<strong>Qualidade:</strong>(.+?)</div>").findall(item)
                                        qualidade_filme = qualidade[0].replace('&#8211;',"-")
                                else:
                                        qualidade_filme = ''
                                ano = re.compile('<strong>Lan\xc3\xa7amento:</strong>(.+?)</div>').findall(item)
                                thumb = re.compile('src="(.+?)"').findall(item)
                                if 'http' not in thumb[0]:
                                        thumbnail = 'http:' + thumb[0]
                                else: thumbnail = thumb[0]
                                print url,thumbnail
                                titulo[0] = titulo[0].replace('&#8217;',"'")
                                titulo[0] = titulo[0].replace('&#8211;',"-")
                                try:
                                        addDir('[B][COLOR green]- ' + titulo[0] + ' [/COLOR][/B][COLOR yellow](' + ano[0] + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',urllink,103,thumbnail.replace('s72-c','s320'),'','')
                                        num_f = num_f + 1
                                except: pass
                        except: pass
        else: num_f = 0
	if num_f == 0:
                if selfAddon.getSetting('movies-view') == "0": addDir1('- No Match Found -','','','',False,'')
	return

#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#


def encontrar_fontes_filmes_TPT(url):
        if selfAddon.getSetting('movies-view') == "0":
                addDir1('[B][COLOR yellow]----- [/COLOR][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][COLOR yellow] -----[/COLOR][/B]','','','',False,'')
	try:
		html_source = abrir_url(url)
	except: html_source = ''
	if '<div class="postmeta-primary">' in html_source: items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	else:
                if selfAddon.getSetting('movies-view') == "0": addDir1('- No Match Found -','','','',False,'')
                return
	if items != []:
                num_f = 0
		print len(items)
		for item in items:
                        try:
                                audio_filme = ''
                                urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(item)
                                if 'title=' in urletitulo[0][0]: urletitulo = re.compile('<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>').findall(item)
                                url = urletitulo[0][0]
                                try:
                                        html_source = abrir_url(url)
                                except: html_source = ''
                                #addDir1(url,'','','',False,'')
                                items = re.findall('<div class="post-(.*?)<span id="more-', html_source, re.DOTALL)
                                if items != []:
                                        print len(items)
                                        for item in items:
                                                audio_filme = ''
                                                titulo = re.compile('<h2 class="title">(.+?)</h2>').findall(item)
                                                #urlpesq = re.compile('<span class="entry-date"><a href="(.+?)" rel="bookmark">').findall(item)
                                                qualidade = re.compile("<b>QUALIDADE:.+?/b>(.+?)<br/>").findall(item)
                                                if not qualidade: qualidade = re.compile("<b>VERSÃO:.+?</b>(.+?)<br/>").findall(item)
                                                ano = re.compile("<b>ANO:.+?/b>(.+?)<br/>").findall(item)
                                                audio = re.compile("<b>AUDIO:.+?/b>(.+?)<br/>").findall(item)
                                                if qualidade == [] or ano == [] or audio == []:
                                                        qualidade = re.compile("<b>QUALIDADE:.+?/b>(.+?)<b").findall(item)
                                                        ano = re.compile("<b>ANO:.+?/b>(.+?)<b").findall(item)
                                                        audio = re.compile("<b>AUDIO:.+?/b>(.+?)<b").findall(item)    
                                                thumbnail = re.compile('src="(.+?)"').findall(item)
                                                print urletitulo,thumbnail
                                                nome = titulo[0]
                                                nome = nome.replace('&#8217;',"'")
                                                nome = nome.replace('&#8211;',"-")
                                                nome = nome.replace('&#038;',"&")
                                                nome = nome.replace('(PT-PT)',"")
                                                nome = nome.replace('(PT/PT)',"")
                                                nome = nome.replace('[PT-PT]',"")
                                                nome = nome.replace('[PT/PT]',"")
                                                generos = re.compile('id="post-.+?" class="post-.+? post type-post status-publish format-standard hentry (.+?)">').findall(item)
                                                if not generos: generos = re.compile('post type-post status-publish format-standard hentry (.+?)id="post-.+?">').findall(item)
                                                if generos:
                                                        genero = generos[0]
                                                else:
                                                        genero = ''
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
                                                                ano_filme = ': ' + ano[0]
                                                        else:
                                                                ano_filme = ''     
                                                if ano:
                                                        ano_filme = ano[0]
                                                        a_q = re.compile('\d+')
                                                        qq_aa = a_q.findall(nome)
                                                        for q_a_q_a in qq_aa:
                                                                if len(q_a_q_a) == 4:
                                                                        tirar_ano = '(' + str(q_a_q_a) + ')'
                                                                        nome = nome.replace(tirar_ano,'')
                                                if qualidade:
                                                        qualidade = qualidade[0]
                                                        qualidade = qualidade.replace('[',' - ')
                                                        qualidade = qualidade.replace(']','')
                                                else:
                                                        qualidade = re.compile("\nQUALIDADE:\xc2\xa0(.+?)<br/>").findall(item)
                                                        if qualidade:
                                                                qualidade = qualidade[0]
                                                                qualidade = qualidade.replace('[',' - ')
                                                                qualidade = qualidade.replace(']','')
                                                        else:
                                                                qualidade = ''
                                                try:
                                                        #addDir(nome,urletitulo[0][0],233,'','','')
                                                        if 'filmes' in genero or 'series' in genero or 'animacao' in genero:
                                                                if 'online' in genero:
                                                                        #if 'OP\xc3\x87\xc3\x83O' in item:
                                                                        addDir('[B][COLOR green]- ' + nome + '[/COLOR][/B][COLOR yellow] (' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR]',url,233,thumbnail[0].replace('s72-c','s320'),'','')
                                                                        num_f = num_f + 1
                                                except: pass
                        except: pass
        else: num_f = 0
        if num_f == 0:
                if selfAddon.getSetting('movies-view') == "0": addDir1('- No Match Found -','','','',False,'')
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

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Checker: "+str(checker)
print "Iconimage: "+str(iconimage)



#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
