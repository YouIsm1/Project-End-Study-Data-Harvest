
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
import random
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

 
# Connecting to the MongoDB database
def connect_to_database():
    client = MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB connection string
    database = client["products_database"]  # Replace with your database name
    print("Connected to MongoDB")
    return database

# Creating the collection in MongoDB
def create_collection(database):
    # Check if the collection exists
    if "amazon_product_collection" in database.list_collection_names():
        # If it exists, drop it
        database["amazon_product_collection"].drop()
        print("Existing collection dropped successfully")

    # Create a new collection
    collection = database["amazon_product_collection"]
    print("Collection created successfully")
    return collection

def convert_currency(indian_price):
   us_dollar_price_temp = float(indian_price) 
   us_dollars = us_dollar_price_temp * 0.012
   return us_dollars
    
# Search for a product and get its URL
def search_products(product_name,user_agents):

    base_search_url = "https://www.amazon.in/s?k="
    search_url_beta = base_search_url + product_name.replace(" ", "+")
    search_url = search_url_beta + "&ref=nb_sb_noss_1"
    
    #defining user agents to try to pass the amazon bot detector hehehe
    
    response = None
    for user_agent in user_agents:
        #set the headers
        HEADERS = ({'User-Agent' : user_agent})

        response = requests.get(search_url,headers=HEADERS)
        print(response)

        # If the response status is not 503, break the loop
        if response.status_code ==200:
            break
        # Otherwise, sleep for a while before trying the next user agent
        
        time.sleep(5)
    
    html_content = BeautifulSoup(response.text, "html.parser")
    product_elements = html_content.find_all("a",{'class' : "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal" })
    
    #getting the price element (if we're on the uk link of amazon!)
    prices = []
    try :
      price_elements = html_content.find_all("span",{"class":"a-price-whole"})
      for price_element in price_elements: 
        if price_element is not None :
           price = price_element
           prices.append(price.text)
        else : 
            print("No Price Found!")
            prices.append('0')
      print("the prices that could be scrapped : ", prices[:5])
    except :
       print("div element not found !")
           
    #print("product_links : ",product_links)find

    links_list = [] # Initialize an empty list to store the product links

    if product_elements:
        print("got the product elements ! nice !")
        
        # Extract all product links and return them in a list
        for link in product_elements :
           link_href = link.get('href')
           if link_href:
              links_list_element = "https://www.amazon.in" + link_href
              links_list.append(links_list_element)
           else : print("the code couldn't get the href elements")
        
        if links_list:
           print("double niice ! Found the products links ") #, links_list
           time.sleep(5)  # Add a delay of 5 seconds between each request
           return (links_list[:1] , prices[:3] ) # return the first 5 links and prices
       
        else : 
            print("link_list variable is equal to none :/ ") 
            return None          
    else:
        print("didn't find product links :( error f search product function ")
        return None 

def get_comments_img(browser, actual_review_div):
  """
  Extracts image URLs from a comment div using Selenium.

  Args:
      driver: A Selenium WebDriver instance.
      actual_review_div: A Selenium WebElement representing the comment div.

  Returns:
      A list of image URLs found within the comment div.
  """
  img_srcs = []

  try:
    # Find the image container div
    img_div = actual_review_div.find_element(By.CSS_SELECTOR, ".a-section.a-spacing-medium.review-image-container")

    if img_div:
      # Find all image elements
      img_elements = img_div.find_elements(By.CSS_SELECTOR, ".review-image-tile")

      for img_element in img_elements:
        # Extract image URL using attribute
        src = img_element.get_attribute("src")
        img_srcs.append(src)

  except NoSuchElementException:
    # Handle case where no image container is found
    pass

  return img_srcs
