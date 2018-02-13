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
    local _template=$1

    [ -z "$_template" ] && usage

    bootstrap_get_bootstrap $_template || bootstrap_check_code
    bootstrap_run_bootstrap $_template && sync $_template
}

list() {
    bootstrap_verbose "off"
    bootstrap_get_list
}

sync() {
    local _template=$2 _random_delay= _common_template=

    # run random delay
    if [[ "$_template" =~ ^--random-delay ]]; then
        _random_delay=${_template##*=}
        _template=
        sleep $((RANDOM%_random_delay))
    fi

    shift 2

    # load template by init
    if [ -z $_template ]; then
        if [ -f $sktx_sysconfig_path ]; then
            . $sktx_sysconfig_path
            _template=$template
        fi
    fi

    # check if template exists
    if [ -n $_template ]; then
        bootstrap_template_in $_template
        if [ "$?" -ne "0" ]; then
            bootstrap_print "error: $_template does not exist in the repository." "red"
            return 1
        fi
    fi

    # sync common-template
    _common_template="common.${os}"

    [ "$_common_template" != "$_template" ] && bootstrap_sync_file "$_common_template"

    # sync user-defined-template
    [ -n $_template ] && bootstrap_sync_file "$_template"

    # exec modules
    bootstrap_sync_jobs "${_template:-$_common_template}"
}

desc() {
    local _template=$2
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
    echo "        --list                         List templates"
    echo "        --init=[template]              Init bootstrap"
    echo "        --sync                         Sync files & Exec modules"
    echo "        --clean                        Clean Cache"
    echo
    echo "Options:"
    echo "        --random-delay=[number]        Integer value for delay time generation"
    echo "                                       when using the --sync option."
    echo
    echo "Examples:"
    echo "        $program_name --list"
    echo "        $program_name --init=mytemplate.centos.7.x86_64"
    echo "        $program_name --sync"
    exit 1
}

option_value=${1##*=}
option_name=${1%%=*}

case "$option_name" in
    --init)
        [ "$option_name" == "$option_value" ] && usage
        init $option_value
        ;;
    --sync)
        sync $*
        ;;
    --list)
        list $*
        ;;
    --desc)
        desc $*
        ;;
    --clean)
        clean $*
        ;;
    *)
        usage
        RETVAL=1
esac
exit $RETVAL

# vi:set ft=sh ts=4 sw=4 et fdm=marker:
