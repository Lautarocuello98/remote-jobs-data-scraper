$ErrorActionPreference = "Stop"

Set-Location -Path $PSScriptRoot

function Get-PythonLauncher {
    if (Get-Command python -ErrorAction SilentlyContinue) {
        return @{
            Command = "python"
            Args = @()
        }
    }

    if (Get-Command py -ErrorAction SilentlyContinue) {
        return @{
            Command = "py"
            Args = @("-3")
        }
    }

    throw "Python no esta instalado o no esta en PATH. Instala Python 3.10+ y vuelve a ejecutar."
}

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    $launcher = Get-PythonLauncher
    & $launcher.Command @($launcher.Args + @("-m", "venv", ".venv"))
}

$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r requirements.txt
& $venvPython main.py

Write-Host ""
Write-Host "Listo. Archivos generados:"
Write-Host "- data\raw\jobs_raw.csv"
Write-Host "- data\processed\remote_jobs_clean.csv"
Write-Host "- output\remote_jobs.xlsx"
Write-Host "- output\remote_jobs.json"
