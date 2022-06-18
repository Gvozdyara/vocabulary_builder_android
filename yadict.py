# encoding="utf8"
import requests
import urllib
import json


def get_lang_pair(api_key):
    respond = requests.get(f'https://dictionary.yandex.net/api/v1/dicservice.json/getLangs?key={api_key}')
    return respond

def translate(word, lang, translated_list, api_key):
    

    respond = requests.get(f'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={api_key}&lang={lang}&text={word}&flags=4')

    respond_dict = json.loads(respond.text)
    
##    with open("translated.txt", "w", encoding="utf8") as f:
##        f.write(json.dumps(translation.text, indent=1))
##    with open("translated.txt", "w", encoding="utf8") as f:
##        f.write(translation.text)
    tr_param = list()
    try:
        initial_form = respond_dict["def"][0]["text"]
        tr_param.append(initial_form)
    except Exception as e:
        print(e)
    try:
        transcription = respond_dict["def"][0]["ts"]
        tr_param.append(transcription)
    except Exception as e:
        print(e)
    try:
        translation = respond_dict["def"][0]["tr"][0]["text"]
        tr_param.append(translation)
    except Exception as e:
        print(e)
    if len(tr_param)>0:
        translated_list.append(f'{word}: {", ".join(tr_param)}\n')




if __name__ == "__main__":
    with open("dictapi.txt", "r") as f:
        api_key = f.read()
    translated_list = list()
    translate("había", "es-ru", translated_list, api_key)
    print(translated_list)
