from ckanapi import RemoteCKAN
from .client_secrets import api_key

ua = 'ckanapiexample/1.0 (+http://example.com/my/website)'

def upload_resource(filepath):
    mysite = RemoteCKAN('http://data.codefordc.org',
            apikey=api_key, user_agent=ua)
    mysite.action.resource_update(
        id='3c505827-08d1-47a3-a620-f196a2cf5b06',
        url='dummy-value',  # ignored but required by CKAN<=2.5.x
        upload=open(filepath, 'rb'))
