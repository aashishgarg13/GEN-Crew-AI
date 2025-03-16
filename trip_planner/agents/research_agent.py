# agents/research_agent.py
from crewai import Agent
from llm.gemini_llm import GeminiLLM
from tools.trip_planning_tools import TripPlanningTools

class ResearchAgent:
    def __init__(self):
        self.llm = GeminiLLM()
        self.tools = TripPlanningTools()
        self.agent = self.create_agent()

    def create_agent(self):
        return Agent(
            role="Travel Research Expert",
            goal="Research and gather information about travel destinations, including weather, attractions, hotels, and restaurants.",
            backstory="You are a seasoned travel researcher with a knack for finding the best information about any travel destination.",
            verbose=True,
            llm=self.llm.llm,
            tools=self.tools.get_tools(),
        )
