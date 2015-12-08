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
        self.base_link = 'http://tuga.io'
        self.search_link = '/procurar'


    def get_movie(self, imdb, title, year):
        try:
            #title,genero_imdb = self.get_portuguese_name(imdb, title, year)

            query = self.base_link+self.search_link

            result = self.abrir_url(query, str(title))
            result = client.parseDOM(result, 'div', attrs = {'class': 'list'})
            result = re.compile('href="(.+?)"').findall(str(result[0]))
            for result_url in result:                
                try:result_imdb = re.compile('filme/(.*)').findall(result_url)[0]
                except: result_imdb = 'result_imdb'
                if imdb == result_imdb:
                        url = result_url
                        break

            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []
            
            if url == None: return sources

            url = self.base_link + url
            result = cloudflare.source(url)
            result = re.compile('src="/player_data(.+?)"></script>').findall(result)[0]
            url = self.base_link + '/player_data' + result
            result = cloudflare.source(url)
            result = re.compile('[[]"(.+?)"[]]').findall(result)[0]
            url = self.Hexadecoder(str(result)).replace('download','xmas-stream')

            audio_filme = ''
            try:
                quality = url.strip().upper()
                if '1080P' in quality: quality = '1080p'
                elif 'BRRIP' in quality or 'BDRIP' in quality or 'HDRIP' in quality or '720P' in quality: quality = 'HD'
                elif 'SCREENER' in quality: quality = 'SCR'
                elif 'CAM' in quality or 'TS' in quality: quality = 'CAM'
                else: quality = 'SD'
                if 'PT-PT' in quality or 'PORTUGU' in quality: audio_filme = ' | PT-PT'
                else: audio_filme = ''
            except: quality = 'SD'

            sources.append({'source': 'TugaIO'+audio_filme, 'quality': quality, 'provider': 'TugaIO', 'url': url})
            
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
        if url != None:return url
        else: return
        

    def abrir_url(self, url, pesquisa=False):
            
        header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}

        data = urllib.urlencode({'procurar' : pesquisa})
        req = urllib2.Request(url, data, headers=header)
            
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link
    

    def Hexadecoder(self, hexstring):

        descodificado = ''

        HEX = [' ','\|20', '!','\|21', '"','\|22', '#','\|23','$','\|24',  '%','\|25', '&','\|26', "'",'\|27', '(','\|28',')','\|29', '*','\|2a','+','\|2b' ,',','\|2c','-','\|2d','.','\|2e' , '/','\|2f' ,'0','\|30','1','\|31' ,'2','\|32' ,'3','\|33' ,'4','\|34' ,'5','\|35' ,'6','\|36' ,'7','\|37' ,'8','\|38' ,'9','\|39' ,':','\|3a' ,';','\|3b' ,'<','\|3c' ,'=','\|3d' ,'>','\|3e' ,'?','\|3f' ,'@','\|40' ,'A','\|41' ,'B','\|42' ,'C','\|43' ,'D','\|44' ,'E','\|45' ,'F','\|46' ,'G','\|47' ,'H','\|48' ,'I','\|49' ,'J','\|4a' ,'K','\|4b','L','\|4c','M','\|4d','N','\|4e','O','\|4f','P','\|50','Q','\|51','R','\|52','S','\|53','T','\|54' ,'U','\|55','V','\|56' ,'W','\|57','X','\|58' ,'Y','\|59' ,'Z','\|5a' ,'[','\|5b' ,']','\|5d' ,'^','\|5e','_','\|5f','`','\|60','a','\|61' ,'b','\|62' ,'c','\|63','d','\|64' , 'e','\|65' ,'f','\|66','g','\|67','h','\|68' ,'i','\|69','j','\|6a' ,'k','\|6b' ,'l','\|6c' ,'m','\|6d' ,'n','\|6e' ,'o','\|6f' ,'p','\|70' ,'q','\|71' ,'r','\|72' ,'s','\|73' ,'t','\|74','u','\|75' ,'v','\|76', 'w','\|77','x','\|78' ,'y','\|79' ,'z','\|7a' ,'{','\|7b' ,'|','\|7c' ,'}','\|7d','~','\|7e','','\|7f']
        stringhex = hexstring+'\|'
        try:
            stringhex = re.compile('(.+?)[\|]').findall(hexstring.replace('x','|'))
            for i in stringhex:
                conta = 0
                for n in HEX:
                    if n+'\|' == '\|'+i+'|':
                        descodificado = descodificado + str(HEX[int(conta-1)])
                    conta = conta + 1
            descodificado = descodificado + '9999'
            if '.mp9999' in descodificado: descodificado = descodificado.replace('.mp9999','.mp4')
        except: descodificado = hexstring

        return str(descodificado)


                

