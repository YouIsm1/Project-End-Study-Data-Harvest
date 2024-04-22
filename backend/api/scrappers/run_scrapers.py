import pymongo
import logging
import threading
import subprocess
from . import alibaba_pyscraper, amazone_pyscraper, ebay_pyscraper

def run():
    client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
    db = client["products_database"]  # Replace with your database name
    collection = db["UserEffect"]  # Replace with your collection name
    product_doc = collection.find_one({})  # Retrieve a single document (assuming a single product name)
    product_name = product_doc["namePoduct"]  # type: ignore # Access the product_name field

    # Create threads for each script
    thread1 = threading.Thread(target=alibaba_pyscraper.main, args=(product_name,))
    thread2 = threading.Thread(target=amazone_pyscraper.main, args=(product_name,))
    thread3 = threading.Thread(target=ebay_pyscraper.main, args=(product_name,))

    # Start all threads
    thread1.start()
    thread2.start()
    thread3.start()

    # Wait for all threads to finish
    thread1.join()
    thread2.join()
    thread3.join()