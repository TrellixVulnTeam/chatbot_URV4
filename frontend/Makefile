# HELP
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Setup developer environment
	rm -rf node_modules
	echo n | npm install @angular/cli
	echo n | npm install @angular-devkit/build-angular

clean: ## Removes any build artifacts and any logs
	rm -rf dist && rm -rf *.log*

run: ## Run dev server. Navigate to http://localhost:4200/. The app will automatically reload if you change any of the source files.
	ng serve --port 4200

dist: clean ## Creates a production build. The build artifacts will be stored in the dist/ directory.
	ng build --delete-output-path
