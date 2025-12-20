import os
import requests
import google.generativeai as genai
import subprocess

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# GitHub Environment Variables
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
    payload = {"body": comment_body}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        print("Successfully posted comment to PR.")
    else:
        print(f"Failed to post comment: {response.status_code}, {response.text}")

def run_review():
    # 1. Fetch main to compare
    subprocess.run(['git', 'fetch', 'origin', 'main'], check=True)
    
    # 2. Get the diff (code changes)
    diff = subprocess.check_output(['git', 'diff', 'origin/main...HEAD']).decode('utf-8')
    
    # 3. Ask Gemini to analyze
    prompt = f"""
    Evaluate this Pull Request:
    - Should we PROCEED or SKIP?
    - Is the code redundant?
    - List 3 quality improvements for professional standards.
    
    DIFF:
    {diff}
    """
    
    response = model.generate_content(prompt)
    
    # 4. Post back to GitHub
    final_feedback = f"### 🤖 Gemini AI Review\n\n{response.text}"
    post_github_comment(final_feedback)

if __name__ == "__main__":
    if pr_number: # Only run if inside a PR context
        run_review()