all: 
verify: test lint
test:
	mkdir -p reports;
	coverage erase;
	coverage run -p --source=deckr --omit='*/management/*','*/migrations/*' manage.py test --with-xunit --xunit-file=reports/unit.xml;
	python manage.py harvest -S -t -skip --with-xunit --xunit-file=reports/lettuce.xml;
	coverage combine;
	coverage html --directory=reports/coverage
	coverage xml -o reports/coverage.xml
lint:
	# Disable R0904 too many public methods since it doesn't
	# ignore parent classes.
	(pylint deckr --rcfile=.pylintrc  > reports/pylint.report) || true
autolint:
	autopep8 --aggressive --in-place -r deckr
