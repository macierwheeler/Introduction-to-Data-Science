import re
import time

#### Question 1

### Part 1.1

## Part a

# start time for the program
start_time_hashtag = time.time()

# mapper function
def mapper_hashtag(filename):

    # opening the file
    file = open(filename)
    # reading the file and splitting by tabs
    lines = file.read().split('\t')

    # pattern to find all hashtags with alphanumeric characters after them
    pattern = re.compile('#\w+')

    # empty list for all the hashtag words
    hashtag_list = []

    # looping through each line of the file
    for line in lines:
        # getting everything in the line that matches the hashtag pattern
        hashtags = re.findall(pattern, line)

        # if the pattern found nothing continue, else add the found hashtag words to the hashtag list
        if len(hashtags) == 0:
            continue
        else:
            # looping through each hashtag word found
            for hashtag in hashtags:
                # making each hashtag word lowercase
                lowercase_hashtag = hashtag.lower()
                # adding that hashtag word to the hashtag list
                hashtag_list.append(lowercase_hashtag)

    # returning each hashtag word as a tuple with the number 1
    return [(hash, 1) for hash in hashtag_list]


# combiner function
def combiner_hashtag(mapper_output):

    # empty dictionary for the combined hashtag word counts
    combined_hashtag_counts = {}

    # looping through each hashtag, count tuple in the mapper output
    for hashtag, count in mapper_output:
        # if the hashtag is already in the dictionary, append the count to the value list, else add the hashtag
        # and its count value as a list
        if hashtag in combined_hashtag_counts:
            combined_hashtag_counts[hashtag].append(count)
        else:
            combined_hashtag_counts[hashtag] = [count]

    # returning the dictionary of combined hashtag word counts
    return combined_hashtag_counts


# reducer function
def reducer_hashtag(hashtag, listofcounts):

    # summing the list of counts for the hashtag
    sum_counts = sum(listofcounts)

    # return the hashtag and its sum of counts for that hashtag
    return (hashtag, sum_counts)


# execute function
def execute_hashtag(filename):

    # getting the dictionary of combined hashtag counts
    combined_hashtag_counts = combiner_hashtag(mapper_hashtag(filename))

    # creating a list from the combined hashtag counts
    list_combined_hashtag_counts = list(combined_hashtag_counts.items())

    # empty list for the final hashtag output
    hashtag_output = []

    # looping through each item in the combined hashtag counts list
    for word, count in list_combined_hashtag_counts:
        # getting the reduced hashtag counts
        reduced_word_count = reducer_hashtag(word, count)
        # adding the reduced hashtag counts to the final hashtag output
        hashtag_output.append(reduced_word_count)

    # sorting the hashtag output by highest occurence to lowest occurence
    hashtag_output.sort(key=lambda x: x[1], reverse= True)

    # returning the top ten occuring hashtags
    return hashtag_output[0:10]


# running the map-reduce to accomplish the task for hashtags
# print(execute_hashtag('/Users/maciewheeler/Downloads/tweets.tsv'))

# finding the run time in seconds of my program for hashtags
end_time_hashtag = time.time() - start_time_hashtag
# print(end_time_hashtag)


### Part 1.2

## Part a

# start time for the program
start_time_username = time.time()

# mapper function
def mapper_username(filename):

    # opening the file
    file = open(filename)
    # reading the file and splitting by tabs
    lines = file.read().split('\t')

    # pattern to find all '@' signs with alphanumeric characters after them (usernames)
    pattern = re.compile('@\w+')

    # empty list for all the username words
    username_list = []

    # looping through each line of the file
    for line in lines:
        # getting everything in the line that matches the username pattern
        usernames = re.findall(pattern, line)

        # if the pattern found nothing continue, else add the found username to the username list
        if len(usernames) == 0:
            continue
        else:
            # looping through each username found
            for username in usernames:
                # making each username word lowercase
                lowercase_username = username.lower()
                # adding that username to the username list
                username_list.append(lowercase_username)

    # returning each username as a tuple with the number 1
    return [(user, 1) for user in username_list]


# combiner function
def combiner_username(mapper_output):

    # empty dictionary for the combined username counts
    combined_username_counts = {}

    # looping through each username, count tuple in the mapper output
    for username, count in mapper_output:
        # if the username is already in the dictionary, append the count to the value list, else add the username
        # and its count value as a list
        if username in combined_username_counts:
            combined_username_counts[username].append(count)
        else:
            combined_username_counts[username] = [count]

    # returning the dictionary of combined username counts
    return combined_username_counts


# reducer function
def reducer_username(username, listofcounts):

    # summing the list of counts for the username
    sum_counts = sum(listofcounts)

    # return the username and its sum of counts for that username
    return (username, sum_counts)


# execute function
def execute_username(filename):

    # getting the dictionary of combined username counts
    combined_username_counts = combiner_username(mapper_username(filename))

    # creating a list from the combined username word counts
    list_combined_username_counts = list(combined_username_counts.items())

    # empty list for the final username output
    username_output = []

    # looping through each item in the combined username counts list
    for word, count in list_combined_username_counts:
        # getting the reduced username counts
        reduced_word_count = reducer_username(word, count)
        # adding the reduced username counts to the final username output
        username_output.append(reduced_word_count)

    # sorting the username output by highest occurence to lowest occurence
    username_output.sort(key=lambda x: x[1], reverse= True)

    # returning the top ten occuring usernames
    return username_output[0:10]


# running the map-reduce to accomplish the task for usernames
# print(execute_username('/Users/maciewheeler/Downloads/tweets.tsv'))

# finding the run time in seconds of my program for usernames
end_time_username = time.time() - start_time_username
# print(end_time_username)


#### Question 2

## Part a

# start time for the program
start_time_followers = time.time()

# mapper function
def mapper_followers(filename):

    # opening the file
    file = open(filename)
    # reading the file
    lines = file.read().split()

    # empty list for the tuples of the user and the user they're following
    user_following = []

    # looping through each line in the file
    for line in lines:
        # splitting the line by a comma
        split_line = line.split(',')
        # adding the user before the comma and the user that they're following after the comma to a tuple
        user_following_tuple = (int(split_line[0]), int(split_line[1]))
        # adding the tuple to a list of all the tuples
        user_following.append(user_following_tuple)

    # returning each user and the user they're following
    return user_following


# combiner function
def combiner_followers(mapper_output):

    # empty dictionary for the users and their list of users they're following
    combined_user_following = {}

    # looping through each user, user following tuple in the mapper output
    for user, following in mapper_output:
        # if the user is already in the dictionary, append the following user to the value list, else add the user
        # and its following user as a list
        if user in combined_user_following:
            combined_user_following[user].append(following)
        else:
            combined_user_following[user] = [following]

    # returning the dictionary users and their list of users they're following
    return combined_user_following


# reducer function
def reducer_followers(user1, user2):

    # checking if user 1 follows user 2 and user 2 follows user 1, and returning a tuple of their following relation
    if user1[0] in user2[1] and user2[0] in user1[1]:
        return [user1[0], user2[0]]


# execute function
def execute_followers(filename):

    # getting the dictionary of users and their list of users they're following
    combined_user_following = combiner_followers(mapper_followers(filename))

    # empty list for the users and their list of users they're following
    combined_user_following_list = []

    # converting the dictionary into a list of tuples
    for key, value in combined_user_following.items():
        combined_user_following_list.append((key, value))

    # empty list for mutual followers
    mutual_followers = []

    # a double for loop to run through each pair of users and the people they're following
    for i in combined_user_following_list:
        for j in combined_user_following_list:
            # if the pair of users are mutual followers then add them to the list, otherwise continue
            pairs = reducer_followers(i, j)
            if pairs is None:
                continue
            else:
                mutual_followers.append(pairs)

    # returning the list of mutual followers
    return mutual_followers


# running the map-reduce to accomplish the task of finding mutual followers
mutual_followers = execute_followers('/Users/maciewheeler/Downloads/edges.csv')
# print(mutual_followers)
# print(len(mutual_followers))

# finding the run time in seconds of my program for finding mutual followers
end_time_followers = time.time() - start_time_followers
# print(end_time_followers)

# writing the mutual followers to a new file
# creating the new file
f = open('/Users/maciewheeler/Downloads/edges.txt', 'w')

# looping through each mutual follower pair
for pair in mutual_followers:
    # writing the pairs to the file, each on a separate line
    f.write(str(pair[0]) + "," + str(pair[1]) + "\n")

# closing the file
f.close()

