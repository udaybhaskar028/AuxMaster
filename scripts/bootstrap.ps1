# scripts/bootstrap.ps1
# Creates a virtual env and installs dependencies on Windows

$ErrorActionPreference = "Stop"

# Pick the best Python launcher available on Windows
$py = "py"
if (-not (Get-Command $py -ErrorAction SilentlyContinue)) {
  $py = "python"
}

Write-Host ">> Using Python launcher:" $py

# Create venv if it doesn't exist
if (-not (Test-Path ".\.venv")) {
  & $py -m venv .venv
  Write-Host ">> Created .venv"
} else {
  Write-Host ">> .venv already exists"
}

# Activate venv
$activate = ".\.venv\Scripts\Activate.ps1"
if (Test-Path $activate) {
  Write-Host ">> Activating venv"
  & $activate
} else {
  throw "Could not find $activate"
}

# Upgrade pip and install deps
python -m pip install --upgrade pip
pip install -r backend\requirements.txt

Write-Host "`n Environment ready."
Write-Host "To activate later in a new shell: .\.venv\Scripts\Activate.ps1"
