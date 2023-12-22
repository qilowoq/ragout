from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

class GPT:
    """
    Represents a chatbot that uses the OpenAI chat model.

    Attributes:
        messages (dict): A dictionary to store the messages for each user.
        chat (ChatOpenAI): An instance of ChatOpenAI for generating responses.

    Methods:    
        new_rag(username: str, rag_content: str) -> None:
            Creates a new RAG (Retrieval-Augmented Generation) conversation.

        ask(username: str, query: str) -> str:
            Sends a query to the chat model and returns the response.

        reset(username: str) -> None:
            Resets the conversation for a given username.

    """
    def __init__(self, api_key: str) -> None:
        """
        Initializes a ChatGPT 3.5 turbo instance.

        Args:
            api_key (str): The API key for accessing the OpenAI chat model.
        """
        self.messages = {}
        self.chat = ChatOpenAI(
            openai_api_key=api_key,
            model='gpt-3.5-turbo'
        )

    def new_rag(self, username: str, rag_content: str) -> None:
        """
        Creates a new RAG (Retrieval-Augmented Generation) conversation.

        Args:
            username (str): The username associated with the conversation.
            rag_content (str): The content of the RAG conversation.
        """
        self.messages[username] = [
            SystemMessage(content="You are a helpful assistant. Your name is Ragoût and you try to help people to find information in the document they will give you."),
            HumanMessage(content=make_rag(rag_content)),
            AIMessage(content="Yes I understand. I will answer to your questions about this document and I will not deviate from it.")
        ]

    def ask(self, username: str, query: str) -> str:
        """
        Sends a query to the chat model and returns the response.

        Args:
            username (str): The username associated with the conversation.
            query (str): The query to be sent to the chat model.

        Returns:
            str: The response from the chat model.
        """
        if username not in self.messages:
            self.messages[username] = [SystemMessage(content="You are a helpful assistant. Your name is Ragoût.")]
        self.messages[username].append(HumanMessage(content=query))
        res = self.chat(self.messages[username])
        self.messages[username].append(res)
        return res
    
    def reset(self, username: str) -> None:
        """
        Resets the conversation for a given username.

        Args:
            username (str): The username associated with the conversation.
        """
        self.messages[username] = [SystemMessage(content="You are a helpful assistant.")]

def make_rag(rag_content: str) -> str:
    """
    Creates a prompt with the given RAG content.

    Args:
        rag_content (str): The content of the RAG conversation.

    Returns:
        str: Prompt for ChatGPT model.
    """
    return f"""The following text is a document I give you. You have to answer to the questions he will ask you about this documentation. 

    Document: {rag_content}

    
    That concludes the documentation. In the next messages, I will ask you questions about this document. 
    Use ONLY the factual information from the transcript to answer the question.
    If you feel like you don't have enough information to answer the question, say "I don't know".
    Your answers should be verbose and detailed. Do you understand?"""