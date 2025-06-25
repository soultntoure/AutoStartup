#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from autostartup.crew import Autostartup

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'idea': 'A mobile app that matches university students with part-time gigs near campus.',
    }
    
    try:
        result = Autostartup().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")



# src/autostartup/main.py
# from crewai.project import CrewBase, agent, crew, task
# from .crew import Autostartup


# def run_with_predefined_idea(idea: str):
#     """
#     Run the crew with a predefined idea (useful for testing)
#     """
#     print(f"Processing predefined idea: '{idea}'")
    
#     try:
#         autostartup_crew = Autostartup()
#         result = autostartup_crew.crew().kickoff(inputs={'idea': idea})
#         return result
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return None
