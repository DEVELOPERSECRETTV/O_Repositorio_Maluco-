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


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,time,os
import json
from array import array
from string import capwords
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
net=Net()

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
perfil = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
tmdb_base_url = 'http://d3gtl9l2a4fn1j.cloudfront.net/t/p/w1280'

progress = xbmcgui.DialogProgress()

#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------#

class themoviedb_api_pagina:
        
        api_key = '3e7807c4a01f18298f64662b257d7059'
        tmdb_base_url = 'http://d3gtl9l2a4fn1j.cloudfront.net/t/p/w1280'
        def fanart_and_id(self,movie_tv,num_mode,items,pagina):
                a = 1
                i = 0
                percent = 0
                message = ''
                progress.create('Progresso', 'A Procurar')
                progress.update( percent, 'A Procurar ...', message, "" )
                url_tmdb = 'http://api.themoviedb.org/3/' + urllib.quote(movie_tv) + '/' + urllib.quote(items) + '?api_key=' + self.api_key + '&language=en&page=' + urllib.quote(pagina)
                try:datass = abrir_url(url_tmdb)
                except: datass = ''
                try: data = json_get(url_tmdb)
                except: data = ''
                if urllib.quote(movie_tv) == 'movie': n = re.findall('"title":"(.+?)"', datass, re.DOTALL)
                if urllib.quote(movie_tv) == 'tv': n = re.findall('"name":"(.+?)"', datass, re.DOTALL)
                numero = len(n)
                num = numero + 0.0
                for nn in n:
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        if urllib.quote(movie_tv) == 'movie': progress.update( percent, 'A Procurar Filmes...', message, "" )
                        if urllib.quote(movie_tv) == 'tv': progress.update( percent, 'A Procurar Séries...', message, "" )
                        print str(a) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        try:
                                name=nn
                        except: name = ''
                        try: fanart=self.tmdb_base_url + data['results'][i]['backdrop_path']
                        except: fanart = ''
                        try: thumb=self.tmdb_base_url.replace('w1280','w600') + data['results'][i]['poster_path']
                        except: thumb = ''
                        try: tmdb_id=str(data['results'][i]['id'])
                        except: tmdb_id = ''
                        if urllib.quote(movie_tv) == 'movie':
                                try:
                                        year=str(data['results'][i]['release_date'])
                                        y = re.compile('(.+?)[-].+?[-]').findall(year)
                                        if y: year = y[0]
                                except: year = ''
                        if urllib.quote(movie_tv) == 'tv':
                                try:
                                        year=str(data['results'][i]['first_air_date'])
                                        y = re.compile('(.+?)[-].+?[-]').findall(year)
                                        if y: year = y[0]
                                except: year = ''
                        try:
                                url_tmdb = 'http://api.themoviedb.org/3/' + urllib.quote(movie_tv) + '/' + urllib.quote(tmdb_id)+'?language=pt&api_key=' + self.api_key
                                try: datas = abrir_url(url_tmdb)
                                except: datas = ''
                                imdb = re.compile('"imdb_id":"(.+?)"').findall(datas)
                                if imdb: imdbcode = imdb[0]
                                else: imdbcode = ''
                                sin = re.compile('"overview":"(.+?)"[,]"popularity').findall(datas)
                                if sin: sinopse = sin[0].replace('\\"','"')
                                else: sinopse = ''
                                gen = re.findall('"genres":[[][{]"id":(.+?)[}][]]', datas, re.DOTALL)
                                if gen:
                                        gen = re.compile('"name":"(.+?)"').findall(gen[0])
                                        if gen:
                                                numgen = 0
                                                for gene in gen:
                                                        if numgen == 0:
                                                                genero = gene
                                                                numgen = 1
                                                        else: genero = genero + ', ' + gene    
                                else: genero = ''
                        except: pass
                        if sinopse == '' or sinopse == '",':
                                try:
                                        url_tmdb = 'http://api.themoviedb.org/3/' + urllib.quote(movie_tv) + '/' + urllib.quote(tmdb_id)+'?language=en&api_key=' + self.api_key
                                        try: datas = abrir_url(url_tmdb)
                                        except: datas = ''
                                        imdb = re.compile('"imdb_id":"(.+?)"').findall(datas)
                                        if imdb: imdbcode = imdb[0]
                                        else: imdbcode = ''
                                        sin = re.compile('"overview":"(.+?)"[,]"popularity').findall(datas)
                                        if sin: sinopse = sin[0].replace('\\"','"')
                                        else: sinopse =''
                                        if gen:
                                                gen = re.compile('"name":"(.+?)"').findall(gen[0])
                                                if gen:
                                                        numgen = 0
                                                        for gene in gen:
                                                                if numgen == 0:
                                                                        genero = gene
                                                                        numgen = 1
                                                                else: genero = genero + ', ' + gene    
                                        else: genero = ''
                                except: pass

                        addDir_trailer('[B][COLOR green]' + name + '[/COLOR][/B][COLOR yellow] (' + year + ')[/COLOR]','IMDB'+imdbcode+'IMDB',urllib.quote(num_mode),thumb,sinopse,fanart,year,genero,name,'http://thetvdb.com/?tab=series&id='+urllib.quote(tmdb_id))
                        a = a + 1
                        i = i + 1


