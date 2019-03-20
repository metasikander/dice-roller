from rdoclient_py3 import RandomOrgClient

api = "64d3f180-7d8d-4abe-a1d0-e9800d253316"

r = RandomOrgClient(api)

print(r.generate_integers(5, 0, 10))

#TODO: run test to check connectivity with random.org
#TODO: run test to see how many requests you have left
#TODO: if test sucsessfull, fill cache up to maxium n bits, else fall back to prng