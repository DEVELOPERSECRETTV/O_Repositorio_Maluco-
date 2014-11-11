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
        #addLink('link','http://89.238.150.212:8777/r4pynj3mnoie2cbd4p4l7dvaaawthhksjizymiwjsvzsn6cc2ur345a7cy/v.mp4.flv','')
        addDir1('[B][COLOR yellow]SITES[/COLOR][COLOR blue]dos[/COLOR][COLOR green]BRAZUCAS[/COLOR][/B][COLOR blue] - Menu Principal[/COLOR]','url',1005,artfolder + 'SDB.png',False,'')
        #----------------------------------------------------------------------
        addDir1('','url',1005,artfolder,False,'')
        #addDir('[B][COLOR yellow]ARMAGEDOM[/COLOR][COLOR green]FILMES[/COLOR][/B]','url',337,artfolder + 'SDB.png','nao','')
        #addDir('[B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].tv','http://megafilmeshd.tv',356,artfolder + 'SDB.png','nao','')
        #addDir('[B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].net','url',337,artfolder + 'SDB.png','nao','')
        #addDir('[B][COLOR green]MEGA[/COLOR][COLOR yellow]SÉRIESONLINEHD[/COLOR][/B].com','url',358,artfolder + 'SDB.png','nao','')
	addDir('[COLOR blue]Filmes - [/COLOR][B][COLOR yellow]ARMAGEDOM[/COLOR][COLOR green]FILMES[/COLOR][/B]','url',337,artfolder + 'SDB.png','nao','')
	addDir('[COLOR blue]Séries - [/COLOR][B][COLOR yellow]ARMAGEDOM[/COLOR][COLOR green]FILMES[/COLOR][/B]','http://www.armagedomfilmes.biz/?cat=21',332,artfolder + 'SDB.png','nao','')	
	addDir('[COLOR blue]Animação - [/COLOR][B][COLOR yellow]ARMAGEDOM[/COLOR][COLOR green]FILMES[/COLOR][/B]','http://www.armagedomfilmes.biz/?cat=3228',332,artfolder + 'SDB.png','nao','')
	addDir('[COLOR blue]Animes/Desenhos - [/COLOR][B][COLOR yellow]ARMAGEDOM[/COLOR][COLOR green]FILMES[/COLOR][/B]','http://www.armagedomfilmes.biz/?cat=36',332,artfolder + 'SDB.png','nao','')
        addDir('[COLOR blue]Categorias - [/COLOR][B][COLOR yellow]ARMAGEDOM[/COLOR][COLOR green]FILMES[/COLOR][/B]','http://www.armagedomfilmes.biz/',338,artfolder + 'SDB.png','nao','')
        addDir('Pesquisar - [B][COLOR yellow]ARMAGEDOM[/COLOR][COLOR green]FILMES[/COLOR][/B]','http://www.armagedomfilmes.biz/?s=',334,artfolder + 'PAGS2.png','nao','')
        #if selfAddon.getSetting('hide-porno') == "false":
			#addDir('[B][COLOR red]M+18 - [/COLOR][COLOR yellow]ARMAGEDOM[/COLOR][COLOR green]FILMES[/COLOR][/B]','http://www.megavideoporno.org/porno/filmes',350,artfolder + 'SDB.png','nao','')
        #----------------------------------------------------------------------
        addDir1('','url',1005,artfolder,False,'')
        addDir('[COLOR blue]Filmes - [/COLOR][B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].tv','http://megafilmeshd.tv/',356,artfolder + 'SDB.png','nao','')	
	addDir('[COLOR blue]Animação - [/COLOR][B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].tv','http://megafilmeshd.tv/category/animacao',349,artfolder + 'SDB.png','nao','')
	#addDir('[COLOR blue]Categorias - [/COLOR][B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].tv','http://megafilmeshd.tv/',349,artfolder + 'SDB.png','nao','')
	addDir('Pesquisar - [B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].tv','http://megafilmeshd.tv/?s-btn=Enviar&s=',334,artfolder + 'PAGS2.png','nao','')
	addDir1('','url',1005,artfolder,False,'')
        #----------------------------------------------------------------------
	addDir('[COLOR blue]Séries - [/COLOR][B][COLOR green]MEGA[/COLOR][COLOR yellow]SÉRIESONLINEHD[/COLOR][/B].com','url',358,artfolder + 'SDB.png','nao','')
	addDir('Pesquisar - [B][COLOR green]MEGA[/COLOR][COLOR yellow]SÉRIESONLINEHD[/COLOR][/B].com','http://megaseriesonlinehd.com/?s=',334,artfolder + 'PAGS2.png','nao','')
	#----------------------------------------------------------------------
        addDir1('','url',1005,artfolder,False,'')
        addDir('[COLOR blue]Filmes - [/COLOR][B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].net','url',337,artfolder + 'SDB.png','nao','')
	addDir('[COLOR blue]Séries - [/COLOR][B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].net','http://megafilmeshd.net/series/',360,artfolder + 'SDB.png','nao','')	
	addDir('[COLOR blue]Animação - [/COLOR][B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].net','http://megafilmeshd.net/category/animacao/',351,artfolder + 'SDB.png','nao','')
	addDir('[COLOR blue]Categorias - [/COLOR][B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].net','http://megafilmeshd.net/category/lancamentos/',352,artfolder + 'SDB.png','nao','')
	addDir('Pesquisar Filmes - [B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].net','http://megafilmeshd.net/?s=',334,artfolder + 'PAGS2.png','nao','')
	addDir('Pesquisar Séries - [B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].net','http://megafilmeshd.net/series/?pesquisaRapida=',334,artfolder + 'PAGS2.png','nao','')
        #----------------------------------------------------------------------
        addDir1('','url',1005,artfolder,False,'')
	#addDir('Pesquisar','url',1,artfolder + 'SDB.png','nao','')
	#addDir('[COLOR brown]ChangeLog[/COLOR]','http://o-repositorio-maluco.googlecode.com/svn/trunk/changelogs/changelog_TugaFilmesTV.txt',56,artfolder + 'SDB.png','nao','')
        #xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        #xbmc.executebuiltin('Container.SetViewMode(502)')
 
def ARM_Menu_Filmes():
        addDir1(name,'url',1005,artfolder + 'SDB.png',False,'')
        addDir1('','url',1005,artfolder,False,'')
        if name == '[COLOR blue]Filmes - [/COLOR][B][COLOR yellow]ARMAGEDOM[/COLOR][COLOR green]FILMES[/COLOR][/B]':
                addDir('[COLOR orange]Lançamentos[/COLOR]','http://www.armagedomfilmes.biz/?cat=3236',332,artfolder + 'SDB.png','nao','')
                addDir('[COLOR orange]Blu-Ray[/COLOR]','http://www.armagedomfilmes.biz/?cat=5529',332,artfolder + 'SDB.png','nao','')
                addDir('[COLOR orange]Legendados[/COLOR]','http://www.armagedomfilmes.biz/?s=legendado',332,artfolder + 'SDB.png','nao','')
        if name == '[COLOR blue]Filmes - [/COLOR][B][COLOR green]MEGA[/COLOR][COLOR yellow]FILMESHD[/COLOR][/B].net':
                addDir('[COLOR orange]Lançamentos[/COLOR]','http://megafilmeshd.net/category/lancamentos/',351,artfolder + 'SDB.png','nao','')
                addDir('[COLOR orange]Últimos[/COLOR]','http://megafilmeshd.net/ultimos',351,artfolder + 'SDB.png','nao','')

def ARM_Menu_Series():
        addDir1('[B][COLOR yellow]Menu Séries[/COLOR][/B]','url',1005,artfolder + 'SDB.png',False,'')
        addDir1('','url',1005,artfolder,False,'')
	addDir('[COLOR blue]A a Z[/COLOR]','url',341,artfolder + 'SDB.png','nao','')
        addDir('[COLOR blue]Recentes[/COLOR]','http://www.armagedomfilmes.biz/?cat=21',332,artfolder + 'SDB.png','nao','')
        addDir1('','url',1005,artfolder + 'SDB.png',False,'')
	#addDir('Pesquisar','http://www.tuga-filmes.tv/search?q=',1,artfolder + 'SDB.png','nao','')

def ARM_Menu_Series_MEGASERIESONLINEHD():
        addDir1('[B][COLOR yellow]Menu Séries[/COLOR][/B]','url',1005,artfolder + 'SDB.png',False,'')
        addDir1('','url',1005,artfolder,False,'')
	addDir('[COLOR blue]Lançamentos[/COLOR]','http://megaseriesonlinehd.com/index.php/category/series/seriados-lancamentos/',357,artfolder + 'SDB.png','nao','')
        addDir('[COLOR blue]Animes/Desenhos[/COLOR]','http://megaseriesonlinehd.com/index.php/category/desenhos/',357,artfolder + 'SDB.png','nao','')
        addDir('[COLOR blue]Atualizados[/COLOR]','http://megaseriesonlinehd.com',357,artfolder + 'SDB.png','nao','')
        addDir('[COLOR blue]Completos[/COLOR]','http://megaseriesonlinehd.com/index.php/page/2/',357,artfolder + 'SDB.png','nao','')
        addDir('[COLOR blue]Dublados[/COLOR]','http://megaseriesonlinehd.com/index.php/category/series/seriados-dublados/',357,artfolder + 'SDB.png','nao','')
        addDir('[COLOR blue]Legendados[/COLOR]','http://megaseriesonlinehd.com/index.php/category/series/seriados-legendados/',357,artfolder + 'SDB.png','nao','')
        addDir1('','url',1005,artfolder + 'SDB.png',False,'')



