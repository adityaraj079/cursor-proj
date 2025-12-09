import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenRouter client will be created when needed

# Page configuration
st.set_page_config(
    page_title="Job Application Analyzer",
    page_icon="💼",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .stTextArea textarea {
        min-height: 200px;
    }
    </style>
""", unsafe_allow_html=True)

def get_openrouter_client(api_key=None):
    """
    Get or create OpenRouter client with API key
    Free models require HTTP-Referer and X-Title headers
    """
    if not api_key:
        return None
    
    # OpenRouter uses OpenAI-compatible API
    # For free models, we need to set custom headers
    return OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "https://github.com/yourusername/job-analyzer",  # Optional: Your site URL
            "X-Title": "Job Application Analyzer"  # Optional: Your app name
        }
    )

def analyze_job_application(job_posting, resume, model="meta-llama/llama-3.1-8b-instruct:free", api_key=None):
    """
    Analyze job posting and resume using OpenRouter API
    """
    client = get_openrouter_client(api_key=api_key)
    if not client:
        return "Error: OpenRouter API key not configured. Please set it in the sidebar or .env file."
    
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
        # For free models, OpenRouter may have rate limits or availability issues
        # Adding timeout and better error handling
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert career advisor with deep knowledge of job markets, hiring trends, and career development. Provide detailed, actionable, and encouraging feedback."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000,
            timeout=60.0  # 60 second timeout
        )
        
        if not response.choices or not response.choices[0].message.content:
            return "Error: Received empty response from the model. This might be due to rate limiting on free models. Please try again in a moment or use a paid model."
        
        return response.choices[0].message.content
    except Exception as e:
        error_msg = str(e)
        
        # Check for common free model issues
        if "rate limit" in error_msg.lower() or "429" in error_msg:
            return f"⚠️ **Rate Limit Reached**: Free models have usage limits (50/day, 1,000/day with $10+ credits). Please wait or consider using a paid model.\n\nTip: Check your usage at [openrouter.ai/activity](https://openrouter.ai/activity)"
        elif "404" in error_msg or "no endpoints found" in error_msg.lower() or "model_not_found" in error_msg.lower():
            return f"⚠️ **Model Not Available**: The model '{model.split(':')[0]}' is not currently available.\n\n**Solutions:**\n1. **Enable Model Training**: Go to [openrouter.ai/settings/privacy](https://openrouter.ai/settings/privacy) and enable 'Model Training' for free models\n2. **Try a different model**: Some free models may be temporarily unavailable\n3. **Use a paid model**: Remove ':free' suffix or select a paid model (more reliable)\n4. **Check model availability**: Visit [openrouter.ai/models](https://openrouter.ai/models) to see available models\n\nOriginal error: {error_msg}"
        elif "timeout" in error_msg.lower():
            return f"Error: Request timed out. Free models may be slow or overloaded. Try:\n1. Use a paid model for faster responses\n2. Retry in a moment\n\nOriginal error: {error_msg}"
        else:
            return f"Error: {error_msg}\n\n💡 **Tips**:\n- Enable 'Model Training' in [Privacy Settings](https://openrouter.ai/settings/privacy) for free models\n- Free models have rate limits (50 requests/day)\n- Paid models are more reliable and faster"

def main():
    # Header
    st.markdown('<h1 class="main-header">💼 Job Application Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar for API key input (if not in .env)
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.info("🆓 **Powered by OpenRouter**\n\nGet your free API key at [openrouter.ai](https://openrouter.ai)")
        
        st.markdown("""
        <div style='background-color: #fff3cd; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
        <strong>⚠️ Important for Free Models:</strong><br>
        Enable <strong>"Model Training"</strong> in your <a href="https://openrouter.ai/settings/privacy" target="_blank">Privacy Settings</a> to access free models!
        </div>
        """, unsafe_allow_html=True)
        
        api_key_input = st.text_input(
            "OpenRouter API Key",
            type="password",
            value=os.getenv("OPENROUTER_API_KEY", ""),
            help="Get your free API key at openrouter.ai"
        )
        
        if api_key_input:
            os.environ["OPENROUTER_API_KEY"] = api_key_input
        
        st.markdown("---")
        
        # Model selection
        st.header("🤖 Model Selection")
        
        st.warning("⚠️ **Free Model Note**: \n- 50 free requests/day (1,000 with $10+ credits)\n- Models may be unavailable or slow\n\n💡 **Tip**: Paid models are more reliable!")
        
        model_options = {
            "Meta Llama 3.1 8B (Free) ⚠️": "meta-llama/llama-3.1-8b-instruct:free",
            "Meta Llama 3.2 3B (Free) ⚠️": "meta-llama/llama-3.2-3b-instruct:free",
            "Mistral 7B (Free) ⚠️": "mistralai/mistral-7b-instruct:free",
            "Google Gemma 2B (Free) ⚠️": "google/gemma-2b-it:free",
            "Qwen 2.5 7B (Free) ⚠️": "qwen/qwen-2.5-7b-instruct:free",
            "--- Paid Models (More Reliable) ---": "---",
            "Meta Llama 3.1 70B": "meta-llama/llama-3.1-70b-instruct",
            "Meta Llama 3.1 8B (Paid)": "meta-llama/llama-3.1-8b-instruct",
            "Mistral Large": "mistralai/mistral-large",
            "Mistral 7B (Paid)": "mistralai/mistral-7b-instruct",
            "Anthropic Claude 3.5 Sonnet": "anthropic/claude-3.5-sonnet",
            "Anthropic Claude 3 Opus": "anthropic/claude-3-opus",
            "Google Gemini Pro": "google/gemini-pro",
        }
        
        selected_model_name = st.selectbox(
            "Choose Model",
            options=list(model_options.keys()),
            index=6,  # Default to a paid model for reliability
            help="Free models may be rate-limited. Paid models are more reliable."
        )
        selected_model = model_options[selected_model_name]
        
        if selected_model == "---":
            st.error("⚠️ Please select a valid model (not the separator).")
            selected_model = "meta-llama/llama-3.1-70b-instruct"  # Fallback
        
        st.markdown("---")
        st.info("📝 Paste your job posting and resume in the main area, then click 'Analyze Application' to get insights.")
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">📄 Job Posting</div>', unsafe_allow_html=True)
        job_posting = st.text_area(
            "Paste the job posting here",
            height=400,
            placeholder="Paste the complete job description, requirements, and details here...",
            help="Include job title, requirements, responsibilities, and company information"
        )
    
    with col2:
        st.markdown('<div class="section-header">📋 Your Resume</div>', unsafe_allow_html=True)
        resume = st.text_area(
            "Paste your resume here",
            height=400,
            placeholder="Paste your complete resume here...",
            help="Include your experience, skills, education, and achievements"
        )
    
    st.markdown("---")
    
    # Analyze button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        analyze_button = st.button(
            "🔍 Analyze Application",
            type="primary",
            use_container_width=True,
            help="Click to analyze your application match"
        )
    
    # Analysis results
    if analyze_button:
        if not job_posting or not resume:
            st.error("⚠️ Please provide both job posting and resume to analyze.")
        elif not api_key_input:
            st.error("⚠️ Please provide your OpenRouter API key in the sidebar. Get a free key at [openrouter.ai](https://openrouter.ai)")
        elif selected_model == "---":
            st.error("⚠️ Please select a valid model from the dropdown.")
        else:
            with st.spinner("🤔 Analyzing your application... This may take a moment."):
                analysis = analyze_job_application(
                    job_posting, 
                    resume, 
                    model=selected_model,
                    api_key=api_key_input
                )
                
                st.markdown("---")
                st.markdown('<div class="section-header">📊 Analysis Results</div>', unsafe_allow_html=True)
                st.markdown(analysis)
                
                # Download button for results
                st.download_button(
                    label="📥 Download Analysis",
                    data=analysis,
                    file_name="job_application_analysis.md",
                    mime="text/markdown"
                )

if __name__ == "__main__":
    main()

