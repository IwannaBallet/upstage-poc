#!/bin/bash
# Script to push AskUp PoC to GitHub
# Replace YOUR_USERNAME with your actual GitHub username

echo "🚀 Pushing AskUp PoC to GitHub..."
echo ""

# Check if remote already exists
if git remote get-url origin &>/dev/null; then
    echo "✅ Remote 'origin' already exists"
    git remote -v
else
    echo "📝 Please provide your GitHub username:"
    read -p "GitHub username: " GITHUB_USERNAME
    
    if [ -z "$GITHUB_USERNAME" ]; then
        echo "❌ Error: GitHub username is required"
        exit 1
    fi
    
    echo ""
    echo "🔗 Adding remote repository..."
    git remote add origin https://github.com/${GITHUB_USERNAME}/askup-poc.git
fi

echo ""
echo "📤 Pushing to GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "🌐 Your repository: https://github.com/${GITHUB_USERNAME}/askup-poc"
else
    echo ""
    echo "❌ Push failed. Make sure:"
    echo "   1. You've created the repository on GitHub.com"
    echo "   2. You're authenticated (git will prompt for credentials)"
    echo "   3. The repository name matches: askup-poc"
fi