# finding number of unique nodes for the old edges.csv file
# opening the file
file_old = open('/Users/maciewheeler/Downloads/edges.csv')
# reading the file
lines_old = file_old.read().split()

# empty list for each user
users_old = []

# looping through each line
for line_old in lines_old:
    split_line_old = line_old.split(',')
    users_old.append(split_line_old[0])
    users_old.append(split_line_old[1])

# getting the number of unique users
unique_old = set(users_old)
# print(len(unique_old))

# closing the file
file_old.close()

# finding number of unique nodes for the new file
# opening the file
file_new = open('/Users/maciewheeler/Downloads/edges.txt')
# reading the file
lines_new = file_new.read().split()

# empty list for each user
users_new = []

# looping through each line
for line_new in lines_new:
    split_line_new = line_new.split(',')
    users_new.append(split_line_new[0])
    users_new.append(split_line_new[1])

# getting the number of unique users
unique_new = set(users_new)
# print(len(unique_new))

# closing the file
file_new.close()

#### Question 3

## Part a

# mapper function
def mapper_friends(filename):

    # opening the file
    file = open(filename)
    # reading the file
    lines = file.read().split()

    # empty list for all the user following pairs
    user_following_list = []

    # looping through each pair
    for line in lines:

        # splitting the line by a comma
        split_line = line.split(',')
        # adding the user before the comma and the user that they're following after the comma to a tuple
        user_following_tuple = (int(split_line[0]), int(split_line[1]))

        # appending the pair to the list
        user_following_list.append(user_following_tuple)

    # emtpy dictionary for the users and the list of users they're following
    user_following = {}

    # looping through each user, user following tuple in the mapper output
    for u, f in user_following_list:
        # if the user is already in the dictionary, append the following user to the value list, else add the user
        # and its following user as a list
        if u in user_following:
            user_following[u].append(f)
        else:
            user_following[u] = [f]

    # returning the user following dictionary
    return user_following


# combiner function
def combiner_friends(mapper_output):

    # empty dictionary for paired users and their combined user following lists
    paired_following = {}

    # looping through each element of the dictionary from the mapper output
    for key, value in mapper_output.items():
        # creating a key based on two users, the smallest being the first in the key
        for v in value:
            if key < v:
                pair = (key, v)
            else:
                pair = (v, key)

            # checking if the pair key is already in the dictionary, if it is append the list of people the user pair is
            # following to the values list, else add the pair of users and the following list as a list
            if pair in paired_following:
                paired_following[pair].append(value)
            else:
                paired_following[pair] = [value]

    # returning the paired users and combined following list dictionary
    return paired_following


# reducer function
def reducer_friends(pair):

    # empty variable for the number of common friends the two users have
    count = 0

    # variable for the key
    key = pair[0]

    # variable for the values
    values = pair[1]

    # looping through the following lists for each user
    for v1 in values[0]:
        for v2 in values[1]:
            # if the two user's friend lists have a friend in common add one to the count
            if v1 == v2:
                count = count + 1

    # returning the user pair and the number of common friends they have
    return key, count


# reducer function
def execute_friends(filename):

    # getting the dictionary of the pairs and their combined user following lists
    paired_following = combiner_friends(mapper_friends(filename))

    # empty list for the pairs and their combined user following lists
    paired_following_list = []

    # looping through each pair and their combined lists
    for pair, lists in paired_following.items():
        # making a list to add to the list
        l = [pair, lists]
        # appending the list to the paired following list
        paired_following_list.append(l)

    # empty list for the output of pairs and the count of friends they had in common
    common_friends_output = []

    # looping through each pair and their combined lists
    for pair in paired_following_list:
        # getting the pair and the number of their common friends
        common_friends_count = reducer_friends(pair)
        # appending this pair and their common friend count to the list
        common_friends_output.append(common_friends_count)

    # sorting the pairs of friends by the lowest key pair
    common_friends_output.sort(key=lambda x: x[0])

    # sorting the pairs of friends by highest number of common friends
    common_friends_output.sort(key=lambda x: x[1], reverse= True)

    # returning the top ten pairs of friends with the most number of friends in common
    return common_friends_output[0:10]


# running the map-reduce to accomplish the task of friends in common
# print(execute_friends('/Users/maciewheeler/Downloads/edges.txt'))
