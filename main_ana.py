import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import nltk
from sixdict import sa
import ssl
import pandas as pd
import psycopg2
from psycopg2 import sql
from io import BytesIO
import base64


def get_playlist(playlist_id):
    
    print("List loading...")
    play_list = []

    auth_manager = SpotifyClientCredentials()
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    results = spotify.playlist_items(playlist_id=playlist_id,limit=20)
    songs = results['items']

    for song in songs:
        name = song['track']['name']
        artist = song['track']['artists'][0]['name']
        play_list.append([artist,name])
    
    print("List loaded.")

    return play_list


def lyrics(play_list):


    print('lyrics loading...')
    Whole_l = []

    for s in play_list:
        connection = None
        try:
            connection = psycopg2.connect(
                host=
                database=
                user=
                password=
                port=
            )
            cursor = connection.cursor()
            
            query = sql.SQL("SELECT lyrics FROM lyric WHERE title = %s AND artist = %s;")
            print('selecting')
            
            cursor.execute(query, (s[1], s[0]))

            result = cursor.fetchone()
            if result:
                Whole_l.append(result[0])
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
            pass
        
        finally:
            if connection is not None:
                connection.close()
    
    if Whole_l ==[]:
        return 'broke'
        
    return Whole_l

def plot_wordcloud(data,title,max_words):
    d = ''
    for i in data:
        d += i
    word_cloud= WordCloud(background_color="white", random_state=1,max_words=max_words,width =800, height = 1500)
    word_cloud.generate(d)
    plt.figure(figsize=[10,10])
    plt.imshow(word_cloud,interpolation="bilinear")
    plt.axis('off')
    plt.title(title)
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300)
    img_buffer.seek(0)
    base64_img = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    return d, base64_img

def sixd(data):
    s = sa()
    motion = s.to_v(data)
    result = pd.DataFrame([motion['Vision'].mean(),motion["Motor"].mean(),
                           motion['Socialness'].mean(),motion['Emotion'].mean(),
                           motion["Time"].mean(), motion['Space'].mean()],index=
                           ['Vision','Motor','Socialness','Emotion','Time','Space']).T
    plt.figure(figsize=(10, 7))
    sns.barplot(result)
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300)
    img_buffer.seek(0)
    base64_img = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    plt.close()
    return base64_img

def main(playlist_id):
    data = get_playlist(playlist_id)
    ly = lyrics(data)
    if ly == 'broke':
        return 'broke'
    d = plot_wordcloud(ly, 'Cloud Plot of Your List', 20000)
    return sixd(d)




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
    data, _ =lyrics(list)
    sixd(data)