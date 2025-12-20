import os
import requests
import subprocess
from google import genai

# 1. Secure API Key Retrieval
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # This will print a clear message in your GitHub Actions log if the key is missing
    raise ValueError("ERROR: GEMINI_API_KEY is not set. Check your GitHub Secrets and YAML 'env' block.")

# Initialize the 2025 Client
client = genai.Client(api_key=api_key)

repo = os.getenv("GITHUB_REPOSITORY")
pr_number = os.getenv("PR_NUMBER")
token = os.getenv("GITHUB_TOKEN")

def post_github_comment(comment_body):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.post(url, json={"body": comment_body}, headers=headers)
    if response.status_code != 201:
        print(f"Failed to post comment. Status: {response.status_code}, Error: {response.text}")

def run_review():
    try:
        # Ensure we have the main branch history to compare against
        subprocess.run(['git', 'fetch', 'origin', 'main'], check=True)
        
        # Get the code changes
        diff = subprocess.check_output(['git', 'diff', 'origin/main...HEAD']).decode('utf-8')
        
        if not diff:
            print("No changes found in this Pull Request.")
            return

        # 2. AI Analysis using Gemini 2.0 Flash
        prompt = f"""
        Act as a professional code reviewer for a student group. 
        Analyze this PR diff and provide:
        - A 'PROCEED' or 'REVISE' recommendation.
        - Analysis of code logic and quality.
        - Check for hardcoded secrets or passwords.
        
        DIFF DATA:
        {diff}
        """
        
        response = client.models.generate_content(
            model='gemini-2.0-flash', # Fastest and latest 2025 model
            contents=prompt
        )
        
        # 3. Post Feedback to GitHub
        feedback = f"### 🤖 Gemini AI Gatekeeper Review\n\n{response.text}"
        post_github_comment(feedback)
        print("Review successfully posted to the Pull Request.")

    except subprocess.CalledProcessError as e:
        print(f"Git Error: {e}. Check if main branch exists in the runner history.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if pr_number:
        run_review()
    else:
        print("PR_NUMBER not found. This script should run within a GitHub Pull Request context.")
