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



import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,os#,TopPt,TugaFilmesTV
import json
from array import array
from string import capwords
from t0mm0.common.addon import Addon

addon_id = 'plugin.video.Sites_dos_Portugas'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
perfil = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
tmdb_base_url = 'http://d3gtl9l2a4fn1j.cloudfront.net/t/p/w1280'

arr_series1 = [['' for i in range(87)] for j in range(1)]
arr_series = ['' for i in range(500)]
arrai_series = ['' for i in range(500)]
todas_series = ['' for i in range(500)]
sinopse_series = ['' for i in range(500)]
_series = []
_series_ = []
_filmes_ = []
arr_filmes = ['' for i in range(200)]
arrai_filmes = ['' for i in range(200)]
thumb_filmes = ['' for i in range(200)]
arr_filmes[4] = '0'
i=arr_filmes[4]

arr_filmes_anima = []
arrai_filmes_anima = []

#http://www.omdbapi.com/?i=tt0903624http://api.themoviedb.org/3/movie/now_playing?api_key=3e7807c4a01f18298f64662b257d7059&append_to_response=overview&page=1

progress = xbmcgui.DialogProgress()

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
                try:datass = MASH_abrir_url(url_tmdb)
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
                                try: datas = MASH_abrir_url(url_tmdb)
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
                                        try: datas = MASH_abrir_url(url_tmdb)
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

                        addDir_teste('[B][COLOR green]' + name + '[/COLOR][/B][COLOR yellow] (' + year + ')[/COLOR]','IMDB'+imdbcode+'IMDB',urllib.quote(num_mode),thumb,sinopse,fanart,year,genero)
                        a = a + 1
                        i = i + 1


class thetvdb_api_tvdbid:
	def _id(self,series_name,year):
		try:
			url = 'http://thetvdb.com/api/GetSeries.php?seriesname=' + urllib.quote(series_name)+'&language=pt'
			html_source = MASH_abrir_url(url)
		except: html_source = ''
		idtvdb = re.findall('<seriesid>(.+?)</seriesid>', html_source, re.DOTALL)
		if idtvdb: tvdbid = idtvdb[0]
		else: tvdbid = ''
		return str(tvdbid)

class thetvdb_api_episodes:
        
	def _id(self,idtvdb,temporada,episodio):
                try:
                        url = 'http://thetvdb.com/api/23B3F3D91B980C9F/series/'+urllib.quote(idtvdb)+'/all/pt.xml'
                        html_source = MASH_abrir_url(url)
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
		if series_name == "24 hours": series_name = "24"
		try:
			url = 'http://thetvdb.com/api/GetSeries.php?seriesname=' + urllib.quote(series_name)+'&language=pt'
			html_source = MASH_abrir_url(url)
		except: html_source = ''
		balisa = re.findall('<Series>(.+?)</Series>', html_source, re.DOTALL)
		#addLink(str(len(balisa))+series_name,'','')
		if balisa:
                        for balisas in balisa:
                                sid = re.compile('<seriesid>(.+?)</seriesid>').findall(balisas)
                                overview = re.compile('<Overview>(.+?)</Overview>').findall(balisas)
                                aired = re.compile('<FirstAired>(.+?)-.+?-.+?</FirstAired>').findall(balisas)
                                if aired:
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
                        try: data = MASH_abrir_url(url_tmdb)
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
                        try: data = MASH_abrir_url(url_tmdb)
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
                                try: data = MASH_abrir_url(url_tmdb)
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
                        try: data = MASH_abrir_url(url_tmdb)
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
                                try: data = MASH_abrir_url(url_tmdb)
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


def ultimos_episodios(url):
        conta_os_items = 0
        a = 1
        percent = 0
        message = ''
        site = ''
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar ...'+site, message, "" )
        urlss = urllib.unquote(url)
        print urlss
        urls=re.compile('url_TFC=(.+?)&url_MVT=(.+?)&url_TFV=(.+?)&xpto=xpto&url_TPT=(.+?)&fim=fim').findall(urlss)
        url_TFV = urls[0][2]
        url_TFC = urls[0][0]
        url_MVT = urls[0][1]
        url_TPT = urls[0][3]
        #i = int(arr_filmes[4])
        i = 0
        #--------------------------------------------------
        num = 0
##        try:
##		html_source = MASH_abrir_url(url_TFV)
##	except: html_source = ''
##	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
##	if items != []:
##		num = len(items)
##	try:
##		html_source = MASH_abrir_url(url_TPT)
##	except: html_source = ''
##	items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
##	if items != []:
##		num = num + len(items)
	num = 29 + 0.0
	#----------------------------------------------------------------------------------------------------
	site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
        progress.update( percent, 'A Procurar Últimos Episódios em '+site, message, "" )
        i = 1
        try:
		html_source = MASH_abrir_url(url_TPT)
	except: html_source = ''
	items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        sinopse = ''
                        fanart = ''
                        thumb = ''
                        qualidade = ''
                        
                        audio_filme = ''
                        
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

                        percent = int( ( i / num ) * 100)
                        message = nome
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        
                        n = re.compile('(.+?)[[].+?[]]').findall(nome)
                        if n: nome_pesquisa = n[0]
                        thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme)
                        ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                        if ftart:  
                                fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                if thumb == '': thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                        snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                        if snpse and sinopse == '': sinopse = snpse[0]
      
                        ano_filme = '('+ano_filme+')'
                        qualidade = '('+qualidade
                        audio_filme = audio_filme+')'
                        try:
                                addDir_teste('[COLOR orange]TPT | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0],233,thumb,sinopse,fanart.replace('w500','w1280'),ano_filme.replace('(','').replace(')',''),genero)
                        except: pass
                        i = i + 1
        else: pass
        if items != []:
                proxima_TPT = re.compile('</span><a class="nextpostslink" rel="next" href="(.+?)">&raquo;</a><a class="last"').findall(html_source)
                try:
                        url_TPT = proxima_TPT[0].replace('#038;','').replace('&amp;','&')
                except: pass
        else: url_TPT = 'http:'
        #----------------------------------------------------------------------------------------------------
	site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv'
	progress.update(percent, 'A Procurar Últimos Episódios em '+site, message, "")
        try:
		html_source = MASH_abrir_url(url_TFV)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        thumb = ''
                        fanart = ''
                        genero = ''
                        sinopse = ''
                        
                        gene = re.compile("nero</b>:(.+?)<br />").findall(item)
                        if gene: genero = gene[0]
                        else: genero = ''
                        resumo = re.compile("<b>Resumo</b>:(.+?)<br />").findall(item)
                        if resumo: sinopse = resumo[0]
                        else: sinopse = ''
			urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)
			ano = re.compile("<b>Ano</b>: (.+?)<br />").findall(item)
			if ano: ano = '('+ano[0]+')'
			qualidade = re.compile("<b>Qualidade</b>: (.+?)<br />").findall(item)
			if qualidade: qualidade = '('+qualidade[0]+')'
			thumbnail = re.compile('src="(.+?)"').findall(item)
			if thumbnail: thumb = thumbnail[0]
                        else: thumb = ''
			print urletitulo,thumbnail
			nome = urletitulo[0][1]
                        nome = nome.replace('&#8217;',"'")
                        nome = nome.replace('&#8211;',"-")
                        nome = nome.replace('&#39;',"'")
                        nome = nome.replace('&amp;','&')
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        tirar_ano = '(' + str(q_a_q_a) + ')'
                                        nome = nome.replace(tirar_ano,'')

                        percent = int( ( i / num ) * 100)
                        message = nome
                        progress.update( percent, "", message, "" )
                        print str(i) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        
                        n = re.compile('(.+?)[(].+?[)]').findall(nome)
                        if n: nome_original = n[0]
                        else: nome_original = nome

                        nome_pesquisa = nome_original
                        thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano.replace('(','').replace(')',''))
                        ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                        if ftart:
                                fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                if thumb == '' or 's1600' in thumb: thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                        snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                        if snpse and sinopse == '': sinopse = snpse[0]

			try:
				addDir_teste('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] ' + ano + '[/COLOR][COLOR red] ' + qualidade + '[/COLOR]',urletitulo[0][0],42,thumb.replace('s72-c','s320'),sinopse,fanart.replace('w500','w1280'),ano,genero)
			except: pass
			i = i + 1
        else: pass
        if items != []:
                proxima_TFV = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
                url_TFV = proxima_TFV[0].replace('&amp;','&')
        else: url_TFV = 'http:'
        #----------------------------------------------------------------------------------------------------
        url_MVT = 'http:'
        url_TFC = 'http:'
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "fim": 'fim',"xpto":'xpto'}
        url_ultimos_episodios = urllib.urlencode(parameters)
        addDir('[B]Página Seguinte >>[/B]',url_ultimos_episodios,508,artfolder + 'PAGS1.png','','')
        progress.close()

        

        