class thetvdb_api_tvdbid:
	def _id(self,series_name,year):
		try:
			url = 'http://thetvdb.com/api/GetSeries.php?seriesname=' + urllib.quote(series_name)+'&language=pt'
			html_source = abrir_url(url)
		except: html_source = ''
		idtvdb = re.findall('<seriesid>(.+?)</seriesid>', html_source, re.DOTALL)
		if idtvdb: tvdbid = idtvdb[0]
		else: tvdbid = ''
		return str(tvdbid)

class thetvdb_api_episodes:
        
	def _id(self,idtvdb,temporada,episodio):
                try:
                        url = 'http://thetvdb.com/api/23B3F3D91B980C9F/series/'+urllib.quote(idtvdb)+'/all/pt.xml'
                        html_source = abrir_url(url)
                except: html_source = ''
                info = re.findall('<Episode>(.+?)</Episode>', html_source, re.DOTALL)
                for infos in info:
                        try:
                                season = re.compile('<DVD_season>(.+?)</DVD_season>').findall(infos)
                                if not season: season = re.compile('<Combined_season>(.+?)</Combined_season>').findall(infos)
                                episode = re.compile('<EpisodeNumber>(.+?)</EpisodeNumber>').findall(infos)
                                if season and episode:
                                        #addLink(season[0],'','')
                                        if season[0] == str(temporada) and episode[0] == str(episodio):
                                                epi_nome =re.compile('<EpisodeName>(.+?)</EpisodeName>').findall(infos)
                                                air = re.compile('<FirstAired>(.+?)</FirstAired>').findall(infos)
                                                sin = re.compile('<Overview>(.+?)</Overview>').findall(infos)
                                                th = re.compile('<filename>(.+?)</filename>').findall(infos)
                                                try: epi_nome = epi_nome[0]
                                                except: epi_nome = ''
                                                try: air = air[0]
                                                except: air = ''
                                                try: sin = sin[0]
                                                except: sin = ''
                                                try: th = 'http://thetvdb.com/banners/'+th[0]
                                                except: th = ''
                                                
                        except:
                                epi_nome = ''
                                air = ''
                                sin = ''
                                th = ''
                return str(epi_nome),str(air),str(sin),str(th)
                        

