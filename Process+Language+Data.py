
# coding: utf-8

# In[1]:

import pickle
import nltk
from nltk.collocations import *
import gensim
from nltk import word_tokenize
import operator
import string
from nltk.util import ngrams
import os
from nltk.tokenize import sent_tokenize


# In[2]:

def remove_data_within_brackets(test_str):
    ret = ''
    skip1c = 0
    skip2c = 0
    skip3c = 0
    for i in test_str:
        if i == '[':
            skip1c += 1
        elif i == '(':
            skip2c += 1
        elif i == '<':
            skip3c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif i == ')'and skip2c > 0:
            skip2c -= 1
        elif i == '>' and skip3c > 0:
            skip3c -= 1
        elif skip1c == 0 and skip2c == 0 and skip3c == 0:
            ret += i
    return ret


# In[14]:

def getPOSTag (sentence,word):
    PosSent = nltk.pos_tag(nltk.word_tokenize(sentence))
    for word_Tag in PosSent:
        if(word_Tag[0].lower()==word.lower()):
            return (word.lower() + "_"+word_Tag[1])
    return ("word not in sentence")


# In[ ]:

#load MT file
inputFile = open('F:\\ParaPhrase\\LanguageData\\NB_EN_1M_LessEdited_a_Mod.txt',  'rb')
data = inputFile.readlines()
inputFile.close()


# In[ ]:

Utterances = []
data[1].decode("utf-8").strip().lower()


# In[ ]:

def AddLines(Utterances,data):
    for lines in data:
        lines = lines.decode("utf-8").strip()
        temp = sent_tokenize(lines)
        for line in temp:
            line = line.replace(","," ")
            line = line.replace ("("," ")
            line = line.replace (")"," ")
            line = line.replace ("*"," ")
            line = line.replace ("#"," ")
            line = line.replace ("."," . ")
            line = line.replace ("?"," ? ")
            line = line.replace ("!"," ! ")
            line = line.replace (" 's","'s")
            line = line.replace (" 'd","'d")
            line = line.replace ("â"," ")
            line = line.replace ("/"," ")
            line = ''.join([i for i in line if not i.isdigit()])
            Utterances.append(line)


# In[ ]:

AddLines(Utterances,data)


# In[ ]:

print(len(Utterances))
print(Utterances[1:5])


# In[ ]:

inputFile = open('F:\\ParaPhrase\\LanguageData\\NB_EN_1M_LessEdited_d_Mod.txt',  'rb')
data = inputFile.readlines()
inputFile.close()


# In[ ]:

AddLines(Utterances,data)


# In[ ]:

print(len(Utterances))
print(Utterances[1:5])


# In[ ]:

NewUtterancesUnique = list(set(Utterances))
print(len(NewUtterancesUnique))
print((NewUtterancesUnique)[1:5])


# In[ ]:

outputFile = open('LanguageData.pkl', 'wb')
pickle.dump(Utterances,outputFile)
outputFile.close()


# In[ ]:

outputFile = open('LanguageData_NewUtterancesUnique.pkl', 'wb')
pickle.dump(NewUtterancesUnique,outputFile)
outputFile.close()


# In[ ]:

print(len(NewUtterancesUnique))


# In[ ]:

count =1
totalInstances = len(NewUtterancesUnique)
for i in range(0,totalInstances,25000):
    filename = "LanguageDataUtterances"+str(count)+".txt"
    print(filename)
    print(i)
    count =count+1
    my_file = open(filename, "wb")
    for utt in NewUtterancesUnique[i+1:min(i+25000,totalInstances)]:
        my_file.write(str(utt).encode("utf-8"))
    my_file.close()
    #print(str(i+50000))


# In[4]:

PATH = "F:\\ParaPhrase\\conllFiles2"
FilesList = [os.path.join(dp, f) for dp, dn, filenames in os.walk(PATH) for f in filenames if os.path.splitext(f)[1] == '.conll']


