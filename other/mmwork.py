def O10(data):
    I0IlOI = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    i = 0
    enc = ''

    while True:
        h1 = I0IlOI.index(data[i]);
        i+=1
        h2 = I0IlOI.index(data[i]);
        i+=1
        h3 = I0IlOI.index(data[i]);
        i+=1
        h4 = I0IlOI.index(data[i]);
        i+=1

        bits = h1 << 18 | h2 << 12 | h3 << 6 | h4;
        o1 = bits >> 16 & 0xff;
        o2 = bits >> 8 & 0xff;
        o3 = bits & 0xff;
        if (h3 == 64):
            enc += chr(o1)
        elif (h4 == 64):
            enc += chr(o1)+chr(o2)
        else:
            enc += chr(o1)+chr(o2)+chr(o3)
        if i >= len(data):
            break
    return enc


aaa=base64.b64decode('Qw1KSDguKGJBMEUcTVF3bCliVTRDFFFOa2R0IU8lTFZTV3RoYnwNNBhKXQw3ODUgRiVEA1tWLzM3PhN5RgkK')

#step1
min_js_string = getUrl('http://www.muchmovies.org/js/jquery.min.js', mobile=True).result
min_js_string=re.compile('lOO\s*=\s*\'(.*?)\'').findall(min_js_string)[0] #get the js variable
min_js_string= O10(min_js_string[::-1]) #first level decrpt


#step2
import jsunpackMM
sUnpacked = jsunpackMM.unpack(min_js_string,1,3) #2nd level encryption , encrypted 3 times	

#step3
import urllib
sUnpacked=urllib.unquote(sUnpacked) #third level encryption


#final step of url decrption
_0xf9b9=re.compile('_0x6781(.*?)];').findall(sUnpacked)[0].split(',')
cf_index=876#get this from decode section
e_index=877#get this from decode section
cf_var=_0xf9b9[cf_index].replace('"','').replace('\\x','').replace(' ','').decode("hex")
e_var=_0xf9b9[e_index].replace('"','').replace('\\x','').replace(' ','').decode("hex")
cf_var=base64.b64decode(base64.b64decode(cf_var))
e_var=base64.b64decode(base64.b64decode(e_var))
print decryptMe(aaa, cf_var, e_var)	#movie link

