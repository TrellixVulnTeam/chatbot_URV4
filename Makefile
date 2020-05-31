# import deploy.env
dpl ?= ./deploy.env
include $(dpl)
export $(shell sed 's/=.*//' $(dpl))

app_name = ai_team_7/chatbot

# HELP
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

clean: ## Removes build artifacts and any logs
	rm -rf *.egg-info && rm -rf dist && rm -rf *.log* && rm -rf build

clean-all: clean ## Removes the virtual environment, any build artifacts, and any logs
	rm -rf venv

env: ## Creates or updates project's virtual enviornment. To activate, run: source venv/bin/activate
	python3 -m venv venv --prompt chatbot
	venv/bin/pip install -r requirements.txt

run: ## Run chat.py
	CONFIG_ENV=config.env,deploy.env venv/bin/python chat.py

docker-build: ## Build docker image
	docker build -t $(app_name) .
	docker tag $(app_name) $(docker_repo)/$(app_name):latest

docker-run: # Run containerized app
	docker run -it --rm -p 8080:8080 \
	--name="chatbot" ${docker_repo}/${app_name}:latest

docker-publish: ## Publish `latest` tagged container to docker repo
	@echo 'publish latest to $(docker_repo)'
	docker push $(docker_repo)/$(app_name):latest