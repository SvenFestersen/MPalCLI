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
import urllib
import urllib2
from xml.dom.minidom import parseString
   
    
def getText(nodelist):
    """
    Get text from text child nodes.
    code from: http://docs.python.org/library/xml.dom.minidom.html
    """
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)
    

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
    url = "http://%s/admin/cgi-bin/state.cgi?fav=0" % ip
    data = mpal_get_data(url)
    dom = parseString(data)
    playing = dom.getElementsByTagName("volume")
    return float(getText(playing[0].childNodes)) * 5
    
def mpal_set_volume(ip, vol):
    #Set the volume in percent
    vol = int(20 * vol / 100.0)
    url = "http://%s/admin/cgi-bin/admin.cgi?f=volume_set&v=%s&n=../now_playing_frame.html" % (ip, vol)
    mpal_get_data(url)
    
    
def mpal_get_now_playing(ip):
    url = "http://%s/admin/cgi-bin/state.cgi?fav=0" % ip
    data = mpal_get_data(url)
    dom = parseString(data)
    playing = dom.getElementsByTagName("now_playing")
    return getText(playing[0].childNodes)
    
    
def mpal_play_pause(ip):
    url = "http://%s/admin/cgi-bin/admin.cgi?f=play_pause&n=../now_playing_frame.html" % ip
    mpal_get_data(url)
    
    
def mpal_get_favs(ip):
    url = "http://%s/admin/cgi-bin/state.cgi?fav=1" % ip
    data = mpal_get_data(url)
    dom = parseString(data)
    favs = dom.getElementsByTagName("favorites")[0]
    names = []
    for fav in favs.getElementsByTagName("favorite"):
        nnode = fav.getElementsByTagName("name")[0].childNodes
        names.append(getText(nnode))
    return [(i, names[i]) for i in range(0, len(names))]
    
def mpal_play_fav(ip, id):
    url = "http://%s/admin/cgi-bin/admin.cgi?f=now_playing&n=../now_playing.html&a=p&i=%s" % (ip, id)
    mpal_get_data(url)
