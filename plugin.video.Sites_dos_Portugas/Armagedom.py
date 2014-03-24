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
from array import array
from string import capwords


arrai_nome_series = ['' for i in range(50)]
arrai_endereco_series = ['' for i in range(50)]
arrai_series1 = [['' for i in range(50)] for j in range(2)]
arrai_series = ['' for i in range(100)]
i=0

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#



def ARM_MenuPrincipal():
        addDir1(name+'[COLOR blue] - Menu Principal[/COLOR]','','',artfolder,False,'')
        #----------------------------------------------------------------------
        addDir1('','','',artfolder,False,'')
	addDir('[COLOR blue]Filmes - [/COLOR][B][COLOR yellow]ARMAGEDOM[/COLOR][COLOR green]FILMES[/COLOR][/B]','url',337,artfolder,'nao','')
	addDir('[COLOR blue]Séries - [/COLOR][B][COLOR yellow]ARMAGEDOM[/COLOR][COLOR green]FILMES[/COLOR][/B]','http://www.armagedomfilmes.biz/?cat=21',332,artfolder,'nao','')	
	addDir('[COLOR blue]Animação - [/COLOR][B][COLOR yellow]ARMAGEDOM[/COLOR][COLOR green]FILMES[/COLOR][/B]','http://www.armagedomfilmes.biz/?cat=3228',332,artfolder,'nao','')
	addDir('[COLOR blue]Animes/Desenhos - [/COLOR][B][COLOR yellow]ARMAGEDOM[/COLOR][COLOR green]FILMES[/COLOR][/B]','http://www.armagedomfilmes.biz/?cat=36',332,artfolder,'nao','')
        addDir('[COLOR blue]Categorias - [/COLOR][B][COLOR yellow]ARMAGEDOM[/COLOR][COLOR green]FILMES[/COLOR][/B]','http://www.armagedomfilmes.biz/',338,artfolder,'nao','')
        addDir('Pesquisar - [B][COLOR yellow]ARMAGEDOM[/COLOR][COLOR green]FILMES[/COLOR][/B]','http://www.armagedomfilmes.biz/?s=',334,artfolder,'nao','')
        if selfAddon.getSetting('hide-porno') == "false":
			addDir('[B][COLOR red]M+18 - [/COLOR][COLOR yellow]ARMAGEDOM[/COLOR][COLOR green]FILMES[/COLOR][/B]','http://www.megavideoporno.org/porno/filmes',350,artfolder,'nao','')
        #----------------------------------------------------------------------
        addDir1('','','',artfolder,False,'')
        addDir('[COLOR blue]Filmes - [/COLOR][B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].tv','url',349,artfolder,'nao','')
	addDir('[COLOR blue]Séries - [/COLOR][B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].tv','url',349,artfolder,'nao','')	
	addDir('[COLOR blue]Animação - [/COLOR][B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].tv','http://megafilmeshd.tv/category/animacao/',349,artfolder,'nao','')
	addDir('[COLOR blue]Categorias - [/COLOR][B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].tv','http://megafilmeshd.tv/',349,artfolder,'nao','')
        #----------------------------------------------------------------------
        addDir1('','','',artfolder,False,'')
        addDir('[COLOR blue]Filmes - [/COLOR][B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].net','url',337,artfolder,'nao','')
	addDir('[COLOR blue]Séries - [/COLOR][B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].net','http://megafilmeshd.net/series/',353,artfolder,'nao','')	
	addDir('[COLOR blue]Animação - [/COLOR][B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].net','http://megafilmeshd.net/category/animacao/',351,artfolder,'nao','')
	addDir('[COLOR blue]Categorias - [/COLOR][B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].net','http://megafilmeshd.net/category/lancamentos/',352,artfolder,'nao','')
	addDir('Pesquisar Filmes - [B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].net','http://megafilmeshd.net/?s=',334,artfolder,'nao','')
	addDir('Pesquisar Séries - [B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].net','http://megafilmeshd.net/series/?pesquisaRapida=',334,artfolder,'nao','')
        #----------------------------------------------------------------------
        addDir1('','','',artfolder,False,'')
	#addDir('Pesquisar','url',1,artfolder,'nao','')
	#addDir('[COLOR brown]ChangeLog[/COLOR]','http://o-repositorio-maluco.googlecode.com/svn/trunk/changelogs/changelog_TugaFilmesTV.txt',56,artfolder,'nao','')
 
