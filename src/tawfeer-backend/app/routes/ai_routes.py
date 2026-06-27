"""
Tawfeer Backend - AI Routes
OpenAI-powered recipe generation and food Q&A.
"""
from fastapi import APIRouter, HTTPException, status

from app.models.ai import (
    AIRecipeRequest, AIRecipeResponse, AIRecipeSuggestion,
    AIQuestionRequest, AIQuestionResponse
)
from app.services.openai_service import generate_recipe_suggestions, answer_food_question

router = APIRouter(prefix="/api/ai", tags=["AI Assistant"])


@router.post("/recipes", response_model=AIRecipeResponse)
async def get_recipe_suggestions(request: AIRecipeRequest):
    """
    Get AI-generated recipe suggestions based on ingredients.

    This endpoint connects to the OpenAI API to generate creative recipe
    suggestions based on the ingredients provided by the user. It supports
    both English and Arabic languages.

    - **ingredients**: Comma-separated list of available ingredients
    - **language**: Response language ('en' or 'ar')
    """
    if not request.ingredients.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please enter your ingredients"
        )

    suggestions = await generate_recipe_suggestions(
        ingredients=request.ingredients,
        language=request.language
    )

    return AIRecipeResponse(
        suggestions=suggestions,
        ingredients_used=request.ingredients
    )


@router.post("/ask", response_model=AIQuestionResponse)
async def ask_food_question(request: AIQuestionRequest):
    """
    Ask AI a food-related question.

    This endpoint uses OpenAI to answer food-related questions such as:
    - What can I cook with specific ingredients?
    - How to store food properly?
    - Food safety tips
    - Cooking techniques and tips

    - **question**: The food-related question
    - **language**: Response language ('en' or 'ar')
    """
    if not request.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please enter your question"
        )

    answer = await answer_food_question(
        question=request.question,
        language=request.language
    )

    return AIQuestionResponse(answer=answer)
