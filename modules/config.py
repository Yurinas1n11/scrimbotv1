#!/usr/bin/python2
# encoding: utf-8

import shutil, os
from importlib.machinery import SourceFileLoader
from modules import console, bot

def init(dirname=""):
	global cfg
	
	#load config
	try:
		cfg = SourceFileLoader('cfg', 'config.cfg').load_module()
	except Exception as e:
		console.display("ERROR| ERROR PARSING config.cfg FILE!!! {0}".format(str(e)))
		console.terminate()
	
	#check if we need to update from previous stats system
	if os.path.isdir('channels'):
		console.display("OLD DATABASE FOLDER FOUND! PLEASE RUN 'updater.py' OR DELETE/RENAME 'channels' FOLDER.")
		os._exit(0)

def new_channel(channel, admin):
	path = "channels/"+channel.id
	shutil.copytree("channels/default", path)
	c = bot.Channel(channel)
	c.update_config("ADMINID", admin.id)
	bot.channels.append(c)
	console.display("SYSTEM| CREATED NEW PICKUP CHANNEL: {0}>{1}".format(channel.server.name, channel.name))

def delete_channel(channelid):
	for i in bot.channels:
		if i.id == channelid:
			bot.channels.remove(i)
			i.stats.close()

	oldpath = "channels/"+channelid
	newpath = "trash/"+channelid
	if os.path.exists(oldpath):
		if os.path.exists(newpath):
			shutil.rmtree(newpath)
		shutil.move(oldpath, newpath)
		return True
	return False

def backup_channel(channel, name):
	path = "channels/{0}/stats.sql".format(channel.id)
	backup_path = "channels/{0}/backup_{1}.sql".format(channel.id, name)
	shutil.copy(path, backup_path)

def load_backup_channel(channel, name):
	backup_path = "channels/{0}/backup_{1}.sql".format(channel.id, name)
	path = "channels/{0}/stats.sql".format(channel.id)
	if os.path.exists(backup_path):
		channel.reset_players()
		channel.stats.close()
		shutil.copy(backup_path, path)
		channel.__init__(channel.channel)
		return True
	else:
		return False
