#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       mpal.py
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
from ConfigParser import SafeConfigParser
import clicmd
import connection
import os
import sys
import urllib2

#MusicPal actions start
def action_default(data):
    p, config = data
    ip = config.get("connection", "ip")
    username = config.get("connection", "username")
    password = config.get("connection", "password")
    connection.mpal_init_login(ip, username, password)
    
    running = connection.mpal_is_running(ip)
    playing = connection.mpal_get_now_playing(ip)
    volume = float(connection.mpal_get_volume(ip))
    
    status = "running" if running else "sleeping"
    
    print "Address: %s" % ip
    print "Status: %s" % status
    print "Now playing: %s" % playing
    print "Volume: %d%%" % volume

def action_ip(data, ip=None):
    if ip == None:
        p, config = data
        ip = config.get("connection", "ip")
        if ip != "":
            print ip
        else:
            print "MusicPal ip not set."
    else:
        action_ip_set(data, ip)
    
def action_ip_set(data, ip):
    p, config = data
    config.set("connection", "ip", ip)
    config.write(open(os.sep.join([p, "mpal.conf"]), "w"))
    print "IP changed."
    
def action_username(data, username=None):
    if username == None:
        p, config = data
        username = config.get("connection", "username")
        if username != "":
            print username
        else:
            print "MusicPal username not set."
    else:
        action_username_set(data, username)
    
def action_username_set(data, username):
    p, config = data
    config.set("connection", "username", username)
    config.write(open(os.sep.join([p, "mpal.conf"]), "w"))
    print "Username changed."
    
def action_password(data, password=None):
    if password == None:
        p, config = data
        password = config.get("connection", "password")
        if password != "":
            print "*" * len(password)
        else:
            print "MusicPal password not set."
    else:
        action_password_set(data, password)
    
def action_password_set(data, password):
    p, config = data
    config.set("connection", "password", password)
    config.write(open(os.sep.join([p, "mpal.conf"]), "w"))
    print "Password changed."
    
def action_on(data):
    p, config = data
    ip = config.get("connection", "ip")
    username = config.get("connection", "username")
    password = config.get("connection", "password")
    connection.mpal_init_login(ip, username, password)
    connection.mpal_power_up(ip)
    
def action_off(data):
    p, config = data
    ip = config.get("connection", "ip")
    username = config.get("connection", "username")
    password = config.get("connection", "password")
    connection.mpal_init_login(ip, username, password)
    connection.mpal_power_down(ip)
    
def action_stop(data):
    p, config = data
    ip = config.get("connection", "ip")
    username = config.get("connection", "username")
    password = config.get("connection", "password")
    connection.mpal_init_login(ip, username, password)
    connection.mpal_stop(ip)
    
def action_fav(data, n=None):
    p, config = data
    if n == None:
        ip = config.get("connection", "ip")
        username = config.get("connection", "username")
        password = config.get("connection", "password")
        connection.mpal_init_login(ip, username, password)
        favs = connection.mpal_get_favs(ip)
        print "Available Favorites:"
        for fav in favs:
            id, name = fav
            print "%2d  %s" % (id, name)
        print "To play a favorite station, run"
        print "\tmpal fav <id>"
    else:
        action_fav_play(data, n)
    
def action_fav_play(data, n):
    p, config = data
    ip = config.get("connection", "ip")
    username = config.get("connection", "username")
    password = config.get("connection", "password")
    connection.mpal_init_login(ip, username, password)
    connection.mpal_play_fav(ip, n)
    
def action_play_pause(data):
    p, config = data
    ip = config.get("connection", "ip")
    username = config.get("connection", "username")
    password = config.get("connection", "password")
    connection.mpal_init_login(ip, username, password)
    connection.mpal_play_pause(ip)
    
