run:
	vidconvert 

setup: requirements.txt
	pip install -r requirements.txt

clean:
	rm -rf __pycache__

.PHONY: run clean #ensure that files named run and clean are ignored by makefile
