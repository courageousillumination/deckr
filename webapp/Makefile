all: test lint
test:
	mkdir -p reports;
	coverage erase;
	coverage run -p --source=deckr --omit='*/management/*','*/migrations/*' manage.py test --with-xunit --xunit-file=reports/unit.xml;
	python manage.py harvest -S --with-xunit --xunit-file=reports/lettuce.xml;
	coverage combine;
	coverage html --directory=reports/coverage
	coverage xml -o reports/coverage.xml
lint:
	autopep8 --aggressive --in-place -r deckr
	(pylint deckr --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > reports/pylint.report) || true