import requests
def get_quote():
    url="http://quotes.stormconsultancy.co.uk/random.json".format()
    main_url=requests.get(url).json()
    return  main_url