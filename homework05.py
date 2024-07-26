import sqlite3
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances_argmin_min

conn = sqlite3.connect('/Users/maciewheeler/Downloads/Chinook_Sqlite.sqlite')
cursor = conn.cursor()

### Question 1

## Part a

cursor.execute("""
SELECT InvoiceId, CustomerId
FROM Invoice
ORDER BY Total DESC
LIMIT 15
""")

# print(cursor.fetchall())

## Part b

cursor.execute("""
SELECT e.FirstName, e.LastName
FROM Customer c
JOIN Employee e
ON e.FirstName = c.FirstName
""")

# print(cursor.fetchall())

## Part c

cursor.execute("""
SELECT e.FirstName, e.LastName
FROM Customer c
JOIN Employee e
ON e.LastName = c.LastName
""")

# print(cursor.fetchall())

## Part d

cursor.execute("""
SELECT g.Name
FROM Track t
JOIN Genre g
ON g.GenreId = t.GenreId
GROUP BY t.GenreId
ORDER BY COUNT(TrackId) DESC
LIMIT 1
""")

# print(cursor.fetchall())

## Part e

cursor.execute("""
SELECT c.FirstName, c.LastName
FROM InvoiceLine l
JOIN Invoice i
ON i.InvoiceId = l.InvoiceId
JOIN Customer c
ON c.CustomerId = i.CustomerId
GROUP BY i.CustomerId
ORDER BY COUNT(Quantity) DESC
LIMIT 5
""")

# print(cursor.fetchall())

## Part f

cursor.execute("""
SELECT art.Name, COUNT(AlbumId) as AlbumCounts
FROM Album al
JOIN Artist art
ON art.ArtistId = al.ArtistId
GROUP BY al.ArtistId
HAVING AlbumCounts > 5
""")

# print(cursor.fetchall())

## Part g

cursor.execute("""
SELECT DISTINCT art.Name, g.Name
FROM Genre g
JOIN Track t
ON t.GenreId = g.GenreId
JOIN Album al
ON al.AlbumId = t.AlbumId
JOIN Artist art
ON art.ArtistId = al.ArtistId
WHERE art.Name = 'Iron Maiden'
""")

# print(cursor.fetchall())

## Part h

cursor.execute("""
SELECT a.Title, COUNT(p.Name) as PlaylistCounts
FROM Playlist p
JOIN PlaylistTrack pt
ON pt.PlaylistId = p.PlaylistId
JOIN Track t
ON t.TrackId = pt.TrackId
JOIN Album a
ON a.AlbumId = t.AlbumId
GROUP BY t.AlbumId
HAVING PlaylistCounts > 5
""")

# print(cursor.fetchall())

### Question 2

## Part a

info = """
SELECT art.ArtistId, art.Name, al.AlbumId, al.Title, t.TrackId, t.Name, t.MediaTypeId, t.GenreId, t.Composer, t.Milliseconds,
 t.Bytes, t. UnitPrice, g.Name, pt.PlaylistId, p.Name
FROM Artist art
JOIN Album al
ON al.ArtistId = art.ArtistId
JOIN Track t
ON t.AlbumId = al.AlbumId
JOIN Genre g
ON g.GenreId = t.GenreId
JOIN PlaylistTrack pt
ON pt.TrackId = t.TrackId
JOIN Playlist p
ON p.PlaylistId = pt.PlaylistId
"""

# reading the SQL query into a dataframe
data = pd.read_sql_query(info, conn)

# creating new column names for the dataframe
data.columns = ['ArtistId', 'ArtistName', 'AlbumId', 'AlbumTitle', 'TrackId', 'TrackName', 'MediaTypeId', 'GenreId',
                'Composer', 'Milliseconds', 'Bytes', 'UnitPrice', 'GenreName', 'PlaylistId', 'PlaylistName']

# print(data)

## Part b

# getting the unique artist ids
unique_artists = data.ArtistId.unique()

# empty list for the artists that have more than one album
artists_more_than_one = []

# looping through each artist
for artist in unique_artists:
    # getting each artists unique album ids
    unique_album = (data.AlbumId[data.ArtistId == artist]).unique()
    # if the artist has more than one album add them to the empty list, else continue
    if len(unique_album) > 1:
        artists_more_than_one.append(artist)
    else:
        continue

# new data frame with only the artists that have more than one album
new_data = data[data.ArtistId.isin(artists_more_than_one)]

# print(new_data)

## Part c

