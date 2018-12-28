import os, time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

data = {
	'eduk_url': 'https://beta.eduk.com.br/',
	'download_url': 'http://savevideo.me/pt/',
	'email': '****',
	'pass': '****',
	'course_id': '4064'
}

driver = webdriver.Firefox()
driver.get(data['eduk_url'] + 'login')
f = open('links.txt', 'w')

# login 
email_input = driver.find_element_by_id('email')
email_input.send_keys(data['email'])

password_input = driver.find_element_by_id('password')
password_input.send_keys(data['pass'])

password_input.send_keys(Keys.RETURN)

time.sleep(1)

# go to course
driver.get(data['eduk_url'] + 'cursos/' + data['course_id'])
print('Opening "%s" course..' %driver.title)

f.write('Curso: %s\n' %driver.title.encode('ascii', 'ignore').decode('ascii'))
f.write('Link: %s\n' %driver.current_url)

time.sleep(1)

# finding course activities
links = driver.find_elements_by_tag_name('a')
activities = []
videos = []

for link in links:
	if 'cursos/' + data['course_id'] in link.get_property('href'):
		activities.append(link.get_property('href'))

print('%d activities/videos found!' %len(activities))

f.write('\nAtividades:\n\n')

for activity in activities:
	print('Opening activity "%s"..' %activity)

	driver.get(activity)
	f.write('Link: %s\n' %activity)

	time.sleep(1)

	try:
		iframes = map(lambda iframe: iframe.get_property('src'), driver.find_elements_by_tag_name('iframe'))
	except Exception as e:
		print('Failed to fetch iframe. Details: %s' %e.__str__())

	for iframe in iframes:
		if 'vimeo' in iframe:
			print('Video found: %s' %iframe)
			videos.append(iframe)
			f.write('Video: %s\n' %iframe)
	
	f.write('\n')
	time.sleep(1)

'''
print('Starting downloading all %d videos!' %len(videos))

for video in videos:
	driver.get(data['download_url'])
	
	vimeo_url = video.split('?')[0].replace('player.', '')
	search_input = driver.find_element_by_id('url')

	search_input.send_keys(vimeo_url)
	search_input.send_keys(Keys.RETURN)

	print('Downloading video %s..' %vimeo_url)
'''

f.close()
driver.close()