# In[5]:

class ConllLine:
    def __init__(self, index, targetWord,tag,affectIndex,relation):
        self.index = index
        self.targetWord =targetWord
        self.tag=tag
        self.affectIndex=affectIndex
        self.relation=relation
        self.children = []
       self.FinalString=" "
    def addChild(self, ci):
        self.children.append(ci)
    def update(self, other):
        self.index = other.index
        self.targetWord =other.targetWord
        self.tag=other.tag
        self.affectIndex=other.affectIndex
        self.relation=other.relation   

# In[6]:

ConllList=[]
treeList = []
count = 1
lineCount = 1
for fname in FilesList:
    print(fname)
    with open(fname) as f:
        contents = f.readlines()
        ConnlUnit=[]
        t = {}
        for line in contents:
            lineCount=lineCount+1
            words = line.split("\t")
            if (len(words)== 7):
                index=words[0]
                targetWord=words[1]
                tag = words[3]
                affectIndex = words[5]
                relation = words[6]
                ConnlUnit.append(ConllLine(index,targetWord,tag,affectIndex,relation))
                if (len(t) < int(index)):
                    t[index] = ConllLine(index,targetWord,tag,affectIndex,relation)
                else:
                    t[index].update( ConllLine(index,targetWord,tag,affectIndex,relation) )
                if (int(index) < int(affectIndex)):
                    t[affectIndex] = ConllLine(affectIndex,"","","","")
                t[index].addChild(affectIndex)
                
            elif (len(words) == 0):
                ConllList.append(ConnlUnit)
                ConnlUnit=[]
                t = {}
                count = count +1
            else:
                error("invalid line: %s\n" % line)
        ConllList.append(ConnlUnit)
        treeList.append(deps)


# In[7]:

print(len(ConllList))
print(count)
print(lineCount)


# In[8]:

lineCount1 = 1
sentences = []
for (cU,t) in zip(ConllList,treeList):
    ConnlUnit=[]
    for (cl,tnode) in zip(cU,t):
        lineCount1=lineCount1+1
        AI = int(cl.affectIndex) - 1
        if(AI>=0):
            cl.FinalString = cl.targetWord + "_"+cl.tag + " "+ cl.relation.strip() + " "+ cU[AI].targetWord+"_"+cU[AI].tag
            cl.FinalString += [(" %s %s_%s" % t[ci].relation+"Inv", t[ci].targetWord, t[ci].tag) for ci in tnode.children]
        else :
            cl.FinalString = cl.targetWord + "_"+cl.tag + " "+ cl.relation.strip()
        sentences.append(cl.FinalString)


# In[9]:

tokenizedSentences = []
for sent in sentences:
    tokenizedSentences.append(nltk.word_tokenize (sent))


# In[11]:

sentences[1:100]


# In[ ]:

str1 = "this is string example.wow!!!";
str2 = ".";
str1.find(str2)


# In[ ]:

# train word2vec on the sentences (https://radimrehurek.com/gensim/models/word2vec.html)
model = gensim.models.Word2Vec(tokenizedSentences, min_count=20,window=100,size=300,sg=1,iter =10)
fname = "LanguageData_deppos_skip_iter10_size_300_min_count_20"
model.save(fname)


# In[ ]:

model = 
vocab = model.index2word
print(len(vocab))


# In[ ]:

model.most_similar_cosmul("denver_NN")


# In[ ]:

model.most_similar_cosmul("will_MD",topn=15)


# In[ ]:

model.most_similar_cosmul("today_NN")


# In[ ]:

model.most_similar_cosmul("than_IN")


# In[ ]:

model.most_similar_cosmul("guess_VBP",topn=15)


# In[ ]:

model.most_similar_cosmul("day_NN",topn=15)


# In[ ]:

model.most_similar_cosmul("not_RB",topn=15)


# In[ ]:

vocab = model.index2word
print(len(vocab))


