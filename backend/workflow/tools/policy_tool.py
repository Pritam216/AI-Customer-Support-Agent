from langchain.tools import tool
from langchain_chroma import Chroma
from scripts.policy_rag import embedding_model


vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embedding_model
    )

retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 1,
            "lambda_mult":0.5
            }
        )

@tool
def rag_tool(query : str):
    """
    Fetch the relevent customer refund plicy based on the query.
    """
    results = retriever.invoke(query)
    # return results
    return results[0].page_content