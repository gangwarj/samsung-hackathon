# Source Code split in steps


#load the libraries

library("ROAuth")
library("twitteR")
library(wordcloud)
library(RCurl) 

api_key <- "bEm0x3zX0y2PwjDGJh1NDhfpb"

api_secret <- "DSFjV8BDNm5nVrDsKnUvKCtbuzqqHs8G7O4p3B0rVHsAvSdL8Q"   # Consumer secret: *

access_token <- "1021116325-q6IB9ujo8dO4FlerNYEttMfUMSInR47KRXhvxoH"  # Access token: 

access_token_secret <- "1fro1HMrQYDpx8QxfHBJkqjlNQbpTkAYHOKmHn9RGKAdR" # Access token secret: 

setup_twitter_oauth(api_key,api_secret,access_token,access_token_secret)


# search for the tweets
tweets=searchTwitter("$AAPL", n=3200)


# print all the tweets
head(tweets)



# returns the number of tweets
length(tweets)


# Load this list of libraries
library(twitteR)
library(tm)
library(wordcloud)
library(RColorBrewer)



# searching for tweets containing the keywords �yahoo finance�
tweet_cloud = searchTwitter("jio", n=3200, lang="en")


# Extract the text from the tweets using sapply function

iphone = read.csv("iphone.csv", header = F)
redmi = read.csv("redmi.csv", header = F)

text_cloud = sapply(tweet_cloud, function(x) x$getText())
text_cloud = redmi$V1
text_cloud = iphone$V1
# Creating corpus
corpus = Corpus(VectorSource(text_cloud))


# creating document term matrix  
matrix = TermDocumentMatrix(corpus,
                            control = list(removePunctuation = TRUE,
                                           stopwords = stopwords((kind='en')),
                                           removeNumbers = TRUE, tolower = TRUE))


# defining tdm as matrix
m = as.matrix(matrix)


# Getting word counts in decreasing order
frequent_words = sort(rowSums(m), decreasing=TRUE) 

# Creating a data frame with words and their frequencies
dframe = data.frame(word=names(frequent_words), freq=frequent_words)


# Plot wordcloud
#wordcloud(dframe$word, dframe$freq, random.order=TRUE, colors=brewer.pal(8, "Dark2"))



# Image in image format
#png("yahoo finance.png", width=12, height=8, units="in", res=300)
#wordcloud(dm$word, dm$freq, random.order=FALSE, colors=brewer.pal(8, "Dark2"))
#dev.off()

# Plyr allows the user to split a data set apart into smaller subsets, apply methods to the subsets, and combine the results.
 library(plyr)


# organize the twitter data using lapply
tweets=lapply(tweets, function(t) t$getText())
summary(tweets)


# write the tweets data frame to the file tweets.csv
write.csv(tweets, file="tweets.csv")


# getting positive and negative words txt file
positive_words=scan("positive-words.txt",what="character",comment.char=";")

negative_words=scan("negative-words.txt",what="character",comment.char=";")



# code for sentiment analysis
score.sentiment = function(sentences, pos.words, neg.words, .progress='none')
{
  require(plyr)
  require(stringr)
  
  # we got a vector of sentences. plyr will handle a list
  # or a vector as an "l" for us
  # we want a simple array ("a") of scores back, so we use 
  # "l" + "a" + "ply" = "lapply":
  scores = laply(sentences, function(sentence, pos.words, neg.words) {
    
    # clean up sentences with R's regex-driven global substitute, gsub():
    sentence = gsub('[[:punct:]]', '', sentence)
    sentence = gsub('[[:cntrl:]]', '', sentence)
    sentence = gsub('\\d+', '', sentence)
    # and convert to lower case:
    sentence = tolower(sentence)
    
    # split into words. str_split is in the stringr package
    word.list = str_split(sentence, '\\s+')
    # sometimes a list() is one level of hierarchy too much
    words = unlist(word.list)
    
    # compare our words to the dictionaries of positive & negative terms
    pos.matches = match(words, pos.words)
    neg.matches = match(words, neg.words)
    
    # match() returns the position of the matched term or NA
    # we just want a TRUE/FALSE:
    pos.matches = !is.na(pos.matches)
    neg.matches = !is.na(neg.matches)
    
    # and conveniently enough, TRUE/FALSE will be treated as 1/0 by sum():
    score = sum(pos.matches) - sum(neg.matches)
    
    return(score)
  }, pos.words, neg.words, .progress=.progress )
  
  scores.df = data.frame(score=scores, text=sentences)
  return(scores.df)
}



# perform sentiment analysis for the dataset tweets and store it in Results
Results=score.sentiment(tweets,positive_words,negative_words)

# getting the summary of the Results
summary(Results)

# plot histogram
hist(Results$score)












