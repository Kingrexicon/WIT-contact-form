from flask import Flask
from config import APP_SECRET_KEY
from routes import register_routes

app = Flask(__name__)
app.secret_key = APP_SECRET_KEY

register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)