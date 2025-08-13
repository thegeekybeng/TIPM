#!/bin/bash

# 🚀 TIPM Hugging Face Spaces Deployment Script
# This script automates the deployment process to HF Spaces

echo "🚀 Starting TIPM v1.5 deployment to Hugging Face Spaces..."

# Check if we're in the right directory
if [ ! -f "huggingface-spaces/app.py" ]; then
    echo "❌ Error: Please run this script from the TIPM project root directory"
    exit 1
fi

# Check if HF Space exists
HF_SPACE_URL="https://huggingface.co/spaces/thegeekybeng/TIPM"
echo "🔍 Checking if HF Space exists: $HF_SPACE_URL"

# Create deployment directory
DEPLOY_DIR="hf_deployment_$(date +%Y%m%d_%H%M%S)"
echo "📁 Creating deployment directory: $DEPLOY_DIR"
mkdir -p "$DEPLOY_DIR"

# Copy HF Spaces files
echo "📋 Copying deployment files..."
cp -r huggingface-spaces/* "$DEPLOY_DIR/"
cp -r tipm "$DEPLOY_DIR/"
cp -r data "$DEPLOY_DIR/"

# Create .gitattributes for HF Spaces
echo "⚙️ Creating HF Spaces configuration..."
cat > "$DEPLOY_DIR/.gitattributes" << 'EOF'
*.py linguist-language=Python
*.md linguist-documentation
*.txt linguist-documentation
*.json linguist-documentation
*.csv linguist-documentation
tipm/ linguist-vendored
data/ linguist-vendored
EOF

# Create deployment info
echo "📊 Creating deployment info..."
cat > "$DEPLOY_DIR/DEPLOYMENT_INFO.md" << 'EOF'
# 🚀 TIPM v1.5 Deployment Package

**Deployment Date**: $(date)
**Version**: 1.5.0
**Status**: Ready for HF Spaces

## 📁 Files Included
- `app.py` - Main Gradio application
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation
- `tipm/` - Core TIPM modules
- `data/` - Sample datasets
- `.gitattributes` - HF Spaces configuration

## 🚀 Next Steps
1. Clone your HF Space: `git clone https://huggingface.co/spaces/YOUR_USERNAME/TIPM`
2. Copy these files to the cloned directory
3. Commit and push: `git add . && git commit -m "Deploy TIPM v1.5" && git push`
4. Monitor build logs in HF Spaces

## ✅ Verification Checklist
- [ ] App builds successfully
- [ ] All dependencies install
- [ ] Interface loads correctly
- [ ] Country selection works
- [ ] Analysis runs without errors
- [ ] Visualizations render properly
EOF

echo "✅ Deployment package created in: $DEPLOY_DIR"
echo ""
echo "📋 Next Steps:"
echo "1. Go to: https://huggingface.co/spaces"
echo "2. Create new Space named 'TIPM' with Gradio SDK"
echo "3. Clone the Space: git clone https://huggingface.co/spaces/YOUR_USERNAME/TIPM"
echo "4. Copy files from $DEPLOY_DIR to the cloned Space"
echo "5. Commit and push: git add . && git commit -m 'Deploy TIPM v1.5' && git push"
echo ""
echo "🎯 TIPM v1.5 is ready for deployment!"
echo "📁 Deployment files are in: $DEPLOY_DIR"
