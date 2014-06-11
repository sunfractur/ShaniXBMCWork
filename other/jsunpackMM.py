"""
    urlresolver XBMC Addon
    Copyright (C) 2011 t0mm0
	Updated by Shani_08 for muchmovies, here they have done the double encrypt.
	
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
"""

import re

def unpack(sJavascript):

    aSplit = sJavascript.split(";',")
    p = str(aSplit[0].split("}('")[1])
    aSplit = aSplit[1].split(",")
    a = int(aSplit[0])
    c = int(aSplit[1])

    k = aSplit[2].split(".")[0].replace("'", '').split('|')
    e = ''
    d = ''
    sUnpacked = str(__unpack(p, a, c, k, e, d))
    return sUnpacked.replace('\\', '')

def __unpack(p, a, c, k, e, d):
    while (c > 1):
        c = c -1
        if (k[c]):
            aa=str(__itoaNew(c, a))
            p = re.sub('\\b' + aa +'\\b', k[c], p)           
    return p

def __itoa(num, radix):
    result = ""
    while num > 0:
        result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result
        num /= radix
    return result
	
def __itoaNew(c, a):
    aa="" if c < a else __itoaNew(int(c / a),a) 
    c = (c % a)
    bb=chr(c + 29) if c> 35 else __itoa(c,36)
    return aa+bb
	
	
