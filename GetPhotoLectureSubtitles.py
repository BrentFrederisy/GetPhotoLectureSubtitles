import requests as rq
import re

# List of lectures to get the subtitles from
lecturesToGetSubtitlesFromURL = ["http://www.3cmediasolutions.org/privid/41231?key=d2b884efdc6529642c1a81c9ffe5c538cb713420", "http://www.3cmediasolutions.org/privid/41232?key=6b39a65f2b0ba86e2ad72ad6195f9229ac01fea8", "http://www.3cmediasolutions.org/privid/41233?key=5c28088727277373db2cf85d7bcc1aec027886ef", "http://www.3cmediasolutions.org/privid/41234?key=d2f1e22ab36dc15817b47dee7a934fd465dd8b90", "http://www.3cmediasolutions.org/privid/41235?key=d1ac4b3370eda44f1a82959a253f90121bc06123", "http://www.3cmediasolutions.org/privid/41236?key=99740addbbebd99c6e9daa5d105d41dbb4b56076", "http://www.3cmediasolutions.org/privid/41237?key=a51c3b8565f39b07aee087498017996ae00aac3c", "http://www.3cmediasolutions.org/privid/41239?key=9a549032172c95d9b2ca0ca9bba706fdba2821f0", "http://www.3cmediasolutions.org/privid/41240?key=e3f6d41a666eebd6d911f601d933019deb2ad0fa"]

outfile = open('PhotographyLecture0X.txt', 'w')
print("Opening the output file")

for lecture in lecturesToGetSubtitlesFromURL:
	# Gets the page source code
	lecturePageHTML = rq.get(lecture)
	print("Lecture Accessed")

	# Finds the url for the subtitles
	subtitleSource = re.search('file: \"(.+\.vtt)', lecturePageHTML.text)
	print("Subtitles Found")

	# Gets the text in the subtitles source
	subtitleText = rq.get(subtitleSource.group(1)).text

	# Text is filtered line by line
	subtitleText = subtitleText.splitlines()

	for line in subtitleText:
		# Ignore the line if its a timestamp--timestamps contain "-->"
		if "-->" in line or len(line) == 0:
			continue
		else:
			# Remove the metadata from the line
			newLine = line.replace("WEBVTT","").replace("&gt;&gt; ","")
			outfile.write(newLine)

			# Add a space at the end if need-be
			if len(newLine) > 0 and newLine[-1] != ' ':
				outfile.write(' ')

	print("Lecture Transcribed")

print("Done.")