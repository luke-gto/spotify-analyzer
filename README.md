## Welcome to Spotify Analyzer

You can use this tool to retrieve data about your listening history on Spotify, export them in a .csv or .xlsx file and do some lovely analysis.

This tools uses the official Spotify Web API and in order to access them you have to:

1. Go to the [Dashboard](https://developer.spotify.com/dashboard/login) page at the *Spotify Developer website* and, if necessary, log in.

2. Click on ["Create an App"](docs/imgs/create_app.png)

3. Choose a name for the app and click on ["Create"](docs/imgs/20220211-184747.png)

4.  Now you have your personal App, congrats. Click on "EDIT SETTINGS" and in the "Redirect URIs" field enter this string: 

      ```http://localhost:8888/callback/```

5. Click on "SAVE".

6. Copy [the Client ID and the Secret ID](docs/imgs/20220211-185711.png) 

7. Open the *Spotify Data Retriever* app and past them in the [appropriate forms](docs/imgs/20220211-185826.png) 

8. Choose the options you like and press "START"

9. Profit(?)
