
from langchain.chains import LLMChain
from langchain_community.llms import YandexGPT
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, BaseMessage

from config import Config, load_config
from config.text import LLM_SYSTEM_MESSAGE


config: Config = load_config()

llm = YandexGPT(api_key=config.llm.token,
                  folder_id=config.llm.url)

system_prompt_template = SystemMessagePromptTemplate.from_template(LLM_SYSTEM_MESSAGE)


async def get_system_prompt(userdata: dict[str, str]):
    system_prompt = await system_prompt_template.aformat(**userdata)
    return system_prompt


async def ask_llm(message_history: list[BaseMessage]) -> str:
    response = llm.invoke(message_history)
    return response