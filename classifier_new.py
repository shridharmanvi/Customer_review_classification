from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
import math

backslash=re.compile(r'\\\w')
utfremove=re.compile(r'[^\x00-\x7F]+')
digitsremove=re.compile(r'[0-9]')
punctuation = ["-",",","/",".","'","?","$","@","!","(",")","[","]"]

stemmer = PorterStemmer()

f = open('training_data/training_set.csv','r')

stopwords=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your','yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her',
      'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
      'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was',
      'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
      'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at',
      'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before',
      'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
      'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
      'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
      'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
      'should', 'now']

raw_data={}

def read_data():
    #this function reads data from file and feeds raw_data: gives a unique id for each of the reviews
    i = 1
    for data in f:
        li = data.lower().strip().split('|')
        if len(li) == 2:
            #print li
            #raw_data[i] = li
            raw_data[i] = [li[0], 'high' if li[1] == '4' or li[1] == '5' else 'low']
            i+=1

    print 'Read data.. Total number of reviews: ' + str(len(raw_data.keys())) + '\n'


def split_test_training(nu,k):
    #n is the number of items in each split
    data = raw_data.keys()
    n=nu #Number of items in k
    chunks=[data[x:x+n] for x in xrange(0, len(data), n)]
    test_data =chunks[k]
    training = []
    for i in range(0,3):
        if(i != k):
            #print 'Here'
            #print i
            training.append(chunks[i])
        else:
            #print i
            ashk = 0
    print 'Training and test split complete! \n'
    return test_data, training


def build_dist(train):
    bag={}
    for chunk in train:
        for item in chunk:
            cl = raw_data[item][1].strip()
            text = raw_data[item][0].strip()
            try:
                bag[cl].append(text)
            except KeyError:
                bag[cl] = [text]
    return bag


def print_stats(dist):
    for key in dist.keys():
        print 'Total number of items in ' + str(key) + ' class is: ' + str(len(dist[key]))
        #print dist[key]
        #print '====================================='
        #print '/n'


def build_bag(dist):
    bag={}
    for item in dist.keys():
        b = dist[item]
        l = ' '.join(map(str,b))
        l = dataCleanse(l)#comment if not needed
        l = removeStopWords(l,stopwords)#comment if not needed
        l = stemming(l)#comment if not needed
        bag[item] = [l]
        #bag[item] = dist[item]
    print 'Bag of words is prepared for each class and stored in bag variable.'
    return bag


def build_counts(bag):
    #This function builds the counts for each of the words in every class
    probs = {}
    for cl in bag.keys():
        cnts={}
        sentance = bag[cl]
        for word in sentance[0].split(' '):
            try:
                cnts[word]= cnts[word] + 1
            except KeyError:
                cnts[word] = 1
        probs[cl] = cnts

    return probs


def calculate_class_probs(dist):
    class_probs={}
    total = 0
    for k in dist.keys():
        total+=len(dist[k])
    # got total number of reviews
    #next, calculate individual class probabilities (prior probabilities)
    print total
    for k in dist.keys():
        class_probs[k]=float(float(len(dist[k]))/float(total))
    print 'Class probabilities calculated... \n'
    return class_probs


def classifier(bag,counts,class_probabilities,test):
    all_prbs=[]
    for item in test:
        #For each test item
        clas = raw_data[item][1]
        item_probs=[]
        text_review= raw_data[item][0]
        text_review = dataCleanse(text_review) #define function for data cleansing
        text_review = removeStopWords(text_review, stopwords) #define function for stop words removal
        text_review = stemming(text_review) #define stemming function for a string
        for cl in bag.keys():
            word_prob=0.0
            for word in text_review.split(' '):
                prob=0.0
                try:
                    wrd_cnt_inClass= float(counts[cl][word])
                except KeyError:
                    wrd_cnt_inClass=0.0
                tot_words_inClass=float(len(bag[cl][0].split(' ')))
                tot_uniq_words_inClass = float(len(counts[cl].keys()))
                prob = float((wrd_cnt_inClass + 1.0)/(tot_words_inClass + tot_uniq_words_inClass))
                word_prob+=math.log(prob)
            item_probs.append({cl:word_prob})
            #print 'Total prob for class ' + str(cl) + ' is ' + str(word_prob) + ' and actual class is ' + str(clas)

        ####Calculated probabilites for the test item belonging to every class. Next part picks the largest probability value and declares the final class
        #print item_probs
        max_prob = - 9999999.0
        predicted_class=0
        for result in item_probs:
            r_class=result.keys()[0]
            r_prob=result[r_class]
            if(r_prob>max_prob):
                predicted_class=r_class
                max_prob = r_prob
        ap={item:predicted_class}
        #print ap
        all_prbs.append(ap)
        #print str(predicted_class) + ' === '  + str(max_prob)
    return all_prbs


def stemming(text):
    text = ' '.join(stemmer.stem(word) for word in [text][0].split(' '))
    return text


def dataCleanse(text):
    text=backslash.sub('',text)
    text=utfremove.sub(' ',text)
    text=''.join(ch for ch in text if ch not in punctuation)# remove punctuation
    text=digitsremove.sub('',text)
    return text


def removeStopWords(text,stopwords):
    text = ' '.join(word for word in [text][0].split(' ') if word not in stopwords)
    return text


def computeAccuracy(raw_data, predicted):
    pos=0
    total=0
    for item in predicted:
        total+=1
        item_id = item.keys()[0]
        predicted_class = item[item_id]
        if(predicted_class == raw_data[item_id][1]):
            #print predicted_class
            #print raw_data[item_id][1]
            pos+=1
        #else:
            #print predicted_class
            #print raw_data[item_id][1]
    print 'Number of test points classified correctly: ' + str(pos)
    print 'Total number of test points: ' +  str(total)
    return float(pos)/float(total)



if __name__ == "__main__":
    read_data()# reads data and assigns unique Ids to each review
    accuracies = []
    for i in range(0,3):
        print '========================================================================================'
        test, training = split_test_training(500,i) #splits data with each fold being 20 and returns training and test IDs
        dist = build_dist(training)
        print_stats(dist)
        print 'Data read and class segaregation complete! \n'
        bag = build_bag(dist)
        counts = build_counts(bag)
        class_probabilities = calculate_class_probs(dist)
        all_probs=classifier(bag, counts, class_probabilities, test)# Returns final predicted classes for all test points
        #print all_probs
        accuracies.append(computeAccuracy(raw_data, all_probs))
    print accuracies
