from langchain_google_genai import ChatGoogleGenerativeAI
from sqlalchemy import create_engine, text
from sqlalchemy import URL
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_agent
import os
from dotenv import load_dotenv

load_dotenv()


def create_db_agent():
    """
    Creates and returns a database agent configured to query the atliq_tshirts database.
    
    Returns:
        agent: The configured LangChain agent
        
    Raises:
        ValueError: If GOOGLE_API_KEY is not found in environment variables
        Exception: If database connection fails
    """
    # Check for API key
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables!")
    
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key
    )
    
    # Create database connection
    url_object = URL.create(
        "mysql+pymysql",
        username="root",
        password="Ishita@1234",
        host="localhost",
        database="atliq_tshirts",
    )
    
    engine = create_engine(url_object)
    
    # Test the database connection
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result.fetchall()]
            print("✓ Database connection successful!")
            print(f"Tables in database: {tables}")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        raise
    
    # Create database toolkit
    db = SQLDatabase(engine)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()
    
    # Create agent
    agent = create_agent(llm, tools=tools)
    
    if agent is None:
        raise Exception("Agent creation failed")
    
    print("✓ Agent created successfully!")
    return agent


def query_database(agent, question):
    """
    Queries the database using the agent with a natural language question.
    
    Args:
        agent: The database agent created by create_db_agent()
        question (str): Natural language question about the database
        
    Returns:
        str: The answer from the agent
        
    Example:
        agent = create_db_agent()
        answer = query_database(agent, "How many Nike t-shirts are in stock?")
    """
    try:
        # Use the messages format
        response = agent.invoke({
            "messages": [{"role": "user", "content": question}]
        })
        
        # Extract answer from response
        last_message = response['messages'][-1]
        content = last_message.content
        
        if isinstance(content, list):
            answer = content[0]['text']
        elif isinstance(content, str):
            answer = content
        else:
            answer = str(content)
        
        return answer
        
    except Exception as e:
        return f"Error querying database: {str(e)}"



# For testing purposes
if __name__ == "__main__":
    # Test the functions
    agent = create_db_agent()
    
    test_question = "If I sell all my Levi t-shirts with discount, how much revenue will the store generate?"
    answer = query_database(agent, test_question)
    
    print(f"\nQuestion: {test_question}")
    print(f"Answer: {answer}")