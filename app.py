
import os
from flask import Flask, render_template_string, request, send_file
import yt_dlp

app = Flask(__name__)

# --- Updated Premium White/Black Minimalist UI with Animations ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Private Downloader 🚀</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }
        
        body { 
            background: radial-gradient(circle, #f5f5f7 0%, #e5e5ea 100%);
            color: #1d1d1f; 
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
            overflow: hidden;
        }

        /* Entrance Animation for Container */
        .container { 
            width: 100%;
            max-width: 440px; 
            background: rgba(255, 255, 255, 0.8); 
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            padding: 40px 30px; 
            border-radius: 24px; 
            border: 1px solid rgba(255, 255, 255, 0.5);
            box-shadow: 0px 20px 40px rgba(0, 0, 0, 0.06); 
            text-align: center;
            transform: translateY(30px);
            opacity: 0;
            animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        h2 { 
            font-size: 28px;
            font-weight: 700;
            color: #000000; 
            margin-bottom: 8px; 
            letter-spacing: -0.5px;
        }

        p {
            font-size: 14px;
            color: #86868b;
            margin-bottom: 30px;
        }

        /* Stylish Input Field */
        .input-group {
            position: relative;
            margin-bottom: 20px;
        }

        input[type="text"] { 
            width: 100%; 
            padding: 16px 18px; 
            border-radius: 12px; 
            border: 1px solid #d2d2d7; 
            background-color: #ffffff;
            color: #1d1d1f;
            font-size: 15px;
            outline: none;
            transition: all 0.3s ease;
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.02);
        }

        input[type="text"]:focus {
            border-color: #000000;
            box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.07);
        }

        /* Stylish Dropdown */
        select { 
            width: 100%; 
            padding: 16px 18px; 
            margin-bottom: 25px; 
            border-radius: 12px; 
            background-color: #ffffff;
            color: #1d1d1f;
            font-size: 15px;
            border: 1px solid #d2d2d7;
            outline: none;
            cursor: pointer;
            transition: all 0.3s ease;
            appearance: none;
            -webkit-appearance: none;
            background-image: url("data:image/svg+xml;utf8,<svg fill='black' height='24' viewBox='0 0 24 24' width='24' xmlns='http://www.w3.org/2000/svg'><path d='M7 10l5 5 5-5z'/><path d='M0 0h24v24H0z' fill='none'/></svg>");
            background-repeat: no-repeat;
            background-position: right 15px center;
        }

        select:focus {
            border-color: #000000;
            box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.07);
        }

        /* Premium Black Button with Hover Scale & Glow */
        button { 
            background-color: #000000; 
            color: #ffffff; 
            border: none; 
            padding: 16px; 
            font-size: 16px; 
            font-weight: 600;
            border-radius: 12px; 
            cursor: pointer; 
            width: 100%; 
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        button:hover { 
            background-color: #1d1d1f;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        }

        button:active {
            transform: translateY(0);
        }

        /* Loading Animation State */
        .loading-text {
            display: none;
            font-size: 14px;
            color: #000000;
            margin-top: 15px;
            font-weight: 500;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .spinner {
            width: 18px;
            height: 18px;
            border: 2px solid #e5e5ea;
            border-top: 2px solid #000000;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            display: inline-block;
        }

        .footer { 
            margin-top: 35px; 
            font-size: 11px; 
            color: #86868b; 
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }

        /* Animations Definition */
        @keyframes fadeInUp {
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>🚀 Private Downloader</h2>
        <p>Enter a YouTube link to download instantly</p>
        
        <form action="/download" method="post" onsubmit="showLoading()">
            <div class="input-group">
                <input type="text" name="url" placeholder="Paste link here..." required>
            </div>
            
            <select name="quality">
                <option value="bestvideo[height<=2160]+bestaudio/best[height<=2160]">4K Ultra HD</option>
                <option value="bestvideo[height<=1440]+bestaudio/best[height<=1440]">2K Quad HD</option>
                <option value="bestvideo[height<=1080]+bestaudio/best[height<=1080]">1080p Full HD</option>
                <option value="bestvideo[height<=720]+bestaudio/best[height<=720]">720p HD</option>
                <option value="bestvideo[height<=480]+bestaudio/best[height<=480]">480p SD</option>
                <option value="best">Best Available</option>
                <option value="bestaudio/best">Audio Only (MP3)</option>
            </select>
            
            <button type="submit" id="dl-btn">Download Now</button>
            
            <div class="loading-text" id="loader">
                <div class="spinner"></div>
                Processing your video... Please wait
            </div>
        </form>
        
        <div class="footer">Exclusively for friends • Powered by yt-dlp</div>
    </div>

    <script>
        function showLoading() {
            // Button disable karna aur loading spinner dikhana submit hone par
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
        
        # 🍪 Cookies file ka path link karna
        'cookiefile': 'cookies.txt', 
        
        # Extra safety bypass options
        'extractor_args': {
            'youtube': {
                'player_client': ['web_safari', 'android']
            }
        },
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'no_warnings': True,
        'quiet': True
        }
        

    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            
        return send_file(filename, as_attachment=True)
        
    except Exception as e:
        return f"""
        <body style="font-family:sans-serif; background:#f5f5f7; display:flex; justify-content:center; align-items:center; height:100vh; margin:0; text-align:center;">
            <div style="background:#fff; padding:40px; border-radius:20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); max-width:400px;">
                <h2 style="color:#ff3b30; margin-bottom:15px;">❌ Something went wrong!</h2>
                <p style="color:#86868b; font-size:14px; margin-bottom:25px;">{str(e)}</p>
                <a href='/' style="background:#000; color:#fff; text-decoration:none; padding:12px 24px; border-radius:10px; font-weight:600; display:inline-block;">Go Back</a>
            </div>
        </body>
        """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
