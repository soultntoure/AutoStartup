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
        'idea': 'An app to assist diabetic patients by providing personalized meal plans, medication reminders, and health tracking.',
    }
    try:
        result = Autostartup().crew().kickoff(inputs=inputs)
        print(f"Crew execution completed successfully at {datetime.now()}.")
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


