from crewai import Agent, Crew, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from crewai_tools import SerperDevTool, ScrapeWebsiteTool

import os
from dotenv import load_dotenv

load_dotenv()

scrape_tool = ScrapeWebsiteTool()
serper_tool = SerperDevTool()

llm = LLM(
    model="gemini-2.5-flash",
    temperature=0.2,
    max_tokens=4000,
    api_key=os.getenv("GEMINI_API_KEY")
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
    def travel_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_specialist'],
            verbose=True,
            tools=[serper_tool, scrape_tool],
            llm=llm
        )
    
    @agent
    def city_selection(self) -> Agent:
        return Agent(
            config=self.agents_config['city_selection'],
            verbose=True,
            tools=[serper_tool, scrape_tool],
            llm=llm
        )
    
    @agent
    def local_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['local_expert'],
            verbose=True,
            tools=[serper_tool, scrape_tool],
            llm=llm
        )
    
    @task
    def input_analyzer_task(self) -> Task:
        return Task(config=self.tasks_config['input_analyzer'])
    
    @task
    def travel_specialist_task(self) -> Task:
        return Task(config=self.tasks_config['plan_travel_itinerary'])
    
    @task
    def city_selection_task(self) -> Task:
        return Task(config=self.tasks_config['select_city'])
    
    @task
    def local_expert_task(self) -> Task:
        return Task(config=self.tasks_config['local_insights'])


    @crew
    def travel_planning_crew(self) -> Crew:
        return Crew(
            agents=[self.input_analyzer(), self.travel_specialist(), self.city_selection(), self.local_expert()],
            tasks=[self.input_analyzer_task(), self.travel_specialist_task(), self.city_selection_task(), self.local_expert_task()],
            llm=llm,
            verbose=True
        )