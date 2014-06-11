Now, you can execute python functions within regex, the format is $pyFunction.FileName.FunctionName

first parameter must be page_data, even if you dont need any page data


for example, if i want to add 2+4, i have created that function and stored in myFunctions.py file. this file should be copied in profile directory 
for example  \XBMC\userdata\addon_data\plugin.video.live.streams

def addme(page_data,a,b):
    return a+b



now, this function should be part of a regex, which then could be used anywhere, since we support regex in regex, you can pass any static of dynamic parameters.
if you need the page_data, it will also be available. the function call should result in proper python syntax.

sample call

<item>
<title>function test</title>
<link>http://$doregex[get-sum]</link>

<regex>
<name>get-sum</name>
<expres>$pyFunction:myFunctions.addme(page_data,2,4)</expres>
<page></page>
</regex>

</item>

Note, this will not run anything but if you look in the log file, 
CDVDPlayer::OpenInputStream - error opening [http://6]
which means it worked.

This will allow you to write python functions, like current date time in certain format, or do the calcualtion which otherwise is too difficult via web calls.

