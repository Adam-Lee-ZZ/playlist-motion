import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from lyricsgenius import Genius
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
import seaborn as sns
import pandas as pd
import sys

def get_playlist(playlist_id):
    
    print("List loading...")
    play_list = []

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    results = spotify.playlist_items(playlist_id=playlist_id,limit=10)
    songs = results['items']

    for song in songs:
        name = song['track']['name']
        artist = song['track']['artists'][0]['name']
        play_list.append([name,artist])
    
    print("List loaded.")

    return play_list


def lyrics_score(play_list,token):

    print('lyrics loading...')
    score_list = []
    Whole_l = []
    count = 1

    for s in play_list:
        genius = Genius(access_token=token)
        lyric = genius.search_song(s[0],artist=s[1]).lyrics
        Whole_l.append(lyric.replace('\n',' ').split(' '))
        blob = TextBlob(lyric)
        sentiment = blob.sentiment
        score = sentiment.polarity
        if score > 0 :
            score_list.append([s[0],1])
        elif score < 0 :
            score_list.append([s[0],-1])
        else:
            score_list.append([s[0],0])
        print(f'{count}/{len(play_list)}')
        count+=1
    
    return score_list, Whole_l

def plot_wordcloud(data,title,max_words):
    data = " ".join(data[0])
    word_cloud= WordCloud(background_color="white", random_state=1,max_words=max_words,width =800, height = 1500)
    word_cloud.generate(data)
    plt.figure(figsize=[10,10])
    plt.imshow(word_cloud,interpolation="bilinear")
    plt.axis('off')
    plt.title(title)
    plt.savefig('foo.png')
    plt.close()
        

if __name__ == '__main__':
    print("Starting...")
    list = get_playlist(sys.argv[1])
    score_list,data =lyrics_score(list,sys.argv[2])
    score_list = pd.DataFrame(score_list)
    score_list.columns = ['song_count','sentiment']
    score_list['sentiment'].replace(1,'positive')
    score_list['sentiment'].replace(2,'negetive')
    plot_wordcloud(data, "word cloud of playlist", 800)
    sns.countplot(data=score_list,x='sentiment')
    plt.title('Sentiment Analysis of review')
    plt.savefig('foo1.png')
    plt.close()
    print(score_list)