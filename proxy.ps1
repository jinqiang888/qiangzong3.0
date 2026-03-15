<#
.SYNOPSIS
代理开关工具，自动配置/取消命令行代理

.DESCRIPTION
支持开启/关闭/查看代理状态，自动配置git、npm等工具的代理
#>

param(
    [Parameter(Position=0)]
    [ValidateSet("on", "off", "status")]
    [string]$Action = "status"
)

$PROXY_HOST = "127.0.0.1"
$PROXY_PORT = "34743"
$PROXY_URL = "http://${PROXY_HOST}:${PROXY_PORT}"

function Set-Proxy {
    # 设置环境变量
    $env:HTTP_PROXY = $PROXY_URL
    $env:HTTPS_PROXY = $PROXY_URL
    $env:ALL_PROXY = $PROXY_URL
    $env:NO_PROXY = "localhost,127.0.0.1,localaddress,.local,.cn,.com.cn"

    # 配置git代理
    git config --global http.proxy $PROXY_URL
    git config --global https.proxy $PROXY_URL

    # 配置npm代理
    npm config set proxy $PROXY_URL
    npm config set https-proxy $PROXY_URL

    Write-Host "✅ 代理已开启: $PROXY_URL" -ForegroundColor Green
    Write-Host "NO_PROXY: $env:NO_PROXY" -ForegroundColor Gray
}

function Remove-Proxy {
    # 清除环境变量
    Remove-Item Env:\HTTP_PROXY -ErrorAction SilentlyContinue
    Remove-Item Env:\HTTPS_PROXY -ErrorAction SilentlyContinue
    Remove-Item Env:\ALL_PROXY -ErrorAction SilentlyContinue
    Remove-Item Env:\NO_PROXY -ErrorAction SilentlyContinue

    # 清除git代理
    git config --global --unset http.proxy
    git config --global --unset https.proxy

    # 清除npm代理
    npm config delete proxy
    npm config delete https-proxy

    Write-Host "❌ 代理已关闭" -ForegroundColor Yellow
}

function Get-ProxyStatus {
    $httpProxy = $env:HTTP_PROXY
    $gitProxy = git config --global http.proxy
    $npmProxy = npm config get proxy

    Write-Host "`n📊 代理状态检查" -ForegroundColor Cyan
    Write-Host "------------------------"
    if ($httpProxy) { Write-Host "环境变量 HTTP_PROXY: $httpProxy" } else { Write-Host "环境变量 HTTP_PROXY: 未设置" }
    if ($gitProxy) { Write-Host "Git 代理: $gitProxy" } else { Write-Host "Git 代理: 未设置" }
    if ($npmProxy) { Write-Host "NPM 代理: $npmProxy" } else { Write-Host "NPM 代理: 未设置" }
    Write-Host "------------------------"

    if ($httpProxy -and $gitProxy -and $npmProxy) {
        Write-Host "✅ 代理已正常启用" -ForegroundColor Green
    } else {
        Write-Host "❌ 代理未启用" -ForegroundColor Yellow
    }
    Write-Host ""
}

switch ($Action) {
    "on" { Set-Proxy }
    "off" { Remove-Proxy }
    "status" { Get-ProxyStatus }
}
