## -*- coding: utf-8 -*-
from app_block import app
from app_block import routes

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

if __name__ == "__main__":
    app.run(debug=True)