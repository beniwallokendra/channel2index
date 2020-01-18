#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import channel2index
import os
import sys

def test():
	pdf_name = channel2index.gen('pincongessence')
	os.system('open %s -g' % pdf_name)
	# pdf_name = channel2index.gen('equality_and_rights')
	# os.system('open %s -g' % pdf_name)
	# pdf_name = channel2index.gen('social_justice_watch')
	# os.system('open %s -g' % pdf_name)
	
test()