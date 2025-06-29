from datetime import UTC, datetime

from pydantic import BaseModel, Field


class CreateTaskRequestBody(BaseModel):
    file_path: str = Field(
        description="Path for file",
        examples=["C:\\users\\user\\Downloads\\my.pcap"],
    )