def action_play(data, path=None):
    if not path:
        print "Stream url missing."
    else:
        p, config = data
        ip = config.get("connection", "ip")
        username = config.get("connection", "username")
        password = config.get("connection", "password")
        connection.mpal_init_login(ip, username, password)
        connection.mpal_play_stream(ip, path)
    
def action_volume(data, volume=None):
    p, config = data
    if volume == None:
        ip = config.get("connection", "ip")
        username = config.get("connection", "username")
        password = config.get("connection", "password")
        connection.mpal_init_login(ip, username, password)
        vol = connection.mpal_get_volume(ip)
        print "Volume: %d%%" % vol
    else:
        action_volume_set(data, volume)
        
def action_volume_set(data, volume):
    p, config = data
    ip = config.get("connection", "ip")
    username = config.get("connection", "username")
    password = config.get("connection", "password")
    connection.mpal_init_login(ip, username, password)
    connection.mpal_set_volume(ip, float(volume))
    print "Volume set to %d%%." % float(volume) 
    
#MusicPal actions end


def show_help():
    print
    print "This is a command-line interface for the Freecom MusicPal. This project is not"
    print "affiliated with Freecom."
    print "See the README file for more information. Run 'mpal license' for license"
    print "information."
    print
    print "Usage:"
    print "\tmpal\t\t\tshow MusicPal status"
    print "\tmpal on\t\t\tturn MusicPal on"
    print "\tmpal off\t\tturn MusicPal off"
    print "\tmpal playpause\t\tplay/pause"
    print "\tmpal volume [<vol>]\tdisplay or set volume; <vol>=0...100"
    print "\tmpal fav [<id>]\t\tdisplay or play favorite station(s)"
    print "\tmpal play <url>\t\tplay stream given by <url>"
    
def show_license():
    license_string = """Copyright 2010 Sven Festersen <sven@sven-festersen.de>
    
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.
"""
    print
    print license_string


def check_settings_directory(p):
    """
    Creates a directory for the configuration file if it does not exist.
    """
    if not os.path.exists(p):
        os.mkdir(p)
        
def load_settings(p):
    """
    Loads the MusicPal's ip, the username and password from the config
    file.
    """
    ip, username, password = None, None, None
    config = SafeConfigParser()
    config.read(os.sep.join([p, "mpal.conf"]))
    if not config.has_section("connection"):
        config.add_section("connection")

    if not config.has_option("connection", "ip"):
        config.set("connection", "ip", "")
    if not config.has_option("connection", "username"):
        config.set("connection", "username", "")
    if not config.has_option("connection", "password"):
        config.set("connection", "password", "")
    return p, config
    
def init_actions(p, config):
    data = p, config
    
    cmd = clicmd.CLICommand()
    cmd.register_command("__default__", action_default, data)
    cmd.register_command("ip", action_ip, data)
    cmd.register_command("ip set", action_ip_set, data)
    cmd.register_command("username", action_username, data)
    cmd.register_command("username set", action_username_set, data)
    cmd.register_command("password", action_password, data)
    cmd.register_command("password set", action_password_set, data)
    cmd.register_command("on", action_on, data)
    cmd.register_command("off", action_off, data)
    cmd.register_command("stop", action_stop, data)
    cmd.register_command("fav", action_fav, data)
    cmd.register_command("fav play", action_fav_play, data)
    cmd.register_command("playpause", action_play_pause, data)
    cmd.register_command("volume", action_volume, data)
    cmd.register_command("volume set", action_volume_set, data)
    cmd.register_command("play", action_play, data)
    cmd.register_command("help", show_help)
    cmd.register_command("license", show_license)
    
    print "MusicPal command-line interface"
    
    try:
        cmd.parse()
    except urllib2.URLError:
        print "Can't connect to MusicPal. Check ip address and login."
        
def main():
    p = os.path.expanduser(os.sep.join(["~", ".mpal"]))
    check_settings_directory(p)
    p, config = load_settings(p)
    init_actions(p, config)
    
    
if __name__ == "__main__":
    main()
