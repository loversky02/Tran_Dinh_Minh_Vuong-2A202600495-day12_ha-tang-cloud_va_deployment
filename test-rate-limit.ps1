# Rate Limiting Test Script
# Run: .\test-rate-limit.ps1

$url = "https://wonderful-delight-production-9390.up.railway.app/ask"
$headers = @{
    "Content-Type" = "application/json"
    "X-API-Key" = "demo-key-change-me"
}
$body = '{"question":"test"}'

Write-Host "=== Rate Limiting Test ===" -ForegroundColor Yellow
Write-Host "Sending 12 requests..." -ForegroundColor Yellow
Write-Host ""

for ($i=1; $i -le 12; $i++) {
    Write-Host "Request $i :" -ForegroundColor Cyan -NoNewline
    
    try {
        $response = Invoke-WebRequest -Uri $url `
            -Method POST `
            -Headers $headers `
            -Body $body `
            -UseBasicParsing `
            -ErrorAction Stop
        
        Write-Host " ✓ Status: $($response.StatusCode)" -ForegroundColor Green
        
    } catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        if ($statusCode -eq 429) {
            Write-Host " ✗ Status: 429 - Rate Limit Exceeded!" -ForegroundColor Red
        } else {
            Write-Host " ✗ Status: $statusCode - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    
    Start-Sleep -Milliseconds 100
}

Write-Host ""
Write-Host "=== Test Complete ===" -ForegroundColor Yellow
