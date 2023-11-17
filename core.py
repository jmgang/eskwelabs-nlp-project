import json
import os
import pandas as pd
import chromadb
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.prompts.prompt import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings

os.environ["OPENAI_API_KEY"] = ''
persist_directory='data/chroma/'

data_science_platform_dev_df = pd.read_csv('data/data_science_platform_dev_df.csv')

def retrieve_job_ids(skills):
    embedding = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

    docs = vectordb.similarity_search(skills, k=3)
    extracted_job_ids = []
    for doc in docs:
        print(f'========================================================\n{doc.page_content}')
        data_json = json.loads(doc.page_content)
        extracted_job_ids.append(data_json['job_id'])
    print(extracted_job_ids)
    return extracted_job_ids

def retrieve_job_information(job_ids):
    template = """Given the following Job Titles and its corresponding Job Descriptions in JSON. Summarize each job description in such a way that a potential job 
    candidate would understand what skills and responsibilities the job needs. Do include salary range and experience level if any.
    Remove any information regarding location, company name and any unnecessary information. Add numbering before each job. 
    Don't add * or any special characters. Start with your response with Here's the job titles and descriptions that I found that is 
    suitable with your skillset. 
    
    JOB INFORMATION JSON:
    {job_information}
    """

    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model='gpt-4-1106-preview'
    )

    job_information = []
    for job_id in job_ids:
        job_info = data_science_platform_dev_df[data_science_platform_dev_df['job_id'] == job_id].iloc[0]
        job_information.append({'job_title':job_info['title'], 'job_description':job_info['description']})

    #print(job_information)

    prompt = PromptTemplate(
        input_variables=['job_information'], template=template
    )

    chain = LLMChain(llm=llm, prompt=prompt, verbose=True,)

    return chain.run(job_information)


# if __name__ == "__main__":
#     print(retrieve_job_information_and_format(retrieve_job_ids('java, spring, aws')))