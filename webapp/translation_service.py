import os
import sys
import requests


API_ENDPOINT = 'https://api.cognitive.microsofttranslator.com' \
    + '/translate?api-version=3.0'

API_KEY = os.getenv('AZURE_TRANSLATION_API_KEY')

assert API_KEY


class TranslationService:

    def __init__(self):
        pass

    def get_translation(self, text, to_language='ja'):

        headers = {
            'Ocp-Apim-Subscription-Key': API_KEY,
            'Content-type': 'application/json'
        }

        requestBody = [{
            'Text': text,
        }]

        url = API_ENDPOINT + '&to=' + to_language
        response = requests.post(url, json=requestBody, headers=headers)
        data = response.json()
        print(data)
        return data[0].get('translations')[0].get('text')


if __name__ == '__main__':
    ts = TranslationService()
    text = ts.get_translation(
        "a brown and white dog carrying a frisbee in its mouth",
        to_language='ja')
    print(text)
