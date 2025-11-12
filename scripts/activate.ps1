param(
    [switch]$CreateIfMissing
)

# Resolve repo root and venv path (return plain string paths)
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$venvPath = Join-Path $repoRoot '.venv'

if (-not (Test-Path $venvPath)) {
    if ($CreateIfMissing) {
        Write-Host "Virtual environment not found at $venvPath - creating..."
        python -m venv $venvPath
    } else {
        Write-Error 'Virtual environment not found at ' + $venvPath + '. Run: python -m venv .venv or call this script with -CreateIfMissing.'
        exit 1
    }
}

$activateScript = Join-Path $venvPath 'Scripts\Activate.ps1'
if (-not (Test-Path $activateScript)) {
    Write-Error 'Activation script not found at ' + $activateScript + '. Is this a Windows venv?'
    exit 1
}

# Dot-source the venv activation so the caller's session becomes activated.
. $activateScript

Write-Host "Activated virtualenv at: $venvPath"
