"""
Tawfeer Backend - Pydantic Models for AI Recipe Generation
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class AIRecipeRequest(BaseModel):
    """Request for AI recipe suggestions based on ingredients."""
    ingredients: str = Field(..., min_length=1, description="Comma-separated list of ingredients")
    language: str = Field(default="en", description="Language for response: 'en' or 'ar'")

    class Config:
        json_schema_extra = {
            "example": {
                "ingredients": "rice, chicken, tomato",
                "language": "en"
            }
        }


class AIRecipeStep(BaseModel):
    """Single recipe step."""
    step_number: int
    instruction: str


class AIRecipeSuggestion(BaseModel):
    """Single recipe suggestion from AI."""
    title: str
    emoji: str
    prep_time: str
    difficulty: str
    steps: List[AIRecipeStep]
    result: str


class AIRecipeResponse(BaseModel):
    """Response containing AI-generated recipe suggestions."""
    suggestions: List[AIRecipeSuggestion]
    ingredients_used: str


class AIQuestionRequest(BaseModel):
    """Ask AI a food-related question."""
    question: str = Field(..., min_length=1)
    language: str = Field(default="en")

    class Config:
        json_schema_extra = {
            "example": {
                "question": "What can I cook with rice and tomato?",
                "language": "en"
            }
        }


class AIQuestionResponse(BaseModel):
    """AI answer to a food-related question."""
    answer: str
