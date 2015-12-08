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
        self.base_link = 'http://toppt.net'
        self.search_link = '/?s=%s'


    def get_movie(self, imdb, title, year):
        try:
            title,genero_imdb = self.get_portuguese_name(imdb, title, year) 
            
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)

            #title = cleantitle.movie(title)

            result = cloudflare.source(query)
            result = client.parseDOM(result, 'div', attrs = {'id': 'main.+?'})[0]            
            result = client.parseDOM(result, 'div', attrs = {'class': 'post clearfix.+?'})

            audiopt = 'audio'
            for results in result:
                try:
                    audiopt = re.compile('<b>AUDIO:</b>(.+?)<br/>').findall(results.replace(" ",''))[0]
                    if 'PT' in audiopt.upper() and genero_imdb == 'Animation':
                        audiopt = 'PT'
                        break
                except:audiopt = 'audio'

            for results in result:
                try:result_audio = re.compile('<b>AUDIO:</b>(.+?)<br/>').findall(results.replace(" ",''))[0]
                except: result_audio = 'result_audio'
                try:result_imdb = re.compile('imdb.com/title/(.+?)/').findall(results)[0]
                except: result_imdb = 'result_imdb'
                try:result_title = client.parseDOM(results, 'a', ret='title')[0]
                except:pass
                try:result_url = client.parseDOM(results, 'a', ret='href')[0]
                except:result_url = ''
                try:
                    if audiopt == 'PT':
                        if imdb == result_imdb and audiopt in result_audio.upper():
                            url = result_url
                            break
                    elif imdb == result_imdb:
                        url = result_url
                        break
                except: pass
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
##        sources = []
##        sources.append({'source': 'Videomega', 'quality': 'HD', 'provider': 'TopPt'+url, 'url': url})
        try:
            sources = []

            if url == None: return sources

            url = url.replace(self.base_link,'')

            result = cloudflare.source(urlparse.urljoin(self.base_link, url))

            try:audiopt = re.compile('<b>AUDIO:</b>(.+?)<br/>').findall(result.replace(" ",''))[0]
            except:audiopt = 'audio'
            if 'PT' in audiopt.upper(): audio_filme = ' | PT-PT'
            else: audio_filme = ''

            try:
                try:quality = re.compile('<b>VERS.+?:</b>(.+?)<br/>').findall(result.replace(' ',''))[0]
                except:quality = re.compile('<b>RELEASE:</b>(.+?)<br/>').findall(result.replace(' ',''))[0]
                quality = quality.strip().upper()
                if 'CAM' in quality or 'TS' in quality: quality = 'CAM'
                elif 'SCREENER' in quality: quality = 'SCR'
                elif 'BRRIP' in quality or 'BDRIP' in quality or 'HDRIP' in quality or '720P' in quality: quality = 'HD'
                elif '1080P' in quality: quality = '1080p'
                else: quality = 'SD'
            except: quality = 'SD'

            host_url = re.compile('<spanclass="su-lightbox"data-mfp-src="(.+?)".+?;-webkit-text-shadow:none">(.+?)</span></a></span>').findall(result.replace(' ',''))
            for url,host in host_url:
                host = host.strip().lower()
                if 'openload' in host:
                    try:
                        if openload.check(url) == False: raise Exception()
                        sources.append({'source': 'Openload'+audio_filme, 'quality': quality, 'provider': 'TopPt', 'url': url})
                    except:
                        pass
                elif 'videomega' in host:
                    try:
                        url = re.compile('hashkey=([\w]+)').findall(result)
                        url += re.compile('ref=[\'|\"](.+?)[\'|\"]').findall(result)
                        url = 'http://videomega.tv/cdn.php?ref=%s' % url[0]
                        url = resolvers.request(url)
                        if url == None: raise Exception()
                        sources.append({'source': 'Videomega'+audio_filme, 'quality': quality, 'provider': 'TopPt', 'url': url})
                    except:
                        pass                
                if 'openload' not in host and 'trailer' not in host: sources.append({'source': host+audio_filme, 'quality': quality, 'provider': 'TopPt', 'url': url})
            return sources
        except:
            return sources

    def get_portuguese_name(self, imdb, title, year):
        try:
            genero_imdb = 'genero_imdb'
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
                    title = str(titulo).replace(':','')
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


