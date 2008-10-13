#!/bin/sh

rev=`LANGUAGE=C svn info | grep Revision | cut -d ' ' -f 2`

if [ x != x$rev ]; then
	echo "#define DRIVER_VERSION	\"SVN r$rev\""
fi

