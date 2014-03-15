__author__ = 'rems'
__author__ = 'yashaswinis'


import re
import random
import math
from collections import Counter

#used to add <s> in the beginning of the file
first = True
def preprocessing(str):

  #Remove XML tags
 remove_tag = re.compile(r'<.*?>')
 str = remove_tag.sub('',str)

 #Remove the header in hotel review
 remove_tag1 = re.compile(r'IsTruthFul,IsPositive,review')
 str = remove_tag1.sub('',str)

 #Remove number,number, pattern in hotel review
 digit_comma = re.compile(r'(\d+,\d+,)', re.UNICODE)
 str = digit_comma.sub('',str)

 #Replace single newline by space and strip multiple newlines
 newline = re.compile(r'(\n)', re.UNICODE)
 str = newline.sub(' ',str)

 newline2 = re.compile(r'(\n)+', re.UNICODE)
 str = newline2.sub('',str)

 #Consider . ? ! as end of sentences so we can add the sentence markers <s> and </s>
 #verse numbers can be in the middle, so consider them for sentence segmentation
 #Remove number:number (verse numbers) in bible corpus
 dot = re.compile(r"(\.)", re.UNICODE)
 question = re.compile(r'\?', re.UNICODE)
 exclaim = re.compile(r'\!', re.UNICODE)
 digit_rem = re.compile(r'(\d+:\d+)', re.UNICODE)

 global first
 if first:
     str = "<s>" + str
     first = False
 str = dot.sub(' . </s> <s> ',str)
 str = question.sub(' ? </s> <s> ',str)
 str = exclaim.sub(' ! </s> <s> ',str)
 str = digit_rem.sub('',str)

 #Strip extra spaces
 space = re.compile(r'(\s)+',re.UNICODE)
 str = space.sub(' ',str)

 return (str)


#For printing various dictionaries
def print_hash(hash):
    for item in hash:
      print(item,hash[item])

#Unigram generation
# Input:preprocessed file name
# Output: unigram probability, unigram frequency dictionary
def unigram(filename):

            fproc = open(filename, 'r').read()
            token = fproc.split()

            unigram_hash = dict(Counter(token).items())
            unigram_prob= dict(unigram_hash)

            unigram_count = sum(unigram_hash.values())
            for value in unigram_hash.keys():
                temp = float(unigram_hash.get(value))/float(unigram_count)
                unigram_prob[value] = temp

            return(unigram_prob,unigram_hash)

#Bigram generation
# Input: Preprocessed file name, unigram frequency
# Output: bigram probability, bigram frequency dictionary
def bigram(filename,unigram_hash):

            newlist = [] #to append the generated bigrams
            fproc = open(filename, 'r').read()
            token = fproc.split()
            i=0
            bigramlist = token

            while i<len(bigramlist):
                if i+1<(len(bigramlist) -1):
                   newlist.append(bigramlist[i]+" " + bigramlist[i+1])
                i += 1

            bigram_hash = dict(Counter(newlist).items())
            bigram_prob = dict(bigram_hash)

            for w in newlist[:]:
              first=w.split(" ")
              bigramfrequency= bigram_hash.get(w)
              unifrequency=unigram_hash.get(first[0])
              temp= float(bigramfrequency)/float(unifrequency)
              bigram_prob[w]= temp

            return(bigram_prob,bigram_hash)

# Trigram generation
# Input: Preprocessed file name, bigram frequency
# Output: trigram probability, trigram frequency dictionary
def trigram(filename, bigram_hash):

            newlist1 = [] #to append the generated trigrams
            fproc = open(filename, 'r').read()
            token = fproc.split()
            j=0
            trigramlist = token

            while j<len(trigramlist):
                if (j+2)<(len(trigramlist) -1):
                   newlist1.append(trigramlist[j]+" " + trigramlist[j+1]+" "+trigramlist[j+2])
                j += 1

            trigram_hash = dict(Counter(newlist1).items())
            trigram_prob = dict(trigram_hash)

            for w in newlist1[:]:
                first1=w.split(" ")
                trigramfrequency1= trigram_hash.get(w)
                seq=[first1[0], first1[1]]
                bigram_split=" ".join(seq)
                bigramfrequency1=bigram_hash.get(bigram_split)
                temp= float(trigramfrequency1)/float(bigramfrequency1)
                trigram_prob[w]= temp

            return(trigram_prob,trigram_hash)

