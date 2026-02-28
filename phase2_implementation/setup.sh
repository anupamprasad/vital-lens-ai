#!/bin/bash

# Phase 2 Setup Script - Vital Lens AI
# Automatically sets up development environment for Phase 2

echo "🚀 Vital Lens AI - Phase 2 Setup"
echo "=================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.9"

if [[ $(echo -e "${python_version}\n${required_version}" | sort -V | head -n1) == "${required_version}" ]]; then
    echo "✅ Python $python_version (required: 3.9+)"
else
    echo "❌ Python 3.9+ required (found: $python_version)"
    exit 1
fi

echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "⚠️  Virtual environment already exists"
fi

echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

echo ""

# Upgrade pip
echo "📥 Upgrading pip..."
pip install --upgrade pip
echo "✅ pip upgraded"

echo ""

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""

# Create project directories
echo "📁 Creating project directories..."
mkdir -p config
mkdir -p src/{preprocessing,algorithms,signal_processing,models}
mkdir -p datasets
mkdir -p notebooks
mkdir -p tests
mkdir -p results/{benchmarks,bias_analysis}
mkdir -p scripts
mkdir -p data/{raw,processed}
mkdir -p models/{checkpoints,exports}
echo "✅ Directories created"

echo ""

# Initialize DVC
echo "🗂️  Initializing DVC..."
if ! command -v dvc &> /dev/null; then
    echo "⚠️  DVC not installed. Install with: pip install dvc"
else
    dvc init --no-scm 2>/dev/null || echo "⚠️  DVC already initialized"
    echo "✅ DVC initialized"
fi

echo ""

# Create __init__.py files
echo "🐍 Creating Python package structure..."
touch src/__init__.py
touch src/preprocessing/__init__.py
touch src/algorithms/__init__.py
touch src/signal_processing/__init__.py
touch src/models/__init__.py
touch tests/__init__.py
echo "✅ Python package structure created"

echo ""

# Display next steps
echo "=================================="
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Activate environment: source venv/bin/activate"
echo "2. Download datasets: python scripts/download_datasets.py"
echo "3. Start development: jupyter lab notebooks/"
echo ""
echo "📚 Documentation:"
echo "- Phase 2 Plan: PHASE_2_PLAN.md"
echo "- README: README.md"
echo ""
echo "🚀 Happy coding!"