def ARM_Menu_Filmes_Por_Categorias():
        addDir1(name,'url',1005,artfolder + 'SDB.png',False,'')
        addDir1('','url',1005,artfolder,False,'')
        html_categorias_source = ARM_abrir_url(url)
	html_items_categorias = re.findall('<h2 class="widgettitle">Categorias</h2>(.*?)<div class="clear"></div>', html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                #filmes_por_categoria = re.compile('href="(.+?)"><b><span style="color: .+?">(.+?)</span>').findall(item_categorias)
                #for endereco_categoria,nome_categoria in filmes_por_categoria:
                        #if 'Assistir' not in nome_categoria and 'Adulto' not in nome_categoria and 'Programas' not in nome_categoria:
                                #addDir('[B][COLOR orange]' + nome_categoria + '[/COLOR][/B] ',endereco_categoria,332,artfolder + 'SDB.png','nao','')
                filmes_por_categoria = re.compile('<a href="(.+?)" title=".+?">(.+?)</a>').findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        addDir('[B][COLOR orange]' + nome_categoria + '[/COLOR][/B] ',endereco_categoria,332,artfolder + 'SDB.png','nao','')

def ARM_Menu_Filmes_Por_Categorias_MEGA_tv():
        addDir1(name,'url',1005,artfolder + 'SDB.png',False,'')
        addDir1('','url',1005,artfolder,False,'')
        try:
                html_categorias_source = ARM_abrir_url(url)
        except: html_categorias_source = ''
        html_items_categorias = re.findall("<div id='bluray-cat'>(.*?)</header><!-- Geral HEADER -->", html_categorias_source, re.DOTALL)
        if html_items_categorias:
                #addDir('[B][COLOR orange]Lançamentos[/COLOR][/B] ','http://megafilmeshd.tv',349,artfolder + 'SDB.png','nao','')
                addDir('[B][COLOR orange]Últimos Adicionados[/COLOR][/B] ','http://megafilmeshd.tv/',349,artfolder + 'SDB.png','nao','')
                for item_categorias in html_items_categorias:
                        filmes_por_categoria = re.compile("<h3><a href='(.+?)' title='.+?'>(.+?)</a></h3>").findall(item_categorias)
                        for endereco_categoria,nome_categoria in filmes_por_categoria:
                                addDir('[B][COLOR orange]' + nome_categoria + '[/COLOR][/B] ','http://megafilmeshd.tv'+endereco_categoria,349,artfolder + 'SDB.png','nao','')
                        for item_categorias in html_items_categorias:
                                filmes_por_categoria = re.compile('<li><a href="(.+?)" title=".+?">(.+?)</a></li>').findall(item_categorias)
                                for endereco_categoria,nome_categoria in filmes_por_categoria:
                                        addDir('[B][COLOR orange]' + nome_categoria + '[/COLOR][/B] ','http://megafilmeshd.tv'+endereco_categoria,349,artfolder + 'SDB.png','nao','')
        else:
                html_items_categorias = re.findall('<div class="menu">(.*?)</div><!--menu-->', html_categorias_source, re.DOTALL)
                if html_items_categorias:
                        for item_categorias in html_items_categorias:
                                filmes_por_categoria = re.compile('<li class=".+?"><a href="(.+?)">(.+?)</a></li>').findall(item_categorias)
                                for endereco_categoria,nome_categoria in filmes_por_categoria:
                                        if 'megafilmeshd.tv' not in nome_categoria: endereco_categoria = 'http://megafilmeshd.tv' + endereco_categoria
                                        if 'Home' in nome_categoria and len(endereco_categoria)>2: nome_categoria = 'Recentes'
                                        if 'Seriados' not in nome_categoria and 'animacao' not in nome_categoria and 'series' not in nome_categoria and 'Infantil' not in nome_categoria and 'Home' not in nome_categoria and 'blank' not in endereco_categoria:
                                                if 'ultimos' in nome_categoria:
                                                        nome_categoria = 'Últimos'
                                                        addDir('[B][COLOR orange]' + nome_categoria + '[/COLOR][/B] ',endereco_categoria,349,artfolder + 'SDB.png','nao','')
        #else:
        url_ = 'http://megafilmeshd.tv/category/animacao'
        try:
                html_categorias_source = ARM_abrir_url(url_)
        except: html_categorias_source = ''
        html_items_categorias = re.findall('<div id="header_centro_menu">(.*?)<div id="header_centro_busca">', html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile('href="(.+?)" target="_blank" title="(.+?)"').findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        if 'Home' in nome_categoria and len(endereco_categoria)>2: nome_categoria = 'Recentes'
                        if 'Seriados' not in nome_categoria and 'animacao' not in nome_categoria and 'series' not in nome_categoria and 'Infantil' not in nome_categoria and 'Home' not in nome_categoria and 'blank' not in endereco_categoria:
                                addDir('[B][COLOR orange]' + nome_categoria + '[/COLOR][/B] ',endereco_categoria,349,artfolder + 'SDB.png','nao','')
                filmes_por_categoria = re.compile('href="(.+?)" title="(.+?)"').findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        if 'Home' in nome_categoria and len(endereco_categoria)>2: nome_categoria = 'Recentes'
                        if 'Seriados' not in nome_categoria and 'animacao' not in nome_categoria and 'series' not in nome_categoria and 'Infantil' not in nome_categoria and 'Home' not in nome_categoria and 'blank' not in endereco_categoria:
                                addDir('[B][COLOR orange]' + nome_categoria + '[/COLOR][/B] ',endereco_categoria,349,artfolder + 'SDB.png','nao','')
        if not html_items_categorias:
                html_items_categorias = re.findall('<div class="styled-select">(.*?)</select>', html_categorias_source, re.DOTALL)
                for item_categorias in html_items_categorias:
                        filmes_por_categoria = re.compile('<option value="(.+?)" style=".+?">(.+?)</option>').findall(item_categorias)
                        for endereco_categoria,nome_categoria in filmes_por_categoria:
                                if 'Seriados' not in nome_categoria and 'animacao' not in nome_categoria and 'series' not in nome_categoria and 'Infantil' not in nome_categoria and 'Home' not in nome_categoria and 'blank' not in endereco_categoria:
                                        addDir('[B][COLOR orange]' + nome_categoria + '[/COLOR][/B] ',endereco_categoria,349,artfolder + 'SDB.png','nao','')
        
                

def ARM_Menu_Filmes_Por_Categorias_MEGA_net():
        addDir1(name,'url',1005,artfolder + 'SDB.png',False,'')
        addDir1('','url',1005,artfolder,False,'')
        html_categorias_source = ARM_abrir_url(url)
	html_items_categorias = re.findall('<li id="menu_genero">(.*?)<ul id="category-thumbs">', html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        if 'Lan\xc3\xa7amentos' not in nome_categoria and 'S\xc3\xa9ries' not in nome_categoria:
                                addDir('[B][COLOR orange]' + nome_categoria + '[/COLOR][/B] ',endereco_categoria,351,artfolder + 'SDB.png','nao','')

def ARM_Menu_Series_MEGA_net():
        addDir1(name,'url',1005,artfolder + 'SDB.png',False,'')
        addDir1('','url',1005,artfolder,False,'')
        addDir('[B][COLOR orange]Séries[/COLOR][/B]','http://megafilmeshd.net/series/',353,artfolder + 'SDB.png','nao','')
        addDir('[B][COLOR orange]Animes/Desenhos[/COLOR][/B]','http://megafilmeshd.net/series/',353,artfolder + 'SDB.png','nao','')


def ARM_pesquisar():
        nomes = name
	keyb = xbmc.Keyboard('', 'Escreva o parâmetro de pesquisa') #Chama o keyboard do XBMC com a frase indicada
	keyb.doModal() #Espera ate que seja confirmada uma determinada string
	if (keyb.isConfirmed()): #Se a entrada estiver confirmada (isto e, se carregar no OK)
		search = keyb.getText() #Variavel search fica definida com o conteudo do formulario
		parametro_pesquisa=urllib.quote(search) #parametro_pesquisa faz o quote da expressao search, isto é, escapa os parametros necessarios para ser incorporado num endereço url
		url_pesquisa = url + str(parametro_pesquisa)#+ '&x=0&y=0' #nova definicao de url. str força o parametro de pesquisa a ser uma string
                nome_pesquisa = str(parametro_pesquisa)
		#addDir1(url_pesquisa,'','',artfolder + 'SDB.png',False,'')
                if 'megaseriesonlinehd' in url_pesquisa: ARM_encontrar_fontes_filmes_MEGASERIESONLINEHD(url_pesquisa)
                if 'megafilmeshd.tv' in url_pesquisa: ARM_encontrar_fontes_filmes_MEGA_tv(url_pesquisa)
		if 'armagedom' in url_pesquisa: ARM_encontrar_fontes_filmes(url_pesquisa) #chama a função listar_videos com o url definido em cima
                if 'Filmes' in url or 'Series' in url: 
                        film_serie = re.compile('http://megafilmeshd.net/(.+?)/').findall(url)
                        if film_serie:
                                nomes = film_serie[0]
                                if nomes == 'Series': nomes = 'Séries'
                if 'megafilmeshd.net' in url_pesquisa and 'Filmes' in nomes: ARM_encontrar_fontes_filmes_pesquisa_MEGA_net('http://megafilmeshd.net/?s='+nome_pesquisa,nome_pesquisa) #chama a função listar_videos com o url definido em cima
                if 'megafilmeshd.net' in url_pesquisa and 'Séries' in nomes: ARM_encontrar_fontes_series_pesquisa_MEGA_net('http://megafilmeshd.net/series/',nome_pesquisa) #chama a função listar_videos com o url definido em cima


#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#

		

def ARM_encontrar_fontes_filmes(url):        
	try:
		html_source = ARM_abrir_url(url)
	except: html_source = ''
	items = re.findall('<div class="titulo-post-us">(.*?)<div class="div-us">', html_source, re.DOTALL)
	#addDir1(str(len(items)),'','',iconimage,False,'')
	duble = ''
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
                                                nome = nome.replace(' '+str(q_a_q_a),'')
                                                ano = ' ('+str(q_a_q_a)+')'
                        else: ano = ''
                        if 'Legendado' in nome and 'Dublado' in nome: dubleg = ' - (Legendado/Dublado)'
                        if 'Legendado' in nome and 'Dublado' not in nome: dubleg = ' - (Legendado)'
                        if 'Legendado' not in nome and 'Dublado' in nome: dubleg = ' - (Dublado)'
                        if 'Legendado' not in nome and 'Dublado' not in nome: dubleg = ''
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
                                addDir('[B][COLOR yellow]' + nome + '[/COLOR][COLOR blue][/B]' + ano + '[/COLOR][COLOR green]' + dubleg + '[/COLOR]',urlfilme,333,thumb,'nao','')
                        except: pass
	proxima = re.compile('<link rel="next" href="(.+?)"/>').findall(html_source)		
	try:
                #addDir1('','url',1005,artfolder + 'SDB.png',False,'')
		addDir("Página Seguinte >>",proxima[0].replace('#038;',''),332,artfolder + 'PAGS2.png','nao','')
        except:pass

def ARM_encontrar_fontes_filmes_MEGASERIESONLINEHD(url):        
	try:
		html_source = ARM_abrir_url(url)
	except: html_source = ''
	if url == 'http://megaseriesonlinehd.com':
                atualizados = re.findall("Seriados Atualizados</h4>(.*?)<span class='pages'>", html_source, re.DOTALL)
                items = re.findall('<div class="title-serie">(.*?)class="link-series">', atualizados[0], re.DOTALL)
        else: items = re.findall('<div class="title-serie">(.*?)class="link-series">', html_source, re.DOTALL)
	ano = ''
	dubleg = ''
	#addDir1(str(len(items)),'','',iconimage,False,'')
	if items != []:
		print len(items)
		for item in items:
                        titulo = re.compile('title="(.+?)Todas(.+?)"').findall(item)
                        #if not titulo: titulo = re.compile('title="(.+?)Todas').findall(item)
                        if titulo:
                                nome = titulo[0][0]
                                if 'Legendado' in titulo[0][1] and 'Dublado' in titulo[0][1]: dubleg = '(Legendado/Dublado)'
                                if 'Legendado' in titulo[0][1] and 'Dublado' not in titulo[0][1]: dubleg = '(Legendado)'
                                if 'Legendado' not in titulo[0][1] and 'Dublado' in titulo[0][1]: dubleg = '(Dublado)'
                                if 'Legendado' not in titulo[0][1] and 'Dublado' not in titulo[0][1]: dubleg = ''
                        else:
                                titulo = re.compile('title="(.+?)"').findall(item)
                                nome = titulo[0]
                        urldofilme = re.compile('href="(.+?)"').findall(item)
                        if urldofilme:
                                urlfilme = urldofilme[0]
                        else:
                                urlfilme = ''
                        thumbnail = re.compile('src="(.+?)"').findall(item)
                        if thumbnail: thumb = thumbnail[0]
                        else: thumb = ''
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8230;',"...")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('#038;','')
                        try:
                                addDir('[B][COLOR yellow]' + nome + '[/COLOR][/B][COLOR green] ' + dubleg + '[/COLOR]',urlfilme,359,thumb,'nao','')
                        except: pass
	proxima = re.compile('<a class="nextpostslink" rel="next" href="(.+?)">&raquo;</a>').findall(html_source)		
	try:
                #addDir1('','','',iconimage,False,'')
		addDir("Página Seguinte >>",proxima[0].replace('amp;',''),357,artfolder + 'PAGS2.png','nao','')
        except:pass


def ARM_encontrar_fontes_filmes_MEGA_tv(url):        
	try:
		html_source = ARM_abrir_url(url)
	except: html_source = ''
	if url == 'http://megafilmeshd.tv/':
                atualizados = re.findall('<div id="bloco_ult">(.*?)<div id="rodape">', html_source, re.DOTALL)
                items = re.findall('<h2 class="titulo">(.*?)width="190" height="294"/>', atualizados[0], re.DOTALL)
        else:
                items = re.findall('<h2 class="titulo">(.*?)width="190" height="294"/>', html_source, re.DOTALL)
	if not items: items = re.findall('<li class="create-tooltip"(.*?)</li>', html_source, re.DOTALL)
	#addDir1(str(len(items)),'','',iconimage,False,'')
	dubleg = ''
	if items != []:
		print len(items)
		for item in items:
                        titulo = re.compile('alt="(.+?)"').findall(item)
                        if titulo:
                                nome = titulo[0].replace('720p','').replace('1080p','')
                        else:
                                nome = ''
                        urldofilme = re.compile('href="(.+?)" class="assistir"></a>').findall(item)
                        if urldofilme:
                                urlfilme = urldofilme[0]
                        else:
                                urlfilme = ''
                        thumbnail = re.compile('src="(.+?)&amp;h=259&amp;w=177"').findall(item)
                        if not thumbnail: thumbnail = re.compile('src="(.+?)"').findall(item)
                        if thumbnail: thumb = thumbnail[0].replace('http://static.filmesonlinegratis.net/thumb.php?src=','')
                        else: thumb = ''
                        if 'Legendado' not in nome and 'Dublado' not in nome: dubleg = ''
                        if ' Dublado ou Legendado' in nome:
                                nome = nome.replace(' Dublado ou Legendado','')
                                dubleg = '(Legendado/Dublado)'
                        if ' Dublado e Legendado &#8211;' in nome:
                                nome = nome.replace(' Dublado e Legendado &#8211;','')
                                dubleg = '(Legendado/Dublado)'
                        if ' Dublado e Legendado' in nome:
                                nome = nome.replace(' Dublado e Legendado','')
                                dubleg = '(Legendado/Dublado)'
                        if ' Online' in nome: nome = nome.replace(' Online','')
                        if ' Dublado' in nome:
                                nome = nome.replace(' Dublado','')
                                dubleg = '(Dublado)'
                        if ' Legendado' in nome:
                                nome = nome.replace(' Legendado','')
                                dubleg = '(Legendado)'
                        
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8230;',"...")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('#038;','')
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        if qq_aa:
                                for q_a_q_a in qq_aa:
                                        if len(q_a_q_a) == 4:
                                                nome = nome.replace(' '+str(q_a_q_a),'')
                                                ano = ' ('+str(q_a_q_a)+')'                                                
                        else: ano = ''
                        try:
                                addDir('[B][COLOR yellow]' + nome + '[/COLOR][/B][COLOR blue]' + ano + '[/COLOR][COLOR green] - ' + dubleg + '[/COLOR]',urlfilme,333,thumb,'nao','')
                        except: pass
	proxima = re.compile('<a class="nextpostslink" rel="next" href="(.+?)">»</a>').findall(html_source)		
	try:
                #addDir1('','url',1005,artfolder + 'SDB.png',False,'')
		addDir("Página Seguinte >>",proxima[0].replace('amp;',''),349,artfolder + 'PAGS2.png','nao','')
        except:pass


def ARM_encontrar_fontes_filmes_MEGA_net(url):        
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
                                addDir('[B][COLOR yellow]' + nome + '[/COLOR][COLOR green] (' + ano_filme + ')[/COLOR][/B]',urlfilme,354,thumb,'nao','')
                        except: pass
	proxima = re.compile('<a class="nextpostslink" rel="next" href="(.+?)">></a>').findall(html_source)		
	try:
                #addDir1('','url',1005,artfolder + 'SDB.png',False,'')
		addDir("Página Seguinte >>",proxima[0].replace('#038;',''),351,artfolder + 'PAGS2.png','nao','')
        except:pass

def ARM_encontrar_fontes_filmes_pesquisa_MEGA_net(url,nome_pesquisa):
	try:
		html_source = ARM_abrir_url(url)
	except: html_source = ''
	num_f = 0
	items = re.findall('<li class="tooltip"(.*?)</li>', html_source, re.DOTALL)
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
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8230;',"...")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('#038;','')
                        try:
                                num_f = num_f + 1
                                addDir('[B][COLOR yellow]' + nome + '[/COLOR][/B]',urlfilme,354,thumb,'nao','')
                        except: pass
	if num_f == 0: addDir1('[B][COLOR red]- No Match Found -[/COLOR][/B]','url',1005,'',False,'')
	proxima = re.compile('<a class="nextpostslink" href="(.+?)">></a>').findall(html_source)
	if proxima:
                try:
                        html_source = ARM_abrir_url(proxima[0].replace('#038;',''))
                except: html_source = ''
                num_f = 0
                items = re.findall('<li class="tooltip"(.*?)</li>', html_source, re.DOTALL)
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
                                nome = nome.replace('&#8217;',"'")
                                nome = nome.replace('&#8230;',"...")
                                nome = nome.replace('&#8211;',"-")
                                nome = nome.replace('#038;','')
                                try:
                                        num_f = num_f + 1
                                        addDir('[B][COLOR yellow]' + nome + '[/COLOR][/B]',urlfilme,354,thumb,'nao','')
                                except: pass


def ARM_encontrar_fontes_series_MEGA_net(url):
        #return
	try:
		html_source = ARM_abrir_url(url)
	except: html_source = ''
	if name == '[B][COLOR orange]Séries[/COLOR][/B]': items_series = re.findall('<div id="listagem-series">(.*?)<!--/listagem-series-->', html_source, re.DOTALL)
	if name == '[B][COLOR orange]Animes/Desenhos[/COLOR][/B]': items_series = re.findall('<div id="listagem-animmes">(.*?)<!--/listagem-animmes-->', html_source, re.DOTALL)
	items = re.findall('<div class="search tooltip box-video"(.*?)</a></div>', items_series[0], re.DOTALL)
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
                                if 'megafilmeshd' not in urlthumb[0][0]: urlfilme = 'http://megafilmeshd.net/series/' + urlthumb[0][0]
                                else: urlfilme = urlthumb[0][0]
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
                                addDir('[B][COLOR yellow]' + nome + '[/COLOR][COLOR green] (' + ano_filme + ')[/COLOR][/B]',urlfilme,354,thumb,'nao','')
                        except: pass
	proxima = re.compile('<a class="nextpostslink"  rel="next" href="(.+?)">></a>').findall(html_source)		
	try:
                #addDir1('','url',1005,artfolder + 'SDB.png',False,'')
		addDir("Página Seguinte >>",proxima[0].replace('#038;',''),351,artfolder + 'PAGS2.png','nao','')
        except:pass

def ARM_encontrar_fontes_series_pesquisa_MEGA_net(url,nome_pesquisa):
	try:
		html_source = ARM_abrir_url(url)
	except: html_source = ''
	num_f = 0
	items = re.findall('<div class="search tooltip box-video"(.*?)/></a></div>', html_source, re.DOTALL)
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
                                nome_capwords = nome.lower()
                                if nome_pesquisa.lower() in nome_capwords:
                                        num_f = num_f + 1
                                        addDir('[B][COLOR yellow] - ' + nome + '[/COLOR][COLOR green] (' + ano_filme + ')[/COLOR][/B]',urlfilme,354,thumb,'nao','')
                        except: pass



#----------------------------------------------------------------------------------------------------------------------------------------------#

def ARM_encontrar_videos_filmes(name,url):
        num_fonte = 0
	addDir1(name,'url',1005,iconimage,False,'')
        addDir1('','url',1005,artfolder,False,'')
	try:
		link2=ARM_abrir_url(url)
	except: link2 = '' 
	if link2:
                if 'ASSISTIR: LEGENDADO' in link2: addDir1('[COLOR orange]Dublado:[/COLOR]','','',iconimage,False,'')
                urls_video = re.findall('<div id="ver-filme-user">(.*?)<div id="box-embed"', link2, re.DOTALL)
                if urls_video:
                        urlss_video = re.compile('src="(.+?)"').findall(urls_video[0])
                        if urlss_video:
                                for url_video in urlss_video:
                                        #addDir1(url_video,'','',iconimage,False,'')
                                        id_video = re.compile('id=(.*)').findall(url_video)
                                        if id_video: id_video = id_video[0]
                                        else: id_video = ''
                                        num_fonte = num_fonte + 1
                                        if 'video.tt' not in url_video: ARM_resolve_not_videomega_filmes(url_video,id_video,num_fonte)
                                        if 'video.tt' in url_video: ARM_resolve_not_videomega_filmes_telecine(url_video,id_video,num_fonte)
                        urlss_video = re.compile('SRC="(.+?)"').findall(urls_video[0])
                        if urlss_video:
                                for url_video in urlss_video:
                                        id_video = re.compile('id=(.*)').findall(url_video)
                                        if id_video: id_video = id_video[0]
                                        else: id_video = ''
                                        num_fonte = num_fonte + 1
                                        if 'video.tt' not in url_video: ARM_resolve_not_videomega_filmes(url_video,id_video,num_fonte)
                                        if 'video.tt' in url_video: ARM_resolve_not_videomega_filmes_telecine(url_video,id_video,num_fonte)
                        if 'telecinemajestic' in link2:
                                linktelecine = re.compile('href="http://telecinemajestic(.+?)"').findall(link2)
                                if linktelecine: telelink = 'http://telecinemajestic' + linktelecine[0]
                                try:
                                        telecine = ARM_abrir_url(telelink)
                                except: telecine = ''
                                if telecine:
                                        telemajestic = re.findall('id="conteudo-filmes">(.*?)</iframe></div><div><object', telecine, re.DOTALL)
                                        urlss_video = re.compile('SRC="(.+?)"').findall(telemajestic[0])
                                        if urlss_video:
                                                for url_video in urlss_video:
                                                        id_video = ''
                                                        num_fonte = num_fonte + 1
                                                        ARM_resolve_not_videomega_filmes_telecine(url_video,id_video,num_fonte)
                                        urlss_video = re.compile('src="(.+?)"').findall(telemajestic[0])
                                        if urlss_video:
                                                for url_video in urlss_video:
                                                        id_video = ''
                                                        num_fonte = num_fonte + 1
                                                        ARM_resolve_not_videomega_filmes_telecine(url_video,id_video,num_fonte)
                        if 'efilmesnarede' in link2:
                                linktelecine = re.compile('href="http://efilmesnarede(.+?)"').findall(link2)
                                if linktelecine: telelink = 'http://efilmesnarede' + linktelecine[0]
                                try:
                                        telecine = ARM_abrir_url(telelink)
                                except: telecine = ''
                                if telecine:
                                        telemajestic = re.findall('id="conteudo-filmes">(.*?)</iframe></div><div><object', telecine, re.DOTALL)
                                        urlss_video = re.compile('SRC="(.+?)"').findall(telemajestic[0])
                                        if urlss_video:
                                                for url_video in urlss_video:
                                                        id_video = ''
                                                        num_fonte = num_fonte + 1
                                                        ARM_resolve_not_videomega_filmes_telecine(url_video,id_video,num_fonte)
                                        urlss_video = re.compile('src="(.+?)"').findall(telemajestic[0])
                                        if urlss_video:
                                                for url_video in urlss_video:
                                                        id_video = ''
                                                        num_fonte = num_fonte + 1
                                                        ARM_resolve_not_videomega_filmes_telecine(url_video,id_video,num_fonte)
                if 'ASSISTIR: LEGENDADO' in link2:
                        num_fonte = 0
                        addDir1('[COLOR orange]Legendado:[/COLOR]','','',iconimage,False,'')
                        matchvideo = re.findall('<p style="text-align: center;">(.*?)<center><a href="https://twitter.com/share"', link2, re.DOTALL)
                        if matchvideo:
                                for match in matchvideo:
                                        urls_video = re.compile('href="(.+?)"').findall(match)
                                        if urls_video:
                                                for url_video in urls_video:                                                        
                                                        if 'telecinemajestic' in url_video:
                                                                try:
                                                                        telecine = ARM_abrir_url(url_video)
                                                                except: telecine = ''
                                                                if telecine:
                                                                        telemajestic = re.findall('</iframe></div><div><object(.*?)class="titulo-bloco">', telecine, re.DOTALL)
                                                                        urlss_video = re.compile('SRC="(.+?)"').findall(telemajestic[0])
                                                                        if urlss_video:
                                                                                for url_video in urlss_video:
                                                                                        id_video = ''
                                                                                        num_fonte = num_fonte + 1
                                                                                        ARM_resolve_not_videomega_filmes_telecine(url_video,id_video,num_fonte)
                                                                        urlss_video = re.compile('src="(.+?)"').findall(telemajestic[0])
                                                                        if urlss_video:
                                                                                for url_video in urlss_video:
                                                                                        id_video = ''
                                                                                        num_fonte = num_fonte + 1
                                                                                        ARM_resolve_not_videomega_filmes_telecine(url_video,id_video,num_fonte)
                                                        else:
                                                                id_video = re.compile('id=(.*)').findall(url_video)
                                                                if id_video: id_video = id_video[0]
                                                                else: id_video = ''
                                                                num_fonte = num_fonte + 1
                                                                ARM_resolve_not_videomega_filmes(url_video,id_video,num_fonte)
                                                        if 'efilmesnarede' in url_video:
                                                                try:
                                                                        telecine = ARM_abrir_url(url_video)
                                                                except: telecine = ''
                                                                if telecine:
                                                                        telemajestic = re.findall('</iframe></div><div><object(.*?)class="titulo-bloco">', telecine, re.DOTALL)
                                                                        urlss_video = re.compile('SRC="(.+?)"').findall(telemajestic[0])
                                                                        if urlss_video:
                                                                                for url_video in urlss_video:
                                                                                        id_video = ''
                                                                                        num_fonte = num_fonte + 1
                                                                                        ARM_resolve_not_videomega_filmes_telecine(url_video,id_video,num_fonte)
                                                                        urlss_video = re.compile('src="(.+?)"').findall(telemajestic[0])
                                                                        if urlss_video:
                                                                                for url_video in urlss_video:
                                                                                        id_video = ''
                                                                                        num_fonte = num_fonte + 1
                                                                                        ARM_resolve_not_videomega_filmes_telecine(url_video,id_video,num_fonte)
                                                        else:
                                                                id_video = re.compile('id=(.*)').findall(url_video)
                                                                if id_video: id_video = id_video[0]
                                                                else: id_video = ''
                                                                num_fonte = num_fonte + 1
                                                                ARM_resolve_not_videomega_filmes(url_video,id_video,num_fonte)
                if 'Temporada' in link2 or 'TEMPORADA' in link2 or 'Epis' in link2:
                        #addDir('ca estou','',342,iconimage,'','')
                        i = 0
                        num_temporada = 1
                        ep = 1
                        legdub = ""
                        ultimoadicionado = ''
                        num_epi = ''
                        matchvideo = re.findall('<div id="HOTWordsTxt" name="HOTWordsTxt">(.+?)<a href="https://twitter.com/share"',link2,re.DOTALL)
                        if not matchvideo: matchvideo = re.findall('<div id="HOTWordsTxt" name="HOTWordsTxt">(.+?)<div class="geral-extra">',link2,re.DOTALL)
                        if matchvideo:
                                #addDir('ca estou eu','',342,iconimage,'','')
                                #return
                                for parte1 in matchvideo:
                                        matchvideolink = re.compile('<iframe src="(.+?)"').findall(parte1)
					if matchvideolink:
                                                #addDir('ca estou eu 1','',342,iconimage,'','')
                                                #return
                                                for url_video in matchvideolink:
                                                        id_video = re.compile('id=(.*)').findall(url_video)
                                                        if id_video: id_video = id_video[0]
                                                        else: id_video = ''
                                                        num_fonte = num_fonte + 1
                                                        #epi = epi.replace('&#8211;',"-").replace('>ASSISTIR','')
                                                        #epi = epi.replace('>Assistir','')
                                                        #addDir('[B]'+epi+'[/B]','',342,iconimage,'','')
                                        #return
                                        matchvideolink = re.compile('<a href="(.+?)".+?target="_blank">(.+?)</a>').findall(parte1)
                                        if matchvideolink:
                                                for videolink,numepi in matchvideolink:
                                                        if '<span' in numepi:
                                                                renumepi = re.compile('<span style="color:.+?">(.*)').findall(numepi)
                                                                numepi = renumepi[0]
                                                        epi = re.compile('dio(.*)').findall(numepi)
                                                        if not epi: epi = re.compile('DIO(.*)').findall(numepi)
                                                        if epi: epinum = epi[0]
                                                        else: epinum = ''
                                                        if '/span' in epinum or '/strong' in epinum:
                                                                a_q = re.compile('\d+')
                                                                epin = a_q.findall(epinum)
                                                                epinum = ''
                                                                for num in epin:
                                                                        epinum = epinum + str(num)
                                                        if 'Temporada' in link2 or 'TEMPORADA' in link2:
                                                                if len(epinum)<7:
                                                                        ultimoadicionado = ''
                                                                        if '00' in epinum or '01' in epinum:
                                                                                if '00' in epinum and '00' not in num_epi:
                                                                                        addDir1('[COLOR blue]'+str(num_temporada)+'ª Temporada[/COLOR]','','',iconimage,False,'')
                                                                                        num_temporada = num_temporada + 1
                                                                                        ep = 0
                                                                                if '01' in epinum and '00' not in num_epi and '01' not in num_epi:
                                                                                        addDir1('[COLOR blue]'+str(num_temporada)+'ª Temporada[/COLOR]','','',iconimage,False,'')
                                                                                        num_temporada = num_temporada + 1
                                                                                        ep = 0
                                                                        num_epi = epinum
                                                                else: ultimoadicionado = '[COLOR blue](NOVO)[/COLOR]'
                                                        if 'dublado' in videolink or 'dubldo' in videolink: legdub = '(DUBLADO)'
                                                        else: legdub = '(LEGENDADO)'
                                                        #if 'dubldo' in videolink: legdub = '(DUBLADO)'
                                                        #else: legdub = '(LEGENDADO)'
                                                        #if 'legendado' in videolink: legdub = '(LEGENDADO)'
                                                        if 'download' not in videolink: addDir(ultimoadicionado+'[COLOR orange]- Épisódio '+str(epinum)+'[/COLOR] '+legdub,videolink,342,iconimage,'','')
                if 'Coleção' in link2 and not 'TEMPORADA' in link2 and not 'Temporada' in link2:
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
                if 'megafilmeshd.tv' in url:
                        id_video = ''
                        matchvideo = re.findall('<li id=".+?" class="box-temp">(.*?)</li>', link2, re.DOTALL)
                        if not matchvideo: matchvideo = re.findall('<li id=".+?">(.*?)</li>', link2, re.DOTALL)
                        #addDir1(str(len(matchvideo)),'','',iconimage,False,'')
                        if matchvideo:
                                for vidlink in matchvideo:
                                        #addDir1(vidlink,'','',iconimage,False,'')
                                        if 'megafilmes' in vidlink:
                                        #if '/ads/' not in vidlink and 'megafilmes' in vidlink and '<span' not in vidlink:
                                                linkvmatch = re.compile('src="(.+?)"').findall(vidlink)
                                                if linkvmatch:
                                                        #addDir1(linkvmatch[0],'','',iconimage,False,'')
                                                        try:
                                                                link2=ARM_abrir_url(linkvmatch[0])
                                                        except: link2 = ''
                                                        vlink = re.findall('<iframe(.*?)</iframe>', link2, re.DOTALL)
                                                        
                                                        for vidurl in vlink:
                                                                linkinho=vidurl
                                                        #if vlink: addDir1(str(len(vlink))+'----'+linkinho,'','',iconimage,False,'')
                                                        linkv = re.compile('src="(.+?)"').findall(linkinho)
                                                        if linkv:
                                                                if 'adsnewflut' not in linkv: url_video = linkv[0]
                                                        else: url_video = ''
                                                        #addDir1(url_video+'----','','',iconimage,False,'')
                                                        if url_video == '':
                                                                linkv = re.compile("src='(.+?)'").findall(linkinho)
                                                                if linkv:
                                                                        if 'adsnewflut' not in linkv: url_video = linkv[0]
                                                                else: url_video = ''
                                                        vlink = re.findall('<embed(.*?)</object>', link2, re.DOTALL)
                                                        if vlink: linkv = re.compile('src="(.+?)"').findall(vlink[0])
                                                        if linkv: url_video = linkv[0]
                                                        #addDir1(url_video+'----','','',iconimage,False,'')
                                                        if 'adsnewflut' not in url_video: num_fonte = num_fonte + 1
                                                        if 'flashx.tv' not in url_video: ARM_resolve_not_videomega_filmes_telecine(url_video,id_video,num_fonte)                                            
                                                        else:
                                                                try:
                                                                        funciona = ''
                                                                        try:
                                                                                flashxtv=ARM_abrir_url(url_video)
                                                                        except: flashxtv = ''
                                                                        flashurl = re.compile('addthis:url="(.+?)" addthis:').findall(flashxtv)
                                                                        if flashurl:
                                                                                url = flashurl[0]
                                                                                url = url + '///' + name
                                                                        else:
                                                                                url = url + '///' + name
                                                                                funciona = '[COLOR red] - Sem link[/COLOR]'
                                                                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](FlashX.tv)[/COLOR][/B]'+funciona,url,30,iconimage,'','')
                                                                except:pass
                                                                #url_video = url_video + '///' + name
                                                                #addDir(url_video+'[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](FlashX.tv)[/COLOR][/B]',url_video,30,iconimage,'','')
                                        else:
                                                if '/ads/' not in vidlink and '<span' not in vidlink:
                                                        linkvmatch = re.compile('src="(.+?)"').findall(vidlink)
                                                        if linkvmatch:
                                                                #addDir1(linkvmatch[0],'','',iconimage,False,'')
                                                                num_fonte = num_fonte + 1
                                                                url_video = linkvmatch[0]
                                                                ARM_resolve_not_videomega_filmes_telecine(url_video,id_video,num_fonte)
                                                
                        else:
                                matchvideo = re.findall('<div class="btn-ver">(.*?)</div>', link2, re.DOTALL)
                                #addDir1(str(len(matchvideo)),'','',iconimage,False,'')
                                if matchvideo:
                                        linkvmatch = re.compile('href="(.+?)"').findall(matchvideo[0])
                                        #addDir1(linkvmatch[0],'','',iconimage,False,'')
                                        try:
                                                link2=ARM_abrir_url(linkvmatch[0])
                                        except: link2 = ''
                                        matchdeo = re.findall('<div class="player">(.*?)</div>', link2, re.DOTALL)
                                        if matchdeo:
                                                linkmatch = re.compile('href="(.+?)"').findall(matchdeo[0])
                                                for vidlink in linkmatch:
                                                        #addDir1(vidlink,'','',iconimage,False,'')
                                                        try:
                                                                link2=ARM_abrir_url(vidlink)
                                                        except: link2 = ''
                                                        linkvmatch = re.compile('src="(.+?)"').findall(link2)
                                                        if '/ads/' not in linkvmatch[0]:
                                                                if linkvmatch:
                                                                        #addDir1(linkvmatch[0],'','',iconimage,False,'')
                                                                        try:
                                                                                link2=ARM_abrir_url(linkvmatch[0])
                                                                        except: link2 = ''
                                                                        vlink = re.findall('<iframe(.*?)</iframe>', link2, re.DOTALL)
                                                                        for vidurl in vlink:
                                                                                linkinho=vidurl
                                                                        #addDir1(linkinho,'','',iconimage,False,'')
                                                                        linkv = re.compile('src="(.+?)"').findall(linkinho)
                                                                        if linkv:
                                                                                if 'adsnewflut' not in linkv: url_video = linkv[0]
                                                                        else: url_video = ''
                                                                        if url_video == '':
                                                                                linkv = re.compile("src='(.+?)'").findall(linkinho)
                                                                                if linkv:
                                                                                        if 'adsnewflut' not in linkv: url_video = linkv[0]
                                                                                else: url_video = ''
                                                                        #addDir1(url_video+'--','','',iconimage,False,'')
                                                                        vlink = re.findall('<embed(.*?)</object>', link2, re.DOTALL)
                                                                        if vlink: linkv = re.compile('src="(.+?)"').findall(vlink[0])
                                                                        if linkv: url_video = linkv[0]
                                                                        #addDir1(url_video+'----','','',iconimage,False,'')
                                                                        if 'adsnewflut' not in url_video: num_fonte = num_fonte + 1
                                                                        if 'flashx.tv' not in url_video: ARM_resolve_not_videomega_filmes_telecine(url_video,id_video,num_fonte)                                            
                                                                        else:
                                                                                try:
                                                                                        funciona = ''
                                                                                        try:
                                                                                                flashxtv=ARM_abrir_url(url_video)
                                                                                        except: flashxtv = ''
                                                                                        flashurl = re.compile('addthis:url="(.+?)" addthis:').findall(flashxtv)
                                                                                        if flashurl:
                                                                                                url = flashurl[0]
                                                                                                url = url + '///' + name
                                                                                        else:
                                                                                                url = url + '///' + name
                                                                                                funciona = '[COLOR red] - Sem link[/COLOR]'
                                                                                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](FlashX.tv)[/COLOR][/B]'+funciona,url,30,iconimage,'','')
                                                                                except:pass
                                                                                #url_video = url_video + '///' + name
                                                                                #addDir(url_video+'[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](FlashX.tv)[/COLOR][/B]',url_video,30,iconimage,'','')
                                else:
                                        matchvideo = re.findall('<div class="btn-ver">(.*?)</div>', link2, re.DOTALL)
                                        #addDir1(str(len(matchvideo)),'','',iconimage,False,'')
                                        #if matchvideo:
                                                
def ARM_encontrar_videos_filmes_MEGASERIESONLINEHD(name,url):
        num_fonte = 0
	addDir1(name,'url',1005,iconimage,False,'')
        addDir1('','url',1005,artfolder,False,'')
	try:
		link2=ARM_abrir_url(url)
	except: link2 = '' 
	if link2:
                partes = re.findall('<ul id="series-player">(.*?)POSTAGENS',link2,re.DOTALL)
                matchvideo = re.findall('an>(.*?)<sp',partes[0],re.DOTALL)
                if matchvideo:
                        for parte in matchvideo:
                                #ultima = re.compile('=(.*)').findall(url)
                                #if ultima: last = ultima[0]
                                temporada = re.compile('(.+?)</span>').findall(parte)
                                for temp in temporada:
                                        if 'final' not in temporada[0].lower():
                                                addDir1('[B][COLOR blue]'+temporada[0].replace('<p>','')+' :[/COLOR][/B]','','',iconimage,False,'')
                                urletitulo = re.compile('href="(.+?)">(.+?)</a>').findall(parte)
                                for url, titulo in urletitulo:
                                        addDir('[COLOR orange]'+titulo+'[/COLOR]',url,342,iconimage,'','')
                #ultimaserie = last + '">' + titulo
                #matchvideo = re.findall(ultimaserie+'(.*?)</ul><!--series player -->',partes[0],re.DOTALL)
                #if matchvideo:
                        #for parte in matchvideo:
                                #temporada = re.compile('(.+?)</span>').findall(parte)
                                #for temp in temporada:
                                        #if 'final' not in temp.lower():
                                                #addDir1('[B][COLOR blue]'+temp.replace('<span>','')+' :[/COLOR][/B]','','',iconimage,False,'')
                                #urletitulo = re.compile('href="(.+?)">(.+?)</a>').findall(parte)
                                #for url, titulo in urletitulo:
                                        #addDir('[COLOR orange]'+titulo+'[/COLOR]',url,342,iconimage,'','')

                                                
def ARM_encontrar_videos_filmes_MEGA_NET(name,url):
        num_fonte = 0
	addDir1(name,'url',1005,iconimage,False,'')
        addDir1('','url',1005,artfolder,False,'')
	try:
		link2=ARM_abrir_url(url)
	except: link2 = '' 
	if link2:
                if 'id="xmain"' in link2 or '<p class="ntemp">' in link2:
                        partes = re.findall('id="xmain"(.+?)',link2,re.DOTALL)
                        num_partes = len(partes)
                        matchvideo = re.findall('JavaScript:(.*?)onclick="',link2,re.DOTALL)
                        #num_partes = len(matchvideo)
                        num_part = 0
                        if matchvideo:
                                for parte in matchvideo:
                                        num_part = num_part + 1
                                        temporada = re.compile('doMenu.+?;">(.+?)</a>').findall(parte)
                                        addDir1('[B][COLOR blue]'+temporada[0]+' :[/COLOR][/B]','','',iconimage,False,'')
                                        urletitulo = re.compile('<a class="video" href="(.+?)">(.+?)</a>').findall(parte)
                                        for url, titulo in urletitulo:
                                                ultima = re.compile('=(.*)').findall(url)
                                                if ultima: last = ultima[0]
                                                epis = re.compile('(.+?)-').findall(titulo)
                                                if epis:
                                                        episodio = epis[0]
                                                        tit = re.compile('-(.*)').findall(titulo)
                                                        title = '-' + tit[0]
                                                else:
                                                        episodio = titulo
                                                        title = ''
                                                addDir('[COLOR orange]'+episodio+'[/COLOR]'+title,url,342,iconimage,'','')
                                #addLink(str(num_part)+partes[0],'','')
                                ultimaserie = last + '">' + titulo
                                if num_partes > num_part:
                                        ntemp = re.findall('(.*?)<p class="ntemp">',link2,re.DOTALL)
                                        matchvideo = re.findall(ultimaserie+'(.*?)<p class="ntemp">',link2,re.DOTALL)
                                        #addLink(url+episodio+'  '+str(num_part)+'  '+str(len(matchvideo)),'','')
                                        num = 0
                                        if matchvideo:
                                                for parte in matchvideo:
                                                        if num == 0:
                                                                num = num + 1
                                                                temporada = re.compile('doMenu.+?;">(.+?)</a>').findall(parte)
                                                                addDir1('[B][COLOR blue]'+temporada[0]+' :[/COLOR][/B]','','',iconimage,False,'')
                                                                urletitulo = re.compile('<a class="video" href="(.+?)">(.+?)</a>').findall(parte)
                                                                for url, titulo in urletitulo:
                                                                        epis = re.compile('(.+?)-').findall(titulo)
                                                                        if epis:
                                                                                episodio = epis[0]
                                                                                tit = re.compile('-(.*)').findall(titulo)
                                                                                title = '-' + tit[0]
                                                                        else:
                                                                                episodio = titulo
                                                                                title = ''
                                                                        addDir('[COLOR orange]'+episodio+'[/COLOR]'+title,url,342,iconimage,'','')
                                        if len(ntemp) == 1:
                                                matchvideo = re.findall('<p class="ntemp">(.*?)href="http://twitter.com/share"',link2,re.DOTALL)
                                                if matchvideo:
                                                        for parte in matchvideo:
                                                                temporada = re.compile('(.+?)</p>').findall(parte)
                                                                addDir1('[B][COLOR blue]'+temporada[0]+' :[/COLOR][/B]','','',iconimage,False,'')
                                                                urletitulo = re.compile('href="(.+?)" class="video">(.+?)</a>').findall(parte)
                                                                if not urletitulo: urletitulo = re.compile('href="(.+?)">(.+?)</a>').findall(parte)
                                                                for url, titulo in urletitulo:
                                                                        epis = re.compile('(.+?)-').findall(titulo)
                                                                        if epis:
                                                                                episodio = epis[0]
                                                                                tit = re.compile('-(.*)').findall(titulo)
                                                                                title = '-' + tit[0]
                                                                        else:
                                                                                episodio = titulo
                                                                                title = ''
                                                                        addDir('[COLOR orange]'+episodio+'[/COLOR]'+title,url,342,iconimage,'','')
                                        if len(ntemp) > 1:
                                                matchvideo = re.findall('emp">(.*?)<p class="nt',link2,re.DOTALL)
                                                if matchvideo:
                                                        for parte in matchvideo:
                                                                temporada = re.compile('(.+?)</p>').findall(parte)
                                                                addDir1('[B][COLOR blue]'+temporada[0]+' :[/COLOR][/B]','','',iconimage,False,'')
                                                                urletitulo = re.compile('href="(.+?)" class="video">(.+?)</a>').findall(parte)
                                                                if not urletitulo:
                                                                        urletitulo = re.compile('href="(.+?)">(.+?)</a>').findall(parte)
                                                                        urltitulo_num = 1
                                                                else: urltitulo_num = 0
                                                                for url, titulo in urletitulo:
                                                                        ultima = re.compile('=(.*)').findall(url)
                                                                        if ultima: last = ultima[0]
                                                                        epis = re.compile('(.+?)-').findall(titulo)
                                                                        if epis:
                                                                                episodio = epis[0]
                                                                                tit = re.compile('-(.*)').findall(titulo)
                                                                                title = '-' + tit[0]
                                                                        else:
                                                                                episodio = titulo
                                                                                title = ''
                                                                        addDir('[COLOR orange]'+episodio+'[/COLOR]'+title,url,342,iconimage,'','')
                                                if urltitulo_num == 0: ultimaserie = last + '" class="video">' + titulo
                                                if urltitulo_num == 1: ultimaserie = last + '">' + titulo
                                                matchvideo = re.findall(ultimaserie+'(.*?)href="http://twitter.com/share"',link2,re.DOTALL)
                                                if matchvideo:
                                                        for parte in matchvideo:
                                                                temporada = re.compile('emp">(.+?)</p>').findall(parte)
                                                                addDir1('[B][COLOR blue]'+temporada[0]+' :[/COLOR][/B]','','',iconimage,False,'')
                                                                urletitulo = re.compile('href="(.+?)" class="video">(.+?)</a>').findall(parte)
                                                                if not urletitulo: urletitulo = re.compile('href="(.+?)">(.+?)</a>').findall(parte)
                                                                for url, titulo in urletitulo:
                                                                        epis = re.compile('(.+?)-').findall(titulo)
                                                                        if epis:
                                                                                episodio = epis[0]
                                                                                tit = re.compile('-(.*)').findall(titulo)
                                                                                title = '-' + tit[0]
                                                                        else:
                                                                                episodio = titulo
                                                                                title = ''
                                                                        addDir('[COLOR orange]'+episodio+'[/COLOR]'+title,url,342,iconimage,'','')
                        else:
                                ntemp = re.findall('(.*?)<p class="ntemp">',link2,re.DOTALL)
                                if ntemp:
                                        if len(ntemp) == 1:
                                                matchvideo = re.findall('<p class="ntemp">(.*?)href="http://twitter.com/share"',link2,re.DOTALL)
                                                if matchvideo:
                                                        for parte in matchvideo:
                                                                temporada = re.compile('(.+?)</p>').findall(parte)
                                                                addDir1('[B][COLOR blue]'+temporada[0]+' :[/COLOR][/B]','','',iconimage,False,'')
                                                                urletitulo = re.compile('href="(.+?)" class="video">(.+?)</a>').findall(parte)
                                                                if not urletitulo: urletitulo = re.compile('href="(.+?)">(.+?)</a>').findall(parte)
                                                                for url, titulo in urletitulo:
                                                                        epis = re.compile('(.+?)-').findall(titulo)
                                                                        if epis:
                                                                                episodio = epis[0]
                                                                                tit = re.compile('-(.*)').findall(titulo)
                                                                                title = '-' + tit[0]
                                                                        else:
                                                                                episodio = titulo
                                                                                title = ''
                                                                        addDir('[COLOR orange]'+episodio+'[/COLOR]'+title,url,342,iconimage,'','')
                                        if len(ntemp) > 1:
                                                matchvideo = re.findall('emp">(.*?)<p class="nt',link2,re.DOTALL)
                                                if matchvideo:
                                                        for parte in matchvideo:
                                                                temporada = re.compile('(.+?)</p>').findall(parte)
                                                                addDir1('[B][COLOR blue]'+temporada[0]+' :[/COLOR][/B]','','',iconimage,False,'')
                                                                urletitulo = re.compile('href="(.+?)" class="video">(.+?)</a>').findall(parte)
                                                                if not urletitulo:
                                                                        urletitulo = re.compile('href="(.+?)">(.+?)</a>').findall(parte)
                                                                        urltitulo_num = 1
                                                                else: urltitulo_num = 0
                                                                for url, titulo in urletitulo:
                                                                        ultima = re.compile('=(.*)').findall(url)
                                                                        if ultima: last = ultima[0]
                                                                        epis = re.compile('(.+?)-').findall(titulo)
                                                                        if epis:
                                                                                episodio = epis[0]
                                                                                tit = re.compile('-(.*)').findall(titulo)
                                                                                title = '-' + tit[0]
                                                                        else:
                                                                                episodio = titulo
                                                                                title = ''
                                                                        addDir('[COLOR orange]'+episodio+'[/COLOR]'+title,url,342,iconimage,'','')
                                                if urltitulo_num == 0: ultimaserie = last + '" class="video">' + titulo
                                                if urltitulo_num == 1: ultimaserie = last + '">' + titulo
                                                matchvideo = re.findall(ultimaserie+'(.*?)href="http://twitter.com/share"',link2,re.DOTALL)
                                                if matchvideo:
                                                        for parte in matchvideo:
                                                                temporada = re.compile('emp">(.+?)</p>').findall(parte)
                                                                addDir1('[B][COLOR blue]'+temporada[0]+' :[/COLOR][/B]','','',iconimage,False,'')
                                                                urletitulo = re.compile('href="(.+?)" class="video">(.+?)</a>').findall(parte)
                                                                if not urletitulo: urletitulo = re.compile('href="(.+?)">(.+?)</a>').findall(parte)
                                                                for url, titulo in urletitulo:
                                                                        epis = re.compile('(.+?)-').findall(titulo)
                                                                        if epis:
                                                                                episodio = epis[0]
                                                                                tit = re.compile('-(.*)').findall(titulo)
                                                                                title = '-' + tit[0]
                                                                        else:
                                                                                episodio = titulo
                                                                                title = ''
                                                                        addDir('[COLOR orange]'+episodio+'[/COLOR]'+title,url,342,iconimage,'','')
                                else:
                                        urletitulo = re.compile('href="(.+?)" class="video">(.+?)</a>').findall(link2)
                                        if not urletitulo: urletitulo = re.compile('href="(.+?)">(.+?)</a>').findall(link2)
                                        for url, titulo in urletitulo:
                                                epis = re.compile('(.+?)-').findall(titulo)
                                                if epis:
                                                        episodio = epis[0]
                                                        tit = re.compile('-(.*)').findall(titulo)
                                                        title = '-' + tit[0]
                                                else:
                                                        episodio = titulo
                                                        title = ''
                                                if 'Tweet' not in episodio and '<span' not in episodio and '<img' not in episodio and 'Sinopse' not in episodio:
                                                        addDir('[COLOR orange]'+episodio+'[/COLOR]'+title,url,342,iconimage,'','')
                if 'id="xmain"' not in link2 and '<p class="ntemp">' not in link2:
                        matchvideo = re.findall('<div class="capa">(.*?)</div>', link2, re.DOTALL)
                        for match in matchvideo:
                                urls_video = re.compile('href="(.+?)"').findall(match)
                                if urls_video:
                                        try:
                                                link2=ARM_abrir_url(urls_video[0])
                                        except: link2 = ''
                                        if link2:
                                                if 'esquerdo' in link2:
                                                        urls_videos = re.findall('<div class="dub">(.*?)<div class="direito">',link2,re.DOTALL)
                                                        if urls_videos: urls_video = re.compile('<a href="(.+?)"').findall(urls_videos[0])
                                                        addDir1('[COLOR orange]Dublado:[/COLOR]','','',iconimage,False,'')
                                                        for url_videos in urls_video:
                                                                id_video = ''
                                                                try:
                                                                        link3=ARM_abrir_url(url_videos)
                                                                except: link3 = ''                                                
                                                                videolink = re.compile('src="(.+?)"').findall(link3)
                                                                if videolink: url_video = videolink[0]
                                                                else: url_video = ''
                                                                if '/vms.php' in url_videos:
                                                                        videolink = re.compile('proxy.link=(.+?)&proxy.image').findall(link3)
                                                                        if videolink: url_video = videolink[0]
                                                                        else: url_video = ''
                                                                if '.jpg' not in url_video and '.png' not in url_video and 'images' not in url_video: num_fonte = num_fonte + 1
                                                                ARM_resolve_not_videomega_filmes_telecine(url_video,id_video,num_fonte)                                                                
                                                if 'direito' in link2:
                                                        urls_videos = re.findall('<div class="direito">(.*?)</body>',link2,re.DOTALL)
                                                        if urls_videos: urls_video = re.compile('<a href="(.+?)"').findall(urls_videos[0])
                                                        addDir1('[COLOR orange]Legendado:[/COLOR]','','',iconimage,False,'')
                                                        num_fonte = 0
                                                        for url_videos in urls_video:
                                                                id_video = ''
                                                                try:
                                                                        link3=ARM_abrir_url(url_videos)
                                                                except: link3 = ''                                                
                                                                videolink = re.compile('src="(.+?)"').findall(link3)
                                                                if videolink: url_video = videolink[0]
                                                                else: url_video = ''
                                                                if '/vms.php' in url_videos:
                                                                        videolink = re.compile('proxy.link=(.+?)&proxy.image').findall(link3)
                                                                        if videolink: url_video = videolink[0]
                                                                        else: url_video = ''
                                                                if '.jpg' not in url_video and '.png' not in url_video and 'images' not in url_video: num_fonte = num_fonte + 1
                                                                ARM_resolve_not_videomega_filmes_telecine(url_video,id_video,num_fonte)
                                                if 'direito' not in link2 and 'esquerdo' not in link2:
                                                        urls_video = re.compile('<a href="(.+?)"').findall(link2)
                                                        for url_videos in urls_video:
                                                                id_video = ''
                                                                try:
                                                                        link3=ARM_abrir_url(url_videos)
                                                                except: link3 = ''
                                                                videolink = re.compile('src="(.+?)"').findall(link3)
                                                                if videolink: url_video = videolink[0]
                                                                else: url_video = ''
                                                                if '/vms.php' in url_videos:
                                                                        videolink = re.compile('proxy.link=(.+?)&proxy.image').findall(link3)
                                                                        if videolink: url_video = videolink[0]
                                                                        else: url_video = ''
                                                                if '.jpg' not in url_video and '.png' not in url_video and 'images' not in url_video: num_fonte = num_fonte + 1
                                                                ARM_resolve_not_videomega_filmes_telecine(url_video,id_video,num_fonte)                               
                

                


                                        
                
def ARM_encontrar_videos_series(name,url):
        num_fonte = 0
	addDir1(name,'url',1005,iconimage,False,'')
        addDir1('','url',1005,artfolder,False,'')
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
                                        if '.jpg' not in url_video and '.png' not in url_video and 'images' not in url_video: num_fonte = num_fonte + 1
                                        ARM_resolve_not_videomega_filmes(url_video,id_video,num_fonte)
                        urls_video = re.compile('SRC="(.+?)"').findall(match)
                        if urls_video:
                                for url_video in urls_video:
                                        id_video = re.compile('id=(.*)').findall(url_video)
                                        if id_video: id_video = id_video[0]
                                        else: id_video = ''
                                        if '.jpg' not in url_video and '.png' not in url_video and 'images' not in url_video: num_fonte = num_fonte + 1
                                        ARM_resolve_not_videomega_filmes(url_video,id_video,num_fonte)
                matchvideo = re.findall('<div class="post-content">(.*?)<!-- Post Content -->', link2, re.DOTALL)
                for match in matchvideo:
                        urls_video = re.compile('src="(.+?)"').findall(match)
                        if urls_video:
                                for url_video in urls_video:
                                        id_video = re.compile('id=(.*)').findall(url_video)
                                        if id_video: id_video = id_video[0]
                                        else: id_video = ''
                                        if '.jpg' not in url_video and '.png' not in url_video and 'images' not in url_video: num_fonte = num_fonte + 1
                                        ARM_resolve_not_videomega_filmes(url_video,id_video,num_fonte)
                        urls_video = re.compile('SRC="(.+?)"').findall(match)
                        if urls_video:
                                for url_video in urls_video:
                                        id_video = re.compile('id=(.*)').findall(url_video)
                                        if id_video: id_video = id_video[0]
                                        else: id_video = ''
                                        if '.jpg' not in url_video and '.png' not in url_video and 'images' not in url_video: num_fonte = num_fonte + 1
                                        ARM_resolve_not_videomega_filmes(url_video,id_video,num_fonte)
                #matchvideo = re.findall('<div class="capa">(.*?)</div>', link2, re.DOTALL)#--------------------------------------------------
                if 'megafilmeshd.net' in url:
                        #addDir1('sim'+url,'','',iconimage,False,'')
                        if 'player' not in url:
                                urls_video = re.compile('<a href="(.+?)"').findall(link2)
                                if urls_video:
                                        for url_videos in urls_video:
                                                #addDir1(url_videos+'sim1','','',iconimage,False,'')
                                                id_video = ''
                                                try:
                                                        link2=ARM_abrir_url(url_videos)
                                                except: link2 = ''
                                                videolink = re.compile('src="(.+?)"').findall(link2)
                                                if videolink: url_video = videolink[0]
                                                else: url_video = ''
                                                #addDir1(url_video+'sim1','','',iconimage,False,'')
                                                if '.jpg' not in url_video and '.png' not in url_video: num_fonte = num_fonte + 1
                                                ARM_resolve_not_videomega_filmes_telecine(url_video,id_video,num_fonte)
                                else:
                                        urls_video = re.compile('<object.+?src="(.+?)".+?</object>').findall(link2)
                                        if not urls_video: urls_video = re.compile('<iframe.+?src="(.+?)".+?</iframe>').findall(link2)
                                        if urls_video:
                                                for url_videos in urls_video:
                                                        id_video = ''
                                                        num_fonte = num_fonte + 1
                                                        ARM_resolve_not_videomega_filmes_telecine(url_videos,id_video,num_fonte)
                        else:
                                urls_video = re.compile('<object.+?src="(.+?)".+?</object>').findall(link2)
                                if not urls_video: urls_video = re.compile('<iframe.+?src="(.+?)".+?</iframe>').findall(link2)
                                if urls_video:
                                        for url_videos in urls_video:
                                                id_video = ''
                                                num_fonte = num_fonte + 1
                                                ARM_resolve_not_videomega_filmes_telecine(url_videos,id_video,num_fonte)
                if 'megaseriesonlinehd.com' in url:
                        urls_video = re.findall('<ul id="filmes">(.*?)background:url', link2, re.DOTALL)
                        if urls_video:
                                id_video = ''
                                videolink = re.compile('src="(.+?)"').findall(urls_video[0])
                                for vid in videolink:
                                        url_video = vid
                                        num_fonte = num_fonte + 1
                                        ARM_resolve_not_videomega_filmes_telecine(url_video,id_video,num_fonte)

                
                        
				
#----------------------------------------------------------------------------------------------------------------------------------------------#

def ARM_resolve_not_videomega_filmes(url,id_video,num_fonte):
        #addDir1(url,'','',iconimage,False,'')
        if "allmyvideos" in url:
		try:
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Allmyvideos)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
	if "clipstube" in url:
		try:
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Clipstube)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "drive.google" in url:
		try:
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](DG)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass

	if "megahd/inde" in url:
		try:
                        try:
                                link2=ARM_abrir_url(url)
                        except: link2 = ''
                        vlink = re.compile('<param name="FlashVars" value="plugins=plugins/proxy.swf&proxy.link=(.+?)" />').findall(link2)
                        if vlink: url = vlink[0]
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](DG)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
	if "cloudzilla" in url:
                try:
                        if '/share/file/' in url: url = url.replace('/share/file/','/embed/')
                        elif id_video != '': url = 'http://www.cloudzilla.to/embed/' + id_video
                        print url
			url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Cloudzilla)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "vkontakte.ru" in url:
		try:
                        url = url.replace('vkontakte.ru','vk.com')
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Vkontakte.ru)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
	if "played.to" in url:
                try:
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Played.to)[/COLOR][/B]',url,30,iconimage,'','')
                except:pass
	if "storage.mais.uol" in url:
		try:
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Storage.mais.uol)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "videomega" in url:
		try:
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Videomega)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "vidto.me" in url:
		try:
                        match = re.compile('http://vidto.me/embed-(.+?).html').findall(url)
			if match:
				id_video = match[0]
				url = 'http://vidto.me/' + id_video + '.html'
				url = url + '///' + name
			else: url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Vidto.me)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "dropvideo" in url or 'drop' in url:
		try:
                        url = 'http://dropvideo.com/embed/' + id_video
			print url
			url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](DropVideo)[/COLOR][/B]',url,30,iconimage,'','')
		except:pass
	if "streamin.to" in url:
                try:
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,30,iconimage,'','')
                except:pass
        if "firedrive" in url:
                try:
                        url = 'http://www.firedrive.com/embed/' + id_video
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Firedrive)[/COLOR][/B]',url,30,iconimage,'','')
                except:pass    
        if "putlocker" in url:
                try:
                        url = 'http://www.firedrive.com/embed/' + id_video
                        print url
                        url = url + '///' + name
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Firedrive)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "nowvideo" in url:
                try:
                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video
                        print url
                        url = url + '///' + name
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Nowvideo)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if 'armage.php' in url:
                try:
                        if len(id_video) == 16:
                                url = 'http://www.firedrive.com/embed/' + id_video
                                print url
                                url = url + '///' + name
                                addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Firedrive)[/COLOR][/B]',url,30,iconimage,'','')
                        if len(id_video) == 13:
                                url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video
                                print url
                                url = url + '///' + name
                                addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Nowvideo)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "primeshare" in url:
                try:
                        url = url + '///' + name
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Primeshare.tv)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "videoslasher" in url:
                try:
                        url = url + '///' + name
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](VideoSlasher)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "sockshare" in url:
                try:
                        url = url + '///' + name
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Sockshare)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "video.mail.ru" in url or 'dcd.php' in url:
                try:
                        #url = url.replace('/embed/','/').replace('.html','.json')
                        if '/videos/' not in url:
                                url = url.replace('http://video.mail.ru/mail/megafilmes/_myvideo/','http://api.video.mail.ru/videos/embed/mail/megafilmes/_myvideo/')
                        url = url + '///' + name
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Video.mail.ru)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "flashx.tv" in url:
                try:
                        url = url + '///' + name
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](FlashX.tv)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	else:
                if "/flashxtv/" in url:
                        try:
                                funciona = ''
                                try:
                                        flashxtv=ARM_abrir_url(url)
                                except: flashxtv = ''
                                flash = re.compile('<iframe width="600" height="480" src="(.+?)"').findall(flashxtv)
                                try:
                                        flashxtv=ARM_abrir_url(flash[0].replace('WWWflash','flash'))
                                except: flashxtv = ''
                                flashurl = re.compile('addthis:url="(.+?)" addthis:').findall(flashxtv)
                                if flashurl:
                                        url = flashurl[0]
                                        url = url + '///' + name
                                else:
                                        url = url + '///' + name
                                        funciona = '[COLOR red] - Sem link[/COLOR]'
                                addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](FlashX.tv)[/COLOR][/B]'+funciona,url,30,iconimage,'','')
                        except:pass
    	if 'videott' in url:
                try:
                        if 'armagedomfilmes' in url: url = url.replace('http://www.armagedomfilmes.biz/player/videott.php?id=','http://www.video.tt/e/')
                        url = url.replace('/video/','/e/')
                        url = url.replace('videott','video.tt')
                        url = url.replace('http://www.video.tt/e/','http://video.tt/e/')
                        url = url.replace('http://video.tt/e/','http://video.tt/player_control/settings.php?v=')+'&fv=v1.2.74'
                        #url = 'http://video.tt/player_control/settings.php?v='+id_video+'&fv=v1.2.74'
                        url = url + '///' + name
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Video.tt)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	else:
                if "video.tt" in url:
                        try:
                                url = url.replace('/video/','/e/')
                                url = url.replace('http://www.video.tt/e/','http://video.tt/e/')
                                url = url.replace('http://video.tt/e/','http://video.tt/player_control/settings.php?v=')+'&fv=v1.2.74'
                                #url = 'http://video.tt/player_control/settings.php?v='+id_video+'&fv=v1.2.74'
                                url = url + '///' + name
                                addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Video.tt)[/COLOR][/B]',url,30,iconimage,'','')
                        except:pass
    	return