def get_comments(browser,link_to_comment_page):
  print("inside the get comment function ! ")
  comments = []
  browser.get(link_to_comment_page)
  for trying in range(10):
    try:
      time.sleep(5)
      WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".a-section.review.aok-relative")))
      actual_review_divs = browser.find_elements(By.CSS_SELECTOR, ".a-section.review.aok-relative")

      if actual_review_divs:
        print("got the actual_review_divs")

        for actual_review_div in actual_review_divs[:10]:
          try:
            review_title_element = actual_review_div.find_element(By.CSS_SELECTOR, "[data-hook='review-title']")
            i_element = review_title_element.find_element(By.CSS_SELECTOR, "[data-hook='review-star-rating']")
            if i_element:
              commentors_rating = i_element.find_element(By.CLASS_NAME, "a-icon-alt").text
              print("comment rating done!")
            elif actual_review_div.find_element(By.CLASS_NAME, "a-icon.a-icon-star.a-star-1.review-rating"):
              i_element = actual_review_div.find_element(By.CLASS_NAME, "a-icon.a-icon-star.a-star-1.review-rating")
              commentors_rating = i_element.find_element(By.CLASS_NAME, "a-icon-alt").text
              print("got the comment rating!")
            else:
              commentors_rating = "No Rating Provided"

            comment_spans = review_title_element.find_elements(By.TAG_NAME, "span")
            comment_title = comment_spans[2].text if len(comment_spans) > 2 else "No Title Found"
            print("comment title:", comment_title)

            comment_temp = actual_review_div.find_element(By.CSS_SELECTOR, ".a-size-base.review-text.review-text-content")
            comment_temp2 = comment_temp.find_element(By.TAG_NAME, "span")
            comment = comment_temp2.text.replace("<br>", " | ")
            print("the actual comment:", comment)

            comments_imgs = [] 
            comments_imgs = get_comments_img(browser,actual_review_div) 

            comment_data = {
                "rating": commentors_rating,
                "title": comment_title,
                "comment": comment,
                "imgs": comments_imgs
            }
            comments.append(comment_data)
            print("one comment done!")

          except (NoSuchElementException, TimeoutException) as e:
            print("Failed scraping specific elements within a comment div:", e)

        if comments:
          print("all done!")
          return comments

    except Exception as e:
      print("Error occurred during comment scraping:", e)

  print("No comments found after", trying + 1, "attempts.")
  return comments


def scrape_data_with_selenium(links_list,product_prices,user_agents, collection):

   un_separated_comments = []
   


   useragent = random.choice(user_agents)
   # Initialize Firefox service and options
   service = Service()
   service.path = GeckoDriverManager().install()
   firefox_options = webdriver.FirefoxOptions()
   firefox_options.headless = True  # Set to True if you don't want a visible browser
   #firefox_options.set_preference("general.useragent.override", random.choice(user_agents))
    


   for link,price in zip(links_list,product_prices):
     time.sleep(5)
     for trying in  range(len(user_agents)): 
      try:
         
         # useragent = random.choice(user_agents)
         # headers = {"User-Agent": useragent,}
         #    # Send a HEAD request with the user-agent to the link
         # response = requests.head(link, headers=headers, timeout=10)
         # print("response of the product page :",response)

         #    # If the request is successful, continue with scraping
         # if response.status_code == 200:
            print("intering the product page...")
      
            #resetting the user-agent
            useragent = random.choice(user_agents)
            firefox_options.add_argument(f"user-agent={useragent}")
            browser = webdriver.Firefox(service=service, options=firefox_options)

            time.sleep(3)
            
            #getting the link 
            browser.get(link)
            if browser is not None: 
               print("entered product page !")

            # wait for the title element to be present on the page
            title_element = WebDriverWait(browser, 10).until(
               EC.presence_of_element_located((By.ID, "productTitle")))
            if title_element : 
               print("got the title ! : ", title_element.text.strip())
            title = title_element.text.strip()

             #getting the imgs
            try: 
               img =''
                
               img_div =  WebDriverWait(browser, 15).until(
               EC.presence_of_element_located((By.ID, 'imgTagWrapperId')))
               img_element = img_div.find_element(By.TAG_NAME,'img')
               print("got the imgs element !") if img_element else print("no img element")
               img = img_element.get_attribute('src')
                    
               if img : 
                    print("got the img src !",img) 
               else : 
                    print("no  image found.")
            except Exception as e :
                print ("error at getting the imgs : " ,e)
            




            #Scraping the rating
            try : 
             average_reviews_span = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'averageCustomerReviews')))
             
             if average_reviews_span is not None :
               print("got the  number of review (average_reviews_span)")
               rating_span = average_reviews_span.find_element(By.ID, 'acrPopover')
               rating = rating_span.get_attribute('title')
               
               if rating is not None:
                  print("got the rating !")
               
               else :
                  rating_span2= rating_span.find_element(By.CSS_SELECTOR,'span.a-size-base a-color-base')
                  rating = rating_span2.text if rating_span2 else print("no rating found")
            
             else : print("no reviews found ! ")
            except Exception as e : 
               # Handle the case when the element is not found within the timeout
               print("No reviews found!")
               rating = "No rating available"



             #Scraping the description text lists
            description_div = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'feature-bullets')))
            if description_div is not None :
               print ("got the description div !")
               description_spans = description_div.find_elements(By.CSS_SELECTOR, 'span.a-list-item')
               description = ' '.join(span.text for span in description_spans) if description_spans else None
            else:
               print("Description div not found.")
               description = "no description found"


            #Scraping the comments 
               #getting data from the comments section 
            link_to_comment_page_div =  WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'reviews-medley-footer')))
            try : 
               print("found the comment div ")
               temp = link_to_comment_page_div.find_element(By.CSS_SELECTOR, '.a-row.a-spacing-medium') 
               link_to_comment_page_element = temp.find_element(By.CSS_SELECTOR, '.a-link-emphasis.a-text-bold')
               link_to_comment_page = link_to_comment_page_element.get_attribute('href')
                               
               if link_to_comment_page is not None :
                  print("got the comment page !" )
                  print(link_to_comment_page)
                  browser.quit()
               else : 
                  print("no comment page link !")
                  break

               #Setting the retrying method 
               for trying in range(len(user_agents)): 
                 
                  #getting the response before trynna run selenium
                  time.sleep(5)
                  useragent = random.choice(user_agents)               
                  try:
                     print("entering the comment page...")
                     try :
                           try:
                                 un_separated_comments =[]
                                 #comment_page_response = BeautifulSoup(response.content, 'html.parser')
                                 #print("comment_page_response:", comment_page_response)
                                 
                                 useragent = random.choice(user_agents)
                                 firefox_options.add_argument(f"user-agent={useragent}")
                                 browser = webdriver.Firefox(service=service, options=firefox_options)

                                 un_separated_comments = get_comments(browser,link_to_comment_page)
                                 print("un_separated_comments:", un_separated_comments)

                                 if un_separated_comments  :
                                    product_data = {
                                                   "name"        : title,
                                                   "img"         : img,
                                                   "price"       : price,
                                                   "rating "     :rating ,
                                                   "description" : description ,
                                                   "un_separated_comments": un_separated_comments,
                                                                }
                                    browser.quit()
                                    break

                                 if not un_separated_comments  :
                                    print ("no comment found")
                                    browser.quit()

                           except  Exception as e:
                                 print("error at getting the comments :",e)
                               

                     except Exception as e:
                        print(f"Error scraping the comment page : {e}...retrying in 5seconds...")
                        browser.quit()
                  except Exception as e:
                        print(f"failed intering the comment page : {e}")
                        browser.quit()
            except Exception as e:
                  print("didnt find the comment div, line 321 : ",e)

             #discount = discount_element.text if discount_element else None
             #seller_name = seller_name_element.text if seller_name_element else None
             
            # Insert the scraped data into the products collection
            collection.insert_one(product_data)
            print("One document's insertion is complete, from amazon to db !")
            time.sleep(random.uniform(3, 15))
            browser.quit()
            break

      except Exception as e:
            print(f"Error scraping data: {e}...retrying in 5seconds...")
            browser.quit()

      time.sleep(2)

            
    # Close the WebDriver after scraping all product pages
   browser.quit()

