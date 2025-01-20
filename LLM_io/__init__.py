
from yandex_cloud_ml_sdk import YCloudML

from config import Config, load_config


config: Config = load_config()

client = YCloudML(auth=config.llm.token,
                  folder_id=config.llm.url)

async def ask_llm(message_history: list[dict[str, str]]) -> str:
    print(message_history)
    response = client.models.completions('yandexgpt').configure(
        temperature=config.llm.temperature).run(message_history)
    alter = response.alternatives[0]
    return {'role': alter.role, 'text': alter.text}