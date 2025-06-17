from flask import Flask, request, render_template
import pycurl
from io import BytesIO
import traceback

app = Flask(__name__)

def fetch_with_pycurl(url):
    """使用 pycurl 发起请求，支持 gopher 协议"""
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.TIMEOUT, 5)
    c.perform()
    c.close()
    # pycurl 获取的内容是 bytes 类型，需要解码
    return buffer.getvalue().decode('utf-8', 'ignore')

@app.route('/', methods=['GET', 'POST'])
def index():
    content = None
    error = None
    url = request.form.get('url', '')

    if request.method == 'POST':
        if not url:
            error = "URL cannot be empty!"
        else:
            try:
                # 使用我们新的 pycurl 函数替换原来的 requests.get()
                content = fetch_with_pycurl(url)
            except Exception as e:
                error = f"An error occurred: \n{traceback.format_exc()}"

    return render_template('index.html', url=url, content=content, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
