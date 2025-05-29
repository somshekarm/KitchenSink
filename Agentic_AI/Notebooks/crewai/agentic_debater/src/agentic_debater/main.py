#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from agentic_debater.crew import AgenticDebater

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        'motion': 'AI is threat or boost for Tech workers?'        
    }
    
    try:
        results = AgenticDebater().crew().kickoff(inputs=inputs)
        print(results)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'motion': 'AI is threat or boost for Tech workers?'  
    }
    try:
        AgenticDebater().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AgenticDebater().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'motion': 'AI is threat or boost for Tech workers?'  
    }
    
    try:
        AgenticDebater().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
