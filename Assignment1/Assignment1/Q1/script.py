import csv
import json
import time
import tweepy

# You must use Python 3.0 or above
# For those who have been using python 2.7.x before, here is an article explaining key differences between python 2.7x & 3.x
# http://sebastianraschka.com/Articles/2014_python_2_3_key_diff.html

# Rate limit chart for Twitter REST API - https://dev.twitter.com/rest/public/rate-limits

def loadKeys(key_file):
	# TODO: put in your keys and tokens in the keys.json file,
	#       then implement this method for loading access keys and token from keys.json
	# rtype: str <api_key>, str <api_secret>, str <token>, str <token_secret>
	with open(key_file) as data_file:    
		data = json.load(data_file)
	return data["api_key"],data["api_secret"],data["token"],data["token_secret"]

# Q1.b - 5 Marks
def getFollowers(api, root_user, no_of_followers):
	# TODO: implement the method for fetching 'no_of_followers' followers of 'root_user'
	# rtype: list containing entries in the form of a tuple (follower, root_user)
	#count=0
	FollowerList=[]
	try:
		for follower in tweepy.Cursor(api.followers, screen_name=root_user).items(no_of_followers):
		#if count < no_of_followers:
		#	count+=1
			FollowerList.append((follower.screen_name,root_user))
	except tweepy.error.RateLimitError:
		time.sleep(60*15)
		FollowerList=getFollowers(api, root_user, no_of_followers)
	return FollowerList
		#print (user.screen_name)

# Q1.b - 7 Marks
def getSecondaryFollowers(api, followers_list, no_of_followers):
	# TODO: implement the method for fetching 'no_of_followers' followers for each entry in followers_list
	# rtype: list containing entries in the form of a tuple (follower, followers_list[i])
	SecondaryFollowersList=[]
	try:
		for root_user in followers_list:
			for follower in tweepy.Cursor(api.followers,screen_name=root_user[0]).items(no_of_followers):
				SecondaryFollowersList.append((follower.screen_name,root_user[0]))
	except tweepy.error.RateLimitError:
		time.sleep(60*15)
		SecondaryFollowersList=getSecondaryFollowers(api, followers_list, no_of_followers)
	return SecondaryFollowersList


# Q1.c - 5 Marks
def getFriends(api, root_user, no_of_friends):
	# TODO: implement the method for fetching 'no_of_friends' friends of 'root_user'
	# rtype: list containing entries in the form of a tuple (root_user, friend)
	FriendsList=[]
	try:
		for friend in tweepy.Cursor(api.friends, screen_name=root_user).items(no_of_friends):
			FriendsList.append((root_user,friend.screen_name))
	except tweepy.error.RateLimitError:
		time.sleep(60*15)
		FriendsList=getFriends(api, root_user, no_of_friends)
	return FriendsList

# Q1.c - 7 Marks
def getSecondaryFriends(api, friends_list, no_of_friends):
	# TODO: implement the method for fetching 'no_of_friends' friends for each entry in friends_list
	# rtype: list containing entries in the form of a tuple (friends_list[i], friend)
	SecondaryFriendsList=[]
	try:
		for root_user in friends_list:
			for friend in tweepy.Cursor(api.friends,screen_name=root_user[1]).items(no_of_friends):
				SecondaryFriendsList.append((root_user[1],friend.screen_name))
	except tweepy.error.RateLimitError:
			time.sleep(60*15)
			SecondaryFriendsList=getSecondaryFriends(api, friends_list, no_of_friends)
	return SecondaryFriendsList

# Q1.b, Q1.c - 6 Marks
def writeToFile(data, output_file):
	# write data to output file
	# rtype: None
	with open(output_file,'w') as out:
		csv_out=csv.writer(out)
		for relation in data:
			csv_out.writerow(relation)   




"""
NOTE ON GRADING:

We will import the above functions
and use testSubmission() as below
to automatically grade your code.

You may modify testSubmission()
for your testing purposes
but it will not be graded.

It is highly recommended that
you DO NOT put any code outside testSubmission()
as it will break the auto-grader.

Note that your code should work as expected
for any value of ROOT_USER.
"""

def testSubmission():
	KEY_FILE = 'keys.json'
	OUTPUT_FILE_FOLLOWERS = 'followers.csv'
	OUTPUT_FILE_FRIENDS = 'friends.csv'

	ROOT_USER = 'PoloChau'
	NO_OF_FOLLOWERS = 10
	NO_OF_FRIENDS = 10


	api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)

	auth = tweepy.OAuthHandler(api_key, api_secret)
	auth.set_access_token(token, token_secret)
	api = tweepy.API(auth)
	print ("API is -----", api)
	primary_followers = getFollowers(api, ROOT_USER, NO_OF_FOLLOWERS)
	print ("The list of primary followers is as follows -\n")
	print (primary_followers)
	#print (primary_followers)
	

	secondary_followers = getSecondaryFollowers(api, primary_followers, NO_OF_FOLLOWERS)
	print ("The list of secondary followers is as follows-\n")
	print (secondary_followers)
	
	followers = primary_followers + secondary_followers
	
	#time.sleep(60*15)
	primary_friends = getFriends(api, ROOT_USER, NO_OF_FRIENDS)
	print ("The list of primary friends are - \n")
	print (primary_friends)
	
	secondary_friends = getSecondaryFriends(api, primary_friends, NO_OF_FRIENDS)
	print ("The list of secondary friends are -\n")
	print (secondary_friends)
	
	friends = primary_friends + secondary_friends
	
	writeToFile(followers, OUTPUT_FILE_FOLLOWERS)
	writeToFile(friends, OUTPUT_FILE_FRIENDS)
	"""
	user=api.get_user('lipu1108')
	#print (user.screen_name)
	#print (user.followers_count)
	#for friend in user.friends():
	#	print (friend.screen_name)
	"""
if __name__ == '__main__':
	testSubmission()