def Filmes_Filmes_Filmes(url):
        
        #folder = perfil
        
        conta_os_items = 0
        a = 1
        percent = 0
        message = ''
        site = ''
        progress.create('Progresso', 'A Procurar')
        progress.update( percent, 'A Procurar Filmes...'+site, message, "" )
        urlss = urllib.unquote(url)
        print urlss
        #addLink(urlss,'','')
        #return
        urls=re.compile('url_TFC=(.+?)&url_CMT=(.+?)&url_FTT=(.+?)&url_TFV=(.+?)&url_MVT=(.+?)&xpto=xpto&url_CME=(.+?)&url_TPT=(.+?)&fim=fim').findall(urlss)
        url_TFV = urls[0][3]
        url_TFC = urls[0][0]
        url_MVT = urls[0][4]
        url_TPT = urls[0][6]
        url_FTT = urls[0][2]
        url_CMT = urls[0][1]
        url_CME = urls[0][5]
        #i = int(arr_filmes[4])
        i = 1
        #--------------------------------------------------
        num = 0
        try:
		html_source = MASH_abrir_url(url_TFV)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		num = len(items)
	try:
		html_source = MASH_abrir_url(url_TFC)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	try:
		html_source = MASH_abrir_url(url_MVT)
	except: html_source = ''
	items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	try:
		html_source = MASH_abrir_url(url_TPT)
	except: html_source = ''
	items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	try:
		html_source = MASH_abrir_url(url_FTT)
	except: html_source = ''
	items = re.findall("<div class='post-body entry-content'>(.+?)<div class='post-outer'>", html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	try:
		html_source = MASH_abrir_url(url_CMT)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	try:
		html_source = MASH_abrir_url(url_CME)
	except: html_source = ''
	items = re.findall("<h3 class='post-title entry-title'(.+?)<div class='post-outer'>", html_source, re.DOTALL)
	if items != []:
		num = num + len(items)
	num = num + 0.0
	i = 1
        a = 1
	percent = int( ( a / num ) * 100)
        message = str(a) + " de " + str(int(num))
        progress.update( percent, 'A Procurar Filmes...', message, "" )
	#----------------------------------------------------------------------------------------------------
	site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
        progress.update( percent, 'A Procurar Filmes em '+site, message, "" )
        
        _filmes_ = []
        folder = perfil
        Filmes_File = open(folder + 'filmesTPT.txt', 'a')
        Filmes_Fi = open(folder + 'filmesTPT.txt', 'r')
        read_Filmes_File = ''
        for line in Filmes_Fi:
                read_Filmes_File = read_Filmes_File + line
                if line!='':_filmes_.append(line)
        try:
		html_source = MASH_abrir_url(url_TPT)
	except: html_source = ''
	items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:

                        sinopse = ''
                        genero = ''
                        fanart = ''
                        thumb = ''
                        qualidade = ''
                        imdbcode = ''
                        audio_filme = ''
                                
                        urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(item)
                        if 'title=' in urletitulo[0][0]: urletitulo = re.compile('<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>').findall(item)
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

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                                
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        progress.update( percent, 'A Procurar Filmes em '+site, message, "" )
                        print str(a) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                                
                                
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
                        O_Nome = nome
                        n_f = re.compile('.net/(.*)').findall(urletitulo[0][0])
                        nome_filme = n_f[0]#nome
                        if nome_filme in read_Filmes_File:
                                for x in range(len(_filmes_)):
                                        if nome_filme in _filmes_[x]:
                                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_filmes_[x])
                                                if _n: nomes = _n[0]
                                                else: nomes = '---'
                                                if nome_filme == nomes:
                                                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_filmes_[x])
                                                        if _i: imdbcode = _i[0]
                                                        else: imdbcode = '---'
                                                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_filmes_[x])
                                                        if _t: thumb = _t[0]
                                                        else: thumb = '---'
                                                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_filmes_[x])
                                                        if _a: ano_filme = _a[0]
                                                        else: ano_filme = '---'
                                                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_filmes_[x])
                                                        if _f: fanart = _f[0]
                                                        else: fanart = '---'
                                                        _g = re.compile('[|]GENERO[|](.+?)[|]SINOPSE[|]').findall(_filmes_[x])
                                                        if _g: genero = _g[0]
                                                        else: genero = '---'
                                                        _s = re.compile('[|]SINOPSE[|](.*)').findall(_filmes_[x])
                                                        if _s: s = _s[0]
                                                        if '|END|' in s: sinopse = s.replace('|END|','')
                                                        else:
                                                                si = re.compile('SINOPSE[|](.+?)\n(.+?)[|]END[|]').findall(_filmes_[x])
                                                                if si: sinopse = si[0][0] + ' ' + si[0][1]
                                                                else: sinopse = '---'
                        else:
                                if fanart == '': fanart = '---'
                                if genero == '': genero = '---'
                                if sinopse == '': sinopse = '---'
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
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

                                Filmes_File.write('NOME|'+str(nome_filme)+'|IMDBCODE|'+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb)+'|ANO|'+str(ano_filme.replace('(','').replace(')',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|SINOPSE|'+str(sinopse)+'|END|\n')
                                
                        if fanart == '---': fanart = ''
                        ano_filme = '('+ano_filme+')'
                        qualidade = '('+qualidade
                        audio_filme = audio_filme+')'
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        try:
                                if 'IMDB' in imdbcode:
                                        addDir_teste('[COLOR orange]TPT | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0]+imdbcode,233,thumb,sinopse,fanart.replace('w500','w1280'),ano_filme.replace('(','').replace(')',''),genero)
                                else:
                                        addDir_teste('[COLOR orange]TPT | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',233,thumb,sinopse,fanart.replace('w500','w1280'),ano_filme.replace('(','').replace(')',''),genero)
                                # addDir_teste('[COLOR orange]TPT | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow] ' + ano_filme + '[/COLOR][COLOR red] ' + qualidade + audio_filme + '[/COLOR]',urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',233,thumb,'[COLOR yellow]INFO:[/COLOR][COLOR red]'+qualidade.replace('(','')+audio_filme.replace(')','')+'[/COLOR]'+'\n'+sinopse,fanart.replace('w500','w1280'),ano_filme.replace('(','').replace(')',''),genero)
                        except: pass
                        i = i + 1
                        a = a + 1
                
        else: pass
        if items != []:
                proxima_TPT = re.compile('</span><a class="nextpostslink" rel="next" href="(.+?)">&raquo;</a><a class="last"').findall(html_source)
                try:
                        url_TPT = proxima_TPT[0].replace('#038;','').replace('&amp;','&')
                except: pass
        else: url_TPT = 'http:'
        Filmes_File.close()
        Filmes_Fi.close()
        
        #----------------------------------------------------------------------------------------------------
        site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].com'
        progress.update( percent, 'A Procurar Filmes em '+site, message, "" )
        i = 1
        _filmes_ = []
        folder = perfil
        Filmes_File = open(folder + 'filmesTFC.txt', 'a')
        Filmes_Fi = open(folder + 'filmesTFC.txt', 'r')
        read_Filmes_File = ''
        for line in Filmes_Fi:
                read_Filmes_File = read_Filmes_File + line
                if line!='':_filmes_.append(line)
        try:
		html_source = MASH_abrir_url(url_TFC)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
                        print str(a) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        #if selfAddon.getSetting('movie-fanart-TFC') == "false": xbmc.sleep( 50 )
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
                        O_Nome = nome
                        n_f = re.compile('.info/(.+?)[.]html').findall(urletitulo[0][0])
                        nome_filme = n_f[0]#nome
                        if nome_filme in read_Filmes_File:
                                for x in range(len(_filmes_)):
                                        if nome_filme in _filmes_[x]:
                                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_filmes_[x])
                                                if _n: nomes = _n[0]
                                                else: nomes = '---'
                                                if nome_filme == nomes:
                                                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_filmes_[x])
                                                        if _i: imdbcode = _i[0]
                                                        else: imdbcode = '---'
                                                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_filmes_[x])
                                                        if _t: thumb = _t[0]
                                                        else: thumb = '---'
                                                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_filmes_[x])
                                                        if _a: ano = _a[0]
                                                        else: ano = '---'
                                                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_filmes_[x])
                                                        if _f: fanart = _f[0]
                                                        else: fanart = '---'
                                                        _g = re.compile('[|]GENERO[|](.+?)[|]SINOPSE[|]').findall(_filmes_[x])
                                                        if _g: genero = _g[0]
                                                        else: genero = '---'
##                                                        _s = re.compile('[|]SINOPSE[|](.*)').findall(_filmes_[x])
##                                                        if _s: s = _s[0]
##                                                        if '|END|' in s: sinopse = s.replace('|END|','')
##                                                        else:
##                                                                si = re.compile('SINOPSE[|](.+?)\n(.+?)[|]END[|]').findall(_filmes_[x])
##                                                                if si: sinopse = si[0][0] + ' ' + si[0][1]
##                                                                else: sinopse = '---'
                        else:
                                if genero == '': genero = '---'
                                if sinopse == '': sinopse = '---'
                                if fanart == '': fanart = '---'
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
                                if qualidade == '': qualidade = '---'
                                nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?)[[].+?[]]').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
                                if not nnnn: nnnn = re.compile('(.+?)[:] ').findall(nome)
                                if nnnn : nome_pesquisa = nnnn[0]
                                if nnnn: nome_pesquisa = nnnn[0]
                                else: nome_pesquisa = nome
                                #fanart,tmdb_id,poster,overview = themoviedb_api_IMDB().fanart_and_id(str(imdbcode),ano_filme)
                                try:
                                        fanart,tmdb_id,poster = themoviedb_api().fanart_and_id(nome_pesquisa,ano)
                                        if thumb == '': thumb = poster
                                except: pass
