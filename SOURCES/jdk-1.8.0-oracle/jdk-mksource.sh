#!/bin/sh

usage() {
	echo "USAGE: $0 version [i386|x86_64]" >& /dev/stderr
	exit 1
}

[ $# != 2 ] && usage

pkg=jdk
version=$1
mversion=${version%.*}
uversion=${version##*_}
workdir="${pkg}-${version}"
arch="$2"
[ "${arch}" = "i386" ] && narch="i586" || narch="x64"

[ -d "${workdir}" ] && rm -rf ${workdir}

echo $version
echo $mversion
echo $uversion

mkdir ${workdir}
pushd ${workdir}
cur=$(/bin/pwd)

wget -O ${cur}/res.html --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

#javaurl=$(cat ${cur}/res.html | grep ${pkg}-8u${uversion}-linux-${narch}.rpm | awk '{print $7}' | sed -e 's/.*"http/http/g' -e 's/"}.*//g')
javaurl=$(cat ${cur}/res.html | grep ${pkg}-8u${uversion}-linux-${narch}.rpm | awk -F '"' '{print $12}')

wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" ${javaurl}
mv ${pkg}-8u${uversion}-linux-${narch}.rpm ${pkg}-${version}-fcs.${arch}.rpm && rm -f ${cur}/res.html

# extract package
rm -rf ${arch}
mkdir -p ${arch}
pushd ${arch}
rpm2cpio ../${pkg}-${version}-fcs.${arch}.rpm | cpio -idmv
popd
rm -f ${pkg}-${version}-fcs.${arch}.rpm

# remove jdk 8
#mv ${arch}/etc/ ./etc/

pushd ${arch}
	mv usr/java/${pkg}${version}/* ./
	rm -f COPYRIGHT LICENSE README *.html *.txt
	rm -rf usr demo sample man/ja* plugin/desktop
popd

mv ${arch}/{src.zip,include,man} ./

# Unpacking jar
pushd ${arch}
	for list in $(find . -name "*.pack")
	do
		echo "Unpacking $list .."
		up_name=$(basename $list .pack)
		up_path=$(dirname $list)
		bin/unpack200 $list $up_path/$up_name.jar
	done
popd
find . -name "*.pack" -exec rm -f {} \;

popd

#tar cvfpj ${pkg}-${version}.tar.bz2 ${workdir}
mv ${workdir}/* ./
#rm -rf ${workdir}

exit 0
