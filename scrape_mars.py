#Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
from time import sleep

url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

#NASA Mars News
def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)




def scrape():
    browser=init_browser()
    mars_data={}
    browser.visit(url)
    sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    #print(soup.prettify())

    titles=soup.find_all('div', class_="content_title")


    latest_headline=titles[0].a.text.replace('\n','')

    mars_data["news_title"]=latest_headline

    sub_title=soup.find_all('div', class_="rollover_description_inner")

    latest_sub_title=sub_title[0].text.replace('\n','')

    mars_data["news_p"]=latest_sub_title

    #JPL Mars Space Images
    image_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(image_url)
    sleep(3)
    image_html=browser.html
    soup=BeautifulSoup(image_html,'lxml')
    

    full_image=soup.find_all('a', class_="button")
    full_image[0]
    mars_url="https://www.jpl.nasa.gov"
    next_image_url=mars_url + full_image[0]['data-link']
    browser.visit(next_image_url)
    sleep(3)
    next_image_html=browser.html
    soup=BeautifulSoup(next_image_html,'lxml')
    image=soup.find_all('img')
    featured_image_url=image[6]['src']

    mars_data["src"] = featured_image_url


    #Mars Weather
    twitter_url="https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    sleep(5)
    twitter_html=browser.html
    soup=BeautifulSoup(twitter_html,'lxml')
    #print(soup.prettify())

    tweets=soup.find_all('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    mars_weather=tweets[0].text

    mars_data["latest_tweet"]=mars_weather


    #Mars Facts
    import pandas as pd

    facts_url="https://space-facts.com/mars/"

    tables=pd.read_html(facts_url)
    df=tables[0]


    html_table=df.to_html().replace('\n','')


    df.to_html('table.html')

    #Mars Hemispheres
    pics_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(pics_url)
    sleep(3)
    pics_html=browser.html
    soup=BeautifulSoup(pics_html,'lxml')
    

    pics=soup.find_all('a', class_='itemLink')

    pics[1]['href']
    url="https://astrogeology.usgs.gov"
    browser.visit(url+pics[1]['href'])

    import requests
    response=requests.get(url+pics[1]['href'])
    soup=BeautifulSoup(response.text,'lxml')
    

    all_a=soup.find_all('a')

    response_two=requests.get(url+pics[3]['href'])
    soup=BeautifulSoup(response_two.text,'lxml')
    

    all_a_second=soup.find_all('a')
    response_three=requests.get(url+pics[5]['href'])
    soup=BeautifulSoup(response_three.text,'lxml')
    
    all_a_third=soup.find_all('a')

    response_four=requests.get(url+pics[7]['href'])
    soup=BeautifulSoup(response_four.text,'lxml')
    

    all_a_fourth=soup.find_all('a')



    hemisphere_image_urls=[{"title":pics[1].h3.text,"img_url":all_a[41]['href']},{"title":pics[3].h3.text,"img_url":all_a_second[41]['href']},
                        {"title":pics[5].h3.text,"img_url":all_a_third[41]['href']},{"title":pics[7].h3.text,"img_url":all_a_fourth[41]['href']}]

    mars_data["src"]=hemisphere_image_urls

    return mars_data

    
