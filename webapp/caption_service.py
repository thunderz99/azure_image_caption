import os
import sys
import requests

API_ENDPOINT = 'https://eastasia.api.cognitive.microsoft.com/' \
    + 'vision/v1.0/describe?maxCandidates=1'

API_ENDPOINT_V2 = 'https://eastasia.api.cognitive.microsoft.com/' \
    + 'vision/v2.0/analyze?visualFeatures=Description'

API_KEY = os.getenv('AZURE_VISION_API_KEY')

assert API_KEY


class CaptionService:

    def __init__(self):
        pass

    def get_caption(self, filepath, language='en'):

        headers = {'Ocp-Apim-Subscription-Key': API_KEY}
        url = API_ENDPOINT_V2 + '&language=' + language
        files = {'media': open(filepath, 'rb')}
        response = requests.post(url, files=files, headers=headers)
        data = response.json()
        print(data)
        return data.get('description', {}).get('captions', [{}])[0].get('text')


if __name__ == '__main__':
    cs = CaptionService()
    captions = cs.get_caption('dogcatch.png', 'en')
    print(captions)
