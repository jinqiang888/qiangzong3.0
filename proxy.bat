@echo off
setlocal enabledelayedexpansion

set "PROXY_HOST=127.0.0.1"
set "PROXY_PORT=34743"
set "PROXY_URL=http://%PROXY_HOST%:%PROXY_PORT%"

if "%1"=="on" goto :set_proxy
if "%1"=="off" goto :remove_proxy
if "%1"=="status" goto :get_status

:: 默认显示状态
goto :get_status

:set_proxy
:: 设置环境变量
set HTTP_PROXY=%PROXY_URL%
set HTTPS_PROXY=%PROXY_URL%
set ALL_PROXY=%PROXY_URL%
set NO_PROXY=localhost,127.0.0.1,localaddress,.local,.cn,.com.cn

:: 配置git代理
git config --global http.proxy %PROXY_URL%
git config --global https.proxy %PROXY_URL%

:: 配置npm代理
npm config set proxy %PROXY_URL%
npm config set https-proxy %PROXY_URL%

echo ✅ 代理已开启: %PROXY_URL%
echo NO_PROXY: %NO_PROXY%
goto :end

:remove_proxy
:: 清除环境变量
set HTTP_PROXY=
set HTTPS_PROXY=
set ALL_PROXY=
set NO_PROXY=

:: 清除git代理
git config --global --unset http.proxy
git config --global --unset https.proxy

:: 清除npm代理
npm config delete proxy
npm config delete https-proxy

echo ❌ 代理已关闭
goto :end

:get_status
echo.
echo 📊 代理状态检查
echo ------------------------

for /f "tokens=2*" %%a in ('git config --global http.proxy 2^>nul') do set "GIT_PROXY=%%a"
for /f "tokens=2*" %%a in ('npm config get proxy 2^>nul') do set "NPM_PROXY=%%a"

if defined HTTP_PROXY (echo 环境变量 HTTP_PROXY: %HTTP_PROXY%) else echo 环境变量 HTTP_PROXY: 未设置
if defined GIT_PROXY (echo Git 代理: !GIT_PROXY!) else echo Git 代理: 未设置
if defined NPM_PROXY (echo NPM 代理: !NPM_PROXY!) else echo NPM 代理: 未设置
echo ------------------------

if defined HTTP_PROXY if defined GIT_PROXY if defined NPM_PROXY (
    echo ✅ 代理已正常启用
) else (
    echo ❌ 代理未启用
)
echo.
goto :end

:end
endlocal
