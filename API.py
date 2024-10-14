import requests


# response = requests.post(
#     'http://127.0.0.1:5000/advertisement/',
#     json={'description': 'лялялял','owner': 'Taras'},
#     headers={'token': 'bla-bla'}
# )

# response = requests.patch(
#     'http://127.0.0.1:5000/advertisement/9',
#     json={"owner": "Nikita"}
# )

# response = requests.get(
#     'http://127.0.0.1:5000/advertisement/10'
# )

response = requests.delete(
    'http://127.0.0.1:5000/advertisement/10'
)

print(response.status_code)
print(response.json())