##                                addLink(ano,'','')
##                                addLink(fanart,'','')
##                                addLink(thumb,'','')
##                                addLink(nome_filme,'','')
##                                addLink(genero,'','')
##                                addLink(sinopse,'','')
##                                addLink(imdbcode,'','')
                                Filmes_File.write('NOME|'+str(nome_filme)+'|IMDBCODE|'+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb.replace('s1600','s320').replace('.gif','.jpg'))+'|ANO|'+str(ano.replace('(','').replace(')',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|END|\n')
                                #Filmes_File.write('NOME|'+nome_filme+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|THUMB|'+thumb.replace('s1600','s320').replace('.gif','.jpg')+'|ANO|'+ano.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|\n')

                        
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        if qualidade == '': qualidade = '---'
			try:
                                if 'ASSISTIR O FILME' in item:
                                        if 'IMDB' in imdbcode:
                                                addDir_teste('[COLOR orange]TFC | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR][COLOR red] (' + qualidade + ')[/COLOR]' + versao,urletitulo[0][0]+imdbcode,73,thumb.replace('s1600','s320').replace('.gif','.jpg'),sinopse,fanart.replace('w500','w1280'),ano,qualidade)
                                        else:
                                                addDir_teste('[COLOR orange]TFC | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR][COLOR red] (' + qualidade + ')[/COLOR]' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',73,thumb.replace('s1600','s320').replace('.gif','.jpg'),sinopse,fanart.replace('w500','w1280'),ano,qualidade)
			except: pass
			a = a + 1
                        i = i + 1
                
        else: pass
        if items != []:
                proxima_TFC = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
                url_TFC = proxima_TFC[0].replace('&amp;','&')
        else: url_TFC = 'http:'
        Filmes_File.close()
        Filmes_Fi.close()
        #----------------------------------------------------------------------------------------------------
        site = '[B][COLOR green]FOIT[/COLOR][COLOR yellow]A[/COLOR][COLOR red]TUGA[/COLOR][/B]'
	progress.update(percent, 'A Procurar Filmes em '+site, message, "")
	_filmes_ = []
        folder = perfil
        Filmes_File = open(folder + 'filmesFTT.txt', 'a')
        Filmes_Fi = open(folder + 'filmesFTT.txt', 'r')
        read_Filmes_File = ''
        for line in Filmes_Fi:
                read_Filmes_File = read_Filmes_File + line
                if line!='':_filmes_.append(line)
        try:
		html_source = MASH_abrir_url(url_FTT)
	except: html_source = ''
	items = re.findall("<a class='comment-link'(.+?)<div class='post-outer'>", html_source, re.DOTALL)
	if items != []:
		for item in items:
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
                        print str(a) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        #if selfAddon.getSetting('movie-fanart-FTT') == "false": xbmc.sleep( 50 )

                        genero = ''
                        sinopse = ''
                        thumb = ''
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

                        snpse = re.compile('Sinopse.png"></a></div>\n(.+?)\n').findall(item)
                        if not snpse: snpse = re.compile('Sinopse.png" /></a></div>\n(.+?)\n').findall(item)
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
                        if '[PT/PT]' in nome:
                                audio_filme = 'PT/PT'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')
                        if '(PT-PT)' in nome:
                                audio_filme = 'PT-PT'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')
                        if '(PT/BR)' in nome:
                                audio_filme = 'PT/BR'
                                nome = nome.replace('-'+audio_filme,'')
                                nome = nome.replace('- '+audio_filme,'')
                                nome = nome.replace(audio_filme,'')
                        if '(PT-BR)' in nome:
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

                        if audio_filme != '': qualidade_filme = qualidade_filme# + ' - ' + audio_filme

                        nome = nome.replace('((','(')
                        nome = nome.replace('))',')')
                        nome = nome.replace('()','(')
                        nome = nome.replace('  ','')
                        nome = nome.replace(' - []','')

                        O_Nome = nome
                        n_f = re.compile('.pt/(.+?)[.]html').findall(urletitulo[0][0])
                        nome_filme = n_f[0]#nome
                        if nome_filme in read_Filmes_File:
                                for x in range(len(_filmes_)):
                                        if nome_filme in _filmes_[x]:
                                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_filmes_[x])
                                                if _n: nomes = _n[0]
                                                else: nomes = '---'
                                                if nome_filme == nomes:
                                                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_filmes_[x])
                                                        if _i: imdbcode = _i[0]
                                                        else: imdbcode = '---'
                                                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_filmes_[x])
                                                        if _t: thumb = _t[0]
                                                        else: thumb = '---'
                                                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_filmes_[x])
                                                        if _a: ano_filme = _a[0]
                                                        else: ano_filme = '---'
                                                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_filmes_[x])
                                                        if _f: fanart = _f[0]
                                                        else: fanart = '---'
                                                        _g = re.compile('[|]GENERO[|](.+?)[|]SINOPSE[|]').findall(_filmes_[x])
                                                        if _g: genero = _g[0]
                                                        else: genero = '---'
                                                        _q = re.compile('[|]QUALIDADE[|](.+?)[|]END[|]').findall(_filmes_[x])
                                                        if _q: qualidade_filme = _q[0]
                                                        else: qualidade_filme = ''
                        else:
                                
                                try:
                                        fonte_video = MASH_abrir_url(urlvideo)
                                except: fonte_video = ''
                                fontes_video = re.findall("<div class='post-body entry-content'>(.*?)<div style='clear: both;'>", fonte_video, re.DOTALL)
                                if fontes_video != []:
                                        qualid = re.compile('ASSISTIR ONLINE (.*)\n').findall(fontes_video[0])
                                        if qualid: qualidade_filme = qualid[0].replace('/ ',' ').replace('</b>','').replace('</span>','').replace('LEGENDADO','')
                                        else:
                                                qualid = re.compile('[[]</span><span style=".+?"><span style=".+?">(.+?)</span><span style=".+?">[]]').findall(fontes_video[0])
                                                if qualid: qualidade_filme = qualid[0].replace('/ ','').replace('</b>','').replace('</span>','')
                                                else: qualidade_filme = '---'
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
                                if fanart == '': fanart = '---'
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
                                Filmes_File.write('NOME|'+nome_filme+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|THUMB|'+str(thumb)+'|ANO|'+anofilme+'|FANART|'+str(fanart)+'|GENERO|'+genero+'|QUALIDADE|'+qualidade_filme.replace('</div>','')+'|END|\n')

                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        try:
                                if 'IMDB' in imdbcode:
                                        addDir_teste('[COLOR orange]FTT | [/COLOR][B][COLOR green]' + O_Nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme.replace('</div>','') + ')[/COLOR]',urlvideo+imdbcode,603,thumb,sinopse,fanart.replace('w500','w1280'),anofilme,genero)
                                else:
                                        addDir_teste('[COLOR orange]FTT | [/COLOR][B][COLOR green]' + O_Nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme.replace('</div>','') + ')[/COLOR]',urlvideo+'IMDB'+imdbcode+'IMDB',603,thumb,sinopse,fanart.replace('w500','w1280'),anofilme,genero)
                        except: pass
                        i = i + 1
                        a = a + 1
                        
                        #---------------------------------------------------------------
	else: pass	
	if items != []:
                proxima = re.compile("<a class='blog-pager-older-link' href='(.+?)' id='Blog1_blog-pager-older-link'").findall(html_source)
                proxima_p = proxima[0]
		url_FTT = proxima_p.replace('&amp;','&')
	else: url_FTT = 'http:'
	Filmes_File.close()
        Filmes_Fi.close()
#------------------------------------------------------------------------------------------------------------------------
	site = '[B][COLOR green]CINE[/COLOR][COLOR yellow]M[/COLOR][COLOR red]ATUGA.net[/COLOR][/B]'
	progress.update(percent, 'A Procurar Filmes em '+site, message, "")
	_filmes_ = []
        folder = perfil
        Filmes_File = open(folder + 'filmesCMT.txt', 'a')
        Filmes_Fi = open(folder + 'filmesCMT.txt', 'r')
        read_Filmes_File = ''
        for line in Filmes_Fi:
                read_Filmes_File = read_Filmes_File + line
                if line!='':_filmes_.append(line)
        try:
		html_source = MASH_abrir_url(url_CMT)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	conta_items = 0
	if items != []:
		print len(items)
		for item in items:
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
                        print str(a) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        #if selfAddon.getSetting('movie-fanart-CMT') == "false": xbmc.sleep( 50 )
                        thumb = ''
                        fanart = ''
                        versao = ''
                        genero = ''
                        sinopse = ''
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
                        else:
                                titulooriginal = re.compile("<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>(.+?)<br />").findall(item)
                                if titulooriginal:
                                        nome_original = titulooriginal[0]
                                else: nome_original = ''
                        urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(item)
                        qualidade = re.compile("<b>Qualidade</b>: (.+?)<br />").findall(item)
                        if not qualidade: qualidade = re.compile("Ass.+?tir online .+?[(](.+?)[)]").findall(item)
                        if qualidade: qualidade = qualidade[0].replace('<b>','').replace('</b>','')
                        else: qualidade = ''
                        ano = re.compile("<b>Ano</b>: (.+?)<br />").findall(item)
                        if ano: ano_filme = ano[0]
                        else: ano_filme = ''
                        #return
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
                        nome = nome.replace('(PT-BR)',"")
                        nome = nome.replace('(PT/BR)',"")
                        nome = nome.replace('[PT-PT]',"")
                        nome = nome.replace('[PT/PT]',"")
                        nome = nome.replace('PT-PT)',"")
                        nome = nome.replace('PT/PT)',"")
                        nome = nome.replace('PT-PT]',"")
                        nome = nome.replace('PT/PT]',"")
                        a_q = re.compile('\d+')
                        qq_aa = a_q.findall(nome)
                        for q_a_q_a in qq_aa:
                                if len(q_a_q_a) == 4:
                                        tirar_ano = '(' + str(q_a_q_a) + ')'
                                        nome = nome.replace(tirar_ano,'')
                                        if ano_filme == '': ano_filme = str(q_a_q_a)
                        O_Nome = nome
                        n_f = re.compile('.org/(.+?)[.]html').findall(urletitulo[0][0])
                        nome_filme = n_f[0]#nome
                        if nome_filme in read_Filmes_File:
                                for x in range(len(_filmes_)):
                                        if nome_filme in _filmes_[x]:
                                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_filmes_[x])
                                                if _n: nomes = _n[0]
                                                else: nomes = '---'
                                                if nome_filme == nomes:
                                                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_filmes_[x])
                                                        if _i: imdbcode = _i[0]
                                                        else: imdbcode = '---'
                                                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_filmes_[x])
                                                        if _t: thumb = _t[0]
                                                        else: thumb = '---'
                                                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_filmes_[x])
                                                        if _a: ano_filme = _a[0]
                                                        else: ano_filme = '---'
                                                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_filmes_[x])
                                                        if _f: fanart = _f[0]
                                                        else: fanart = '---'
                                                        _g = re.compile('[|]GENERO[|](.+?)[|]SINOPSE[|]').findall(_filmes_[x])
                                                        if _g: genre = _g[0]
                                                        else: genre = '---'
