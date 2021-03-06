import numpy as np
import svmImplementation as svm
MACRO_TIME_GAP = 1.4
MACRO_PLAYER_WON = 1
MACRO_PLAYER_LOST = 0
MACRO_PLAYER_ONE = 2
MACRO_PLAYER_TWO = 1
#
# function that seperates the team who won or lost
#
def seperateWinner(rawData):

	i = 0
	length = len(rawData)
	while( i < length):
		if rawData[i] == "":
			del rawData[i]
			length -= 1
		else:
			i+=1

	# converting in an np array
	rawData = np.array(rawData)
	rawData = rawData[np.argsort(rawData[:,0])]

	rawDataWin = [[]]
	rawDataLost = [[]]

	for element in rawData:

		if(element[-1] == MACRO_PLAYER_LOST):
			rawDataLost += [element]
		else:
			rawDataWin += [element]

	# getting the classification
	rawDataWin = np.array(rawDataWin[1:])
	rawDataLost = np.array(rawDataLost[1:])
	rawDataWin = rawDataWin[:,:-1]
	rawDataLost = rawDataLost[:,:-1]

	return rawDataWin, rawDataLost

#
# function that seperates the team who won or lost
#
def seperatePlayer(rawData):
	# converting in an np array
	rawData = np.array(rawData)
	rawData = rawData[np.argsort(rawData[:,0])]

	rawData1 = [[]]
	rawData2 = [[]]

	for element in rawData:

		if(element[-1] == MACRO_PLAYER_ONE):
			rawData1 += [element]
		else:
			rawData2 += [element]

	# getting the classification
	rawData1 = np.array(rawData1[1:])
	rawData2 = np.array(rawData2[1:])
	rawData1 = rawData1[:,:-1]
	rawData2 = rawData2[:,:-1]

	return rawData2, rawData1


#
# function that takes in raw data of zero hot vectors
# and converts it into svm
#
def callTrainSVM(rawData):

	rawDataWin, rawDataLost = seperateWinner(rawData)

	# retrieve winning and losing data
	xTrainData = [[]]
	yTranData = []

	seconds = 0
	temp = []
	winCounter = 0
	lossCounter = 0

	for element in rawDataWin:
		# group events into minutes, divide by time gap to get correct minute
		if( element[0]/MACRO_TIME_GAP >= seconds ) :
			if(temp != []):

				# updating x and y train data 
				temp[0] = seconds/60
				xTrainData += [temp]
				yTranData += [1]
				winCounter += 1

			# set a new temp and update seconds to move to next minute
			temp = element
			seconds += 60

		# if not a new minute
		else:
			for index in range(len(element)):
				# adding event to group of events
				temp[index] = temp[index] + element[index]

	# include last data into last minute and update
	temp[0] = seconds/60
	xTrainData += [temp]
	yTranData += [1]
	temp = []
	winCounter += 1

	# same as done for win set, but for loss set
	seconds = 0
	for element in rawDataLost:

		if( element[0]/MACRO_TIME_GAP >= seconds ) :
			if(temp != []):
				temp[0] = seconds/60
				xTrainData += [temp]
				yTranData += [0]
				lossCounter += 1
			temp = element
			seconds += 60

		# if not a new minute
		else:
			for index in range(len(element)):
				# adding stuff
				temp[index] = temp[index] + element[index]

	temp[0] = seconds/60
	xTrainData += [temp]
	yTranData += [0]
	lossCounter += 1

	if(winCounter != lossCounter):
		print "ERRROOORRRRR"
		return [],[]

	# remove first element of xTrainData due to initializing with an empty
	xTrainData = np.array(xTrainData[1:])
	# print xTrainData
	# print yTranData
	return xTrainData, yTranData


#
# function that takes in raw data of zero hot vectors
# and converts it into svm
#
def callTestSVM(rawData):

	rawData1, rawData2 = seperatePlayer(rawData)

	# retrieve winning and losing data
	xTrainData = [[]]

	seconds = 0
	temp = []


	for element in rawData1:
		# group events into minutes, divide by time gap to get correct minute
		if( element[0]/MACRO_TIME_GAP >= seconds ) :
			if(temp != []):

				# updating x and y train data 
				temp[0] = seconds/60
				xTrainData += [temp]

			# set a new temp and update seconds to move to next minute
			temp = element
			seconds += 60

		# if not a new minute
		else:
			for index in range(len(element)):
				# adding event to group of events
				temp[index] = temp[index] + element[index]

	# include last data into last minute and update
	temp[0] = seconds/60
	xTrainData += [temp]
	temp = []

	# same as done for win set, but for loss set
	seconds = 0
	for element in rawData2:

		if( element[0]/MACRO_TIME_GAP >= seconds ) :
			if(temp != []):
				temp[0] = seconds/60
				xTrainData += [temp]
			temp = element
			seconds += 60

		# if not a new minute
		else:
			for index in range(len(element)):
				# adding stuff
				temp[index] = temp[index] + element[index]

	temp[0] = seconds/60
	xTrainData += [temp]

	yOut1 = []
	yOut2 = []
	xTrainData = np.array(xTrainData[1:])

	for element in range(0,len(xTrainData)/2):
		if(element != 0):
			yOut1 += [svm.checkForWin(xTrainData[element], 'SVM/clfLinear.pkl') + yOut1[element - 1]]
		else:
			yOut1 += [svm.checkForWin(xTrainData[element], 'SVM/clfLinear.pkl')]

	for element in range(len(xTrainData)/2, len(xTrainData)):
		if((element - len(xTrainData)/2) != 0):
			yOut2 += [svm.checkForWin(xTrainData[element], 'SVM/clfLinear.pkl') + yOut2[(element - len(xTrainData)/2) - 1]]

		else:
			yOut2 += [svm.checkForWin(xTrainData[element], 'SVM/clfLinear.pkl')]
	
	# # remove first element of xTrainData due to initializing with an empty

	return yOut1, yOut2


def callTrainReplays(xTrainData, yTraindata):

	svm.trainReplays(xTrainData, yTraindata)



# a = [[1,1,1,1,1,2],[120,2,2,2,2,2],[45,2,2,2,2,2],[2,10,10,10,10,1], [49,10,10,10,10,1],[100,1,1,1,1,2],[101, 12,12,12,12,1]]
# b = [[1,2,2,2,2,1], [100,3,3,3,3,1], [1,11,11,11,11,2],[100,12,12,12,12,2]]
# xTrainData, yTraindata = callTrainSVM(a)
# svm.trainReplays(xTrainData, yTraindata)

# yOut1, yOut2 = callTestSVM(b)

