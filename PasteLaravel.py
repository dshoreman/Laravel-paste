#!/usr/bin/python
import sublime, sublime_plugin, urllib, urllib2

class PastelaravelCommand(sublime_plugin.TextCommand):
	def send_to_paste(self, body):
		data = urllib.urlencode( { 'paste' : body } ).encode('utf-8')
		http_file = urllib2.urlopen('http://paste.laravel.com/', data)
		return http_file

	def run(self, edit):
		body = self.view.substr(self.view.sel()[0])
		res = self.send_to_paste(body)
		url = res.geturl()
		sublime.set_clipboard(url)
		sublime.status_message('Paste URL is in your clipboard: ' + url)