run:
	./vidconvert 

setup: requirements.txt
	pip3 install -r requirements.txt
	cp vidconvert.py /usr/local/bin/

clean:
	rm -rf __pycache__

.PHONY: run clean #ensure that files named run and clean are ignored by makefile
