#!/bin/env bash
#
# @file: sktx-manager
# @brief: bootstrap Manager
# @author: YoungJoo.Kim
# @version:
# @date:
#
# source function library

default_functions_path="/usr/share/sktx/manager/common/bash/functions"

[ -f "$default_functions_path" ] && . $default_functions_path

program_name=$(basename $0)

init() {
    _template=$2

    [ -z "$_template" ] && usage

    shift 2
    bootstrap_get_bootstrap $_template || bootstrap_check_code
    bootstrap_run_bootstrap "$_template" "$*" && sync "$_template"
}

list() {
    _template=$2
    shift 2
    bootstrap_get_list "$_template"
}

sync() {
    _template=$2
    shift 2
    bootstrap_sync_file "$_template"
}

desc() {
    _template=$2
    [ -z  "$_template" ] && usage
    bootstrap_get_desc "$_template" "$program_name"
}

clean() {
    bootstrap_remove_cache
}

usage() {
    echo $"Usage: $program_name [COMMAND] [OPTIONS...]"
    echo
    echo "Commands:"
    echo "        list              List templates"
    echo "        init              Init bootstrap"
    echo "        sync              Sync files"
    echo "        clean             Clean Cache"
    echo
    echo "Options:"
    echo "        [options...]      Options"
    echo
    echo "Examples:"
    echo "        $program_name list"
    #echo "        $program_name init {TEMPLATE} {OPTIONS...}"
    echo "        $program_name init [template]"
    echo "        $program_name sync"
    exit 1
}

case "$1" in
    init)
        init $*
        ;;
    sync)
        sync $*
        ;;
    list)
        list $*
        ;;
    desc)
        desc $*
        ;;
    clean)
        clean $*
        ;;

    *)
        usage
        RETVAL=1
esac
exit $RETVAL

# vi:set ft=sh ts=4 sw=4 et fdm=marker:
