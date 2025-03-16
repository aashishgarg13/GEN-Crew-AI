# agents/travel_agent.py
from crewai import Agent
from llm.gemini_llm import GeminiLLM

class TravelAgent:
    def __init__(self):
        self.llm = GeminiLLM()
        self.agent = self.create_agent()

    def create_agent(self):
        return Agent(
            role="Travel Planner",
            goal="Create detailed travel plans based on the research provided.",
            backstory="You are an expert travel planner who can create detailed itineraries for any destination.",
            verbose=True,
            llm=self.llm.llm,
        )
