# start_backend_tunnel.ps1
# Automates starting localtunnel and updating the mobile app configuration

$port = 8000
$subdomain = "young-bobcats-begin"
$mobileConfigPath = "..\..\..\appdev mob\config.json"
$backendLogPath = "tunnel_url.txt"

Write-Host "Starting tunnel on port $port with subdomain $subdomain..." -ForegroundColor Cyan

# Start localtunnel in the background and capture output
$process = Start-Process npx -ArgumentList "localtunnel --port $port --subdomain $subdomain" -NoNewWindow -PassThru -RedirectStandardOutput $backendLogPath

# Wait a few seconds for the tunnel to initialize
Start-Sleep -Seconds 5

# Read the URL from the log file
if (Test-Path $backendLogPath) {
    $content = Get-Content $backendLogPath
    $urlMatch = $content | Select-String -Pattern "https://[a-zA-Z0-9.-]+"
    
    if ($urlMatch) {
        $url = $urlMatch.Matches[0].Value
        Write-Host "Tunnel established at: $url" -ForegroundColor Green
        
        # Update mobile config.json
        if (Test-Path $mobileConfigPath) {
            $config = @{ apiUrl = $url }
            $config | ConvertTo-Json | Set-Content $mobileConfigPath
            Write-Host "Updated mobile config.json successfully." -ForegroundColor Green
        } else {
            Write-Host "Warning: Could not find mobile config at $mobileConfigPath" -ForegroundColor Yellow
        }
        
        # Keep URL in tunnel_url.txt for reference
        "your url is: $url" | Set-Content $backendLogPath
    } else {
        Write-Host "Error: Could not retrieve URL from tunnel output. Check $backendLogPath" -ForegroundColor Red
    }
} else {
    Write-Host "Error: Tunnel log file was not created." -ForegroundColor Red
}

Write-Host "Tunnel is running. Keep this window open or monitor $backendLogPath" -ForegroundColor Cyan
