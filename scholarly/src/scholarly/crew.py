from crewai import Crew, Process
from crewai.project import CrewBase, crew

@CrewBase
class Scholarly():
    """Scholarly crew (YAML-driven)"""

    @crew
    def crew(self) -> Crew:
        """Loads crew from YAML configuration"""
        return Crew(
            config_files=[
                "src/scholarly/config/agents.yaml",
                "src/scholarly/config/tasks.yaml"
            ],
            process=Process.sequential,  # or hierarchical if preferred
            verbose=True
        )
