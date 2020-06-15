import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.common.exceptions import NoSuchElementException
import imdb
import sys
from optparse import OptionParser
import time
import zipfile
import os
import glob

profile = FirefoxProfile()
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", 'application/octet-stream')
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", 'application/zip')

ia = imdb.IMDb()

parser = OptionParser()
parser.add_option("-M", "--movie", dest="movie",
                  help="the name of the movie")

parser.add_option("-S", "--serie", dest="serie",
                  help="the name of the serie")

parser.add_option("-s", "--season", dest="season",
                  help="the number of season if serie")

parser.add_option("-e", "--episode", dest="episode",
                  help="the number of episode if serie")

parser.add_option("-l", "--langage", dest="langage",
                  help="the langage of subtitles")

(options, args) = parser.parse_args()

print(options, args)

home = os.path.expanduser('~')

if options.serie:
	driver = webdriver.Firefox(firefox_profile=profile)	
	
	ID = ia.search_movie(str(options.serie))[0].movieID
	series = ia.get_movie(ID)

	for nb_lang in options.langage.split():
		for nb_season in options.season.split(): 
			for nb_epi in options.episode.split():
				season = int(nb_season)
				episode = int(nb_epi)
				lang = str(nb_lang)
				
				ia.update(series, 'episodes')
				sorted(series['episodes'].keys())

				episode_id = series['episodes'][season][episode].movieID

				driver.get(f'https://www.opensubtitles.org/en/search/sublanguageid-{lang}/imdbid-{episode_id}')
				time.sleep(5)

				try:
					
					sub = driver.find_element_by_xpath('/html/body/div[1]/form/table/tbody/tr[2]/td[1]/strong/a')
					sub.click()
					time.sleep(10)

					dl = driver.find_element_by_css_selector('#bt-dwl-bt')
					dl.click()
					time.sleep(15)

				except NoSuchElementException:

					dl = driver.find_element_by_css_selector('#bt-dwl-bt')
					dl.click()
					time.sleep(15)

				filename = max([home + '/Downloads/' + f for f in os.listdir(home + '/Downloads/')],key=os.path.getctime)

				with zipfile.ZipFile(filename, 'r') as zip_ref:
					zip_ref.extractall(home + f'/Downloads/{options.serie}/{nb_lang}/Season {nb_season}/Episode {nb_epi}')

				os.remove(filename)
				
				folder = home + f'/Downloads/{options.serie}/{nb_lang}/Season {nb_season}/Episode {nb_epi}/'

				for file in glob.glob(folder + '*.nfo'):
				    os.remove(file)

	driver.close()
