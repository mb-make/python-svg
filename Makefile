
.PHONY: all clean

all: test

test:
	./pytest.sh

clean:
	rm -fR *.pyc */*.pyc */*/*.pyc __pycache__ */__pycache__ */*/__pycache__ .pytest_cache