##                                                        _s = re.compile('[|]SINOPSE[|](.*)').findall(_filmes_[x])
##                                                        if _s: s = _s[0]
##                                                        if '|END|' in s: sinopse = s.replace('|END|','')
##                                                        else:
##                                                                si = re.compile('SINOPSE[|](.+?)\n(.+?)[|]END[|]').findall(_filmes_[x])
##                                                                if si: sinopse = si[0][0] + ' ' + si[0][1]
##                                                                else: sinopse = '---'
                        else:
                                if thumb == '': thumb = poster
                                if genre == '': genre = '---'
                                if sinopse == '': sinopse = '---'
                                if fanart == '': fanart = '---'
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
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
                                Filmes_File.write('NOME|'+str(nome_filme)+'|IMDBCODE|'+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb.replace('s72-c','s320'))+'|ANO|'+str(ano_filme.replace(' ',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(genre)+'|END|\n')
                                                      
                        if thumb == '': thumb = poster
                        if genre == '': genre = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        
                        
                        try:
                                if "Temporada" in urletitulo[0][1]:
                                        num_mode = 712
                                else:
                                        num_mode = 703
                                if 'IMDB' in imdbcode:
                                        addDir_teste('[COLOR orange]CMT | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow](' + ano_filme.replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+imdbcode,num_mode,thumb.replace('s72-c','s320'),sinopse,fanart.replace('w500','w1280'),ano_filme.replace(' ',''),genre)
                                else:
                                        addDir_teste('[COLOR orange]CMT | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow](' + ano_filme.replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',num_mode,thumb.replace('s72-c','s320'),sinopse,fanart.replace('w500','w1280'),ano_filme.replace(' ',''),genre)

                        except: pass
                        #---------------------------------------------------------------
                        i = i + 1
                        a = a + 1
                        #---------------------------------------------------------------

	else: pass
	if items != []:
                        proxima = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
                        url_CMT = proxima[0].replace('&amp;','&')
        else: url_CMT = 'http:'
        Filmes_File.close()
        Filmes_Fi.close()
#------------------------------------------------------------------------------------------------------------------------------------
	site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv'
	progress.update(percent, 'A Procurar Filmes em '+site, message, "")
	_filmes_ = []
        folder = perfil
        Filmes_File = open(folder + 'filmesTFV.txt', 'a')
        Filmes_Fi = open(folder + 'filmesTFV.txt', 'r')
        read_Filmes_File = ''
        for line in Filmes_Fi:
                read_Filmes_File = read_Filmes_File + line
                if line!='':_filmes_.append(line)
        try:
		html_source = MASH_abrir_url(url_TFV)
	except: html_source = ''
	items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
                        print str(a) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        #if selfAddon.getSetting('movie-fanart-TFV') == "false": xbmc.sleep( 50 )
                        thumb = ''
                        fanart = ''
                        versao = ''
                        audio_filme = ''
                        imdbcode = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
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
                        else:
                                titulooriginal = re.compile("<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>(.+?)<br />").findall(item)
                                if titulooriginal:
                                        nome_original = titulooriginal[0]
                                else: nome_original = ''
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
                        if qualidade: qualidade = qualidade[0]
                        else: qualidade = ''
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
                                        
                        O_Nome = nome
                        n_f = re.compile('.us/(.+?)[.]html').findall(urletitulo[0][0])
                        nome_filme = n_f[0]#nome
                        if nome_filme in read_Filmes_File:
                                for x in range(len(_filmes_)):
                                        if nome_filme in _filmes_[x]:
                                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_filmes_[x])
                                                if _n: nomes = _n[0]
                                                else: nomes = '---'
                                                if nome_filme == nomes:
                                                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_filmes_[x])
                                                        if _i: imdbcode = _i[0]
                                                        else: imdbcode = '---'
                                                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_filmes_[x])
                                                        if _t: thumb = _t[0]
                                                        else: thumb = '---'
                                                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_filmes_[x])
                                                        if _a: ano_filme = _a[0]
                                                        else: ano_filme = '---'
                                                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_filmes_[x])
                                                        if _f: fanart = _f[0]
                                                        else: fanart = '---'
                                                        _g = re.compile('[|]GENERO[|](.+?)[|]SINOPSE[|]').findall(_filmes_[x])
                                                        if _g: genre = _g[0]
                                                        else: genre = '---'
                        else:
                                if thumb == '': thumb = '---'
                                if genre == '': genre = '---'
                                if sinopse == '': sinopse = '---'
                                if fanart == '---': fanart = ''
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
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
                                

                                Filmes_File.write('NOME|'+str(nome_filme)+'|IMDBCODE|'+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb.replace('s72-c','s320'))+'|ANO|'+str(ano[0].replace(' ',''))+'|FANART|'+str(fanart)+'|GENERO|'+str(genre)+'|END|\n')
   
                        if thumb == '': thumb = '---'
                        if genre == '': genre = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        
                        
                        try:
                                if "Temporada" in urletitulo[0][1] or 'Season'  in urletitulo[0][1] or 'Mini-Série' in urletitulo[0][1]:
                                        num_mode = 42
                                else:
                                        num_mode = 33
                                if 'IMDB' in imdbcode:
                                        addDir_teste('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+imdbcode,num_mode,thumb.replace('s72-c','s320'),sinopse,fanart.replace('w500','w1280'),ano[0].replace(' ',''),genre)
                                else:
                                        addDir_teste('[COLOR orange]TFV | [/COLOR][B][COLOR green]' + O_Nome + '[/COLOR][/B][COLOR yellow](' + ano[0].replace(' ','') + ')[/COLOR][COLOR red] (' + qualidade + audio_filme + ')[/COLOR] ' + versao,urletitulo[0][0]+'IMDB'+imdbcode+'IMDB',num_mode,thumb.replace('s72-c','s320'),sinopse,fanart.replace('w500','w1280'),ano[0].replace(' ',''),genre)
                        except: pass
                        i = i + 1
                        a = a + 1
        else: pass
        if items != []:
                proxima_TFV = re.compile(".*href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)
                url_TFV = proxima_TFV[0].replace('&amp;','&')
        else: url_TFV = 'http:'
        Filmes_File.close()
        Filmes_Fi.close()
        #----------------------------------------------------------------------------------------------------
        progress.update( percent, 'A Procurar Filmes em '+site, message, "" )
        site = '[B][COLOR green]MOVIE[/COLOR][COLOR yellow]-[/COLOR][COLOR red]TUGA[/COLOR][/B]'
        i = 3
        _filmes_ = []
        folder = perfil
        Filmes_File = open(folder + 'filmesMVT.txt', 'a')
        Filmes_Fi = open(folder + 'filmesMVT.txt', 'r')
        read_Filmes_File = ''
        for line in Filmes_Fi:
                read_Filmes_File = read_Filmes_File + line
                if line!='':_filmes_.append(line)
	try:
		html_source = MASH_abrir_url(url_MVT)
	except: html_source = ''
	items = re.findall('<div class=\'entry\'>(.+?)<div class="btnver">', html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
                        print str(a) + " de " + str(int(num))
                        if progress.iscanceled():
                                break

                        thumb = ''
                        genero = ''
                        sinopse = ''
                        fanart = ''
                        imdbcode = ''

                        imdb = re.compile('imdb.com/title/(.+?)/').findall(item)
                        if imdb: imdbcode = imdb[0]
                        else: imdbcode = ''
                        
                        url = re.compile('<div class="btns"><a href="(.+?)" target="Player">').findall(item)
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
                        #return
                        O_Nome = nome
                        n_f = re.compile('filmes/(.+?)[.]pt[.]vu').findall(url[0].replace(' ','%20'))
                        nome_filme = n_f[0]#nome
                        #return
                        if nome_filme in read_Filmes_File:
                                for x in range(len(_filmes_)):
                                        if nome_filme in _filmes_[x]:
                                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_filmes_[x])
                                                if _n: nomes = _n[0]
                                                else: nomes = '---'
                                                if nome_filme == nomes:
                                                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_filmes_[x])
                                                        if _i: imdbcode = _i[0]
                                                        else: imdbcode = '---'
                                                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_filmes_[x])
                                                        if _t: thumb = _t[0]
                                                        else: thumb = '---'
                                                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_filmes_[x])
                                                        if _a: ano_filme = _a[0]
                                                        else: ano_filme = '---'
                                                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_filmes_[x])
                                                        if _f: fanart = _f[0]
                                                        else: fanart = '---'
                                                        _g = re.compile('[|]GENERO[|](.+?)[|]SINOPSE[|]').findall(_filmes_[x])
                                                        if _g: genero = _g[0]
                                                        else: genero = '---'
                        else:
                                if thumb == '': thumb = '---'
                                if genero == '': genero = '---'
                                if sinopse == '': sinopse = '---'
                                if fanart == '': fanart = '---'
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
                                if ano: ano_filme = ano[0].replace('20013','2013').replace(' ','')
                                else: ano_filme = '---'
        ##                        nnnn = re.compile('.+?[(](.+?)[)]').findall(nome)
        ##                        if not nnnn: nnnn = re.compile('.+?[[](.+?)[]]').findall(nome)
        ##                        #if not nnnn: nnnn = re.compile('(.+?)[:]').findall(nome)
        ##                        #if not nnnn: nnnn = re.compile('(.+?) [-] ').findall(nome)
        ##                        if nnnn : nome_pesquisa = nnnn[0]
        ##                        else: nome_pesquisa = nome
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

                                Filmes_File.write('NOME|'+str(nome_filme)+'|IMDBCODE|'+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb.replace(' ','%20'))+'|ANO|'+str(ano_filme)+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|END|\n')
                        
                        if thumb == '': thumb = '---'
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        if ano: ano_filme = ano[0]
                        else: ano_filme = '---'
                        try:
                                if 'IMDB' in imdbcode:
                                        addDir_teste('[COLOR orange]MVT | [/COLOR][B][COLOR green]' + O_Nome + ' [/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',url[0].replace(' ','%20')+imdbcode,103,thumb.replace(' ','%20'),sinopse,fanart.replace('w500','w1280').replace(' ','%20'),ano_filme,genero)
                                else:
                                        addDir_teste('[COLOR orange]MVT | [/COLOR][B][COLOR green]' + O_Nome + ' [/COLOR][/B][COLOR yellow](' + ano_filme + ')[/COLOR][COLOR red] (' + qualidade_filme + ')[/COLOR]',url[0].replace(' ','%20')+'IMDB'+imdbcode+'IMDB',103,thumb.replace(' ','%20'),sinopse,fanart.replace('w500','w1280').replace(' ','%20'),ano_filme,genero)

                        except: pass
                        a = a + 1
                        i = i + 1
        else: pass
        if items != []:
                proxima_MVT = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
                try:
                        url_MVT = proxima_MVT[0].replace('%3A',':')
                        url_MVT = proxima_MVT[0].replace('&amp;','&')
                except: pass
        else: url_MVT = 'http:'
        Filmes_File.close()
        Filmes_Fi.close()
        #----------------------------------------------------------------------------------------------------
        progress.update( percent, 'A Procurar Filmes em '+site, message, "" )
        site = '[B][COLOR green]CINE[/COLOR][COLOR yellow]M[/COLOR][COLOR red]ATUGA.eu[/COLOR][/B]'
        i = 3
        _filmes_ = []
        folder = perfil
        Filmes_File = open(folder + 'filmesCME.txt', 'a')
        Filmes_Fi = open(folder + 'filmesCME.txt', 'r')
        read_Filmes_File = ''
        for line in Filmes_Fi:
                read_Filmes_File = read_Filmes_File + line
                if line!='':_filmes_.append(line)
        try:
		html_source = MASH_abrir_url(url_CME)
	except: html_source = ''
	items = re.findall("<h3 class='post-title entry-title'(.+?)<div class='post-outer'>", html_source, re.DOTALL)
	if items != []:
		for item in items:
                        percent = int( ( a / num ) * 100)
                        message = str(a) + " de " + str(int(num))
                        progress.update(percent, 'A Procurar Filmes em '+site, message, "")
                        print str(a) + " de " + str(int(num))
                        if progress.iscanceled():
                                break
                        
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

                        O_Nome = nome
                        n_f = re.compile('.eu/(.+?)[.]html').findall(urlvideo)
                        nome_filme = n_f[0]#nome
                        if nome_filme in read_Filmes_File:
                                for x in range(len(_filmes_)):
                                        if nome_filme in _filmes_[x]:
                                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_filmes_[x])
                                                if _n: nomes = _n[0]
                                                else: nomes = '---'
                                                if nome_filme == nomes:
                                                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_filmes_[x])
                                                        if _i: imdbcode = _i[0]
                                                        else: imdbcode = '---'
                                                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_filmes_[x])
                                                        if _t: thumb = _t[0]
                                                        else: thumb = '---'
                                                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_filmes_[x])
                                                        if _a: ano_filme = _a[0]
                                                        else: ano_filme = '---'
                                                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_filmes_[x])
                                                        if _f: fanart = _f[0]
                                                        else: fanart = '---'
                                                        _g = re.compile('[|]GENERO[|](.+?)[|]SINOPSE[|]').findall(_filmes_[x])
                                                        if _g: genero = _g[0]
                                                        else: genero = '---'
                        else:
                                if genero == '': genero = '---'
                                if sinopse == '': sinopse = '---'
                                if fanart == '---': fanart = ''
                                if imdbcode == '': imdbcode = '---'
                                if thumb == '': thumb = '---'
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
                                Filmes_File.write('NOME|'+str(nome_filme)+'|IMDBCODE|'+'IMDB'+str(imdbcode)+'IMDB'+'|THUMB|'+str(thumb)+'|ANO|'+str(ano_filme)+'|FANART|'+str(fanart)+'|GENERO|'+str(genero)+'|END|\n')
                        
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '---': fanart = ''
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        try:
                                if 'IMDB' in imdbcode:
                                        addDir_teste('[COLOR orange]CME | [/COLOR][B][COLOR green]' + O_Nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme.replace('</div>','') + ')[/COLOR]',urlvideo+imdbcode,803,thumb,sinopse,fanart,anofilme,genero)
                                else:
                                        addDir_teste('[COLOR orange]CME | [/COLOR][B][COLOR green]' + O_Nome + ' [/COLOR][/B][COLOR yellow](' + anofilme + ')[/COLOR][COLOR red] (' + qualidade_filme.replace('</div>','') + ')[/COLOR]',urlvideo+'IMDB'+imdbcode+'IMDB',803,thumb,sinopse,fanart,anofilme,genero)
                        except: pass
                        #---------------------------------------------------------------
                        i = i + 1
                        a = a + 1
                        #---------------------------------------------------------------
        else: pass
        if items != []:
                proxima_CME = re.compile("<a class='blog-pager-older-link' href='(.+?)' id='Blog1_blog-pager-older-link'").findall(html_source)	
                try:
                        url_CME = proxima_CME[0].replace('&amp;','&')
                except: pass
	else: url_CME = 'http:'
        Filmes_File.close()
        Filmes_Fi.close()
       #----------------------------------------------------------------------------------------------------
	
        for x in range(len(arrai_filmes)):
                if arrai_filmes[x] != '':           #8
                        addDir(arrai_filmes[x],'url',7,thumb_filmes[x],'nao','')
                        conta_os_items = conta_os_items + 1
        parameters = {"url_TFV" : url_TFV, "url_TFC": url_TFC, "url_MVT": url_MVT, "url_TPT": url_TPT, "url_FTT": url_FTT, "url_CMT": url_CMT, "url_CME": url_CME, "fim": 'fim',"xpto":'xpto'}
        url_filmes_filmes = urllib.urlencode(parameters)
        progress.close()
        addDir('[B]Página Seguinte >>[/B]',url_filmes_filmes,507,artfolder + 'PAGS1.png','','')


