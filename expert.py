import os
import json
import pickle

import openai
import pickle as pkl
import logging
from config import DEFAULT_PROMPT, CHAT_COMPLETION_MODEL


class OpenaiExpert():
    def __init__(self, persona):
        self.name = persona
        with open('secrete_loc.txt') as file:
            f = file.readlines()
            self.secrete_loc = f[0]
        self.__model_initiator__()
        self.__model__ = CHAT_COMPLETION_MODEL
        self.default_prompt = DEFAULT_PROMPT
        self.messages = []
        print('Expert initiated')

    def read_secrets(self):
        stream = json.load(open('secrets_loc.json'))
        return stream

    def __model_initiator__(self):
        """Set API KEY from Secrets """
        stream = json.load(open(self.secrete_loc))
        self.__user__ = stream['User']
        self.__API_KEY__ = stream['API-KEY']
        openai.api_key = self.__API_KEY__
        self.expert = openai

class ExpertHandler():
    def __init__(self, object):
        self.expert = object

    def save_persona(self, obj):
        with open(obj.name + '.pickle', 'wb') as file:
            data = {"name": obj.name,
                    'messages': []}
            pkl.dump(data, file)

    def load_persona(self, persona):
        try:
            with open(persona + '.pickle', 'rb') as file:
                data = pkl.load(file)
                obj = OpenaiExpert(data['name'])
                obj.messages = data['messages']
                return obj

        except (OSError, IOError) as e:
            print(f"No such file exists, Create one now with name {persona}.pickle")
            base_obj = OpenaiExpert(persona)
            with open(persona + '.pickle', "wb") as file:
                data = {"name": base_obj.name,
                        'messages': []}
                pickle.dump(data, file)
                return base_obj
