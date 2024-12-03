$tesseractPath = "C:\Program Files\Tesseract-OCR"

# Check if Tesseract directory exists
if (Test-Path $tesseractPath) {
    # Get the current PATH
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    
    # Check if Tesseract is already in PATH
    if ($currentPath -notlike "*$tesseractPath*") {
        # Add Tesseract to PATH
        $newPath = $currentPath + ";" + $tesseractPath
        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
        Write-Host "Successfully added Tesseract-OCR to PATH"
    } else {
        Write-Host "Tesseract-OCR is already in PATH"
    }
} else {
    Write-Host "Error: Tesseract-OCR directory not found at $tesseractPath"
    Write-Host "Please make sure Tesseract is installed in the correct location"
}
