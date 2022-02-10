from __future__ import print_function
import spotipy
from spotipy.oauth2 import SpotifyOAuth
#from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
from PyQt5.QtWidgets import QMessageBox

def normal_round(num, ndigits=0):
        if ndigits == 0:
            return int(num + 0.5)
        else:
            digit_value = 10 ** ndigits
            return int(num * digit_value + 0.5) / digit_value

def top_artist(time_range, songs_num):
    scope = 'user-top-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    results = sp.current_user_top_artists(limit=songs_num, offset=0, time_range=time_range)
    name_list = []
    genre_list = []
    followers_list = []
    url_list = []

    for item in (results['items']):
        name_list.append(item['name'])
        genre_list.append(item['genres'])
        followers_list.append(item['followers']['total'])
        url_list.append(item['external_urls']['spotify'])

    df = pd.DataFrame({'artist_name':name_list, 'genre':genre_list, 'followers':followers_list, 'URL': url_list})

    return df

def tracks_analyzer(time_range, songs_num):
    scope = 'user-top-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    results = sp.current_user_top_tracks(limit=songs_num, offset=0, time_range=time_range)
    title_list = []
    artist_list = []
    link_list = []
    url_list = []
    feature_list = []

    for item in (results['items']):
        title_list.append(item['name'])
        artist_list.append(item['artists'][0]['name'])
        url_list.append(item['external_urls']['spotify'])
        link_list.append((item['uri'][14:]))

    df = pd.DataFrame({'track_title':title_list, 'artist_name':artist_list, 'URL': url_list, 'track_id':link_list})

    for item in link_list:

        feature_list.append(track_feature(item))

    df2 = pd.DataFrame(feature_list, columns=('danceability_%','energy_%', 'positivity_%', 'tempo_BPM', 'loudness_dB',
            'speechiness_%', 'instrumentalness_%', 'duration_seconds'))

    data_df = pd.concat([df, df2], axis=1)

    av_dance = normal_round(data_df['danceability_%'].mean(axis=0), 2)
    av_energy = normal_round(data_df['energy_%'].mean(axis=0), 2)
    av_positivity = normal_round(data_df['positivity_%'].mean(axis=0), 2)
    av_tempo = data_df['tempo_BPM'].mean(axis=0)
    av_loudness = data_df['loudness_dB'].mean(axis=0)
    av_speechiness = normal_round(data_df['speechiness_%'].mean(axis=0), 2)
    av_instrument = normal_round(data_df['instrumentalness_%'].mean(axis=0), 2)
    av_duration = data_df['duration_seconds'].mean(axis=0)

    av_df = pd.DataFrame({'average_danceability_%':av_dance, 'average_energy_%':av_energy, 'average_positivity_%':av_positivity, 
        'average_tempo':av_tempo, 'average_loudness_dB':av_loudness, 'average_speechiness_%':av_speechiness, 'average_instrument_%':av_instrument,
        'av_duration': av_duration}, index=[0])

    return data_df, av_df


def track_feature(link):

    def stats_percentage(value):
        return normal_round((float(value)/1) * 100, 2)

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
    analysis = sp.audio_features(link)
    danceability = stats_percentage((analysis[0]['danceability']))
    energy = stats_percentage((analysis[0]['energy']))
    positivity = stats_percentage((analysis[0]['valence']))
    tempo = (analysis[0]['tempo'])
    loudness = (analysis[0]['loudness'])
    speechiness = stats_percentage((analysis[0]['speechiness']))
    instrumentalness = stats_percentage((analysis[0]['instrumentalness']))
    duration = (analysis[0]['duration_ms'])/1000.0

    return danceability, energy, positivity, tempo, loudness, speechiness, instrumentalness, duration

def export_ods(dataframe):

    dataframe.to_excel('spotify_data.xlsx')

    success_export(format='xlsx')

def export_csv(dataframe):

    dataframe.to_csv('spotify_data.csv')

    success_export(format='csv')

def success_export(format):

    msg = QMessageBox()
    msg.setWindowTitle("Yeah!")
    msg.setText("Data succesfully exported in a beautiful " + format + " file!")
    msg.setIcon(msg.Information)
    msg.exec()
