import json
import yaml
from mistralai import Mistral


def is_pm(title, abstract):
    with open('config.yaml', 'r', encoding='utf8') as f:
        config = yaml.safe_load(f)
    client = Mistral(config['api']['key'])

    system_prompt = """
    SUPER IMPORTANT: RESPOND ONLY WITH JSON STRING!!!
    DO NOT USE ANY MARKDOWN, ONLY JSON STRING STARTING WITH { AND ENDING WITH } !!!
    You're world class scientific journal editor. Your ability do assign topics to articles is immaculate.
    You will be provided with title and abstract of an article. Determine if this article suits the topic of Proccess Mining.
    If it does, respond only with {"is_suitable": "True"}. If it does not, respond with {"is_suitable": "False"}. Do not respond with anything else.
    """

    chat_response = client.chat.complete(
        model = config['api']['model'],
        messages = [
            {
                'role': 'system',
                'content': system_prompt
            },
            {
                'role': 'user',
                'content': f'Title: {title}, Abstract: {abstract}',
            },
        ]
    )

    try:
        json_response = json.loads(chat_response.choices[0].message.content)
    except json.JSONDecodeError:
        # TODO: Logging of erroneuous responses
        return {'is_suitable': 'False'}

    return json_response
