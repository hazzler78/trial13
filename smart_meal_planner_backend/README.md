# Smart Meal Planner API

A powerful meal planning API with advanced AI features for recipe management, meal planning, and cooking assistance.

[![CI/CD](https://github.com/yourusername/smart-meal-planner/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/smart-meal-planner/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/yourusername/smart-meal-planner/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/smart-meal-planner)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

## Project Status

✅ Completed Features:
- User authentication with JWT
- Inventory management
- Recipe management
- Shopping list generation
- Multi-user support
- Database migrations
- Error handling (including rate limits)
- Comprehensive test coverage
- CI/CD pipeline with:
  - Automated testing
  - Code quality checks
  - Security scanning
  - Coverage reporting

## Features

### Core Features
- User authentication with JWT
- Inventory management
- Recipe management
- Shopping list generation
- Multi-user support
- Database migrations
- Error handling with proper status codes
- Rate limit handling for AI services

### AI-Powered Features

#### Recipe Management
- **Recipe Suggestions**: Get personalized recipe suggestions based on:
  - Available ingredients
  - User preferences
  - Dietary restrictions
  - Nutritional goals

- **Recipe Scaling**: Automatically adjust recipes for different serving sizes:
  - Smart quantity calculations
  - Adjusted cooking times
  - Modified instructions
  - Special handling for seasonings

- **Nutritional Analysis**: Detailed nutritional breakdown including:
  - Macro and micronutrients
  - Vitamin content
  - Mineral content
  - Dietary quality analysis
  - Personalized recommendations

- **Ingredient Substitutions**: Smart ingredient replacement suggestions with:
  - Exact conversion ratios
  - Impact on flavor and texture
  - Nutritional differences
  - Required cooking adjustments

- **Recipe Fusion**: Create unique recipes by combining different cuisines:
  - Intelligent flavor combinations
  - Cross-cultural cooking techniques
  - Balanced fusion elements
  - Pairing suggestions

#### Meal Planning
- **Personalized Meal Plans**: Generate complete meal plans considering:
  - Dietary preferences
  - Nutritional goals
  - Budget constraints
  - Available ingredients
  - Activity level
  - Body composition
  - Fitness goals

- **Meal Plan Optimization**: Optimize meal plans for specific goals:
  - Weight loss/gain
  - Muscle building
  - Athletic performance
  - Health conditions
  - Macro/micronutrient targets
  - Meal timing
  - Supplement recommendations
  - Hydration guidelines

- **Seasonal Menu Planning**: Create occasion-specific menus with:
  - Seasonal ingredients
  - Wine pairings
  - Timing guides
  - Cost estimates
  - Presentation tips

#### Cooking Assistance
- **Technique Tutorials**: Detailed cooking technique guides including:
  - Step-by-step instructions
  - Common mistakes to avoid
  - Visual cues for success
  - Practice exercises
  - Troubleshooting tips
  - Equipment guidance
  - Safety considerations

- **Recipe Difficulty Adaptation**: Adapt recipes to different skill levels:
  - Simplified instructions
  - Equipment alternatives
  - Technique breakdowns
  - Timing adjustments
  - Confidence-building steps

## API Endpoints

### Authentication
- POST `/api/v1/auth/register`: Register new user
- POST `/api/v1/auth/login`: Login user
- POST `/api/v1/auth/token`: Get access token
- GET `/api/v1/auth/me`: Get current user info

### Core Functionality
- GET/POST `/api/v1/inventory/`: Manage inventory items
- GET/POST `/api/v1/recipes/`: Manage recipes
- GET/POST `/api/v1/shopping-list/`: Manage shopping list

### AI Features
- POST `/api/v1/ai/recipes/suggest`: Get recipe suggestions
- POST `/api/v1/ai/meal-plan/optimize`: Generate optimized meal plans
- POST `/api/v1/ai/recipes/scale`: Scale recipe servings
- POST `/api/v1/ai/recipes/analyze`: Analyze recipe nutrition
- POST `/api/v1/ai/recipes/substitute`: Get ingredient substitutions
- POST `/api/v1/ai/recipes/fusion`: Create fusion recipes
- POST `/api/v1/ai/recipes/adapt`: Adapt recipe difficulty

## Setup and Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with:
```
DATABASE_URL=sqlite:///./smart_meal_planner.db
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Run the server:
```bash
uvicorn main:app --reload
```

## Testing

Run tests with:
```bash
python -m pytest -v
```

For test coverage:
```bash
python -m pytest --cov=. tests/
```

## Error Handling

The API implements comprehensive error handling:
- Input validation errors (422)
- Authentication errors (401)
- Authorization errors (403)
- Rate limit errors (429)
- Server errors (500)
- OpenAI API errors with proper status codes

## Development Status

### Completed
- ✅ Core API structure
- ✅ Database models and migrations
- ✅ Authentication system
- ✅ Inventory management
- ✅ Recipe management
- ✅ Shopping list functionality
- ✅ AI integration
- ✅ Error handling
- ✅ Rate limit handling
- ✅ Test coverage

### In Progress
- 🔄 Frontend development
- 🔄 Additional AI features
- 🔄 Performance optimization
- 🔄 Documentation improvements

### Planned
- 📋 Deployment guides
- 📋 CI/CD setup
- 📋 Monitoring and logging
- 📋 User feedback system
- 📋 Advanced analytics

## License

MIT License

## Development

### Code Quality

The project uses several tools to maintain code quality:

- **black**: Code formatting
- **pylint**: Code linting
- **mypy**: Static type checking
- **bandit**: Security scanning
- **safety**: Dependency security checking

Run code quality checks locally:

```bash
# Format code
black .

# Run linting
pylint **/*.py

# Run type checking
mypy .

# Run security checks
bandit -r .
safety check
```

### CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment. The pipeline:

1. Runs on every push and pull request to main branch
2. Tests against Python 3.9, 3.10, 3.11, and 3.12
3. Performs:
   - Code formatting check (black)
   - Linting (pylint)
   - Type checking (mypy)
   - Unit tests (pytest)
   - Coverage reporting (pytest-cov)
   - Security scanning (bandit, safety)
4. Uploads coverage reports to Codecov

### Environment Variables for CI/CD

Required secrets in GitHub:
- `OPENAI_API_KEY`: OpenAI API key for tests
- `SECRET_KEY`: JWT secret key for tests

### Pre-commit Hooks

To set up pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

This will run code quality checks before each commit.