#_______________________________________________MAIN_________________________________________________________________
import sys
def main(product_name):
   print("strating the amazone scraping script")

    
   user_agents = [
    
   #  'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1',
   #  'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
   #  'Mozilla/5.0 (compatible; YandexAccessibilityBot/3.0; +http://yandex.com/bots)',
   #   'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion',
   #   'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
   #   'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
   #   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
   #   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
   #   'Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00',
   #   'Opera/9.60 (Windows NT 6.0; U; en) Presto/2.1.1',
   #  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123."                                   ,
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.3"    ,
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.3"    ,
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117."                                   ,
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0 (Edition Campaign 75",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.3"              ,
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Config/91.2.2025.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115."                                     ,
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"                                     ,
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"                                          ,
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko"                                          ,
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"   ,
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"                                   ,
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"    , 
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'    ,
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' ,
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'                                           ,
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'  ,
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'  ,
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'  ,
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'          ,
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36' ,
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36' ,
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' ,
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'  ,
    ]
 
   # if len(sys.argv) != 2:
   #      print("Usage: python amazon_pyscraper.py <product_name>")
   #      sys.exit(1)
   # product_name = sys.argv[1]



   try:   
        
        db_connection = connect_to_database()
        if db_connection is not None:
            product_collection = create_collection(db_connection)
            
            # Search for the product and get its URL
            links_list , product_prices =  search_products(product_name,user_agents)

            if links_list:
               # Scrape data using the obtained product URL
               scrape_data_with_selenium(links_list, product_prices, user_agents, product_collection)
               print("Scraping finished. Check the database for the results.")
            else:
               print(f"No search results found for {product_name}")


   except Exception as e:
       print("Error (main function) at scraping the data:", str(e))