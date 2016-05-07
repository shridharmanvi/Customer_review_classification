# Customer_review_classification

### Data collection - Crawling target site

* The training data for classifier model is scrapped off the target web page: http://www.burlingtoncoatfactory.com/burlingtoncoatfactory/Default.aspx
* The script visits each of the sub category pages like Women, Men, Shoes, Handbags etc. and obtains all the urls of the products.
* The urls are then visited programatically in an asynchronous fashion to scrape te data received from the servers. This async behavior of the script enables us to get all the data in minutes as compared to several hours or even days if done synchronously
* Data from all the categories is combined and fed to the model as training data for classification
