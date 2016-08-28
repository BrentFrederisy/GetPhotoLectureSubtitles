"""
	GetPhotoLecturesSubtitles - A commandline application to download the subtitles for the Photography A130 Lectures hosted on 3mediasolutions.com

	Takes a txt file as a commandline argument and writes the lectures subtitles to a txt file.
"""

import requests as rq
import re
from sys import argv

from Exceptions import *
from requests.exceptions import *

infile = open(argv[1], 'r')
outfile = open('PhotographyLecture.txt', 'w')

currentLine = 0

for lecture in infile:
	currentLine += 1

	if lecture[-1] == '\n':
		lecture = lecture[:-1] 

	try:
		lecturePageHTML = rq.get(lecture)

		lecturePageHTML.raise_for_status()

		print("Lecture Accessed")

	except (ConnectionError, HTTPError, Timeout, TooManyRedirects):
		print("ERROR ACCESSING LECTURE")

		outfile.write("\nERROR ACCESSING LECTURE\n")

		continue

	try:
		subtitleSource = re.search('file: \"(.+\.vtt)', lecturePageHTML.text)

		if subtitleSource is None:
			raise SubtitlesNotFoundError(currentLine)

		print("Subtitles Found")

	except SubtitlesNotFoundError:
		print("ERROR SUBTITLES NOT FOUND")

		outfile.write("\nERROR FINDING SUBTITLES\n")

		continue

	subtitleText = rq.get(subtitleSource.group(1)).text

	subtitleText = subtitleText.splitlines()

	for line in subtitleText:
		# timestamps contain "-->" and are to be ignored
		if "-->" in line or len(line) == 0:
			continue
		else:
			# Remove the metadata sometimes present on the line
			newLine = line.replace("WEBVTT","").replace("&gt;&gt; ","")
			
			outfile.write(newLine)

			# Add a space at the end if needed
			if len(newLine) > 0 and newLine[-1] != ' ':
				outfile.write(' ')

	print("Lecture Transcribed")

print("Done.")