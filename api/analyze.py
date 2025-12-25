import json
import os
import requests
from http.server import BaseHTTPRequestHandler

def get_gemini_api_url():
    """
    Get Gemini API URL from environment or use default
    """
    api_url = os.getenv("GEMINI_API_URL", "https://generativelanguage.googleapis.com/v1beta")
    # Ensure it doesn't end with a slash
    return api_url.rstrip('/')

def get_gemini_model(api_key=None, model_name="gemini-pro"):
    """
    Get Gemini model name - defaults to gemini-pro
    """
    # Default model for Gemini
    return model_name

def analyze_job_application(job_posting, resume, model="gemini-pro", api_key=None):
    """
    Analyze job posting and resume using Google Gemini API
    """
    if not api_key:
        return {"error": "Gemini API key not configured."}
    
    api_url = get_gemini_api_url()
    
    prompt = f"""You are an expert career advisor and job application analyst. Analyze the following job posting and resume to provide comprehensive feedback.

JOB POSTING:
{job_posting}

USER RESUME:
{resume}

Please provide a detailed analysis in the following format:

## 🎯 APPLICATION RECOMMENDATION
[Provide a clear recommendation: Should the user apply for this job? Why or why not? Include a confidence level (High/Medium/Low) and specific reasons.]

## 📋 JOB PROFILE MATCH ANALYSIS
[Analyze how well the resume matches the job requirements. Break down:
- Skills match percentage
- Experience level alignment
- Education/qualifications match
- Key strengths that align with the role
- Potential gaps or concerns]

## 🎯 TARGET JOB PROFILES
[Based on the user's resume, list 5-7 specific job titles/roles they should target. For each role, explain:
- Why this role fits their profile
- What experience level (Entry/Junior/Mid/Senior/Lead)
- Key skills that make them suitable]

## 📊 EXPERIENCE LEVEL ASSESSMENT
[Assess the user's experience level based on their resume:
- Current level (e.g., "Mid-level with 3-5 years experience")
- Appropriate roles for their level
- What they need to reach the next level]

## ⏰ TIMING ANALYSIS
[Provide insights on application timing:
- Is this a good time to apply for this role? (Consider market trends, hiring seasons)
- When do major companies typically open roles at this seniority level?
- Best times of year to apply for similar positions
- Market demand for this role currently]

## 💡 RECOMMENDATIONS
[Provide actionable recommendations:
- What to emphasize in their application
- Skills to highlight
- Any resume improvements needed
- Networking or preparation tips]

Be specific, actionable, and encouraging. Use emojis sparingly for better readability."""

    try:
        # Gemini API endpoint
        model_name = get_gemini_model(api_key, model)
        url = f"{api_url}/models/{model_name}:generateContent"
        
        # Gemini API request format
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"You are an expert career advisor with deep knowledge of job markets, hiring trends, and career development. Provide detailed, actionable, and encouraging feedback.\n\n{prompt}"
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 2048,
            }
        }
        
        headers = {
            "Content-Type": "application/json",
        }
        
        # Make request to Gemini API
        response = requests.post(
            f"{url}?key={api_key}",
            headers=headers,
            json=payload,
            timeout=60.0
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Extract text from Gemini response
        if "candidates" not in result or not result["candidates"]:
            return {"error": "Received empty response from Gemini API. Please try again."}
        
        if "content" not in result["candidates"][0] or "parts" not in result["candidates"][0]["content"]:
            return {"error": "Unexpected response format from Gemini API. Please try again."}
        
        analysis_text = result["candidates"][0]["content"]["parts"][0]["text"]
        
        if not analysis_text:
            return {"error": "Received empty response from the model. Please try again."}
        
        return {"analysis": analysis_text}
    except requests.exceptions.HTTPError as e:
        error_msg = str(e)
        status_code = e.response.status_code if hasattr(e, 'response') else None
        
        if status_code == 429:
            return {"error": "⚠️ **Rate Limit Reached**: You've exceeded the API rate limit. Please wait a moment and try again.\n\nTip: Check your Gemini API quota in the Google Cloud Console."}
        elif status_code == 401 or status_code == 403:
            return {"error": "⚠️ **Authentication Error**: Invalid API key. Please check your Gemini API key and ensure it's correctly configured.\n\nTip: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)"}
        elif status_code == 404:
            return {"error": f"⚠️ **Model Not Available**: The model '{model}' is not available or doesn't exist.\n\n**Solutions:**\n1. Try using 'gemini-pro' or 'gemini-1.5-pro'\n2. Check available models at [Google AI Studio](https://makersuite.google.com/app/apikey)\n\nOriginal error: {error_msg}"}
        else:
            return {"error": f"⚠️ **API Error** (Status {status_code}): {error_msg}\n\nPlease check your API key and try again."}
    except requests.exceptions.Timeout:
        return {"error": "Error: Request timed out. The API took too long to respond. Please try again."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error: Network error occurred. {str(e)}\n\nPlease check your internet connection and API URL configuration."}
    except Exception as e:
        error_msg = str(e)
        return {"error": f"Error: {error_msg}\n\n💡 **Tips**:\n- Check that your Gemini API key is valid\n- Verify the API URL is correct in your .env file\n- Ensure you have API access enabled"}

class handler(BaseHTTPRequestHandler):
    """
    Vercel serverless function handler
    """
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            body_data = json.loads(body.decode('utf-8'))
            
            job_posting = body_data.get("job_posting", "")
            resume = body_data.get("resume", "")
            model = body_data.get("model", "gemini-pro")
            api_key = os.getenv("GEMINI_API_KEY")
            
            if not job_posting or not resume:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Please provide both job posting and resume."}).encode('utf-8'))
                return
            
            if not api_key:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Gemini API key is not configured. Please set GEMINI_API_KEY environment variable."}).encode('utf-8'))
                return
            
            result = analyze_job_application(job_posting, resume, model, api_key)
            
            status_code = 400 if "error" in result else 200
            self.send_response(status_code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
        
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON in request body"}).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"Internal server error: {str(e)}"}).encode('utf-8'))
