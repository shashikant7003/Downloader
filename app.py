import os
from flask import Flask, render_template_string, request, send_file
import yt_dlp

app = Flask(__name__)

# --- Updated HTML/UI (Saare Quality Options ke saath) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Private Downloader 🚀</title>
    <style>
        body { 
            font-family: 'Segoe UI', Arial, sans-serif; 
            background-color: #121212; 
            color: #ffffff; 
            text-align: center; 
            padding: 50px 20px; 
        }
        .container { 
            max-width: 450px; 
            margin: auto; 
            background: #1e1e1e; 
            padding: 40px 30px; 
            border-radius: 15px; 
            box-shadow: 0px 10px 25px rgba(0,0,0,0.5); 
        }
        h2 { color: #ff0055; margin-bottom: 20px; }
        input[type="text"] { 
            width: 100%; 
            padding: 12px; 
            margin: 15px 0; 
            border-radius: 8px; 
            border: 1px solid #333; 
            background-color: #2a2a2a;
            color: white;
            box-sizing: border-box;
        }
        select { 
            width: 100%; 
            padding: 12px; 
            margin: 15px 0; 
            border-radius: 8px; 
            background-color: #2a2a2a;
            color: white;
            border: 1px solid #333;
        }
        button { 
            background-color: #ff0055; 
            color: white; 
            border: none; 
            padding: 14px; 
            font-size: 16px; 
            border-radius: 8px; 
            cursor: pointer; 
            width: 100%; 
            font-weight: bold;
        }
        button:hover { background-color: #e0004c; }
        .footer { margin-top: 30px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🚀 Private Video Downloader</h2>
        <p>Link paste karo aur quality select karo!</p>
        <form action="/download" method="post">
            <input type="text" name="url" placeholder="YouTube Link Paste Karein..." required>
            
            <select name="quality">
                <option value="bestvideo[height<=2160]+bestaudio/best[height<=2160]">4K (Ultra HD)</option>
                <option value="bestvideo[height<=1440]+bestaudio/best[height<=1440]">2K (Quad HD)</option>
                <option value="bestvideo[height<=1080]+bestaudio/best[height<=1080]">1080p (Full HD)</option>
                <option value="bestvideo[height<=720]+bestaudio/best[height<=720]">720p (HD)</option>
                <option value="bestvideo[height<=480]+bestaudio/best[height<=480]">480p</option>
                <option value="best">Best Available (Auto)</option>
                <option value="bestaudio/best">Sirf Audio (MP3)</option>
            </select>
            
            <button type="submit">Download Shuru Karein</button>
        </form>
        <div class="footer">Doston ke liye khas banaya gaya 😎</div>
    </div>
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
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            
        return send_file(filename, as_attachment=True)
        
    except Exception as e:
        return f"<h3>❌ Kuch galti hui! Error: {str(e)}</h3><a href='/'>Wapas Jao</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
