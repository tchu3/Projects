## IMPORTS SECTION ##
import numpy
import pandas

import nltk
import xlwings
import re

from nltk.corpus import wordnet as guru
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.util import ngrams

# Function Definitions
ps = PorterStemmer()
lem = WordNetLemmatizer()
en_stops = set(stopwords.words('english'))

brokenRodWords = ["break","broken","prorod","rod"]
corrosionWords = ["corrosion","visual","minor", "signs", "major"]

def lookForBreak():
	## Defining XLWings file formats to connect to Excel ##
	ws = xlwings.Book('RodBreakAnalysis.xlsx')
	EOJSheet = ws.sheets['Data Dump']

	## VARIABLE DECLARATIONS ##
	counter = 2

	while EOJSheet.range(counter, 1).value is not None:

		## LIST DECLARATIONS ##
		commentDictionary = []
		filteredDictionary = []
		lemDictionary = []
		rootCauseDictionary = []
		valuesDictionary = []
		frequencyDictionary = {}

		## FLAG DECLARATIONS ##
		foundBreak = False
		foundCorrosion = False
		currentRodBreakDepth = "N/A"

        # Get string
		currentEOJString = EOJSheet.range(counter, 12).value

		### NOISE REMOVAL ###

		# Remove punctuation
		currentEOJString = re.sub('[@&?()/:~,.-]', ' ', currentEOJString)
		currentEOJString = " ".join(currentEOJString.split())
		# Lowercase all words
		currentEOJString = currentEOJString.lower()
		## Tokenize the paragraph
		# commentDictionary = sent_tokenize(currentEOJString)
		commentDictionary = word_tokenize(currentEOJString)
		# Remove stop words
		commentDictionary = [i for i in commentDictionary if not i in en_stops]
		# print(commentDictionary)
		# Lemmatize the all the words
		#for i in commentDictionary:
		#	stemmedDictionary.append(ps.stem(i))
		for i in commentDictionary:
			lemDictionary.append(lem.lemmatize(i,"v"))

		# Trim the root cause dictionary down to only alpha characters and measurements to alphanumeric characters
		rootCauseDictionary = [word.lower() for word in lemDictionary if word.isalpha()]
		valuesDictionary = [word.lower() for word in lemDictionary if not word.isalpha()]
		print(valuesDictionary)

		# Get word count frequencyDictionary
		for key in rootCauseDictionary:
			frequencyDictionary[key] = frequencyDictionary.get(key, 0) + 1
		sorted(frequencyDictionary.items(), key = lambda x: x[1], reverse = True)

		# Create trigrams of the rootCauseDictionary -> alphabetic words ONLY
		rootCauseTrigrams = list(ngrams(rootCauseDictionary,3))
		# Create trigrams of the lemmatized dictionary -> to find the break
		lemGrams = list(ngrams(lemDictionary, 4))

		# temporary print functions to see data
		#print(lemDictionary)
		print(lemGrams)

		# Iterate through trigrams to search for keywords indicated a rod break
		# Keywords = prorod, rod, break
		for i in range(0,len(lemGrams)):
			# Initialize counters
			rodCounter = 0
			corrosionCounter = 0
			for j in range(0,4):
				# Initialize counters
				depthCounter = 0
				# if two keywords are found check to see if the third is the break depth
				if rodCounter >= 2:
					for characters in lemGrams[i][j]:
						#print(lemGrams[i][j])
						if characters.isdigit() == True:
							#print("testing")
							depthCounter += 1
							#print(depthCounter)
						if depthCounter >= 3:
							#print(lemGrams[i][j])
							currentRodBreakDepth = lemGrams[i][j][:3]
						else:
							next
				if lemGrams[i][j] in brokenRodWords:
					rodCounter += 1
				if lemGrams[i][j] in corrosionWords:
					corrosionCounter += 1
				else:
					next

			# If at least 2 keywords are found in the trigrams rod or corrosion is present
			if rodCounter >= 2:
				foundBreak = True
			if corrosionCounter >= 2:
				foundCorrosion = True

		# Print results
		if foundBreak == True:
			#print("There is a broken rod at: " + currentRodBreakDepth)
			EOJSheet.range(counter,13).value = currentRodBreakDepth
		if foundCorrosion == True:
			#print("There is corrosion")
			EOJSheet.range(counter,14).value = "Corrosion Found"
		counter += 1
	return;

lookForBreak()
