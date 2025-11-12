param(
    [switch]$RunStreamlit,
    [string]$Script = 'main.py'
)

# Start a new PowerShell window rooted at the project and activate the project's .venv
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPath = Join-Path $repoRoot '.venv'
$activateScript = Join-Path $venvPath 'Scripts\Activate.ps1'

if (-not (Test-Path $venvPath)) {
    Write-Host ".venv not found. Creating virtualenv at $venvPath..."
    python -m venv $venvPath
}

if (-not (Test-Path $activateScript)) {
    Write-Error "Activation script not found at $activateScript. Aborting."
    exit 1
}

# Build command to run in the new PowerShell window. Use -NoExit so user keeps the shell.
if ($RunStreamlit) {
    $cmd = ". '$activateScript'; python -m pip install --upgrade pip; python -m streamlit run '$repoRoot\$Script'"
} else {
    $cmd = ". '$activateScript'; Write-Host 'Virtualenv activated in new PowerShell. You can run commands here.'"
}

# Launch new PowerShell with the command
Start-Process -FilePath 'powershell.exe' -ArgumentList '-NoExit', '-ExecutionPolicy','Bypass','-Command', $cmd
