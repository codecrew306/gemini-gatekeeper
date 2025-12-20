import os
import requests
import subprocess
from google import genai

# 1. Setup the new 2025 Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

repo = os.getenv("GITHUB_REPOSITORY")
pr_number = os.getenv("PR_NUMBER")
token = os.getenv("GITHUB_TOKEN")

def post_github_comment(comment_body):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    requests.post(url, json={"body": comment_body}, headers=headers)

def run_review():
    try:
        # Ensure we have the main branch to compare against
        subprocess.run(['git', 'fetch', 'origin', 'main'], check=True)
        
        # Get the code changes
        diff = subprocess.check_output(['git', 'diff', 'origin/main...HEAD']).decode('utf-8')
        
        if not diff:
            print("No changes to review.")
            return

        # 2. Generate Review using Gemini 2.0 Flash
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=f"You are a professional code reviewer. Analyze this PR diff for quality and logic:\n\n{diff}"
        )
        
        # 3. Post to PR
        feedback = f"### 🤖 Gemini AI Code Review\n\n{response.text}"
        post_github_comment(feedback)
        print("Review posted successfully!")

    except Exception as e:
        print(f"Error during review: {e}")

if __name__ == "__main__":
    if pr_number:
        run_review()