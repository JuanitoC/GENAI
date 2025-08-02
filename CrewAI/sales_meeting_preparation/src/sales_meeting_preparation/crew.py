import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool

# Set model override
groq_llm = "groq/llama-3.3-70b-versatile"

@CrewBase
class SalesMeetingPreparation:
    """Crew for preparing a pre-sales meeting report"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def company_research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['company_research_agent'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            llm=groq_llm
        )

    @agent
    def executive_profile_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['executive_profile_agent'],
            tools=[SerperDevTool(), WebsiteSearchTool()],
            llm=groq_llm
        )

    @agent
    def sales_pitch_strategist_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['sales_pitch_strategist_agent'],
            tools=[SerperDevTool()],
            llm=groq_llm
        )

    @agent
    def report_quality_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['report_quality_agent']
        )

    @task
    def research_company_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_company'],
            agent=self.company_research_agent()
        )

    @task
    def profile_executive_task(self) -> Task:
        return Task(
            config=self.tasks_config['profile_executive'],
            agent=self.executive_profile_agent()
        )

    @task
    def generate_sales_pitch_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_sales_pitch'],
            agent=self.sales_pitch_strategist_agent(),
            context=[
                self.research_company_task(),
                self.profile_executive_task()
            ]
        )

    @task
    def finalize_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['finalize_report'],
            agent=self.report_quality_agent(),
            context=[
                self.research_company_task(),
                self.profile_executive_task(),
                self.generate_sales_pitch_task()
            ]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
