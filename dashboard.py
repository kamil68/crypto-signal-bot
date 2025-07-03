#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Persian Dashboard for Crypto Signals
داشبورد فارسی سیگنال های ارز دیجیتال
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import json
from datetime import datetime
from signals import analyze, get_active_signals, get_market_summary
import os

app = FastAPI(title="داشبورد سیگنال ارز دیجیتال")

# Persian months for date formatting
PERSIAN_MONTHS = {
    1: "فروردین", 2: "اردیبهشت", 3: "خرداد", 4: "تیر",
    5: "مرداد", 6: "شهریور", 7: "مهر", 8: "آبان", 
    9: "آذر", 10: "دی", 11: "بهمن", 12: "اسفند"
}

def get_persian_date():
    """Get current date in Persian format"""
    now = datetime.now()
    return f"{now.day} {PERSIAN_MONTHS[now.month]} {now.year}"

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Main dashboard page in Persian"""
    
    # Get latest signals
    try:
        signals = await analyze()
        market_summary = await get_market_summary()
        active_signals = await get_active_signals()
    except Exception as e:
        signals = [("ERROR", f"خطا: {str(e)}")]
        market_summary = {}
        active_signals = []
    
    # Create HTML dashboard
    html_content = f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>داشبورد سیگنال ارز دیجیتال</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
                direction: rtl;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }}
            
            .header {{
                text-align: center;
                color: white;
                margin-bottom: 30px;
            }}
            
            .header h1 {{
                font-size: 2.5rem;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }}
            
            .header p {{
                font-size: 1.1rem;
                opacity: 0.9;
            }}
            
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            
            .stat-card {{
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                padding: 25px;
                text-align: center;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                backdrop-filter: blur(4px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                transition: transform 0.3s ease;
            }}
            
            .stat-card:hover {{
                transform: translateY(-5px);
            }}
            
            .stat-value {{
                font-size: 2rem;
                font-weight: bold;
                color: #667eea;
                margin-bottom: 10px;
            }}
            
            .stat-label {{
                color: #666;
                font-size: 1rem;
            }}
            
            .signals-section {{
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                backdrop-filter: blur(4px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                margin-bottom: 30px;
            }}
            
            .section-title {{
                font-size: 1.8rem;
                color: #333;
                margin-bottom: 25px;
                text-align: center;
                position: relative;
            }}
            
            .section-title:after {{
                content: '';
                position: absolute;
                bottom: -10px;
                left: 50%;
                transform: translateX(-50%);
                width: 50px;
                height: 3px;
                background: linear-gradient(90deg, #667eea, #764ba2);
                border-radius: 2px;
            }}
            
            .signal-item {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 20px;
                margin: 10px 0;
                background: #f8f9fa;
                border-radius: 10px;
                border-left: 4px solid #667eea;
                transition: all 0.3s ease;
            }}
            
            .signal-item:hover {{
                background: #e9ecef;
                transform: translateX(-5px);
            }}
            
            .signal-symbol {{
                font-weight: bold;
                font-size: 1.1rem;
                color: #333;
            }}
            
            .signal-info {{
                font-size: 0.95rem;
                color: #666;
            }}
            
            .refresh-btn {{
                position: fixed;
                bottom: 30px;
                left: 30px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border: none;
                border-radius: 50px;
                padding: 15px 25px;
                font-size: 1rem;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
            }}
            
            .refresh-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            }}
            
            .status-indicator {{
                display: inline-block;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                margin-left: 10px;
            }}
            
            .status-active {{ background: #28a745; }}
            .status-waiting {{ background: #ffc107; }}
            .status-stopped {{ background: #dc3545; }}
            
            .no-signals {{
                text-align: center;
                color: #666;
                font-style: italic;
                padding: 40px;
            }}
            
            .emoji {{
                font-size: 1.5rem;
                margin-left: 10px;
            }}
            
            @media (max-width: 768px) {{
                .container {{
                    padding: 10px;
                }}
                
                .header h1 {{
                    font-size: 2rem;
                }}
                
                .stats-grid {{
                    grid-template-columns: 1fr;
                }}
                
                .signal-item {{
                    flex-direction: column;
                    text-align: center;
                }}
            }}
        </style>
        <script>
            // Auto refresh every 5 minutes
            setTimeout(() => {{
                location.reload();
            }}, 300000);
            
            function refreshPage() {{
                location.reload();
            }}
        </script>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 داشبورد سیگنال ارز دیجیتال</h1>
                <p>تحلیل هوشمند و به‌روز بازار کریپتو • {get_persian_date()}</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{market_summary.get('fear_greed_index', 'N/A')}</div>
                    <div class="stat-label">🧠 شاخص ترس و طمع</div>
                    <div style="margin-top: 10px; color: #667eea;">{market_summary.get('mood_persian', 'نامشخص')}</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-value" style="color: #28a745;">{market_summary.get('bullish_signals', 0)}</div>
                    <div class="stat-label">🟢 سیگنال های خرید</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-value" style="color: #dc3545;">{market_summary.get('bearish_signals', 0)}</div>
                    <div class="stat-label">🔴 سیگنال های فروش</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-value">{len(active_signals)}</div>
                    <div class="stat-label">📊 سیگنال های فعال</div>
                </div>
            </div>
            
            <div class="signals-section">
                <h2 class="section-title">🔥 آخرین سیگنال ها</h2>
                {generate_signals_html(signals)}
            </div>
            
            {generate_active_signals_html(active_signals) if active_signals else ''}
        </div>
        
        <button class="refresh-btn" onclick="refreshPage()">
            🔄 به‌روزرسانی
        </button>
    </body>
    </html>
    """
    
    return html_content

