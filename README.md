# ambiance-backend

Service that interacts with Spotify API, pulls user data such as top tracks, saved tracks, and playlists to intelligently curating a ranked list of songs for a user or a group of users.\n
A user, or users, can now play this list, with our service automatically queueing more songs in the Spotify app, and always keeping a low amount in the queue (to allow the user to easily queue any songs he might want to).\n
A user can extract the list to a playlist in Spotify.\n
A user can use Playlist Live, a feature that creates a playlist in Spotify, and keeps track of any changes in users, or vibes, and updates the Playlist accordingly.
A user can define a Vibe to set the mood for the session. A vibe can be defined as a single track, or a playlist or album, where the average ranking of all songs will be used for the Vibe.\n
This application ranks songs based on the feature information Spotify provides. A user has a personalized profile, based on their top tracks, and then is compared to a large pool of tracks, which gets ranked and ordered based on the user. If there is a group of users in the session, the algorithm will find the best way to average everyone's profile, and order the large pool based on that.
