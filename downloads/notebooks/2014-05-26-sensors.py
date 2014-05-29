# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from IPython.core.display import HTML

with open('creative_commons.txt', 'r') as f:
    html = f.read()
    
with open('./styles/custom.css', 'r') as f:
    styles = f.read()
    
HTML(styles)

name = '2014-05-26-sensors'

html = """
<small>
<p> This post was written as an IPython notebook.  It is available for
<a href="http://ocefpaf.github.com/python4oceanographers/downloads/
notebooks/%s.ipynb">download</a> or as a static
<a href="http://nbviewer.ipython.org/url/ocefpaf.github.com/
python4oceanographers/downloads/notebooks/%s.ipynb">html</a>.</p>
<p></p>
%s """ % (name, name, html)

# <markdowncell>

# Again another late post!  Still getting settle here in beautiful
# [Salvador](http://pt.wikipedia.org/wiki/Salvador_%28Bahia%29).  Unfortunately
# the transportation strike, World Cup preparations are not helping our
# apartment search.
# 
# Because of that this will be another "script dump."  This one is very useful
# for those who insist on using Linux on machine designed for windows and suffer
# from overheating.
# 
# It uses an interesting library to use shell commands as python functions
# called [sh](https://github.com/amoffat/sh), and
# [Google Translate Speech Service](http://translate.google.com/translate_tts?q=Hello&tl=en) to say out loud the
# core temperature.
# 
# Hope it is useful!

# <codecell>

HTML(html)

