import config

from pytz import timezone

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor


class Scheduler():
    """ Initialize Advanced Python Scheduler. """

    def initialize(self, app):
        app.logger.info("Initialize Advanced Python Scheduler.")
        app.logger.info(app)

        user_timezone = timezone(config.TIMEZONE)

        # Persistence settings using SQLAlchemy and PostgreSQL.
        jobstores = {
            'default': SQLAlchemyJobStore(url=config.SQLALCHEMY_DATABASE_URI)
        }

        executors = {
            'default': ThreadPoolExecutor(10)  # 20
        }

        job_defaults = {
            'coalesce': False,
            'max_instances': 5
        }

        # Use the BackgroundScheduler.
        scheduler = BackgroundScheduler(
            jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=user_timezone)

        # Start the scheduler.
        scheduler.start()
        return scheduler
