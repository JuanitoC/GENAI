#!/usr/bin/env python

import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

from pydantic import BaseModel
from typing import List

from crewai.flow import Flow, start, listen

from src.sdr_assistant_flow.crews.analyze_customer_profile_crew.analyze_customer_profile_crew import AnalyzeCustomerProfileCrew
from src.sdr_assistant_flow.crews.draft_cold_email_crew.draft_cold_email_crew import DraftColdEmailCrew

from src.sdr_assistant_flow.lead_types import LeadReadinessResult


# === Define the Flow State ===
class SDRFlowState(BaseModel):
    leads: List[dict] = []
    analyzed_leads: List[LeadReadinessResult] = []
    emails: List[str] = []


# === Define the Flow ===
class SDRAssistantFlow(Flow[SDRFlowState]):

    @start()
    def load_leads(self):
        print("Loading new leads...")
        self.state.leads = [
            {
                "lead_data": {
                    "name": "Mark Benioff",
                    "job_title": "CEO",
                    "company": "Salesforce",
                    "email": "mark@salesforce.com",
                    "use_case": "Exploring GenAI strategy for executive-level productivity"
                }
            }
        ]

    @listen(load_leads)
    def analyze_leads(self):
        print("Analyzing lead profiles...")
        results = []

        for lead in self.state.leads:
            result = AnalyzeCustomerProfileCrew().crew().kickoff(inputs={"lead_data": lead["lead_data"]})
            results.append(result.pydantic)

        self.state.analyzed_leads = results
        print("Analysis complete:", self.state.analyzed_leads)

    @listen(analyze_leads)
    def write_emails(self):
        print("Writing cold outreach emails...")
        emails = []

        for lead in self.state.analyzed_leads:
            lead_dict = lead.model_dump()
            result = DraftColdEmailCrew().crew().kickoff(inputs={
                "personal_info": lead_dict["personal_info"],
                "company_info": lead_dict["company_info"],
                "engagement_fit": lead_dict["engagement_fit"]
            })
            emails.append(result.raw)

        self.state.emails = emails
        print("Emails ready to send:", self.state.emails)

    @listen(write_emails)
    def simulate_send(self):
        print("Simulating email send...")
        for email in self.state.emails:
            print("Sent email:\n", email)


# === Entry Point Functions ===
def kickoff():
    flow = SDRAssistantFlow()
    flow.kickoff()


def plot():
    flow = SDRAssistantFlow()
    flow.plot()


if __name__ == "__main__":
    kickoff()
