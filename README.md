# gemini-gatekeeper
# 🤖 Gemini Gatekeeper: AI-Powered Code Governance

This repository features an automated **CI/CD Pipeline** that uses **Google Gemini 1.5 Flash** to perform intelligent code reviews on every Pull Request. It is designed to ensure high code quality, consistency, and logical necessity before any code is merged into the `main` branch.

## 🚀 Key Features

- **Automated PR Analysis:** Every Pull Request is automatically scanned by Gemini AI.
- **State Comparison:** Checks if the proposed changes are necessary or redundant.
- **Quality Gatekeeping:** Enforces professional standards (SOLID principles, naming conventions, and security).
- **Instant Feedback:** Gemini posts a detailed review comment directly on the GitHub PR page.

---

## 🛠️ How It Works

1. **Trigger:** A student opens a Pull Request in the Organization.
2. **Workflow:** GitHub Actions triggers the `.github/workflows/gemini-review.yml`.
3. **Analysis:** The `.github/scripts/gemini_review.py` script extracts the code `diff` and sends it to the Gemini API.
4. **Action:** Gemini evaluates the code based on professional developer standards and provides a "PROCEED" or "SKIP" recommendation.

---

## 📁 Repository Structure

Plaintext

`.github/
├── workflows/
│   └── gemini-review.yml  # GitHub Actions configuration
└── scripts/
    └── gemini_review.py   # Python logic & Gemini API integration`

---

## ⚙️ Setup for Organization Members

To contribute to this project and use the AI gatekeeper:

1. **Create a New Branch:**Bash
    
    `git checkout -b feature/your-feature-name`
    
2. **Commit Your Changes:**Bash
    
    `git add .
    git commit -m "Add professional logic"`
    
3. Open a Pull Request:
    
    Once you push your branch, open a PR on GitHub. Look at the "Actions" tab or wait for the Gemini AI comment to appear on your PR.
    

---

## ⚖️ Standards Enforced

Our Gemini Gatekeeper is instructed to look for:

- **Clean Code:** Variable naming and function length.
- **Security:** Prevention of hardcoded secrets.
- **Logic:** Efficiency of algorithms ($O(n)$ vs $O(n^2)$).
- **Documentation:** Presence of helpful comments.