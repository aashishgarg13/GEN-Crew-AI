# tools/trip_planning_tools.py
from langchain_core.tools import StructuredTool

class TripPlanningTools:
    def get_current_weather(self, location: str) -> str:
        """Useful to get the current weather in a given location."""
        return f"The weather in {location} is good."

    def get_popular_attractions(self, location: str) -> str:
        """Useful to get the popular attractions in a given location."""
        return f"Popular attractions in {location} are Red Fort, Qutub Minar, and Humayun's Tomb."

    def get_hotel_recommendations(self, location: str) -> str:
        """Useful to get hotel recommendations in a given location."""
        return f"Hotel recommendations in {location} are The Imperial, The Leela Palace, and Oberoi."

    def get_restaurant_recommendations(self, location: str) -> str:
        """Useful to get restaurant recommendations in a given location."""
        return f"Restaurant recommendations in {location} are Bukhara, Indian Accent, and Karim's."

    def get_tools(self):
        return [
            StructuredTool.from_function(
                func=self.get_current_weather,
                name="Get Current Weather",
                description="Useful to get the current weather in a given location.",
            ),
            StructuredTool.from_function(
                func=self.get_popular_attractions,
                name="Get Popular Attractions",
                description="Useful to get the popular attractions in a given location.",
            ),
            StructuredTool.from_function(
                func=self.get_hotel_recommendations,
                name="Get Hotel Recommendations",
                description="Useful to get hotel recommendations in a given location.",
            ),
            StructuredTool.from_function(
                func=self.get_restaurant_recommendations,
                name="Get Restaurant Recommendations",
                description="Useful to get restaurant recommendations in a given location.",
            ),
        ]
