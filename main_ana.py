import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from lyricsgenius import Genius
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sixdict import sa
import ssl

def get_playlist(playlist_id):
    
    print("List loading...")
    play_list = []

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    results = spotify.playlist_items(playlist_id=playlist_id,limit=20)
    songs = results['items']

    for song in songs:
        name = song['track']['name']
        artist = song['track']['artists'][0]['name']
        play_list.append([name,artist])
    
    print("List loaded.")

    return play_list


def lyrics(play_list,token):

    print('lyrics loading...')
    Whole_l = []

    for s in play_list:
        genius = Genius(access_token=token)
        lyric = genius.search_song(s[0],artist=s[1]).lyrics
        lyric = lyric.replace('\n',' ').split(' ')
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(" ".join(lyric))
        filtered_lyric = []
        
        for w in word_tokens:
            if w.lower() not in stop_words and w.lower() not in ['s','ohh','chorus',"n't"]:
                filtered_lyric.append(w)
        
        Whole_l.append(filtered_lyric)
    
    return Whole_l

def plot_wordcloud(data,title,max_words):
    data = " ".join(data[0])
    word_cloud= WordCloud(background_color="white", random_state=1,max_words=max_words,width =800, height = 1500)
    word_cloud.generate(data)
    plt.figure(figsize=[10,10])
    plt.imshow(word_cloud,interpolation="bilinear")
    plt.axis('off')
    plt.title(title)
    plt.savefig('css/cloud.png')
    plt.close()

def sixd(data):
    s = sa()
    motion = s.to_v(data)
    result = pd.DataFrame([motion['Vision'].mean(),motion["Motor"].mean(),
                           motion['Socialness'].mean(),motion['Emotion'].mean(),
                           motion["Time"].mean(), motion['Space'].mean()],index=
                           ['Vision','Motor','Socialness','Emotion','Time','Space']).T
    plt.figure(figsize=(10, 7))
    sns.barplot(result)
    plt.savefig('css/six.png')
    plt.close()

def main(url):
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    
    nltk.download('stopwords')
    nltk.download('punkt_tab')
    p_list = get_playlist(url)
    data =lyrics(p_list,'cBsCaaON_gUaD405OQYgObdBY8JnFxpLDrcTEFQYd3sMoBlGIBdv6Yl4e1jibULE')
    plot_wordcloud(data, "word cloud of playlist", 800)
    sixd(data[0])



if __name__ == '__main__':
    print("Starting...")

    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    
    nltk.download('stopwords')
    nltk.download('punkt_tab')

    list = get_playlist('0xBR12jNDKZUOxYnH5ejnS')
    data =lyrics(list,'cBsCaaON_gUaD405OQYgObdBY8JnFxpLDrcTEFQYd3sMoBlGIBdv6Yl4e1jibULE')
    
    plot_wordcloud(data, "word cloud of playlist", 800)
    sixd(data[0])