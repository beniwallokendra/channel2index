#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import channel2pdf
import os
import sys

def test():
	pdf_name = channel2pdf.gen('pincongessence')
	os.system('open %s -g' % pdf_name)
	# pdf_name = channel2pdf.gen('equality_and_rights')
	# os.system('open %s -g' % pdf_name)
	# pdf_name = channel2pdf.gen('social_justice_watch')
	# os.system('open %s -g' % pdf_name)
	
test()