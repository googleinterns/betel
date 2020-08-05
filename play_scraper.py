from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve

class PlayPageScraper:
	def __init__(self, location):
		self._base_url = "https://play.google.com/store/apps/details?id="
		self._storage_dir = location
		
	def get_html(self, app_id, language=None):
		url = self._base_url + app_id
		
		if language is not None:
			url += "&hl=" + language
		
		page = urlopen(url)
		soup = BeautifulSoup(page, 'html.parser')
		
		return soup
		
	def get_icon(self, app_id, language=None, directory=""):
		html = self.get_html(app_id, language)
		
		icon = html.find(class_="T75of sHb2Xb")
		src = icon["src"]
		
		location = self._storage_dir + directory

		_, _ = urlretrieve(src, location + "/icon_" + app_id)

