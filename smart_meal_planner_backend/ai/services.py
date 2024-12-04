from typing import List, Dict, Any, Optional
import openai
import json
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import User, Recipe, InventoryItem
from config import OPENAI_API_KEY
from datetime import datetime
import logging
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_api_key():
    """Validate that the OpenAI API key is properly configured"""
    if not OPENAI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable."
        )

def handle_openai_error(func):
    """Decorator to handle OpenAI API errors gracefully"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            validate_api_key()
            return await func(*args, **kwargs)
        except openai.BadRequestError as e:
            logger.error(f"Invalid request to OpenAI API: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except openai.AuthenticationError:
            logger.error("OpenAI API authentication failed")
            raise HTTPException(status_code=500, detail="API authentication failed")
        except openai.RateLimitError as e:
            logger.error(f"OpenAI API rate limit exceeded: {str(e)}")
            # Re-raise the original exception to be handled by the global exception handler
            raise
        except openai.APIStatusError as e:
            logger.error(f"OpenAI API status error: {str(e)}")
            if e.status_code == 429:
                # Convert to RateLimitError to be handled by the global exception handler
                raise openai.RateLimitError(
                    message=str(e),
                    response=e.response,
                    body=e.body
                )
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding OpenAI response: {str(e)}")
            raise HTTPException(status_code=500, detail="Invalid response format from AI service")
        except Exception as e:
            logger.error(f"Unexpected error in AI service: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    return wrapper

# Initialize OpenAI API key with validation
validate_api_key()
openai.api_key = OPENAI_API_KEY

class AIService:
    RECIPE_TEMPLATE = {
        "name": str,
        "description": str,
        "ingredients": list,
        "instructions": list,
        "prep_time": int,
        "difficulty": str,
        "nutrition": dict
    }

    MEAL_PLAN_TEMPLATE = {
        "meal_plan": {
            "days": list,
            "shopping_list": list,
            "total_cost": float
        }
    }

    NUTRITION_TEMPLATE = {
        "nutrition": {
            "macronutrients": {
                "calories": float,
                "protein": float,
                "carbs": float,
                "fat": float,
                "fiber": float
            },
            "micronutrients": {
                "vitamins": dict,
                "minerals": dict
            },
            "dietary_analysis": {
                "protein_quality": str,
                "carb_quality": str,
                "fat_quality": str,
                "fiber_adequacy": str,
                "vitamin_adequacy": str,
                "mineral_adequacy": str,
                "recommendations": list
            }
        }
    }

    SUBSTITUTION_TEMPLATE = {
        "substitutions": list
    }

    FUSION_TEMPLATE = {
        "fusion_recipe": {
            "name": str,
            "description": str,
            "cuisine_influences": list,
            "ingredients": list,
            "instructions": list,
            "cooking_techniques": list,
            "prep_time": int,
            "difficulty": str,
            "nutrition": dict,
            "fusion_notes": list,
            "pairing_suggestions": list
        }
    }

    TUTORIAL_TEMPLATE = {
        "tutorial": {
            "technique": dict,
            "steps": list,
            "variations": list,
            "practice_exercises": list,
            "troubleshooting": list
        }
    }

    SEASONAL_MENU_TEMPLATE = {
        "seasonal_menu": {
            "season": str,
            "theme": str,
            "occasion": str,
            "menu_sections": list,
            "wine_pairings": list,
            "timing_guide": dict,
            "presentation_tips": list,
            "estimated_costs": dict
        }
    }

    OPTIMIZATION_TEMPLATE = {
        "optimized_meal_plan": {
            "goal": "",
            "daily_targets": {
                "calories": 0.0,
                "protein": 0.0,
                "carbs": 0.0,
                "fat": 0.0,
                "fiber": 0.0
            },
            "meals": [
                {
                    "meal_type": "",
                    "timing": "",
                    "recipes": [
                        {
                            "recipe": {
                                "name": "",
                                "description": "",
                                "ingredients": [],
                                "instructions": [],
                                "prep_time": 0,
                                "difficulty": "",
                                "nutrition": {
                                    "calories": 0.0,
                                    "protein": 0.0,
                                    "carbs": 0.0,
                                    "fat": 0.0
                                }
                            },
                            "portion_size": 0.0,
                            "contribution_to_goals": {
                                "calories": 0.0,
                                "protein": 0.0,
                                "carbs": 0.0,
                                "fat": 0.0
                            },
                            "timing_notes": "",
                            "pre_post_workout": False
                        }
                    ],
                    "nutritional_balance": "",
                    "meal_synergy": ""
                }
            ],
            "supplements": [
                {
                    "name": "",
                    "timing": "",
                    "dosage": "",
                    "purpose": "",
                    "notes": ""
                }
            ],
            "hydration_plan": {
                "daily_water": 0.0,
                "electrolytes": False,
                "timing_guidelines": []
            },
            "progress_tracking": {
                "metrics": [],
                "measurement_frequency": "",
                "expected_progress": ""
            }
        }
    }

    ADAPTATION_TEMPLATE = {
        "adapted_recipe": {
            "original_difficulty": str,
            "adapted_difficulty": str,
            "simplifications": list,
            "equipment_substitutions": list,
            "technique_breakdown": list,
            "timing_adjustments": dict,
            "recipe": dict,
            "confidence_building_steps": list,
            "common_mistakes_prevention": list
        }
    }

    @staticmethod
    def _format_recipe_prompt(inventory_text: str, ingredients: List[str], prefs: str, restrictions: str) -> str:
        example_recipe = {
            "name": "Example Recipe",
            "description": "A sample recipe",
            "ingredients": [
                {"name": "ingredient", "quantity": 100, "unit": "g"}
            ],
            "instructions": ["Step 1"],
            "prep_time": 30,
            "difficulty": "medium",
            "nutrition": {
                "calories": 500,
                "protein": 20,
                "carbs": 50,
                "fat": 15
            }
        }

        prompt_parts = [
            "As a professional chef, suggest 3 recipes based on these ingredients:",
            inventory_text,
            "\nAdditional ingredients mentioned:",
            ", ".join(ingredients)
        ]

        if prefs:
            prompt_parts.append("\nUser preferences:\n" + prefs)
        if restrictions:
            prompt_parts.append("\nDietary restrictions:\n" + restrictions)

        prompt_parts.extend([
            "\nFor each recipe, provide:",
            "1. Name",
            "2. Description",
            "3. Ingredients with quantities",
            "4. Step-by-step instructions",
            "5. Preparation time",
            "6. Difficulty level (Easy/Medium/Hard)",
            "7. Nutritional information (calories, protein, carbs, fat)",
            "\nFormat as JSON:",
            json.dumps({"recipes": [example_recipe]}, indent=2)
        ])

        return "\n".join(prompt_parts)

    @staticmethod
    def _format_meal_plan_prompt(
        days: int,
        meals_per_day: int,
        recipes_text: str,
        prefs: str,
        restrictions: str,
        budget: float = None
    ) -> str:
        prompt_parts = [
            f"Create a {days}-day meal plan with {meals_per_day} meals per day.",
            "\nUser's favorite recipes:",
            recipes_text
        ]

        if prefs:
            prompt_parts.append("\nUser preferences:\n" + prefs)
        if restrictions:
            prompt_parts.append("\nDietary restrictions:\n" + restrictions)
        if budget:
            prompt_parts.append(f"\nBudget constraint: ${budget} total")

        prompt_parts.extend([
            "\nConsider:",
            "1. Nutritional balance",
            "2. Variety in meals",
            "3. Prep time",
            "4. Ingredient availability",
            "5. Cost-effectiveness"
        ])

        if budget:
            prompt_parts.append("6. Budget constraints")

        prompt_parts.extend([
            "\nFormat as JSON:",
            json.dumps(AIService.MEAL_PLAN_TEMPLATE, indent=2)
        ])

        return "\n".join(prompt_parts)

    @staticmethod
    async def suggest_recipes(
        db: Session,
        user: User,
        ingredients: List[str],
        preferences: Dict[str, Any] = None,
        dietary_restrictions: List[str] = None
    ) -> Dict[str, Any]:
        """
        Suggest recipes based on available ingredients and user preferences.
        """
        # Get user's inventory items
        inventory_items = db.query(InventoryItem).filter(
            InventoryItem.user_id == user.id
        ).all()
        
        # Format inventory for prompt
        inventory_text = "\n".join([
            f"- {item.name}: {item.quantity} {item.unit}"
            for item in inventory_items
        ])
        
        # Format preferences and restrictions
        prefs = "\n".join([f"- {k}: {v}" for k, v in (preferences or {}).items()])
        restrictions = "\n".join([f"- {r}" for r in (dietary_restrictions or [])])
        
        # Construct prompt
        prompt = AIService._format_recipe_prompt(
            inventory_text,
            ingredients,
            prefs,
            restrictions
        )

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional chef and nutritionist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Parse and validate response
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error generating recipe suggestions: {str(e)}"
            )
    
    @staticmethod
    async def generate_meal_plan(
        db: Session,
        user: User,
        days: int = 7,
        meals_per_day: int = 3,
        preferences: Dict[str, Any] = None,
        dietary_restrictions: List[str] = None,
        budget: float = None
    ) -> Dict[str, Any]:
        """
        Generate a personalized meal plan based on user preferences and restrictions.
        """
        # Get user's existing recipes
        user_recipes = db.query(Recipe).filter(Recipe.user_id == user.id).all()
        recipes_text = "\n".join([
            f"- {recipe.name}: {recipe.description}"
            for recipe in user_recipes[:5]  # Include a few examples of user's recipes
        ])
        
        # Format preferences and restrictions
        prefs = "\n".join([f"- {k}: {v}" for k, v in (preferences or {}).items()])
        restrictions = "\n".join([f"- {r}" for r in (dietary_restrictions or [])])
        
        # Construct prompt
        prompt = AIService._format_meal_plan_prompt(
            days,
            meals_per_day,
            recipes_text,
            prefs,
            restrictions,
            budget
        )

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional chef and nutritionist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            # Parse and validate response
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error generating meal plan: {str(e)}"
            )

    @staticmethod
    async def scale_recipe(
        recipe: Dict[str, Any],
        target_servings: float,
        original_servings: float = 1.0
    ) -> Dict[str, Any]:
        """
        Scale recipe ingredients for a different number of servings while maintaining proportions
        and adjusting instructions accordingly.
        """
        prompt = f"""Scale this recipe from {original_servings} to {target_servings} servings.
