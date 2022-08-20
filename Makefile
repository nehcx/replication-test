preprocess:
	cd src; python preprocess.py
feature:
	cd src; sh context_detect.sh
hyparams:
	cd src; python hyparams.py
search:
	cd src; python main.py
ex_value:
	cd src; python eu_value.py -f ../data/example.csv -a ../cache/after.txt -b ../cache/before.txt -o ../artifact/ex_valued.csv 
stat:
	cd src; Rscript stat.R
