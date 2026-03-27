TARGETS := venv

run: venv
	venv/bin/python main.py

all: $(TARGETS)

venv: requirements.txt
	-rm -rf venv
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt

clean:
	rm -rf $(TARGETS)

.PHONY: run all clean
