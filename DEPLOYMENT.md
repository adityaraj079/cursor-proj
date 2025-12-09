# 🚀 Vercel Deployment Guide

## Step-by-Step Deployment Instructions

### Prerequisites
1. A GitHub account
2. A Vercel account (sign up at [vercel.com](https://vercel.com) - free tier available)
3. Your code pushed to a GitHub repository

### Method 1: Deploy via Vercel Dashboard (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Vercel deployment"
   git push origin main
   ```

2. **Go to Vercel Dashboard**
   - Visit [vercel.com](https://vercel.com)
   - Sign in with your GitHub account

3. **Create a New Project**
   - Click "Add New..." → "Project"
   - Import your GitHub repository (`cursor-proj`)
   - Click "Import"

4. **Configure Project Settings**
   - **Framework Preset**: Leave as "Other" (or "Vite" if available)
   - **Root Directory**: Leave as `./` (root)
   - **Build Command**: Leave empty (not needed)
   - **Output Directory**: Leave empty
   - **Install Command**: Leave empty (Vercel will auto-detect `requirements.txt`)

5. **Set Environment Variables** (Optional)
   - Click "Environment Variables"
   - Add: `OPENROUTER_API_KEY` = `your_api_key_here`
   - This is optional - users can enter their own API key in the app

6. **Deploy**
   - Click "Deploy"
   - Wait for the build to complete (usually 1-2 minutes)

7. **Access Your App**
   - Once deployed, Vercel will provide a URL like: `https://your-app.vercel.app`
   - Your app is now live! 🎉

### Method 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```
   Or using other package managers:
   ```bash
   # Using yarn
   yarn global add vercel
   
   # Using pnpm
   pnpm add -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```
   - This will open a browser window for authentication

3. **Navigate to your project directory**
   ```bash
   cd /Users/adityaraj/Desktop/Projects/cursor-proj
   ```

4. **Deploy to Production**
   ```bash
   vercel --prod
   ```
   
   Or for a preview deployment:
   ```bash
   vercel
   ```

5. **Follow the prompts**
   - "Set up and deploy? [Y/n]" → Press `Y` or Enter
   - "Which scope?" → Select your account/team
   - "Link to existing project? [y/N]" → Press `N` for first deployment
   - "What's your project's name?" → Enter a name or press Enter for default
   - "In which directory is your code located?" → Press Enter for `./`
   - "Want to override the settings? [y/N]" → Press `N` (unless you need to change something)

6. **Set Environment Variables** (if needed)
   ```bash
   vercel env add OPENROUTER_API_KEY
   ```
   - Enter your API key when prompted
   - Select environments: Production, Preview, Development

7. **Your app is deployed!**
   - Vercel will provide a URL like: `https://your-app.vercel.app`

### Troubleshooting 404 Errors

If you're getting a 404 error:

1. **Check your file structure**
   - Ensure `public/index.html` exists
   - Ensure `api/analyze.py` exists
   - Ensure `vercel.json` is in the root directory

2. **Verify vercel.json configuration**
   - The file should match the current configuration
   - Routes should be properly defined

3. **Check build logs**
   - Go to your Vercel dashboard
   - Click on your project
   - Go to "Deployments" tab
   - Click on the latest deployment
   - Check the "Build Logs" for any errors

4. **Redeploy**
   - Sometimes a fresh deployment fixes routing issues
   - In Vercel dashboard: Click "Redeploy" on the latest deployment

5. **Clear cache and redeploy**
   ```bash
   vercel --prod --force
   ```

### Project Structure Verification

Make sure your project has this structure:
```
cursor-proj/
├── api/
│   └── analyze.py          ✅ Serverless function
├── public/
│   └── index.html          ✅ Frontend
├── requirements.txt        ✅ Dependencies (minimal - just openai)
├── vercel.json             ✅ Vercel configuration
└── README.md
```

### Environment Variables

**Optional**: Set `OPENROUTER_API_KEY` in Vercel dashboard:
- Go to Project Settings → Environment Variables
- Add: `OPENROUTER_API_KEY` = `your_key_here`
- This allows the app to work without users entering their own key

**Note**: Users can still enter their own API key in the app UI, so this is optional.

### Post-Deployment Checklist

- [ ] App loads at the root URL (`https://your-app.vercel.app`)
- [ ] API endpoint works (`/api/analyze`)
- [ ] Frontend can communicate with the API
- [ ] Test with a sample job posting and resume
- [ ] Verify error handling works correctly

### Common Issues

**Issue**: "404 NOT_FOUND" error
- **Solution**: Check that `vercel.json` routes are correct and files exist in the right locations

**Issue**: "Function exceeded size limit"
- **Solution**: Already fixed - `requirements.txt` only contains `openai` (minimal dependencies)

**Issue**: "Module not found" errors
- **Solution**: Ensure `requirements.txt` has all needed packages (should only be `openai`)

**Issue**: CORS errors
- **Solution**: Already handled in `api/analyze.py` with CORS headers

### Need Help?

- Vercel Documentation: https://vercel.com/docs
- Vercel Community: https://github.com/vercel/vercel/discussions
- Check deployment logs in Vercel dashboard for specific error messages