# computing top 7 genres
cursor.execute("""
SELECT g.Name
FROM Track t
JOIN Genre g
ON g.GenreId = t.GenreId
GROUP BY t.GenreId
ORDER BY COUNT(TrackId) DESC
LIMIT 7
""")

# top 7 genres found using the SQL query
top_7 = cursor.fetchall()

# empty list for the top 7 genres
top_7_genres = []

# looping through each entry from the SQL query
for genre in top_7:
    # adding each genre to the list
    top_7_genres.append(genre[0])

# empty feature list for all of the artists combined
feature_list = []

# empty feature list for all of the artists combined with artist names
feature_list_with_artist_names = []

# looping through each artist to construct their 10 features
for a in artists_more_than_one:

    # data frame for each artist
    artist_data = new_data[new_data.ArtistId == a]

    # empty feature list for each artist
    artist_feature_list = []

    # empty feature list for each artist with artist names
    artist_feature_list_with_artist_names = []

    # appending the artist name to the feature list with artist names
    artist_feature_list_with_artist_names.append(artist_data.iloc[0, 1])

    # looping through each genre
    for genre in top_7_genres:
        # count of how many songs for each genre
        count_songs = (artist_data.TrackId[new_data.GenreName == genre]).unique()
        # adding the genre song counts to the artist's feature list
        artist_feature_list.append(len(count_songs))
        # adding the genre song counts to the artist's feature list with artist names
        artist_feature_list_with_artist_names.append(len(count_songs))

    # count of how many albums
    count_albums = (artist_data.AlbumId[artist_data.ArtistId == a]).unique()
    # adding album counts to the artist's feature list
    artist_feature_list.append(len(count_albums))
    # adding album counts to the artist's feature list with artist names
    artist_feature_list_with_artist_names.append(len(count_albums))

    # count of how many tracks
    count_tracks = (artist_data.TrackId[artist_data.ArtistId == a]).unique()
    # adding track counts to the artist's feature list
    artist_feature_list.append(len(count_tracks))
    # adding track counts to the artist's feature list with artist names
    artist_feature_list_with_artist_names.append(len(count_tracks))

    # count of how many playlist the artist appears in
    count_playlists = (artist_data.PlaylistId[artist_data.ArtistId == a]).unique()
    # adding playlist counts to the artist's feature list
    artist_feature_list.append(len(count_playlists))
    # adding playlist counts to the artist's feature list with artist names
    artist_feature_list_with_artist_names.append(len(count_playlists))

    # adding the artist's feature list to the feature list of all artists
    feature_list.append(artist_feature_list)

    # adding the artist's feature list to the feature list of all artists with names
    feature_list_with_artist_names.append(artist_feature_list_with_artist_names)

# creating a data frame for the feature list
feature_data = pd.DataFrame(feature_list, index=artists_more_than_one, columns=[top_7_genres[0], top_7_genres[1],
                            top_7_genres[2], top_7_genres[3], top_7_genres[4], top_7_genres[5], top_7_genres[6],
                            'NumberOfAlbums', 'NumberOfTracks', 'NumberOfPlaylists'])

# creating a data frame for the feature list with artist names
feature_data_with_artist_names = pd.DataFrame(feature_list_with_artist_names, index=artists_more_than_one,
                                              columns=['ArtistName', top_7_genres[0], top_7_genres[1], top_7_genres[2],
                                                       top_7_genres[3], top_7_genres[4], top_7_genres[5],
                                                       top_7_genres[6], 'NumberOfAlbums', 'NumberOfTracks',
                                                       'NumberOfPlaylists'])

# print(feature_data)
# print(feature_data_with_artist_names)

## Part d

# list of k points to plot
k_points = [2, 4, 6, 8, 10]
# empty list of inertia points to plot
inertia_points = []

# applying kmeans for k = 2
kmeans2 = KMeans(n_clusters=2)
kmeans2.fit(feature_data)
inertia2 = kmeans2.inertia_
inertia_points.append(inertia2)

# applying kmeans for k = 4
kmeans4 = KMeans(n_clusters=4)
kmeans4.fit(feature_data)
inertia4 = kmeans4.inertia_
inertia_points.append(inertia4)

# applying kmeans for k = 6
kmeans6 = KMeans(n_clusters=6)
kmeans6.fit(feature_data)
inertia6 = kmeans6.inertia_
inertia_points.append(inertia6)

# applying kmeans for k = 8
kmeans8 = KMeans(n_clusters=8)
kmeans8.fit(feature_data)
inertia8 = kmeans8.inertia_
inertia_points.append(inertia8)