# In[ ]:

#increased size to 500 and min count is 20
model1 = gensim.models.Word2Vec(tokenizedSentences, min_count=20,window=100,size=500,sg=1,iter =10)
fname = "LanguageData_deppos_minCount20_skip_iter10_size_500"
model1.save(fname)


# In[ ]:

vocab = model1.index2word
print(len(vocab))


# In[12]:

model = gensim.models.Word2Vec.load("LanguageData_deppos_minCount20_skip_iter10_size_500")


# In[13]:

vocab = model.index2word


# In[15]:

path = "F:\\ParaPhrase\\Notebooks\\UnigramContext.txt"
unigrams = []
with open(path,'r') as source:
    for line in source:
        fields = line.split('\t')
        unigrams.append(fields)


# In[32]:

tagged_word = getPOSTag ("is that an  option","option")
print(tagged_word)
result = model.most_similar(tagged_word,topn=15)
print(result)


# In[16]:

with open( "UnigramCandidates.tsv", "w" ) as f :
    for uni in unigrams:
        tagged_word = getPOSTag (uni[0],uni[1].strip())
        tagged_word_pos = tagged_word.split('_')

        f.write ( "\" " + uni[1].strip().upper() + "\" "+ " in context of  "+ "\" " + uni[0] + "\" "+ " is tagged as " + "\" " + tagged_word + "\" " + "\n")
        if(tagged_word in vocab):
            result = model.most_similar(tagged_word,topn=15)
            for words_score in result:
                if("_" not in words_score[0] or words_score[1] < 0.2):
                    continue;
                wordsTags = words_score[0].split("_")
                f.write ("\t"+wordsTags[0] + "\t" + str(words_score[1])+ "\t"+wordsTags[1])
                if(tagged_word_pos[1][0:2] in words_score[0]):
                    f.write("\t TRUE\n")
                else:
                    f.write("\t FALSE\n") 


# In[ ]:




# In[ ]:

model1.most_similar_cosmul("will_MD",topn=15)


# In[ ]:

model1.most_similar_cosmul("today_NN",topn=15)


# In[ ]:

model1.most_similar_cosmul("than_IN",topn=15)


# In[ ]:

model1.most_similar_cosmul("guess_VBP",topn=15)


# In[ ]:

model.most_similar_cosmul("guess_VBP",topn=15)


# In[ ]:

model1.most_similar_cosmul("day_NN",topn=15)


# In[ ]:

model1.most_similar_cosmul("not_RB",topn=15)


# In[ ]:

wordtag = getPOSTag("what does that mean","mean")
print(wordtag)
model.most_similar(wordtag)


# In[ ]:

#No negative sampling
model2 = gensim.models.Word2Vec(tokenizedSentences, min_count=20,window=100,size=500,sg=1,iter =15,negative =0)
fname = "LanguageData_deppos_minCount15_skip_iter15_size_500_min_count_50_no_neg"
model2.save(fname)


# In[ ]:

model2.most_similar_cosmul("denver_NN",topn=15)


# In[ ]:

model2.most_similar_cosmul("will_MD",topn=15)


# In[ ]:

model2.most_similar_cosmul("today_NN",topn=15)


# In[ ]:

model.most_similar_cosmul("today_NN",topn=15)


# In[ ]:

model2.most_similar_cosmul("than_IN",topn=15)


# In[ ]:

model.most_similar_cosmul("than_IN",topn=15)


# In[ ]:

model2.most_similar_cosmul("guess_VBP",topn=15)


# In[ ]:

model.most_similar_cosmul("guess_VBP",topn=15)


# In[ ]:

model2.most_similar_cosmul("day_NN",topn=15)


# In[ ]:

model2.most_similar_cosmul("not_RB",topn=15)


# ## tsne

# In[ ]:

import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


# In[ ]:

vocabulary = ["not","dont","day","won't","besides","today"]

