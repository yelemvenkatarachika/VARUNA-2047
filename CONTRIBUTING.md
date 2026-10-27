# Contributing to VARUNA 2047

Thank you for your interest in contributing to **VARUNA 2047: Viksit Bharat Agricultural Resilience Using National Earth Observation**.

## Code of Conduct & Scientific Principles
1. **Zero Fabrication:** Never introduce synthetic or fabricated climate measurements into production screens.
2. **Pre-Monsoon Issuance Boundary:** Strictly preserve the May 31 forecast issuance cutoff. No feature may use observations collected during or after the target monsoon season (June–September).
3. **Reproducibility:** Every model artifact must be accompanied by its feature schema, scaler, and deterministic random seed.
4. **Honest Attribution:** Accurately credit all remote sensing data providers (ISRO, NOAA, NASA, Copernicus).

## Development Workflow
1. Fork and clone the repository.
2. Create a virtual environment with Python 3.12:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
3. Run tests before submitting changes:
   ```bash
   python -m pytest tests/
   ```
4. For frontend contributions:
   ```bash
   cd frontend
   npm install
   npm run build
   ```
