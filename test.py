#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import channel2index
import os
import yaml

with open('CREDENTIALS.yaml') as f:
	CREDENTIALS = yaml.load(f, Loader=yaml.FullLoader)

def test():
	link = channel2index.gen(
		'https://t.me/freedom_watch', 
		bot_token = CREDENTIALS['bot_token'],
		telegraph_token = CREDENTIALS['telegraph_token'])
	os.system('open %s -g' % link)
	
if __name__ == "__main__":
	test()