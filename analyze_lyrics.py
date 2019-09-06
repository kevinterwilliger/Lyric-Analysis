import nltk
import pandas as pd
import phonetics as ph
import lyrics as ly

# nltk.download("cmudict")
data = pd.read_csv("billboard_lyrics_1964-2015.csv", encoding = "ISO-8859-1")

vowels = ['a','e','i','o','u']
lyric = data.Lyrics[1]

l = ly.Lyrics(print_stats=None,text=lyric,language="en",lookback=15)
print(l.rhyme_stats())
