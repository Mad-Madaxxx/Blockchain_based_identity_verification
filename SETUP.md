# Setup Guide

## Git Configuration

Before committing, configure your Git identity:

```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

Or set globally:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Linking to GitHub

1. **Create a new repository on GitHub**:
   - Go to https://github.com/new
   - Create a new repository (e.g., `blockchain-identity-verification`)
   - Do NOT initialize with README, .gitignore, or license

2. **Link your local repository to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/blockchain-identity-verification.git
   ```

3. **Push your code**:
   ```bash
   git branch -M main
   git push -u origin main
   ```

## First Time Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Open browser to http://localhost:5000

