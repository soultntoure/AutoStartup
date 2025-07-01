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
        'idea': ' An app that helps users track their daily water intake and reminds them to stay hydrated, with features like personalized goals, reminders, and progress tracking.',
    }
    
    try:
        result = Autostartup().crew().kickoff(inputs=inputs)
        print(f"Crew execution completed successfully at {datetime.now()}.")
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