class thetvdb_api:
	def _id(self,series_name,year):
		_id_init = []
		self.si = ''
		self.sin = ''
		self.idserie = ''
		self.anne = ''
		yea = re.compile('(.+?)[|](.*)').findall(year)
		if yea:
                        year = yea[0][0]
                        imdb = yea[0][1]
                else: imdb = ''
		if series_name == "24 hours": series_name = "24"
		try:
			url = 'http://thetvdb.com/api/GetSeries.php?seriesname=' + urllib.quote(series_name)+'&language=pt'
			html_source = abrir_url(url)
		except: html_source = ''
		balisa = re.findall('<Series>(.+?)</Series>', html_source, re.DOTALL)
		#addLink(str(len(balisa))+series_name,'','')
		if balisa:# and len(balisa) > 1:
                        for balisas in balisa:
                                sid = re.compile('<seriesid>(.+?)</seriesid>').findall(balisas)
                                overview = re.compile('<Overview>(.+?)</Overview>').findall(balisas)
                                imdbcode = re.compile('<IMDB_ID>(.+?)</IMDB_ID>').findall(balisas)
                                aired = re.compile('<FirstAired>(.+?)-.+?-.+?</FirstAired>').findall(balisas)
                                if imdbcode and imdb != '':
                                        self.imdbc = imdbcode[0]
                                        #addLink(self.imdbc+imdb+urllib.quote(series_name),'','','')
                                        if self.imdbc == imdb and self.idserie == '':
                                                if overview: self.sin = overview[0]
                                                else: self.sin = '---'
                                                if sid: self.idserie = sid[0]
                                                else: self.idserie = ''
                                elif aired:
                                        #addLink(self.anne,'','','')
                                        self.anne = aired[0]
                                        if self.anne == year and self.idserie == '':
                                                if overview: self.sin = overview[0]
                                                else: self.sin = '---'
                                                if sid: self.idserie = sid[0]
                                                else: self.idserie = ''
                                                
                if self.idserie != '': return self.idserie+'|'+self.sin                                          
                else:
                        id_and_year = re.findall('<seriesid>(.+?)</seriesid>.*?<Overview>(.+?)</Overview>.+?<FirstAired>(.+?)-.+?-.+?</FirstAired>', html_source, re.DOTALL)
                        if id_and_year == []:
                                self.si = re.compile('<Overview>(.+?)</Overview>').findall(html_source)
                                if self.si: self.sin = self.si[0]
                                else: self.sin = '---'
                                _id = re.compile('<seriesid>(.+?)</seriesid>').findall(html_source)
                                if _id == []: return ''
                                else: return _id[0]+'|'+self.sin
                                
                        else:
                                for serieid,sino,ano in id_and_year:
                                        if ano == year: _id_init.append(serieid)
                                        else: pass
                                if _id_init == []: return id_and_year[0][0]+'|'+id_and_year[0][1]
                                else:
                                        self.si = re.compile('<Overview>(.+?)</Overview>').findall(html_source)
                                        if self.si: self.sin = self.si[0]
                                        else: self.sin = '---'
                                        return _id_init[0]+'|'+self.sin#id_and_year[0][1]

##	def fanart(self,series_id):#http://thetvdb.com/banners/posters/72129-2.jpg
##		fanart_image = 'http://thetvdb.com/banners/fanart/original/' + series_id + '-1.jpg'
####		if check_if_image_exists(fanart_image): fanart_image = ''
####		else: pass
##		return fanart_image

class thetvdb_api_IMDB:
        
	def _id(self,series_name,imdb):
                
		self.sin = ''
		self.idserie = ''

		try:
			url = 'http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=' + urllib.quote(imdb)+'&language=pt'
			html_source = abrir_url(url)
		except: html_source = ''
		
                sid = re.compile('<seriesid>(.+?)</seriesid>').findall(html_source)
                overview = re.compile('<Overview>(.+?)</Overview>').findall(html_source)
                imdbcode = re.compile('<IMDB_ID>(.+?)</IMDB_ID>').findall(html_source)
                aired = re.compile('<FirstAired>(.+?)-.+?-.+?</FirstAired>').findall(html_source)

                if overview: self.sin = overview[0]
                else: self.sin = '---'
                if sid: self.idserie = sid[0]
                else: self.idserie = ''
                                                
                return self.idserie, self.sin                                          

class themoviedb_api_IMDB1:
        api_key = '3e7807c4a01f18298f64662b257d7059'
        tmdb_base_url = 'http://d3gtl9l2a4fn1j.cloudfront.net/t/p/w1280'
        
        def fanart_and_id(self,movie_info_imdb_code):
                try:
                        url_tmdb = 'http://api.themoviedb.org/3/movie/'+urllib.quote_plus(movie_info_imdb_code)+'?language=pt&api_key=' + self.api_key 
                        try: data = json_get(url_tmdb)
                        except: data = ''
                        
                        try: fanart = self.tmdb_base_url + data[u'backdrop_path']
                        except: fanart = ''
                        
                        try: thumb = tmdb_base_url.replace('w1280','w600') + data[u'poster_path']
                        except: thumb =''
                        
                        try: id_tmdb = data[u'id']
                        except: id_tmdb=''
                except: pass

                if fanart == '':
                        try:
                                url_tmdb = 'http://api.themoviedb.org/3/movie/'+urllib.quote_plus(movie_info_imdb_code)+'?language=en&api_key=' + self.api_key 
                                try: data = json_get(url_tmdb)
                                except: data = ''
                                
                                try: fanart = self.tmdb_base_url + data[u'backdrop_path']
                                except: fanart = ''
                                
                                try: thumb = tmdb_base_url.replace('w1280','w600') + data[u'poster_path']
                                except: thumb =''
                                
                                try: id_tmdb = data[u'id']
                                except: id_tmdb=''
                        except: pass
                        
                return fanart,str(id_tmdb),thumb

