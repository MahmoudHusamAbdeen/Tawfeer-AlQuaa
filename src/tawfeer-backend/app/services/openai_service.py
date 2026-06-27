"""
Tawfeer Backend - OpenAI Service
Handles AI recipe generation and food-related Q&A using the OpenAI API.
"""
import json
from typing import List
from openai import AsyncOpenAI

from app.config import get_settings
from app.models.ai import AIRecipeSuggestion, AIRecipeStep

settings = get_settings()

# Initialize OpenAI client
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def generate_recipe_suggestions(ingredients: str, language: str = "en") -> List[AIRecipeSuggestion]:
    """
    Generate recipe suggestions based on provided ingredients using OpenAI.

    Args:
        ingredients: Comma-separated list of available ingredients
        language: Response language ('en' for English, 'ar' for Arabic)

    Returns:
        List of AIRecipeSuggestion objects with recipe details
    """
    if language == "ar":
        system_prompt = """أنت طاهٍ محترف ومساعد ذكي للمطبخ الإماراتي والعربي.
عندما يعطيك المستخدم قائمة من المكونات، اقترح 3 وصفات يمكن تحضيرها بهذه المكونات.

أجب بتنسيق JSON فقط (بدون نص إضافي) بالهيكل التالي:
[
  {
    "title": "اسم الوصفة",
    "emoji": "رمز تعبيري مناسب",
    "prep_time": "XX دقيقة",
    "difficulty": "سهل/متوسط/صعب",
    "steps": [
      {"step_number": 1, "instruction": "خطوة التحضير"},
      {"step_number": 2, "instruction": "خطوة التحضير"}
    ],
    "result": "وصف نتيجة الوصفة"
  }
]

كن إبداعياً واقترح وصفات من المطبخ الإماراتي والعربي والهندي عند الإمكان.
تأكد من أن الوصفات عملية وسهلة التحضير مع المكونات المتاحة."""
    else:
        system_prompt = """You are a professional chef and smart kitchen assistant specializing in UAE, Arab, and Indian cuisine.
When given a list of ingredients, suggest 3 recipes that can be made with those ingredients.

Respond ONLY with valid JSON (no extra text) in this exact format:
[
  {
    "title": "Recipe Name",
    "emoji": "appropriate emoji",
    "prep_time": "XX mins",
    "difficulty": "Easy/Medium/Hard",
    "steps": [
      {"step_number": 1, "instruction": "Step instruction"},
      {"step_number": 2, "instruction": "Step instruction"}
    ],
    "result": "Description of the final dish"
  }
]

Be creative and suggest recipes from UAE, Arab, and Indian cuisine when possible.
Make sure recipes are practical and easy to prepare with the available ingredients."""

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"I have these ingredients: {ingredients}"}
            ],
            max_tokens=2000,
            temperature=0.8,
        )

        content = response.choices[0].message.content.strip()

        # Clean up the response - remove markdown code blocks if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()

        # Parse JSON response
        recipes_data = json.loads(content)

        suggestions = []
        for i, recipe in enumerate(recipes_data[:3]):  # Limit to 3 suggestions
            steps = []
            for step in recipe.get("steps", []):
                steps.append(AIRecipeStep(
                    step_number=step.get("step_number", len(steps) + 1),
                    instruction=step.get("instruction", "")
                ))

            suggestions.append(AIRecipeSuggestion(
                title=recipe.get("title", f"Recipe {i+1}"),
                emoji=recipe.get("emoji", "🍽️"),
                prep_time=recipe.get("prep_time", "30 mins"),
                difficulty=recipe.get("difficulty", "Medium"),
                steps=steps,
                result=recipe.get("result", "A delicious meal!")
            ))

        return suggestions

    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        # Return fallback suggestions if AI response parsing fails
        return _get_fallback_suggestions(ingredients, language)

    except Exception as e:
        print(f"OpenAI API error: {e}")
        return _get_fallback_suggestions(ingredients, language)


async def answer_food_question(question: str, language: str = "en") -> str:
    """
    Answer a food-related question using OpenAI.

    Args:
        question: The food-related question
        language: Response language

    Returns:
        AI-generated answer string
    """
    if language == "ar":
        system_prompt = """أنت مساعد ذكي متخصص في الطعام والطبخ.
أجب على الأسئلة المتعلقة بالطعام بشكل مختصر ومفيد.
يمكنك تقديم نصائح حول الوصفات وتخزين الطعام وسلامة الغذاء.
أجب باللغة العربية."""
    else:
        system_prompt = """You are a smart food and cooking assistant.
Answer food-related questions concisely and helpfully.
You can provide advice on recipes, food storage, and food safety.
Keep answers practical and easy to follow."""

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            max_tokens=500,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"OpenAI API error: {e}")
        if language == "ar":
            return "عذراً، لم أتمكن من معالجة سؤالك. يرجى المحاولة مرة أخرى لاحقاً."
        return "Sorry, I couldn't process your question. Please try again later."