# applying kmeans for k = 10
kmeans10 = KMeans(n_clusters=10)
kmeans10.fit(feature_data)
inertia10 = kmeans10.inertia_
inertia_points.append(inertia10)

# plotting inertia scores for each value of k
plt.scatter(k_points, inertia_points, color='orange')
plt.plot(k_points, inertia_points)
# plt.show()

## Part e

# copy of the feature data frame with artist names
copy_feature_data_with_artist_names = feature_data_with_artist_names

# copy of the feature data frame
copy_feature_data = feature_data

# resetting index of both the data frames and removing the new index column
copy_feature_data_with_artist_names = copy_feature_data_with_artist_names.reset_index()
copy_feature_data = copy_feature_data.reset_index()

copy_feature_data_with_artist_names = copy_feature_data_with_artist_names.drop(['index'], axis=1)
copy_feature_data = copy_feature_data.drop(['index'], axis=1)


# getting the centroids of each cluster (4 centroids, one for each cluster)
centers = kmeans4.cluster_centers_

# getting the labels for each artist, which cluster they belong in
labels = kmeans4.labels_


# list for first cluster
cluster_one = []
cluster_one_names = []

# list for second cluster
cluster_two = []
cluster_two_names = []

# list for third cluster
cluster_three = []
cluster_three_names = []

# list for fourth cluster
cluster_four = []
cluster_four_names = []


# count variable
c = 0

# looping through each cluster label for each artist
for cluster in labels:
    # adding the artist and their info to the cluster list they were assigned
    if cluster == 0:
        cluster_one.append(copy_feature_data.iloc[c, :])
        cluster_one_names.append(copy_feature_data_with_artist_names.iloc[c, :])
    elif cluster == 1:
        cluster_two.append(copy_feature_data.iloc[c, :])
        cluster_two_names.append(copy_feature_data_with_artist_names.iloc[c, :])
    elif cluster == 2:
        cluster_three.append(copy_feature_data.iloc[c, :])
        cluster_three_names.append(copy_feature_data_with_artist_names.iloc[c, :])
    elif cluster == 3:
        cluster_four.append(copy_feature_data.iloc[c, :])
        cluster_four_names.append(copy_feature_data_with_artist_names.iloc[c, :])

    # increasing the count variable by 1
    c = c + 1


# creating two data frames for cluster one, one with names, the other without
cluster_one_df = pd.DataFrame(cluster_one)
cluster_one_names_df = pd.DataFrame(cluster_one_names)

# resetting the index of the cluster one data frames and removing the index column
cluster_one_df = cluster_one_df.reset_index()
cluster_one_names_df = cluster_one_names_df.reset_index()

cluster_one_df = cluster_one_df.drop(['index'], axis=1)
cluster_one_names_df = cluster_one_names_df.drop(['index'], axis=1)

# creating two data frames for cluster two, one with names, the other without
cluster_two_df = pd.DataFrame(cluster_two)
cluster_two_names_df = pd.DataFrame(cluster_two_names)

# resetting the index of the cluster two data frames and removing the index column
cluster_two_df = cluster_two_df.reset_index()
cluster_two_names_df = cluster_two_names_df.reset_index()

cluster_two_df = cluster_two_df.drop(['index'], axis=1)
cluster_two_names_df = cluster_two_names_df.drop(['index'], axis=1)

# creating two data frames for cluster three, one with names, the other without
cluster_three_df = pd.DataFrame(cluster_three)
cluster_three_names_df = pd.DataFrame(cluster_three_names)

# resetting the index of the cluster three data frames and removing the index column
cluster_three_df = cluster_three_df.reset_index()
cluster_three_names_df = cluster_three_names_df.reset_index()

cluster_three_df = cluster_three_df.drop(['index'], axis=1)
cluster_three_names_df = cluster_three_names_df.drop(['index'], axis=1)

# creating two data frames for cluster four, one with names, the other without
cluster_four_df = pd.DataFrame(cluster_four)
cluster_four_names_df = pd.DataFrame(cluster_four_names)

# resetting the index of the cluster four data frames and removing the index column
cluster_four_df = cluster_four_df.reset_index()
cluster_four_names_df = cluster_four_names_df.reset_index()

cluster_four_df = cluster_four_df.drop(['index'], axis=1)
cluster_four_names_df = cluster_four_names_df.drop(['index'], axis=1)


# empty list for the 3 closest artists to the first centroid
closest_artists_cluster_one = []

# empty list for the 3 closest artists to the second centroid
closest_artists_cluster_two = []

# empty list for the 3 closest artists to the third centroid
closest_artists_cluster_three = []

