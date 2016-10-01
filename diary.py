#!/usr/bin/env python2
from collections import OrderedDict
import datetime
import os
import sys

from peewee import *

db = SqliteDatabase('diary.db')

class Entry(Model):
	#no limit to how long text is
	content = TextField()

	#notice that there are no parenthesis after datetime.datetime.now
	#that's because it will be executed when the timestamp is created
	#not when the script is run
	timestamp = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = db


def initialize():
	"""create the database and the table if they don't exist"""
	db.connect()
	db.create_tables([Entry], safe=True)


def clear():
	os.system('cls' if os.name == 'nt' else 'clear')


def menu_loop():
	"""show the menu"""
	#initializing a variable without setting a value
	choice = None

	while(choice != 'q'):
		clear()
		print("Enter 'q' to quit.")
		for key, value in menu.items():
			print('{}) {}'.format(key, value.__doc__))
		choice = raw_input('Action: ').lower().strip()
	
		if choice in menu:
			clear()
			menu[choice]()


import sys, tempfile, os
from subprocess import call

def myEditor(msg=""):
	"""Editor that gets data"""
	EDITOR = os.environ.get('EDITOR','vim') #that easy!
	initial_message = msg # if you want to set up the file somehow

	with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
		tf.write(initial_message)
		tf.flush()
		call([EDITOR, tf.name])
		# do the parsing with `tf` using regular File operations.
		# for instance:
		tf.seek(0)
		edited_message = tf.read()
	return edited_message

def add_entry(prev_data=""):
	"""Add an entry"""

	print("Enter  your entry. please ctrl+d when finished.")
	data = myEditor(prev_data)#sys.stdin.read().strip()

	if data:
		if raw_input('Save entry? [Y/n] ').lower() != 'n':
			Entry.create(content=data, unique=True)
			print("Saved successfully!")


def view_entries(search_query=None):
	"""View previous entries"""
	entries = Entry.select().order_by(Entry.timestamp.desc())
	if search_query:
		entries = entries.where(Entry.content.contains(search_query))


	for entry in entries:
		timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
		clear()
		print(timestamp)
		print('='*len(timestamp))
		print(entry.content)
		print('\n\n' + '='*len(timestamp))
		print('n) next entry')
		print('d) delete entry')
		print('q) return to main menu')
		print('e) edit this entry') 
		next_action = raw_input('Action: [Ndq] ').lower().strip()

		if next_action == 'q':
			break
		elif next_action == 'd':
			delete_entry(entry)
		elif next_action == 'e':
			if raw_input("are you sure: [y/n]").lower() == 'y':
				prev_data = entry.content
				entry.delete_instance()
				clear()
				add_entry(prev_data)


def search_entries():
	"""Search entries for a string."""
	view_entries(raw_input('Search query: ').split()[0])


def delete_entry(entry):
	"""Delete an entry"""
	if raw_input('Are you sure? [Y/N]').lower() == 'y':
		entry.delete_instance()
		print("Entry deleted successfully")

def Help():
	"""Help"""
	helpmsg = "Note: searching only supports single word search in diary entry.\n\
	So it is remommended to mark special events,\n\
	and headings using your own format.\n\
	For example:  ```first_day_school```\n"
	print helpmsg
	raw_input('press any key..')

menu = OrderedDict([
	('a', add_entry),
	('v', view_entries),
	('s', search_entries),
	('h', Help)
])


if __name__ == '__main__':
	initialize()
	menu_loop()
