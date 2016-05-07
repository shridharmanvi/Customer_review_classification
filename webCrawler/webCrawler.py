__author__ = 'Shridhar.Manvi'

# BURLINGTON COAT FACTORY WEB CRAWLER

from selenium import webdriver
import time
import datetime
from lxml import html
import requests
from pyvirtualdisplay import Display
from subprocess import call
import grequests
from grequests import imap
import urllib2 as u
import requests

'''
Start the display driver
'''

display = Display(visible=0, size=(800, 600))
display.start()

# starturls is a list of root urls from which traversal is carried out to other branches
# base_url is the base skeleton which will be used further in appending the tail to get the complete url of a product

data = open('/home/smanvi/bcf/output/BCF_toys.csv', 'w')
#data1 = open('./urls/BCF_shoes_urls.txt', 'w')
base_url = "http://www.burlingtoncoatfactory.com/burlingtoncoatfactory/"

#header = "Product ID" + '|' + "Product Name" + '|' + "Price" + '|' + "Deep link" + '|' + "Picture url" + '|' + "Description" + '\n'
#data.writelines(header)

#start_urls = ["http://www.burlingtoncoatfactory.com/burlingtoncoatfactory/Coats-58378.aspx?h="]#,"http://www.burlingtoncoatfactory.com/burlingtoncoatfactory/Shoes-65023.aspx?h="]

start_urls = ["http://www.burlingtoncoatfactory.com/burlingtoncoatfactory/Toys-Books-61196.aspx?h="]

def async_product_parse(response_obj_list):
    #The following loop parses product information from response objects list :http status 200
    for item in response_obj_list:
        try:
	    item_page = item
            item_tree = html.fromstring(item_page.text)
	    item_name = item_tree.xpath('//*[@class= "product-details-title"]/text()')
	    rating=item_tree.xpath('//*[@class="bv-content-rating bv-rating-ratio"]//meta/@content')
    	    views=item_tree.xpath('//*[@class="bv-content-summary-body-text"]//p/text()')
    	    ratings=rating[0::2]
    	    print ratings
    	    print views
	    print item_name
    	    if len(ratings) > 0:
	    	for i in range(0,len(ratings)):
			print str(views[i]) + ',' + str(ratings[i]) + '\n'
	    
            data.writelines(write)
            item.close()
        except Exception:
            continue


def individual_get(url_list):
    for item in url_list:
        try:
	    #item = requests.get(item)
	    item_page = requests.get(item)
            item_tree = html.fromstring(item_page.text)
            rating=item_tree.xpath('//*[@class="bv-content-rating bv-rating-ratio"]//meta/@content')
            views=item_tree.xpath('//*[@class="bv-content-summary-body-text"]//p/text()')
            ratings=rating[0::2]
            #print ratings
            #print views
            if len(ratings) > 0:
                for i in range(0,len(ratings)):
                        print str(views[i]) + ',' + str(ratings[i]) + '\n'
            
	    data.writelines(write)
            item.close()
        except Exception:
            continue


if __name__ == '__main__':

    driver = webdriver.Firefox()  # Create a firefox driver
    print str(datetime.datetime.utcnow()) + '  ----  ' + 'Starting web crawler...'

    for url in start_urls:  # for each url category - Ex. Women, Men, Boys etc..
        # For each category
        driver.get(url)  # Access the web page
        selenium_page = driver.page_source.encode('utf-8')
        tree = html.fromstring(selenium_page)
        # Next, fetch all <a> links to subcategory pages
        urls = tree.xpath('//div[@class="productContainer"]/div[@class="subcategoryTitle"]/a/@href')  #subcategory links
        for inner_url in urls:
            # For each sub-category
            # The subcategory urls are partial. Hence, append it to base url
            if base_url in inner_url:
	    	x = inner_url + '#sort=rating'
	    else:
		x = base_url + inner_url + '#sort=rating' 
            driver.get(x)
            current_page = driver.page_source.encode('utf-8')
            current_tree = html.fromstring(current_page)
            span = current_tree.xpath('//*[@class = "inactive-page-number"]/text()')  # Get the number of pages
            span = map(int, span)  # Convert the list of strings to int
            try:
                n = max(span)  # pick the maximum number - Gives the last page and loop for scroll down these many times
            except ValueError:
                n = 80
            i = 0
            for i in range(0, int(n)):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll down
                time.sleep(2)  # pause for 2 seconds
                i += 1

            print str(datetime.datetime.utcnow()) + '  ----  ' + 'Loaded page: ' + str(x)
            current_page = driver.page_source.encode('utf-8')  # Replaces current page pointer to fully loaded page
            current_tree = html.fromstring(current_page)
            item_links = current_tree.xpath('//*[@class="product-title clearfix"]/@href')
            main_items = []  # Hold list for rectified urls

            # Correcting and verifying urls in the below loop - feeds the above hold list
            for link in item_links:
                link = base_url + link
                link = link.replace('http:/', 'http://')
                link = link.replace('/../../', '/')
                link = link.replace('//', '/')
                link = link.replace('/../', '/')
                link = link.replace('/burlingtoncoatfactory/burlingtoncoatfactory', '/burlingtoncoatfactory')
		link = link.rstrip('\n')
                #print link
		main_items.append(link)
                w = str(link) + '\n'
                #data1.writelines(w)
            #print main_items
	    print 'Number of items: ' + str(len(main_items))
            print 'Starting item fetch and crawl'
	    
	    for sub_i in main_items:
		driver.get(sub_i)  # Access the web page
    		selenium_page = driver.page_source.encode('utf-8')
    		tree = html.fromstring(selenium_page)
    		rating=tree.xpath('//*[@class="bv-content-rating bv-rating-ratio"]//meta/@content')
    		views=tree.xpath('//*[@class="bv-content-summary-body-text"]//p/text()')
    		ratings=rating[0::2]
    		print ratings
    		print views
    		if len(ratings) > 0:
		     for i in range(0,len(ratings)):
		         data.write(str(views[i]) + '|' + str(ratings[i]) + '\n')
		else:
		     break	

    driver.close()
    driver.quit()
    display.stop()



