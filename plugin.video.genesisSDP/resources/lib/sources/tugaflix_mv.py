# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re,urllib,urllib2,urlparse

from resources.lib.libraries import cleantitle
from resources.lib.libraries import cloudflare
from resources.lib.libraries import client
from resources.lib.libraries import jsunpack
from resources.lib.resolvers import openload
from resources.lib import resolvers

class source:
    def __init__(self):
        self.base_link = 'http://tugaflix.com'
        self.search_link = '/Filmes?G=&O=1&T='


    def get_movie(self, imdb, title, year):
        try:
            #title,genero_imdb = self.get_portuguese_name(imdb, title, year)

            query = self.base_link+self.search_link+str(title.replace(' ','+'))

            #result = self.abrir_url(query)
            result = cloudflare.source(query)
            result = re.compile('<div class="browse-movie-wrap.+?"> <a href="(.+?)" class="browse-movie-link"> <figure>').findall(result)
            
            a = str(len(result))
            
            for result_url in result:
                try:result_imdb = re.compile('=(.*)').findall(result_url)[0]
                except:result_imdb='result_imdb'                
                if imdb == 'tt'+result_imdb:                                
                        url = self.base_link+'/Filme?F='+result_imdb
                        break
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
##        sources = []
##        sources.append({'source': 'TugaFlix', 'quality': 'HD', 'provider': 'Redcouch'+url, 'url': url})
        try:
            sources = []
            
            if url == None: return sources

            result = cloudflare.source(url)
            
            audio_filme = ''
            try:
                titulo = client.parseDOM(result, 'h1', attrs = {'class': 'title'})[0]
                if 'PT-PT' in titulo or 'PORTUGU' in titulo: audio_filme = ' | PT-PT'
                else: audio_filme = ''
            except: audio_filme = ''
            try:
                quality = url.strip().upper()
                if '1080P' in quality: quality = '1080p'
                elif 'BRRIP' in quality or 'BDRIP' in quality or 'HDRIP' in quality or '720P' in quality: quality = 'HD'
                elif 'SCREENER' in quality: quality = 'SCR'
                elif 'CAM' in quality or 'TS' in quality: quality = 'CAM'
                else: quality = 'SD'
            except: quality = 'SD'

            try:
                vurl = re.compile('hashkey=([\w]+)').findall(result)
                vurl += re.compile('ref=[\'|\"](.+?)[\'|\"]').findall(result)
                vurl = 'http://videomega.tv/cdn.php?ref=%s' % vurl[0]
                vurl = resolvers.request(vurl)
                if vurl == None: raise Exception()
                sources.append({'source': 'Videomega'+audio_filme, 'quality': quality, 'provider': 'TugaFlix', 'url': vurl})
            except:
                pass
            
            url = client.parseDOM(result, 'iframe', ret='src')
            for urls in url:
                if 'openload' in urls:
                    try:
                        try:
                            ul = re.compile('(.+?)/embed/(.+?)/').findall(urls)
                            urlO = ul[0][0]+'/embed/'+ul[0][1]
                        except: urlO = urls                        
                        if openload.check('https://openload.co/embed/DjeH9frIdKU') == False: raise Exception()
                        sources.append({'source': 'Openload'+audio_filme, 'quality': quality, 'provider': 'TugaFlix', 'url': urlO})
                    except:
                        pass
                elif 'videomega' in urls:
                    try:
                        sources.append({'source': 'Videomega'+audio_filme, 'quality': quality, 'provider': 'TugaFlix', 'url': url})
                    except:
                        pass
                #sources.append({'source': 'Openload'+audio_filme, 'quality': quality, 'provider': 'Redcouch'+urls, 'url': urls})
            return sources
        except:
            return sources
        

    def get_portuguese_name(self, imdb, title, year):
        genero_imdb = 'genero_imdb'
        try:
            genre_imdb = 'http://akas.imdb.com/title/'+imdb+'/?ref_=fn_al_tt_1'
            req = urllib2.Request(genre_imdb)
            req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.2; pt-Pt; rv:1.8.1.18) Gecko/20081029 Firefox/2.0.0.18')
            response = urllib2.urlopen(req)
            genre_imdb=response.read()
            response.close()
            
            titulo=re.compile('itemprop="name">(.+?)</span>').findall(genre_imdb)
            if titulo:
                t = titulo[0]
                titulo = str(t)
            else: titulo = str(title)
            genre_imdb = client.parseDOM(genre_imdb, 'span', attrs = {'class': 'itemprop.+?'})            
            for i in genre_imdb:
                if 'Animation' in i:
                    genero_imdb = 'Animation'
                    title = str(titulo)
                    break
            return title,genero_imdb
        except:
            return title,genero_imdb


    def resolve(self, url):
        try:
            url = resolvers.request(url)
            return url
        except:
            return
        

    def abrir_url(self, url):            
        req = urllib2.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.2; en-GB; rv:1.8.1.18) Gecko/20081029 Firefox/2.0.0.18')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link


                

