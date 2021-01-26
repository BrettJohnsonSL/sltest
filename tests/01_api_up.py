import requests


def test_api_access():
	response = requests.get("http://127.0.0.1:8888/api/test1")
	assert response.status_code == 200
