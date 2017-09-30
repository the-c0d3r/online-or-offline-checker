online-or-offline
=================

A simple multi-threaded python script to check if website is down or up. 

Using the webservice 
- [DownOrIsItJustMe?](http://downorisitjustme.com) 


Usage 
=====

`uod.py google.com`

Customization
=============

You can customize the websites it uses by editing `sites.json` file. Give it a proper `name`, `url`, and as for the `encoder` if the url to query the site has some suffix you can add it there. And lastly the regular expression to parse the result of the scan.

Update Log
==========
- 0x1 Added new site, [Is-It-Down?](http://is-it-down.com/), and rewritten almost all functions. 
- 0x2 Writing the whole thing in OOP Style format
- 0x3 Made it to read individual site settings from `sites.json` so it's scalable
