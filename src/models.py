"""Models for object serialization and data validation in the app.

Define Pydantic models for Todo items and Todo creation requests.
Pydantic is a library for data validation and serialization using
Python type annoatations. It is often used with FastAPI and SqlAlchemy..
"""
from pydantic import BaseModel, Field, field_validator

MIN_TEXT_LENGTH = 2


class TodoCreate(BaseModel):
    """Information required to create a new Todo item.
    
    The application will assign an ID when the Todo is created.

    :param done: indicates if this Todo is completed or not. 
    """
    text: str = Field(
        ...,
        min_length=3,
        max_length=200,
        title="Description",
        description="Describes the thing to do",
        examples=["Learn REST in Python"],
    )
    done: bool = Field(False,
       description="Indicates if this Todo is completed or not")

    @field_validator("text")
    def validate_text(cls, v: str) -> str:
        """Ensure `text` field is at least MIN_TEXT_LENGTH characters and not blank."""
        if not isinstance(v, str):
            raise TypeError("text must be a string")
        v = v.strip()
        if len(v) < MIN_TEXT_LENGTH:
            raise ValueError(f"text must be at least {MIN_TEXT_LENGTH} characters long")
        return v


class Todo(TodoCreate):
    """A Todo item with an ID."""
    id: int
    # other fields inherited from TodoCreate
