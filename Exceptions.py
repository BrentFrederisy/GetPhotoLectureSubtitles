class SubtitlesNotFoundError(Exception):
	def __init__(self, lineNumber):
		self.lineNumber = lineNumber
	def __str__(self):
		return "Subtitle not found!"