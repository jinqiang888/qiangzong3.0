$date = Get-Date -Format "yyyy-MM-dd"
$path = "C:\Users\Administrator\.openclaw\workspace\memory\$date.md"
if (Test-Path $path) {
    $content = Get-Content $path -Raw
    if ($content -match "backup.*done") {
        Write-Output "backed_up"
    } else {
        Write-Output "not_backed_up"
    }
} else {
    Write-Output "not_created"
}
