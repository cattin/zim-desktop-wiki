# -*- coding: utf-8 -*-

# Copyright 2008 Jaap Karssenberg <pardus@cpan.org>

'''FIXME'''

import webbrowser

from zim.fs import TmpFile
from zim.plugins import PluginClass
import zim.templates
from zim.exporter import BaseLinker

ui_xml = '''
<ui>
	<menubar name='menubar'>
		<menu action='file_menu'>
			<placeholder name='print_actions'>
				<menuitem action='print_to_browser'/>
			</placeholder>
		</menu>
	</menubar>
</ui>
'''

ui_actions = (
	# name, stock id, label, accelerator, tooltip
	('print_to_browser', 'gtk-print', '_Print to Browser', '<ctrl>P', 'Printto browser'),

)

class SpellPlugin(PluginClass):
	'''FIXME'''

	plugin_info = {
		'name': 'Print to Browser',
		'description': '''\
This plugin provides a workaround for the lack of
printing support in zim. It exports the current page
to html and opens a browser. Assuming the browser
does have printing support this will get your
data to the printer in two steps.

This is a core plugin shipping with zim.
''',
		'author': 'Jaap Karssenberg',
	}

	def __init__(self, ui):
		PluginClass.__init__(self, ui)
		if self.ui.ui_type == 'gtk':
			self.ui.add_actions(ui_actions, self)
			self.ui.add_ui(ui_xml, self)

	def print_to_browser(self):
		file = self.print_to_file()
		webbrowser.open('file://%s' % file)

	def print_to_file(self):
		file = TmpFile('print-to-browser.html') 
		template = zim.templates.get_template('html', 'Print')
		template.set_linker(BaseLinker('html', self.ui.notebook, self.ui.page))
		html = template.process(self.ui.notebook, self.ui.page)
		file.writelines(html)
		return file