def Series_Series(url):
        origem = url
        conta_os_items = 0
        folder = perfil
        Series_File = open(folder + 'series.txt', 'a')
        Series_Fi = open(folder + 'series.txt', 'r')
        read_Series_File = ''
        for line in Series_Fi:
                read_Series_File = read_Series_File + line
                if line!='':_series_.append(line)
        if origem == 'urlTODAS':
                percent = 0
                message = ''
                site = ''
                progress.create('Progresso', 'A Procurar')
                progress.update( percent, 'A Procurar Séries...'+site, message, "" )
        #---------------------------------------------------------------------------
        s = 0
        urltfv = 'http://www.tuga-filmes.us'
        try:
                html_series_source = MASH_abrir_url(urltfv)
        except: html_series_source = ''
	html_items_series = re.findall("<div class=\'widget Label\' id=\'Label3\'>\n<h2>S\xc3\xa9ries(.*?)<div class=\'clear\'>", html_series_source, re.DOTALL)
        for item_series in html_items_series:
                series = re.compile("<a dir=\'ltr\' href=\'.+?\'>(.+?)</a>").findall(item_series)
                for nome_series in series:
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        nome_series = nome_series.replace('&#8217;',"'")
                        nome_series = nome_series.replace('&#8230;',"...")
                        nome_series = nome_series.replace('&#8211;',"-")
                        nome_series = nome_series.lower()
                        nome_series = nome_series.title()
                        nome_series = nome_series.replace('Agents Of S.H.I.E.L.D',"Agents Of S.H.I.E.L.D.")
                        _series.append(nome_series)
			s = s + 1
        urltpt = 'http://toppt.net/'
        try:
                html_series_source = MASH_abrir_url(urltpt)
        except: html_series_source = ''
	html_items_series = re.findall('<a href="http://toppt.net/category/series/">SÈRIES NOVAS</a>(.*?)<div class="clearfix">', html_series_source, re.DOTALL)
        print len(html_items_series)
        for item_series in html_items_series:
                series = re.compile('<a href=".+?">(.+?)</a>').findall(item_series)
                for nome_series in series:
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        nome_series = nome_series.replace('&#8217;',"'")
                        nome_series = nome_series.replace('&#8230;',"...")
                        nome_series = nome_series.replace('&#8211;',"-")
                        nome_series = nome_series.replace('Da Vincis Demons',"Da Vinci'S Demons")
                        nome_series = nome_series.lower()
                        nome_series = nome_series.title()
                        if nome_series not in _series:
                                _series.append(nome_series)
				s = s + 1
	html_items_series = re.findall('href="http://toppt.net/category/series/">SÉRIES</a>(.*?)<div id="main">', html_series_source, re.DOTALL)
        print len(html_items_series)
        for item_series in html_items_series:
                series = re.compile('<a href=".+?">(.+?)</a>').findall(item_series)
                for nome_series in series:
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        nome_series = nome_series.replace('&#8217;',"'")
                        nome_series = nome_series.replace('&#8230;',"...")
                        nome_series = nome_series.replace('&#8211;',"-")
                        nome_series = nome_series.replace('Da Vincis Demons',"Da Vinci'S Demons")
                        nome_series = nome_series.lower()
                        nome_series = nome_series.title()
                        if nome_series not in _series:
                                _series.append(nome_series)
				s = s + 1
	#------------------------------------------------------------------------------
        num = s + 0.0
        site = '[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].tv'
        try:
                html_series_source = MASH_abrir_url(urltfv)
        except: html_series_source = ''
	html_items_series = re.findall("<div class=\'widget Label\' id=\'Label3\'>\n<h2>S\xc3\xa9ries(.*?)<div class=\'clear\'>", html_series_source, re.DOTALL)
        i=0
        p=1
        for item_series in html_items_series:
                series = re.compile("<a dir=\'ltr\' href=\'(.+?)\'>(.+?)</a>").findall(item_series)
                for endereco_series,nome_series in series:
                        thumb = ''
                        fanart = ''
                        versao = ''
                        audio_filme = ''
                        imdbcode = ''
                        genre = ''
                        sinopse = ''
                        if origem == 'urlTODAS':
                                percent = int( ( p / num ) * 100)
                                message = str(p) + " de " + str(int(num))
                                progress.update( percent, 'A Procurar Séries em '+site, message, "" )
                                print str(p) + " de " + str(int(num))
                                if progress.iscanceled():
                                        break
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        nome_series = nome_series.replace('&#8217;',"'")
                        nome_series = nome_series.replace('&#8230;',"...")
                        nome_series = nome_series.replace('&#8211;',"-")
                        nome_series = nome_series.lower()
                        nome_series = nome_series.title()
                        nome_series = nome_series.replace('Agents Of S.H.I.E.L.D',"Agents Of S.H.I.E.L.D.")
                        if nome_series in read_Series_File:
                                #arr_series[i] = nome_series
                                for x in range(len(_series_)):
                                        if nome_series in _series_[x]:
                                                #nomeesta = re.compile(
                                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_series_[x])
                                                if _n: nome = _n[0]
                                                else: nome = '---'
                                                if nome_series in nome:
                                                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_series_[x])
                                                        if _i: imdbcode = _i[0]
                                                        else: imdbcode = '---'
                                                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_series_[x])
                                                        if _t: thumb = _t[0]
                                                        else: thumb = '---'
                                                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_series_[x])
                                                        if _a: ano_filme = _a[0]
                                                        else: ano_filme = '---'
                                                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_series_[x])
                                                        if _f: fanart = _f[0]
                                                        else: fanart = '---'
                                                        _g = re.compile('[|]GENERO[|](.+?)[|]SINOPSE[|]').findall(_series_[x])
                                                        if _g: genre = _g[0]
                                                        else: genre = '---'
                                                        _s = re.compile('[|]SINOPSE[|](.*)').findall(_series_[x])
                                                        if _s: s = _s[0]
                                                        if '|END|' in s: sinopse = s.replace('|END|','')
                                                        else:
                                                                si = re.compile('SINOPSE[|](.+?)\n(.+?)[|]END[|]').findall(_series_[x])
                                                                if si: sinopse = si[0][0] + ' ' + si[0][1]
                                                                else: sinopse = '---'
                                                        if fanart == '' or fanart == '---':
                                                                if selfAddon.getSetting('Fanart') == "true":
                                                                        nome_pesquisa = nome_series
                                                                        thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme.replace('(','').replace(')',''))
                                                                        ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                                                        if ftart: fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                                        if thumb == '' or 's1600' in thumb: thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                                                                        snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                                        if sinopse == '---':
                                                                                if snpse: sinopse = snpse[0]
                                                        todas_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|THUMB|'+thumb.replace('s72-c','s320')+'|ANO|'+ano_filme.replace('  ','').replace(' ','')+'|FANART|'+fanart+'|GENERO|'+genre+'|SINOPSE|'+sinopse+'|END|'
                                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|THUMB|'+thumb.replace('s72-c','s320')+'|ANO|'+ano_filme.replace('  ','').replace(' ','')+'|FANART|'+fanart+'|GENERO|'+genre+'|SINOPSE|'+sinopse+'|END|'
                                                        arr_series[i] = nome_series
                                                        
                                                                        
                        else:
                                #return
                                try:
                                        html_source = MASH_abrir_url(endereco_series)
                                except: html_source = ''
                                items = re.findall("<div class=\'video-item\'>(.*?)<div class=\'clear\'>", html_source, re.DOTALL)
                                thumb = ''
                                fanart = ''
                                versao = ''
                                audio_filme = ''
                                imdbcode = ''
                                genre = ''
                                sinopse = ''
                                

                                imdb = re.compile('imdb.com/title/(.+?)/').findall(items[0])
                                if imdb: imdbcode = imdb[0]
                                else: imdbcode = ''
                                #return
                                try:
                                        if 'Portug' and 'Legendado' in items[0]: versao = '[COLOR blue]2 VERSÕES[/COLOR]'
                                        genero = re.compile("nero</b>:(.+?)<br />").findall(items[0])
                                        if genero: genre = genero[0]
                                        else: genre = ''
                                        resumo = re.compile("<b>Resumo</b>:(.+?)<br />").findall(items[0])
                                        if resumo: sinopse = resumo[0]
                                        else: sinopse = ''
                                        sinopse = sinopse.replace('&#8216;',"'")
                                        sinopse = sinopse.replace('&#8217;',"'")
                                        sinopse = sinopse.replace('&#8211;',"-")
                                        sinopse = sinopse.replace('&#8220;',"'")
                                        sinopse = sinopse.replace('&#8221;',"'")
                                        sinopse = sinopse.replace('&#39;',"'")
                                        sinopse = sinopse.replace('&amp;','&')
                                        #return
                                        titulooriginal = re.compile("tulo Original:</b>(.+?)<br />").findall(items[0])
                                        if titulooriginal:
                                                nome_original = titulooriginal[0]
                                        else:
                                                titulooriginal = re.compile("<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>(.+?)<br />").findall(items[0])
                                                if titulooriginal:
                                                        nome_original = titulooriginal[0]
                                                else: nome_original = ''
                                        urletitulo = re.compile("<a href=\'(.+?)' title=\'.+?'>(.+?)</a>").findall(items[0])

                                        tto=re.compile('tulo Original:</b>:(.+?)<br').findall(items[0])
                                        if tto: ttor = tto[0]
                                        else:
                                                tto=re.compile('tulo Original:</b>(.+?)<br').findall(items[0])
                                                if tto: ttor = tto[0]
                                        ttp=re.compile('<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>:(.+?)<br').findall(items[0])
                                        if ttp: ttpo = ttp[0]
                                        else:
                                                ttp=re.compile('<b>T\xc3\xadtulo Portugu\xc3\xaas:</b>(.+?)<br').findall(items[0])
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
                                        
                                        qualidade = re.compile("<b>Qualidade</b>: (.+?)<br />").findall(items[0])
                                        ano = re.compile("<b>Ano</b>: (.+?)<br />").findall(items[0])
                                        audio = re.compile("<b>.+?udio</b>(.+?)<br />").findall(items[0])
                                        imdb_code = re.compile('<b>Mais INFO</b>: <a href="http://www.imdb.com/title/(.+?)/" target="_blank">IMDb</a>').findall(items[0])
                                        if audio != []:
                                                if 'Portug' in audio[0]:
                                                        audio_filme = ': PT-PT'
                                                else:
                                                        audio_filme = audio[0]
                                        thumbnail = re.compile('src="(.+?)"').findall(items[0])
                                        if thumbnail: thumb = thumbnail[0]
                                        else: thumb = ''
                                        print urletitulo,thumb
                                        #nome = urletitulo[0][1]
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
                                                        
                                        if ano: ano_filme = ano[0]
                                        else: ano_filme = '---'
                                        
                                        if selfAddon.getSetting('Fanart') == "true":
                                                nome_pesquisa = nome_series
                                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme.replace('(','').replace(')',''))
                                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                                if ftart: fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                if thumb == '' or 's1600' in thumb: thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                if snpse and sinopse == '': sinopse = snpse[0]

                                        if qualidade:
                                                qualidade = qualidade[0]
                                        else:
                                                qualidade = ''
                                        
                                        if genre == '': genre = '---'
                                        if sinopse == '': sinopse = '---'
                                        if fanart == '': fanart = '---'
                                        if imdbcode == '': imdbcode = '---'
                                        if thumb == '': thumb = '---'
                                        #Series_File.write('NOME|'+nome_series+'|SINOPSE|'+sinopse+'|END|\n')
                                        Series_File.write('NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb.replace('s72-c','s320')+'|ANO|'+ano_filme.replace('  ','').replace(' ','')+'|FANART|'+fanart+'|GENERO|'+genre+'|SINOPSE|'+sinopse+'|END|\n')
                                except: pass
                        #if nome_series in arr_series:
                                #arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|THUMB|'+thumb.replace('s72-c','s320')+'|ANO|'+ano_filme.replace('  ','').replace(' ','')+'|FANART|'+fanart+'|GENERO|'+genre+'|SINOPSE|'+sinopse+'|END|'
                        if genre == '': genre = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '': fanart = '---'
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        if nome_series not in arr_series:
                                if fanart == '' or fanart == '---':
                                        if selfAddon.getSetting('Fanart') == "true":
                                                nome_pesquisa = nome_series
                                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme.replace('(','').replace(')',''))
                                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                                if ftart: fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                if thumb == '' or 's1600' in thumb: thumb = 'http://thetvdb.com/banners/posters/' + ftart[0] + '-1.jpg'
                                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                if sinopse == '---':
                                                        if snpse: sinopse = snpse[0]
                                arr_series[i] = nome_series
                                if 'IMDB' in imdbcode:
                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|'+endereco_series+'|THUMB|'+thumb.replace('s72-c','s320')+'|ANO|'+ano_filme.replace('  ','').replace(' ','')+'|FANART|'+fanart+'|GENERO|'+genre+'|SINOPSE|'+sinopse+'|END|'
                                        todas_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|'+endereco_series+'|THUMB|'+thumb.replace('s72-c','s320')+'|ANO|'+ano_filme.replace('  ','').replace(' ','')+'|FANART|'+fanart+'|GENERO|'+genre+'|SINOPSE|'+sinopse+'|END|'
                                else:
                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb.replace('s72-c','s320')+'|ANO|'+ano_filme.replace('  ','').replace(' ','')+'|FANART|'+fanart+'|GENERO|'+genre+'|SINOPSE|'+sinopse+'|END|'
                                        todas_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb.replace('s72-c','s320')+'|ANO|'+ano_filme.replace('  ','').replace(' ','')+'|FANART|'+fanart+'|GENERO|'+genre+'|SINOPSE|'+sinopse+'|END|'                                
                        i = i + 1
                        p = p + 1
        Series_Fi.close()
        Series_File.close()
        #return
        Series_File = open(folder + 'series.txt', 'a')
        Series_Fi = open(folder + 'series.txt', 'r')
        read_Series_File = ''
        for line in Series_Fi:
                read_Series_File = read_Series_File + line
                if line!='':_series_.append(line)
        url = 'http://toppt.net/'
        site = '[B][COLOR green]TOP[/COLOR][COLOR yellow]-[/COLOR][COLOR red]PT.net[/COLOR][/B]'
        try:
                html_series_source = MASH_abrir_url(url)
        except: html_series_source = ''
	html_items_series = re.findall('<a href="http://toppt.net/category/series/">SÈRIES NOVAS</a>(.*?)<div class="clearfix">', html_series_source, re.DOTALL)
        print len(html_items_series)
        for item_series in html_items_series:
                series = re.compile('<a href="(.+?)">(.+?)</a>').findall(item_series)
                for endereco_series,nome_series in series:
                        genero = ''
                        sinopse = ''
                        fanart = ''
                        thumb = ''
                        qualidade = ''
                        imdbcode = ''
                        audio_filme = ''
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        nome_series = nome_series.replace('&#8217;',"'")
                        nome_series = nome_series.replace('&#8230;',"...")
                        nome_series = nome_series.replace('&#8211;',"-")
                        nome_series = nome_series.replace('NCIS ',"NCIS:")
                        nome_series = nome_series.replace('Da Vincis Demons',"Da Vinci'S Demons")
                        nome_series = nome_series.lower()
                        nome_series = nome_series.title()
                        ##########################################################
                        if nome_series in read_Series_File:
                                #arr_series[i] = nome_series
                                for x in range(len(_series_)):
                                        if nome_series in _series_[x]:
                                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_series_[x])
                                                if _n: nome = _n[0]
                                                else: nome = '---'
                                                if nome_series in nome:
                                                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_series_[x])
                                                        if _i: imdbcode = _i[0]
                                                        else: imdbcode = '---'
                                                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_series_[x])
                                                        if _t: thumb = _t[0]
                                                        else: thumb = '---'
                                                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_series_[x])
                                                        if _a: ano_filme = _a[0]
                                                        else: ano_filme = '---'
                                                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_series_[x])
                                                        if _f: fanart = _f[0]
                                                        else: fanart = '---'
                                                        _g = re.compile('[|]GENERO[|](.+?)[|]SINOPSE[|]').findall(_series_[x])
                                                        if _g: genero = _g[0]
                                                        else: genero = '---'
                                                        _s = re.compile('[|]SINOPSE[|](.*)').findall(_series_[x])
                                                        if _s: s = _s[0]
                                                        if '|END|' in s: sinopse = s.replace('|END|','')
                                                        else:
                                                                si = re.compile('SINOPSE[|](.+?)\n(.+?)[|]END[|]').findall(_series_[x])
                                                                if si: sinopse = si[0][0] + ' ' + si[0][1]
                                                                else: sinopse = '---'
                                                        #arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                                        #arr_series[i] = nome_series
                        else:
                                try:
                                        html_source = MASH_abrir_url(endereco_series)
                                except: html_source = ''
                                items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
                                genero = ''
                                sinopse = ''
                                fanart = ''
                                thumb = ''
                                qualidade = ''
                                imdbcode = ''
                                audio_filme = ''

                                imdb = re.compile('imdb.com/title/(.+?)/').findall(items[0])
                                if imdb: imdbcode = imdb[0]
                                else: imdbcode = ''

                                try:
                                        urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(items[0])
                                        if 'title=' in urletitulo[0][0]: urletitulo = re.compile('<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>').findall(items[0])
                                        
                                        qualid = re.compile("<b>QUALIDADE:.+?/b>(.+?)<br/>").findall(items[0])
                                        if not qualid: qualid = re.compile("<b>VERSÃO:.+?</b>(.+?)<br/>").findall(items[0])
                                        if qualid:
                                                qualidade = qualid[0]
                                                qualidade = qualidade.replace('[',' - ')
                                                qualidade = qualidade.replace(']','')
                                        else:
                                                qualid = re.compile("\nQUALIDADE:\xc2\xa0(.+?)<br/>").findall(items[0])
                                                if qualid:
                                                        qualidade = qualid[0]
                                                        qualidade = qualidade.replace('[',' - ')
                                                        qualidade = qualidade.replace(']','')
                                                else:
                                                        qualid = re.compile("<b>VERS.+?</b>(.+?)<br/>").findall(items[0])
                                                        if qualid:
                                                                qualidade = qualid[0]
                                                                qualidade = qualidade.replace('[',' - ')
                                                                qualidade = qualidade.replace(']','')
                                                        else:
                                                                qualidade = ''

                                        genr = re.compile("NERO:.+?/b>(.+?)<br/>").findall(items[0])
                                        if genr: genero = genr[0]
                                        
                                        ano = re.compile("<b>ANO:.+?/b>(.+?)<br/>").findall(items[0])
                                        audio = re.compile("<b>AUDIO:.+?/b>(.+?)<br/>").findall(items[0])
                                        thumbnail = re.compile('src="(.+?)"').findall(items[0])
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
                                                        audio = re.compile('<b>AUDIO: </b>(.+?)<span style="color: red;"><b>(.+?)</b></span><br/>').findall(items[0])
                                                        if audio:
                                                                audio_filme = ': ' + audio[0][0] + audio[0][1]
                                                        else:
                                                                audio = re.compile('<b>AUDIO: </b> <b><span style="color: red;">(.+?)</span> <span style="color: #38761d;">(.+?)</span></b><br/>').findall(items[0])
                                                                if audio:
                                                                        audio_filme = audio[0][0] + audio[0][1]
                                                                        if 'Portug' or 'PORTUG' in audio_filme:
                                                                                audio_filme = ': PT-PT'
                                                                else:
                                                                        audio = re.compile('<b>AUDIO:.+?<strong>(.+?)</strong>').findall(items[0])
                                                                        if audio:
                                                                                audio_filme = audio[0][0] + audio[0][1]
                                                                                if 'Portug' or 'PORTUG' in audio_filme:
                                                                                        audio_filme = ': PT-PT'
                                                else:
                                                        audio_filme = ': ' + audio[0]
                                        if not audio:
                                                audio = re.compile("\nAUDIO:\xc2\xa0(.+?)<br/>").findall(items[0])
                                                if audio:
                                                        audio_filme = ': ' + audio[0]
                                                else:
                                                        audio_filme = ''
                                        if not ano:
                                                ano = re.compile("\nANO:\xc2\xa0(.+?)<br/>").findall(items[0])
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
                                                        
                                        if selfAddon.getSetting('Fanart') == "true":
                                                nome_pesquisa = nome_series
                                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme)
                                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                                if ftart: fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                if snpse and sinopse == '': sinopse = snpse[0]
                                
                                        ano_filme = '('+ano_filme+')'
                                        qualidade = '('+qualidade
                                        audio_filme = audio_filme+')'
                                        if genero == '': genero = '---'
                                        if sinopse == '': sinopse = '---'
                                        if fanart == '': fanart = '---'
                                        if imdbcode == '': imdbcode = '---'
                                        if thumb == '': thumb = '---'
                                        #Series_File.write('NOME|'+nome_series+'|SINOPSE|'+sinopse+'|END|\n')
                                        Series_File.write('NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|\n')
                                except: pass
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '': fanart = '---'
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        if nome_series in arr_series:
                                _imdb = re.compile('[|]IMDBCODE[|](.+?)[|](.+?)[|](.+?)[|]THUMB[|]').findall(arrai_series[arr_series.index(nome_series)])
                                if not _imdb:
                                        _imdb = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(arrai_series[arr_series.index(nome_series)])
                                        if _imdb:
                                                if 'toppt' not in _imdb[0]:
                                                        imdb = _imdb[0]
                                                        arrai_series[arr_series.index(nome_series)]=arrai_series[arr_series.index(nome_series)].replace(imdb,imdb+'|'+endereco_series)
                                                        todas_series[arr_series.index(nome_series)]=todas_series[arr_series.index(nome_series)].replace(imdb,imdb+'|'+endereco_series)

                        if nome_series not in arr_series:
                                if origem == 'urlTODAS':
                                        percent = int( ( p / num ) * 100)
                                        message = str(p) + " de " + str(int(num))
                                        progress.update( percent, 'A Procurar Séries em '+site, message, "" )
                                        print str(p) + " de " + str(int(num))
                                        if progress.iscanceled():
                                                break
                                if fanart == '' or fanart == '---':
                                        if selfAddon.getSetting('Fanart') == "true":
                                                nome_pesquisa = nome_series
                                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme.replace('(','').replace(')',''))
                                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                                if ftart: fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                if sinopse == '---':
                                                        if snpse: sinopse = snpse[0]
                                arr_series[i] = nome_series
                                if 'IMDB' in imdbcode:
                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                        todas_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                else:
                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                        todas_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                i = i + 1
                                p = p + 1
        Series_Fi.close()
        Series_File.close()
        #return
        Series_File = open(folder + 'series.txt', 'a')
        Series_Fi = open(folder + 'series.txt', 'r')
        read_Series_File = ''
        for line in Series_Fi:
                read_Series_File = read_Series_File + line
                if line!='':_series_.append(line)
        html_items_series = re.findall('href="http://toppt.net/category/series/">SÉRIES</a>(.*?)<div id="main">', html_series_source, re.DOTALL)
        print len(html_items_series)
        for item_series in html_items_series:
                series = re.compile('<a href="(.+?)">(.+?)</a>').findall(item_series)
                for endereco_series,nome_series in series:
                        genero = ''
                        sinopse = ''
                        fanart = ''
                        thumb = ''
                        qualidade = ''
                        imdbcode = ''
                        audio_filme = ''
                        nome_series = nome_series.replace('&amp;','&')
                        nome_series = nome_series.replace('&#39;',"'")
                        nome_series = nome_series.replace('&#8217;',"'")
                        nome_series = nome_series.replace('&#8230;',"...")
                        nome_series = nome_series.replace('&#8211;',"-")
                        nome_series = nome_series.replace('NCIS ',"NCIS:")
                        nome_series = nome_series.replace('Da Vincis Demons',"Da Vinci'S Demons")
                        nome_series = nome_series.lower()
                        nome_series = nome_series.title()
                        if nome_series in read_Series_File:
                                #arr_series[i] = nome_series
                                for x in range(len(_series_)):
                                        if nome_series in _series_[x]:
                                                _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(_series_[x])
                                                if _n: nome = _n[0]
                                                else: nome = '---'
                                                if nome_series in nome:
                                                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(_series_[x])
                                                        if _i: imdbcode = _i[0]
                                                        else: imdbcode = '---'
                                                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(_series_[x])
                                                        if _t: thumb = _t[0]
                                                        else: thumb = '---'
                                                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(_series_[x])
                                                        if _a: ano_filme = _a[0]
                                                        else: ano_filme = '---'
                                                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(_series_[x])
                                                        if _f: fanart = _f[0]
                                                        else: fanart = '---'
                                                        _g = re.compile('[|]GENERO[|](.+?)[|]SINOPSE[|]').findall(_series_[x])
                                                        if _g: genero = _g[0]
                                                        else: genero = '---'
                                                        _s = re.compile('[|]SINOPSE[|](.*)').findall(_series_[x])
                                                        if _s: s = _s[0]
                                                        if '|END|' in s: sinopse = s.replace('|END|','')
                                                        else:
                                                                si = re.compile('SINOPSE[|](.+?)\n(.+?)[|]END[|]').findall(arrai_series[x])
                                                                if si: sinopse = si[0][0] + ' ' + si[0][1]
                                                                else: sinopse = '---'
                                                        #arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                                        #arr_series[i] = nome_series
                        else:
                                try:
                                        html_source = MASH_abrir_url(endereco_series)
                                except: html_source = ''
                                items = re.findall('<div class="postmeta-primary">(.*?)<div class="readmore">', html_source, re.DOTALL)
                                genero = ''
                                sinopse = ''
                                fanart = ''
                                thumb = ''
                                qualidade = ''
                                imdbcode = ''
                                audio_filme = ''

                                imdb = re.compile('imdb.com/title/(.+?)/').findall(items[0])
                                if imdb: imdbcode = imdb[0]
                                else: imdbcode = ''

                                try:
                                        urletitulo = re.compile('<a href="(.+?)" rel="bookmark">(.+?)</a>').findall(items[0])
                                        if 'title=' in urletitulo[0][0]: urletitulo = re.compile('<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>').findall(items[0])
                                        
                                        qualid = re.compile("<b>QUALIDADE:.+?/b>(.+?)<br/>").findall(items[0])
                                        if not qualid: qualid = re.compile("<b>VERSÃO:.+?</b>(.+?)<br/>").findall(items[0])
                                        if qualid:
                                                qualidade = qualid[0]
                                                qualidade = qualidade.replace('[',' - ')
                                                qualidade = qualidade.replace(']','')
                                        else:
                                                qualid = re.compile("\nQUALIDADE:\xc2\xa0(.+?)<br/>").findall(items[0])
                                                if qualid:
                                                        qualidade = qualid[0]
                                                        qualidade = qualidade.replace('[',' - ')
                                                        qualidade = qualidade.replace(']','')
                                                else:
                                                        qualid = re.compile("<b>VERS.+?</b>(.+?)<br/>").findall(items[0])
                                                        if qualid:
                                                                qualidade = qualid[0]
                                                                qualidade = qualidade.replace('[',' - ')
                                                                qualidade = qualidade.replace(']','')
                                                        else:
                                                                qualidade = ''

                                        genr = re.compile("NERO:.+?/b>(.+?)<br/>").findall(items[0])
                                        if genr: genero = genr[0]
                                        
                                        ano = re.compile("<b>ANO:.+?/b>(.+?)<br/>").findall(items[0])
                                        audio = re.compile("<b>AUDIO:.+?/b>(.+?)<br/>").findall(items[0])
                                        thumbnail = re.compile('src="(.+?)"').findall(items[0])
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
                                                        audio = re.compile('<b>AUDIO: </b>(.+?)<span style="color: red;"><b>(.+?)</b></span><br/>').findall(items[0])
                                                        if audio:
                                                                audio_filme = ': ' + audio[0][0] + audio[0][1]
                                                        else:
                                                                audio = re.compile('<b>AUDIO: </b> <b><span style="color: red;">(.+?)</span> <span style="color: #38761d;">(.+?)</span></b><br/>').findall(items[0])
                                                                if audio:
                                                                        audio_filme = audio[0][0] + audio[0][1]
                                                                        if 'Portug' or 'PORTUG' in audio_filme:
                                                                                audio_filme = ': PT-PT'
                                                                else:
                                                                        audio = re.compile('<b>AUDIO:.+?<strong>(.+?)</strong>').findall(items[0])
                                                                        if audio:
                                                                                audio_filme = audio[0][0] + audio[0][1]
                                                                                if 'Portug' or 'PORTUG' in audio_filme:
                                                                                        audio_filme = ': PT-PT'
                                                else:
                                                        audio_filme = ': ' + audio[0]
                                        if not audio:
                                                audio = re.compile("\nAUDIO:\xc2\xa0(.+?)<br/>").findall(items[0])
                                                if audio:
                                                        audio_filme = ': ' + audio[0]
                                                else:
                                                        audio_filme = ''
                                        if not ano:
                                                ano = re.compile("\nANO:\xc2\xa0(.+?)<br/>").findall(items[0])
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
                                                        
                                        if selfAddon.getSetting('Fanart') == "true":
                                                nome_pesquisa = nome_series
                                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme)
                                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                                if ftart: fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                if snpse and sinopse == '': sinopse = snpse[0]
                                                
                                        ano_filme = '('+ano_filme+')'
                                        qualidade = '('+qualidade
                                        audio_filme = audio_filme+')'
                                        if genero == '': genero = '---'
                                        if sinopse == '': sinopse = '---'
                                        if fanart == '': fanart = '---'
                                        if imdbcode == '': imdbcode = '---'
                                        if thumb == '': thumb = '---'
                                        #Series_File.write('NOME|'+nome_series+'|SINOPSE|'+sinopse+'|END|\n')
                                        Series_File.write('NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|\n')
                                except:pass
                        if genero == '': genero = '---'
                        if sinopse == '': sinopse = '---'
                        if fanart == '': fanart = '---'
                        if imdbcode == '': imdbcode = '---'
                        if thumb == '': thumb = '---'
                        if nome_series in arr_series:
                                _imdb = re.compile('[|]IMDBCODE[|](.+?)[|](.+?)[|](.+?)[|]THUMB[|]').findall(arrai_series[arr_series.index(nome_series)])
                                if not _imdb:
                                        _imdb = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(arrai_series[arr_series.index(nome_series)])
                                        if _imdb:
                                                if 'toppt' not in _imdb[0]:
                                                        imdb = _imdb[0]
                                                        arrai_series[arr_series.index(nome_series)]=arrai_series[arr_series.index(nome_series)].replace(imdb,imdb+'|'+endereco_series)
                                                        todas_series[arr_series.index(nome_series)]=todas_series[arr_series.index(nome_series)].replace(imdb,imdb+'|'+endereco_series)

                        if nome_series not in arr_series:
                                if origem == 'urlTODAS': 
                                        percent = int( ( p / num ) * 100)
                                        message = str(p) + " de " + str(int(num))
                                        progress.update( percent, 'A Procurar Séries em '+site, message, "" )
                                        print str(p) + " de " + str(int(num))
                                        if progress.iscanceled():
                                                break
                                if fanart == '' or fanart == '---':
                                        if selfAddon.getSetting('Fanart') == "true":
                                                nome_pesquisa = nome_series
                                                thetvdb_id = thetvdb_api()._id(nome_pesquisa,ano_filme.replace('(','').replace(')',''))
                                                ftart = re.compile('(.+?)[|].+?').findall(thetvdb_id)
                                                if ftart: fanart = 'http://thetvdb.com/banners/fanart/original/' + ftart[0] + '-1.jpg'
                                                snpse = re.compile('.+?[|](.*)').findall(thetvdb_id)
                                                if sinopse == '---':
                                                        if snpse: sinopse = snpse[0]
                                arr_series[i] = nome_series
                                if 'IMDB' in imdbcode:
                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                        todas_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+imdbcode+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                else:
                                        arrai_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                        todas_series[i] = 'NOME|'+nome_series+'|IMDBCODE|'+'IMDB'+imdbcode+'IMDB'+'|'+endereco_series+'|THUMB|'+thumb+'|ANO|'+ano_filme.replace('(','').replace(')','')+'|FANART|'+fanart+'|GENERO|'+genero+'|SINOPSE|'+sinopse+'|END|'
                                i = i + 1
                                p = p + 1
        if origem == 'urlTFV' or origem == 'urlTPT':
                todas_series.sort()
                SeriesFile = open(folder + 'series.txt', 'w')
                for x in range(len(todas_series)):
                        if todas_series[x] != '': SeriesFile.write(todas_series[x]+'\n')
                SeriesFile.close()
                Series_Fi.close()
                Series_File.close()
                return
        arrai_series.sort()
        a = 1
        for x in range(len(arrai_series)):
                if arrai_series[x] != '':
                        _n = re.compile('NOME[|](.+?)[|]IMDBCODE[|]').findall(arrai_series[x])
                        if _n: nome = _n[0]
                        else: nome = '---'
                        _i = re.compile('[|]IMDBCODE[|](.+?)[|]THUMB[|]').findall(arrai_series[x])
                        if _i: imdbcode = _i[0]
                        else: imdbcode = '---'
                        _t = re.compile('[|]THUMB[|](.+?)[|]ANO[|]').findall(arrai_series[x])
                        if _t: thumb = _t[0]
                        else: thumb = '---'
                        _a = re.compile('[|]ANO[|](.+?)[|]FANART[|]').findall(arrai_series[x])
                        if _a: ano = _a[0]
                        else: ano = '---'
                        _f = re.compile('[|]FANART[|](.+?)[|]GENERO[|]').findall(arrai_series[x])
                        if _f:
                                if fanart == '---': fanart == ''
                                else: fanart = _f[0]
                        else: fanart = ''
                        _g = re.compile('[|]GENERO[|](.+?)[|]SINOPSE[|]').findall(arrai_series[x])
                        if _g: genero = _g[0]
                        else: genero = '---'
                        _s = re.compile('[|]SINOPSE[|](.*)').findall(arrai_series[x])
                        if _s: s = _s[0]
                        if '|END|' in s: sinopse = s.replace('|END|','')
                        else:
                                si = re.compile('SINOPSE[|](.+?)\n(.+?)[|]END[|]').findall(arrai_series[x])
                                if si: sinopse = si[0][0] + ' ' + si[0][1]
                                else: sinopse = '---'
                        if fanart == '---': fanart = ''
                        addDir_teste('[B][COLOR green]' + nome + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR]',imdbcode,3006,thumb,sinopse,fanart.replace('w500','w1280'),ano,genero)
        todas_series.sort()
        SeriesFile = open(folder + 'series.txt', 'w')
        for x in range(len(todas_series)):
                if todas_series[x] != '': SeriesFile.write(todas_series[x]+'\n')
        SeriesFile.close()
        Series_Fi.close()
        Series_File.close()
        progress.close()




#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#
	
def MASH_abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

#----------------------------------------------------------------------------------------------------------------------------------------------#
              
def MASH_get_params():
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
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&checker="+urllib.quote_plus(checker)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'FAN3.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir1(name,url,mode,iconimage,folder,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'FAN3.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
        return ok

def addDir_teste(name,url,mode,iconimage,plot,fanart,year,genre):
        if fanart == '': fanart = artfolder + 'FAN3.jpg'
        #text = plot
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&year="+urllib.quote_plus(year)+"&genre="+urllib.quote_plus(genre)+"&iconimage="+urllib.quote_plus(iconimage)
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


          
params=MASH_get_params()
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


