from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import json
from bs4 import BeautifulSoup

def index(request):
	context = {}
	return render(request, 'index.html', context)

def search(request, book_id):

	# Get book content
	# content_url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
	# response = requests.get(content_url)
	# book_content = response.text

	# Get metadata
	metadata_url = f"https://www.gutenberg.org/ebooks/{book_id}"
	response = requests.get(metadata_url)
	metadata = response.text

	soup = BeautifulSoup(metadata, 'html.parser')

	book_dict = {
		"book_id": str(book_id)
	}

	# Get link to read online
	a_tag = soup.find('a', string='Read online (web)')
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