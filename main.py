from app_instance import app
from database import init_db

init_db()

import auth
import patient
import doctor
import admin

if __name__ == "__main__":
    app.run(debug=True)