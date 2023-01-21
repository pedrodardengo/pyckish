

test:
	python -m pytest --cov=pyckish tests/

publish:
	poetry build
	poetry publish