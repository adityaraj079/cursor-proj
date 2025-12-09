import json
import os
from http.server import BaseHTTPRequestHandler
from openai import OpenAI

def get_openrouter_client(api_key=None):
    """
    Get or create OpenRouter client with API key
    Free models require HTTP-Referer and X-Title headers
    """
    if not api_key:
        return None
    
    # OpenRouter uses OpenAI-compatible API
    # For free models, we need to set custom headers
    # VERCEL_URL contains only the domain (e.g., "my-app.vercel.app")
    # We need to ensure it has the https:// protocol prefix
    vercel_url = os.getenv("VERCEL_URL", "")
    if vercel_url:
        # Ensure protocol prefix is present
        if not vercel_url.startswith("http://") and not vercel_url.startswith("https://"):
            vercel_url = f"https://{vercel_url}"
    else:
        # Fallback to a default URL with protocol
        vercel_url = "https://your-app.vercel.app"
    
    return OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": vercel_url,
            "X-Title": "Job Application Analyzer"
        }
    )

def analyze_job_application(job_posting, resume, model="meta-llama/llama-3.1-8b-instruct:free", api_key=None):
    """
    Analyze job posting and resume using OpenRouter API
    """
    client = get_openrouter_client(api_key=api_key)
    if not client:
        return {"error": "OpenRouter API key not configured."}
    
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
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert career advisor with deep knowledge of job markets, hiring trends, and career development. Provide detailed, actionable, and encouraging feedback."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000,
            timeout=60.0
        )
        
        if not response.choices or not response.choices[0].message.content:
            return {"error": "Received empty response from the model. This might be due to rate limiting on free models. Please try again in a moment or use a paid model."}
        
        return {"analysis": response.choices[0].message.content}
    except Exception as e:
        error_msg = str(e)
        
        # Check for common free model issues
        if "rate limit" in error_msg.lower() or "429" in error_msg:
            return {"error": "⚠️ **Rate Limit Reached**: Free models have usage limits (50/day, 1,000/day with $10+ credits). Please wait or consider using a paid model.\n\nTip: Check your usage at [openrouter.ai/activity](https://openrouter.ai/activity)"}
        elif "404" in error_msg or "no endpoints found" in error_msg.lower() or "model_not_found" in error_msg.lower():
            return {"error": f"⚠️ **Model Not Available**: The model '{model.split(':')[0]}' is not currently available.\n\n**Solutions:**\n1. **Try a different model**: Some free models may be temporarily unavailable\n2. **Use a paid model**: Remove ':free' suffix or select a paid model (more reliable)\n3. **Check model availability**: Visit [openrouter.ai/models](https://openrouter.ai/models) to see available models\n\nOriginal error: {error_msg}"}
        elif "timeout" in error_msg.lower():
            return {"error": f"Error: Request timed out. Free models may be slow or overloaded. Try:\n1. Use a paid model for faster responses\n2. Retry in a moment\n\nOriginal error: {error_msg}"}
        else:
            return {"error": f"Error: {error_msg}\n\n💡 **Tips**:\n- Free models have rate limits (50 requests/day)\n- Paid models are more reliable and faster"}

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
            model = body_data.get("model", "meta-llama/llama-3.1-70b-instruct")
            api_key = body_data.get("api_key", os.getenv("OPENROUTER_API_KEY"))
            
            if not job_posting or not resume:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Please provide both job posting and resume."}).encode('utf-8'))
                return
            
            if not api_key:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "OpenRouter API key is required. Please provide it in the request or set OPENROUTER_API_KEY environment variable."}).encode('utf-8'))
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
