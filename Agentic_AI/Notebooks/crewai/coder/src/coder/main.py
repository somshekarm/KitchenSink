#!/usr/bin/env python
import sys
import warnings
import os

from datetime import datetime

from coder.crew import Coder

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

os.makedirs('output', exist_ok=True)

assignment = 'Write a C# code to reverse an interger in the array [984569847569832475, -2345243, 472375, 0, 10, -1] and return the reversed array.\
    if the value go outside the range of 32 bit signed integer, return 0.'

def run():
    """
    Run the crew.
    """
    inputs = {
        'assignment': assignment
    }
    
    result = Coder().crew().kickoff(inputs=inputs)
    print(f"Result: {result.raw}")