def ARM_Menu_Filmes():
        addDir1(name,'','',artfolder,False,'')
        addDir1('','','',artfolder,False,'')
        if name == '[COLOR blue]Filmes - [/COLOR][B][COLOR yellow]ARMAGEDOM[/COLOR][COLOR green]FILMES[/COLOR][/B]':
                addDir('[COLOR orange]Lançamentos[/COLOR]','http://www.armagedomfilmes.biz/?cat=3236',332,artfolder,'nao','')
                addDir('[COLOR orange]Blu-Ray[/COLOR]','http://www.armagedomfilmes.biz/?cat=5529',332,artfolder,'nao','')
                addDir('[COLOR orange]Legendados[/COLOR]','http://www.armagedomfilmes.biz/?s=legendado',332,artfolder,'nao','')
        if name == '[COLOR blue]Filmes - [/COLOR][B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].net':
                addDir('[COLOR orange]Lançamentos[/COLOR]','http://megafilmeshd.net/category/lancamentos/',351,artfolder,'nao','')
                addDir('[COLOR orange]Últimos[/COLOR]','http://megafilmeshd.net/ultimos',351,artfolder,'nao','')

def ARM_Menu_Series():
        addDir1('[B][COLOR yellow]Menu Séries[/COLOR][/B]','','',artfolder,False,'')
        addDir1('','','',artfolder,False,'')
	addDir('[COLOR blue]A a Z[/COLOR]','url',341,artfolder,'nao','')
        addDir('[COLOR blue]Recentes[/COLOR]','http://www.armagedomfilmes.biz/?cat=21',332,artfolder,'nao','')
        addDir1('','','',artfolder,False,'')
	#addDir('Pesquisar','http://www.tuga-filmes.tv/search?q=',1,artfolder,'nao','')



