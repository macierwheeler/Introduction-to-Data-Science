import pandas as pd
import numpy as np
from sklearn import *
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD

#### Question 1

# reading in the dataframe
rating_final = pd.read_csv('/Users/maciewheeler/Downloads/rating_final.csv')

# creating the user ratings data frame with users as rows and restaurants as columns
user_restaurant_ratings_df = pd.pivot_table(rating_final, index='userID', values='rating', columns='placeID')

# getting rid of placeID row name
user_restaurant_ratings_df.columns.name = None
# resetting index so the table lines up
user_restaurant_ratings_df = user_restaurant_ratings_df.reset_index(0)

# filling na values with 0s
user_restaurant_ratings_df = user_restaurant_ratings_df.fillna(0)

# remove userID column
user_restaurant_ratings_df = user_restaurant_ratings_df.drop(columns=['userID'])

# convert the data frame to a user ratings matrix
user_restaurant_ratings_matrix = user_restaurant_ratings_df.to_numpy()
# print(user_restaurant_ratings_matrix)

# code to find the most common entry in the matrix

# gets the mode of each row in the data frame
modes = user_restaurant_ratings_df.mode(axis=1)
# finds the counts of the modes for each row
mode_counts = modes.value_counts()
# print(mode_counts)

#### Question 2

### Part a

# transposing the user ratings matrix
transposed_user_restaurant_ratings_matrix = np.transpose(user_restaurant_ratings_matrix)
# mean centering the data
mean_centered = preprocessing.scale(transposed_user_restaurant_ratings_matrix, with_std=False)

### Part b

# getting PCA model with k = 2 components
pca = decomposition.PCA(n_components=2)

# applying the PCA model to the mean centered data
fitted = pca.fit_transform(mean_centered)

# plotting the new representation of the restaurants
plt.scatter(fitted[:, 0], fitted[:, 1])
# plt.show()

### Part c

# getting the percentage of variance explained by each of the first two components
variances = pca.explained_variance_ratio_
# print(variances)

### Part d

# ran different PCA models with different k values to find the number of components needed to explain 80% of the
# variance of the data
pca2 = decomposition.PCA(n_components=36)
fitted2 = pca2.fit_transform(mean_centered)
variances2 = pca2.explained_variance_ratio_
# print(sum(variances2))

#### Question 3

### Part a

# list of k points to plot
k_points = [2, 4, 8, 16, 32]
# empty list of inertia points to plot
inertia_points = []

# applying kmeans for k = 2, measuring inertia for each value of k, and adding the inertia point to the list
kmeans2 = KMeans(n_clusters=2)
kmeans2.fit(transposed_user_restaurant_ratings_matrix)
inertia2 = kmeans2.inertia_
inertia_points.append(inertia2)

# applying kmeans for k = 4, measuring inertia for each value of k, and adding the inertia point to the list
kmeans4 = KMeans(n_clusters=4)
kmeans4.fit(transposed_user_restaurant_ratings_matrix)
inertia4 = kmeans4.inertia_
inertia_points.append(inertia4)

# applying kmeans for k = 8, measuring inertia for each value of k, and adding the inertia point to the list
kmeans8 = KMeans(n_clusters=8)
kmeans8.fit(transposed_user_restaurant_ratings_matrix)
inertia8 = kmeans8.inertia_
inertia_points.append(inertia8)

# applying kmeans for k = 16, measuring inertia for each value of k, and adding the inertia point to the list
kmeans16 = KMeans(n_clusters=16)
kmeans16.fit(transposed_user_restaurant_ratings_matrix)
inertia16 = kmeans16.inertia_
inertia_points.append(inertia16)

# applying kmeans for k = 32, measuring inertia for each value of k, and adding the inertia point to the list
kmeans32 = KMeans(n_clusters=32)
kmeans32.fit(transposed_user_restaurant_ratings_matrix)
inertia32 = kmeans32.inertia_
inertia_points.append(inertia32)

# plotting inertia scores for each k
plt.scatter(k_points, inertia_points, color='orange')
plt.plot(k_points, inertia_points)
# plt.show()

#### Question 4

### Part a

# getting SVD model with k = 32 components
svd = TruncatedSVD(n_components=32)

# applying the SVD model to the transposed user ratings matrix
fitted = svd.fit(transposed_user_restaurant_ratings_matrix)

# getting the singular values of the SVD fitted user ratings matrix
values = svd.singular_values_

# plotting the singular values
plt.scatter(range(0, 32), values)
# plt.show()

### Part b

# list of k points to plot
k_points_svd = [2, 4, 8, 16, 32]
# empty list of variance points
variance_points = []

# applying SVD with k = 2 components, measuring the sum of explained variance ratios, and adding the variance point to
# the list
svd2 = TruncatedSVD(n_components=2)
fittedvariances2 = svd2.fit(transposed_user_restaurant_ratings_matrix)
svdvariances2 = sum(svd2.explained_variance_ratio_)
variance_points.append(svdvariances2)

# applying SVD with k = 4 components, measuring the sum of explained variance ratios, and adding the variance point to
# the list
svd4 = TruncatedSVD(n_components=4)
fittedvariances4 = svd4.fit(transposed_user_restaurant_ratings_matrix)
svdvariances4 = sum(svd4.explained_variance_ratio_)
variance_points.append(svdvariances4)

# applying SVD with k = 8 components, measuring the sum of explained variance ratios, and adding the variance point to
# the list
svd8 = TruncatedSVD(n_components=8)
fittedvariances8 = svd8.fit(transposed_user_restaurant_ratings_matrix)
svdvariances8 = sum(svd8.explained_variance_ratio_)
variance_points.append(svdvariances8)

# applying SVD with k = 16 components, measuring the sum of explained variance ratios, and adding the variance point to
# the list
svd16 = TruncatedSVD(n_components=16)
fittedvariances16 = svd16.fit(transposed_user_restaurant_ratings_matrix)
svdvariances16 = sum(svd16.explained_variance_ratio_)
variance_points.append(svdvariances16)

# applying SVD with k = 32 components, measuring the sum of explained variance ratios, and adding the variance point to
# the list
svd32 = TruncatedSVD(n_components=32)
fittedvariances32 = svd32.fit(transposed_user_restaurant_ratings_matrix)
svdvariances32 = sum(svd32.explained_variance_ratio_)
variance_points.append(svdvariances32)

# plotting variances for each k
plt.scatter(k_points_svd, variance_points, color='orange')
plt.plot(k_points_svd, variance_points)
# plt.show()

### Part c

# getting SVD model with k = 2 components
svd2 = TruncatedSVD(n_components=2)

# applying the SVD model to the transposed user ratings matrix
fitted_and_transformed = svd.fit_transform(transposed_user_restaurant_ratings_matrix)

### Part d

# cluster membership for color
labels = kmeans16.labels_

# plotting the SVD results for k = 16 components
plt.scatter(fitted_and_transformed[:, 0], fitted_and_transformed[:, 1], c=labels)
# plt.show()
