# test_graph.py
import os
import pprint
from dotenv import load_dotenv

# This is crucial for loading your OPENROUTER_API_KEY from the .env file
load_dotenv()

# Make sure the OPENROUTER_API_KEY is set
if not os.getenv("OPENROUTER_API_KEY"):
    print("ERROR: OPENROUTER_API_KEY environment variable not set.")
    print("Please create a .env file and add your key.")
else:
    # We will try to build and run the graph
    try:
        print("--- Attempting to import and build the graph... ---")
        from app.graph_builder import get_graph

        graph_app = get_graph()
        print("--- Graph compiled successfully. ---")
        print("--- Invoking the graph with test data... ---")

        # Define the input, just like in the API
        inputs = {
            "topic": "the future of renewable energy",
            "target_language": "spanish",
            "draft": "",
            "structured_blog": None,
            "translated_blog": None,
        }

        # Run the graph
        final_state = graph_app.invoke(inputs)

        print("\n--- GRAPH EXECUTION COMPLETE ---")
        print("--- FINAL STATE: ---")
        pprint.pprint(final_state)

    except Exception as e:
        print("\n--- AN ERROR OCCURRED ---")
        import traceback
        traceback.print_exc()