def ARM_Menu_Filmes_Por_Categorias():
        addDir1(name,'','',artfolder,False,'')
        addDir1('','','',artfolder,False,'')
        html_categorias_source = ARM_abrir_url(url)
	html_items_categorias = re.findall('<h2 class="widgettitle">Categorias</h2>(.*?)<div class="clear"></div>', html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                #filmes_por_categoria = re.compile('href="(.+?)"><b><span style="color: .+?">(.+?)</span>').findall(item_categorias)
                #for endereco_categoria,nome_categoria in filmes_por_categoria:
                        #if 'Assistir' not in nome_categoria and 'Adulto' not in nome_categoria and 'Programas' not in nome_categoria:
                                #addDir('[B][COLOR orange]' + nome_categoria + '[/COLOR][/B] ',endereco_categoria,332,artfolder,'nao','')
                filmes_por_categoria = re.compile('<a href="(.+?)" title=".+?">(.+?)</a>').findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        addDir('[B][COLOR orange]' + nome_categoria + '[/COLOR][/B] ',endereco_categoria,332,artfolder,'nao','')

def ARM_Menu_Filmes_Por_Categorias_MEGA_net():
        addDir1(name,'','',artfolder,False,'')
        addDir1('','','',artfolder,False,'')
        html_categorias_source = ARM_abrir_url(url)
	html_items_categorias = re.findall('<li id="menu_genero">(.*?)<ul id="category-thumbs">', html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        if 'Lan\xc3\xa7amentos' not in nome_categoria and 'S\xc3\xa9ries' not in nome_categoria:
                                addDir('[B][COLOR orange]' + nome_categoria + '[/COLOR][/B] ',endereco_categoria,351,artfolder,'nao','')


def ARM_pesquisar():
	keyb = xbmc.Keyboard('', 'Escreva o parâmetro de pesquisa') #Chama o keyboard do XBMC com a frase indicada
	keyb.doModal() #Espera ate que seja confirmada uma determinada string
	if (keyb.isConfirmed()): #Se a entrada estiver confirmada (isto e, se carregar no OK)
		search = keyb.getText() #Variavel search fica definida com o conteudo do formulario
		parametro_pesquisa=urllib.quote(search) #parametro_pesquisa faz o quote da expressao search, isto é, escapa os parametros necessarios para ser incorporado num endereço url
		url_pesquisa = url + str(parametro_pesquisa)#+ '&x=0&y=0' #nova definicao de url. str força o parametro de pesquisa a ser uma string
		#addDir1(url_pesquisa,'','',artfolder,False,'')
		if 'armagedom' in url_pesquisa: ARM_encontrar_fontes_filmes(url_pesquisa) #chama a função listar_videos com o url definido em cima
                if 'megafilmeshd.net' in url_pesquisa and 'Filmes' in name: ARM_encontrar_fontes_filmes_MEGA_net(url_pesquisa) #chama a função listar_videos com o url definido em cima
                if 'megafilmeshd.net' in url_pesquisa and 'Séries' in name: ARM_encontrar_fontes_series_MEGA_net(url_pesquisa) #chama a função listar_videos com o url definido em cima


#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#

		

def ARM_encontrar_fontes_filmes(url):        
        if 'Seguinte' not in name:
                addDir1(name + ':','','',iconimage,False,'')
                addDir1('','','',iconimage,False,'')
	try:
		html_source = ARM_abrir_url(url)
	except: html_source = ''
	items = re.findall('<div class="titulo-post-us">(.*?)<div class="div-us">', html_source, re.DOTALL)
	#addDir1(str(len(items)),'','',iconimage,False,'')
	if items != []:
		print len(items)
		for item in items:
                        urletitulo = re.compile('<a href="(.+?)" title="(.+?)">').findall(item)
                        thumbnail = re.compile('src="(.+?)"').findall(item)
                        if thumbnail: thumb = thumbnail[0]
                        else: thumb = ''
                        urlfilme = urletitulo[0][0]
                        nome = urletitulo[0][1].replace('Assistir ','')
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        if qq_aa:
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) == 4:
                                                ano = str(q_a_q_a)
                                                nome = nome.replace(' '+ano,'')
                        else: ano = ''
                        if ' Dublado ou Legendado' in nome: nome = nome.replace(' Dublado ou Legendado','')
                        if ' Dublado e Legendado &#8211;' in nome: nome = nome.replace(' Dublado e Legendado &#8211;','')
                        if ' Dublado e Legendado' in nome: nome = nome.replace(' Dublado e Legendado','')
                        if ' Online' in nome: nome = nome.replace(' Online','')
                        if ' Dublado' in nome: nome = nome.replace(' Dublado','')
                        if ' Legendado' in nome: nome = nome.replace(' Legendado','')
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8230;',"...")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('#038;','')
                        try:
                                addDir('[B][COLOR yellow]' + nome + '[/COLOR][COLOR green] (' + ano + ')[/COLOR][/B]',urlfilme,333,thumb,'nao','')
                        except: pass
	proxima = re.compile('<link rel="next" href="(.+?)"/>').findall(html_source)		
	try:
                addDir1('','','',iconimage,False,'')
		addDir("Página Seguinte >>",proxima[0].replace('#038;',''),332,artfolder,'nao','')
        except:pass


def ARM_encontrar_fontes_filmes_MEGA():        
        if 'Seguinte' not in name:
                addDir1(name + ':','','',iconimage,False,'')
                addDir1('','','',iconimage,False,'')
	try:
		html_source = ARM_abrir_url(url)
	except: html_source = ''
	items = re.findall('<li>(.*?)<div class="autor-thumb">', html_source, re.DOTALL)
	#addDir1(str(len(items)),'','',iconimage,False,'')
	if items != []:
		print len(items)
		for item in items:
                        urletitulo = re.compile('<a href="(.+?)" title="(.+?)" class="link-tumb"></a>').findall(item)
                        if urletitulo:
                                urlfilme = urletitulo[0][0]
                                nome = urletitulo[0][1].replace('Assistir ','')
                        else:
                                urlfilme = ''
                                nome = ''
                        thumbnail = re.compile('src="(.+?)&amp;h=259&amp;w=177"').findall(item)
                        if thumbnail: thumb = thumbnail[0].replace('http://static.filmesonlinegratis.net/thumb.php?src=','')
                        else: thumb = ''
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        if qq_aa:
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) == 4:
                                                ano = str(q_a_q_a)
                                                nome = nome.replace(' '+ano,'')
                        else: ano = ''
                        if ' Dublado ou Legendado' in nome: nome = nome.replace(' Dublado ou Legendado','')
                        if ' Dublado e Legendado &#8211;' in nome: nome = nome.replace(' Dublado e Legendado &#8211;','')
                        if ' Dublado e Legendado' in nome: nome = nome.replace(' Dublado e Legendado','')
                        if ' Online' in nome: nome = nome.replace(' Online','')
                        if ' Dublado' in nome: nome = nome.replace(' Dublado','')
                        if ' Legendado' in nome: nome = nome.replace(' Legendado','')
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8230;',"...")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('#038;','')
                        try:
                                addDir('[B][COLOR yellow]' + nome + '[/COLOR][COLOR green] (' + ano + ')[/COLOR][/B]',urlfilme,333,thumb,'nao','')
                        except: pass
	proxima = re.compile('<a class="nextpostslink" href="(.+?)">&raquo;').findall(html_source)		
	try:
                addDir1('','','',iconimage,False,'')
		addDir("Página Seguinte >>",proxima[0].replace('#038;',''),349,artfolder,'nao','')
        except:pass


def ARM_encontrar_fontes_filmes_MEGA_net(url):        
        if 'Seguinte' not in name:
                addDir1(name + ':','','',iconimage,False,'')
                addDir1('','','',iconimage,False,'')
	try:
		html_source = ARM_abrir_url(url)
	except: html_source = ''
	items = re.findall('<li ti(.*?)<div class="tt-category">', html_source, re.DOTALL)
	#addDir1(str(len(items)),'','',iconimage,False,'')
	if items != []:
		print len(items)
		for item in items:
                        titulo = re.compile('tle="(.+?)"').findall(item)
                        if titulo: nome = titulo[0]
                        else: nome = ''
                        urlthumb = re.compile('<a href="(.+?)"><img src="(.+?)"').findall(item)
                        if urlthumb:
                                thumb = urlthumb[0][1]
                                urlfilme = urlthumb[0][0]
                        else:
                                thumb = ''
                                urlfilme = ''
                        ano = re.compile('<div class="tt-calendar">(.+?)</div>').findall(item)
                        if ano: ano_filme = ano[0]
                        else: ano_filme = ''
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8230;',"...")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('#038;','')
                        try:
                                addDir('[B][COLOR yellow]' + nome + '[/COLOR][COLOR green] (' + ano_filme + ')[/COLOR][/B]',urlfilme,333,thumb,'nao','')
                        except: pass
	proxima = re.compile('<a href=\'(.+?)\' class=\'nextpostslink\'>').findall(html_source)		
	try:
                addDir1('','','',iconimage,False,'')
		addDir("Página Seguinte >>",proxima[0].replace('#038;',''),351,artfolder,'nao','')
        except:pass

