# Mission to Mars

## Step 1 - Scraping

########### import dependencies ###########
from bs4 import BeautifulSoup
from splinter import Browser
import request
import pandas as pd
import pymongo
import time

# This is for debugging
def savetofile(contents):
    file = open('_temporary.txt', "a", encoding="utf-8")
    file.write(contents)
    file.close()


############ Initialize browser ###########
def scrape(): 
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


############ NASA MARS NEWS ###############
def scrape_mars_info():

    # Create Mission to Mars dictionary that can be imported into Mongo
    mars_info = {} 

    try:
        # Initialize browser
        browser = init_browser()
    
        # URL of page to be scraped - NASA Mars News Site 
        nasa_url = 'https://mars.nasa.gov/news/'
        browser.visit(nasa_url)
        time.sleep(5)
        
        # Create BeautifulSoup object; parse with 'html.parser'
        html = browser.html
        soup_nasa = BeautifulSoup(html, 'html.parser')
        
        # Collect the latest News Title from NASA Mars News Site
        news_info = []
    
        news_title = soup_nasa.find('div', class_='content_title').find('a').text.strip()
        print(news_title)

        # Retrieve the latest news paragraph from NASA Mars News Site
        news_p = soup_nasa.find('div', class_='article_teaser_body').text.strip()
        print(news_p)

        # Add title and paragraph to a dictionary
        news_dict = {"news_title" : news_title, "news Paragraph" : news_p}

        # Append the retreived information
        news_info.append(news_dict)

        ## Dictionary entry from MARS NEWS
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p
    
        browser.quit()

    except Exception as error:
        print(error)
    
###############################################################
############ JPL Mars Space Images - Featured Image ###########
    try:

        # Initialize browser
        browser = init_browser()
        # URL of page to be scraped for featured image - JPL Mars Space Images
        jpl_url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(jpl_url_image)
        time.sleep(5)
        
        # Browse through the page
        # Find the image url for the current Featured Mars and click the full image button
        featured_full_image = browser.find_by_id('full_image')
        featured_full_image.click()
        
        # Browse through the page
        time.sleep(5)

        # Find the more info button and click
        more_info_images = browser.find_link_by_partial_text('more info')
        more_info_images.click()
        
        # Using BeautifulSoup create an object and parse with 'html.parser'
        html = browser.html
        image_soup = BeautifulSoup(html, 'html.parser')

        # find the related image url
        image_url = image_soup.find('figure', class_='lede').find('img')['src']

        # Use the base url to create an full url
        JPL_link = 'https://www.jpl.nasa.gov'

        featured_image_url = JPL_link + image_url    

        
        ## Dictionary entry from FEATURED IMAGE
        mars_info['featured_image_url'] = featured_image_url 
        
        browser.quit()

    except Exception as error:
        print(error)
###############################################################
############  Mars Weather ####################################
    
    try:
        # Initialize browser
        browser = init_browser()
        
        # URL of page to be scraped - Mars Weather
        mars_twitter_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(url_weather)
        time.sleep(5)
        
        # Create BeautifulSoup object; parse with 'html.parser'
        html_weather = browser.html

        mars_soup = BeautifulSoup(html_weather, 'html.parser')
        
        # Find all elements that contain tweets
        latest_tweets = mars_soup.find_all('div', class_='js-tweet-text-container')
        
        # Loop through latest_tweets to extract for the weather report
        for tweet in latest_tweets:
            weather_tweet = tweet.find('p').text
            if 'Sol' and 'pressure' in weather_tweet:
                print(weather_tweet)
                break       
            else:         
                pass
                    
        latest_tweet = weather_tweet.split("hPa")[0]+"hPa"
        print(latest_tweet)


        ## Dictionary entry from WEATHER TWEET
        mars_info['weather_tweet'] = latest_tweet
        
        browser.quit()

    except Exception as error:
        print(error)

###############################################################
############  Mars Facts ######################################
    try:    
        # Initialize browser
        browser = init_browser()

        # URL of page to be scraped - Mars Facts
        mars_facts_url = 'http://space-facts.com/mars/'
        browser.visit(mars_facts_url)
        time.sleep(5)
        
        # Use Panda's `read_html` to parse the url
        mars_facts = pd.read_html(browser.html)
        mars_facts 
    
        # Find the mars facts DataFrame in the list of DataFrames 
        mars_df = mars_facts[1]
        
        # Set columns to ['Description', 'Value']
        mars_df.columns = ['Description', 'Value']
        
        # Set the index to the `Description` column without row indexing
        mars_df.set_index('Description', inplace=True)
        
        # Use pandas to generate Html Tables from dataframes and save as html file
        # mars_df.to_html('mars_fact_table.html') 
        mars_fact_table = mars_df.to_html('mars_fact_table.html')

        # print(mars_df)
        print(mars_fact_table)

        
        ## Dictionary entry from MARS FACTS
        mars_info['mars_facts'] = mars_fact_table
        
        browser.quit()

    except Exception as error:
        print(error)

###############################################################
############ Mars Hemispheres #################################
    
    try:
        # Initialize browser
        browser = init_browser()
        
        # URL of page to be scraped - Mars Hemispheres
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)
        time.sleep(5)
        
        # Create BeautifulSoup object; parse with 'html.parser'
        html_hemispheres = browser.html

        # Parse HTML with Beautiful Soup
        hemispheres_soup = BeautifulSoup(html_hemispheres, 'html.parser')
        
        # Retreive all items that contain mars hemispheres information
        items = hemispheres_soup.find_all('div', class_='item')

        # Create an empty list to hold dictionaries of hemisphere title with the image url string
        hemisphere_image_urls = []

        # Store the main_ul 
        hemispheres_main_url = 'https://astrogeology.usgs.gov'
        
        # Loop through the items previously stored
        for item in items: 
            # Store title
            title = item.find('h3').text

            # Store link that leads to full image website
            partial_img_url = item.find('a', class_='itemLink product-item')['href']

            # Visit the link that contains the full image website 
            browser.visit(hemispheres_main_url + partial_img_url)

            # HTML Object of individual hemisphere information website 
            partial_img_html = browser.html

            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            individual_soup = BeautifulSoup( partial_img_html, 'html.parser')

            # Retrieve full image source 
            img_url = hemispheres_main_url + individual_soup.find('img', class_='wide-image')['src']

            # Add to dictionary
            hemi_urls = {"title" : title, "img_url" : img_url}
            #hemisphere_image_urls = {"title" : title, "img_url" : img_url}

            # Append the retreived information 
            hemisphere_image_urls.append(hemi_urls)
         
        print(hemisphere_image_urls)
        
        # Close the browser after scraping
        browser.quit()

    except Exception as error:
        print(error)    

    mars_info['hemi_urls'] = hemi_urls

    # Return mars_data dictionary 
    return mars_info