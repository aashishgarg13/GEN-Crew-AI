# app.py
import streamlit as st
from crewai import Crew, Task
from agents.research_agent import ResearchAgent
from agents.travel_agent import TravelAgent
from dotenv import load_dotenv
import re

load_dotenv()

st.title("Trip Advisor")

location = st.text_input("Enter the location:")
duration = st.number_input("Enter the duration (in days):", min_value=1, value=7)
interests = st.text_input("Enter your interests (e.g., history, food, nature):")

def extract_final_plan(text):
    """Extracts the final trip plan from the CrewAI output."""
    # 1. Try to find a "Final Answer:" section
    match = re.search(r"Final Answer:\s*(.*?)(?=\n\n|$)", text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # 2. If no "Final Answer:", look for the last block of text that might be the plan
    blocks = re.split(r"\n\n+", text)  # Split into blocks separated by two or more newlines
    if blocks:
        last_block = blocks[-1].strip()
        # Check if the last block is too short to be a plan
        if len(last_block) > 50:  # Adjust this threshold as needed
            return last_block
        else:
            # If the last block is too short, try the second to last block
            if len(blocks) > 1:
                second_to_last_block = blocks[-2].strip()
                if len(second_to_last_block) > 50:
                    return second_to_last_block
                else:
                    return "No final trip plan found."
            else:
                return "No final trip plan found."
    else:
        return "No final trip plan found."

if st.button("Create Trip Plan"):
    if location and duration and interests:
        research_agent = ResearchAgent().agent
        travel_agent = TravelAgent().agent

        research_task = Task(
            description=f"Research the location {location} for {duration} days, focusing on {interests}.",
            agent=research_agent,
            expected_output="A detailed report about the location, including weather, attractions, hotels, and restaurants.",
        )

        plan_task = Task(
            description=f"Create a detailed trip plan for {location} for {duration} days, focusing on {interests}. Use the research provided to create the plan.",
            agent=travel_agent,
            expected_output="A detailed trip plan for the given location, duration, and interests.",
        )

        crew = Crew(
            agents=[research_agent, travel_agent],
            tasks=[research_task, plan_task],
            verbose=True,
        )

        with st.spinner("Creating your trip plan..."):
            try:
                result = crew.kickoff()
                final_plan = extract_final_plan(result)
                st.markdown(final_plan)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.error("Please fill in all the fields.")
