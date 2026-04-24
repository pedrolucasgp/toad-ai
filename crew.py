from crewai import Agent, Crew, Task, LLM, Process
from crewai.project import CrewBase, agent, crew, task

from crewai_tools import SerperDevTool, ScrapeWebsiteTool

import os

from dotenv import load_dotenv

load_dotenv()

scrape_tool = ScrapeWebsiteTool()
serper_tool = SerperDevTool()

llm = LLM(
    model="azure/gpt-4o-2024-11-20",
    temperature=0.2,
    max_tokens=2000,
    api_key=os.getenv("AZURE_API_KEY"),
    api_base=os.getenv("AZURE_API_BASE"),
    api_version=os.getenv("AZURE_API_VERSION")
)

@CrewBase
class TravelCrew():
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def input_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['input_analyzer'],
            verbose=True,
            llm=llm
        )
    
    @agent
    def destination_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['destination_expert'],
            verbose=True,
            tools=[serper_tool, scrape_tool],
            llm=llm
        )
    
    @agent
    def toad(self) -> Agent:
        return Agent(
            config=self.agents_config['toad'],
            verbose=True,
            llm=llm
        )
    
    @task
    def input_analyzer_task(self) -> Task:
        return Task(config=self.tasks_config['input_analyzer'])
    
    @task
    def destination_expert_task(self) -> Task:
        task = Task(config=self.tasks_config['destination_expert_comprehensive'])
        return task
    
    @task
    def toad_compilation_task(self) -> Task:
        task = Task(config=self.tasks_config['toad_compilation'])
        task.context = [self.destination_expert_task()]
        return task


    @crew
    def travel_planning_crew(self) -> Crew:
        return Crew(
            agents=[self.input_analyzer(), self.destination_expert(), self.toad()],
            tasks=[self.input_analyzer_task(), self.destination_expert_task(), self.toad_compilation_task()],
            llm=llm,
            verbose=True,
            process=Process.sequential
        )