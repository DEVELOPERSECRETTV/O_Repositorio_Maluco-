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
        self.base_link = 'http://www.tuga-filmes.com'
        self.search_link = '/?s='


    def get_movie(self, imdb, title, year):
        try:
            title,genero_imdb = self.get_portuguese_name(imdb, title, year)

            query = self.base_link+self.search_link+urllib.quote_plus(title)

            title = cleantitle.movie(title)

            result = cloudflare.source(query)
            result = client.parseDOM(result, 'div', attrs = {'class': 'wrapper.+?'})[0]
            result = re.compile('<a href="(.+?)" class="thumbnail-wrapper" title="(.+?)">').findall(result)

            for result_url,result_title in result:
                if title == cleantitle.movie(result_title):
                        url = result_url
                        break
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
##        sources = []
##        sources.append({'source': 'Videomega', 'quality': 'HD', 'provider': 'TugafilmesCOM'+url, 'url': url})
        try:
            sources = []
            
            if url == None: return sources

            result = cloudflare.source(url)
            result = client.parseDOM(result, 'div', attrs = {'class': 'entry-content.+?'})[0]

            try:
                quality = re.compile('<b>vers.+?:</b>(.+?)</p>').findall(result.lower().replace(' ',''))[0]
                quality = quality.strip().upper()
                if 'CAM' in quality or 'TS' in quality: quality = 'CAM'
                elif 'SCREENER' in quality: quality = 'SCR'
                elif 'BRRIP' in quality or 'BDRIP' in quality or 'HDRIP' in quality or '720P' in quality: quality = 'HD'
                elif '1080P' in quality: quality = '1080p'
                else: quality = 'SD'
                if 'PT-PT' in quality or 'PORTUGU' in quality: audio_filme = ' | PT-PT'
                else: audio_filme = ''
            except: quality = 'SD'

            try:
                url = re.compile('hashkey=([\w]+)').findall(result)
                url += re.compile('ref=[\'|\"](.+?)[\'|\"]').findall(result)
                url = 'http://videomega.tv/cdn.php?ref=%s' % url[0]
                url = resolvers.request(url)
                if url == None: raise Exception()
                sources.append({'source': 'Videomega'+audio_filme, 'quality': quality, 'provider': 'TugafilmesCOM', 'url': url})
            except:
                pass
            host_url = re.compile('<ahref="(.+?)"target="_blank">(.+?)Online').findall(result.replace(' ',''))#.+?\n').findall(result.replace(' ',''))
            for url,host in host_url:
                host = host.strip().lower().replace('(','')
                if 'openload' in host.lower():
                    try:
                        if openload.check(url) == False: raise Exception()
                        sources.append({'source': 'Openload'+audio_filme, 'quality': quality, 'provider': 'TugafilmesCOM', 'url': url})
                    except:
                        pass                                    
                elif 'download' not in host.lower() and 'trailer' not in host.lower(): sources.append({'source': host+audio_filme, 'quality': quality, 'provider': 'TugafilmesCOM', 'url': url})
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
            if 'videowood' in url:
                try:
                    packed = cloudflare.source(url.replace('/video/','/embed/'))
                    packed = re.compile('eval(.+?)</script>').findall(packed.replace("\n", "").replace(" ",""))[0]
                    packed = 'eval'+packed.replace('\\','')
                    unpacked = jsunpack.unpack(packed)
                    url = re.compile('"file":"(.+?)"').findall(unpacked)#[1]
                    url = [i for i in url if not i.endswith('.srt') and not i.endswith('.png')][0]
                except:
                    pass
            else: url = resolvers.request(url)
            return url
        except:
            return


