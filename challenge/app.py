from flask import Flask
import redis
import os 
host_value = os.getenv("REDIS_HOST", "redis")
port_value = int(os.getenv("REDIS_PORT", "6379"))

app = Flask(__name__)
client = redis.Redis(host=host_value, port=port_value, decode_responses=True)

@app.route('/')
def hello():
    return """
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Rachida — London Flask + Redis</title>
        <style>
          * { margin: 0; padding: 0; box-sizing: border-box; }

          body {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            padding: 20px;
            overflow: hidden;
            position: relative;
          }

          /* Stars */
          body::before {
            content: "";
            position: fixed;
            top: 0; left: 0; right: 0; height: 60%;
            background-image:
              radial-gradient(1px 1px at 20px 30px, #fff, transparent),
              radial-gradient(1px 1px at 80px 70px, #fff, transparent),
              radial-gradient(1px 1px at 150px 40px, #fff, transparent),
              radial-gradient(1px 1px at 220px 90px, #fff, transparent),
              radial-gradient(1px 1px at 300px 20px, #fff, transparent),
              radial-gradient(1px 1px at 380px 60px, #fff, transparent),
              radial-gradient(1px 1px at 460px 100px, #fff, transparent),
              radial-gradient(1px 1px at 540px 30px, #fff, transparent);
            opacity: 0.6;
            pointer-events: none;
          }

          /* Skyline */
          .skyline {
            position: fixed;
            bottom: 0; left: 0; right: 0;
            height: 220px;
            pointer-events: none;
            z-index: 1;
          }

          /* Big Ben */
          .bigben {
            position: absolute;
            bottom: 0;
            left: 8%;
            width: 70px;
            height: 180px;
            background: #1a1a2e;
            border-radius: 4px 4px 0 0;
          }
          .bigben::before {
            content: "";
            position: absolute;
            top: 15px; left: 50%;
            transform: translateX(-50%);
            width: 40px; height: 40px;
            border-radius: 50%;
            background: radial-gradient(circle, #fbbf24 0%, #b45309 100%);
            box-shadow: 0 0 30px rgba(251, 191, 36, 0.6);
            animation: glow 3s ease-in-out infinite alternate;
          }
          .bigben::after {
            content: "";
            position: absolute;
            top: -20px; left: 50%;
            transform: translateX(-50%);
            width: 0; height: 0;
            border-left: 35px solid transparent;
            border-right: 35px solid transparent;
            border-bottom: 20px solid #1a1a2e;
          }
          @keyframes glow {
            from { box-shadow: 0 0 20px rgba(251, 191, 36, 0.4); }
            to   { box-shadow: 0 0 40px rgba(251, 191, 36, 0.8); }
          }

          /* Buildings */
          .building {
            position: absolute;
            bottom: 0;
            background: #1a1a2e;
            border-radius: 2px 2px 0 0;
          }
          .b1 { left: 20%;  width: 50px;  height: 90px; }
          .b2 { left: 28%;  width: 40px;  height: 130px; }
          .b3 { left: 36%;  width: 65px;  height: 100px; }
          .b4 { left: 48%;  width: 45px;  height: 150px; }
          .b5 { left: 56%;  width: 80px;  height: 110px; }
          .b6 { left: 68%;  width: 55px;  height: 140px; }
          .b7 { left: 78%;  width: 60px;  height: 95px; }
          .b8 { left: 88%;  width: 45px;  height: 120px; }

          .building::after {
            content: "";
            position: absolute;
            top: 20%; left: 20%; right: 20%; bottom: 20%;
            background-image:
              radial-gradient(2px 2px at 10px 15px, #fbbf24, transparent),
              radial-gradient(2px 2px at 25px 30px, #fbbf24, transparent),
              radial-gradient(2px 2px at 15px 45px, #fbbf24, transparent);
            opacity: 0.7;
          }

          /* Card */
          .card {
            position: relative;
            z-index: 10;
            background: rgba(255, 255, 255, 0.98);
            border-radius: 24px;
            padding: 55px 45px;
            max-width: 520px;
            width: 100%;
            box-shadow: 0 30px 80px rgba(0, 0, 0, 0.5);
            text-align: center;
            animation: fadeIn 0.8s ease-out;
            border-top: 6px solid #dc2626;
          }
          @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to   { opacity: 1; transform: translateY(0); }
          }

          .avatar {
            width: 90px;
            height: 90px;
            border-radius: 50%;
            background: linear-gradient(135deg, #dc2626 0%, #7f1d1d 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 25px;
            color: #ffffff;
            font-size: 36px;
            font-weight: 700;
            box-shadow: 0 8px 20px rgba(220, 38, 38, 0.4);
          }

          h1 {
            color: #1a1a2e;
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 12px;
            letter-spacing: -0.5px;
          }

          p.subtitle {
            color: #6b7280;
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 30px;
          }

          .badge-row {
            display: flex;
            justify-content: center;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 30px;
          }
          .badge {
            background: #f3f4f6;
            color: #4b5563;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 500;
          }
          .badge.highlight {
            background: #dc2626;
            color: #ffffff;
          }

          a.btn {
            display: inline-block;
            background: linear-gradient(135deg, #dc2626 0%, #7f1d1d 100%);
            color: #ffffff;
            text-decoration: none;
            padding: 14px 32px;
            border-radius: 50px;
            font-size: 16px;
            font-weight: 600;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            box-shadow: 0 8px 20px rgba(220, 38, 38, 0.4);
          }
          a.btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 28px rgba(220, 38, 38, 0.55);
          }

          footer {
            margin-top: 28px;
            color: #9ca3af;
            font-size: 12px;
          }
        </style>
      </head>
      <body>

        <div class="skyline">
          <div class="bigben"></div>
          <div class="building b1"></div>
          <div class="building b2"></div>
          <div class="building b3"></div>
          <div class="building b4"></div>
          <div class="building b5"></div>
          <div class="building b6"></div>
          <div class="building b7"></div>
          <div class="building b8"></div>
        </div>

        <div class="card">
          <div class="avatar">R</div>
          <h1>Hello, I'm Rachida</h1>
          <p class="subtitle">
            Welcome to my Flask + Redis application.<br />
            Built with Docker, orchestrated with Compose, served by Nginx.
          </p>
          <div class="badge-row">
            <span class="badge highlight">🇬🇧 London</span>
            <span class="badge">🐳 Docker</span>
            <span class="badge">🐍 Flask</span>
            <span class="badge">⚡ Redis</span>
            <span class="badge">🌐 Nginx</span>
          </div>
          <a href="/count" class="btn">View Visit Count →</a>
          <footer>Rachida · Docker &amp; DevOps Challenge</footer>
        </div>

      </body>
    </html>
    """
