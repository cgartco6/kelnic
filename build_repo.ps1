# Kelnic Solutions – Repository Builder (Windows PowerShell)
# Run this script to generate the complete repository structure.

Write-Host "🚀 Building Kelnic Solutions repository..." -ForegroundColor Cyan

# Create root directory
New-Item -ItemType Directory -Force -Path Kelnic | Out-Null
Set-Location Kelnic

# Create directory structure
$dirs = @(
    ".github/workflows",
    "evo_core/orchestrator",
    "evo_core/agents",
    "evo_core/memory",
    "evo_core/evolution_engine",
    "evo_core/runtime",
    "evo_core/studio",
    "evo_core/models",
    "tiers/tier1_software_demo/product/templates",
    "tiers/tier1_software_demo/product/assets",
    "tiers/tier1_software_demo/funnel/ads",
    "tiers/tier1_software_demo/metrics",
    "tiers/tier2_industry_explainers",
    "tiers/tier3_ai_tool_breakdown",
    "tiers/tier4_educational_maps",
    "tiers/tier5_business_case_studies",
    "tiers/shared",
    "frontend/app/api",
    "frontend/components",
    "backend/routes",
    "docker",
    "scripts",
    "data/training_data",
    "tests",
    "docs"
)
foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

# Create placeholder files
@(".env.example", "LICENSE", "README.md", "requirements.txt", "pyproject.toml") | ForEach-Object {
    New-Item -ItemType File -Force -Path $_ | Out-Null
}

Write-Host "✅ Repository structure created at .\Kelnic" -ForegroundColor Green
Write-Host "Next: populate the files using the provided code snippets."
