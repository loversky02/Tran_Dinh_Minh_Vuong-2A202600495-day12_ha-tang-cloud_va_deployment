for ($i=1; $i -le 12; $i++) {
    Write-Host ""
    Write-Host "Request $i" -ForegroundColor Cyan
    $response = curl.exe -X POST http://localhost:8001/ask `
        -H "Content-Type: application/json" `
        -H "X-API-Key: demo-key-change-me" `
        --data "@test_request.json" 2>&1
    
    if ($response -match "Rate limit exceeded") {
        Write-Host "RATE LIMITED!" -ForegroundColor Red
    } elseif ($response -match "answer") {
        Write-Host "Success" -ForegroundColor Green
    } else {
        Write-Host "Response: $response"
    }
    Start-Sleep -Milliseconds 100
}
