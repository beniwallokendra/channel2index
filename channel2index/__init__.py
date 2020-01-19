#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'channel2index'

import os
import time
import re

from html_telegraph_poster import TelegraphPoster
import telegram
import telegram.ext
from telegram.ext import Updater, MessageHandler, Filters
from telegram_util import isUrl
import cached_url
from bs4 import BeautifulSoup

def getPoster(token):
	if token:
		return TelegraphPoster(access_token = token)
	return TelegraphPoster()

def getList(db):
	real_index = 0
	raw = 0
	posts = []
	while real_index < len(db):
		raw += 1
		if raw not in db:
			continue
		brief, message_type, link = db[raw]
		real_index += 1
		posts.append(
			'<p>%d. <a href="%s">%s</a></p>' % 
			(real_index, link, brief))
	return ''.join(posts)

def post(token, source, db):
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
	''' % (source.description.split()[0], getList(db))
	r = p.post(
		title = '【频道手册】' + source.title, 
		author = source.title, 
		author_url = author_url,
		text = text)
	return r['url']

def tooShort(text):
	if re.search(u'[\u4e00-\u9fff]', text):
		return len(text) < 8
	else:
		return len(text) < 20

def process(soup, db):
	for message in soup.find_all('div', class_='tgme_widget_message_bubble'):
		link = message.find('a', class_='tgme_widget_message_date')['href']
		raw_index = int(link.split('/')[-1])
		if raw_index in db:
			continue
		external_link = message.find('a', class_='tgme_widget_message_link_preview')
		if not external_link:
			continue
		link_title = external_link.find('div', class_='link_preview_title')
		if not link_title:
			continue
		text = link_title.text
		if tooShort(text):
			text = external_link.find('div', class_='link_preview_description').text
		db[raw_index] = text, '链接', external_link['href']
			
def gen(source, bot_token, telegraph_token=None):
	tele = Updater(bot_token, use_context=True)
	test_channel = tele.bot.get_chat(-1001181967872)
	source = source.split('/')[-1]
	source = tele.bot.get_chat('@' + source)
	db = {}
	raw_index = 0
	real_index = 0
	skip = 0
	while skip < 20:
		raw_index +=5
		link = 'https://t.me/s/%s/%s' % (source.username, raw_index)
		try:
			soup = BeautifulSoup(cached_url.get(link), 'html.parser')
		except Exception as e:
			print(e)
			skip += 1
			continue
		old_len = len(db)
		process(soup, db)
		if old_len == len(db):
			skip +=1
		else:
			skip = 0
			if len(db) % 40 == 0:
				r = post(telegraph_token, source, db)
				print(r)
				os.system('open %s -g' % r)
	return post(telegraph_token, source, posts)
		

