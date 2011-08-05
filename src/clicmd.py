#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       clicmd.py
#       
#       Copyright 2010 Sven Festersen <sven@sven-festersen.de>
#       
#       This program is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys

class CLICommand(object):
    
    def __init__(self):
        self._commands = {}
        
    def register_command(self, command, handler, data=None):
        a = command.split()
        if not len(a) in self._commands:
            self._commands[len(a)] = {}
        self._commands[len(a)][command] = (handler, data)
        
    def parse(self):
        cmd = sys.argv[1:]
        i = len(cmd)
        
        if i == 0:
            cmd = ["__default__"]
            i = 1
                
        while i > 0:
            if i in self._commands:
                command = cmd[:i]
                args = cmd[i:]
                
                if " ".join(command) in self._commands[i]:
                    handler, data = self._commands[i][" ".join(command)]
                    if not data:
                        handler(*args)
                    else:
                        handler(data, *args)
                    break
            i -= 1
