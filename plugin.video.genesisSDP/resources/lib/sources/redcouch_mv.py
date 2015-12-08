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
        self.base_link = 'http://www.redcouch.me'
        self.search_link = '/index.php?do=search&subaction=search&story='


    def get_movie(self, imdb, title, year):
        try:
            #title,genero_imdb = self.get_portuguese_name(imdb, title, year)

            query = self.base_link+self.search_link+str(title.replace(' ','+'))

            result = self.abrir_url(query)
            result = client.parseDOM(result, 'div', attrs = {'class': 'short-film'})
            a = str(len(result))
            
            for div in result:
                try:result_url = re.compile('href="(.+?)"').findall(div)[0]
                except:pass
                O_title = cloudflare.source(result_url)
                try:O_title = re.compile('tulooriginal.+?/span><pclass="text"><strong>(.+?)</strong></p>').findall(O_title.replace('\n','').replace(' ',''))[0]
                except: O_title = 'O_title'
                if O_title == title.replace(' ',''):                                
                        url = result_url
                        break
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
##        sources = []
##        sources.append({'source': 'Redcouch', 'quality': 'HD', 'provider': 'Redcouch'+url, 'url': url})
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
                url = re.compile('hashkey=([\w]+)').findall(result)
                url += re.compile('ref=[\'|\"](.+?)[\'|\"]').findall(result)
                url = 'http://videomega.tv/cdn.php?ref=%s' % url[0]
                url = resolvers.request(url)
                if url == None: raise Exception()
                sources.append({'source': 'Videomega'+audio_filme, 'quality': quality, 'provider': 'Redcouch', 'url': url})
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
                        if openload.check(urlO) == False: raise Exception()
                        sources.append({'source': 'Openload'+audio_filme, 'quality': quality, 'provider': 'Redcouch', 'url': urlO})
                    except:
                        pass
                elif 'videomega' in urls:
                    try:
                        sources.append({'source': 'Videomega'+audio_filme, 'quality': quality, 'provider': 'Redcouch', 'url': url})
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


                