class themoviedb_api_TMDB:
        api_key = '3e7807c4a01f18298f64662b257d7059'
        
        def fanart_and_id(self,movie_info_original_title,movie_info_year):#movie_info_imdb_code):
                try:
                        url_tmdb = 'http://api.themoviedb.org/3/search/tv?api_key=' + self.api_key + '&query=' + urllib.quote_plus(movie_info_original_title) + '&year=' + urllib.quote_plus(movie_info_year)
                        #url_tmdb = 'http://api.themoviedb.org/3/tv/'+urllib.quote_plus(movie_info_imdb_code)+'?language=en&api_key=' + self.api_key 
                        try: data = json_get(url_tmdb)
                        except: data = ''

                        try: id_tmdb = data['results'][0]['id']
                        except: id_tmdb=''
                except: pass
                        
                return str(id_tmdb)

class themoviedb_api_search_imdbcode:
        api_key = '3e7807c4a01f18298f64662b257d7059'
        
        def fanart_and_id(self,movie_info_original_title,movie_info_year):#movie_info_imdb_code):
                try:
                        url_tmdb = 'http://api.themoviedb.org/3/search/tv?api_key=' + self.api_key + '&query=' + urllib.quote_plus(movie_info_original_title) + '&year=' + urllib.quote_plus(movie_info_year)
                        try: data = json_get(url_tmdb)
                        except: data = ''
                        
                        try: id_tmdb = data['results'][0]['id']
                        except: id_tmdb=''

                        url_tmdb = 'http://api.themoviedb.org/3/tv/'+str(id_tmdb)+'/external_ids?api_key='+self.api_key
                        try: data = abrir_url(url_tmdb)
                        except: data = ''
                        try:
                                imdb = re.compile('"imdb_id":"(.+?)"').findall(data)
                                imdbcode = imdb[0]
                        except: imdbcode=''
                except: pass
                        
                return str(imdbcode)

class themoviedb_api_IMDB:
        api_key = '3e7807c4a01f18298f64662b257d7059'
        tmdb_base_url = 'http://d3gtl9l2a4fn1j.cloudfront.net/t/p/w1280'
        
        def fanart_and_id(self,movie_info_imdb_code,movie_info_year):
                try:
                        url_tmdb = 'http://api.themoviedb.org/3/movie/' + urllib.quote_plus(movie_info_imdb_code) + '?language=pt&api_key=' + self.api_key
                        try: data = abrir_url(url_tmdb)
                        except: data = ''
                        
                        fan = re.compile('"backdrop_path":"(.+?)"').findall(data)
                        if fan: fanart = self.tmdb_base_url + fan[0]
                        else: fanart = ''

                        th = re.compile('"poster_path":"(.+?)"').findall(data)
                        if th: thumb = tmdb_base_url.replace('w1280','w600') + th[0]
                        else: thumb =''
                        
                        sin = re.compile('"overview":"(.+?)"[,]"popularity').findall(data)
                        if sin: sinopse = sin[0].replace('\\"','"')
                        else: sinopse =''
                        
                        id_t = re.compile('"id":"(.+?)"').findall(data)
                        if id_t: id_tmdb = id_t[0]
                        else: id_tmdb=''
                except: pass
                
                if sinopse == '' or sinopse == '",':
                        try:
                                url_tmdb = 'http://api.themoviedb.org/3/movie/' + urllib.quote_plus(movie_info_imdb_code) + '?language=en&api_key=' + self.api_key
                                try: data = abrir_url(url_tmdb)
                                except: data = ''
                        
                                fan = re.compile('"backdrop_path":"(.+?)"').findall(data)
                                if fan: fanart = self.tmdb_base_url + fan[0]
                                else: fanart = ''

                                th = re.compile('"poster_path":"(.+?)"').findall(data)
                                if th: thumb = tmdb_base_url.replace('w1280','w600') + th[0]
                                else: thumb =''
                                
                                sin = re.compile('"overview":"(.+?)"[,]"popularity').findall(data)
                                if sin: sinopse = sin[0].replace('\\"','"')
                                else: sinopse =''
                                
                                id_t = re.compile('"id":"(.+?)"').findall(data)
                                if id_t: id_tmdb = id_t[0]
                                else: id_tmdb=''
                        except: pass
                if data == '':
                        fanart = ''
                        id_tmdb = ''
                        thumb = ''
                        sinopse = ''
                return fanart,str(id_tmdb),thumb,sinopse
        
