"""
Dimensions quick launcher menubar for OSx
"""

from menus_items import *
from VERSION import VERSION

import rumps
# rumps.debug_mode(True)
from rumps import *
import webbrowser
from collections import OrderedDict
import urllib

def get_clipboard():
	"""Paste the clipboard
	https://stackoverflow.com/questions/7083313/python-get-mac-clipboard-contents/59456366
	"""
	from AppKit import NSPasteboard, NSStringPboardType
	pb = NSPasteboard.generalPasteboard()
	pbstring = pb.stringForType_(NSStringPboardType)
	# print("Pastboard string: %s" % pbstring)
	return pbstring

def url_safe(s):
	return urllib.parse.quote_plus(s.strip())
	

def identifier_menu_builder(nicetitle, MENU_DICT):
	"Reusable code to build menus from an Ordered Dict of identifiers fields"
	menu = rumps.MenuItem(nicetitle)
	SUBTITLE = """Note: clipboard contents are pasted automatically below."""
	for opt_title, opt_tuple in MENU_DICT.items():

		def cb(sender):
			# print(sender.value)
			opt_url, opt_help_msg = sender.value
			clp = get_clipboard()
			window = rumps.Window(message=opt_help_msg + "\n" + SUBTITLE, 
						title=f'Enter a {nicetitle} {sender.title}', 
						default_text=clp, 
						ok="Go!", 
						cancel=True)
			window.icon = "dimensions.icns"
			response = window.run()
			if response.clicked:
				url = opt_url.format(url_safe(response.text))
				webbrowser.open(url)
			else:
				pass

		mi = rumps.MenuItem(opt_title, callback=cb)
		mi.value = opt_tuple
		menu[opt_title] = mi

	return menu



def generic_category_menu_builder(nicetitle, CATS_LIST, url_template):
	"""Build the menu for Dimensions categories. NOTE this this slightly different from
	the version above cause the url needs to be passed. By doing so we can reuse directly
	dimcli.CATEGORIES_DICT (in menus_items.py)"""

	menu = rumps.MenuItem(nicetitle)
	for cat in CATS_LIST:
		def cb(sender):
			url = url_template.format(sender.value)
			webbrowser.open(url)
		mi = rumps.MenuItem(cat['name'], callback=cb)
		mi.value = cat['id']
		menu[cat['name']] = mi

	return menu



def do_full_text_search(sender):
	clp = get_clipboard()
	window = rumps.Window(message='Use quotes for exact searches (clipboard pasted automatically)', title='Full text search - Dimensions', default_text=clp, ok="Go!", cancel=True)
	window.icon = sender.icon
	response = window.run()
	# print(response)
	if response.clicked:
		stringa = url_safe(response.text)
		url = f"https://app.dimensions.ai/discover/publication?search_mode=content&search_text={stringa}&search_type=kws&search_field=full_search"
		webbrowser.open(url)
	else:
		pass