# empty list for the 3 closest artists to the fourth centroid
closest_artists_cluster_four = []


# checking to see if the cluster one list has 3 or less artists assigned to it, if so return those, otherwise find top
# 3 closest artists to the centroid
if len(cluster_one) <= 3:
    for artist in cluster_one_names:
        closest_artists_cluster_one.append(artist)
else:
    # finding the first closest artist to the first centroid
    closest_one1, distances_one1 = pairwise_distances_argmin_min([centers[0]], cluster_one_df)
    # adding the first artist to the list for centroid one
    closest_artists_cluster_one.append(cluster_one_names_df.iloc[closest_one1[0], :])

    # removing the artist from the data frames for cluster one
    cluster_one_df = cluster_one_df.drop(closest_one1)
    cluster_one_names_df = cluster_one_names_df.drop(closest_one1)

    # resetting the index of both data frames and removing the index column
    cluster_one_df = cluster_one_df.reset_index()
    cluster_one_names_df = cluster_one_names_df.reset_index()

    cluster_one_df = cluster_one_df.drop(['index'], axis=1)
    cluster_one_names_df = cluster_one_names_df.drop(['index'], axis=1)

    # finding the second closest artist to the first centroid
    closest_one2, distances_one2 = pairwise_distances_argmin_min([centers[0]], cluster_one_df)
    # adding the second artist to the list for centroid one
    closest_artists_cluster_one.append(cluster_one_names_df.iloc[closest_one2[0], :])

    # removing the artist from the data frames for cluster one
    cluster_one_df = cluster_one_df.drop(closest_one2)
    cluster_one_names_df = cluster_one_names_df.drop(closest_one2)

    # resetting the index of both data frames and removing the index column
    cluster_one_df = cluster_one_df.reset_index()
    cluster_one_names_df = cluster_one_names_df.reset_index()

    cluster_one_df = cluster_one_df.drop(['index'], axis=1)
    cluster_one_names_df = cluster_one_names_df.drop(['index'], axis=1)

    # finding the third closest artist to the first centroid
    closest_one3, distances_one3 = pairwise_distances_argmin_min([centers[0]], cluster_one_df)
    # adding the second artist to the list for centroid one
    closest_artists_cluster_one.append(cluster_one_names_df.iloc[closest_one3[0], :])


# checking to see if the cluster two list has 3 or less artists assigned to it, if so return those, otherwise find top
# 3 closest artists to the centroid
if len(cluster_two) <= 3:
    for artist in cluster_two_names:
        closest_artists_cluster_two.append(artist)
else:
    # finding the first closest artist to the second centroid
    closest_two1, distances_two1 = pairwise_distances_argmin_min([centers[1]], cluster_two_df)
    # adding the first artist to the list for centroid two
    closest_artists_cluster_two.append(cluster_two_names_df.iloc[closest_two1[0], :])

    # removing the artist from the data frames for cluster two
    cluster_two_df = cluster_two_df.drop(closest_two1)
    cluster_two_names_df = cluster_two_names_df.drop(closest_two1)

    # resetting the index of both data frames and removing the index column
    cluster_two_df = cluster_two_df.reset_index()
    cluster_two_names_df = cluster_two_names_df.reset_index()

    cluster_two_df = cluster_two_df.drop(['index'], axis=1)
    cluster_two_names_df = cluster_two_names_df.drop(['index'], axis=1)

    # finding the second closest artist to the second centroid
    closest_two2, distances_two2 = pairwise_distances_argmin_min([centers[1]], cluster_two_df)
    # adding the second artist to the list for centroid two
    closest_artists_cluster_two.append(cluster_two_names_df.iloc[closest_two2[0], :])

    # removing the artist from the data frames for cluster two
    cluster_two_df = cluster_two_df.drop(closest_two2)
    cluster_two_names_df = cluster_two_names_df.drop(closest_two2)

    # resetting the index of both data frames and removing the index column
    cluster_two_df = cluster_two_df.reset_index()
    cluster_two_names_df = cluster_two_names_df.reset_index()

    cluster_two_df = cluster_two_df.drop(['index'], axis=1)
    cluster_two_names_df = cluster_two_names_df.drop(['index'], axis=1)

    # finding the third closest artist to the second centroid
    closest_two3, distances_two3 = pairwise_distances_argmin_min([centers[1]], cluster_two_df)
    # adding the second artist to the list for centroid two
    closest_artists_cluster_two.append(cluster_two_names_df.iloc[closest_two3[0], :])