# Random Sentence
# Input: Bigram/Trigram frequency dictionary, ngram - 2 for bigram and 3 for trigram
# Output: Prints the random sentences
def random_sentence(prob_hash, ngram):

            sentence_len = 0
            random_sentence = ''
            maxlen = 30

            if ngram==2:
                while (sentence_len < maxlen):
                        random_p = random.uniform(0,1)

                        for key,value in prob_hash.items():
                           if sentence_len==0:
                             if((value == random_p and key.split()[0] == '<s>') or (value < random_p + 0.1 and value > random_p - 0.1 and key.split()[0] == '<s>')):
                                 random_sentence += key.split()[1] + ' '
                                 prev = key.split()[1]
                                 sentence_len += 1
                           elif sentence_len == maxlen -1:
                                  if((value == random_p and key.split()[1] == '</s>') or (value < random_p + 0.1 and value > random_p - 0.1 and key.split()[1] == '</s>')):
                                     random_sentence += key.split()[0]
                                     sentence_len += 1
                           else:
                                if((value == random_p and key.split()[0] == prev) or (value < random_p + 0.1 and value > random_p - 0.1 and key.split()[0] == prev)):
                                  random_sentence +=  key.split()[1] + ' '
                                  prev = key.split()[1]
                                  sentence_len += 1
            elif ngram==3:
                while (sentence_len < maxlen):
                        random_p = random.uniform(0,1)

                        for key,value in prob_hash.items():
                           if sentence_len==0:
                             if((value == random_p and key.split()[0] == '<s>') or (value < random_p + 0.1 and value > random_p - 0.1 and key.split()[0] == '<s>')):
                                 random_sentence += key.split()[1]+' '+key.split()[2] + ' '
                                 prev1= key.split()[1]
                                 prev2 = key.split()[2]
                                 sentence_len += 2
                                 break
                           elif sentence_len >= maxlen -2:
                                  if((value == random_p and key.split()[2] == '</s>') or (value < random_p + 0.1 and value > random_p - 0.1 and key.split()[2] == '</s>')):
                                     random_sentence += key.split()[0]+' '+key.split()[1]
                                     sentence_len += 2
                                     break
                           else:
                                if((value == random_p and key.split()[0] == prev1 and key.split()[1]==prev2) or (value < random_p + 0.1 and value > random_p - 0.1 and key.split()[0] == prev1 and key.split()[1]==prev2)):
                                  random_sentence +=  key.split()[2] + ' '
                                  prev1 = key.split()[1]
                                  prev2= key.split()[2]
                                  sentence_len += 1
                                  break

            random_sentence = re.sub(' </s> <s>', "", random_sentence)
            random_sentence = re.sub('</s>', "", random_sentence)
            random_sentence = re.sub('<s>', "", random_sentence)
            print(random_sentence)

#Check if the count is present in the hash_count dictionary(which has
# been precalculated to hold the Nc values.
def countN(hash,count):
    if count in hash:
       return hash[count]
    else:
        return 0

#Implement the good turning smoothing.
#Input: The unigram/bigram/trigram dictionary
#Output: The smoothed probabilities
def good_turing_smoothing(fd):
    gt_temp = dict()
    count_hash = dict()
    fd['<UNK>'] = 0 #Include an entry in the hash to handle unknowns

    count_hash = dict(Counter(fd.values()).most_common())
    N = sum(fd.values()) + 1

    for sample in fd:
       count = fd[sample]
       if count < 1:
            gt_temp[sample] = float (countN(count_hash,1)) / float(N)

       if count> 1 and count < 5:
            nc = countN(count_hash,count)
            ncn = countN(count_hash,count + 1)

            if nc ==0 or ncn == 0:
                gt_temp[sample] = float(fd[sample])/float(N)
            else:
                gt_temp[sample] = float(count + 1) * float(float(ncn) / float(nc * N))

    return gt_temp

#Calculate the perplexity
#Input: Unigram/bigram/trigram frequency table, ngram -1(unigram) 2(bigram) 3(trigram)
# and the preprocessed file name
#Output: Perplexity value

