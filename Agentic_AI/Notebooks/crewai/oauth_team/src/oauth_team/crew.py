from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class OauthTeam():
    """OauthTeam crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'],
            verbose=True,
        )
    
    @agent
    def backend_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_developer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode='safe', # Uses Docker for safety
            max_execution_time=120,
            max_retry_limit=3
        )
    
    @agent
    def frontend_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_developer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode='safe', # Uses Docker for safety
            max_execution_time=120,
            max_retry_limit=3
        )
        
    @agent
    def backend_unit_test_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_unit_test_developer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode='safe',
            max_execution_time=120,
            max_retry_limit=3
        )
        
    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task']
        )
        
    @task
    def backend_developer_task(self) -> Task:
        return Task(
            config=self.tasks_config['backend_developer_task']
        )
    
    @task
    def frontend_developer_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_developer_task']
        )
    
    @task
    def backend_unit_test_developer_task(self) -> Task:
        return Task(
            config=self.tasks_config['backend_unit_test_developer_task']
        )    

  
    @crew
    def crew(self) -> Crew:
        """Creates the oauth for crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,

        )