# checking to see if the cluster three list has 3 or less artists assigned to it, if so return those, otherwise find top
# 3 closest artists to the centroid
if len(cluster_three) <= 3:
    for artist in cluster_three_names:
        closest_artists_cluster_three.append(artist)
else:
    # finding the first closest artist to the third centroid
    closest_three1, distances_three1 = pairwise_distances_argmin_min([centers[2]], cluster_three_df)
    # adding the first artist to the list for centroid three
    closest_artists_cluster_three.append(cluster_three_names_df.iloc[closest_three1[0], :])

    # removing the artist from the data frames for cluster three
    cluster_three_df = cluster_three_df.drop(closest_three1)
    cluster_three_names_df = cluster_three_names_df.drop(closest_three1)

    # resetting the index of both data frames and removing the index column
    cluster_three_df = cluster_three_df.reset_index()
    cluster_three_names_df = cluster_three_names_df.reset_index()

    cluster_three_df = cluster_three_df.drop(['index'], axis=1)
    cluster_three_names_df = cluster_three_names_df.drop(['index'], axis=1)

    # finding the second closest artist to the third centroid
    closest_three2, distances_three2 = pairwise_distances_argmin_min([centers[2]], cluster_three_df)
    # adding the second artist to the list for centroid three
    closest_artists_cluster_three.append(cluster_three_names_df.iloc[closest_three2[0], :])

    # removing the artist from the data frames for cluster three
    cluster_three_df = cluster_three_df.drop(closest_three2)
    cluster_three_names_df = cluster_three_names_df.drop(closest_three2)

    # resetting the index of both data frames and removing the index column
    cluster_three_df = cluster_three_df.reset_index()
    cluster_three_names_df = cluster_three_names_df.reset_index()

    cluster_three_df = cluster_three_df.drop(['index'], axis=1)
    cluster_three_names_df = cluster_three_names_df.drop(['index'], axis=1)

    # finding the third closest artist to the third centroid
    closest_three3, distances_three3 = pairwise_distances_argmin_min([centers[2]], cluster_three_df)
    # adding the second artist to the list for centroid one
    closest_artists_cluster_three.append(cluster_three_names_df.iloc[closest_three3[0], :])


# checking to see if the cluster four list has 3 or less artists assigned to it, if so return those, otherwise find top
# 3 closest artists to the centroid
if len(cluster_four) <= 3:
    for artist in cluster_four_names:
        closest_artists_cluster_four.append(artist)
else:
    # finding the first closest artist to the fourth centroid
    closest_four1, distances_four1 = pairwise_distances_argmin_min([centers[3]], cluster_four_df)
    # adding the first artist to the list for centroid four
    closest_artists_cluster_four.append(cluster_four_names_df.iloc[closest_four1[0], :])

    # removing the artist from the data frames for cluster four
    cluster_four_df = cluster_four_df.drop(closest_four1)
    cluster_four_names_df = cluster_four_names_df.drop(closest_four1)

    # resetting the index of both data frames and removing the index column
    cluster_four_df = cluster_four_df.reset_index()
    cluster_four_names_df = cluster_four_names_df.reset_index()

    cluster_four_df = cluster_four_df.drop(['index'], axis=1)
    cluster_four_names_df = cluster_four_names_df.drop(['index'], axis=1)

    # finding the second closest artist to the fourth centroid
    closest_four2, distances_four2 = pairwise_distances_argmin_min([centers[3]], cluster_four_df)
    # adding the second artist to the list for centroid four
    closest_artists_cluster_four.append(cluster_four_names_df.iloc[closest_four2[0], :])

    # removing the artist from the data frames for cluster four
    cluster_four_df = cluster_four_df.drop(closest_four2)
    cluster_four_names_df = cluster_four_names_df.drop(closest_four2)

    # resetting the index of both data frames and removing the index column
    cluster_four_df = cluster_four_df.reset_index()
    cluster_four_names_df = cluster_four_names_df.reset_index()

    cluster_four_df = cluster_four_df.drop(['index'], axis=1)
    cluster_four_names_df = cluster_four_names_df.drop(['index'], axis=1)

    # finding the third closest artist to the fourth centroid
    closest_four3, distances_four3 = pairwise_distances_argmin_min([centers[3]], cluster_four_df)
    # adding the second artist to the list for centroid four
    closest_artists_cluster_four.append(cluster_four_names_df.iloc[closest_four3[0], :])


# print(closest_artists_cluster_one)
# print(closest_artists_cluster_two)
# print(closest_artists_cluster_three)
# print(closest_artists_cluster_four)
