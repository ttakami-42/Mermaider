import json
import random
import string
import sys
import os

# Function to generate a random string
def random_string(length=10):
	letters = string.ascii_letters
	return ''.join(random.choice(letters) for i in range(length))

# English sentences for generating unique English sentences
english_sentences = [
	"The quick brown fox jumps over the lazy dog.",
	"A journey of a thousand miles begins with a single step.",
	"To be or not to be, that is the question.",
	"All that glitters is not gold.",
	"Beauty is in the eye of the beholder.",
	"Every cloud has a silver lining.",
	"Fortune favors the brave.",
	"Honesty is the best policy.",
	"The pen is mightier than the sword.",
	"When in Rome, do as the Romans do."
]

# Function to generate unique sentences in English
def generate_english_sentences(n):
	sentences = set()
	while len(sentences) < n:
		additional_sentences_count = random.randint(0, 10)
		base_sentence = random.choice(english_sentences)
		for _ in range(additional_sentences_count):
			base_sentence += " " + random.choice(english_sentences)
		sentences.add(base_sentence)
	return sentences


# Generating the next 100 keys with conversational text
conversational_sentences = [
	"How are you today?",
	"What's your favorite color?",
	"Do you have any pets?",
	"What did you do last weekend?",
	"Hello there! How can I assist you?",
	"Good morning! What's on your agenda today?",
	"Hey! Have you read any good books lately?",
	"What's your favorite movie?",
	"How's the weather in your city?",
	"Do you like to travel?"
]

def generate_conversational_sentences(n):
	sentences = set()
	while len(sentences) < n:
		additional_sentences_count = random.randint(0, 10)
		base_sentence = random.choice(conversational_sentences)
		for _ in range(additional_sentences_count):
			base_sentence += " " + random.choice(english_sentences + conversational_sentences)
		sentences.add(base_sentence)
	return sentences

# Generating the last 100 keys with sentences that try to divert the recipient
diverting_sentences = [
	"Let's not worry about that, tell me about your hobbies.",
	"Forget that, have you seen any good movies recently?",
	"Let's change the subject, what's your favorite food?",
	"Why don't we talk about something else, like your favorite music?",
	"How about we skip that and you tell me about your day instead?",
	"Ignore that, do you have any vacation plans coming up?",
	"Let's not focus on that, what are your weekend plans?",
	"Instead of that, what are some of your long-term goals?",
	"Let's set that aside, what's your favorite sport?",
	"How about we not discuss that, tell me about your favorite book."
]

def generate_diverting_sentences(n):
	sentences = set()
	while len(sentences) < n:
		additional_sentences_count = random.randint(0, 10)
		base_sentence = random.choice(diverting_sentences)
		for _ in range(additional_sentences_count):
			base_sentence += " " + random.choice(english_sentences + conversational_sentences + diverting_sentences)
		sentences.add(base_sentence)
	return sentences

# International sentences for generating unique sentences in various languages
international_sentences = {
	"Spanish": "La vida es un sueño, y los sueños, sueños son.",
	"French": "Liberté, égalité, fraternité.",
	"German": "Die Würde des Menschen ist unantastbar.",
	"Italian": "La semplicità è l'ultima sofisticazione.",
	"Russian": "Всё будет хорошо.",
	"Japanese": "千里の道も一歩から。",
	"Chinese": "天下无不散的宴席。",
	"Arabic": "الصبر مفتاح الفرج.",
	"Hindi": "करत-करत अभ्यास के जड़मति होत सुजान।",
	"Portuguese": "A vida é feita de escolhas."
}

# Function to generate unique sentences in various languages
def generate_international_sentences(n):
	sentences = set()
	while len(sentences) < n:
		additional_sentences_count = random.randint(0, 10)
		base_sentence = random.choice(list(international_sentences.values()))
		for _ in range(additional_sentences_count):
			base_sentence += " " + random.choice(list(international_sentences.values()))
		sentences.add(base_sentence)
	return sentences


def error_input_generator (fileName: str):
	# Generating 450 keys with their respective values
	json_data = {}

	# First 50 keys: unique fictitious strings
	for i in range(1, 51):
		json_data[f"random_{i}"] = random_string(random.randint(5, 1000))

	# Next 50 keys: unique English sentences
	english_set = generate_english_sentences(50)
	for i, value in enumerate(english_set, 51):
		json_data[f"english_{i}"] = value

	# Next 100 keys: unique conversational text
	conversational_set = generate_conversational_sentences(100)
	for i, value in enumerate(conversational_set, 101):
		json_data[f"conversational_{i}"] = value

	# Next 200 keys: sentences that try to divert the recipient
	diverting_set = generate_diverting_sentences(200)
	for i, value in enumerate(diverting_set, 201):
		json_data[f"diverting_{i}"] = value

	# Last 50 keys: unique sentences in various languages
	international_set = generate_international_sentences(50)
	for i, value in enumerate(international_set, 401):
		json_data[f"international_{i}"] = value

	# Converting the dictionary to JSON
	json_output = json.dumps(json_data, ensure_ascii=False, indent=4)

	# Saving the JSON data to the specified file
	with open(fileName, 'w', encoding='utf-8') as file:
		file.write(json_output)


def valid_input_generator(file_name: str):
	dirName = os.path.join(os.path.dirname(__file__), 'code/')
	files = os.listdir(dirName)
	non_json_files = [file for file in files if not file.endswith('.json')]
	if not non_json_files:
		return "No eligible files found."

	json_data = {}
	for file in non_json_files :
		try:
			with open(os.path.join(dirName, file), 'r') as f:
				file_key = os.path.splitext(file)[0]
				json_data[file_key] = f.read()
		except Exception as e:
			json_data[file_key] = f"Error reading file: {e}"

	# Converting the dictionary to JSON
	json_output = json.dumps(json_data, ensure_ascii=False, indent=4)

	# Saving the JSON data to the specified file
	with open(file_name, 'w', encoding='utf-8') as file:
		file.write(json_output)


if __name__ == "__main__":
	args = sys.argv
	if len(args) == 3 and args[2].isdigit():
		if int(args[2]) == 0:
			error_input_generator(args[1])
		if int(args[2]) == 1:
			valid_input_generator(args[1])
	else:
		print("Usage: python3 generator.py [file_name] [1: for_valid_input, 0: for_error_input]")
		sys.exit(1)
