from pymongo import MongoClient

import requests
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# Connecting to the MongoDB database
def connect_to_database():
    client = MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB connection string
    database = client["products_database"]  # Replace with your database name
    print("ebay response : Connected to MongoDB")
    return database

# Creating the collection in MongoDB
def create_collection(database):
    # Check if the collection exists
    if "ebay_product_collection" in database.list_collection_names():
        # If it exists, drop it
        database["ebay_product_collection"].drop()
        print("ebay response : Existing collection dropped successfully")

    # Create a new collection
    collection = database["ebay_product_collection"]
    print("ebay response : Collection created successfully")
    return collection

# Search for a product and get its URL
def search_products(product_name,user_agents):

    base_search_url = "https://www.ebay.com/sch/i.html?_nkw="
    search_url = base_search_url + product_name.replace(" ", "+")
    
    #defining user agents to try to pass the eBay bot detector
    
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
    product_elements = html_content.find_all("li",{'class' : "s-item s-item__pl-on-bottom" })
    
    links_list = [] # Initialize an empty list to store the product links
    prices_list=[]

    if product_elements:
        print("ebay response : got the product elements ! nice !")

        for product in product_elements[1:2] :
           
        
        # Extract all product links and return them in a list
            link_element = product.find("a",{'class' : "s-item__link"})
            link_href = link_element.get('href')
           
            if link_href:
              links_list.append(link_href)
           
            else : 
               print("ebay response : the code couldn't get the href elements")
               links_list.append('no link found')

        #getting the price
            price_element = product.find("span",{'class' : "s-item__price"})
            if price_element is not None:
                price = price_element.text
                prices_list.append(price)  
            

        if prices_list :
            print("ebay response : the prices we got  : ",prices_list)

        else :
            print("ebay response : we got no prices !")



        if links_list:
           print("ebay response : double nice! Found the products links ") 
            # Add a delay of 5 seconds between each request
           
        else : 
            print("ebay response : link_list variable is equal to none :/ ") 
            return None          


    
    else:
        print("ebay response : didn't find product links :( error of search product function ")
        return None 
    return (links_list , prices_list)

def get_comments(comment_page_response,browser):
   comments =[]
   try:
      print("ebay response : waiting 10 seconds for the comment elements...")
      time.sleep(10)
      actual_review_divs = comment_page_response.find_all("div",{"class":"card__comment"})
      review_rating_divs  = comment_page_response.find_all("div",{"class":"card__rating"})
      
      #actual_review_divs = WebDriverWait(browser, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card__comment')))
      #review_rating_divs =  WebDriverWait(browser, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card__rating')))

      if actual_review_divs is not None:
         print("ebay response : got the divs!")
         
         for (actual_review_div , review_rating_div ) in zip(actual_review_divs[:10] , review_rating_divs[:20] ):
            
            if actual_review_div  :
               try:
                  
                  comment_temp = actual_review_div.find('span')
                  if comment_temp is not None:
                        comment = comment_temp.text.strip() 
                        
                        print("ebay response : the actual comment : ", comment)
                  else :
                        print("ebay response : problem finding the span element of the comment !")
                  
               
               except Exception as e:
                  print("ebay response : failed scraping the comment text .",e)
            
            else : 
               print("ebay response : Failed to get reviews.")
               

            if review_rating_div :
          
              sgv_element = review_rating_div.find("svg")

              if  sgv_element : 
                  rating = sgv_element.get("data-test-type")
                  print("ebay response : value of rating :" , rating)
              else :
                  rating = ''

            else:
                print('Could not find the review_rating_divs')
                rating = ''
        
            comment_data ={"rating" : rating,   "comment": comment }
            comments.append(comment_data)

      else :
          print("ebay response : No reviews found!")

   except Exception as e:
      print("ebay response : Error in getting all comments : ", e)
         
   return comments if comments else []
                                
