#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'channel2index'

import os
import time

from html_telegraph_poster import TelegraphPoster
import telegram
import telegram.ext
from telegram.ext import Updater, MessageHandler, Filters

def getPoster(token):
	if token:
		return TelegraphPoster(access_token = token)
	return TelegraphPoster()

def post(token, source, posts):
	p = getPoster(token)
	if source.username:
		author_url = 'https://t.me/' + source.username,
	else:
		author_url = None
	text = '''	
<div>
	<p><strong>【频道简介】</strong></p>
	<p>%s</p>
	<br/>
	<p><strong>【索引】</strong></p>
	%s
</div>
	''' % (source.description.split()[0], ''.join(posts))
	r = p.post(
		title = source.title + '频道手册', 
		author = source.title, 
		author_url = author_url,
		text = text)
	print(r)
	return r['url']

TEST = -1001181967872
CUT = [':', '：', '\n', '.']

def trim(t):
	for c in CUT:
		t = t.split(c)[0]
	return t

def getBrief(r):
	if r.document:
		return trim(r.document.file_name)
	if r.text: 
		return trim(r.text)
	else:
		print(r)
		return 'xx'

def gen(source, bot_token, telegraph_token=None):
	tele = Updater(bot_token, use_context=True)
	test_channel = tele.bot.get_chat(-1001181967872)
	source = source.split('/')[-1]
	source = tele.bot.get_chat('@' + source)
	posts = []
	raw_index = 0
	real_index = 0
	skip = 0
	while skip < 30:
		raw_index +=1
		try:
			r = tele.bot.forward_message(TEST, source.id, raw_index)
		except:
			skip += 1
			continue
		skip = 0
		brief = getBrief(r)
		link = 't.me/%s/%s' % (source.username, raw_index)
		real_index += 1
		posts.append(
			'<div>%d.<a href="%s">%s</a></div>' % 
			(real_index, link, brief))
		if raw_index > 10:
			break
	post(telegraph_token, source, posts)
		

