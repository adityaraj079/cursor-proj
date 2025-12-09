# 💼 Job Application Analyzer

An AI-powered web application that helps job seekers determine whether they should apply for a position by analyzing their resume against job postings. Powered by OpenRouter, the app provides comprehensive insights including job match analysis, target job profiles, experience level assessment, and timing recommendations.

**Deployed on Vercel** - Ready for production use!

## Features

- **Application Recommendation**: Get a clear recommendation on whether to apply with confidence levels
- **Job Profile Match Analysis**: Detailed breakdown of skills, experience, and qualifications alignment
- **Target Job Profiles**: Discover 5-7 job roles that match your resume
- **Experience Level Assessment**: Understand your current level and appropriate roles
- **Timing Analysis**: Insights on when to apply based on market trends and hiring seasons
- **Actionable Recommendations**: Get specific advice on improving your application

## 🚀 Quick Start (Vercel Deployment)

### Deploy to Vercel

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Deploy the application**:
   ```bash
   vercel
   ```

3. **Set environment variable** (optional, for default API key):
   - Go to your Vercel project dashboard
   - Navigate to Settings → Environment Variables
   - Add `OPENROUTER_API_KEY` with your API key value
   - Users can still enter their own API key in the app

4. **Your app is live!** Visit the URL provided by Vercel

### Local Development

1. **Clone or download this repository**

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Vercel development server**:
   ```bash
   vercel dev
   ```

4. **Or use Python's HTTP server for frontend** (for testing):
   ```bash
   cd public && python -m http.server 8000
   ```

## Usage

1. **Open the application** in your web browser (deployed URL or localhost)

2. **In the sidebar**:
   - Enter your OpenRouter API key (get a free one at [openrouter.ai](https://openrouter.ai))
   - Select a model (free and paid models available!)

3. **Paste the job posting** in the left text area

4. **Paste your resume** in the right text area

5. **Click "🔍 Analyze Application"** to get comprehensive insights

6. **Review the analysis results**, which include:
   - Application recommendation
   - Job profile match analysis
   - Target job profiles you should consider
   - Experience level assessment
   - Timing analysis for applications
   - Actionable recommendations

7. **Download the analysis** as a markdown file (optional)

## Project Structure

```
cursor-proj/
├── api/
│   └── analyze.py     # Vercel serverless function (Python)
├── public/
│   └── index.html     # Frontend web application
├── app.py             # Original Streamlit app (legacy)
├── requirements.txt   # Python dependencies
├── vercel.json        # Vercel configuration
└── README.md          # This file
```

## Technologies Used

- **Vercel**: Serverless hosting platform
- **Python**: Serverless API functions
- **HTML/CSS/JavaScript**: Frontend interface
- **OpenRouter API**: Access to free and paid AI models

## Available Models

This app uses **OpenRouter**, which provides access to various AI models:

### Free Models (May have limitations)
- Meta Llama 3.1 8B (Free) ⚠️
- Meta Llama 3.2 3B (Free) ⚠️
- Mistral 7B (Free) ⚠️
- Google Gemma 2B (Free) ⚠️
- Qwen 2.5 7B (Free) ⚠️

### Paid Models (More Reliable)
- Meta Llama 3.1 70B
- Mistral Large
- Anthropic Claude 3.5 Sonnet
- Anthropic Claude 3 Opus
- Google Gemini Pro
- And many more!

## ⚠️ Why Free Models May Not Work

Free models on OpenRouter may experience:
1. **Rate Limiting**: Free models have usage limits and may return empty responses when limits are reached
2. **Availability**: Free models may be temporarily unavailable due to high demand
3. **Slower Responses**: Free models may take longer to respond or timeout
4. **Model Restrictions**: Some free models may not be accessible depending on your account status

**Solution**: 
- Wait a few minutes and try again
- Use a paid model (they're more reliable and faster)
- Check your OpenRouter dashboard for usage limits and model availability

Get your free API key at [openrouter.ai](https://openrouter.ai) - no credit card required!

## How It Works

The application uses OpenAI's GPT-4 model to analyze:
1. The job posting requirements, responsibilities, and qualifications
2. Your resume's experience, skills, education, and achievements
3. Market trends and hiring patterns

It then provides a comprehensive analysis covering all aspects mentioned in the features section.

## Tips for Best Results

- Include complete job descriptions with all requirements
- Provide a comprehensive resume with all relevant experience
- Be specific about your skills and achievements
- The more detailed the inputs, the better the analysis

## License

This project is open source and available for personal use.

## Support

For issues or questions, please check:
- OpenRouter API documentation: https://openrouter.ai/docs
- Vercel documentation: https://vercel.com/docs

