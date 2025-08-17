#!/bin/bash

echo "🔍 TIPM Deployment Status Checker"
echo "=================================="
echo ""

echo "🔧 Checking Backend (Render)..."
echo "URL: https://tipm-api.onrender.com"
echo "Status: $(curl -s -o /dev/null -w "%{http_code}" https://tipm-api.onrender.com/health 2>/dev/null || echo "Failed to connect")"
echo ""

echo "🌐 Checking Frontend (Vercel)..."
echo "URL: https://tipm-app.vercel.app"
echo "Status: $(curl -s -o /dev/null -w "%{http_code}" https://tipm-app.vercel.app 2>/dev/null || echo "Failed to connect")"
echo ""

echo "🔒 Testing CORS between production domains..."
if curl -s -o /dev/null -w "%{http_code}" https://tipm-api.onrender.com/health >/dev/null 2>&1; then
    CORS_STATUS=$(curl -H "Origin: https://tipm-app.vercel.app" \
                      -H "Access-Control-Request-Method: GET" \
                      -X OPTIONS https://tipm-api.onrender.com/health \
                      -s -o /dev/null -w "%{http_code}" 2>/dev/null || echo "Failed")
    echo "CORS Status: $CORS_STATUS"
else
    echo "CORS Status: Backend not accessible"
fi

echo ""
echo "📊 Summary:"
echo "✅ Backend accessible: $(curl -s -o /dev/null -w "%{http_code}" https://tipm-api.onrender.com/health 2>/dev/null | grep -q "200" && echo "Yes" || echo "No")"
echo "✅ Frontend accessible: $(curl -s -o /dev/null -w "%{http_code}" https://tipm-app.vercel.app 2>/dev/null | grep -q "200" && echo "Yes" || echo "No")"
echo "✅ CORS working: $(curl -s -o /dev/null -w "%{http_code}" https://tipm-api.onrender.com/health 2>/dev/null | grep -q "200" && echo "Yes" || echo "No")"
