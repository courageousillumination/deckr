all: 
verify: test lint
test:
	mkdir -p reports;
	coverage erase;
	coverage run -p --source=deckr,engine --omit='*/management/*','*/migrations/*' manage.py test --with-xunit --xunit-file=reports/unit.xml;
	python manage.py harvest -S -t -skip --with-xunit --xunit-file=reports/lettuce.xml;
	coverage combine;
	coverage html --directory=reports/coverage
	coverage xml -o reports/coverage.xml
lint:
	(pylint deckr engine --rcfile=.pylintrc  > reports/pylint.report) || true
autolint:
	autopep8 --aggressive --in-place -r deckr
	autopep8 --aggressive --in-place -r engine
