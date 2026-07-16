

import os
from flask import Flask, render_template_string, request, send_file
import yt_dlp

app = Flask(__name__)

# --- Premium White/Black Minimalist UI ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Private Downloader 🚀</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        body { background: radial-gradient(circle, #f5f5f7 0%, #e5e5ea 100%); color: #1d1d1f; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
        .container { width: 100%; max-width: 440px; background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); padding: 40px 30px; border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.5); box-shadow: 0px 20px 40px rgba(0, 0, 0, 0.06); text-align: center; }
        h2 { font-size: 28px; font-weight: 700; color: #000000; margin-bottom: 8px; }
        p { font-size: 14px; color: #86868b; margin-bottom: 30px; }
        input[type="text"] { width: 100%; padding: 16px 18px; border-radius: 12px; border: 1px solid #d2d2d7; background-color: #ffffff; color: #1d1d1f; font-size: 15px; outline: none; margin-bottom: 20px; }
        input[type="text"]:focus { border-color: #000000; box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.07); }
        select { width: 100%; padding: 16px 18px; margin-bottom: 25px; border-radius: 12px; background-color: #ffffff; color: #1d1d1f; font-size: 15px; border: 1px solid #d2d2d7; outline: none; cursor: pointer; }
        button { background-color: #000000; color: #ffffff; border: none; padding: 16px; font-size: 16px; font-weight: 600; border-radius: 12px; cursor: pointer; width: 100%; transition: all 0.3s ease; }
        button:hover { background-color: #1d1d1f; transform: translateY(-2px); }
        .loading-text { display: none; font-size: 14px; color: #000000; margin-top: 15px; font-weight: 500; align-items: center; justify-content: center; gap: 8px; }
        .spinner { width: 18px; height: 18px; border: 2px solid #e5e5ea; border-top: 2px solid #000000; border-radius: 50%; animation: spin 0.8s linear infinite; display: inline-block; }
        .footer { margin-top: 35px; font-size: 11px; color: #86868b; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="container">
        <h2>🚀 Private Downloader</h2>
        <p>Enter a YouTube link to download instantly</p>
        <form action="/download" method="post" onsubmit="showLoading()">
            <input type="text" name="url" placeholder="Paste link here..." required>
            <select name="quality">
                <option value="bestvideo[height<=2160]+bestaudio/best[height<=2160]">4K Ultra HD</option>
                <option value="bestvideo[height<=1440]+bestaudio/best[height<=1440]">2K Quad HD</option>
                <option value="bestvideo[height<=1080]+bestaudio/best[height<=1080]">1080p Full HD</option>
                <option value="bestvideo[height<=720]+bestaudio/best[height<=720]">720p HD</option>
                <option value="best">Best Available</option>
                <option value="bestaudio/best">Audio Only (MP3)</option>
            </select>
            <button type="submit" id="dl-btn">Download Now</button>
            <div class="loading-text" id="loader"><div class="spinner"></div> Processing your video... Please wait</div>
        </form>
        <div class="footer">Exclusively for friends • Powered by yt-dlp</div>
    </div>
    <script>
        function showLoading() {
            document.getElementById('dl-btn').style.opacity = '0.5';
            document.getElementById('dl-btn').innerText = 'Starting...';
            document.getElementById('loader').style.display = 'flex';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('url')
    quality = request.form.get('quality')
    
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
        
    ydl_opts = {
        'format': quality,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'merge_output_format': 'mp4' if quality != 'bestaudio/best' else None,
        
        # Safe options bina crash ke chalne ke liye
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'no_warnings': True,
        'quiet': True
    }

    # Agar folder mein cookies.txt file maujood hai toh automatically use karo
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'
        
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            
        return send_file(filename, as_attachment=True)
        
    except Exception as e:
        error_msg = str(e).replace('<', '&lt;').replace('>', '&gt;')
        return f"<body style='font-family:sans-serif; background:#f5f5f7; display:flex; justify-content:center; align-items:center; height:100vh;'><div style='background:#fff; padding:40px; border-radius:20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); text-align:center; max-width:500px;'><h2>❌ Error Details</h2><p style='color:red; font-family:monospace;'>{error_msg}</p><br><a href='/'>Go Back</a></div></body>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
