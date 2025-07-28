import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool, RagTool, FileReadTool
from crewai.knowledge.source.crew_docling_source import CrewDoclingSource
#from tools.calculator_tool import calculate #? doesn't read calculator_tool.py

from langchain_openai import ChatOpenAI
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Powerpoint_Helper():
    """Powerpoint_Helper crew"""

    #agents_config = "config/agents.yaml" 
    # ?Is this needed?

    os.environ["OPENAI_API_KEY"] = "sk-proj-dummy"
    # Check if the .env executes before the following line
    llm = ChatOpenAI(
        model="llama3.2:3b",
        base_url = "http://localhost:11434/v1",  # Replace with your LLM server URL
    )

    agents: [BaseAgent] # type: ignore
    tasks: [Task] # type: ignore

    print ("## What is the company you'd like to analyze?##")
    search_input = input("Enter the company name: ")
    
    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def financial_researcher(self) -> Agent:
        # Create tools
        search_tool = SerperDevTool()
        #rag_tool = RagTool()
        file_read_tool = CrewDoclingSource()

        return Agent(
            config=self.agents_config['financial_researcher'], # type: ignore[index]
            verbose=False,
            llm = self.llm,
            tools = [search_tool, file_read_tool]  # Adding tools to the researcher agent
        )

    @agent
    def powerpoint_builder(self) -> Agent:
        return Agent(
            config=self.agents_config['powerpoint_builder'], # type: ignore[index]
            verbose=True,
            llm = self.llm
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def query_data(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def plot_graph(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Powerpoint_Helper crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
