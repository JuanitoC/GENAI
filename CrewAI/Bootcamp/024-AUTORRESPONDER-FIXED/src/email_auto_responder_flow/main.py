#!/usr/bin/env python
import time
import os
import json
from typing import List

from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

from email_auto_responder_flow.types import Email
from email_auto_responder_flow.utils.emails import check_email, format_emails

from .crews.email_filter_crew.email_filter_crew import EmailFilterCrew


class AutoResponderState(BaseModel):
    emails: List[Email] = []
    checked_emails_ids: set[str] = set()


class EmailAutoResponderFlow(Flow[AutoResponderState]):
    initial_state = AutoResponderState

    @start("wait_next_run")
    def fetch_new_emails(self):
        print("🔄 Checking for new emails...")
        new_emails, updated_checked_email_ids = check_email(
            checked_emails_ids=self.state.checked_emails_ids
        )

        self.state.emails = new_emails
        self.state.checked_emails_ids = updated_checked_email_ids
        print(f"📥 Found {len(new_emails)} new email(s).")
        return self.state

    @listen(fetch_new_emails)
    def generate_draft_responses(self):
        print("📨 Current email queue:", len(self.state.emails))

        if self.state.emails:
            print("✍️ Generating responses for new emails...")
            print(format_emails(self.state.emails))  # Optional: human-readable output

            try:
                # ✅ FIX: Skip .dict() since these are already dictionaries
                emails_json = json.dumps(self.state.emails)

                result = EmailFilterCrew().crew().kickoff(inputs={"emails_json": emails_json})

                # ✅ Print full raw output
                print("✅ Crew output:")
                print(result.raw)

                # ✅ Optional: Per-task debug output
                print("\n🔍 Debug Output Breakdown:\n")
                try:
                    for task_name, output in result.task_outputs.items():
                        print(f"📌 Task '{task_name}' output:\n{output}\n")
                except Exception as e:
                    print("⚠️ Could not extract task-level output:", str(e))

                # ✅ Save to disk
                os.makedirs("output", exist_ok=True)
                with open("output/last_draft_output.txt", "w") as f:
                    f.write(result.raw)

            except Exception as e:
                print("❌ Error running the Email Filter Crew:", str(e))

            self.state.emails = []  # ✅ Clear processed emails
        else:
            print("⏳ No new emails to process.")

        print("🕒 Waiting for 180 seconds before next run...")
        time.sleep(180)


def kickoff():
    """Run the flow."""
    print("🚀 Starting Email Auto-Responder Flow...")
    email_auto_response_flow = EmailAutoResponderFlow()
    email_auto_response_flow.kickoff()


def plot_flow():
    """Plot the flow."""
    email_auto_response_flow = EmailAutoResponderFlow()
    email_auto_response_flow.plot()


if __name__ == "__main__":
    kickoff()
