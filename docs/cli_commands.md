# KiBot Command-Line Reference

## PowerShell Commands
Use these formats when running in Windows PowerShell:

```powershell
# Check KiBot version
& "C:\Program Files\KiCad\9.0\bin\python.exe" "-m" "kibot" "--version"

# Quick start - scans current directory for KiCad projects
& "C:\Program Files\KiCad\9.0\bin\python.exe" "-m" "kibot" "--quick-start"

# Run with specific board and config
& "C:\Program Files\KiCad\9.0\bin\python.exe" "-m" "kibot" "-b" "your_board.kicad_pcb" "-c" "your_config.kibot.yaml"
```

## Bash/Linux Commands
Use these formats when running in Bash or Linux terminal:

```bash
# Check KiBot version
kibot --version

# Quick start - scans current directory for KiCad projects
kibot --quick-start

# Run with specific board and config
kibot -b your_board.kicad_pcb -c your_config.kibot.yaml
```

Note: Always run these commands from your KiCad project directory.