class DimensionsApp(rumps.App):

	def __init__(self):

		menu_spec = [
			"Search Dimensions",
			None,
			self._build_pubs_submenu(),
			self._build_grants_submenu(),
			self._build_patent_submenu(),
			self._build_poldoc_submenu(),
			self._build_cltrial_submenu(),
			self._build_dataset_submenu(),
			self._build_res_submenu(),
			self._build_orgs_submenu(),
			None,
			self._build_cat_for_submenu(), 
			self._build_cat_sdg_submenu(),
			self._build_cat_uoa_submenu(),
			self._build_cat_rcdc_submenu(),
			self._build_cat_hrcs_rac_submenu(),
			self._build_cat_hrcs_hc_submenu(),
			self._build_cat_hra_submenu(),
			self._build_cat_bra_submenu(),		
			None,
			self._build_othersites_submenu(),
			"About",
			None,
		]

		super(DimensionsApp, self).__init__("Dimensions", menu=menu_spec)

		# TIP mac icons: copy image, open in Preview, save as .icns
		self.icon = "dimensions.icns"

	# @rumps.clicked("Open Dimensions")
	# def open_dimensions(self, _):
	# 	webbrowser.open("https://app.dimensions.ai/")

	@rumps.clicked("Search Dimensions")
	def search(self, _):
		"""Full text search submenu"""
		do_full_text_search(self)
	#
	# ABOUT menu
	#

	@rumps.clicked("About")
	def _about_submenu(self, _):
		"""About popup"""
		window = rumps.Window(message=f"Version: {VERSION}", title='QuickDimensions', ok="More info", cancel="Back")
		window.icon = self.icon
		window.default_text = """QuickDimensions is an unofficial Mac OS menu bar launcher for the Dimensions research database.\n\nFor more information see the Github repository."""

		response = window.run()
		if response.clicked:
			url = "https://github.com/lambdamusic/Quick-Dimensions-Menubar/blob/main/README.md"
			webbrowser.open(url)
		else:
			pass

	# @rumps.clicked("Docs: API")
	# def open_docs_api(self, _):
	# 	webbrowser.open("https://docs.dimensions.ai/dsl/")

	# @rumps.clicked("Docs: BigQuery")
	# def open_doc_gbq(self, _):
	# 	webbrowser.open("https://docs.dimensions.ai/bigquery/")

	# @rumps.clicked("Releases..")
	# def open_releases(self, _):
	# 	webbrowser.open("https://github.com/lambdamusic/Quick-Dimensions-Menubar/releases")


	#	
	# sources identifiers 
	#

	def _build_pubs_submenu(self):
		return identifier_menu_builder("Publications..", PUBS_MENU)

	def _build_grants_submenu(self):
		return identifier_menu_builder("Grants..", GRANTS_MENU)

	def _build_patent_submenu(self):
		return identifier_menu_builder("Patents..", PATENTS_MENU)

	def _build_poldoc_submenu(self):
		return identifier_menu_builder("Policy Documents..", POLICY_DOCUMENTS_MENU)

	def _build_cltrial_submenu(self):
		return identifier_menu_builder("Clinical Trials..", CLINICAL_TRIALS_MENU)

	def _build_dataset_submenu(self):
		return identifier_menu_builder("Datasets..", DATASETS_MENU)

	def _build_res_submenu(self):
		return identifier_menu_builder("Researchers..", RESEARCHERS_MENU)

	def _build_orgs_submenu(self):
		return identifier_menu_builder("Organizations..", GRID_MENU)

	#
	# categories
	#

	def _build_cat_for_submenu(self):
		newlist = sorted(CATEGORIES_DICT['category_for'], key=lambda k: k['name'])
		return generic_category_menu_builder("FOR", newlist, 
			"""https://app.dimensions.ai/discover/publication?and_facet_for={}""")

	def _build_cat_sdg_submenu(self):
		newlist = sorted(CATEGORIES_DICT['category_sdg'], key=lambda k: k['name'])
		return generic_category_menu_builder("SDG", newlist, 
			"""https://app.dimensions.ai/discover/publication?and_facet_sdg={}""")

	def _build_cat_uoa_submenu(self):
		newlist = sorted(CATEGORIES_DICT['category_uoa'], key=lambda k: k['name'])
		return generic_category_menu_builder("UoA", newlist, 
			"""https://app.dimensions.ai/discover/publication?and_facet_uoa={}""")

	def _build_cat_rcdc_submenu(self):
		newlist = sorted(CATEGORIES_DICT['category_rcdc'], key=lambda k: k['name'])
		return generic_category_menu_builder("RCDC", newlist, 
			"""https://app.dimensions.ai/discover/publication?and_facet_rcdc={}""")


	def _build_cat_hrcs_rac_submenu(self):
		newlist = sorted(CATEGORIES_DICT['category_hrcs_rac'], key=lambda k: k['name'])
		return generic_category_menu_builder("HCRC RAC", newlist, 
			"""https://app.dimensions.ai/discover/publication?and_facet_hrcs_rac={}""")

	def _build_cat_hrcs_hc_submenu(self):
		newlist = sorted(CATEGORIES_DICT['category_hrcs_hc'], key=lambda k: k['name'])
		return generic_category_menu_builder("HCRC HC", newlist, 
			"""https://app.dimensions.ai/discover/publication?and_facet_hrcs_hc={}""")

	def _build_cat_hra_submenu(self):
		newlist = sorted(CATEGORIES_DICT['category_hra'], key=lambda k: k['name'])
		return generic_category_menu_builder("HRA", newlist, 
			"""https://app.dimensions.ai/discover/publication?and_facet_health_research_areas={}""")

	def _build_cat_bra_submenu(self):
		newlist = sorted(CATEGORIES_DICT['category_bra'], key=lambda k: k['name'])
		return generic_category_menu_builder("BRA", newlist, 
			"""https://app.dimensions.ai/discover/publication?and_facet_broad_research_areas={}""")



	def _build_othersites_submenu(self):
		"Static links menu"
		menu = rumps.MenuItem("Other sites..")

		for title, value in ABOUT_MENU.items():
			def cb(sender):
				url = sender.value
				webbrowser.open(url)

			mi = rumps.MenuItem(title, callback=cb)
			mi.value = value
			menu[title] = mi

		return menu


if __name__ == "__main__":
	DimensionsApp().run()