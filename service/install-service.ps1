# Compile listenerWrapper.py to .exe and Install as Windows Service

try {
    # Look for pyinstaller
    $dir = Get-ChildItem -Path "$Env:LocalAppData\Packages" -Filter "pyinstaller.exe" -Name -Recurse -ErrorAction Stop

    # Ensure pyinstaller Found and $dir Not Empty
    if ($null -eq $dir) {
        throw "Pyinstaller Not Found"
    }

    # Handle Full Path
    $PYINSTALLER_PATH = Join-Path -Path "$Env:LocalAppData\Packages" -ChildPath $dir
    Write-Output "Found pyinstaller at:" $PYINSTALLER_PATH
}
catch {
    # Handle Error
    Write-Output "Error Occured"
    Write-Output $_
    exit
}

# Run pyinstaller to Compile
& $PYINSTALLER_PATH --runtime-tmpdir=. --onefile --hidden-import win32timezone ./listenerWrapper.py

# Check if PyInstaller generated the executable successfully
try {
    if (Test-Path -Path "dist\listenerWrapper.exe") {
        Write-Output "Your script has been successfully packaged as an executable."
    } else {
        throw "pyinstaller Failed to Create The Executable"
    }
}
catch {
    Write-Output "Error Occured"
    Write-Output $_
    exit
}

# Install or Update The Service
& ./dist/listenerWrapper.exe install

