from core.celery import app


@app.task
def transfer_student_to_student(from_id, to_id, sum_count):
	...
