# Development-related targets

# gather dependencies
requirements:
	pip freeze > requirements.txt

# install dependencies for production
install:
	pip install -r requirements.txt

# remove Python file artifacts
clean:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -rf {} +
	@find . -name '.ipynb_checkpoints' -exec rm -rf {} +

# check style
lint: format
	pylint --exit-zero --jobs=0 --output-format=colorized .
	pycodestyle --show-source .
	pydocstyle .

# format according to style guide
format:
	black .
	isort -rc .

# build Docker image of project
docker-build: clean
	docker build --no-cache --rm --tag gbacon/cerberus:latest .

# run and enter container from image
docker-run:
	docker run -it -p 8080:8080 gbacon/cerberus:latest bash

# remove Docker cruft
docker-clean:
	docker system prune -af

# run app
run:
	streamlit run front/app.py

.PHONY: requirements install install-dev clean lint format docker-build \
  docker-run docker-clean run