class themoviedb_api_IMDB_episodios:
        api_key = '3e7807c4a01f18298f64662b257d7059'
        tmdb_base_url = 'http://d3gtl9l2a4fn1j.cloudfront.net/t/p/w1280'
        
        def fanart_and_id(self,movie_info_imdb_code,season,episode):
##                addLink('d','','')
##                return '1'
                try:
                        url_tmdb = 'http://api.themoviedb.org/3/tv/' + urllib.quote_plus(movie_info_imdb_code) + '/season/' + urllib.quote_plus(season) + '/episode/' + urllib.quote_plus(episode) + '?&api_key=' + self.api_key + '&language=pt'
                        try: data = abrir_url(url_tmdb)
                        except: data = ''
                        
                        air = re.compile('"air_date":"(.+?)"').findall(data)
                        if air: air_date = air[0]
                        else: air_date = ''

                        th = re.compile('"still_path":"(.+?)"').findall(data)
                        if th: thumbep = tmdb_base_url.replace('w1280','w600') + th[0]
                        else: thumbep =''
                                
                        sin = re.compile('"overview":"(.+?)"[,]"id').findall(data)
                        if sin: sinopse = sin[0].replace('\\"','"')
                        else: sinopse =''
                                
                        nome_t = re.compile('"name":"(.+?)","overview"').findall(data)
                        if nome_t: nome_e = nome_t[0]
                        else: nome_e=''
                except: pass
                
                if sinopse == '' or sinopse == '",':
                        try:
                                url_tmdb = 'http://api.themoviedb.org/3/tv/' + urllib.quote_plus(movie_info_imdb_code) + '/season/' + urllib.quote_plus(season) + '/episode/' + urllib.quote_plus(episode) + '?&api_key=' + self.api_key + '&language=en'
                                try: data = abrir_url(url_tmdb)
                                except: data = ''
                        
                                air = re.compile('"air_date":"(.+?)"').findall(data)
                                if air: air_date = air[0]
                                else: air_date = ''

                                th = re.compile('"still_path":"(.+?)"').findall(data)
                                if th: thumbep = tmdb_base_url.replace('w1280','w600') + th[0]
                                else: thumbep =''
                                
                                sin = re.compile('"overview":"(.+?)"[,]"id').findall(data)
                                if sin: sinopse = sin[0].replace('\\"','"')
                                else: sinopse =''
                                
                                nome_t = re.compile('"name":"(.+?)","overview"').findall(data)
                                if nome_t: nome_e = nome_t[0]
                                else: nome_e=''
                        except: pass
                        
                return air_date,nome_e,thumbep,sinopse

class themoviedb_api:
        api_key = '3e7807c4a01f18298f64662b257d7059'
        tmdb_base_url = 'http://d3gtl9l2a4fn1j.cloudfront.net/t/p/w1280'
        def fanart_and_id(self,movie_info_original_title,movie_info_year):
                url_tmdb = 'http://api.themoviedb.org/3/search/movie?api_key=' + self.api_key + '&query=' + urllib.quote_plus(movie_info_original_title) + '&year=' + movie_info_year
                try: data = json_get(url_tmdb)
                except: data = ''
                try: fanart=self.tmdb_base_url + data['results'][0]['backdrop_path']
                except: #fanart = ''
                        try:
                                url_tmdb = 'http://api.themoviedb.org/3/search/movie?api_key=' + self.api_key + '&query=' + urllib.quote_plus(movie_info_original_title) + '&year='
                                data = json_get(url_tmdb)
                        except: data = ''
                try: fanart=self.tmdb_base_url + data['results'][0]['backdrop_path']
                except: fanart=''
                #addLink(fanart+movie_info_original_title+movie_info_year,'','')
                try: thumb=tmdb_base_url.replace('w1280','w600') + data['results'][0]['poster_path']
                except: thumb =''
                try: id_tmdb = data['results'][0]['id']
                except: id_tmdb=''
                #addLink('2'+str(fanart),'','')
                return fanart,str(id_tmdb),thumb

