import requests
 
response = requests.get('https://portal.exoscale.com/api/pricing/dbaas-kafka')
content = response.json()['chf']

for plan in content:
    print(f"{plan},{content[plan]}")