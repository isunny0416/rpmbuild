# -*-Shell-script-*-
#
# @file: sktx-tar
# @brief: SKTechx Compression tool
# @author: YoungJoo.Kim
# @version:
# @date:
#
# https://wiki.archlinux.org/index.php/Color_Bash_Prompt

# source function library

program_name=$(basename $0)

usage() {
    echo $"Usage: $program_name [TARGET] [OPTIONS...]"
    echo
    echo "Target:"
    echo "        {Compress file}   Decompress file"
    echo "        {Directory}       Compress directory"
    echo
    echo "Options:"
    echo "        {options...}      Compress options"
    echo
    echo "Decompress:"
    echo "        $program_name test.tgz"
    echo "        $program_name test.tar.bz2"
    echo "        $program_name {compress file}"
    echo
    echo "Compress:"
    echo "        $program_name test"
    echo "        $program_name test zip"
    echo "        $program_name {directory} {compression type}"
    exit 1
}

# SKTechx compress|uncompress
# compress: txtar dir | txtar dir tgz | txtar dir zip...
# uncompress: txtar compress.tar.bz2
txtar() {
    ansiEcho() {
        echo -en "\\033[1;34m$*\033[0m"
    }

    cmdEcho() {
        echo
        echo -n "["
        ansiEcho $*
        echo "]";
    }

    whatDo() {
        [ -d "$zipfile" ] && ido="zip" && return 1
        [ ! -f "$zipfile" ] && return 1
        ido="unzip"
    }

    uncompress() {
        for ((a=0; a < ${#unzips[@]} ; a++))
        do
            ext=${unzips[$a]}
            ext0=${ext##*:}
            cmd0=${ext%%:*}
            index=$(( ${#zipfile} - ${#ext0} ))
            zipfileext=${zipfile:index}
            if [ "x${ext0}" == "x${zipfileext}" ]; then
                if [ "${ext0}" == "rpm" ]; then
                    $cmd0 $zipfile | cpio -ivdu
                    cmdEcho $cmd0 $zipfile "| cpio -ivdu"
                    return
                fi
                $cmd0 $zipfile
                cmdEcho $cmd0 $zipfile
                return
            fi
        done
    }

    compress() {
        dstfile=$(basename $zipfile)
        if [ -z "$options" ]; then
            ext=${zips[0]}
            ext0=${ext##*:}
            cmd0=${ext%%:*}
            $cmd0 $dstfile.$ext0 $zipfile
            cmdEcho $cmd0 $dstfile.$ext0 $zipfile
            return
        fi

        for ((a=0; a < ${#zips[@]} ; a++))
        do
            ext=${zips[$a]}
            ext0=${ext##*:}
            cmd0=${ext%%:*}
            if [ "x${ext0}" == "x${options}" ]; then
                if [ "${ext0}" == "bz2" ]; then
                    $cmd0 $zipfile
                    cmdEcho $cmd0 $zipfile
                    return
                fi
                $cmd0 $dstfile.$ext0 $zipfile
                cmdEcho $cmd0 $dstfile.$ext0 $zipfile
                return
            fi
        done
    }

    # uncompress
    unzips=( "tar xvjfp:tar.bz2" \
            "tar xvzfp:tar.gz" \
            "tar xvJfp:tar.xz" \
            "tar xvzfp:tgz" \
            "bzip2 -fkd:bz2" \
            "unzip -o:zip" \
            "gzip -df:gz" \
            "jar -xvf:jar" \
            "rpm2cpio:rpm" \
            "tar xvf:tar" )
   
    # compress
    zips=( "tar cvjfp:tar.bz2" \
            "tar cvzfp:tar.gz" \
            "tar cvJfp:tar.xz" \
            "tar cvzfp:tgz" \
            "bzip2 -fk:bz2" \       # Not working: only file
            "zip -r:zip" \
            "jar -cvf:jar" \
            "tar cvf:tar" )

    zipfile=$1
    options=$2

    whatDo

    [ "x${ido}" == "xzip" ] && compress $options && return
    [ "x${ido}" == "xunzip" ] && uncompress && return
}  

[ -z "$1" ] && usage || txtar $*


# vi:set ft=sh ts=4 sw=4 et fdm=marker:
