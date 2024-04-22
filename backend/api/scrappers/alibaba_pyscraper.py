
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
from selenium.common.exceptions import TimeoutException


# Connecting to the MongoDB database
def connect_to_database():
    client = MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB connection string
    database = client["products_database"]  # Replace with your database name
    print("aliexpress response : Connected to MongoDB")
    return database

# Creating the collection in MongoDB
def create_collection(database):
    # Check if the collection exists
    if "alibaba_product_collection" in database.list_collection_names():
        # If it exists, drop it
        database["alibaba_product_collection"].drop()
        print("aliexpress response : Existing collection dropped successfully")

    # Create a new collection
    collection = database["alibaba_product_collection"]
    print("aliexpress response : Collection created successfully")
    return collection


# Search for a product and get its URL
def search_products(product_name,user_agents):

    base_search_url = "https://www.aliexpress.com/wholesale?SearchText="
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
    product_elements = html_content.find_all("a",{'class' : "multi--container--1UZxxHY cards--card--3PJxwBm search-card-item" })
    
    links_list = [] # Initialize an empty list to store the product links
    prices_list=[]

    if product_elements:
        print("aliexpress response : got the product elements ! nice !")

        for product in product_elements[:1] :
        
        # Extract all product links and return them in a list
            #link_element = product.find("a",{'class' : "s-item__link"})
            link_href = 'https:' + product.get('href')
           
            if link_href:
              
              links_list.append(link_href)
           
            else : 
               print("aliexpress response : the code couldn't get the href elements")
               links_list.append('no link found')

        #getting the price
            price_element = product.find("div",{'class' : "multi--price-sale--U-S0jtj"})
            if price_element is not None:
                price = price_element.get_text(strip=True)
                prices_list.append(price)  
            

        if prices_list :
            print("aliexpress response : the prices we got  : ",prices_list)

        else :
            print("aliexpress response : we got no prices !")



        if links_list:
           print("aliexpress response : double nice! Found the products links ") 
            # Add a delay of 5 seconds between each request
           
        else : 
            print("aliexpress response : link_list variable is equal to none :/ ") 
            return None          


    
    else:
        print("aliexpress response : didn't find product links :( error of search product function ")
        return None 
    return (links_list , prices_list)


def get_possible_comments(browser,commentpagediv):
    comments =[]
    product_rating =' '
    try:
        
        print("aliexpress response : waiting 5 seconds for the comment elements...")
        time.sleep(5)
        
        #getting the rating
        rating_div = commentpagediv.find_element(By.CSS_SELECTOR, '.ae-header-content-num')
        if rating_div :
            product_rating = rating_div.text.strip() 
        
        
        commentpagediv = commentpagediv.find_element(By.CSS_SELECTOR,'.ae-evaluateList-box')
        
        actual_review_divs = commentpagediv.find_elements(By.CSS_SELECTOR, '.ae-evaluateList-card')
        if actual_review_divs is not None:
            for div in actual_review_divs:
                #getting the comment
                try:
                    text_div =div.find_element(By.CSS_SELECTOR,'.ae-evaluateList-card-content')
                    comment = text_div.text.strip() 
                    if comment:    
                        print("aliexpress response : got the actual comment : ", comment)
                    else :
                        print("aliexpress response : problem finding the span element of the comment !")
                except:
                    comment = ' '

                try:
                    #getting the comments imgs[source]
                    imgs_div_element = div.find_element(By.CSS_SELECTOR,".ae-evaluateList-card-img-box")
                    if  imgs_div_element : 
                        img_imgs = imgs_div_element.find_elements(By.TAG_NAME,'img')
                        imgs = [img.get_attribute('src') for img in img_imgs]
                        if imgs :
                            print("aliexpress response : got the comments imgs")
                    else:
                        print("aliexpress response : no imgs found")
                        imgs=[]
                        pass
                except Exception as e :
                    print(e)
                
                comment_data ={"imgs" : imgs,   "comment": comment }
                comments.append(comment_data)

        else :
            print('couldnt find any review divs ')
            comment = ' '
        
        

        if (comments , product_rating) is not None  :
            print("aliexpress response : got the comments data + the price")
            
        else : 
            print('error at getting either the rating/comments/imgs')
        
        return comments , product_rating
    except Exception as e:
        print('no comment found ! maybe there is an error  or this page has no more comments ',e)
        return comments , product_rating


def get_comments(browser):
   comments =[]
   product_rating =' '
   try:
      print("aliexpress response : waiting 5 seconds for the comment elements...")
      time.sleep(5)
      

      comment_page_div = WebDriverWait(browser, 15).until(
               EC.presence_of_element_located((By.CSS_SELECTOR, '.ae-all-list-content')))
      
      #getting the rating
      rating_div = comment_page_div.find_element(By.CSS_SELECTOR, '.ae-header-content-num')
      if rating_div :
        product_rating = rating_div.text.strip() 
      else : 
        print("aliexpress response : no rating found")
        product_rating = ' '

      comment_page_div = comment_page_div.find_element(By.CSS_SELECTOR,'.ae-evaluateList-box')
      
      actual_review_divs = comment_page_div.find_elements(By.TAG_NAME,"div")
      
      if actual_review_divs is not None:
        print("aliexpress response : got the divs!")
        for div in actual_review_divs[:10] :
            
            if div  :

                #getting the comment
                try:
                    actual_review_div = div.find_element(By.CSS_SELECTOR,'.ae-evaluateList-card-content')
                    comment = actual_review_div.text.strip() 
                    if comment:    
                        print("aliexpress response : got the actual comment : ", comment)
                    else :
                        print("aliexpress response : empty comment !")
                except Exception as e:
                  print("aliexpress response : failed scraping the comment text .")
                  comment = ' '
                
                           
                #getting the imgs
                try:
                    imgs_div_element = div.find_element(By.CSS_SELECTOR,".ae-evaluateList-card-img-box")

                    if  imgs_div_element : 
                        img_imgs = imgs_div_element.find_elements(By.TAG_NAME,'img')
                        imgs = [img.get_attribute('src') for img in img_imgs]
                    else:
                        print("aliexpress response : no imgs found")
                        imgs=[]
                

                except Exception as e:
                  print("aliexpress response : failed scraping the comment imgs .")
                  imgs =[]
                
                if  len(comment)>2 or len(imgs)>0:
                    comment_data ={"imgs" : imgs,   "comment": comment }
                    comments.append(comment_data)

                
            else:
                print('no actualreviewdiv element found')
                imgs = []
                comment =' '
        
            

      else :
          print("aliexpress response : No reviews found!")

   except Exception as e:
      print("aliexpress response : Error in getting all comments : ", e)
         
   return  comments , product_rating 


def remove_empty_comments_and_images_field(db):
    # Access the collection
    collection = db['alibaba_product_collection']

    # Query to find products with empty comments and images
    query = {"un_separated_comments": [{"imgs": [], "comment": " "}]}

    # Update operation to unset the comments and images fields
    update = {"$pull": {"un_separated_comments": {"imgs": [], "comment": " "}}}

    # Update the products
    collection.update_many(query, update)
                                                   

def scrape_data_with_selenium(links_list,prices,user_agents, collection):
   print("aliexpress response : the links to the 5 products : ",links_list)
   useragent = random.choice(user_agents)

   # Initialize Firefox service and options
   service = Service()
   service.path = GeckoDriverManager().install()
   firefox_options = webdriver.FirefoxOptions()
   firefox_options.headless = True  # Set to True if you don't want a visible browser
   #firefox_options.set_preference("general.useragent.override", random.choice(user_agents))
    


   for (link,price) in zip(links_list,prices):
     time.sleep(5)
     for trying in  range(len(user_agents)): 
         useragent = random.choice(user_agents)
         headers = {"User-Agent": useragent,}
            # Send a HEAD request with the user-agent to the link
         response = requests.head(link, headers=headers, timeout=10)
         
         print("aliexpress response : response of the product page :",response)

            # If the request is successful, continue with scraping
         if response.status_code == 200:
            print("aliexpress response : intering the product page...")
            
      
            #resetting the user-agent
            useragent = random.choice(user_agents)
            firefox_options.add_argument(f"user-agent={useragent}")
            browser = webdriver.Firefox(service=service, options=firefox_options)

            time.sleep(3)
            
            #getting the link 
            browser.get(link)
            if browser is not None: 
               print("aliexpress response : entered product page !")

               
            # getting the title
            title_element_temp = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'title--wrap--Ms9Zv4A')))
            title_element =title_element_temp.find_element(By.TAG_NAME,'h1')
            if title_element : 
                    titlespan =  title_element.text.strip()
                    try:
                        print("aliexpress response : got the title ! : ", titlespan)
                    except Exception as e :
                        print("aliexpress response : title span error ! ")

                    title = titlespan
            else:
                print("aliexpress response : title_element not found")

            #getting the imgs
            try:
                img_div =  WebDriverWait(browser, 15).until(
               EC.presence_of_element_located((By.CSS_SELECTOR, '.slider--box--TJYmEtw')))
                img_imgs = img_div.find_elements(By.TAG_NAME, 'img')
                print("aliexpress response : got the imgs elements !") if img_imgs else print("aliexpress response : no imgs elements")
                
                imgs = [img.get_attribute('src') for img in img_imgs]
                
                if imgs : 
                    print("aliexpress response : got the imgs srcs !",imgs) 
                else : 
                    print("aliexpress response : no  images found.")
            except Exception as e :
                print ("error at getting the imgs : " ,e)
            
            
            #getting the description :
            try : 
                #soup = BeautifulSoup(browser.page_source,"html.parser")
                #time.sleep(5)
                #print("aliexpress response : waiting 5 seconds ...")
                # Find label and value elements
                nav_spesification = WebDriverWait(browser, 15).until(
               EC.presence_of_element_located((By.ID, 'nav-specification')))
                
                showmore_button = nav_spesification.find_element(By.TAG_NAME,'button')
                if  showmore_button.is_displayed():
                    browser.execute_script("arguments[0].click();", showmore_button)
                    print("aliexpress response : getting the showmore button clicked ...")
                else :
                    print("aliexpress response : no show more button found !")
                time.sleep(3)
                
                label_elements = nav_spesification.find_elements(By.CLASS_NAME,'specification--title--UbVeyic')
                value_elements = nav_spesification.find_elements(By.CLASS_NAME,'specification--desc--Mz148Bl')

                
                if len(label_elements) != 0:
                    print("aliexpress response : label element found")
                else : print("aliexpress response : didnt find the label element")

                # Extract label-value pairs
                label_value_pairs = []
                try:

                    for label, value in zip(label_elements[5:], value_elements[5:]):
                        label_text = label.text.strip()
                        value_text = value.text.strip()
                        label_value_pairs.append({'label': label_text, 'value': value_text})
    
                    if label_value_pairs:
                        print("aliexpress response : Here are the description pairs:", label_value_pairs)
                    else : 
                        print("aliexpress response : label_value_pairs not found !")
                
                except Exception as e:
                    print("aliexpress response : Error at getting the description table:", e)
            except Exception as e :
                print("aliexpress response : error at getting the description ! :",e)
               

            #Scraping the comments 
            #getting data from the comments section 
            try:
                

                #creating a while loop that keeps scrolling until it finds the element ...
                scroll_y = 0
                continue_scrolling = True  # Add a flag for scrolling

                while (continue_scrolling):
                    # Scroll down
                    scroll_y = scroll_y + 600
                    browser.execute_script(f"window.scrollTo(0, {scroll_y});")
                    time.sleep(2)  # pause to allow loading of new content
                    try :
                        commentpagediv = WebDriverWait(browser, 2).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "div#nav-review"))
                        )
                        if commentpagediv : 
                            print("aliexpress response : found the div hehehe")
                            continue_scrolling = False  # Stop further scrolling
                            break
                    except TimeoutException:
                        pass

                    
                time.sleep(2)
                
                if commentpagediv : print("aliexpress response : got the comment's button div")
                try:
                        #Case handling : scraping method IF THE SHOW MORA BUTTON IS CLICKED:::
                        
                        comments_showmore_button = commentpagediv.find_element(By.CSS_SELECTOR,'.comet-v2-btn.comet-v2-btn-slim.comet-v2-btn-large.comet-v2-btn-important')
                
                        #clicking the showmorebutton
                        if comments_showmore_button:
                            print("aliexpress response : got the button")
                            if  comments_showmore_button.is_displayed() :
                                browser.execute_script("arguments[0].click();", comments_showmore_button)
                                print("aliexpress response : comments showmore button clicked ...")


                                for trying in range(len(user_agents)): 
                                    un_separated_comments =[]
                                    time.sleep(3)
                                    useragent = random.choice(user_agents)
                                    #firefox_options.add_argument(f"user-agent={useragent}")
                                    #browser = webdriver.Firefox(service=service, options=firefox_options)
                    
                                    try :
                                        un_separated_comments,rating = get_comments(browser)
                                    
                                        if un_separated_comments :
                                            print("aliexpress response : niice ... got the comments ")
                                            print(un_separated_comments)
                                            break
                                            
                                        else :
                                            print ("no comment found")
                                            
                                    except Exception as e:
                                        print(f"Error scraping the comment page : {e}...retrying in 5seconds...")
                                
                            else :
                                print("aliexpress response : no show more button found !")
                        else:
                            print("aliexpress response : didnt get the button")

                except Exception as e   :
                     #Case handling : scraping method IF THE SHOW MORA BUTTON WAS NOT CLICKED:::
                    print("aliexpress response : Couldn't click on the show more button ", e,"gonna try to get the possible/displayed comments...")
                    un_separated_comments , rating = get_possible_comments(browser,commentpagediv)

                    if un_separated_comments :
                        print("aliexpress response : niice ... got the comments ")
                        print(un_separated_comments)
                        browser.quit() 
                    else :
                        print ("no comment found")
                        browser.quit()

                    if rating :
                        print("aliexpress response : niice ... got the rating ")
                        print(rating)
                        browser.quit() 
                    else :
                        print ("no rating found")
                        browser.quit()

                    
            except Exception as e:
               print(f"Error scraping comments {e}")
               un_separated_comments = []
               rating = ' '
               browser.quit()
            
            
            '''   #getting the contact infos link and store link
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
                        print("aliexpress response :  couldn't find the contact link ! ")
                        contact_link = ''
                    
                    if store_link_element is not None :
                        store_link = store_link_element.get_attribute('href')
                        print('found the contact link ')
                    else : 
                        store_link =''
                        print('didnt get the store link')
                except Exception as e : 
                    print("aliexpress response : error at getting the store and contact links")

            except Exception as e:
                print('Could not extract contact and store links ',e)
                
            '''




            product_data = {"name"        : title,
                            "images"      : imgs,
                            "price"       : price,
                            "rating"      : rating,
                            "description" : label_value_pairs ,
                            #"contact"     : contact_link,
                            #"seller_store" : store_link,
                            "un_separated_comments": un_separated_comments,
                                                                    }
            
            collection.insert_one(product_data)
            print("aliexpress response : One document's insertion is complete from aliexpress to db !")
            time.sleep(random.uniform(3, 15))
            browser.quit()
            break
         time.sleep(5)
         

     browser.quit()

            


            
   # Close the WebDriver after scraping all product pages
   browser.quit()


# Usage
import sys
def main(product_name):
    print("aliexpress response : strating the aliexpress scraping script")



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
        
    # Search for each product and scrape its data
    print(f"Searching for {product_name}...")
    
    links_list , prices_list = search_products(product_name, user_agents)
    if links_list:
        print(f"Scraping data for {product_name}...")
        scrape_data_with_selenium(links_list,prices_list, user_agents, collection)
        remove_empty_comments_and_images_field(db)
    else:
        print(f"No search results found for {product_name}")