def ARM_encontrar_fontes_series_MEGA_net(url):        
        if 'Seguinte' not in name:
                addDir1(name + ':','','',iconimage,False,'')
                addDir1('','','',iconimage,False,'')
	try:
		html_source = ARM_abrir_url(url)
	except: html_source = ''
	items = re.findall('<div id="quadrado"(.*?)/></a></div>', html_source, re.DOTALL)
	#addDir1(str(len(items)),'','',iconimage,False,'')
	if items != []:
		print len(items)
		for item in items:
                        titulo = re.compile('title="(.+?)"').findall(item)
                        if titulo: nome = titulo[0]
                        else: nome = ''
                        urlthumb = re.compile('<a href="(.+?)"><img src="(.+?)"').findall(item)
                        if urlthumb:
                                thumb = urlthumb[0][1]
                                urlfilme = urlthumb[0][0]
                        else:
                                thumb = ''
                                urlfilme = ''
                        ano = re.compile('<div class="tt-calendar">(.+?)</div>').findall(item)
                        if ano: ano_filme = ano[0]
                        else: ano_filme = ''
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8230;',"...")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('#038;','')
                        try:
                                addDir('[B][COLOR yellow]' + nome + '[/COLOR][COLOR green] (' + ano_filme + ')[/COLOR][/B]',urlfilme,333,thumb,'nao','')
                        except: pass
	proxima = re.compile('<a href=\'(.+?)\' class=\'nextpostslink\'>').findall(html_source)		
	try:
                addDir1('','','',iconimage,False,'')
		addDir("Página Seguinte >>",proxima[0].replace('#038;',''),351,artfolder,'nao','')
        except:pass

#----------------------------------------------------------------------------------------------------------------------------------------------#

