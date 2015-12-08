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
        self.base_link = 'http://www.tuga-filmes.us'
        self.search_link = '/search?q='


    def get_movie(self, imdb, title, year):
        try:
            title,genero_imdb = self.get_portuguese_name(imdb, title, year)

            query = self.base_link+self.search_link+urllib.quote_plus(title)

            #title = cleantitle.movie(title)

            result = cloudflare.source(query)
            try:result = client.parseDOM(result.replace('\n',''), 'div', attrs = {'id': 'Blog1.+?'})[0]
            except:result = client.parseDOM(result.replace('\n',''), 'div', attrs = {'class': 'widget Blog.+?'})[0]
            result = client.parseDOM(result.replace('\n',''), 'div', attrs = {'class': 'video-item.+?'})

            audiopt = 'audio'
            for results in result:
                try:
                    audiopt = re.compile('udio</b>:(.+?)<br/>').findall(results.replace(" ",''))[0]
                    if 'PT' in audiopt.upper() and genero_imdb == 'Animation':
                        audiopt = 'PT'
                        break
                except:audiopt = 'audio'

            for results in result:
                try:result_audio = re.compile('udio</b>:(.+?)<br/>').findall(results.replace(" ",''))[0]
                except: result_audio = 'result_audio'
                try:result_imdb = re.compile('imdb.com/title/(.+?)"').findall(results)[0].replace('/','')
                except: result_imdb = 'result_imdb'
                try:result_title = client.parseDOM(results, 'a', ret='title')[0]
                except:pass
                try:result_url = client.parseDOM(results, 'a', ret='href')[0]
                except:result_url = 'nada'
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
##        sources.append({'source': 'Videomega', 'quality': 'HD', 'provider': 'TugafilmesUS'+url, 'url': url})
        try:
            sources = []
            
            if url == None: return sources

            result = cloudflare.source(url)
            result = client.parseDOM(result, 'div', attrs = {'class': 'video-item.+?'})[0]
            
            try:audiopt = re.compile('udio</b>:(.+?)<br/>').findall(result.replace('\n','').replace(' ',''))[0]
            except:audiopt = 'audio'

            try:
                try:quality = re.compile('<b>Qualidade</b>:(.+?)<br />').findall(result.replace(' ',''))[0]
                except:quality = re.compile('<b>RELEASE:</b>(.+?)<br/>').findall(result.replace(' ',''))[0]
                quality = quality.strip().upper()
                if 'CAM' in quality or 'TS' in quality: quality = 'CAM'
                elif 'SCREENER' in quality: quality = 'SCR'
                elif 'BRRIP' in quality or 'BDRIP' in quality or 'HDRIP' in quality or '720P' in quality: quality = 'HD'
                elif '1080P' in quality: quality = '1080p'
                else: quality = 'SD'
            except: quality = 'SD'

            try: host_url = re.compile("<divclass='id(.+?)'>Assistir(.+?)Cliqueaquiparaver").findall(result.replace('\n','').replace(' ',''))
            except:
                try: host_url = re.compile("<divclass='id(.+?)'>Assistir(.+?)</p>").findall(result.replace('\n','').replace(' ',''))
                except:
                    try:host_url = re.compile('<divclass="id(.+?)">Assistir(.+?)Cliqueaquiparaver').findall(result.replace('\n','').replace(' ',''))
                    except:
                        try: host_url = re.compile('<divclass="id(.+?)">Assistir(.+?)</p>').findall(result.replace('\n','').replace(' ',''))
                        except: host_url = []
            for host,url in host_url:
                if 'PT-PT' in url.upper() or 'PORTUGU' in url.upper(): audio_filme = ' | PT-PT'
                else: audio_filme = ''
                host = host.strip().lower()
                try: id_video = re.compile('href="(.+?)"').findall(url)[0]
                except: id_video = re.compile('src="(.+?)"').findall(url)[0]
                try:id_video = re.compile('=(.*)').findall(id_video)[0]
                except: id_video=''
                if "ep" in host:
                    host = 'videomega'
                    try:
                        url = re.compile('hashkey=([\w]+)').findall(result)
                        url += re.compile('ref=[\'|\"](.+?)[\'|\"]').findall(result)
                        url = 'http://videomega.tv/cdn.php?ref=%s' % url[0]
                        url = resolvers.request(url)
                        if url == None: raise Exception()
                        sources.append({'source': 'Videomega'+audio_filme, 'quality': quality, 'provider': 'TugafilmesUS', 'url': url})
                    except:
                        try:
                            url = 'http://videomega.tv/cdn.php?ref='+id_video
                            sources.append({'source': 'Videomega'+audio_filme, 'quality': quality, 'provider': 'TugafilmesUS', 'url': url})
                        except: pass
                elif "vw" in host:
                    host = 'videowood'
                    url = 'http://www.videowood.tv/embed/' + id_video
                elif "dv" in host:
                    host = 'dropvideo'
                    url = 'http://dropvideo.com/embed/' + id_video
                elif "vt" in host:
                    host = 'vidto.me'
                    url = 'http://vidto.me/' + id_video + '.html'
                elif "nv" in host:
                    host = 'nowvideo'
                    url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video
                elif 'openload' in host:
                    try:
                        if openload.check(url) == False: raise Exception()
                        sources.append({'source': 'Openload'+audio_filme, 'quality': quality, 'provider': 'TugafilmesUS', 'url': url})
                    except:
                        pass                                    
                if 'videomega' not in host and 'openload' not in host and 'trailer' not in host: sources.append({'source': host+audio_filme, 'quality': quality, 'provider': 'TugafilmesUS', 'url': url})
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
                    packed = cloudflare.source(url)
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