@app.route('/count')
def count():
    client.incr('hits')
    counter = client.get('hits')
    return f"""
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Visit Count — London</title>
        <style>
          * {{ margin: 0; padding: 0; box-sizing: border-box; }}

          body {{
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            padding: 20px;
            position: relative;
            overflow: hidden;
          }}

          body::before {{
            content: "";
            position: fixed;
            top: 0; left: 0; right: 0; height: 60%;
            background-image:
              radial-gradient(1px 1px at 40px 30px, #fff, transparent),
              radial-gradient(1px 1px at 120px 80px, #fff, transparent),
              radial-gradient(1px 1px at 200px 40px, #fff, transparent),
              radial-gradient(1px 1px at 280px 100px, #fff, transparent),
              radial-gradient(1px 1px at 360px 50px, #fff, transparent),
              radial-gradient(1px 1px at 440px 90px, #fff, transparent);
            opacity: 0.6;
            pointer-events: none;
          }}

          .skyline {{
            position: fixed;
            bottom: 0; left: 0; right: 0;
            height: 220px;
            pointer-events: none;
            z-index: 1;
          }}

          .bigben {{
            position: absolute;
            bottom: 0;
            left: 10%;
            width: 70px;
            height: 180px;
            background: #1a1a2e;
            border-radius: 4px 4px 0 0;
          }}
          .bigben::before {{
            content: "";
            position: absolute;
            top: 15px; left: 50%;
            transform: translateX(-50%);
            width: 40px; height: 40px;
            border-radius: 50%;
            background: radial-gradient(circle, #fbbf24 0%, #b45309 100%);
            box-shadow: 0 0 30px rgba(251, 191, 36, 0.6);
            animation: glow 3s ease-in-out infinite alternate;
          }}
          .bigben::after {{
            content: "";
            position: absolute;
            top: -20px; left: 50%;
            transform: translateX(-50%);
            width: 0; height: 0;
            border-left: 35px solid transparent;
            border-right: 35px solid transparent;
            border-bottom: 20px solid #1a1a2e;
          }}
          @keyframes glow {{
            from {{ box-shadow: 0 0 20px rgba(251, 191, 36, 0.4); }}
            to   {{ box-shadow: 0 0 40px rgba(251, 191, 36, 0.8); }}
          }}

          .building {{
            position: absolute;
            bottom: 0;
            background: #1a1a2e;
            border-radius: 2px 2px 0 0;
          }}
          .b1 {{ left: 25%;  width: 50px;  height: 90px; }}
          .b2 {{ left: 33%;  width: 40px;  height: 130px; }}
          .b3 {{ left: 41%;  width: 65px;  height: 100px; }}
          .b4 {{ left: 53%;  width: 45px;  height: 150px; }}
          .b5 {{ left: 61%;  width: 80px;  height: 110px; }}
          .b6 {{ left: 73%;  width: 55px;  height: 140px; }}
          .b7 {{ left: 83%;  width: 60px;  height: 95px; }}

          .ticket {{
            position: relative;
            z-index: 10;
            background: #fef3c7;
            border-radius: 20px;
            padding: 50px 45px;
            max-width: 520px;
            width: 100%;
            box-shadow: 0 30px 80px rgba(0, 0, 0, 0.5);
            text-align: center;
            animation: fadeIn 0.6s ease-out;
            border-top: 8px dashed #dc2626;
            border-bottom: 8px dashed #dc2626;
          }}
          @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
          }}

          .stamp {{
            display: inline-block;
            background: #dc2626;
            color: #ffffff;
            padding: 6px 16px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 20px;
          }}

          h1 {{
            color: #1a1a2e;
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
          }}

          p.subtitle {{
            color: #78350f;
            font-size: 14px;
            margin-bottom: 35px;
          }}

          .counter-box {{
            background: #1a1a2e;
            border-radius: 12px;
            padding: 30px 20px;
            margin-bottom: 30px;
            box-shadow: inset 0 4px 12px rgba(0, 0, 0, 0.4);
          }}

          .counter-label {{
            color: #fbbf24;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-bottom: 8px;
          }}

          .counter-value {{
            color: #fef3c7;
            font-size: 64px;
            font-weight: 800;
            font-family: "Courier New", monospace;
            letter-spacing: 4px;
            text-shadow: 0 0 20px rgba(251, 191, 36, 0.6);
          }}

          .actions {{
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
          }}

          a.btn {{
            display: inline-block;
            color: #ffffff;
            text-decoration: none;
            padding: 12px 26px;
            border-radius: 50px;
            font-size: 14px;
            font-weight: 600;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
          }}
          a.btn.primary {{
            background: linear-gradient(135deg, #dc2626 0%, #7f1d1d 100%);
            box-shadow: 0 8px 20px rgba(220, 38, 38, 0.4);
          }}
          a.btn.secondary {{
            background: linear-gradient(135deg, #334155 0%, #1e293b 100%);
            box-shadow: 0 8px 20px rgba(51, 65, 85, 0.4);
          }}
          a.btn:hover {{
            transform: translateY(-2px);
          }}

          footer {{
            margin-top: 24px;
            color: #92400e;
            font-size: 12px;
          }}
        </style>
      </head>
      <body>

        <div class="skyline">
          <div class="bigben"></div>
          <div class="building b1"></div>
          <div class="building b2"></div>
          <div class="building b3"></div>
          <div class="building b4"></div>
          <div class="building b5"></div>
          <div class="building b6"></div>
          <div class="building b7"></div>
        </div>

        <div class="ticket">
          <span class="stamp">London · Visit Pass</span>
          <h1>Visit Count</h1>
          <p class="subtitle">Every refresh adds one to the count.</p>

          <div class="counter-box">
            <div class="counter-label">Total Visits</div>
            <div class="counter-value">{counter}</div>
          </div>

          <div class="actions">
            <a href="/" class="btn secondary">← Home</a>
            <a href="/count" class="btn primary">Refresh Count ↻</a>
          </div>

          <footer>Rachida · Docker &amp; DevOps Challenge · Served by Nginx</footer>
        </div>

      </body>
    </html>
    """
    client.incr('hits')
    counter = client.get('hits')
    return f"This webpage has been viewed {counter} time(s)."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)