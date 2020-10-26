#!/bin/sh


echo ".sh file test"
python --version

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

echo $SELF_PATH
echo $PROGNAME
echo $CURRENT_PATH
python --version

<<'TEST1'
if ! test -d env; then
    # standard macOS does not ship 'virtualenv', so let's add /usr/local/bin to the PATH:
    export PATH=/usr/local/bin:$PATH
    virtualenv env
    . env/bin/activate
#	pip install configparser
#    pip install https://github.com/sekipaolo/pypingdom/archive/master.zip
fi
#. env/bin/activate
export LANG="${LANG:-en_US.UTF-8}"  # needed when printing utf-8 chars
python3 --version
TEST1


export PATH=/opt/anaconda3/bin/:$PATH
source /opt/anaconda3/etc/profile.d/conda.sh
conda activate base
exec $CURRENT_PATH/pyversion.py



