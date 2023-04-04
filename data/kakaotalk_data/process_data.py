import re
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

def get_opponent_name(text: str) -> str:
    # The name of the other person is written on the first line of kakaotalk chat data.
    return text.split(" 님과")[0]


def mask_personal_info(chat: str, my_name: str, opponent_name: str) -> str:
    masked_chat = chat.replace(opponent_name, "You").replace(my_name, "Doppelganger")
    return masked_chat


def delete_date_info(chat: str) -> str:
    patterns = [
        r"\d{4}년\s\d{1,2}월\s\d{1,2}일\s[오후|오전]*\s\d{1,2}:\d{1,2}, ",
        r"\d{4}년\s\d{1,2}월\s\d{1,2}일\s[오후|오전]*\s\d{1,2}:\d{1,2}",
    ]

    for pattern in patterns:
        chat = re.sub(pattern, "", chat)

    return chat


def preprocess_kakaotalk_data(file_path: str) -> str:
    with open(file_path) as f:
        chat = f.read()

    my_name = "my_name"  # TODO: Replace with actual logic for getting the user's name
    opponent_name = get_opponent_name(chat)
    chat = mask_personal_info(chat, my_name, opponent_name)
    chat = delete_date_info(chat)

    return chat


def create_text_vectordb(text: str) -> None:
    persist_directory = '../../db'
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=250,
        length_function=len,
    )
    texts: List[str] = text_splitter.create_documents([text])[1:]

    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(documents=texts, embedding=embeddings, persist_directory=persist_directory)
    vectordb.persist()


def main() -> None:
    kakao_data_path: str = "./KakaoTalkChats.txt"
    chat: str = preprocess_kakaotalk_data(kakao_data_path)
    
    create_text_vectordb(chat)


if __name__ == "__main__":
    main()
