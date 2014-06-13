# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from IPython.core.display import HTML

with open('creative_commons.txt', 'r') as f:
    html = f.read()
    
with open('./styles/custom.css', 'r') as f:
    styles = f.read()
    
HTML(styles)

name = '2014-06-09-cf-compliance'

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

# If you never heard about the Climate and Forecast
# ([CF]([CF-rules](http://cfconventions.org/1.6.html))) Metadata Conventions you
# are probably living under a rock deep down the
# [Mariana Trench](http://en.wikipedia.org/wiki/Mariana_Trench).
# 
# Now, hearing about it is one thing, claiming to fully understand it is another.
# First, it is under constant [change](https://cf-pcmdi.llnl.gov/trac/ticket/93),
# second, it seems to be more complex than the
# [Brazilian constitution](http://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm).
# 
# Still, CF-rules are a necessary evil.  It allows us to create tools that will
# read any dataset in a standardize way.  That **is** a big deal for
# <s>climate</s> scientists.
# 
# I won't get too technical here.  I won't even mention the rules!  To be honest,
# I do not know all most of them.  But I do try to copy good examples from datasets
# similar to mine when I am saving my netcdf files.
# 
# But how to determine if a particular netcdf file is a good example of
# CF-compliance?  There is a very promising project from the
# [IOOS group](https://github.com/ioos/compliance-checker), but it s not ready
# yet.  In the meanwhile we have two alternatives.  The first one is to try to
# load the data with `iris`, the second is running cdat's `cfchecker`.
# 
# Iris uses the Python Knowledge Engine [PyKE](http://pyke.sourceforge.net/) to
# create a set of rules that enforces CF standards.  But sometimes the error
# messages are not that helpful at all to understand what is wrong if the
# metadata.  On the other hand, `cfchecker` returns a report that on the
# compliance itself, but requires to upload the dataset to test it using the
# [online checker]((http://cfconventions.org/compliance-checker.html)) to install [cdat] (https://pypi.python.org/pypi/cdat-lite/6.0rc2).
# 
# If you find that installing cdat is a challenge, do not fear!  Appeal to conda
# and follow [these](https://github.com/ioos/secoora/wiki/Install-cfchecker)
# instructions.  You will get chchecker working in no time.

# <codecell>

HTML(html)