def generate_signals_html(signals):
    """Generate HTML for signals display"""
    if not signals:
        return '<div class="no-signals">🔍 در حال جستجوی سیگنال های جدید...</div>'
    
    html = ""
    for symbol, signal_text in signals:
        if symbol == "ERROR":
            html += f'<div class="signal-item" style="border-left-color: #dc3545;"><span class="signal-symbol">❌ خطا</span><span class="signal-info">{signal_text}</span></div>'
        elif symbol == "STATUS":
            html += f'<div class="signal-item" style="border-left-color: #ffc107;"><span class="signal-symbol">📊 وضعیت</span><span class="signal-info">{signal_text}</span></div>'
        elif symbol == "MARKET":
            html += f'<div class="signal-item" style="border-left-color: #17a2b8;"><span class="signal-symbol">🌍 بازار</span><span class="signal-info">{signal_text}</span></div>'
        else:
            # Determine signal color based on type
            color = "#28a745" if "خرید" in signal_text else "#dc3545" if "فروش" in signal_text else "#667eea"
            html += f'<div class="signal-item" style="border-left-color: {color};"><span class="signal-symbol">{symbol}</span><span class="signal-info">{signal_text}</span></div>'
    
    return html

def generate_active_signals_html(active_signals):
    """Generate HTML for active signals"""
    if not active_signals:
        return ""
    
    html = '''
    <div class="signals-section">
        <h2 class="section-title">⚡ سیگنال های فعال</h2>
    '''
    
    for signal in active_signals:
        status = signal.get('current_status', {})
        status_text = status.get('status', 'نامشخص')
        pnl = status.get('pnl_percent', 0)
        
        # Status indicator
        status_class = "status-active" if "PROFIT" in status_text else "status-waiting" if "WAITING" in status_text else "status-stopped"
        
        # Persian status translation
        persian_status = {
            'IN_PROFIT': 'در سود',
            'WAITING_ENTRY': 'انتظار ورود',
            'STOPPED_OUT': 'استاپ خورده',
            'TP1_HIT': 'هدف ۱ رسید',
            'TP2_HIT': 'هدف ۲ رسید',
            'TP3_HIT': 'هدف ۳ رسید'
        }.get(status_text, status_text)
        
        pnl_color = "#28a745" if pnl > 0 else "#dc3545" if pnl < 0 else "#666"
        
        html += f'''
        <div class="signal-item">
            <span class="signal-symbol">
                <span class="status-indicator {status_class}"></span>
                {signal.get('symbol', 'N/A')}
            </span>
            <span class="signal-info">
                {persian_status} | 
                <span style="color: {pnl_color};">
                    {pnl:+.1f}%
                </span>
            </span>
        </div>
        '''
    
    html += '</div>'
    return html

@app.get("/api/signals")
async def api_signals():
    """API endpoint for signals"""
    try:
        signals = await analyze()
        return {"signals": signals, "timestamp": datetime.now().isoformat()}
    except Exception as e:
        return {"error": str(e), "timestamp": datetime.now().isoformat()}

@app.get("/api/market")
async def api_market():
    """API endpoint for market summary"""
    try:
        summary = await get_market_summary()
        return summary
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/active")
async def api_active():
    """API endpoint for active signals"""
    try:
        active = await get_active_signals()
        return {"active_signals": active, "count": len(active)}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("🚀 راه‌اندازی داشبورد فارسی...")
    print("🌐 دسترسی در: http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)