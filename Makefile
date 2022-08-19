preprocess:
	cd src; python preprocess.py
feature:
	cd src; sh context_detect.sh
hyparams:
	cd src; python hyparams.py
search:
	cd src; python main.py
stat:
	cd src; Rscript stat.R
