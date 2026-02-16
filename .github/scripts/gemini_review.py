import os
import requests
import subprocess
from google import genai

# 1. Initialize API Key with Error Handling
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # This will print a clear message in your GitHub Actions logs if the secret is missing
    raise ValueError("ERROR: GEMINI_API_KEY is not set. Check your GitHub Secrets and YAML 'env' block.")

# Setup the new 2025 Client
client = genai.Client(api_key=api_key)

repo = os.getenv("GITHUB_REPOSITORY")
pr_number = os.getenv("PR_NUMBER")
token = os.getenv("GITHUB_TOKEN")

def post_github_comment(comment_body):
    """Posts the Gemini review as a comment on the Pull Request."""
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.post(url, json={"body": comment_body}, headers=headers)
    if response.status_code == 201:
        print("Successfully posted comment to PR.")
    else:
        print(f"Failed to post comment. Status: {response.status_code}, Error: {response.text}")

def run_review():
    try:
        # Fetch the main branch history to ensure a 'merge base' exists
        subprocess.run(['git', 'fetch', 'origin', 'main'], check=True)
        
        # Get the code changes (the 'diff')
        diff = subprocess.check_output(['git', 'diff', 'origin/main...HEAD']).decode('utf-8')
        
        if not diff:
            print("No changes detected in this Pull Request.")
            return

        # 2. Generate Review using Gemini 2.0 Flash
        response = client.models.generate_content(
            model='gemini-2.0-flash', # Fastest 2025 model
            contents=f"You are a professional code reviewer. Analyze this PR diff for quality, logic, and security:\n\n{diff}"
        )
        
        # 3. Post Feedback to GitHub
        feedback = f"### 🤖 Gemini AI Gatekeeper Review\n\n{response.text}"
        post_github_comment(feedback)

    except subprocess.CalledProcessError as e:
        print(f"Git Error: {e}. Ensure your YAML has 'fetch-depth: 0'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if pr_number:
        run_review()
    else:
        print("PR_NUMBER not found. This script must run inside a Pull Request context.")