def scrape_data_with_selenium(links_list,prices,user_agents, collection):
   print("ebay response : the links to the 5 products : ",links_list)
   useragent = random.choice(user_agents)

   # Initialize Firefox service and options
   service = Service()
   service.path = GeckoDriverManager().install()
   firefox_options = webdriver.FirefoxOptions()
   firefox_options.headless = True  # Set to True if you don't want a visible browser
   #firefox_options.set_preference("general.useragent.override", random.choice(user_agents))
    


   for (link,price) in zip(links_list[:3],prices):
     time.sleep(5)
     for trying in  range(len(user_agents)): 
        try:
            print("ebay response : intering the product page...")
            
      
            #resetting the user-agent
            useragent = random.choice(user_agents)
            firefox_options.add_argument(f"user-agent={useragent}")
            browser = webdriver.Firefox(service=service, options=firefox_options)

            time.sleep(3)
            
            #getting the link 
            browser.get(link)
            if browser is not None: 
               print("ebay response : entered product page !")

            # gotta wait for specific elements to load
               
            # getting the title
            title_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.x-item-title__mainTitle')))
            if title_element : 
                    titlespan =  title_element.find_element(By.CSS_SELECTOR,('span')).text.strip()
                    try:
                        print("ebay response : got the title ! : ", titlespan)
                    except Exception as e :
                        print("ebay response : title span error ! ")

                    title = title_element.text.strip()

            #getting the imgs
            try: 
                imgs =[]
                
                img_div =  WebDriverWait(browser, 15).until(
               EC.presence_of_element_located((By.CSS_SELECTOR, '.ux-image-grid.no-scrollbar')))
                img_buttons = img_div.find_elements(By.CSS_SELECTOR, '.ux-image-grid-item.image-treatment.rounded-edges')
                for img_button in img_buttons :
                    img_element = img_button.find_element(By.TAG_NAME,'img')
                    print("ebay response : got the imgs element !") if img_element else print("ebay response : no img element")
                    imgs.append(img_element.get_attribute('src')) 
                    
                if imgs : 
                    print("ebay response : got the imgs srcs !",imgs) 
                else : 
                    print("ebay response : no  images found.")

            except Exception as e :
                print ("error at getting the imgs : " ,e)
            
            
            #getting the description :
            try : 
                soup = BeautifulSoup(browser.page_source,"html.parser")
                time.sleep(5)
                print("ebay response : waiting 5 seconds ...")
                # Find label and value elements
                label_elements = soup.find_all('div', class_='ux-labels-values__labels-content')
                value_elements = soup.find_all('div', class_='ux-labels-values__values-content')
                if len(label_elements) != 0:
                    print("ebay response : label element found")
                else : print("ebay response : didnt find the label element")

                # Extract label-value pairs
                label_value_pairs = []
                try:

                    for label, value in zip(label_elements[5:], value_elements[5:]):
                        label_text = label.get_text(strip=True)
                        value_text = value.get_text(strip=True)
                        label_value_pairs.append({'label': label_text, 'value': value_text})
    
                    if label_value_pairs:
                        print("ebay response : Here are the description pairs:", label_value_pairs)
                    else : 
                        print("ebay response : label_value_pairs not found !")
                
                except Exception as e:
                    print("ebay response : Error at getting the description table:", e)
            except Exception as e :
                print("ebay response : error at getting the description ! ")
               

            #Scraping the comments 
            #getting data from the comments section 
            try:


                # Initialize link_to_comment_page_element as None to enter the loop
                link_to_comment_page_element = None

                # Do-while loop to keep changing the value of link_to_comment_page_element( cuz in the page's html it keeps varying)
                while link_to_comment_page_element is None:
                    time.sleep(3)
                    
                    try:
                        # Try the first CSS selector
                        link_to_comment_page_element = WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.fdbk-detail-list__tabbed-btn.fake-btn.fake-btn--large.fake-btn--secondary')))
                    except:
                        try:
                            # Try the second CSS selector if the first one fails
                            link_to_comment_page_element = WebDriverWait(browser, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '.fdbk-detail-list__btn-container__btn.black-btn.fake-btn.fake-btn--large.fake-btn--secondary')))
                        except:
                            # If both CSS selectors fail, continue the loop to try again
                            print("ebay response : both ways failed , didn't get the link to comment page")
                            link_to_comment_page_element = None
                            break
                            



                # At this point, link_to_comment_page_element is not None
                print("ebay response : The comment page element:", link_to_comment_page_element)

                if link_to_comment_page_element is not None : 
                  print("ebay response : found the comment div ")
                  link_to_comment_page = link_to_comment_page_element.get_attribute('href')
                               
                  if link_to_comment_page is not None :
                     print("ebay response : got the comment page link ! :" )
                     print(link_to_comment_page)
                     browser.quit()
                  
                  else : 
                     print("ebay response : no comment page link !")
                     
                  #mn hna ltehht dkhlna lpage dlcomments____________________________________________
                  #Setting the retrying method 
                  for trying in range(len(user_agents)): 
                     
                     #getting the response before trynna run selenium
                     time.sleep(3)
                     useragent = random.choice(user_agents)
                    
                     firefox_options.add_argument(f"user-agent={useragent}")
                     browser = webdriver.Firefox(service=service, options=firefox_options)
                    
                     headers = {"User-Agent": useragent}
                     response = requests.get(link_to_comment_page, headers=headers, timeout=30)
                     
                     print("ebay response : response of the comments page : ",response)

                     # If the request is successful, continue with scraping
                     if response.status_code == 200:
                        print("ebay response : entering the comment page...")
                        
                        try :
                              try:
                                    un_separated_comments = []
                                    time.sleep(5)
                                    browser.get(link_to_comment_page)
                                    time.sleep(10)

                                    comment_page_response = BeautifulSoup(browser.page_source, 'html.parser')
                                    #print("ebay response : comment_page_response:", comment_page_response)
                                    
                                    
                                    un_separated_comments = get_comments(comment_page_response, browser)
                                    print("ebay response : un_separated_comments:", un_separated_comments)
                                    if un_separated_comments :
                                        print("ebay response : niice ... got the comments ")
                                        browser.quit()
                                        break

         
                                    if not un_separated_comments  :
                                       print ("no comment found ...retrying in 5seconds...")
                                       browser.quit()

                              except  Exception as e:
                                    print("ebay response : error at getting the comments :",e,"...retrying in 5seconds...")
                                    browser.quit()
                        except Exception as e:
                           print(f"Error scraping the comment page : {e}...retrying in 5seconds...")
                           browser.quit()
                else:
                     print("ebay response : didnt find the comment div, line 321 : ")
                     un_separated_comments=[]

            except Exception as e:
               print(f"Error scraping the comments {e}")
               browser.quit()
            
            
            '''#getting the contact infos link and store link
            try :
                contact_link = ' '
                store_link = ' '
                try :
                    contact_link_element = WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.d-stores-info-categories__container__action__contact.fake-btn.fake-btn--secondary')))
                    
                    store_link_element = WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.d-stores-info-categories__container__action__visit.fake-btn.fake-btn--primary')))
                    
                    if contact_link_element is not None:
                        contact_link = contact_link_element.get_attribute('href')
                        print('found the contact link ')
                    else :
                        print("ebay response :  couldn't find the contact link ! ")
                        contact_link = ''
                    
                    if store_link_element is not None :
                        store_link = store_link_element.get_attribute('href')
                        print('found the contact link ')
                    else : 
                        store_link =''
                        print('didnt get the store link')
                except Exception as e : 
                    print("ebay response : error at getting the store and contact links")

            except Exception as e:
                print('Could not extract contact and store links ',e)'''
                





            product_data = {"name"        : title,
                            "images"      : imgs,
                            "price"       : price,
                            "description" : label_value_pairs ,
                            # "contact"     : contact_link,
                            # "seller_store" : store_link,
                            "un_separated_comments": un_separated_comments,
                                                                    }
            
            collection.insert_one(product_data)
            print("ebay response : One document's insertion has finished , from ebay to db !")
            time.sleep(random.uniform(3, 15))
            browser.quit()
            break
        except Exception as e:
               print(f"Error scraping the comments {e}")
               browser.quit()
        time.sleep(5)
         

     browser.quit()

            


            
   # Close the WebDriver after scraping all product pages
   browser.quit()

#_______________________________________________MAIN_________________________________________________________________
import sys
def main(product_name):

    user_agents = [
    #"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.3"   ,
    #"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.3"   ,
    #"Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.",
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

    # Connect to MongoDB
    db = connect_to_database()

    # Create collection
    collection = create_collection(db)


    # Search for the product and scrape its data
    # product_name = input(f"Enter a search term: ")

    print(f"Searching for {product_name}...")
    links_list , prices_list = search_products( product_name , user_agents)
    if links_list:
        print(f"Scraping data for {product_name}...")
        scrape_data_with_selenium(links_list,prices_list, user_agents, collection)
    else:
        print(f"No search results found for {product_name}")

    print("ebay response : ebay Scraping finished. Check the database for the results.")


