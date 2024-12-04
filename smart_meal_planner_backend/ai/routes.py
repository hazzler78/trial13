from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth.utils import get_current_active_user
from models import User
from . import schemas, services
from typing import List

router = APIRouter(prefix="/api/v1/ai", tags=["ai"])
ai_service = services.AIService()

def validate_ingredients(ingredients: List[str]):
    """Validate ingredients list"""
    if not ingredients:
        raise HTTPException(
            status_code=400,
            detail="Ingredients list cannot be empty"
        )

def validate_days(days: int):
    """Validate number of days for meal plan"""
    if days <= 0:
        raise HTTPException(
            status_code=400,
            detail="Days must be positive"
        )

@router.post("/recipes/suggest", response_model=schemas.RecipeSuggestionResponse)
@services.handle_openai_error
async def suggest_recipes(
    request: schemas.RecipeSuggestionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get AI-powered recipe suggestions based on available ingredients and preferences.
    """
    validate_ingredients(request.ingredients)
    suggestions = await ai_service.suggest_recipes(
        db,
        current_user,
        request.ingredients,
        request.preferences,
        request.dietary_restrictions
    )
    return suggestions

@router.post("/meal-plan", response_model=schemas.MealPlanResponse)
@services.handle_openai_error
async def generate_meal_plan(
    request: schemas.MealPlanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Generate an AI-powered personalized meal plan.
    """
    validate_days(request.days)
    meal_plan = await ai_service.generate_meal_plan(
        db,
        current_user,
        request.days,
        request.meals_per_day,
        request.preferences,
        request.dietary_restrictions,
        request.budget
    )
    return meal_plan

@router.post("/recipes/scale", response_model=schemas.RecipeScalingResponse)
async def scale_recipe(
    request: schemas.RecipeScalingRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Scale a recipe to a different number of servings.
    Adjusts ingredient quantities and instructions accordingly.
    """
    scaled_recipe = await ai_service.scale_recipe(
        request.recipe.model_dump(),
        request.target_servings,
        request.original_servings
    )
    return {"scaled_recipe": scaled_recipe}

@router.post("/recipes/analyze", response_model=schemas.NutritionAnalysisResponse)
async def analyze_recipe_nutrition(
    request: schemas.NutritionAnalysisRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Provide detailed nutritional analysis of a recipe.
    Includes macro and micronutrients, dietary quality analysis,
    and personalized recommendations based on user info and health goals.
    """
    analysis = await ai_service.analyze_nutrition(
        request.recipe.model_dump(),
        request.user_info,
        request.health_goals
    )
    return analysis

@router.post("/recipes/substitute", response_model=schemas.SubstitutionResponse)
async def suggest_ingredient_substitutions(
    request: schemas.SubstitutionRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Suggest suitable substitutions for ingredients in a recipe.
    Provides detailed conversion ratios, cooking adjustments,
    and impact on flavor, texture, and nutrition.
    """
    substitutions = await ai_service.suggest_substitutions(
        request.recipe.model_dump(),
        request.ingredients_to_replace,
        request.dietary_restrictions,
        request.available_ingredients
    )
    return substitutions

@router.post("/recipes/fusion", response_model=schemas.FusionResponse)
async def create_fusion_recipe(
    request: schemas.FusionRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a fusion recipe by combining elements from two different recipes.
    Intelligently merges ingredients, techniques, and flavors while
    maintaining culinary harmony and respecting both cuisines.
    """
    fusion_recipe = await ai_service.create_fusion_recipe(
        request.recipe1.model_dump(),
        request.recipe2.model_dump(),
        request.fusion_style,
        request.preferences
    )
    return fusion_recipe

@router.post("/tutorials/technique", response_model=schemas.TutorialResponse)
async def generate_technique_tutorial(
    request: schemas.TutorialRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Generate a detailed tutorial for a cooking technique.
    Includes step-by-step instructions, tips, common mistakes,
    practice exercises, and troubleshooting guide.
    """
    tutorial = await ai_service.generate_technique_tutorial(
        request.technique_name,
        request.skill_level,
        request.cuisine_context,
        request.specific_dish
    )
    return tutorial

@router.post("/menu/seasonal", response_model=schemas.SeasonalMenuResponse)
async def create_seasonal_menu(
    request: schemas.SeasonalMenuRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a seasonal menu plan with timing, presentation tips,
    wine pairings, and cost estimates based on season and occasion.
    """
    menu = await ai_service.create_seasonal_menu(
        request.season,
        request.occasion,
        request.guests,
        request.preferences,
        request.dietary_restrictions,
        request.budget_per_person,
        request.location
    )
    return menu

@router.post("/meal-plan/optimize", response_model=schemas.OptimizationResponse)
async def optimize_meal_plan(
    request: schemas.OptimizationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create an optimized meal plan for specific fitness/health goals.
    Takes into account user's stats, activity level, and preferences
    to create a scientifically-backed meal plan with:
    - Macro and micronutrient targets
    - Meal timing and portions
    - Supplement recommendations
    - Hydration guidelines
    - Progress tracking metrics
    """
    optimized_plan = await ai_service.optimize_meal_plan(
        request.goal,
        request.user_stats.model_dump(),
        request.activity_level,
        request.preferences,
        request.restrictions,
        [recipe.model_dump() for recipe in (request.existing_recipes or [])]
    )
    return optimized_plan

@router.post("/recipes/adapt", response_model=schemas.AdaptationResponse)
async def adapt_recipe_difficulty(
    request: schemas.AdaptationRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Adapt a recipe to match a user's skill level.
    Provides:
    - Simplified steps with explanations
    - Equipment alternatives
    - Detailed technique breakdowns
    - Timing adjustments
    - Confidence-building progression
    """
    adapted_recipe = await ai_service.adapt_recipe_difficulty(
        request.recipe.model_dump(),
        request.target_skill_level,
        request.user_equipment,
        request.time_constraints,
        request.specific_techniques
    )
    return adapted_recipe 