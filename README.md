# simple_diary
simple diary maintaining app in python

# DIARY

This diary application uses the PeeWee ORM to allow us to connect to a SQLite database.
The project is part of a course on Treehouse therefore it is mainly for reference. The application currently allows for the following:

- Adding an entry
- Edition an entry
- Deleting an entry
- Viewing all entries
- Searching entries (with containig word)


```python
menu = OrderedDict([
	('a', add_entry),
	('v', view_entries),
	('s', search_entries),
  ('h', Help)
])
```
