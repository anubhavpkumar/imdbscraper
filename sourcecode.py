## Python Code to get the Rating of an Input Movie
## Anubhav Kumar
## Sept 25. 2018

########################################################
import requests
from xml.dom.minidom import *
from bs4 import BeautifulSoup
import datetime
########################################################

def getMovieList(movieName):
	parameterLoad = movieName.lower().replace(" ","+")
	postUrl = "https://www.imdb.com/find?ref_=nv_sr_fn&q="+parameterLoad+"&s=tt"
	requestObject = requests.post(postUrl)
	sourceCode = requestObject.content
	fileObject = open("HTMLSouceCode.html","w+")
	fileObject.write(sourceCode)
	fileObject.close()
	soupObject = BeautifulSoup(sourceCode,'lxml')
	tableDataList = soupObject.find_all("td", class_="result_text")
	#print "Length = "+ str(len(tableList))
	#print "Type = "+ str(type(tableList[0]))
	tableDataTop10 = tableDataList[0:11]
	movieNames = []
	movieLinks = []
	for tableData in tableDataTop10 :
		tableDataChildren = list(tableData.children)
		tableDataAttribute = tableDataChildren[1]
		movieLink = tableDataAttribute['href']
		movieLinks.append(movieLink)
		movieName = tableData.get_text()
		movieNames.append(movieName)
	return [movieNames, list(movieLinks)]
	
def getImdbRatingFromUrl(Url):
	##/title/tt0395453/?ref_=fn_tt_tt_1
	postUrl = "https://www.imdb.com/"+Url
	requestObject = requests.post(postUrl)
	sourceCode = requestObject.content
	soupObject = BeautifulSoup(sourceCode , 'lxml')
	textDataTag = soupObject.find("div",class_="ratings_wrapper")
	textData  = textDataTag.get_text()
	textDataSplit = textData.split()
	if textDataSplit[0].lower() == "rate":
		return "N/A"
	else:
		return textDataSplit[0]






######################## Front End #########################
exceptionFileObject = open("Exception.log","a+")


while(1):
	imdbRating = "NULL"
	movieName = raw_input("Enter Movie Name to Search, \'q\' to quit: ")
	if movieName == "q":
		print "\n\n\nThank You For using this CLI Code"
		print "Coded By Anubhav Kumar"
		break
	if movieName.strip() == "":
		continue
	try:
		[movieList, movieLinks] = getMovieList(movieName)
	except Exception as e:
		dateTimeObject = datetime.datetime.now()
		errorString = str(dateTimeObject)+"getMovieList: "+movieName+":="+str(e)+"\n"
		exceptionFileObject.write(errorString)
	print "Probable Movie List are: "
	for i in range(0,len(movieList)):
		print str(i+1)+". "+movieList[i]
	while(True):
		try:
			movieNumber = input("Enter a Number to select the Movie (Enter 0 to search Another): ")
			if movieNumber == 0:
				break
		except NameError:
			print "Please Enter a Number"
		except Exception:
			print "Unknown Exception. Please contact the Developer at anu2anubhav@gmail.com"	
		try:	
			imdbRating = getImdbRatingFromUrl(movieLinks[movieNumber-1])
		except Exception as e:
			dateTimeObject = datetime.datetime.now()
			errorString = str(dateTimeObject)+"getImdbRatingFromUrl: "+"movieLinks["+str(movieNumber-1)+"]"+":="+str(e)+"\n"
			exceptionFileObject.write(errorString)
		print "IMDB Rating of the Movie is :"+str(imdbRating)

exceptionFileObject.close()
###########################################################
