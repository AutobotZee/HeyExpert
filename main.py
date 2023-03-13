from expert import OpenaiExpert, ExpertHandler
import openai
from config import PERSONA_LIST, DEFAULT_PROMPT


def run_process(expert, start):
    data = DEFAULT_PROMPT
    data.append(message_builder("user", start))
    while start:
        response = openai.ChatCompletion.create(
            model = expert_obj.__model__,
            messages = data
        )
        token = input(f"$BOT : {response.choices[0].message.content}")
        start = message_builder('assistant', token)
        data.append(start)
        expert.messages.append(data)
        sorted_messages = set(expert.messages)
        expert.messages = sorted_messages
        if "Thanks" in token:
            print("Closing now")
            break


def message_builder(participant, prompt):
    element = {"role": participant, "content": prompt}
    return element


if __name__ == '__main__':
    print('The following Experts are available')
    for i in PERSONA_LIST:
        print(i)
    selected_persona = input("Enter the name of Persona")

    expert_obj = OpenaiExpert(selected_persona)
    handler = ExpertHandler(expert_obj)
    if selected_persona in PERSONA_LIST:
        obj = handler.load_persona(selected_persona)
        print('Persona Loaded')
        token = input('What would you like to ask now ??')
        while (token != None) or (token in 'Thanks'):
            run_process(expert_obj, token)
            handler.save_persona(expert_obj)


