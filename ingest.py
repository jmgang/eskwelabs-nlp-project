import os
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from json_splitter import JSONSplitter

os.environ["OPENAI_API_KEY"] = ''
persist_directory='data/chroma/'

def ingest_docs():
    loader = TextLoader("data/job_title_and_description_document.json", encoding='utf-8')
    raw_document = loader.load()

    # print(raw_documents)

    text_splitter = JSONSplitter()

    documents = text_splitter.split_document(raw_document[0])

    print(documents[0])

    embeddings = OpenAIEmbeddings()

    print(f"Going to add {len(documents)} to Vector Store")

    db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory)

    print(db._collection.count())

    db.persist()

    query = "I have experience in data"
    docs = db.similarity_search(query.lower(), by_text=False)

    for doc in docs:
        print(f'========================================================\n{doc}')

