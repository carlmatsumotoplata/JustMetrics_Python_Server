runserver:
	watchmedo auto-restart --pattern="*.py" --recursive -- python pythonserver.py

install:
	pip install -r requirements.txt

test:
	pytest