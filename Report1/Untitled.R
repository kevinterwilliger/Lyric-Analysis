temp = data %>% select(-Sentiment)

data = data %>% 
  mutate("Sentiment" = analyzeSentiment(as.character(Lyrics))$SentimentQDAP) %>%
  rename("AverageWordLength" = AverageLengths)

l = list()
for(lyric in lyrics) {
  append(l,analyzeSentiment())
}
