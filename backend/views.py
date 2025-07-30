from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import json
from bs4 import BeautifulSoup
from django.conf import settings
import os
from groq import Groq
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=10, period=60)
def index(request):
	context = {}
	return render(request, 'index.html', context)

@sleep_and_retry
@limits(calls=15, period=600)
def search(request, book_id):

	if not book_id.isdigit():
		response_dict = {
			'status_message': 'error',
			'status_code': 400,
			'message': 'Invalid book ID.'
		}
		return JsonResponse(response_dict, safe=False)

	# Get metadata
	metadata_url = f"https://www.gutenberg.org/ebooks/{book_id}"
	response = requests.get(metadata_url)
	metadata = response.text

	soup = BeautifulSoup(metadata, 'html.parser')

	book_dict = {
		"book_id": str(book_id),
		"analysis": {}
	}

	# Get link to read online
	a_tag = soup.find('a', string='Read now!')
	if a_tag:
		link = a_tag['href']
		if 'http' in link:
			book_dict['read_online'] = link
		else:
			book_dict['read_online'] = f"https://www.gutenberg.org{link}"
	else:   
		book_dict['read_online'] = None

	# Get link to download book as html
	a_tag = soup.find('a', string='Download HTML (zip)')
	if a_tag:
		link = a_tag['href']
		if 'http' in link:
			book_dict['download_html'] = link
		else:
			book_dict['download_html'] = f"https://www.gutenberg.org{link}"
	else:   
		book_dict['download_html'] = None

	# Get all metadata from table
	table = soup.find('table', class_='bibrec')
	if table:
		rows = table.find_all('tr')
		for row in rows:
			th = row.find('th')
			td = row.find('td')
			if th and td:
				key = th.text.replace('\n', '')
				value = td.text.replace('\n', '')

				key = key.replace(' ', '_')
				key = key.lower()
				book_dict[key] = value
			

	response_dict = {
		'status_message': 'success',
		'status_code': 200,
		'data': book_dict
	}
	return JsonResponse(response_dict, safe=False)


def analysis(request):

	book_id = request.GET.get('book_id')
	action = request.GET.get('action')

	if not book_id.isdigit():
		response_dict = {
			'status_message': 'error',
			'status_code': 400,
			'message': 'Invalid book ID.'
		}
		return JsonResponse(response_dict, safe=False)

	# Get book content
	content_url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
	response = requests.get(content_url)
	book_content = response.text

	client = Groq(
		api_key=os.environ.get("GROQ_API_KEY"),
	)

	try:
		book_sample = book_content[:6000]
	except:
		book_sample = book_content

	# Set the correct instruction for the AI
	if action == 'characters':
		user_content = f"Give me only a list of the key characters based on the following book sample: {book_sample}"
	elif action == 'language':
		user_content = f"Please give me only in one word what language is used in this book sample: {book_sample}"
	elif action == 'sentiment':
		user_content = f'''
			Please do an analysis and return in one word the sentiment evaluation from a text. The answer can only be positive, negative, or neutral.
			Give me only in one word the sentiment analysis of the following book sample: {book_sample}
		'''
	else:
		user_content = f"Please give me the plot summary from this text: {book_sample}"

	chat_completion = client.chat.completions.create(
		messages=[
			{
				"role": "system",
				"content": "you are a helpful assistant."
			},
			{
				"role": "user",
				"content": user_content,
			}
		],
		model="llama-3.3-70b-versatile",
		temperature=1,
		max_completion_tokens=1024,
		top_p=1,
		stop=None,
	)

	analysis_text = chat_completion.choices[0].message.content

	response_dict = {
		'status_message': 'success',
		'status_code': 200,
		'data': analysis_text
	}
	return JsonResponse(response_dict, safe=False)