##        def trailer(self,id_tmdb):
##                url_tmdb = 'http://api.themoviedb.org/3/movie/' + id_tmdb +'/trailers?api_key=' + self.api_key
##                try: data = json_get(url_tmdb)
##                except: data = ''
##                try: youtube_id = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + str(data['youtube'][0]['source'])
##                except: youtube_id= ''
##                return str(youtube_id)

class themoviedb_api_tv:
        api_key = '3e7807c4a01f18298f64662b257d7059'
        tmdb_base_url = 'http://d3gtl9l2a4fn1j.cloudfront.net/t/p/w1280'
        def fanart_and_id(self,movie_info_original_title,movie_info_year):
                url_tmdb = 'http://api.themoviedb.org/3/search/tv?api_key=' + self.api_key + '&query=' + urllib.quote_plus(movie_info_original_title) + '&year=' + movie_info_year
                try: data = json_get(url_tmdb)
                except: data = ''
                try: fanart=self.tmdb_base_url + data['results'][0]['backdrop_path']
                except: fanart=''
                try:
                        thumb=tmdb_base_url.replace('w1280','w600') + data['results'][0]['poster_path']
                except: thumb =''
                try: id_tmdb = data['results'][0]['id']
                except: id_tmdb=''
                return fanart,str(id_tmdb),thumb

##        def trailer(self,id_tmdb):
##                url_tmdb = 'http://api.themoviedb.org/3/movie/' + id_tmdb +'/trailers?api_key=' + self.api_key
##                try: data = json_get(url_tmdb)
##                except: data = ''
##                try: youtube_id = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + str(data['youtube'][0]['source'])
##                except: youtube_id= ''
##                return str(youtube_id)

class theomapi_api:
        tapi_base_url = 'http://www.omdbapi.com/?i='
        def sinopse(self,imdbcode):
                url_tmdb =  self.tapi_base_url + imdbcode + '&plot=full'
                try: data = json_get(url_tmdb)
                except: data = ''
                try: sinopse=data[u'Plot']
                except: sinopse = ''
                return sinopse

class theomapi_api_nome:
        tapi_base_url = 'http://www.omdbapi.com/?t='
        def sinopse(self,nomefilme):
                url_tmdb =  self.tapi_base_url + nomefilme + '&plot=full'
                try: data = json_get(url_tmdb)
                except: data = ''
                try: sinopse=data[u'Plot']
                except: sinopse = ''
                return sinopse


def json_get(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        data = json.load(urllib2.urlopen(req))
        return data



######################################################
#########   THANKS MAFARRICOS   ####################

def trailer(namet, url):
	print namet,url
	url = trailer2().run(namet, url)
	if url == None: return
	item = xbmcgui.ListItem(path=url)
	item.setProperty("IsPlayable", "true")
	xbmc.Player().play(url, item)

class trailer2:
        def __init__(self):
                self.youtube_base = 'http://www.youtube.com'
                self.youtube_query = 'http://gdata.youtube.com/feeds/api/videos?q='
                self.youtube_watch = 'http://www.youtube.com/watch?v=%s'
                self.youtube_info = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2'

        def run(self, name, url):
                try:
                        if url.startswith(self.youtube_base):
                                url = self.youtube(url)
                                if url == None: raise Exception()
                                return url
                        elif not url.startswith('http://'):
                                url = self.youtube_watch % url
                                url = self.youtube(url)
                                if url == None: raise Exception()
                                return url
                        else:
                                raise Exception()
                except:
                        url = self.youtube_query + name + ' trailer'
                        url = self.youtube_search(url)
                        if url == None: return
                        return url

        def youtube_search(self, url):
                try:
                        query = url.split("?q=")[-1].split("/")[-1].split("?")[0]
                        url= url.split('[/B]')[0].replace('[B]','')
                        url = url.replace(query, urllib.quote_plus(query))
                        result = getUrl(url, timeout='10').result
                        result = parseDOM(result, "entry")
                        result = parseDOM(result, "id")
			
                        for url in result[:5]:
                                url = url.split("/")[-1]	
                                url = self.youtube_watch % url
                                url = self.youtube(url)
                                if not url == None: return url
                except: return

        def youtube(self, url):
                print '#youtube'
                try:
                        id = url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]
                        state, reason = None, None
                        result = getUrl(self.youtube_info % id, timeout='10').result
                        try:
                                state = common.parseDOM(result, "yt:state", ret="name")[0]
                                reason = common.parseDOM(result, "yt:state", ret="reasonCode")[0]
                        except:
                                pass
                        if state == 'deleted' or state == 'rejected' or state == 'failed' or reason == 'requesterRegion' : return
                        try:
                                result = getUrl(self.youtube_watch % id, timeout='10').result
                                alert = common.parseDOM(result, "div", attrs = { "id": "watch7-notification-area" })[0]
                                return
                        except:
                                pass
                        url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % id
                        return url
                except:
                        return


