##################################################
## This python code performs speech to text
## translation and awakens when a specific word
## is recognized
##################################################
## No license
##################################################
## Author: Laurent Lava
## Copyright: Copyright 2020, Speech_to_text_wakener
## Credits: [{credit_list}]
## License: {license}
## Version: 0.0.2
## Mmaintainer: Laurent Lava
## Email: Laurentlava04[at]gmail.com
## Status: under dev
##################################################


###############
## Libraries ##
###############


from datetime import datetime
import time
import speech_recognition as sr
import warnings
from time import perf_counter


###############
## Variables ##
###############

file_name = "logs.txt"
ROWS_TO_KEEP = 100
WAKE_UP = ["mango"]


###############
## Functions ##
###############


def keep_n_lines(n, filename):
	"""
	This function reads a file and only returns the last n 
	elements if the number of elements is greater or equal to
	n.
	"""

	shorten_file = False

	with open(filename, 'r') as f:
		data = f.read()
		num_of_lines = data.count('\n')
		list_of_indexes = [pos for pos, char in enumerate(data) if char == '\n']
		if num_of_lines > n:
			start = list_of_indexes[-100]
			data = data[start:]
			shorten_file = True

	if shorten_file:
		with open(filename, 'w') as f:
			f.write(data)


def my_logger(fn):
	"""
	This function will be used as a decorator to log API calls.
	"""

	def inner(*args, **kwargs):
		result = fn(*args, **kwargs)

		# Open file
		with open(file_name, 'a') as f:
			# Get current date and format it
			now = datetime.now()
			dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

			# Add line
			f.write("@: {0}: Results: {1}\n".format(dt_string, result))

		keep_n_lines(ROWS_TO_KEEP, file_name)

		return result
	return inner


@my_logger
def recognize_speech_from_mic(recognizer, microphone):
    """Translate speech from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

###############
## Main func ##
###############

if __name__ == "__main__":

	warnings.filterwarnings("ignore", category=DeprecationWarning)

	# Create the recognizer and mic instances
	recognizer = sr.Recognizer()
	microphone = sr.Microphone()

	time.sleep(3)

	while True:

		print("I am listening to you")
		guess = recognize_speech_from_mic(recognizer, microphone)

		# API is not available
		if not guess["success"]:
			print("API not available, sorry")

		else:
			# Sentence not understood
			if guess["error"] == "Unable to recognize speech":

				pass
			# Sentence is understood
			else:

				for word in WAKE_UP:
					if word.lower() in guess["transcription"].lower():
						print("I am wakink up !!")

						# Once the listenner is waken up, 
						# try to catch a usefull command.
						start = perf_counter()
						end = perf_counter()
						exit = False

						# Be awaken for 30 seconds or until catching a usefull command
						while (end - start <= 30) or not exit:

							# perform speech to text transformation
							guess = recognize_speech_from_mic(recognizer, microphone)

							# API is not available
							if not guess["success"]:
								print("API not available, sorry")


							else:
								# Sentence not understood
								if guess["error"] == "Unable to recognize speech":
									pass

								# Sentence is understood
								else:

									# Turn on kitchen lights
									if "turn on the kitchen lights" in guess["transcription"].lower():
										print("Kitchen lights ON")
										exit = True

									# Turn off kitchen lights
									elif "turn off the kitchen lights" in guess["transcription"].lower():
										print("Kitchen lights off")
										exit = True

							end = perf_counter()

						







