# 🚀 Quick Installation Script for Autonomous BI Suite Pro

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Autonomous BI Suite Pro - Installer" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "✓ Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "  Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found! Please install Python 3.8+ first" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✓ Installing required packages..." -ForegroundColor Yellow
Write-Host "  This may take a few minutes..." -ForegroundColor Gray
Write-Host ""

# Install requirements
pip install -r requirements.txt --quiet --upgrade

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ All packages installed successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Installation failed. Please check errors above." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Installation Complete!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Configure Groq API (optional):" -ForegroundColor White
Write-Host "   • Copy .env.example to .env" -ForegroundColor Gray
Write-Host "   • Get API key from: https://console.groq.com" -ForegroundColor Gray
Write-Host "   • Add key to .env file" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Launch the application:" -ForegroundColor White
Write-Host "   streamlit run app.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Or use sample data immediately:" -ForegroundColor White
Write-Host "   • Select 'Use Sample Data' in sidebar" -ForegroundColor Gray
Write-Host "   • Click 'Load Sample Data'" -ForegroundColor Gray
Write-Host ""

Write-Host "📚 Documentation:" -ForegroundColor Yellow
Write-Host "   • README.md - Quick start guide" -ForegroundColor Gray
Write-Host "   • FEATURES_GUIDE.md - Complete feature documentation" -ForegroundColor Gray
Write-Host ""

$launch = Read-Host "Launch the application now? (Y/N)"
if ($launch -eq "Y" -or $launch -eq "y") {
    Write-Host ""
    Write-Host "🚀 Launching Autonomous BI Suite Pro..." -ForegroundColor Green
    Write-Host ""
    streamlit run app.py
} else {
    Write-Host ""
    Write-Host "Run 'streamlit run app.py' when ready!" -ForegroundColor Cyan
    Write-Host ""
}