class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='', timeout='5'):
        if not proxy == None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post == None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if mobile == True:
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')
        if not referer == None:
            request.add_header('Referer', referer)
        if not cookie == None:
            request.add_header('cookie', cookie)
        response = urllib2.urlopen(request, timeout=int(timeout))
        if output == 'cookie':
            result = str(response.headers.get('Set-Cookie'))
        elif output == 'geturl':
            result = response.geturl()
        else:
            result = response.read()
        if close == True:
            response.close()
        self.result = result

def parseDOM(html, name=u"", attrs={}, ret=False):
    if isinstance(name, str): # Should be handled
        try:  name = name #.decode("utf-8")
        except: pass

    if isinstance(html, str):
        try: html = [html.decode("utf-8")] # Replace with chardet thingy
        except: html = [html]
    elif isinstance(html, unicode): html = [html]
    elif not isinstance(html, list): return u""

    if not name.strip(): return u""

    ret_lst = []
    for item in html:
        temp_item = re.compile('(<[^>]*?\n[^>]*?>)').findall(item)
        for match in temp_item: item = item.replace(match, match.replace("\n", " "))

        lst = _getDOMElements(item, name, attrs)

        if isinstance(ret, str):
            lst2 = []
            for match in lst:
                lst2 += _getDOMAttributes(match, name, ret)
            lst = lst2
        else:
            lst2 = []
            for match in lst:
                temp = _getDOMContent(item, name, match, ret).strip()
                item = item[item.find(temp, item.find(match)) + len(temp):]
                lst2.append(temp)
            lst = lst2
        ret_lst += lst

    return ret_lst

def _getDOMContent(html, name, match, ret):  # Cleanup

    endstr = u"</" + name  # + ">"

    start = html.find(match)
    end = html.find(endstr, start)
    pos = html.find("<" + name, start + 1 )

    while pos < end and pos != -1:  # Ignore too early </endstr> return
        tend = html.find(endstr, end + len(endstr))
        if tend != -1:
            end = tend
        pos = html.find("<" + name, pos + 1)

    if start == -1 and end == -1:
        result = u""
    elif start > -1 and end > -1:
        result = html[start + len(match):end]
    elif end > -1:
        result = html[:end]
    elif start > -1:
        result = html[start + len(match):]

    if ret:
        endstr = html[end:html.find(">", html.find(endstr)) + 1]
        result = match + result + endstr

    return result

def _getDOMAttributes(match, name, ret):
    lst = re.compile('<' + name + '.*?' + ret + '=([\'"].[^>]*?[\'"])>', re.M | re.S).findall(match)
    if len(lst) == 0:
        lst = re.compile('<' + name + '.*?' + ret + '=(.[^>]*?)>', re.M | re.S).findall(match)
    ret = []
    for tmp in lst:
        cont_char = tmp[0]
        if cont_char in "'\"":

            # Limit down to next variable.
            if tmp.find('=' + cont_char, tmp.find(cont_char, 1)) > -1:
                tmp = tmp[:tmp.find('=' + cont_char, tmp.find(cont_char, 1))]

            # Limit to the last quotation mark
            if tmp.rfind(cont_char, 1) > -1:
                tmp = tmp[1:tmp.rfind(cont_char)]
        else:
            if tmp.find(" ") > 0:
                tmp = tmp[:tmp.find(" ")]
            elif tmp.find("/") > 0:
                tmp = tmp[:tmp.find("/")]
            elif tmp.find(">") > 0:
                tmp = tmp[:tmp.find(">")]

        ret.append(tmp.strip())

    return ret

