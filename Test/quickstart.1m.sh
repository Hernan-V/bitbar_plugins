#!/bin/sh

SELF_PATH=$(cd -P -- "$(dirname -- "$0")" && pwd -P) && SELF_PATH=$SELF_PATH/$(basename -- "$0")
CURRENT_PATH=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
# resolve symlinks
while [ -h "$SELF_PATH" ]; do
    # 1) cd to directory of the symlink
    # 2) cd to the directory of where the symlink points
    # 3) get the pwd
    # 4) append the basename
    DIR=$(dirname -- "$SELF_PATH")
    SYM=$(readlink "$SELF_PATH")
    SELF_PATH=$(cd "$DIR" && cd "$(dirname -- "$SYM")" && pwd)/$(basename -- "$SYM")
done

PROGNAME="$(basename "$SELF_PATH")"

error_exit()
{
	echo "${PROGNAME}: ${1:-"Unknown Error"}" 1>&2
	exit 1
}

export PATH=/opt/anaconda3/bin/:$PATH
source /opt/anaconda3/etc/profile.d/conda.sh
<<'TEST1'
if ! test -d gapi; then
    # standard macOS does not ship 'virtualenv', so let's add /usr/local/bin to the PATH:
    export PATH=/opt/anaconda3/bin/:$PATH
    source /opt/anaconda3/etc/profile.d/conda.sh
    conda create -n gapi python=3.6 ipykernel numpy
    conda activate gapi
#	pip install configparser
#    pip install https://github.com/sekipaolo/pypingdom/archive/master.zip
fi
TEST1

conda activate gapi
#conda info
export LANG="${LANG:-en_US.UTF-8}"  # needed when printing utf-8 chars
exec $CURRENT_PATH/Test/g-api-quickstart/quickstart.py



