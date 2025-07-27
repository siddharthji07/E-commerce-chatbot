import os
import openai
import pinecone
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv
load_dotenv()

openai.api_key=os.environ["OPENAI_API_KEY"]
pinecone_api_key=os.environ["PINECONE_API_KEY"]
index_name=os.environ["INDEX_NAME"]


import os
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

pinecone.init(api_key=pinecone_api_key, environment='gcp-starter')
index = Pinecone.from_existing_index(index_name, embeddings)

model_name = "gpt-3.5-turbo"
llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"],model_name=model_name)
chain = load_qa_chain(llm, chain_type="stuff")

history = []

def append_history(query,answer):
    history.append(("User", query))
    history.append(("Bot", answer))

def get_similiar_docs(query,k=4,score=False):
        if score:
            similar_docs = index.similarity_search_with_score(query,k=k)
        else:
            similar_docs = index.similarity_search(query,k=k)
        return similar_docs

def get_answer(query):
    
    similar_docs = get_similiar_docs(query)
    prompt=f"""You are e-commerce support chatbot for ONDC (Open Network for Digital Commerce), your primary role is to assist users with their queries related to products, provide structured product recommendations, and address other store-related inquiries. Your responses should be truthful, non-offensive, and strictly based on the provided knowledge base.

Instructions:
Provide assistance within the scope of e-commerce and ONDC.
If the query context require more information ask user but only if necessary.
For product related queries show 3-5 if available products in your knowledge base with the name, price, small combined description and image link.
If you lack information on a topic, respond with "I Don't know."
You must provide answer without asking much questions with minimal words in user query.
For Legal compliance, policies and related queries be concis in response.
Below is the user request history, if this is relevant to 
current user query then you need to use it if necessary and refer to this while creating response.
User request history:
{history[-6:]}
\n
USER QUERY:\n """
    user_query=prompt+query
    print(user_query)
    answer = chain.run(input_documents=similar_docs, question=user_query)
    append_history(query,answer)
    return answer


