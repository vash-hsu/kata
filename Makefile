PYTHONPATH=$(shell pwd)
UNITTESTS=$(shell find */ -type f -iname 'test_*.py')
MAINS=$(shell find */ -type f -iname '*.py')

all: sonar

.PHONY: clean main test coverage cov sonar

main:
	@for target in ${MAINS}; do\
		echo "===== ===== ===== ====="; \
		echo $$target; \
		echo "===== ===== ===== ====="; \
		python $$target ; \
	done


test:
	@for target in ${UNITTESTS}; do\
		echo $$target; \
		PYTHONPATH=${PYTHONPATH} python $$target ; \
	done


cov:
	-nosetests */test* --with-coverage --cover-erase --cover-inclusive \
	--cover-tests --cover-branches --cover-html \
	--cover-xml --cover-xml-file=coverage_unittest.xml \
	--with-xunit --xunit-file=nosetests_unittest.xml


coverage:
	@coverage erase
	@for target in ${UNITTESTS}; do\
		PYTHONPATH=${PYTHONPATH} coverage run -a --branch $$target ; \
	done
	@for target in ${MAINS}; do\
		PYTHONPATH=${PYTHONPATH} coverage run -a --branch $$target ; \
	done
	@coverage report
	@coverage html


sonar: cov
	sonar-scanner -X


clean:
	rm -rf *.pyc
	find . -name *.pyc | xargs rm -rf
	rm -rf htmlcov cover .coverage coverage*.xml
	rm -rf tests/*/cover tests/*/.coverage tests/*/coverage*.xml
	rm -f coverage*.xml nosetests*.xml
	rm -rf cover
