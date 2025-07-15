# Match Predictor Project Overview

## 1. Technologies

### Backend (Python)
- **Flask**: Web framework for serving APIs
- **scikit-learn**: Machine learning (regression, simulation)
- **NumPy**: Numerical computations
- **requests**: HTTP requests for fetching CSV data
- **dacite**: Data class instantiation from dicts
- **mypy**: Static type checking
- **responses**: HTTP mocking for tests

### Frontend (JavaScript/TypeScript)
- **React**: UI framework
- **Vite**: Build tool
- **Jest**: Testing framework
- **ESLint**: Linting
- **@testing-library/react**: React component testing

### Integration
- **Cypress**: End-to-end testing

### Infrastructure
- **Makefile**: Task automation
- **.env**: Environment variable configuration
- **Python virtualenv**: Isolated Python environment

---

## 2. Systems

### Backend API
- **Flask app** serves as the main API server.
- **Predictor models** (e.g., Home, Points, Alphabet Enhanced) are initialized and exposed via API endpoints.
- **CSV provider**: Fetches match data from a remote or local CSV.
- **Environment variables**: Configured via `.env` in `backend/`.
- **No external queues or caches** (in current codebase).

### Frontend
- **React app**: Consumes backend API, renders UI.
- **Vite**: Handles dev server, build, and hot reload.
- **Environment variables**: Can be set in `frontend/public/env.js` or `.env` (if needed).

### Integration Tests
- **Cypress**: Runs against the running frontend and backend, configured in `integration-tests/cypress.json`.
- **Logs**: Output to `integration-tests/cypress/log/`.

---

## 3. Code Mapping

### Backend Initialization
- **Flask App**: `@match-predictor/backend/matchpredictor/app.py`
  ```python
  def create_app(env: AppEnvironment) -> Flask:
      app = Flask(__name__)
      ...
      app.register_blueprint(forecast_api(forecaster))
  ```
- **ModelProvider**: `@match-predictor/backend/matchpredictor/app.py`
  ```python
  def build_model_provider(training_data: List[Result]) -> ModelProvider:
      return ModelProvider([
          Model("Home", HomePredictor()),
          Model("Alphabet Enhanced", train_alphabet_enhanced_predictor(training_data)),
          ...
      ])
  ```
- **Environment Variables**: `.env` in `@match-predictor/backend/.env`
  ```env
  PORT=5010
  CSV_LOCATION=http://localhost:5020/fixture.csv
  FOOTBALL_DATA_API_KEY=your-api-key-here
  ```

### Frontend Initialization
- **Vite Config**: `@match-predictor/frontend/vite.config.ts`
  ```ts
  export default defineConfig({
    plugins: [react()],
    ...
  });
  ```
- **React App Entry**: `@match-predictor/frontend/src/main.tsx`
  ```tsx
  import React from 'react';
  import ReactDOM from 'react-dom/client';
  import App from './App/App';
  ReactDOM.createRoot(document.getElementById('root')!).render(<App />);
  ```
- **Frontend Env**: `@match-predictor/frontend/public/env.js`
  ```js
  window.env = { ... };
  ```

### Integration Test Config
- **Cypress Config**: `@match-predictor/integration-tests/cypress.json`
  ```json
  {
    "baseUrl": "http://localhost:3010"
  }
  ```
- **Cypress Test Example**: `@match-predictor/integration-tests/cypress/integration/predictor.spec.js`
  ```js
  describe('Predictor', () => {
    it('should show predictions', () => { ... });
  });
  ```