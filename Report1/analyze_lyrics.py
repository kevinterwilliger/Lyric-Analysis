import nltk
import sys,os
import pandas as pd
import phonetics as ph
import lyrics as ly

# nltk.download("cmudict")
data = pd.read_csv("billboard_lyrics_1964-2015.csv", encoding = "ISO-8859-1")
# data = pd.read_csv("data_new.csv")

def get_unique_words(lyrics):
    words = lyrics.split(sep=" ")
    unique_words = dict()
    sum = 0
    for word in words :
        sum += len(word)
        if word not in unique_words:
            unique_words[word] = 1
        else:
            unique_words[word] += 1
    avg = sum / len(words)
    if len(words) is 0 :
        length = 0
    else:
        length = len(words)
    return(len(unique_words),avg,length)


'''
This finds the average rhyme length of every song in the table and binds it to
the original data. Saves new data table to new csv.

uses Eric Malme's algorithm to measure the average length of rhymes in lyrics.
github: https://github.com/ekQ/raplysaattori
'''
avg_rhyme_length = []
unique_words = []
average_lengths = []
num_words = []

sys.stdout = open(os.devnull, 'w')

for i in range(0,len(data.index)) :
    # sometimes the lyrics are float values, idk why
    # if the lyrics aren't a string, the avg_rhyme_length is set to a constant 9999
    if type(data.loc[i].Lyrics) is not type(" ") or data.loc[i].Lyrics is "" :
        avg_rhyme_length.append(9999)
        unique_words.append(9999)
        average_lengths.append(9999)
        num_words.append(9999)
    else :
        # clean lyrics
        lyric = data.loc[i].Lyrics.strip()
        lyric = lyric.replace("  "," ")

        w,a,n = get_unique_words(lyric)
        unique_words.append(w)
        average_lengths.append(a)
        num_words.append(n)

        l = ly.Lyrics(print_stats=None,text=lyric,language="en",lookback=15)
        avg_rhyme_length.append(l.get_avg_rhyme_length())

columns = pd.DataFrame({
                'AverageRhymeLength': avg_rhyme_length,
                'UniqueWords' : unique_words,
                'AverageLengths' : average_lengths,
                'NumberWords' : num_words})

# columns = pd.DataFrame(unique_words,columns=['unique_words'])
data_new = pd.concat([data,columns],axis=1,ignore_index=False)
data_new.to_csv("data_new.csv",index=True)

sys.stdout = sys.__stdout__
print("saved")