def _getDOMElements(item, name, attrs):
    lst = []
    for key in attrs:
        lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=[\'"]' + attrs[key] + '[\'"].*?>))', re.M | re.S).findall(item)
        if len(lst2) == 0 and attrs[key].find(" ") == -1:  # Try matching without quotation marks
            lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=' + attrs[key] + '.*?>))', re.M | re.S).findall(item)

        if len(lst) == 0:
            lst = lst2
            lst2 = []
        else:
            test = range(len(lst))
            test.reverse()
            for i in test:  # Delete anything missing from the next list.
                if not lst[i] in lst2:
                    del(lst[i])

    if len(lst) == 0 and attrs == {}:
        lst = re.compile('(<' + name + '>)', re.M | re.S).findall(item)
        if len(lst) == 0:
            lst = re.compile('(<' + name + ' .*?>)', re.M | re.S).findall(item)

    return lst
################################################################################################
################################################################################################
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

def addLink(name,url,iconimage,fanart):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	#liz.setProperty('fanart_image',artfolder + 'FAN3.jpg')
	liz.setProperty('fanart_image',fanart)
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
        if fanart == '': fanart = artfolder + 'FAN3.jpg'
        #text = 'nnnnnn'
        text = ''
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)+"&checker="+urllib.quote_plus(checker)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',fanart)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
        #cm = []
	#cm.append(('Sinopse', 'XBMC.Action(Info)'))
	#liz.addContextMenuItems(cm, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir_episode(name,url,mode,iconimage,checker,fanart,episod,air,namet,urltrailer):
        if fanart == '': fanart = artfolder + 'FAN3.jpg'
        #text = 'nnnnnn'
        text = ''
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&urltrailer="+urllib.quote_plus(urltrailer)+"&name="+urllib.quote_plus(name)+"&namet="+urllib.quote_plus(namet)+"&air="+urllib.quote_plus(air)+"&episod="+urllib.quote_plus(episod)+"&fanart="+urllib.quote_plus(fanart)+"&checker="+urllib.quote_plus(checker)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',fanart)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker, "Episode": episod, "Premiered": air } )
        cm = []
  	#cm.append(('Sinopse', 'XBMC.Action(Info)'))
        cm.append(('Ver Trailer', 'RunPlugin(%s?mode=8000&url=%s&namet=%s)' % (sys.argv[0],urllib.quote_plus(urltrailer),namet)))
        liz.addContextMenuItems(cm, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir2(nome,url,mode,iconimage,checker,fanart):
        #text = 'nnnnnn'
        text = ''
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&nome="+urllib.quote_plus(nome)+"&checker="+urllib.quote_plus(checker)+"&fanart="+urllib.quote_plus(fanart)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(nome, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'FAN3.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": nome, "Plot": text } )
        #cm = []
	#cm.append(('Sinopse', 'XBMC.Action(Info)'))
	#liz.addContextMenuItems(cm, replaceItems=True)
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
        #cm.append(('Ver Trailer', 'RunPlugin(%s?mode=8000&url=%s&name=%s)' % (sys.argv[0],urllib.quote_plus(url),name)))
        #liz.addContextMenuItems(cm, replaceItems=False)
        
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir_trailer(name,url,mode,iconimage,plot,fanart,year,genre,namet,urltrailer):
        if fanart == '': fanart = artfolder + 'FAN3.jpg'
        #text = plot
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&urltrailer="+urllib.quote_plus(urltrailer)+"&name="+urllib.quote_plus(name)+"&namet="+urllib.quote_plus(namet)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&year="+urllib.quote_plus(year)+"&genre="+urllib.quote_plus(genre)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',fanart)
        #liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Year": year, "Genre": genre } )
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Year": year, "Genre": genre } )
        
        cm = []
  	#cm.append(('Sinopse', 'XBMC.Action(Info)'))
        cm.append(('Ver Trailer', 'RunPlugin(%s?mode=8000&url=%s&namet=%s)' % (sys.argv[0],urllib.quote_plus(urltrailer),namet)))
        liz.addContextMenuItems(cm, replaceItems=False)
        
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

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

