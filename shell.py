from flask import Flask
from .models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

# Create a shell context to use in the interactive shell
@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db, 'User': User}

if __name__ == '__main__':
    app.run()