def ARM_encontrar_videos_filmes(name,url):
        num_fonte = 0
	addDir1(name,'','',iconimage,False,'')
        addDir1('','','',iconimage,False,'')
	try:
		link2=ARM_abrir_url(url)
	except: link2 = '' 
	if link2:
                if 'ASSISTIR: LEGENDADO' in link2: addDir1('[COLOR orange]Dublado:[/COLOR]','','',iconimage,False,'')
                urls_video = re.compile('<div id="ver-filme-user">\n<iframe frameborder="0" height="480" scrolling="no" src="(.+?)" width="600"></iframe>\n</div>').findall(link2)
                for url_video in urls_video:
                        id_video = re.compile('id=(.*)').findall(url_video)
                        if id_video: id_video = id_video[0]
                        else: id_video = ''
                        num_fonte = num_fonte + 1
                        ARM_resolve_not_videomega_filmes(url_video,id_video,num_fonte)          
                matchvideo = re.findall('\n \n \n<div id=".+?">\n(.*?)\n</div>\n \n \n', link2, re.DOTALL)
                for match in matchvideo:
                        urls_video = re.compile('src="(.+?)"').findall(match)
                        if urls_video:
                                for url_video in urls_video:
                                        id_video = re.compile('id=(.*)').findall(url_video)
                                        if id_video: id_video = id_video[0]
                                        else: id_video = ''
                                        num_fonte = num_fonte + 1
                                        ARM_resolve_not_videomega_filmes(url_video,id_video,num_fonte)
                        urls_video = re.compile('SRC="(.+?)"').findall(match)
                        if urls_video:
                                for url_video in urls_video:
                                        id_video = re.compile('id=(.*)').findall(url_video)
                                        if id_video: id_video = id_video[0]
                                        else: id_video = ''
                                        num_fonte = num_fonte + 1
                                        ARM_resolve_not_videomega_filmes(url_video,id_video,num_fonte)
                if 'ASSISTIR: LEGENDADO' in link2:
                        num_fonte = 0
                        addDir1('[COLOR orange]Legendado:[/COLOR]','','',iconimage,False,'')
                        matchvideo = re.findall('<p style="text-align: center;">(.*?)<center><a href="https://twitter.com/share"', link2, re.DOTALL)
                        for match in matchvideo:
                                urls_video = re.compile('href="(.+?)"').findall(match)
                                if urls_video:
                                        for url_video in urls_video:
                                                id_video = re.compile('id=(.*)').findall(url_video)
                                                if id_video: id_video = id_video[0]
                                                else: id_video = ''
                                                num_fonte = num_fonte + 1
                                                ARM_resolve_not_videomega_filmes(url_video,id_video,num_fonte)
                if 'Temporada' in link2:
                        i = 0
                        num_fonte = 0
                        num_temporada = 1
                        ep = 1
                        matchvideo = re.findall('style="text-align: center.+?Assistir (.+?) Temporada(.+?)<center><a href="https://twitter.com/share"',link2,re.DOTALL)
			if matchvideo:
				for parte1,parte2 in matchvideo:				
					matchvideo = re.compile('<iframe src="(.+?)"').findall(parte2)	
					for url_video in matchvideo:
                                                id_video = re.compile('id=(.*)').findall(url_video)
                                                if id_video: id_video = id_video[0]
                                                else: id_video = ''
                                                num_fonte = num_fonte + 1
                                                addDir('[B]'+epi+'[/B]','',342,iconimage,'','')
					matchvideo = re.compile('<a href="(.+?)" target="_bla.+?Assistir (.+?)<.+?<span style="color: .+?">(.+?)</span>').findall(parte2)
					if matchvideo:
                                                for url_video,epi,ver in matchvideo:
                                                        i=i+1
                                                        if 'DUB' not in ver and 'dublado' not in url_video:
                                                                dub_leg = ' (LEGENDADO)'
                                                        if 'dublado' in url_video or 'DUB' in ver:
                                                                dub_leg = ' (DUBLADO)'
                                                                if 'DUB' in ver:
                                                                        ver = ''
                                                        if 'LEG' in ver:
                                                                dub_leg = ' (LEGENDADO)'
                                                                ver = ''
                                                        if 'Dub' in ver and 'Leg' in ver: dub_leg = ''
                                                        epi = epi.replace('&#8211;',"-")
                                                        arrai_series[i] = epi
                                                        if '00' in epi and ('00' not in arrai_series[i-1] and '01' not in arrai_series[i-1]):
                                                                addDir1('[COLOR blue]'+str(num_temporada)+'ª Temporada[/COLOR]','','',iconimage,False,'')
                                                                num_temporada = num_temporada + 1
                                                                ep = 0
                                                        if '01' in epi and ('00' not in arrai_series[i-1] and '01' not in arrai_series[i-1]):
                                                                addDir1('[COLOR blue]'+str(num_temporada)+'ª Temporada[/COLOR]','','',iconimage,False,'')
                                                                num_temporada = num_temporada + 1
                                                                ep = 0
                                                        id_video = re.compile('id=(.*)').findall(url_video)
                                                        if id_video: id_video = id_video[0]
                                                        else: id_video = ''
                                                        num_fonte = num_fonte + 1
                                                        addDir('[B]'+epi+'[/B]'+dub_leg+ver,url_video,342,iconimage,'','')
                                        else:
                                                matchvideo = re.compile('<a href="(.+?)" target="_bla.+?Assistir (.+?)<').findall(parte2)
                                                for url_video,epi in matchvideo:
                                                        i=i+1
                                                        if 'dublado' in url_video: dub_leg = ' (DUBLADO)'
                                                        else: dub_leg = ' (LEGENDADO)'
                                                        epi = epi.replace('&#8211;',"-")
                                                        arrai_series[i] = epi
                                                        if '00' in epi and ('00' not in arrai_series[i-1] and '01' not in arrai_series[i-1]):
                                                                addDir1('[COLOR blue]'+str(num_temporada)+'ª Temporada[/COLOR]','','',iconimage,False,'')
                                                                num_temporada = num_temporada + 1
                                                                ep = 0
                                                        if '01' in epi and ('00' not in arrai_series[i-1] and '01' not in arrai_series[i-1]):
                                                                addDir1('[COLOR blue]'+str(num_temporada)+'ª Temporada[/COLOR]','','',iconimage,False,'')
                                                                num_temporada = num_temporada + 1
                                                                ep = 0
                                                        id_video = re.compile('id=(.*)').findall(url_video)
                                                        if id_video: id_video = id_video[0]
                                                        else: id_video = ''
                                                        num_fonte = num_fonte + 1
                                                        addDir('[B]'+epi+'[/B]'+dub_leg,url_video,342,iconimage,'','')
                if 'TEMPORADA' in link2:
                        i = 0
                        num_fonte = 0
                        num_temporada = 1
                        ep = 1
                        matchvideo = re.findall('style="text-align: center.+?ASSISTIR (.+?) TEMPORADA(.+?)<center><a href="https://twitter.com/share"',link2,re.DOTALL)
			if matchvideo:			
				for parte1,parte2 in matchvideo:				
					matchvideo = re.compile('<iframe src="(.+?)"').findall(parte2)	
					for url_video in matchvideo:
                                                id_video = re.compile('id=(.*)').findall(url_video)
                                                if id_video: id_video = id_video[0]
                                                else: id_video = ''
                                                num_fonte = num_fonte + 1
                                                addDir('[B]'+epi+'[/B]','',342,iconimage,'','')
					matchvideo = re.compile('<a href="(.+?)" target="_bla.+?Assistir (.+?)<.+?<span style="color: .+?">(.+?)</span>').findall(parte2)
                                        if matchvideo:
                                                for url_video,epi,ver in matchvideo:
                                                        i=i+1
                                                        if 'DUB' not in ver and 'dublado' not in url_video:
                                                                dub_leg = ' (LEGENDADO)'
                                                        if 'dublado' in url_video or 'DUB' in ver:
                                                                dub_leg = ' (DUBLADO)'
                                                                if 'DUB' in ver:
                                                                        ver = ''
                                                        if 'LEG' in ver:
                                                                dub_leg = ' (LEGENDADO)'
                                                                ver = ''
                                                        if 'Dub' in ver and 'Leg' in ver: dub_leg = ''
                                                        epi = epi.replace('&#8211;',"-")
                                                        arrai_series[i] = epi
                                                        if '00' in epi and ('00' not in arrai_series[i-1] and '01' not in arrai_series[i-1]):
                                                                addDir1('[COLOR blue]'+str(num_temporada)+'ª Temporada[/COLOR]','','',iconimage,False,'')
                                                                num_temporada = num_temporada + 1
                                                                ep = 0
                                                        if '01' in epi and ('00' not in arrai_series[i-1] and '01' not in arrai_series[i-1]):
                                                                addDir1('[COLOR blue]'+str(num_temporada)+'ª Temporada[/COLOR]','','',iconimage,False,'')
                                                                num_temporada = num_temporada + 1
                                                                ep = 0
                                                        id_video = re.compile('id=(.*)').findall(url_video)
                                                        if id_video: id_video = id_video[0]
                                                        else: id_video = ''
                                                        num_fonte = num_fonte + 1
                                                        addDir('[B]'+epi+'[/B]'+dub_leg+ver,url_video,342,iconimage,'','')
                                        else:
                                                #addDir('nao','',342,iconimage,'','')
                                                matchvideo = re.compile('<a href="(.+?)" target="_bla.+?Assistir (.+?)<').findall(parte2)
                                                for url_video,epi in matchvideo:
                                                        i=i+1
                                                        if 'dublado' in url_video: dub_leg = ' (DUBLADO)'
                                                        else: dub_leg = ' (LEGENDADO)'
                                                        epi = epi.replace('&#8211;',"-")
                                                        arrai_series[i] = epi
                                                        if '00' in epi and ('00' not in arrai_series[i-1] and '01' not in arrai_series[i-1]):
                                                                addDir1('[COLOR blue]'+str(num_temporada)+'ª Temporada[/COLOR]','','',iconimage,False,'')
                                                                num_temporada = num_temporada + 1
                                                                ep = 0
                                                        if '01' in epi and ('00' not in arrai_series[i-1] and '01' not in arrai_series[i-1]):
                                                                addDir1('[COLOR blue]'+str(num_temporada)+'ª Temporada[/COLOR]','','',iconimage,False,'')
                                                                num_temporada = num_temporada + 1
                                                                ep = 0
                                                        id_video = re.compile('id=(.*)').findall(url_video)
                                                        if id_video: id_video = id_video[0]
                                                        else: id_video = ''
                                                        num_fonte = num_fonte + 1
                                                        addDir('[B]'+epi+'[/B]'+dub_leg,url_video,342,iconimage,'','')
                if 'Coleção' in link2:
                        matchvideo = re.findall('style="text-align: center;">(.*?)>ASSISTIR FILME ONLINE',link2,re.DOTALL)
                        if not matchvideo: matchvideo = re.findall('style="text-align: center;">(.*?)border="0"/></a>',link2,re.DOTALL)
			if matchvideo:			
				for parte in matchvideo:
                                        url_filmes = re.compile('href="(.+?)"').findall(parte)
                                        for url in url_filmes:
                                                if 'p=' in url: url_filme = url
					thumb = re.compile('src="(.+?)"').findall(parte)
					nome_filme = re.compile('<strong>(.+?)</strong>').findall(parte)
					if nome_filme:
                                                for n in nome_filme:
                                                        #addDir(n,'',333,'','','')
                                                        if n != '[' and n != ']' and 'href' not in n: nome = n
					else:
                                                nome_filme = re.compile('<strong>(.+?)<br/>').findall(parte)
                                                if nome_filme: nome = nome_filme[0]
                                                else:
                                                        nome_filme = re.compile('<span style="color: .+?">(.+?)</span>').findall(parte)
                                                        if nome_filme:
                                                                for n in nome_filme:
                                                                        #addDir(n,'',333,'','','')
                                                                        if n != '[' and n != ']' and 'href' not in n: nome = n
                                                        else: nome = ''
                                        if 'span' in nome:
                                                nome_filme = re.compile('<span style="color: .+?">(.+?)</span>').findall(parte)
                                                if nome_filme: nome = nome_filme[0]
                                                else: nome = ''
					nome = nome.replace('&#8217;',"'")
                                        nome = nome.replace('&#8230;',"...")
                                        nome = nome.replace('&#8211;',"-")
                                        nome = nome.replace('#038;','&')
                                        addDir('[B]'+nome+'[/B]',url_filme,333,thumb[0],'','')
                        else:
                                matchvideo = re.findall('style="text-align: center;">(.*?)>ASSISTIR FILME',link2,re.DOTALL)
                                if matchvideo:			
                                        for parte in matchvideo:
                                                titulo = re.compile('<address style="text-align: center;"><strong>(.+?)</strong></address>').findall(parte)
                                                if titulo:
                                                        for tit in titulo:
                                                                if 'span' not in tit and 'img' not in tit and 'href' not in tit:
                                                                        title = tit
                                                else:
                                                        titulo = re.compile('<strong>(.+?)<br/>').findall(parte)
                                                        if titulo:
                                                                for tit in titulo:
                                                                        if 'span' not in tit and 'img' not in tit and 'href' not in tit:
                                                                                title = tit
                                                                                if 'strong' in title:
                                                                                        title = title.replace('<strong>','').replace('</strong>','')
                                                        else: title = ''
                                                title = title.replace('&#8217;',"'")
                                                title = title.replace('&#8230;',"...")
                                                title = title.replace('&#8211;',"-")
                                                title = title.replace('#038;','&')
                                                url_filme = re.compile('href="(.+?)"').findall(parte)
                                                thumb = re.compile('src="(.+?)"').findall(parte)
                                                nome_filme = re.compile('<strong>.+?[[](.+?)[]].+?</strong>').findall(parte)
                                                if nome_filme: nome = nome_filme[0]
                                                else:
                                                        nome_filme = re.compile('<strong>.+?[[](.+?)[]].+?<br/>').findall(parte)
                                                        nome = nome_filme[0]
                                                if 'span' in nome:
                                                        nome_filme = re.compile('<span style="color: .+?">(.+?)</span>').findall(parte)
                                                        nome = nome_filme[0]
                                                nome = nome.replace('&#8217;',"'")
                                                nome = nome.replace('&#8230;',"...")
                                                nome = nome.replace('&#8211;',"-")
                                                nome = nome.replace('#038;','&')
                                                addDir('[B]'+nome+' - '+title+'[/B]',url_filme[0],333,thumb[0],'','')
                matchvideo = re.findall('main"(.*?)id="x',link2,re.DOTALL)
                if matchvideo:
                        partes = re.findall('id="xmain"(.*)',link2,re.DOTALL)
                        num_partes = len(partes)
                        num_part = 0
                        for parte in matchvideo:
                                num_part = num_part + 1
                                temporada = re.compile('onclick="JavaScript:doMenu.+?;">(.+?)</a>').findall(parte)
                                addDir1(str(num_partes)+'[COLOR blue]'+temporada[0]+'[/COLOR]','','',iconimage,False,'')
                                urletitulo = re.compile('<a class="video" href="(.+?)">(.+?)</a>').findall(parte)
                                for url, titulo in urletitulo:
                                        addDir('[B]'+titulo+'[/B]',url,342,iconimage,'','')
                        addLink(str(num_part)+partes[0],'','')
                        if num_partes > num_part:
                                #for part in partes:
                                matchvideo = re.findall('onclick="JavaScript(.*?)<p class="ntemp">',partes[num_part],re.DOTALL)
                                if matchvideo: addLink(str(num_part),'','')
                                        
                
                


                                        
                
