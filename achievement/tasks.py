from celery import shared_task


@shared_task
def grant_achievement(student_id, achievement_id):
	pass
