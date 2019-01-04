import nltk
training_count = int(len(nltk.corpus.brown.tagged_sents(categories='news')) * 0.9)
training_sents = nltk.corpus.brown.tagged_sents(categories='news')[:training_count]
testing_sents = nltk.corpus.brown.tagged_sents(categories='news')[training_count+1:]
testing_sents_notags = nltk.corpus.brown.sents(categories='news')[training_count+1:]
tags = [tag for (word, tag) in nltk.corpus.brown.tagged_words(categories='news')]
nltk.FreqDist(tags).max()
default_tagger = nltk.DefaultTagger('NN')
unigram_tagger = nltk.UnigramTagger(training_sents, backoff=default_tagger)
bigram_tagger = nltk.BigramTagger(training_sents, backoff=unigram_tagger)
print(testing_sents_notags[11])
print(bigram_tagger.tag(testing_sents_notags[11]))
print(bigram_tagger.evaluate(testing_sents))
def findtags(tag_prefix, tagged_text):
    cfd = nltk.ConditionalFreqDist((tag, word) for (word, tag) in tagged_text
                                  if tag.startswith(tag_prefix))
    return dict((tag, cfd[tag].most_common(5)) for tag in cfd.conditions())
tagdict = findtags('VB', nltk.corpus.brown.tagged_words(categories='news'))
for tag in sorted(tagdict):
    print(tag, tagdict[tag])