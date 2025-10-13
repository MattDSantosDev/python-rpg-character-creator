PowerShell auto-activate and local development notes
===============================================

This project includes a recommended convenience snippet for Windows PowerShell that auto-activates a local `.venv` when you open a shell in the project folder.

Why this helps
--------------
- Makes it easier for contributors to run the app without manually activating the virtual environment every time.

Minimal snippet (paste into your PowerShell profile)
--------------------------------------------------
Add the following lines to your PowerShell profile (open it with `notepad $PROFILE`):

```powershell
# Auto-activate local .venv when starting shell in that folder
$projVenv = Join-Path (Get-Location) '.venv\Scripts\Activate.ps1'
if (Test-Path $projVenv) { & $projVenv }
```

Notes and alternatives
----------------------
- If you prefer activation to follow you when you `cd` into the project tree, consider the "parent-search" snippet or use `direnv` for explicit per-directory environment control. See the project README for more advanced setup.
- If PowerShell prevents scripts from running, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
```

Contributing
------------
If you make changes to the repo or the development environment instructions, please open a pull request describing the change.

Thanks for contributing!