def ARM_encontrar_videos_series(name,url):
        num_fonte = 0
	addDir1(name,'','',iconimage,False,'')
        addDir1('','','',iconimage,False,'')
	try:
		link2=ARM_abrir_url(url)
	except: link2 = '' 
	if link2:         
                matchvideo = re.findall("<div class=\'post-header\'>(.*?)<div class=\'post-footer\'>", link2, re.DOTALL)
                for match in matchvideo:
                        urls_video = re.compile('src="(.+?)"').findall(match)
                        if urls_video:
                                for url_video in urls_video:
                                        id_video = re.compile('id=(.*)').findall(url_video)
                                        if id_video: id_video = id_video[0]
                                        else: id_video = ''
                                        if '.jpg' not in url_video and '.png' not in url_video: num_fonte = num_fonte + 1
                                        ARM_resolve_not_videomega_filmes(url_video,id_video,num_fonte)
                        urls_video = re.compile('SRC="(.+?)"').findall(match)
                        if urls_video:
                                for url_video in urls_video:
                                        id_video = re.compile('id=(.*)').findall(url_video)
                                        if id_video: id_video = id_video[0]
                                        else: id_video = ''
                                        if '.jpg' not in url_video and '.png' not in url_video: num_fonte = num_fonte + 1
                                        ARM_resolve_not_videomega_filmes(url_video,id_video,num_fonte)
                matchvideo = re.findall('<div class="post-content">(.*?)<!-- Post Content -->', link2, re.DOTALL)
                for match in matchvideo:
                        urls_video = re.compile('src="(.+?)"').findall(match)
                        if urls_video:
                                for url_video in urls_video:
                                        id_video = re.compile('id=(.*)').findall(url_video)
                                        if id_video: id_video = id_video[0]
                                        else: id_video = ''
                                        if '.jpg' not in url_video and '.png' not in url_video: num_fonte = num_fonte + 1
                                        ARM_resolve_not_videomega_filmes(url_video,id_video,num_fonte)
                        urls_video = re.compile('SRC="(.+?)"').findall(match)
                        if urls_video:
                                for url_video in urls_video:
                                        id_video = re.compile('id=(.*)').findall(url_video)
                                        if id_video: id_video = id_video[0]
                                        else: id_video = ''
                                        if '.jpg' not in url_video and '.png' not in url_video: num_fonte = num_fonte + 1
                                        ARM_resolve_not_videomega_filmes(url_video,id_video,num_fonte)
                        
				