Adjust ingredient quantities proportionally and modify instructions if needed.
Consider any special scaling factors for seasonings or leavening agents.

Original recipe:
{json.dumps(recipe, indent=2)}

Format the response as JSON with the same structure as the input recipe.
Ensure instructions are updated to reflect new quantities."""

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional chef expert in recipe scaling."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for more precise scaling
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error scaling recipe: {str(e)}"
            )

    @staticmethod
    async def analyze_nutrition(
        recipe: Dict[str, Any],
        user_info: Optional[Dict[str, Any]] = None,
        health_goals: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Provide detailed nutritional analysis of a recipe, including macro and micronutrients,
        and personalized dietary recommendations based on user info and health goals.
        """
        prompt_parts = [
            "Provide a detailed nutritional analysis of this recipe:",
            json.dumps(recipe, indent=2),
        ]

        if user_info:
            prompt_parts.append("\nUser Information:")
            prompt_parts.extend([f"- {k}: {v}" for k, v in user_info.items()])

        if health_goals:
            prompt_parts.append("\nHealth Goals:")
            prompt_parts.extend([f"- {goal}" for goal in health_goals])

        prompt_parts.extend([
            "\nProvide:",
            "1. Complete macro and micronutrient breakdown",
            "2. Analysis of nutritional quality",
            "3. Specific recommendations for improvement",
            "4. Potential health benefits and concerns",
            "\nFormat as JSON:",
            json.dumps(AIService.NUTRITION_TEMPLATE, indent=2)
        ])

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a registered dietitian and nutritionist."
                    },
                    {"role": "user", "content": "\n".join(prompt_parts)}
                ],
                temperature=0.3,  # Lower temperature for more accurate analysis
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error analyzing nutrition: {str(e)}"
            )

    @staticmethod
    async def suggest_substitutions(
        recipe: Dict[str, Any],
        ingredients_to_replace: List[str],
        dietary_restrictions: Optional[List[str]] = None,
        available_ingredients: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Suggest suitable substitutions for ingredients in a recipe.
        Considers dietary restrictions and available ingredients.
        Provides detailed conversion ratios and cooking adjustments.
        """
        prompt_parts = [
            "Suggest substitutions for the following ingredients in this recipe:",
            json.dumps(recipe, indent=2),
            "\nIngredients to replace:",
            ", ".join(ingredients_to_replace)
        ]

        if dietary_restrictions:
            prompt_parts.extend([
                "\nDietary restrictions:",
                ", ".join(dietary_restrictions)
            ])

        if available_ingredients:
            prompt_parts.extend([
                "\nAvailable ingredients:",
                ", ".join(available_ingredients)
            ])

        prompt_parts.extend([
            "\nFor each substitution, provide:",
            "1. Exact conversion ratios",
            "2. Impact on flavor and texture",
            "3. Nutritional differences",
            "4. Required cooking adjustments",
            "\nFormat as JSON:",
            json.dumps(AIService.SUBSTITUTION_TEMPLATE, indent=2)
        ])

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional chef expert in ingredient substitutions."
                    },
                    {"role": "user", "content": "\n".join(prompt_parts)}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error suggesting substitutions: {str(e)}"
            )

    @staticmethod
    async def create_fusion_recipe(
        recipe1: Dict[str, Any],
        recipe2: Dict[str, Any],
        fusion_style: Optional[str] = None,
        preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a fusion recipe by combining elements from two different recipes.
        Intelligently merges ingredients, techniques, and flavors while maintaining
        culinary harmony and respecting the essence of both source recipes.
        """
        prompt_parts = [
            "Create a fusion recipe by combining these two recipes:",
            "\nRecipe 1:",
            json.dumps(recipe1, indent=2),
            "\nRecipe 2:",
            json.dumps(recipe2, indent=2)
        ]

        if fusion_style:
            prompt_parts.extend([
                "\nDesired fusion style:",
                fusion_style
            ])

        if preferences:
            prompt_parts.extend([
                "\nPreferences:",
                json.dumps(preferences, indent=2)
            ])

        prompt_parts.extend([
            "\nCreate a fusion recipe that:",
            "1. Combines key elements from both recipes",
            "2. Maintains flavor harmony",
            "3. Uses appropriate cooking techniques",
            "4. Preserves the essence of both cuisines",
            "5. Provides clear instructions for fusion elements",
            "\nFormat as JSON:",
            json.dumps(AIService.FUSION_TEMPLATE, indent=2)
        ])

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional chef specializing in fusion cuisine."
                    },
                    {"role": "user", "content": "\n".join(prompt_parts)}
                ],
                temperature=0.7,  # Higher temperature for more creativity
                max_tokens=2500
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error creating fusion recipe: {str(e)}"
            )

    @staticmethod
    async def generate_technique_tutorial(
        technique_name: str,
        skill_level: str = "beginner",
        cuisine_context: Optional[str] = None,
        specific_dish: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a detailed tutorial for a cooking technique.
        Includes step-by-step instructions, tips, common mistakes,
        and practice exercises tailored to the user's skill level.
        """
        prompt_parts = [
            f"Create a detailed cooking tutorial for {technique_name}",
            f"Target skill level: {skill_level}"
        ]

        if cuisine_context:
            prompt_parts.append(f"\nCuisine context: {cuisine_context}")
        if specific_dish:
            prompt_parts.append(f"\nSpecific dish context: {specific_dish}")

        prompt_parts.extend([
            "\nInclude:",
            "1. Detailed step-by-step instructions",
            "2. Equipment needed and safety tips",
            "3. Common mistakes and how to avoid them",
            "4. Visual cues for success",
            "5. Practice exercises",
            "6. Troubleshooting guide",
            "\nFormat as JSON:",
            json.dumps(AIService.TUTORIAL_TEMPLATE, indent=2)
        ])

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional chef and cooking instructor."
                    },
                    {"role": "user", "content": "\n".join(prompt_parts)}
                ],
                temperature=0.5,
                max_tokens=2500
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error generating technique tutorial: {str(e)}"
            )

    @staticmethod
    async def create_seasonal_menu(
        season: str,
        occasion: Optional[str] = None,
        guests: int = 4,
        preferences: Optional[Dict[str, Any]] = None,
        dietary_restrictions: Optional[List[str]] = None,
        budget_per_person: Optional[float] = None,
        location: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a seasonal menu plan with timing, presentation tips,
        and wine pairings based on the season and occasion.
        """
        current_date = datetime.now()
        
        prompt_parts = [
            f"Create a seasonal menu for {season}",
            f"Number of guests: {guests}"
        ]

        if occasion:
            prompt_parts.append(f"\nOccasion: {occasion}")
        if preferences:
            prompt_parts.append(f"\nPreferences: {json.dumps(preferences, indent=2)}")
        if dietary_restrictions:
            prompt_parts.append(f"\nDietary restrictions: {', '.join(dietary_restrictions)}")
        if budget_per_person:
            prompt_parts.append(f"\nBudget per person: ${budget_per_person}")
        if location:
            prompt_parts.append(f"\nLocation: {location}")

        prompt_parts.extend([
            "\nProvide:",
            "1. Menu sections with seasonal dishes",
            "2. Wine pairings and alternatives",
            "3. Detailed timing guide",
            "4. Presentation tips",
            "5. Cost estimates and budget alternatives",
            "\nFormat as JSON:",
            json.dumps(AIService.SEASONAL_MENU_TEMPLATE, indent=2)
        ])

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional chef and event planner."
                    },
                    {"role": "user", "content": "\n".join(prompt_parts)}
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error creating seasonal menu: {str(e)}"
            )

    @staticmethod
    @handle_openai_error
    async def optimize_meal_plan(
        goal: str,
        user_stats: Dict[str, Any],
        activity_level: str,
        preferences: Optional[Dict[str, Any]] = None,
        restrictions: Optional[List[str]] = None,
        existing_recipes: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Create an optimized meal plan for specific fitness/health goals.
        Takes into account user's stats, activity level, and preferences
        to create a scientifically-backed meal plan.
        """
        prompt_parts = [
            f"Create an optimized meal plan for {goal}",
            "\nUser Statistics:",
            json.dumps(user_stats, indent=2),
            f"\nActivity Level: {activity_level}"
        ]

        if preferences:
            prompt_parts.append("\nPreferences: " + json.dumps(preferences, indent=2))
        if restrictions:
            prompt_parts.append("\nRestrictions: " + ", ".join(restrictions))
        if existing_recipes:
            prompt_parts.append("\nExisting Recipes: " + json.dumps(existing_recipes, indent=2))

        prompt_parts.extend([
            "\nProvide:",
            "1. Detailed macro and micro nutrient targets",
            "2. Meal timing and portions",
            "3. Supplement recommendations",
            "4. Hydration guidelines",
            "5. Progress tracking metrics",
            "\nFormat as JSON:",
            json.dumps(AIService.OPTIMIZATION_TEMPLATE, indent=2)
        ])

        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional nutritionist and fitness expert."
                },
                {"role": "user", "content": "\n".join(prompt_parts)}
            ],
            temperature=0.4,  # Lower temperature for more precise recommendations
            max_tokens=2500
        )
        
        content = response.choices[0].message.content
        return json.loads(content)

    @staticmethod
    async def adapt_recipe_difficulty(
        recipe: Dict[str, Any],
        target_skill_level: str,
        user_equipment: Optional[List[str]] = None,
        time_constraints: Optional[int] = None,
        specific_techniques: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Adapt a recipe to match a user's skill level by simplifying techniques,
        suggesting equipment alternatives, and providing detailed guidance.
        """
        prompt_parts = [
            "Adapt this recipe for a different skill level:",
            json.dumps(recipe, indent=2),
            f"\nTarget Skill Level: {target_skill_level}"
        ]

        if user_equipment:
            prompt_parts.append("\nAvailable Equipment: " + ", ".join(user_equipment))
        if time_constraints:
            prompt_parts.append(f"\nTime Constraint: {time_constraints} minutes")
        if specific_techniques:
            prompt_parts.append("\nTechniques to Focus On: " + ", ".join(specific_techniques))

        prompt_parts.extend([
            "\nProvide:",
            "1. Simplified steps with explanations",
            "2. Equipment alternatives",
            "3. Detailed technique breakdowns",
            "4. Timing adjustments",
            "5. Confidence-building progression",
            "\nFormat as JSON:",
            json.dumps(AIService.ADAPTATION_TEMPLATE, indent=2)
        ])

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional chef and cooking instructor."
                    },
                    {"role": "user", "content": "\n".join(prompt_parts)}
                ],
                temperature=0.5,
                max_tokens=2500
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error adapting recipe difficulty: {str(e)}"
            ) 