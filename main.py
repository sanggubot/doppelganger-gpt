import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, TransformChain, SequentialChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma

load_dotenv()

def get_memory():
    memory = ConversationBufferMemory(memory_key="chat_history", ai_prefix="Doppelganger", human_prefix="You")
    return memory

def get_search_chain():
    embeddings = OpenAIEmbeddings()
    persist_directory = "db"
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    def transform_func(input_variables):
        chat = input_variables["chat"]
        docs = vectordb.similarity_search(chat)
        example_conversations = [doc.page_content for doc in docs]
        return {"example_conversations": example_conversations}
    
    search_chain = TransformChain(input_variables=["chat"], output_variables=["example_conversations"], transform=transform_func)

    return search_chain


def get_current_memory_chain():
    def transform_memory_func(input_variables):
        current_chat_history = input_variables["chat_history"].split('\n')[-10:]
        current_chat_history = '\n'.join(current_chat_history)
        return{"current_chat_history": current_chat_history}
    
    current_memory_chain = TransformChain(input_variables=["chat_history"], output_variables=["current_chat_history"], transform=transform_memory_func)

    return current_memory_chain


def get_chatgpt_chain():
    llm = ChatOpenAI(model_name='gpt-4')
    template = """너는 'You'가 말을 했을 때 'Doppelganger' 처럼 행동해야해

    예시를 보여줄테니 'Doppelganger' 의 말과 습관, 생각을 잘 유추해봐
    Examples:
    {example_conversations[0]}

    자 이제 다음 대화에서 'Doppelganger'가 할것같은 답변을 해봐.
    1. 'Doppelganger' 의 스타일대로, 'Doppelganger'가 할것같은 말을 해야해.
    2. 자연스럽게 'Doppelganger'의 말투와 성격을 따라해야해. 번역한거같은 말투 쓰지마
    3. 'You' 의 말을 이어서 만들지 말고 'Doppelganger' 말만 결과로 줘.
    4. 너무 길게 말하지는 마
    5. 'Doppelganger'의 평소 생각을 담아봐

    이전 대화:
    {current_chat_history}
    You: {chat}
    Doppelganger: """

    prompt_template = PromptTemplate(input_variables=["chat", "example_conversations", "current_chat_history"], template=template)
    chatgpt_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="received_chat")

    return chatgpt_chain


class OverallChain:
    def __init__(self) -> None:
        self.memory = get_memory()
        self.search_chain = get_search_chain()
        self.current_memory_chain = get_current_memory_chain()
        self.chatgpt_chain = get_chatgpt_chain()

        self.overall_chain = SequentialChain(
            memory=self.memory,
            chains=[self.search_chain, self.current_memory_chain, self.chatgpt_chain],
            input_variables=["chat"],
            # Here we return multiple variables
            output_variables=["received_chat"],
            verbose=True)
    
    def receive_chat(self, chat):
        review = self.overall_chain({"chat":chat})
        return review['received_chat']

def main() -> None:
    overall_chain = OverallChain()

    while True:
        recieved_chat = input("You: ")
        overall_chain.receive_chat(recieved_chat)

        os.system("clear")
        print(overall_chain.memory.load_memory_variables({})['chat_history'])


if __name__ == "__main__":
    main()