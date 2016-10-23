from flask import url_for


def test_home_page(client):
    """ Home page should respond with a success 200. """
    response = client.get('/')
    assert response.status_code == 200

def test_login(client):
	""" Check for authentication for valid user. """ 
	data = { 'username': 'Joey', 'password': 'Joey'}
	response = client.post('/api/authentication', data=data)
	assert response.status_code == 200

def test_bad_login(client):
	""" Check for authentication for valid user. """ 
	data = { 'username': 'Joey', 'password': 'oey'}
	response = client.post('/api/authentication', data=data)
	assert response.status_code == 401

def test_logout(client):
	data = { 'username': 'Joey', 'password': 'Joey'}
	response = client.post('/api/authentication', data=data)
	assert response.status_code == 200
	response = client.get('/api/logout')
	assert response.status_code == 200
