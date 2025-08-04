#!/usr/bin/env python
import sys
import textwrap
import warnings
from datetime import datetime
from pathlib import Path

from sales_meeting_preparation.crew import SalesMeetingPreparation

warnings.filterwarnings("ignore", category=SyntaxWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)


def run():
    """
    Run the crew with a target person and company.
    """
    inputs = {
        'person': 'Marc Benioff',
        'company': 'Salesforce'
    }

    try:
        result = SalesMeetingPreparation().crew().kickoff(inputs=inputs)

        # Try to extract final output from known CrewAI formats
        final_output = None
        if hasattr(result, "final_output"):
            final_output = result.final_output
        elif hasattr(result, "output"):
            final_output = result.output
        elif isinstance(result, str):
            final_output = result
        else:
            final_output = str(result)

        if final_output:
            print("\n=== Sales Meeting Preparation Report ===\n")
            print(final_output)

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            filename = f"sales_meeting_prep_{inputs['company'].lower()}_{timestamp}.md"
            Path("outputs").mkdir(parents=True, exist_ok=True)
            with open(f"outputs/{filename}", "w", encoding="utf-8") as f:
                f.write(final_output)

            print(f"\nReport saved to outputs/{filename}")
        else:
            print("No output content returned.")

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "person": "Training Exec",
        "company": "Training Co."
    }
    try:
        SalesMeetingPreparation().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        SalesMeetingPreparation().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and return the results.
    """
    inputs = {
        "person": "Test Person",
        "company": "Test Company"
    }
    try:
        SalesMeetingPreparation().crew().test(
            n_iterations=int(sys.argv[1]),
            openai_model_name=sys.argv[2],
            inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
