# Python RPG Character Creator

[![CI](https://github.com/MattDSantosDev/python-rpg-character-creator/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/MattDSantosDev/python-rpg-character-creator/actions/workflows/test.yml)

This project is a Python-based application for creating RPG characters. It allows users to customize attributes, abilities, and more.

## Frontend
The frontend of this application will be built using Streamlit, providing an interactive and user-friendly interface.

## Background
The frontend will feature a background inspired by the attached image, creating a medieval-themed aesthetic for the RPG character creator.

## Assets

This project includes various assets to support RPG character creation:

### Images
| File | Description |
|------|-------------|
| `brick_wall.jpg` | Medieval-themed background image for the interface |

### D&D 5e Reference Materials
| File | Description |
|------|-------------|
| `D&D Character Sheet.pdf` | Official D&D 5e character sheet template |
| `D&D-Barbaro.pdf` | Barbarian class reference (Portuguese) |
| `D&D-Bardo.pdf` | Bard class reference (Portuguese) |
| `D&D-Bruxo.pdf` | Warlock class reference (Portuguese) |
| `D&D-Clerigo.pdf` | Cleric class reference (Portuguese) |
| `D&D-Druida.pdf` | Druid class reference (Portuguese) |
| `D&D-Equipamentos.pdf` | Equipment reference (Portuguese) |
| `D&D-Feiticeiro.pdf` | Sorcerer class reference (Portuguese) |
| `D&D-Feitiços.pdf` | Spells reference (Portuguese) |
| `D&D-Guardiao.pdf` | Guardian/Ranger class reference (Portuguese) |
| `D&D-Guerreiro.pdf` | Fighter class reference (Portuguese) |
| `D&D-Ladino.pdf` | Rogue class reference (Portuguese) |
| `D&D-Mago.pdf` | Wizard class reference (Portuguese) |
| `D&D-Monge.pdf` | Monk class reference (Portuguese) |
| `D&D-Origens.pdf` | Backgrounds reference (Portuguese) |
| `D&D-Paladino.pdf` | Paladin class reference (Portuguese) |
| `D&D-Raças.pdf` | Races reference (Portuguese) |
| `D&D-Talentos.pdf` | Feats reference (Portuguese) |

### Ordem Paranormal (OP) Reference Materials
| File | Description |
|------|-------------|
| `OP Criação Personagem.pdf` | Character creation guide for Ordem Paranormal |
| `OP Equipamentos.pdf` | Equipment reference for Ordem Paranormal |
| `OP Ficha.pdf` | Character sheet for Ordem Paranormal |
| `OP Poderes e Rituais.pdf` | Powers and rituals reference for Ordem Paranormal |
| `OP Sobrevivendo ao Horror.pdf` | Surviving horror guide for Ordem Paranormal |

## Run & Test (Windows PowerShell)

Install dependencies into the repository virtualenv (or your preferred environment):

```powershell
# from project root
.
# create venv if needed
python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run the Streamlit UI:

```powershell
& .\.venv\Scripts\python.exe -m streamlit run main.py
```

Run the parser test script (fast reproduction of table extraction):

```powershell
& .\.venv\Scripts\python.exe .\scripts\test_extract.py
```

Tesseract (OCR) dependency
- The project uses `pytesseract` for OCR fallbacks. `pytesseract` is a Python wrapper and requires the Tesseract system binary (`tesseract`) to be installed and on PATH.
- On Windows you can install it from: https://github.com/UB-Mannheim/tesseract/wiki or via Chocolatey: `choco install tesseract`
- On Ubuntu: `sudo apt-get install tesseract-ocr`

CI note
- The included GitHub Actions workflow will attempt to install `tesseract-ocr` on the Ubuntu runner. On Windows the workflow will try to use Chocolatey but will still run even if system Tesseract is not available — OCR tests are skipped when the `SKIP_OCR` environment variable is set.

## VS Code: auto-activate project virtualenv in integrated terminal

This workspace includes a VS Code settings file that attempts to automatically activate the project's virtual environment when you open a new integrated terminal.

- To use it: open this project in VS Code and select **Terminal → New Terminal**. The new PowerShell terminal should run `.\.venv\Scripts\Activate.ps1` and show the `(.venv)` prompt.
- If you use PowerShell Core (`pwsh`) instead of Windows PowerShell, update the workspace profile in `.vscode/settings.json` to point to the `pwsh` executable (for example `C:\\Program Files\\PowerShell\\7\\pwsh.exe`).
- To revert this behavior, remove or edit `.vscode/settings.json` in the project root.

If the terminal doesn't activate the venv automatically, you can activate it manually:

```powershell
# from project root
& .\.venv\Scripts\Activate.ps1
```
