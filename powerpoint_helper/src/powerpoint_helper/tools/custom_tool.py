from crewai.tools import BaseTool
from crewai_tools import FileReadTool
from crewai.knowledge.source.crew_docling_source import CrewDoclingSource
from typing import Type
from pydantic import BaseModel, Field


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Read PDF Links"
    description: str = (
        "Read PDF Links from a text file"
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        file_reader = FileReadTool(file_path = "WEB_RESULT.txt")
        urls_content = file_reader._run() # Use _run() to directly get the content
        pdf_urls = [url.strip() for url in urls_content.split('\n') if url.strip()]

        # Create tools
        #rag_tool = RagTool()
        global content_source
        content_source = CrewDoclingSource(
            file_paths = [pdf_urls],
        )
        return "this is an example of a tool output, ignore it and move along."
