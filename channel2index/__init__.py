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

PSIZE = 40

def getPoster(token):
	if token:
		return TelegraphPoster(access_token = token)
	return TelegraphPoster()

def getList(db, start, end):
	print(start, end, len(db))
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
	return ''.join(posts[start:end])

def post(token, source, db, page):
	p = getPoster(token)
	if source.username:
		author_url = 'https://t.me/' + source.username,
	else:
		author_url = None
	content = getList(db, (page - 1) * PSIZE, page * PSIZE)
	text = '''	
<div>
	<p><strong>【频道简介】</strong></p>
	<p>%s</p>
	<p><a href="%s">点此进入频道</a></p>
	<br/>
	<p><strong>【索引】</strong></p>
	%s
</div>
	''' % (source.description.split()[0], author_url, content)
	r = p.post(
		title = '【频道手册】%s 第%d页' % (source.title, page), 
		author = source.title, 
		author_url = author_url,
		text = text)
	return r['url']

def trim(text):
	if re.search(u'[\u4e00-\u9fff]', text):	
		if len(text) > 35:	
			return text[:30] + '...'	
	else:
		if len(text) > 65:
			return text[:60] + '...'	
	return text

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
		if 't.co' in external_link['href']:
			text = trim(external_link.find('div', class_='link_preview_description').text)
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
	page = 1
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
			if len(db) >= page * PSIZE:
				r = post(telegraph_token, source, db, page)
				os.system('open %s -g' % r)
				page += 1
	r = post(telegraph_token, source, db, page)
	os.system('open %s -g' % r)
	return post(telegraph_token, source, posts)
		

