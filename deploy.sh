#!/bin/bash

# Vital Lens AI - Quick Deployment Script
# This script helps set up the deployment environment

set -e

echo "🚀 Vital Lens AI - Deployment Setup"
echo "===================================="
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."
command -v git &> /dev/null && echo "✅ Git installed" || { echo "❌ Git not found"; exit 1; }
command -v node &> /dev/null && echo "✅ Node.js installed" || { echo "❌ Node.js not found"; exit 1; }

# Verify git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Please run from project root."
    exit 1
fi

echo "✅ In git repository"
echo ""

# Check git status
echo "📌 Git Status:"
git status --short | head -5
echo ""

# Ask for deployment method
echo "🔧 Choose deployment method:"
echo "1) Vercel (Frontend only) - Recommended"
echo "2) Railway (Full stack)"
echo "3) Render (Full stack)"
echo "4) Manual setup"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "📍 Vercel Frontend Deployment"
        echo "=============================="
        echo ""
        echo "Prerequisites:"
        echo "1. Create a Vercel account: https://vercel.com"
        echo "2. Push code to GitHub: https://github.com/new"
        echo ""
        echo "Steps:"
        echo "1. Visit https://vercel.com/dashboard"
        echo "2. Click 'Add New' → 'Project'"
        echo "3. Select 'Import Git Repository'"
        echo "4. Choose 'vital-lens-ai' repository"
        echo "5. Configure settings:"
        echo "   - Framework: Vite"
        echo "   - Root Directory: phase3_application/frontend"
        echo "   - Build: npm run build"
        echo "   - Output: dist"
        echo "6. Add environment variables:"
        echo "   - VITE_API_URL=https://your-backend-url.com/api/v1"
        echo "7. Click Deploy"
        echo ""
        read -p "Press Enter after deploying to Vercel..."
        echo "✅ Vercel deployment complete!"
        ;;
    2)
        echo ""
        echo "📍 Railway Full Stack Deployment"
        echo "================================="
        echo ""
        echo "Prerequisites:"
        echo "1. Create Railway account: https://railway.app"
        echo "2. Push code to GitHub"
        echo ""
        echo "Steps:"
        echo "1. Visit https://railway.app"
        echo "2. Create 'New Project' → 'Deploy from GitHub repo'"
        echo "3. Select 'vital-lens-ai' repository"
        echo "4. Add PostgreSQL service"
        echo "5. Configure backend environment variables"
        echo "6. Deploy and copy backend URL"
        echo ""
        echo "Then deploy frontend to Vercel (see option 1)"
        echo ""
        read -p "Press Enter after setting up Railway..."
        ;;
    3)
        echo ""
        echo "📍 Render Full Stack Deployment"
        echo "================================"
        echo ""
        echo "Prerequisites:"
        echo "1. Create Render account: https://render.com"
        echo "2. Push code to GitHub"
        echo ""
        echo "Steps:"
        echo "1. Visit https://render.com"
        echo "2. Create 'New' → 'Web Service'"
        echo "3. Connect GitHub repo"
        echo "4. Configure:"
        echo "   - Root: phase3_application/backend"
        echo "   - Build: pip install -r requirements-prod.txt"
        echo "   - Start: uvicorn main:app --host 0.0.0.0 --port \$PORT"
        echo "5. Add PostgreSQL service"
        echo "6. Deploy"
        echo ""
        echo "Then deploy frontend to Vercel (see option 1)"
        echo ""
        read -p "Press Enter after setting up Render..."
        ;;
    4)
        echo ""
        echo "📍 Manual Deployment"
        echo "===================="
        echo ""
        echo "See DEPLOYMENT_CHECKLIST.md for detailed instructions"
        echo "Run: cat DEPLOYMENT_CHECKLIST.md"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

# Final steps
echo ""
echo "🎉 Next Steps:"
echo "1. Visit your deployed frontend URL"
echo "2. Test camera functionality"
echo "3. Try saving a measurement"
echo "4. Check Reports page for saved data"
echo "5. Monitor logs in Vercel/Railway/Render dashboards"
echo ""
echo "📚 For more details, see VERCEL_DEPLOYMENT_GUIDE.md"
echo "✅ Deployment setup complete!"
