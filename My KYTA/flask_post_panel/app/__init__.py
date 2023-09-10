# ... __init__.py ...


from flask import Flask
from .extensions import bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
from flask_migrate import Migrate
import pytz
from flask_bcrypt import Bcrypt

app = Flask(__name__)


app = Flask(__name__)

bcrypt.init_app(app)




app.config['JSON_AS_ASCII'] = False

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

migrate = Migrate(app, db)

from app import routes, models

def remove_expired_panels():
    now = datetime.utcnow()
    threshold = timedelta(days=30)
    expired_panels = models.Panel.query.filter(models.Panel.last_accessed < now - threshold).all()
    for panel in expired_panels:
        db.session.delete(panel)
    db.session.commit()

scheduler = BackgroundScheduler(timezone=pytz.utc)


scheduler.start()
scheduler.add_job(
    func=remove_expired_panels,
    trigger=IntervalTrigger(hours=24),
    id='remove_expired_panels',
    name='Remove expired panels',
    replace_existing=True
)
