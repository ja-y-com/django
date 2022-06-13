from django.apps import AppConfig


class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'

    def ready(self):
        from django.conf import settings

        if settings.APP_ROLE == "API":
            from conf.settings import scheduler
            from .schedulers import some_scheduler

            if "some_scheduler" not in scheduler.get_jobs():
                scheduler.add_job(
                    some_scheduler,
                    "interval",
                    seconds=60,
                    id="some_scheduler"
                )
