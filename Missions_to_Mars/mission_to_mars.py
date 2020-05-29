from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
import requests
import re
import time

def scrape():
    
    mars = {}
    
    # ### Scrape NASA Mars News
    
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    browser = webdriver.Chrome()
    browser.get(url)
    soup = bs(browser.page_source, "html.parser")
    
    news_title = soup.find_all('div', class_="content_title")[1].text.strip()
#    news_p = soup.find_all('div', class_="article_teaser_body")[0].text.strip()
    
    mars['news_title'] = news_title
#    mars['news_para'] = news_p
    browser.close()
    # ### Scrape JPL site
    
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser = webdriver.Chrome()
    browser.get(url)
    soup = bs(browser.page_source, "html.parser")
    
    featured_image_url = 'https://www.jpl.nasa.gov'+soup.find_all('a', class_='fancybox')[0]['data-fancybox-href']
    
    mars['featured_image_url'] = featured_image_url
    browser.close()    
    # ### Scrape Mars Weather twitter
    
    url = 'https://twitter.com/marswxreport?lang=en'
    browser = webdriver.Chrome()
    browser.get(url)
    soup = bs(browser.page_source, "html.parser")
    
#    mars_weather = soup.find_all(string=re.compile('InSight'))[0]
    
#    mars['weather_tweet'] = mars_weather
    
    # ### Scrape Mars Facts
    
    facts = pd.read_html('https://space-facts.com/mars/')[0]
    facts_html = facts.to_html(header=False, index=False)
    
    mars['facts_html'] = facts_html
    
    # ### Get Hemisphere Images
    
    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif"},
        {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif"},
    ]
    
    mars['images'] = hemisphere_image_urls
    browser.close()
    return mars