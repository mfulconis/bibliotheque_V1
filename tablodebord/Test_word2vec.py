import requests
import json
params = ()
airtable_records = []
run = True
while run is True:
    r = requests.get('https://api.airtable.com/v0/appBvKk6a0YWsf0ay/'
                 'Biblioth%C3%A8que%20des%20Fulcos?api_key=keyAeXwxVMw0lLYtK&'
                 'fields%5B%5D=Titre&fields%5B%5D=Nomtxt&fields%5B%5D=Tagstxt&'
                 'fields%5B%5D=Formatcm&fields%5B%5D=Pages&fields%5B%5D=Lutxt&', params=params)
    airtable_reponse = r.json()
    airtable_records += (airtable_reponse['records'])
    if 'offset' in airtable_reponse:
        run = True
        params = (('offset', airtable_reponse['offset']),)
    else:
        run = False
base2 = {'records' : airtable_records}
print(base2)

def getdata():
    r = requests.get('https://api.airtable.com/v0/appBvKk6a0YWsf0ay/'
                     'Biblioth%C3%A8que%20des%20Fulcos?api_key=keyAeXwxVMw0lLYtK&'
                     'fields%5B%5D=Titre&fields%5B%5D=Nomtxt&fields%5B%5D=Tagstxt&'
                     'fields%5B%5D=Formatcm&fields%5B%5D=Pages&fields%5B%5D=Lutxt&')
    base = json.loads(r.text)
    print(base)
    return base

getdata()