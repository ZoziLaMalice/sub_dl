from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import imdb
import sys
from optparse import OptionParser
import time

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

print(options.season.split())

if options.serie:
	season = int(options.season)
	episode = int(options.episode)
	lang = str(options.langage)

	ID = ia.search_movie(str(options.serie))[0].movieID
	series = ia.get_movie(ID)
	
	ia.update(series, 'episodes')
	sorted(series['episodes'].keys())

	episode_id = series['episodes'][season][episode].movieID

	driver = webdriver.Firefox(executable_path='/home/zozi/Downloads/geckodriver', firefox_profile=profile)

	driver.get(f'https://www.opensubtitles.org/en/search/sublanguageid-{lang}/imdbid-{episode_id}')
	time.sleep(5)

	sub = driver.find_element_by_xpath('/html/body/div[1]/form/table/tbody/tr[2]/td[1]/strong/a')
	sub.click()
	time.sleep(10)

	dl = driver.find_element_by_css_selector('#bt-dwl-bt')
	dl.click()
	time.sleep(15)

	driver.close()