def _get_fallback_suggestions(ingredients: str, language: str) -> List[AIRecipeSuggestion]:
    """Fallback suggestions when OpenAI API is unavailable."""
    if language == "ar":
        return [
            AIRecipeSuggestion(
                title="برياني دجاج",
                emoji="🍛",
                prep_time="45 دقيقة",
                difficulty="متوسط",
                steps=[
                    AIRecipeStep(step_number=1, instruction="تبل الدجاج بالزبادي والتوابل لمدة 30 دقيقة"),
                    AIRecipeStep(step_number=2, instruction="اقلي البصل حتى يصبح ذهبياً"),
                    AIRecipeStep(step_number=3, instruction="رتب الأرز والدجاج والبصل المقلي طبقات"),
                    AIRecipeStep(step_number=4, instruction="أضف حليب الزعفران واطبخ على نار هادئة لمدة 25 دقيقة"),
                ],
                result="أرز عطري بنكهة رائعة مع قطع دجاج طرية"
            ),
            AIRecipeSuggestion(
                title="كاري الطماطم بالدجاج",
                emoji="🍲",
                prep_time="35 دقيقة",
                difficulty="سهل",
                steps=[
                    AIRecipeStep(step_number=1, instruction="قلب البصل والثوم والزنجبيل"),
                    AIRecipeStep(step_number=2, instruction="أضف الطماطم المفرومة واطبخ حتى تنضج"),
                    AIRecipeStep(step_number=3, instruction="أضف الدجاج والتوابل واتركه يغلي ببطء"),
                    AIRecipeStep(step_number=4, instruction="قدم مع الأرز أو خبز النان"),
                ],
                result="كاري غني ولاذع مع دجاج طري في صلصة طماطم شهية"
            ),
            AIRecipeSuggestion(
                title="خليط الأرز بالخضروات",
                emoji="🥘",
                prep_time="20 دقيقة",
                difficulty="سهل",
                steps=[
                    AIRecipeStep(step_number=1, instruction="اسلق الأرز وضعه جانباً"),
                    AIRecipeStep(step_number=2, instruction="قلب الخضروات مثل الطماطم والبطاطا والبازلاء"),
                    AIRecipeStep(step_number=3, instruction="اخلط مع الأرز المطبوخ وتبل بالأعشاب والتوابل"),
                ],
                result="طبق أرز ملون ومغذي مليء بالخضروات والنكهات"
            ),
        ]

    return [
        AIRecipeSuggestion(
            title="Chicken Biryani",
            emoji="🍛",
            prep_time="45 mins",
            difficulty="Medium",
            steps=[
                AIRecipeStep(step_number=1, instruction="Marinate the chicken with yogurt and spices for 30 minutes."),
                AIRecipeStep(step_number=2, instruction="Fry onions until golden brown."),
                AIRecipeStep(step_number=3, instruction="Layer rice, marinated chicken, and fried onions."),
                AIRecipeStep(step_number=4, instruction="Add saffron milk and cook on low heat for 25 minutes."),
            ],
            result="Fragrant, flavorful rice dish with tender chicken pieces, perfect for special occasions."
        ),
        AIRecipeSuggestion(
            title="Tomato Chicken Curry",
            emoji="🍲",
            prep_time="35 mins",
            difficulty="Easy",
            steps=[
                AIRecipeStep(step_number=1, instruction="Saute onions, garlic, and ginger."),
                AIRecipeStep(step_number=2, instruction="Add chopped tomatoes and cook till soft."),
                AIRecipeStep(step_number=3, instruction="Add chicken and spices and simmer till done."),
                AIRecipeStep(step_number=4, instruction="Serve with rice or naan bread."),
            ],
            result="Rich, tangy curry with tender chicken in a flavorful tomato-based sauce."
        ),
        AIRecipeSuggestion(
            title="Vegetable Rice Mix",
            emoji="🥘",
            prep_time="20 mins",
            difficulty="Easy",
            steps=[
                AIRecipeStep(step_number=1, instruction="Boil rice and set aside."),
                AIRecipeStep(step_number=2, instruction="Saute vegetables like tomato, potato, and canned peas."),
                AIRecipeStep(step_number=3, instruction="Mix with cooked rice and season with herbs and spices."),
            ],
            result="Colorful, nutritious rice dish packed with vegetables and flavors."
        ),
    ]