def perplexity(prob_hash, n_gram,filename):

 fproc = open(filename, 'r').read()
 token = fproc.split()
 M = len(token)

 newlist_per = [] #for bi/trigram model

 p =0
 i=0
 j=0

 if n_gram == 1:
          for word in token:
            if word in prob_hash:
                p+= math.log(prob_hash[word],2)
            else:
                p+= math.log(prob_hash["<UNK>"],2)

 elif n_gram == 2:
           while i<len(token):
              if i+1<(len(token) -1):
                newlist_per.append(token[i]+" " + token[i+1])
              i += 1

           for word in newlist_per:
            if word in prob_hash:
                p+= math.log(prob_hash[word],2)
            else:
                p+= math.log(prob_hash["<UNK>"],2)

 elif n_gram == 3:
           while j<len(token):
                if (j+2)<(len(token) -1):
                     newlist_per.append(token[j]+" " + token[j+1]+" "+token[j+2])
                j += 1

           for word in newlist_per:
                if word in prob_hash:
                    p+= math.log(prob_hash[word],2)
                else:
                    p+= math.log(prob_hash["<UNK>"],2)

 l= float(p)/float(M)
 perplexity = 2 ** (-1 *l)
 return (perplexity)



def main():
   #f = open("C:/Users/rems/Documents/NLP/bible_corpus/bible_corpus/kjbible.train","r")
   #f = open('C:/Users/rems/Documents/NLP/HotelReviews/HotelReviews/reviews.train',"r")
   #f = open("train","r")
   #f = open("C:\Users\rems\PycharmProjects\untitled\train1.txt",r);

   oper = -1

   while int(oper) != 0:
        print('')
        print('Choose one of the following: ')
        print('1 - Unigram Model')
        print('2 - Bigram Model')
        print('3 - Random Sentence Generation')
        print('4 - Good Turing Smoothing')
        print('5 - Perplexity')
        print('6 - Trigram(Extension)')
        print('7 - Truthfulness of the review')
        print('0 - Exit')
        print('')

        oper = raw_input("Enter your input: ")

        if oper > 0:
             filename = raw_input('Enter training file name:')
             f = open(filename,"r")

             if int(oper) == 5:
                filename_test = raw_input('Enter the test file name:')
                ftest1 = open(filename_test,"r")
                ftest = open("preprocessed_test","w+")
                for line in ftest1:
                  proc_line = preprocessing(line)
                  ftest.write(proc_line)
                ftest.close()
                first = True

             #Truthfulness
             if int(oper) == 7:
                 ftest = raw_input('Enter the test file name')

                 ftrain = open(filename, 'r').read()
                 hotel_train_reviews=ftrain.split("\n")

                 ft_review = open(ftest, 'r').read()
                 hotel_test_reviews=ft_review.split("\n")
                 ftrain_true=open("test_truedata","w+")
                 ftrain_false=open("test_falsedata","w+")

                 for t in hotel_train_reviews:
                     t_split=t.split(",")

                     if t_split[0] =="IsTruthFul" or t_split[0] == '':
                         continue
                     elif int(t_split[0]) == 1:
                         ftrain_true.write(preprocessing(t))
                         ftrain_true.write("\n")
                     elif int(t_split[0]) == 0:
                        ftrain_false.write(preprocessing(t))
                        ftrain_false.write("\n")

                 ftrain_true.close()
                 ftrain_false.close()
                 first = True

                 ftrain_true="test_truedata"
                 ftrain_false="test_falsedata"

                 true_unigram_prob,true_unigram_hash=unigram(ftrain_true)
                 true_bigram_prob,true_bigram_hash=bigram(ftrain_true,true_unigram_hash)
                 true_trigram_prob,true_trigram_hash=trigram(ftrain_true,true_bigram_hash)

                 false_unigram_prob,false_unigram_hash=unigram(ftrain_false)
                 false_bigram_prob,false_bigram_hash=bigram(ftrain_false,false_unigram_hash)
                 false_trigram_prob,false_trigram_hash=trigram(ftrain_false,false_bigram_hash)

                 true_unigram_gt_prob= good_turing_smoothing(true_unigram_hash)
                 true_bigram_gt_prob= good_turing_smoothing(true_bigram_hash)
                 true_trigram_gt_prob = good_turing_smoothing(true_trigram_hash)
                 for key in true_trigram_gt_prob.keys():
                      true_trigram_prob[key] = true_trigram_gt_prob[key]

                 false_unigram_gt_prob=good_turing_smoothing(false_unigram_hash)
                 false_bigram_gt_prob=good_turing_smoothing(false_bigram_hash)
                 false_trigram_gt_prob = good_turing_smoothing(false_trigram_hash)

                 for key in false_trigram_gt_prob.keys():
                       false_trigram_prob[key] = false_trigram_gt_prob[key]

                 test_count=0

                 results=open("results.csv","w+")
                 results.write("Id,Label"+"\n")

                 file_separate_review=open("test_separate_review","w+")
                 file_separate_r = "test_separate_review"

                 for reviews in hotel_test_reviews:

                     if reviews=="IsTruthful,review" or reviews=='':
                         continue
                     file_separate_review.write(preprocessing(reviews))
                     file_separate_review.close()

                     true_trigram_perplexity=perplexity(true_trigram_prob,3,file_separate_r)
                     false_trigram_perplexity=perplexity(false_trigram_prob,3,file_separate_r)

                     if true_trigram_perplexity<false_trigram_perplexity:
                         results.write(str(test_count)+","+"1"+"\n")
                     elif true_trigram_perplexity>false_trigram_perplexity:
                         results.write(str(test_count)+","+"0"+"\n")

                     test_count+=1
                     file_separate_review=open("test_separate_review","w+")
                     file_separate_review.seek(0)
                     file_separate_review.truncate()

                 results.close()
                 if(int(oper) == 7):
                     exit()

             #In case of other operations
             fwrite = open("preprocessed_train","w+")
             for line in f:
                proc_line = preprocessing(line)
                fwrite.write(proc_line)
             fwrite.close()
             first = True

        if int(oper) >= 1 and int(oper) <=6:
               filename = "preprocessed_train"

               #Unigram and Bigram and Trigram
               unigram_prob,unigram_hash = unigram(filename)
               print("Unigram probability"+"\n")
               print_hash(unigram_prob)
               if(int(oper) == 1):
                   exit()

               bigram_prob,bigram_hash = bigram(filename,unigram_hash)
               print("Bigram probability"+"\n")
               print_hash(bigram_prob)
               if(int(oper)== 2):
                   exit()

               trigram_prob,trigram_hash = trigram(filename,bigram_hash)
               print("Trigram probability"+"\n")
               print_hash(trigram_prob)
               if(int(oper) == 6):
                   exit()

               #Random number Generation using Trigram+-
               if int(oper)==3:
                 print("Random sentences using bigram model"+"\n")
                 for i in range(5):
                     random_sentence(bigram_prob,2)
                 print("Random sentences using trigram model"+"\n")
                 for i in range(5):
                     random_sentence(trigram_prob,3)
                 if int(oper) == 3:
                    exit()

               #For good turing and perplexity
               if int(oper) == 4 or int(oper)==5:

                  global gt_prob
                  gt_prob = dict(unigram_prob)
                  global gt_bi_prob
                  gt_bi_prob = dict(bigram_prob)

                  gt_prob = good_turing_smoothing(unigram_hash)
                  print("Good Turing smoothing - unigram"+"\n")
                  print_hash(gt_prob)

                  gt_bi_prob = good_turing_smoothing(bigram_hash)
                  for key in gt_bi_prob.keys():
                      bigram_prob[key] = gt_bi_prob[key]
                  print("Good Turing smoothing - bigram"+"\n")
                  print_hash(gt_bi_prob)

                  if(int(oper) == 4):
                    exit()

               #For perplexity of unigram and bigram
               if int(oper) == 5:
                  filename = "preprocessed_test"
                  unigram_perplexity = perplexity(gt_prob,1,filename)
                  bigram_perplexity = perplexity(bigram_prob,2,filename)
                  print("Unigram perplexity is "+ str(unigram_perplexity))
                  print("Bigram perplexity is "+ str(bigram_perplexity))

                  if (int(oper)== 5):
                    exit()


if __name__ == "__main__":
    main()