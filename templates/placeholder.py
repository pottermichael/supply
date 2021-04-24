from flask import Flask
from .routes import routes_routes
app = Flask(__name__)

app.config.from_envvar('APP_CONFIG_FILE', silent=True)

MAPBOX_ACCESS_KEY = app.config['MAPBOX_ACCESS_KEY']

@app.route('/', methods=['GET'])
def index():
    return render_template(
    'index.html',
    ACCESS_KEY=MAPBOX_ACCESS_KEY
    )

if __name__ == '__main__':
  app.run(host='0.0.0.0')
