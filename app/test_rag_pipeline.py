from dotenv import load_dotenv
from rag.chain import AgentState, retrieve, generate
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
import os

def test_rag_pipeline():
    # Load environment variables
    load_dotenv()
    
    # Verify OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("generate", generate)
    
    # Set the entry point
    workflow.set_entry_point("retrieve")
    
    # Add edges
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)
    
    # Compile the graph
    chain = workflow.compile()
    
    # Test query
    test_query = "What are the key safety measures for handling hazardous materials?"
    
    # Run the pipeline
    print("\nRunning RAG pipeline test...")
    print(f"Query: {test_query}\n")
    
    try:
        # Initialize state with a valid messages list
        state = {
            "messages": [HumanMessage(content=test_query)],
            "context": "",
            "question": test_query
        }
        result = chain.invoke(state)
        print("Pipeline executed successfully!")
        # Optionally print the answer
        print("\nGenerated Response:")
        print("-" * 50)
        print(result["messages"][-1].content)
    except Exception as e:
        print(f"Error running pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    test_rag_pipeline() 