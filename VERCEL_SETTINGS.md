# Vercel Project Settings Configuration

## Correct Settings for This Project

When setting up your project in Vercel Dashboard, use these settings:

### Framework Preset
- **Select**: `Other` (or `Vite` if available, but `Other` is safer)

### Build and Output Settings
- **Build Command**: Leave **EMPTY** (no build needed - we have static HTML)
- **Output Directory**: Leave **EMPTY** (Vercel will auto-detect `public/` folder)
- **Install Command**: Leave **EMPTY** (Vercel will auto-detect Python and use `requirements.txt`)

### Root Directory
- **Root Directory**: `./` (leave as default - root of repository)

### Environment Variables (Optional)
- **OPENROUTER_API_KEY**: Your OpenRouter API key (optional - users can enter their own)

## Why These Settings?

1. **No Build Command**: This project uses static HTML (`public/index.html`) - no build step needed
2. **No Output Directory**: Vercel automatically serves files from the `public/` directory
3. **No Install Command**: Vercel detects `requirements.txt` and automatically installs Python dependencies
4. **Framework: Other**: This is a Python serverless function + static HTML, not a Node.js framework

## Important Notes

- The `vercel.json` file handles all the routing and build configuration
- Vercel will automatically:
  - Detect Python from `requirements.txt`
  - Install dependencies from `requirements.txt`
  - Build the Python serverless function in `api/analyze.py`
  - Serve static files from `public/` directory

## If You Still Get 404

1. Make sure `vercel.json` is committed to your repository
2. Check that all files are pushed to GitHub:
   - `api/analyze.py`
   - `public/index.html`
   - `vercel.json`
   - `requirements.txt`
3. After deployment, check the "Functions" tab in Vercel dashboard to see if the Python function built successfully
