# Migration from OpenRouter to Google Gemini API

## Changes Made

### 1. Backend API (`api/analyze.py`)

**Replaced:**
- `OpenAI` client library (OpenAI-compatible OpenRouter API)
- OpenRouter-specific headers and configuration

**With:**
- `requests` library for direct HTTP calls to Gemini API
- Gemini API REST endpoint structure
- Environment variable support for `GEMINI_API_KEY` and `GEMINI_API_URL`

### 2. Frontend (`index.html`)

**Updated:**
- All references to "OpenRouter" → "Google Gemini"
- API key input label and placeholders
- Model selection dropdown (now shows Gemini models: gemini-pro, gemini-1.5-pro, gemini-1.5-flash)
- Error messages and help text
- Links point to Google AI Studio instead of OpenRouter

### 3. Dependencies (`requirements.txt`)

**Changed:**
- Removed: `openai>=2.0.0`
- Added: `requests>=2.31.0`

### 4. Environment Variables

**New environment variables:**
- `GEMINI_API_KEY` - Your Gemini API key (required)
- `GEMINI_API_URL` - Optional, defaults to `https://generativelanguage.googleapis.com/v1beta`

## Environment Setup

Add these to your `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta
```

**Note:** `GEMINI_API_URL` is optional - if not provided, it defaults to the standard Gemini API URL.

## How It Works

### API Request Flow

1. User submits job posting and resume via frontend
2. Frontend sends POST request to `/api/analyze` with:
   - `job_posting`: The job description
   - `resume`: The user's resume
   - `model`: Gemini model name (e.g., "gemini-pro")
   - `api_key`: User's Gemini API key (or uses env var if not provided)

3. Backend (`api/analyze.py`):
   - Validates inputs
   - Constructs Gemini API request:
     - URL: `{GEMINI_API_URL}/models/{model}:generateContent?key={api_key}`
     - Method: POST
     - Body: JSON with prompt in Gemini format
   - Makes HTTP request to Gemini API
   - Parses response and extracts analysis text
   - Returns JSON response to frontend

### Gemini API Format

The code now uses Gemini's native API format:
```json
{
  "contents": [{
    "parts": [{
      "text": "Your prompt here"
    }]
  }],
  "generationConfig": {
    "temperature": 0.7,
    "maxOutputTokens": 2048
  }
}
```

## Available Models

The frontend now offers these Gemini models:

1. **gemini-pro** (Default) - General purpose, balanced performance
2. **gemini-1.5-pro** - Latest and most capable model
3. **gemini-1.5-flash** - Fast and efficient model

## Error Handling

The code now handles Gemini-specific errors:
- **401/403**: Invalid API key
- **404**: Model not found
- **429**: Rate limit exceeded
- **Timeout**: Request timeout
- **Network errors**: Connection issues

All errors return user-friendly messages with helpful tips.

## Testing

1. **Local Testing:**
   ```bash
   # Make sure your .env has GEMINI_API_KEY
   vercel dev
   ```

2. **Production:**
   - Set `GEMINI_API_KEY` in Vercel dashboard → Settings → Environment Variables
   - Users can also enter their own API key in the UI

## Getting Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key and add it to your `.env` file or Vercel environment variables

## Differences from OpenRouter

| Feature | OpenRouter | Gemini |
|---------|------------|--------|
| API Format | OpenAI-compatible | Native REST API |
| Key Location | Header | Query parameter |
| Base URL | `https://openrouter.ai/api/v1` | Configurable (default: `https://generativelanguage.googleapis.com/v1beta`) |
| Model Names | Various providers | Gemini-specific |
| Rate Limits | Varies by model | Based on Google Cloud quota |

## Troubleshooting

### "Invalid API key" error
- Verify your `GEMINI_API_KEY` is correct
- Check that the API key is enabled in Google Cloud Console
- Ensure you haven't exceeded your quota

### "Model not found" error
- Verify the model name (should be: `gemini-pro`, `gemini-1.5-pro`, or `gemini-1.5-flash`)
- Check that the model is available in your region

### API URL issues
- If using a custom API URL, ensure `GEMINI_API_URL` is set correctly
- The URL should not include `/models` or trailing slashes
- Default URL: `https://generativelanguage.googleapis.com/v1beta`
