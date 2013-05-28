#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# keep the .com address to properly find disqus comments
SITEURL = 'http://ocefpaf.github.io'

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing
#RELATIVE_URLS = False
DISQUS_SITENAME = "python2oceanographers"
#GOOGLE_ANALYTICS = ""
