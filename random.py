from rdoclient_py3 import RandomOrgClient

api = "64d3f180-7d8d-4abe-a1d0-e9800d253316"

r = RandomOrgClient(api)

print(r.generate_integers(5, 0, 10))