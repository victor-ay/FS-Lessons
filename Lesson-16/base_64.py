import base64

url_id = base64.urlsafe_b64encode('https://edulabs.co.il/ci1-Full-stack-individual-morning-he.html'.encode()).decode().strip('=')
url_id = base64.urlsafe_b64encode('https://edulabs.co.il'.encode()).decode().strip('=')

print(url_id)

url_id = base64.urlsafe_b64encode('u-8a3dbdfe3b1fd8b18a0c77ee44c4f59a156a94cf6e73c00162eaa649ad245ede-1673971515'.encode()).decode().strip('=')
print(url_id)

url_id = base64.urlsafe_b64encode('https://edulabs.co.il/courses-individual-he.html'.encode()).decode().strip('=')
print(url_id)