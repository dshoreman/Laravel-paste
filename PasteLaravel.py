#!/usr/bin/python
import sublime, sublime_plugin, urllib, os, webbrowser
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

    def get_information(self):
        show_paste_by = self.get_setting("show_paste_by")
        return show_paste_by and ( os.linesep + show_paste_by ) or ''

    def get_signature(self):
        signature = self.get_setting("signature")
        if (signature):
            return os.linesep + os.linesep + '// ' + signature
        else:
            return ''

    def open_in_browser(self, url):
        open_in_browser = self.get_setting("open_in_browser")
        if (open_in_browser == True):
            webbrowser.open_new_tab(url)

    def get_setting(self, key):
        s = sublime.load_settings("PasteLaravel.sublime-settings")
        if s and s.has(key):
            return s.get(key)

    def run(self, edit):
        body = self.get_file_name()
        body += self.get_text()
        body += self.get_signature()
        body += self.get_information()
        res = self.send_to_paste(body)
        url = res.geturl()
        sublime.set_clipboard(url)
        sublime.status_message('Paste URL is in your clipboard: ' + url)
        self.open_in_browser(url)