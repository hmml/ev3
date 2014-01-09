#!/bin/sh
#
# Script updates ev3 module on EV3 brick.
#
# It's suggested to have key based authorisation see README.md.
#

EV3=root@10.0.1.1
EV3_TMP_DIR=/tmp/ev3
EV3_PACKAGE=ev3.tar.gz

cd $(dirname $0)

echo "* Preparing package..."
find . -iname '*.pyc' | xargs rm
tar cfz ${EV3_PACKAGE} ev3 setup.py

echo "* Coping package..."
ssh ${EV3} "rm -rf ${EV3_TMP_DIR}"
ssh ${EV3} "mkdir -p ${EV3_TMP_DIR}"
scp ${EV3_PACKAGE} ${EV3}:${EV3_TMP_DIR}/${EV3_PACKAGE}
ssh ${EV3} "cd ${EV3_TMP_DIR} && tar xf ${EV3_PACKAGE}"

echo "* Uninstalling previous package..."
ssh ${EV3} "yes | pip uninstall python-ev3"

echo "* Installing new package..."
ssh ${EV3} "cd ${EV3_TMP_DIR} && pip install ."

echo "* Cleanup..."
rm ${EV3_PACKAGE}
ssh ${EV3} "rm -rf ${EV3_TMP_DIR}"

echo "* Done."