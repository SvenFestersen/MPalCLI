#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       connection.py
#       
#       Copyright 2010 Sven Festersen <sven@sven-festersen.de>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
from BeautifulSoup import BeautifulSoup
from htmlentitydefs import name2codepoint as n2cp
import re
import urllib
import urllib2

#HTML entity substitution from
#http://github.com/sku/python-twitter-ircbot/blob/master/html_decode.py

def substitute_entity(match):
    ent = match.group(3)
    
    if match.group(1) == "#":
        if match.group(2) == '':
            return unichr(int(ent))
        elif match.group(2) == 'x':
            return unichr(int('0x'+ent, 16))
    else:
        cp = n2cp.get(ent)

        if cp:
            return unichr(cp)
        else:
            return match.group()

def decode_htmlentities(string):
    entity_re = re.compile(r'&(#?)(x?)(\d{1,5}|\w{1,8});')
    return entity_re.subn(substitute_entity, string)[0]


def mpal_init_login(ip, username, password):
    #Installs a urlib2 opener that manages username and password
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    top_level_url = "http://%s/admin/cgi-bin/" % ip
    password_mgr.add_password(None, top_level_url, username, password)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    
def mpal_get_data(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    html = response.read()
    return html

def mpal_get_volume(ip):
    #Returns the current volume in percent
    html = mpal_get_data("http://%s/admin/cgi-bin/admin.cgi?f=now_playing_frame&n=../now_playing_frame.html" % ip)
    soup = BeautifulSoup(html)
    imgs = soup.findAll("img", attrs={"src": "/images/volume_on.gif"})
    return 100 * (len(imgs) - 1) / 20.0
    
def mpal_set_volume(ip, vol):
    #Set the volume in percent
    vol = int(20 * vol / 100.0)
    url = "http://%s/admin/cgi-bin/admin.cgi?f=volume_set&v=%s&n=../now_playing_frame.html" % (ip, vol)
    mpal_get_data(url)
    
def mpal_get_now_playing(ip):
    url = "http://%s/cgi-bin/user.cgi?f=welcome_now_playing&n=../welcome_now_playing.html" % ip
    html = mpal_get_data(url)
    soup = BeautifulSoup(html)
    a = soup.body.contents[0].strip().split(": ", 1)
    if len(a) == 2:
        return a[1]
    return None
    
def mpal_play_pause(ip):
    url = "http://%s/admin/cgi-bin/admin.cgi?f=play_pause&n=../now_playing_frame.html" % ip
    mpal_get_data(url)
    
def mpal_get_favs(ip):
    url = "http://%s/admin/cgi-bin/admin.cgi?f=now_playing&n=../now_playing.html" % ip
    html = mpal_get_data(url)
    soup = BeautifulSoup(html)
    table = soup.find("table", attrs={"class": "table_line"})
    rows = table.findAll("tr", attrs={"class": "table_alt1"})
    
    result = []
    
    for row in rows:
        col = row.findAll("td")[1]
        div = col.find("div")
        name = decode_htmlentities(div.contents[0])
        id = int(div.attrs[2][1].replace("window.location.href='/admin/cgi-bin/admin.cgi?f=now_playing&n=../now_playing.html&a=p&i=", "").replace("';", ""))
        result.append((id, name))
        
    return result
    
def mpal_play_fav(ip, id):
    url = "http://%s/admin/cgi-bin/admin.cgi?f=now_playing&n=../now_playing.html&a=p&i=%s" % (ip, id)
    mpal_get_data(url)
