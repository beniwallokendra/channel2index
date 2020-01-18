#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'channel2index'

import os

from html_telegraph_poster import TelegraphPoster
from telegram.ext import Updater, MessageHandler, Filters

def getPoster(token):
	if token:
		return TelegraphPoster(access_token = token)
	return TelegraphPoster()

def post(token, source):
	p = getPoster(token)
	print(source)
	if source.username:
		author_url = 't.me/' + source.username,
	else:
		author_url = None
	r = p.post(
		title = source.name + '频道手册', 
		author = source.name, 
		author_url = author_url,
		text = str(article.text))
	return r['url']

def gen(source, bot_token, telegraph_token=None):
	tele = Updater(bot_token, use_context=True)
	test_channel = tele.bot.get_chat(-1001181967872)
	source = source.split('/')[-1]
	source = tele.bot.get_chat(source)
	post(telegraph_token, source)
		

