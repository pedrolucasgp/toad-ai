from crew import TravelCrew

def run_crew(prompt: str):
    if not prompt:
        print("Please provide a prompt.")
        return
    
    crew_instance = TravelCrew()
    
    result = crew_instance.travel_planning_crew().kickoff(inputs={"user_input": prompt})

    return result