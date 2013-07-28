#!/bin/bash

#rm -fR .coverage cover/

if ! test "x$(which nosetests-2.6)" = "x"; then
	printf "Testing \033[32mpython 2.6\033[0m\n"
	nosetests-2.6 --with-coverage --cover-html --cover-package=pybonjour || exit
fi

if ! test "x$(which nosetests-2.7)" = "x"; then
	printf "Testing \033[32mpython 2.7\033[0m\n"
	nosetests-2.7 --with-coverage --cover-html --cover-package=pybonjour || exit
fi

if ! test "x$(which nosetests-3.3)" = "x"; then
	printf "Testing \033[32mpython 3.3\033[0m\n"
	nosetests-3.3 --with-coverage --cover-html --cover-package=pybonjour || exit
fi
