#!/usr/bin/python
import sublime, sublime_plugin, urllib, os
try:
    from urllib.request import urlopen
    import urllib.parse
except ImportError:
    from urllib2 import urlopen

class PastelaravelCommand(sublime_plugin.TextCommand):
    def send_to_paste(self, body):
        try:
            data = urllib.urlencode( { 'paste' : body } ).encode('utf-8')
        except AttributeError:
            data = urllib.parse.urlencode( { 'paste' : body } ).encode('utf-8')

        http_file = urlopen('http://paste.laravel.com/', data)
        return http_file

    def get_text(self):
        text = "";
        selection = 1;

        for region in self.view.sel():

            if not region.empty():

                if text != "":
                    text += os.linesep + os.linesep + os.linesep

                text += "// Selection: " + str(selection) + os.linesep
                text += self.view.substr(sublime.Region(region.begin(), region.end()))
                selection += 1

        if text != "":
            return text
        else:
            return self.view.substr(sublime.Region(0, self.view.size()))

    def get_file_name(self):
        filename = self.view.file_name()
        if not filename is None:
            filenames = filename.split('/')
            return '// Filename: ' + filenames[-1] + os.linesep
        else:
            return '// Filename: (empty)' + os.linesep

    def run(self, edit):
        body = self.get_file_name();
        body += self.get_text()
        res = self.send_to_paste(body)
        url = res.geturl()
        sublime.set_clipboard(url)
        sublime.status_message('Paste URL is in your clipboard: ' + url)