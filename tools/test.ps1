$ProcessName = "C:\Program Files (x86)\OpenPype\3.18.6\openpype_console.exe"
$tools = "C:\Users\will_sunandmoonstudi\LatestOpenpypeBuild\OpenPype\tools"
$localCache = Join-Path $env:LOCALAPPDATA "pypeclub\openpype\3.18\"

if (Get-Process -Name "openpype_console" -ErrorAction SilentlyContinue) {
    Stop-Process -Name "openpype_console" -Force -ErrorAction Stop
    Write-Host "Console Process stopped"
} else {
    Write-Host "Console Process not running"
}

if (Get-Process -Name "openpype_gui" -ErrorAction SilentlyContinue) {
    Stop-Process -Name "openpype_gui" -Force -ErrorAction Stop
    Write-Host "GUI Process stopped"
} else {
    Write-Host "GUI Process not running"
}

foreach ($item in Get-ChildItem -Path $localCache) {
    Remove-Item -Path $item.FullName -Recurse -Force
}

& "$tools\create_zip.ps1"



 
Start-Process $ProcessName 
