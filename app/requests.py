from urllib import response
import urllib.request,json
def get_quote():
    
    urlget="http://quotes.stormconsultancy.co.uk/random.json".format()
    with urllib.request.urlopen(urlget) as url:
        quote=url.read()
        response=json.loads(quote)
        return response
   