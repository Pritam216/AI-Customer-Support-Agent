from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_cohere import CohereEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import re
import os

load_dotenv()

loader = TextLoader("data/policy.txt", encoding="utf-8")
docs = loader.load()

text = docs[0].page_content
matches = re.finditer(
    r'RULE \d+:.*?(?=RULE \d+:|$)',
    text,
    re.DOTALL
)

docs = [
    Document(
        page_content=m.group(0),
        metadata={
            "rule_id": re.search(
                r'RULE (\d+):',
                m.group(0)
            ).group(1)
        }
    )
    for m in matches
]

# print(len(docs))

# for doc in docs:
#     print(doc)

embedding_model = CohereEmbeddings(
    model = "embed-english-light-v3.0",
    cohere_api_key= os.getenv("COHERE_API_KEY")
)
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
    persist_directory="./chroma_db"
)