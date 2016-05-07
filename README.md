# Customer_review_classification

### Github repository link:
* https://github.com/shridharmanvi/Customer_review_classification
* Experementation results have been included as part of the presentation 

### Data collection - Crawling target site

* The training data for classifier model is scrapped off the target web page: http://www.burlingtoncoatfactory.com/burlingtoncoatfactory/Default.aspx
* The script visits each of the sub category pages like Women, Men, Shoes, Handbags etc. and obtains all the urls of the products.
* The urls are then visited programatically in an asynchronous fashion to scrape the data received from the servers. This async behavior of the script enables us to get all the data in minutes as compared to several hours or even days if done synchronously
* Data from all the categories is combined and fed to the model as training data for classification

### Naive Bayes Classifier

* The classifier is built using Naive Bayes Text Classification algorithm. We have used the source from Stanford university class extensively in implementing the algorithm 
* The script reads the pipe delimited data produced by the web crawler and splits into training and test data.  
* Perform data pre processing on each of the records and assign unique ID (IDs will help later for validation)
* Split training and test data for cross validation
* Build bag of words
* Calculate word counts of every word in each class
* Class Prior probabilities P(C) for each class
* For every test record, calculate argmax of conditional probabilities of that record belonging to each class
* Calculate accuracy based on number of test records classified correctly
* Perform cross validation: Repeat steps 2 through 7 for 3 times
* Declare final classification accuracy

### Code execution
```
# First install all the dependencies and run the web crawler. Once the data is scraped and downloaded, run the classifier
python webcrawler.py

# After generating all the csv files for each category. Combine them using the following command
cat *.csv > training_set.csv

# Run the classifier
python naiveBayesClassifier.py

```

###References:

* https://web.stanford.edu/class/cs124/lec/naivebayes.pdf
* https://github.com/kennethreitz/grequests
* https://christopher.su/2015/selenium-chromedriver-ubuntu/

