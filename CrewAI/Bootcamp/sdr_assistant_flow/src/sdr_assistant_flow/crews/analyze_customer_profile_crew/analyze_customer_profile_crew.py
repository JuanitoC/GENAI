from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

from src.sdr_assistant_flow.lead_types import LeadReadinessResult

@CrewBase
class AnalyzeCustomerProfileCrew:
    """Crew that analyzes a new lead's personal and company profile to assess outreach readiness."""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # === Agents ===
    @agent
    def profile_insights_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['profile_insights_agent'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True
        )

    @agent
    def business_context_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['business_context_agent'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True
        )

    @agent
    def engagement_readiness_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['engagement_readiness_agent'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True
        )

    # === Tasks ===
    @task
    def build_lead_profile_task(self) -> Task:
        return Task(
            config=self.tasks_config['build_lead_profile'],
            agent=self.profile_insights_agent()
        )

    @task
    def assess_engagement_fit_task(self) -> Task:
        return Task(
            config=self.tasks_config['assess_engagement_fit'],
            agent=self.business_context_agent()
        )

    @task
    def generate_lead_readiness_score_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_lead_readiness_score'],
            agent=self.engagement_readiness_agent(),
            context=[
                self.build_lead_profile_task(),
                self.assess_engagement_fit_task()
            ],
            output_pydantic=LeadReadinessResult
        )

    # === Crew Composition ===
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