#----------------------------------------------------------------------------------------------------------------------------------------------#

def ARM_resolve_not_videomega_filmes(url,id_video,num_fonte):
        if "videomega" in url:
		try:
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Videomega)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "vidto.me" in url:
		try:
                        match = re.compile('http://vidto.me/embed-(.+?).html').findall(url)
			if match:
				id_video = match[0]
				url = 'http://vidto.me/' + id_video + '.html'
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Vidto.me)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "dropvideo" in url or 'drop' in url:
		try:
                        url = 'http://dropvideo.com/embed/' + id_video
			print url
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](DropVideo)[/COLOR][/B]',url,30,iconimage,'','')
		except:pass
	if "streamin.to" in url:
                try:
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,30,iconimage,'','')
                except:pass                        
        if "putlocker" in url or 'armage.php' in url:
                try:
                        url = 'http://www.putlocker.com/embed/' + id_video
                        print url
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Putlocker)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "nowvideo" in url:
                try:
                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video
                        print url
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Nowvideo)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "primeshare" in url:
                try:
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Primeshare.tv)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "videoslasher" in url:
                try:
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](VideoSlasher)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "sockshare" in url:
                try:
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Sockshare)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "flashx.tv" in url:
                try:
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](FlashX.tv)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "/flashxtv/" in url:
                try:
                        try:
                                flashxtv=ARM_abrir_url(url)
                        except: flashxtv = ''
                        flash = re.compile('</head><body><iframe width="600" height="480" src="(.+?)"').findall(flashxtv)
                        try:
                                flashxtv=ARM_abrir_url(flash[0])
                        except: flashxtv = ''
                        flashurl = re.compile('addthis:url="(.+?)" addthis:').findall(flashxtv)
                        url = flashurl[0]
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](FlashX.tv)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "video.tt" in url:
                try:
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Video.tt)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	return

   




