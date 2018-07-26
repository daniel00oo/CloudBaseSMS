if [ $# -ne 0 ]; then
	if [ $1 -eq "help" ]; then
		python receive.py "help"
	else
		python receive.py $1 $2 $3 > log.txt
	fi
else
	python receive.py > log.txt
fi
