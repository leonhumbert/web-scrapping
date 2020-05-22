from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from time import sleep
import requests as req
import pandas as pd

#def browser with chromedriver
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
    #create global dictionary for the scrapping data
    mars_data = {}

    #Visit Nasa Mars News url
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    #needs rest!!! To self: time.sleep goes after the visit!!!
    time.sleep(3)

    #Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')
   

    # Retrieve the latest element that contains news title and news_paragraph
    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="article_teaser_body").text

    # Add scrapped data to the dictionary 
    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_p

    #JPL Mars Space Images - Featured Image
    # Visit Mars Space Images through splinter module
    image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url_featured)

    # HTML Object 
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_image, 'html.parser')

    # Retrieve background-image url from style tag 
    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Website Url 
    main_url = 'https://www.jpl.nasa.gov'

    # Concatenate website url with scrapped route
    featured_image_url = main_url + featured_image_url

    # Dictionary entry from FEATURED IMAGE
    mars_data['featured_image_url'] = featured_image_url 

    #Mars Weather
    # I am using req.get and xpath here
    # Visit Mars Weather Twitter through splinter module
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    # Request response from weather_url
    twitter_response = req.get(weather_url)

    # Parse HTML with Beautiful Soup
    soup = bs(twitter_response.text, 'html.parser')

    # Find all elements that contain tweets
    latest_tweet = soup.find_all('div', class_="js-tweet-text-container")

    #last tweet is the first elelment of the soup list
    mars_weather = latest_tweet[0].text

    #add to global dictionary
    mars_data['weather_tweet'] = mars_weather

    #Mars Weather Scrap Twitter
    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # Find the rars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']

    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)

    # Save html code to folder Assets
    mars_df.to_html()
    mars_facts = mars_df.to_html()

    # Add to global dictionary
    mars_data['mars_facts'] = mars_facts

    #Mars Hemispheres
    #Visit hemispheres website through splinter module 
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls they ARE 4!!!
    hemisphere_image_urls = []

    # Store the main_url 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for i in items: 
        # Grab and store title
        title = i.find('h3').text
        
        # Store link that takes to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
        
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
        
        # Parse HTML with BeautifulSoup for each individual information website 
        soup = bs( partial_img_html, 'html.parser')
        
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    #Add to global dictionary. choose a shorter name!!!
    mars_data['hiu'] = hemisphere_image_urls

    browser.quit()

    return mars_data




