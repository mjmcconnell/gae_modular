help:
	@echo "clean - remove build artifacts"
	@echo "deploy - deploy the app to appengine"
	@echo "run - run the local development server for testing/debugging purposes"
	@echo "test - run all of the app's tests and print a coverage report"

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -empty -type d -delete
	-rm -f .coverage

deploy: clean
	# deploy application to the default environment
	appcfg.py update . -A $(app) -V $(version)

run:
	# run the appengine development server
	dev_appserver.py .

test:
	@python tests/run-tests.py
