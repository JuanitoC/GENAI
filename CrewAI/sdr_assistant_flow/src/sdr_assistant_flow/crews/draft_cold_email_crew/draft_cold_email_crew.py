from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from src.sdr_assistant_flow.lead_types import LeadReadinessResult

@CrewBase
class DraftColdEmailCrew:
    """Crew that crafts and optimizes personalized cold outreach emails based on lead profile and readiness."""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # === Agents ===
    @agent
    def cold_email_copywriter(self) -> Agent:
        return Agent(
            config=self.agents_config['cold_email_copywriter'],
            verbose=True
        )

    @agent
    def conversion_focus_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['conversion_focus_agent'],
            verbose=True
        )

    # === Tasks ===
    @task
    def draft_personalized_cold_email(self) -> Task:
        return Task(
            config=self.tasks_config['draft_personalized_cold_email'],
            agent=self.cold_email_copywriter()
        )

    @task
    def optimize_for_response(self) -> Task:
        return Task(
            config=self.tasks_config['optimize_for_response'],
            agent=self.conversion_focus_agent(),
            context=[self.draft_personalized_cold_email()]
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
