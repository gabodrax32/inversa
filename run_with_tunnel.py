from pyngrok import ngrok, conf
import subprocess
import sys
import time
import os

PY = sys.executable
BASE = os.path.dirname(__file__)
APP = os.path.join(BASE, 'app.py')

if not os.path.exists(APP):
    print('app.py not found at', APP)
    sys.exit(1)

print('Starting Flask app...')
p = subprocess.Popen([PY, APP], cwd=BASE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
time.sleep(1)
print('Opening ngrok tunnel on port 5000...')
# Use the user-provided ngrok binary to avoid antivirus blocking of pyngrok's downloaded binary
user_ngrok_path = r"C:\Users\gabri\ngrok\ngrok.exe"
pyngrok_config = conf.PyngrokConfig(ngrok_path=user_ngrok_path)
tunnel = ngrok.connect(5000, pyngrok_config=pyngrok_config)
print('Public URL:', tunnel.public_url)

try:
    for line in p.stdout:
        print(line, end='')
except KeyboardInterrupt:
    pass
finally:
    ngrok.disconnect(tunnel.public_url)
    p.terminate()