def ARM_encontrar_fontes_filmes_M18():        
        if 'Seguinte' not in name:
                addDir1(name + ':','','',iconimage,False,'')
                addDir1('','','',iconimage,False,'')
	try:
		html_source = ARM_abrir_url(url)
	except: html_source = ''
	items = re.findall('<img src="http://www.megavideoporno.org/wp-content/themes/25-MegaPorno/timthumb.php?(.*?)title="">', html_source, re.DOTALL)
	addDir1(str(len(items)),'','',iconimage,False,'')
	if items != []:
                addDir1(name + ':','','',iconimage,False,'')
		print len(items)
		for item in items:
                        url = re.compile('href="(.+?)"').findall(item)
                        titulo = re.compile('title="(.+?)"').findall(item)
                        thumbnail = re.compile('src=(.+?)&amp;h=226&amp;w=165"').findall(item)
                        if thumbnail: thumb = thumbnail[0]
                        else: thumb = ''
                        urlfilme = url[0]
                        nome = titulo[0]
                        ano = ''
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8230;',"...")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('#038;','')
                        try:
                                addDir('[B][COLOR yellow]' + nome + '[/COLOR][COLOR green] (' + ano + ')[/COLOR][/B]',urlfilme,333,thumb,'nao','')
                        except: pass
	proxima = re.compile('<a class="next page-numbers" href="(.+?)">').findall(html_source)		
	try:
                addDir1('','','',iconimage,False,'')
		addDir("Página Seguinte >>",proxima[0].replace('#038;',''),332,artfolder,'nao','')
        except:pass
	
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#

	
def ARM_abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

#----------------------------------------------------------------------------------------------------------------------------------------------#
              
def ARM_get_params():
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
	liz.setProperty('fanart_image',artfolder + 'flag.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addLink1(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'flag_brasil.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,checker,fanart):
        text = 'nnnnnn'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&checker="+urllib.quote_plus(checker)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'flag_brasil.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": text } )
        #cm = []
	#cm.append(('Sinopse', 'XBMC.Action(Info)'))
	#liz.addContextMenuItems(cm, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir1(name,url,mode,iconimage,folder,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'flag_brasil.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
        return ok


#----------------------------------------------------------------------------------------------------------------------------------------------#
	
params=ARM_get_params()
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


