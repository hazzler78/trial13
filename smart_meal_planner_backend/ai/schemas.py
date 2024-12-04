from pydantic import BaseModel, Field, ConfigDict, PositiveFloat
from typing import List, Dict, Any, Optional

class RecipeNutrition(BaseModel):
    calories: float = Field(description="Total calories")
    protein: float = Field(description="Protein content in grams")
    carbs: float = Field(description="Carbohydrate content in grams")
    fat: float = Field(description="Fat content in grams")

class AIRecipe(BaseModel):
    name: str = Field(description="Recipe name")
    description: str = Field(description="Recipe description")
    ingredients: List[Dict[str, Any]] = Field(description="List of ingredients with quantities")
    instructions: List[str] = Field(description="Step-by-step instructions")
    prep_time: int = Field(description="Preparation time in minutes")
    difficulty: str = Field(description="Difficulty level (Easy/Medium/Hard)")
    nutrition: RecipeNutrition = Field(description="Nutritional information")

class RecipeSuggestionRequest(BaseModel):
    ingredients: List[str] = Field(description="List of ingredients to use")
    preferences: Optional[Dict[str, Any]] = Field(None, description="User preferences")
    dietary_restrictions: Optional[List[str]] = Field(None, description="Dietary restrictions")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "ingredients": ["chicken", "rice", "tomatoes"],
            "preferences": {
                "cuisine": "Italian",
                "spiciness": "medium"
            },
            "dietary_restrictions": ["gluten-free", "dairy-free"]
        }
    })

class RecipeSuggestionResponse(BaseModel):
    recipes: List[AIRecipe] = Field(description="List of suggested recipes")

class MealPlanShoppingItem(BaseModel):
    name: str = Field(description="Ingredient name")
    quantity: float = Field(description="Quantity needed")
    unit: str = Field(description="Unit of measurement")
    estimated_cost: float = Field(description="Estimated cost")

class MealPlanMeal(BaseModel):
    type: str = Field(description="Meal type (breakfast/lunch/dinner)")
    recipe: AIRecipe = Field(description="Recipe for this meal")

class MealPlanDay(BaseModel):
    day: int = Field(description="Day number")
    meals: List[MealPlanMeal] = Field(description="Meals for this day")
    total_nutrition: RecipeNutrition = Field(description="Total nutritional information for the day")

class MealPlan(BaseModel):
    days: List[MealPlanDay] = Field(description="Daily meal plans")
    shopping_list: List[MealPlanShoppingItem] = Field(description="Consolidated shopping list")
    total_cost: float = Field(description="Total estimated cost")

class MealPlanRequest(BaseModel):
    days: int = Field(7, description="Number of days to plan for")
    meals_per_day: int = Field(3, description="Number of meals per day")
    preferences: Optional[Dict[str, Any]] = Field(None, description="User preferences")
    dietary_restrictions: Optional[List[str]] = Field(None, description="Dietary restrictions")
    budget: Optional[float] = Field(None, description="Budget constraint")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "days": 7,
            "meals_per_day": 3,
            "preferences": {
                "cuisine": ["Italian", "Mexican"],
                "calories_per_day": 2000,
                "protein_target": 150
            },
            "dietary_restrictions": ["vegetarian"],
            "budget": 200.0
        }
    })

class MealPlanResponse(BaseModel):
    meal_plan: MealPlan = Field(description="Generated meal plan")

class RecipeScalingRequest(BaseModel):
    recipe: AIRecipe = Field(description="Recipe to scale")
    target_servings: PositiveFloat = Field(description="Desired number of servings")
    original_servings: PositiveFloat = Field(1.0, description="Original number of servings")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "recipe": {
                "name": "Spaghetti Bolognese",
                "description": "Classic Italian pasta dish",
                "ingredients": [
                    {"name": "spaghetti", "quantity": 500, "unit": "g"},
                    {"name": "ground beef", "quantity": 400, "unit": "g"}
                ],
                "instructions": ["Step 1", "Step 2"],
                "prep_time": 30,
                "difficulty": "Easy",
                "nutrition": {
                    "calories": 800,
                    "protein": 40,
                    "carbs": 80,
                    "fat": 30
                }
            },
            "target_servings": 4,
            "original_servings": 2
        }
    })

class RecipeScalingResponse(BaseModel):
    scaled_recipe: AIRecipe = Field(description="Scaled version of the recipe")

class Vitamins(BaseModel):
    A: float = Field(description="Vitamin A content")
    C: float = Field(description="Vitamin C content")
    D: float = Field(description="Vitamin D content")
    E: float = Field(description="Vitamin E content")
    K: float = Field(description="Vitamin K content")
    B1: float = Field(description="Vitamin B1 (Thiamin) content")
    B2: float = Field(description="Vitamin B2 (Riboflavin) content")
    B3: float = Field(description="Vitamin B3 (Niacin) content")
    B6: float = Field(description="Vitamin B6 content")
    B12: float = Field(description="Vitamin B12 content")
    folate: float = Field(description="Folate content")

class Minerals(BaseModel):
    calcium: float = Field(description="Calcium content")
    iron: float = Field(description="Iron content")
    magnesium: float = Field(description="Magnesium content")
    zinc: float = Field(description="Zinc content")
    potassium: float = Field(description="Potassium content")
    sodium: float = Field(description="Sodium content")

class Macronutrients(BaseModel):
    calories: float = Field(description="Total calories")
    protein: float = Field(description="Protein content in grams")
    carbs: float = Field(description="Carbohydrate content in grams")
    fat: float = Field(description="Fat content in grams")
    fiber: float = Field(description="Fiber content in grams")

class Micronutrients(BaseModel):
    vitamins: Vitamins = Field(description="Vitamin content")
    minerals: Minerals = Field(description="Mineral content")

class DietaryAnalysis(BaseModel):
    protein_quality: str = Field(description="Analysis of protein sources and quality")
    carb_quality: str = Field(description="Analysis of carbohydrate sources and quality")
    fat_quality: str = Field(description="Analysis of fat sources and quality")
    fiber_adequacy: str = Field(description="Analysis of fiber content adequacy")
    vitamin_adequacy: str = Field(description="Analysis of vitamin content adequacy")
    mineral_adequacy: str = Field(description="Analysis of mineral content adequacy")
    recommendations: List[str] = Field(description="Specific dietary recommendations")

class DetailedNutrition(BaseModel):
    macronutrients: Macronutrients = Field(description="Macronutrient breakdown")
    micronutrients: Micronutrients = Field(description="Micronutrient breakdown")
    dietary_analysis: DietaryAnalysis = Field(description="Detailed dietary analysis")

class NutritionAnalysisRequest(BaseModel):
    recipe: AIRecipe = Field(description="Recipe to analyze")
    user_info: Optional[Dict[str, Any]] = Field(None, description="User information for personalized analysis")
    health_goals: Optional[List[str]] = Field(None, description="Health and dietary goals")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "recipe": {
                "name": "Spaghetti Bolognese",
                "description": "Classic Italian pasta dish",
                "ingredients": [
                    {"name": "spaghetti", "quantity": 500, "unit": "g"},
                    {"name": "ground beef", "quantity": 400, "unit": "g"}
                ],
                "instructions": ["Step 1", "Step 2"],
                "prep_time": 30,
                "difficulty": "Easy",
                "nutrition": {
                    "calories": 800,
                    "protein": 40,
                    "carbs": 80,
                    "fat": 30
                }
            },
            "user_info": {
                "age": 30,
                "weight": 70,
                "height": 175,
                "activity_level": "moderate",
                "dietary_preferences": ["high-protein", "low-carb"]
            },
            "health_goals": [
                "weight loss",
                "muscle gain",
                "improve energy levels"
            ]
        }
    })

class NutritionAnalysisResponse(BaseModel):
    nutrition: DetailedNutrition = Field(description="Detailed nutritional analysis")

class IngredientSubstitute(BaseModel):
    name: str = Field(description="Name of the substitute ingredient")
    quantity: float = Field(description="Quantity needed")
    unit: str = Field(description="Unit of measurement")
    conversion_ratio: float = Field(description="Ratio for converting from original ingredient")
    flavor_impact: str = Field(description="How the substitution affects flavor")
    texture_impact: str = Field(description="How the substitution affects texture")
    nutrition_impact: str = Field(description="How the substitution affects nutrition")
    cooking_adjustments: List[str] = Field(description="Required adjustments to cooking process")

class IngredientSubstitution(BaseModel):
    original_ingredient: Dict[str, Any] = Field(description="Original ingredient details")
    substitutes: List[IngredientSubstitute] = Field(description="List of possible substitutes")
    notes: str = Field(description="Additional notes about the substitution")

class SubstitutionRequest(BaseModel):
    recipe: AIRecipe = Field(description="Recipe containing ingredients to substitute")
    ingredients_to_replace: List[str] = Field(description="List of ingredients needing substitution")
    dietary_restrictions: Optional[List[str]] = Field(None, description="Dietary restrictions to consider")
    available_ingredients: Optional[List[str]] = Field(None, description="List of available ingredients")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "recipe": {
                "name": "Classic Lasagna",
                "description": "Traditional Italian lasagna",
                "ingredients": [
                    {"name": "ground beef", "quantity": 500, "unit": "g"},
                    {"name": "lasagna noodles", "quantity": 250, "unit": "g"}
                ],
                "instructions": ["Step 1", "Step 2"],
                "prep_time": 60,
                "difficulty": "Medium",
                "nutrition": {
                    "calories": 800,
                    "protein": 45,
                    "carbs": 60,
                    "fat": 35
                }
            },
            "ingredients_to_replace": ["ground beef", "lasagna noodles"],
            "dietary_restrictions": ["vegetarian", "gluten-free"],
            "available_ingredients": ["lentils", "zucchini", "mushrooms"]
        }
    })

class SubstitutionResponse(BaseModel):
    substitutions: List[IngredientSubstitution] = Field(description="List of suggested substitutions")

class CookingTechnique(BaseModel):
    name: str = Field(description="Name of the cooking technique")
    cuisine_origin: str = Field(description="Origin cuisine of the technique")
    description: str = Field(description="Detailed description of the technique")

class FusionIngredient(BaseModel):
    name: str = Field(description="Name of the ingredient")
    quantity: float = Field(description="Quantity needed")
    unit: str = Field(description="Unit of measurement")
    cuisine_origin: str = Field(description="Origin cuisine of the ingredient")

class FusionRecipe(BaseModel):
    name: str = Field(description="Name of the fusion recipe")
    description: str = Field(description="Description of the fusion concept")
    cuisine_influences: List[str] = Field(description="List of cuisines influencing the recipe")
    ingredients: List[FusionIngredient] = Field(description="List of ingredients with origins")
    instructions: List[str] = Field(description="Step-by-step cooking instructions")
    cooking_techniques: List[CookingTechnique] = Field(description="Cooking techniques used")
    prep_time: int = Field(description="Preparation time in minutes")
    difficulty: str = Field(description="Difficulty level")
    nutrition: RecipeNutrition = Field(description="Nutritional information")
    fusion_notes: List[str] = Field(description="Notes about fusion elements")
    pairing_suggestions: List[str] = Field(description="Suggested pairings")

class FusionRequest(BaseModel):
    recipe1: AIRecipe = Field(description="First recipe to combine")
    recipe2: AIRecipe = Field(description="Second recipe to combine")
    fusion_style: Optional[str] = Field(None, description="Desired style of fusion")
    preferences: Optional[Dict[str, Any]] = Field(None, description="Preferences for fusion")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "recipe1": {
                "name": "Classic Margherita Pizza",
                "description": "Traditional Italian pizza",
                "ingredients": [
                    {"name": "pizza dough", "quantity": 300, "unit": "g"},
                    {"name": "tomatoes", "quantity": 200, "unit": "g"}
                ],
                "instructions": ["Step 1", "Step 2"],
                "prep_time": 45,
                "difficulty": "Medium",
                "nutrition": {
                    "calories": 600,
                    "protein": 20,
                    "carbs": 80,
                    "fat": 25
                }
            },
            "recipe2": {
                "name": "Thai Green Curry",
                "description": "Spicy Thai curry",
                "ingredients": [
                    {"name": "coconut milk", "quantity": 400, "unit": "ml"},
                    {"name": "green curry paste", "quantity": 50, "unit": "g"}
                ],
                "instructions": ["Step 1", "Step 2"],
                "prep_time": 30,
                "difficulty": "Medium",
                "nutrition": {
                    "calories": 500,
                    "protein": 25,
                    "carbs": 30,
                    "fat": 35
                }
            },
            "fusion_style": "Modern Asian-Italian",
            "preferences": {
                "spiciness": "medium",
                "preferred_cooking_method": "baking",
                "texture_preference": "crispy"
            }
        }
    })

class FusionResponse(BaseModel):
    fusion_recipe: FusionRecipe = Field(description="Generated fusion recipe")

class TechniqueStep(BaseModel):
    order: int = Field(description="Step order number")
    title: str = Field(description="Step title")
    description: str = Field(description="Detailed step description")
    tips: List[str] = Field(description="Helpful tips for this step")
    common_mistakes: List[str] = Field(description="Common mistakes to avoid")
    visual_cues: List[str] = Field(description="Visual indicators of success")

class TechniqueVariation(BaseModel):
    name: str = Field(description="Name of the variation")
    description: str = Field(description="Description of how to perform the variation")
    when_to_use: str = Field(description="When to use this variation")

class PracticeExercise(BaseModel):
    name: str = Field(description="Name of the exercise")
    description: str = Field(description="Exercise description")
    difficulty: str = Field(description="Exercise difficulty level")
    learning_objectives: List[str] = Field(description="What you'll learn from this exercise")

class TroubleshootingGuide(BaseModel):
    problem: str = Field(description="Description of the problem")
    causes: List[str] = Field(description="Possible causes")
    solutions: List[str] = Field(description="Solutions to try")

class CookingTechnique(BaseModel):
    name: str = Field(description="Name of the technique")
    difficulty: str = Field(description="Difficulty level")
    equipment_needed: List[str] = Field(description="Required equipment")
    safety_tips: List[str] = Field(description="Safety considerations")

class TechniqueTutorial(BaseModel):
    technique: CookingTechnique = Field(description="Technique details")
    steps: List[TechniqueStep] = Field(description="Step-by-step instructions")
    variations: List[TechniqueVariation] = Field(description="Technique variations")
    practice_exercises: List[PracticeExercise] = Field(description="Practice exercises")
    troubleshooting: List[TroubleshootingGuide] = Field(description="Troubleshooting guide")

class TutorialRequest(BaseModel):
    technique_name: str = Field(description="Name of the cooking technique")
    skill_level: str = Field("beginner", description="Target skill level")
    cuisine_context: Optional[str] = Field(None, description="Specific cuisine context")
    specific_dish: Optional[str] = Field(None, description="Specific dish context")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "technique_name": "knife skills",
            "skill_level": "intermediate",
            "cuisine_context": "Japanese",
            "specific_dish": "Sashimi"
        }
    })

class TutorialResponse(BaseModel):
    tutorial: TechniqueTutorial = Field(description="Generated technique tutorial")

class SeasonalIngredient(BaseModel):
    name: str = Field(description="Ingredient name")
    peak_season: str = Field(description="Peak season for the ingredient")
    substitutes: List[str] = Field(description="Possible substitutes")

class SeasonalRecipe(BaseModel):
    name: str = Field(description="Recipe name")
    description: str = Field(description="Recipe description")
    seasonal_ingredients: List[SeasonalIngredient] = Field(description="Seasonal ingredients used")
    preparation_timing: str = Field(description="When to prepare")
    can_make_ahead: bool = Field(description="Can be made in advance")
    plating_suggestions: List[str] = Field(description="Plating and presentation suggestions")

class MenuSection(BaseModel):
    name: str = Field(description="Section name (e.g., 'Appetizers')")
    dishes: List[Dict[str, SeasonalRecipe]] = Field(description="Dishes in this section")

class WinePairing(BaseModel):
    wine: str = Field(description="Wine recommendation")
    pairing_notes: str = Field(description="Notes about the pairing")
    alternatives: List[str] = Field(description="Alternative beverages")

class TimingSchedule(BaseModel):
    time: str = Field(description="Time or timing")
    tasks: List[str] = Field(description="Tasks to complete")

class MenuTimingGuide(BaseModel):
    preparation_schedule: List[TimingSchedule] = Field(description="Advance preparation schedule")
    day_of_schedule: List[TimingSchedule] = Field(description="Day-of schedule")

class MenuCosts(BaseModel):
    per_person: float = Field(description="Cost per person")
    total: float = Field(description="Total cost")
    budget_alternatives: List[str] = Field(description="Budget-friendly alternatives")

class SeasonalMenu(BaseModel):
    season: str = Field(description="Season")
    theme: str = Field(description="Menu theme")
    occasion: str = Field(description="Special occasion")
    menu_sections: List[MenuSection] = Field(description="Menu sections")
    wine_pairings: List[WinePairing] = Field(description="Wine pairing suggestions")
    timing_guide: MenuTimingGuide = Field(description="Timing and scheduling")
    presentation_tips: List[str] = Field(description="Presentation suggestions")
    estimated_costs: MenuCosts = Field(description="Cost estimates")

class SeasonalMenuRequest(BaseModel):
    season: str = Field(description="Target season")
    occasion: Optional[str] = Field(None, description="Special occasion")
    guests: int = Field(4, description="Number of guests")
    preferences: Optional[Dict[str, Any]] = Field(None, description="Dining preferences")
    dietary_restrictions: Optional[List[str]] = Field(None, description="Dietary restrictions")
    budget_per_person: Optional[float] = Field(None, description="Budget per person")
    location: Optional[str] = Field(None, description="Geographic location")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "season": "summer",
            "occasion": "garden party",
            "guests": 8,
            "preferences": {
                "style": "casual elegant",
                "temperature": "cold dishes preferred",
                "cuisine": "Mediterranean"
            },
            "dietary_restrictions": ["vegetarian", "gluten-free"],
            "budget_per_person": 50.0,
            "location": "California"
        }
    })

class SeasonalMenuResponse(BaseModel):
    seasonal_menu: SeasonalMenu = Field(description="Generated seasonal menu")

class NutrientTargets(BaseModel):
    calories: float = Field(description="Daily calorie target")
    protein: float = Field(description="Daily protein target in grams")
    carbs: float = Field(description="Daily carbohydrate target in grams")
    fat: float = Field(description="Daily fat target in grams")
    fiber: float = Field(description="Daily fiber target in grams")

class MealContribution(BaseModel):
    calories: float = Field(description="Calories in this meal")
    protein: float = Field(description="Protein content in grams")
    carbs: float = Field(description="Carbohydrate content in grams")
    fat: float = Field(description="Fat content in grams")

class OptimizedRecipe(BaseModel):
    recipe: AIRecipe = Field(description="Base recipe")
    portion_size: float = Field(description="Portion size for this meal")
    contribution_to_goals: MealContribution = Field(description="Nutritional contribution")
    timing_notes: str = Field(description="When to consume")
    pre_post_workout: bool = Field(description="Whether this is a workout meal")

class OptimizedMeal(BaseModel):
    meal_type: str = Field(description="Type of meal (breakfast, lunch, etc.)")
    timing: str = Field(description="When to have this meal")
    recipes: List[OptimizedRecipe] = Field(description="Recipes in this meal")
    nutritional_balance: str = Field(description="Notes on nutritional balance")
    meal_synergy: str = Field(description="How components work together")

class Supplement(BaseModel):
    name: str = Field(description="Supplement name")
    timing: str = Field(description="When to take")
    dosage: str = Field(description="How much to take")
    purpose: str = Field(description="Why to take it")
    notes: str = Field(description="Additional notes")

class HydrationPlan(BaseModel):
    daily_water: float = Field(description="Daily water intake in liters")
    electrolytes: bool = Field(description="Whether electrolyte supplementation is needed")
    timing_guidelines: List[str] = Field(description="When to hydrate")

class ProgressTracking(BaseModel):
    metrics: List[str] = Field(description="What to measure")
    measurement_frequency: str = Field(description="How often to measure")
    expected_progress: str = Field(description="Expected timeline and results")

class OptimizedMealPlan(BaseModel):
    goal: str = Field(description="Fitness/health goal")
    daily_targets: NutrientTargets = Field(description="Daily nutritional targets")
    meals: List[OptimizedMeal] = Field(description="Planned meals")
    supplements: List[Supplement] = Field(description="Supplement recommendations")
    hydration_plan: HydrationPlan = Field(description="Hydration guidelines")
    progress_tracking: ProgressTracking = Field(description="Progress monitoring plan")

class UserStats(BaseModel):
    age: int = Field(description="User's age")
    weight: float = Field(description="Current weight in kg")
    height: float = Field(description="Height in cm")
    body_fat: Optional[float] = Field(None, description="Body fat percentage")
    target_weight: Optional[float] = Field(None, description="Target weight in kg")
    medical_conditions: Optional[List[str]] = Field(None, description="Relevant medical conditions")
    fitness_level: str = Field(description="Current fitness level")

class OptimizationRequest(BaseModel):
    goal: str = Field(description="Fitness or health goal")
    user_stats: UserStats = Field(description="User statistics")
    activity_level: str = Field(description="Activity level")
    preferences: Optional[Dict[str, Any]] = Field(None, description="Dietary preferences")
    restrictions: Optional[List[str]] = Field(None, description="Dietary restrictions")
    existing_recipes: Optional[List[AIRecipe]] = Field(None, description="Favorite recipes")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "goal": "muscle gain",
            "user_stats": {
                "age": 28,
                "weight": 75,
                "height": 180,
                "body_fat": 15,
                "target_weight": 80,
                "fitness_level": "intermediate"
            },
            "activity_level": "very active",
            "preferences": {
                "meal_frequency": 5,
                "protein_sources": ["chicken", "fish", "eggs"],
                "preferred_cuisines": ["mediterranean", "asian"]
            },
            "restrictions": ["no_dairy"],
            "existing_recipes": []
        }
    })

class OptimizationResponse(BaseModel):
    optimized_meal_plan: OptimizedMealPlan = Field(description="Optimized meal plan")

class RecipeSimplification(BaseModel):
    original_step: str = Field(description="Original recipe step")
    simplified_step: str = Field(description="Simplified version")
    reason: str = Field(description="Why this simplification helps")
    tips: List[str] = Field(description="Helpful tips")

class EquipmentSubstitution(BaseModel):
    original_equipment: str = Field(description="Original equipment needed")
    alternative: str = Field(description="Alternative equipment")
    usage_instructions: List[str] = Field(description="How to use the alternative")

class TechniqueBreakdown(BaseModel):
    technique: str = Field(description="Cooking technique")
    difficulty_level: str = Field(description="Technique difficulty")
    detailed_steps: List[str] = Field(description="Step-by-step breakdown")
    practice_suggestions: List[str] = Field(description="How to practice")

class TimingAdjustment(BaseModel):
    original_time: int = Field(description="Original preparation time")
    adjusted_time: int = Field(description="New preparation time")
    explanation: str = Field(description="Why the timing changed")

class AdaptedRecipe(BaseModel):
    original_difficulty: str = Field(description="Original recipe difficulty")
    adapted_difficulty: str = Field(description="New recipe difficulty")
    simplifications: List[RecipeSimplification] = Field(description="Step simplifications")
    equipment_substitutions: List[EquipmentSubstitution] = Field(description="Equipment alternatives")
    technique_breakdown: List[TechniqueBreakdown] = Field(description="Technique explanations")
    timing_adjustments: TimingAdjustment = Field(description="Time adjustments")
    recipe: AIRecipe = Field(description="Adapted recipe")
    confidence_building_steps: List[str] = Field(description="Confidence building tips")
    common_mistakes_prevention: List[str] = Field(description="How to avoid mistakes")

class AdaptationRequest(BaseModel):
    recipe: AIRecipe = Field(description="Recipe to adapt")
    target_skill_level: str = Field(description="Desired difficulty level")
    user_equipment: Optional[List[str]] = Field(None, description="Available equipment")
    time_constraints: Optional[int] = Field(None, description="Time limit in minutes")
    specific_techniques: Optional[List[str]] = Field(None, description="Techniques to focus on")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "recipe": {
                "name": "Beef Wellington",
                "description": "Classic British dish",
                "ingredients": [
                    {"name": "beef tenderloin", "quantity": 1000, "unit": "g"}
                ],
                "instructions": ["Step 1", "Step 2"],
                "prep_time": 120,
                "difficulty": "advanced",
                "nutrition": {
                    "calories": 800,
                    "protein": 45,
                    "carbs": 30,
                    "fat": 35
                }
            },
            "target_skill_level": "beginner",
            "user_equipment": ["oven", "skillet", "baking sheet"],
            "time_constraints": 60,
            "specific_techniques": ["searing", "pastry work"]
        }
    })

class AdaptationResponse(BaseModel):
    adapted_recipe: AdaptedRecipe = Field(description="Difficulty-adapted recipe") 