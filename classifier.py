from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

f = open('BCF_boys.csv','r')

stop=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your','yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her',
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
        #print str(li)
        raw_data[i] = li
        i+=1

    print 'Read data.. Total number of reviews: ' + str(len(raw_data.keys())) + '\n'


def split_test_training(nu):
    #n is the number of items in each split
    data = raw_data.keys()
    n=nu #Number of items in k
    chunks=[data[x:x+n] for x in xrange(0, len(data), n)]
    test_data =chunks[0]
    training_data=chunks[1:]
    print 'Training and test split complete! \n'
    return test_data, training_data


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
        #b.replace('"','')
        #b.replace("'",'')
        bag[item] = [''.join(map(str,b))]
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
        #text_review = dataCleanse(text_review) #define function for data cleansing
        #text_review = stemming(text_review) #define stemming function for a string
        #text_review = removeStopWords(text_review) #define function for stop words removal
        for cl in bag.keys():
            #text_review= raw_data[item][0]
            #text_review = dataCleanse(text_review) #define function for data cleansing
            #text_review = stemming(text_review) #define stemming function for a string
            #text_review = removeStopWords(text_review) #define function for stop words removal
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
                word_prob+=prob
            item_probs.append({cl:word_prob})
            #print 'Total prob for class ' + str(cl) + ' is ' + str(word_prob) + ' and actual class is ' + str(clas)
        print item_probs

        ####Calculated probabilites for the test item belonging to every class. Next part picks the largest probability value and declares the final class

        max_prob = 0.0
        predicted_class=0
        for result in item_probs:
            r_class=result.keys()[0]
            r_prob=result[r_class]
            if(r_prob>max_prob):
                predicted_class=r_class
                max_prob = r_prob
        print str(predicted_class) + ' === '  + str(max_prob)



if __name__ == "__main__":
    read_data()# reads data and assigns unique Ids to each review
    test, training = split_test_training(20) #splits data with each fold being 20 and returns training and test IDs
    dist = build_dist(training)
    print_stats(dist)
    print 'Data read and class segaregation complete! \n'
    bag = build_bag(dist)
    counts = build_counts(bag)
    #print len(bag['2'][0].split(' '))
    class_probabilities = calculate_class_probs(dist)
    classifier(bag,counts,class_probabilities,test)

