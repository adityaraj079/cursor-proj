# Troubleshooting 404 Errors on Vercel

## Current Configuration

The `vercel.json` is now configured with:
- API route: `/api/analyze` → `api/analyze.py`
- Filesystem handler: Serves static files from `public/` directory
- Catch-all route: Falls back to `public/` for any other paths

## Debugging Steps

### 1. Check Deployment Logs
- Go to Vercel Dashboard → Your Project → Deployments
- Click on the latest deployment
- Check "Build Logs" and "Function Logs" for errors

### 2. Verify File Structure
Make sure these files exist in your repository:
```
✅ api/analyze.py
✅ public/index.html
✅ vercel.json
✅ requirements.txt
```

### 3. Test the API Endpoint
Try accessing: `https://your-app.vercel.app/api/analyze`
- If this works, the Python function is deployed correctly
- If this fails, check the function logs

### 4. Check Function Status
- Go to Vercel Dashboard → Your Project → Functions
- Verify that `api/analyze.py` appears and shows as "Ready"

## Alternative Solution: Move index.html to Root

If the current setup still doesn't work, try this:

1. **Move index.html to root**:
   ```bash
   mv public/index.html index.html
   ```

2. **Update vercel.json** to:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "api/analyze.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/api/analyze",
         "dest": "api/analyze.py"
       },
       {
         "src": "/(.*)",
         "dest": "/$1"
       }
     ]
   }
   ```

3. **Update .gitignore** to not ignore `index.html` (if needed)

## Alternative Solution: Root Route Handler

Create `api/index.py` to serve the HTML:

```python
from http.server import BaseHTTPRequestHandler
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Read index.html from public directory
        html_path = os.path.join(os.path.dirname(__file__), '..', 'public', 'index.html')
        with open(html_path, 'r') as f:
            html_content = f.read()
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
```

Then update `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/analyze.py",
      "use": "@vercel/python"
    },
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/analyze",
      "dest": "api/analyze.py"
    },
    {
      "src": "/",
      "dest": "api/index.py"
    },
    {
      "handle": "filesystem"
    }
  ]
}
```

## Quick Fix: Verify Current Setup

1. **Commit and push the updated vercel.json**:
   ```bash
   git add vercel.json
   git commit -m "Fix vercel.json routing"
   git push origin main
   ```

2. **Redeploy in Vercel**:
   - Go to Vercel Dashboard
   - Click "Redeploy" on the latest deployment
   - Or trigger a new deployment by pushing to GitHub

3. **Wait for deployment to complete** (check the status)

4. **Test the URL**:
   - Root: `https://your-app.vercel.app/`
   - API: `https://your-app.vercel.app/api/analyze` (POST request)

## Common Issues

**Issue**: Still getting 404
- **Check**: Are all files committed and pushed to GitHub?
- **Check**: Does the deployment show any errors in logs?
- **Try**: Clear browser cache or use incognito mode

**Issue**: API works but frontend doesn't
- **Check**: Is `public/index.html` in the repository?
- **Try**: Access `https://your-app.vercel.app/index.html` directly

**Issue**: Function not found
- **Check**: Is `api/analyze.py` in the repository?
- **Check**: Does it have the correct `handler` class?
