import nltk
import random
import nltk.tag, nltk.data
from nltk.corpus import brown
import re
from nltk.tag.sequential import ClassifierBasedTagger

class ClassifierBasedGermanTagger(ClassifierBasedTagger):
    """A classifier based German part-of-speech tagger. It has an accuracy of
    96.09% after being trained on 90% of the German TIGER corpus. The tagger
    extends the NLTK ClassifierBasedTagger and implements a slightly modified
    feature detector.
    """

    def feature_detector(self, tokens, index, history):
        """Implementing a slightly modified feature detector.
        @param tokens: The tokens from the sentence to tag.
        @param index: The current token index to tag.
        @param history: The previous tagged tokens.
        """

        word = tokens[index]
        if index == 0: # At the beginning of the sentence
            prevword = prevprevword = None
            prevtag = prevprevtag = None
            #word = word.lower() # Lowercase at the beginning of sentence
        elif index == 1:
            prevword = tokens[index-1] # Note: no lowercase
            prevprevword = None
            prevtag = history[index-1]
            prevprevtag = None
        else:
            prevword = tokens[index-1]
            prevprevword = tokens[index-2]
            prevtag = history[index-1]
            prevprevtag = history[index-2]

        if re.match('[0-9]+([\.,][0-9]*)?|[0-9]*[\.,][0-9]+$', word):
            # Included "," as decimal point
            shape = 'number'
        elif re.compile('\W+$', re.UNICODE).match(word):
            # Included unicode flag
            shape = 'punct'
        elif re.match('([A-ZÄÖÜ]+[a-zäöüß]*-?)+$', word):
            # Included dash for dashed words and umlauts
            shape = 'upcase'
        elif re.match('[a-zäöüß]+', word):
            # Included umlauts
            shape = 'downcase'
        elif re.compile("\w+", re.UNICODE).match(word):
            # Included unicode flag
            shape = 'mixedcase'
        else:
            shape = 'other'

        features = {
            'prevtag': prevtag,
            'prevprevtag': prevprevtag,
            'word': word,
            'word.lower': word.lower(),
            'suffix3': word.lower()[-3:],
            #'suffix2': word.lower()[-2:],
            #'suffix1': word.lower()[-1:],
            'preffix1': word[:1], # included
            'prevprevword': prevprevword,
            'prevword': prevword,
            'prevtag+word': '%s+%s' % (prevtag, word),
            'prevprevtag+word': '%s+%s' % (prevprevtag, word),
            'prevword+word': '%s+%s' % (prevword, word),
            'shape': shape
            }
        return features

corp = nltk.corpus.ConllCorpusReader('.', 'tiger_release_aug07.corrected.16012013.conll09',
                                     ['ignore', 'words', 'ignore', 'ignore', 'pos'],
                                     encoding='utf-8')
tagged_sents = corp.tagged_sents()
random.shuffle(tagged_sents)


def evaluate(tagger, sentences):
    good,total = 0,0.
    for sentence,func in sentences:
        tags = tagger.tag(nltk.word_tokenize(sentence))
        good += func(tags)
        total += 1



