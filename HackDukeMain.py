from facepy import GraphAPI
import statistics
import math
# import numpy
from tkinter import *

ACCESS_TOKEN = "HIDDEN"


# Code used to pull a certain post's message, name, and likes
# 10203826343832506_10206167857488884/?fields=message,name,likes

# Code used to pull a certain post's link and the picture associated with the link:
# 10203826343832506_10206128557826417/?fields=link
graph = GraphAPI(ACCESS_TOKEN)

class Post:
	"""takes inputs message, likes, comments, and link bool"""
	def __init__(self, message, likes, comments, link):
		self.message = message
		self.likes = likes
		self.comments = comments
		self.link = link

	def __str__(self):
		return self.message 

def getPosts():
	# Need to figure out how to use the generator here to get last 100 posts
	posts = graph.get('me/posts?limit=100', page=False)
	# Posts return two variable: paging and data
	return posts["data"]

def getLikes(post):
	# Code needed to pull number of likes from posts variable
	if "likes" in list(post.keys()):
		# print(post.keys())
		newLikes = graph.get(('{}/likes?limit=999').format(post['id']))
		# theSum = 0
		# nextLikes = post['likes']
		# while "next" in nextLikes.keys():
		# 	nextLikes = graph.get(nextLikes['next'], page=False)
		# 	theSum += len(nextLikes['data'])
		return len(newLikes['data'])
		# return len(post['likes']['data'])
	else:
		return 0

def getComments(post):
	# Code needed to pull the number of comments from posts variable

	if "comments" in list(post.keys()):
		# theSum = 0
		# while "next" in post['comments'].keys():
			# nextComments = graph.get(post['comments']['next'], page=False)
			# theSum += len(nextComments['data'])
		return len(post['comments']['data'])
		# ACTIVATE THESE LINES IF YOU EXPECT TO HAVE +25 COMMENTS ON A POST
		# newComments = graph.get(('{}/comments?limit=999').format(post['id']))
		# return len(newComments['data'])
	else:
		return 0

def hasLink(post):
	if "link" in list(post.keys()):
		return True
	else:
		return False

def getMessage(post):
	# Code need to get the message from a post
	if "message" in list(post.keys()):
		return post['message']

def getAnalysis(postList, item):
	theSum = 0
	dataList = []
	if item == "likes":
		for each in postList:
			dataList.append(each.likes)
	elif item == "comments":
		for each in postList:
			dataList.append(each.comments)
	else:
		return 0
	return {'mean': statistics.mean(dataList),
		# 'median': numpy.percentile(dataList, 50),
		# 'lowerQ': numpy.percentile(dataList, 25),
		# 'higherQ': numpy.percentile(dataList, 75),
		# 'mode': statistics.mode(dataList),
		'variance': statistics.variance(dataList),
		'max': max(dataList),
		'min': min(dataList)}

def constructPostList():
	posts = getPosts()
	postList = []

	for each in posts:
		postList.append(Post(getMessage(each),
 			getLikes(each), getComments(each),
 			hasLink(each)))
	return postList

class GUI:
	def __init__(self, window):
		self.win = window

		headerFrame = Frame(self.win)
		headerFrame.pack()
		Label(headerFrame, text="Welcome to the Facebook Posts Manager").pack()
		startButton = Button(headerFrame, text="Check my Facebook", command=self.loadData)
		startButton.pack()


	def loadData(self):
		self.postList = constructPostList()

		likeMetrics = getAnalysis(self.postList, "likes")
		commentMetrics = getAnalysis(self.postList, "comments")
		
		statsFrame = Frame(self.win)
		statsFrame.pack()

		Label(statsFrame, text=("Average Likes: " + str(likeMetrics["mean"]))).pack()
		Label(statsFrame, text=("Average Comments: " + str(commentMetrics["mean"]))).pack()

		scrollbar = Scrollbar(window)
		scrollbar.pack(side=RIGHT, fill=Y)

		text = Text(window, wrap=WORD, yscrollcommand=scrollbar.set)
		text.tag_config("g", foreground="green")
		text.tag_config("r", foreground="red")
		

		color = ""

		for each in self.postList:
			if each.message == None:
				each.message = "N/A"
			text.insert(END, each.message + "\n")
			if each.likes >= likeMetrics["mean"]:
				color = 'g'
			else:
				color = 'r'
			text.insert(END, "Likes: " + str(each.likes) + "\n", color)
			if each.comments >= commentMetrics["mean"]:
				color = 'g'
			else:
				color = 'r'
			text.insert(END, "Comments: " 
				+ str(each.comments) 
				+ "\n\n", color) 
		text.pack(side=LEFT, fill=BOTH)

		scrollbar.config(command=text.yview)

window = Tk()
GUI(window)
window.mainloop()


posts = getPosts()
postList = []

# for each in posts:
# 	postList.append(Post(getMessage(each),
# 		getLikes(each), getComments(each),
# 		hasLink(each)))

# print(getAnalysis(postList, "likes"))
# print(getAnalysis(postList, "comments"))

# TESTING ######################
# posts = getPosts()

# for each in posts:
# 	print(getMessage(each),"\n", 
# 	getLikes(each), "\n", 
# 	getComments(each), "\n",
# 	hasLink(each), "\n")

# posts = constructPostList()

# print(posts[0])
# print(list(posts[3].keys()))
# print(posts[3]['object_id'])

# print(posts[3]['likes'])

# print(getLikes(posts[0]))
# print(getComments(posts[0]))
# print(getMessage(posts[0]))
# print(hasLikes(posts[0]))
# print(hasComments(posts[0]))

print("done")