def ARM_resolve_not_videomega_filmes_telecine(url,id_video,num_fonte):
        #addDir1(url,'','',iconimage,False,'')
        if "cloudzilla" in url:
                try:
                        if '/share/file/' in url: url = url.replace('/share/file/','/embed/')
                        elif id_video != '': url = 'http://www.cloudzilla.to/embed/' + id_video
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Cloudzilla)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
	if "vidbull" in url:
		try:
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Vidbull)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
	if "played.to" in url:
                try:
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Played.to)[/COLOR][/B]',url,30,iconimage,'','')
                except:pass
	if "clipstube" in url:
		try:
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Clipstube)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "drive.google" in url:
		try:
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](DG)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
	if "megahd/inde" in url:
		try:
                        try:
                                link2=ARM_abrir_url(url)
                        except: link2 = ''
                        vlink = re.compile('<param name="FlashVars" value="plugins=plugins/proxy.swf&proxy.link=(.+?)" />').findall(link2)
                        if vlink: url = vlink[0]
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](DG)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "allmyvideos" in url:
		try:
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Allmyvideos)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
	if "vodlocker" in url:
		try:
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Vodlocker)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
	if "vk.com" in url:
		try:
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](VK)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
	if "youwatch" in url:
		try:
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Youwatch)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
	if "hostingbulk" in url:
		try:
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Hostingbulk)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "vkontakte.ru" in url:
		try:
                        url = url.replace('vkontakte.ru','vk.com')
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Vkontakte.ru)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
	if "storage.mais.uol" in url:
		try:
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Storage.mais.uol)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "videomega" in url:
		try:
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Videomega)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "vidto.me" in url:
		try:
                        match = re.compile('http://vidto.me/embed-(.+?).html').findall(url)
			if match:
				id_video = match[0]
				url = 'http://vidto.me/' + id_video + '.html'
				url = url + '///' + name
			else: url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Vidto.me)[/COLOR][/B]',url,30,iconimage,'','')
		except: pass
        if "dropvideo" in url or 'drop' in url:
		try:
			url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](DropVideo)[/COLOR][/B]',url,30,iconimage,'','')
		except:pass
	if "streamin.to" in url:
                try:
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,30,iconimage,'','')
                except:pass
        if "firedrive" in url:
                try:
                        url = url + '///' + name
			addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Firedrive)[/COLOR][/B]',url,30,iconimage,'','')
                except:pass    
        if "putlocker" in url or 'armage.php' in url:
                try:
                        url = url + '///' + name
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Firedrive)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "nowvideo" in url:
                try:
                        url = url + '///' + name
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Nowvideo)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "primeshare" in url:
                try:
                        url = url + '///' + name
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Primeshare.tv)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "videoslasher" in url:
                try:
                        url = url + '///' + name
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](VideoSlasher)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "sockshare" in url:
                try:
                        url = url + '///' + name
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Sockshare)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "playfreehd" in url:
                try:
                        url = url + '///' + name
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](PlayfreeHD)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "video.mail.ru" in url or 'dcd.php' in url:
                try:
                        #url = url.replace('/embed/','/').replace('.html','.json')
                        if '/videos/' not in url:
                                url = url.replace('http://video.mail.ru/mail/megafilmes/_myvideo/','http://api.video.mail.ru/videos/embed/mail/megafilmes/_myvideo/')
                        url = url + '///' + name  #http://api.video.mail.ru/videos/mail/megafilmes/_myvideo/172.json
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Video.mail.ru)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "flashx.tv" in url:
                try:
                        try:
                                flashxtv=ARM_abrir_url(url)
                        except: flashxtv = ''
                        flashurl = re.compile('addthis:url="(.+?)" addthis:').findall(flashxtv)
                        if flashurl: url = flashurl[0]
                        url = url + '///' + name
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](FlashX.tv)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if "/flashxtv/" in url:
                try:
                        url = url + '///' + name
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](FlashX.tv)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	if 'videott' in url:
                try:
                        if 'armagedomfilmes' in url: url = url.replace('http://www.armagedomfilmes.biz/player/videott.php?id=','http://www.video.tt/e/')
                        url = url.replace('/video/','/e/')
                        url = url.replace('videott','video.tt')
                        url = url.replace('http://www.video.tt/e/','http://video.tt/e/')
                        url = url.replace('http://video.tt/e/','http://video.tt/player_control/settings.php?v=')+'&fv=v1.2.74///' + name
                        addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Video.tt)[/COLOR][/B]',url,30,iconimage,'','')
    		except:pass
    	else:
                if "video.tt" in url:
                        try:
                                url = url.replace('/video/','/e/')
                                url = url.replace('http://www.video.tt/e/','http://video.tt/e/')
                                url = url.replace('http://video.tt/e/','http://video.tt/player_control/settings.php?v=')+'&fv=v1.2.74///' + name
                                addDir('[B]- Fonte ' + str(num_fonte) + ' : [COLOR blue](Video.tt)[/COLOR][/B]',url,30,iconimage,'','')
                        except:pass
    	return
   




def ARM_encontrar_fontes_filmes_M18():        
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
                #addDir1('','','',iconimage,False,'')
		addDir("Página Seguinte >>",proxima[0].replace('#038;',''),332,artfolder + 'PAGS2.png','nao','')
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
	liz.setProperty('fanart_image',artfolder + 'FAN3.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addLink1(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'FAN3.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,checker,fanart):
        text = 'nnnnnn'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&checker="+urllib.quote_plus(checker)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'FAN3.jpg')
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
	liz.setProperty('fanart_image',artfolder + 'FAN3.jpg')
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


