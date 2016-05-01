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
        print raw_data[i]
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
            #print word
            try:
                cnts[word]= cnts[word] + 1
            except KeyError:
                cnts[word] = 1
        probs[cl] = cnts

    return probs


if __name__ == "__main__":
    read_data()# reads data and assigns unique Ids to each review
    test, training = split_test_training(20) #splits data with each fold being 20 and returns training and test IDs
    dist = build_dist(training)
    print_stats(dist)
    print 'Data read and class segaregation complete! \n'
    bag = build_bag(dist)
    counts = build_counts(bag)
    print counts
    """
    for clas in counts:
        print clas
        print counts[clas]
        print '/n'
    """