class Text():
    def __init__(self, text):
        self.text = nltk.word_tokenize(text)
        self.training_count = int(len(nltk.corpus.brown.tagged_sents(categories='news')) * 0.9)
        self.training_sents = nltk.corpus.brown.tagged_sents(categories='news')[:self.training_count]
        
    def word_tagger(self):
        default_tagger = nltk.DefaultTagger('NN')
        unigram_tagger = nltk.UnigramTagger(self.training_sents, backoff=default_tagger)
        bigram_tagger = nltk.BigramTagger(self.training_sents, backoff=unigram_tagger)
        self.text = bigram_tagger.tag(self.text)
        
    def find_sentence(self, word):
        #TODO: normal sentence
        pass 
    
        
    def find_word(self, word):
        IN = self.text.count((word, 'IN'))
        if IN != 0:
            print('word "' + word +'" as preposition or conjunction : ' + str(IN))
        NN = self.text.count((word, 'NN'))
        if NN != 0:
            print('word "' + word +'" as noun, common, singular or mass : ' + str(NN))  
        RB = self.text.count((word, 'RB'))
        if RB != 0:
            print('word "' + word +'" as adverb : ' + str(RB)) 
        JJ = self.text.count((word, 'JJ'))
        if JJ != 0:
            print('word "' + word +'" as adjective or numeral, ordinal : ' + str(JJ))   
        CC = self.text.count((word, 'CC'))
        if CC != 0:
            print('word "' + word +'" as conjunction, coordinating : ' + str(CC))   
        CD = self.text.count((word, 'CD'))
        if CD != 0:
            print('word "' + word +'" as numeral, cardinal : ' + str(CD))   
        DT = self.text.count((word, 'DT'))
        if DT != 0:
            print('word "' + word +'" as determiner : ' + str(DT))   
        EX = self.text.count((word, 'EX'))
        if EX != 0:
            print('word "' + word +'" as existential there : ' + str(EX))   
        JJR = self.text.count((word, 'JJR'))
        if JJR != 0:
            print('word "' + word +'" as adjective, comparative : ' + str(JJR))
        JJS = self.text.count((word, 'JJS'))
        if JJS != 0:
            print('word "' + word +'" as adjective, superlative : ' + str(JJS))               
        LS = self.text.count((word, 'LS'))
        if LS != 0:
            print('word "' + word +'" as list item marker : ' + str(LS))               
        MD = self.text.count((word, 'MD'))
        if MD != 0:
            print('word "' + word +'" as modal auxiliary : ' + str(MD))               
        NNP = self.text.count((word, 'NNP'))
        if NNP != 0:
            print('word "' + word +'" as noun, proper, singular : ' + str(NNP))               
        NNS = self.text.count((word, 'NNS'))
        if NNS != 0:
            print('word "' + word +'" as noun, common, plural : ' + str(NNS))             
        PDT = self.text.count((word, 'PDT'))
        if PDT != 0:
            print('word "' + word +'" as pre-determiner : ' + str(PDT))               
        POS = self.text.count((word, 'POS'))
        if POS != 0:
            print('word "' + word +'" as genitive marker : ' + str(POS))               
        PRP = self.text.count((word, 'PRP'))
        if PRP != 0:
            print('word "' + word +'" as pronoun, personal : ' + str(PRP))               
        PRPS = self.text.count((word, 'PRP$'))
        if PRPS != 0:
            print('word "' + word +'" as pronoun, possessive : ' + str(PRPS))                 
        RBR = self.text.count((word, 'RBR'))
        if RBR != 0:
            print('word "' + word +'" as adverb, comparative : ' + str(RBR))             
        RBS = self.text.count((word, 'RBS'))
        if RBS != 0:
            print('word "' + word +'" as adverb, superlative : ' + str(RBS))               
        RP = self.text.count((word, 'RP'))
        if RP != 0:
            print('word "' + word +'" as particle : ' + str(RP))               
        TO = self.text.count((word, 'TO'))
        if TO != 0:
            print('word "' + word +'" as "to" as preposition or infinitive marker: ' + str(TO))               
        UH = self.text.count((word, 'UH'))
        if UH != 0:
            print('word "' + word +'" as interjection : ' + str(UH))                 
        VB = self.text.count((word, 'VB'))
        if VB != 0:
            print('word "' + word +'" as  verb, base form : ' + str(VB))             
        VBD = self.text.count((word, 'VBD'))
        if VBD != 0:
            print('word "' + word +'" as verb, past tense : ' + str(VBD))               
        VBG = self.text.count((word, 'VBG'))
        if VBG != 0:
            print('word "' + word +'" as verb, present participle or gerund : ' + str(VBG))               
        VBN = self.text.count((word, 'VBN'))
        if VBN != 0:
            print('word "' + word +'" as verb, past participle : ' + str(VBN))               
        VBP = self.text.count((word, 'VBP'))
        if VBP != 0:
            print('word "' + word +'" as verb, present tense, not 3rd person singular : ' + str(VBP))                 
        VBZ = self.text.count((word, 'VBZ'))
        if VBZ != 0:
            print('word "' + word +'" as verb, present tense, 3rd person singular : ' + str(VBZ))             
        WPT = self.text.count((word, 'WPT'))
        if WPT != 0:
            print('word "' + word +'" as WH-determiner : ' + str(WPT))               
        WP = self.text.count((word, 'WP'))
        if WP != 0:
            print('word "' + word +'" as WH-pronoun : ' + str(WP))               
        WRB = self.text.count((word, 'WRB'))
        if WRB != 0:
            print('word "' + word +'" as WH-adverb : ' + str(WRB))               
        FW = self.text.count((word, 'FW'))
        if FW != 0:
            print('word "' + word +'" as foreign word : ' + str(FW))              
        WPS = self.text.count((word, 'WP$'))
        if WPS != 0:
            print('word "' + word +'" as WH-pronoun, possessive : ' + str(WPS))             
        NNPS = self.text.count((word, 'NNPS'))
        if NNPS != 0:
            print('word "' + word +'" as noun, proper, plural : ' + str(NNPS))               
        SYM = self.text.count((word, 'SYM'))
        if SYM != 0:
            print('word "' + word +'" as symbol : ' + str(SYM))               
        AT = self.text.count((word, 'AT'))
        if AT != 0:
            print('word "' + word +'" as article : ' + str(AT))               

class Gertext(Text):
    def __init__(self, text):
        self.text = nltk.word_tokenize(text)
        self.training_count = int(len(corp.tagged_sents()) * 0.9)
        self.training_sents = corp.tagged_sents[:self.training_count]
    def word_tagger(self):
        tagger = ClassifierBasedGermanTagger(train=self.training_sents)
        self.text = tagger.tag(self.text)



def start():
    print('Enter your text')            
    letter = Text(str(input()).lower())
    letter.word_tagger()
    print(letter.text)
    print('Enter sought word')
    letter.find_word(str(input()).lower())
    
    
if __name__ == "__main__":
    start()