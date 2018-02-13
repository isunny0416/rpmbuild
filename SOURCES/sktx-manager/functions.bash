# -*-Shell-script-*-
#
# @file: functions
# @brief: Bootstrap Bash Script functions
# @author: YoungJoo.Kim
# @version:
# @date:
#

TEXTDOMAIN=bootstrapscripts

# Make sure umask is sane
umask 022

# Set up a default search path.
SKTX_PATH="/usr/share/sktx/manager/common/bin"
PATH="/sbin:/usr/sbin:/bin:/usr/bin:$SKTX_PATH"
export PATH

# Global Manager Configs
sktx_version=2017122700
sktx_banner="SKTX Manager"
sktx_root=/var/lib/sktx
sktx_config_path=/etc/sktx/sktx.conf
sktx_sysconfig_path=/etc/sysconfig/sktx

# Global Return Variables
G_RET_VAL=
G_RET_STR=
G_RET_CAC=
G_HASH_VAL=

bootstrap_verbose() {
    local _flag=$1
    [ -z "${sktx_verbose_flag:-}" ] && sktx_verbose_flag=1 || sktx_verbose_flag=
    if [ -n "$_flag" ]; then
        [ "$_flag" == "on" ] && sktx_verbose_flag=1 || sktx_verbose_flag=
    fi
}

bootstrap_ansi() {
    local _flag=$1
    [ -z "${sktx_ansi_flag:-}" ] && sktx_ansi_flag=1 || sktx_ansi_flag=
    if [ -n "$_flag" ]; then
        [ "$_flag" == "on" ] && sktx_ansi_flag=1 || sktx_ansi_flag=
    fi
}

bootstrap_cache() {
    local _flag=$1
    [ -z "${sktx_cache_flag:-}" ] && sktx_cache_flag=1 || sktx_cache_flag=
    if [ -n "$_flag" ]; then
        [ "$_flag" == "on" ] && sktx_cache_flag=1 || sktx_cache_flag=
    fi
}

bootstrap_install_global_dependency() {
    # Install curl
    bootstrap_check_package_install curl

    # Install perl
    bootstrap_check_package_install perl

    # Install sktx-release
    bootstrap_check_package ${sktx_release_name:-}
    if [ "$G_RET_VAL" != "0" ]; then
        bootstrap_install_release
        bootstrap_check_package ${sktx_release_name:-}
        [ "$G_RET_VAL" != "0" ] && return 1
    fi

    return $G_RET_VAL
}

bootstrap_set_global_config() {
    bootstrap_parse_config ${sktx_config_path:-}

    # System info
    cpe=$(</etc/system-release-cpe)
    cpes=(${cpe//:/ })
    os=${cpes[2]}.${cpes[4]}.$(arch)

    sktx_manager_domain=${sktx_manager_domain:-$(bootstrap_get_config "manager_domain")}
    sktx_manager_url=${sktx_manager_url:-$(bootstrap_get_config "manager_url")}
    sktx_cache_flag=${sktx_cache_flag:-$(bootstrap_get_config "cache")}
    sktx_cache_expire=${sktx_cache_expire:-$(bootstrap_get_config "cache_expire")}
    bootstrap_cache "$sktx_cache_flag"

    sktx_rpm_domain="pkgrepos.sktx.com"
    sktx_manager_root="${sktx_root:-}/control"
    sktx_deploy_root="${sktx_manager_root:-}/deploy"
    sktx_deploy_url="${sktx_manager_url:-}/deploy"
    sktx_release_name="sktx-release"
    sktx_release_url="http://${sktx_rpm_domain:-}/centos/7/x86_64/Packages/${sktx_release_name:-}-7-1.sk.el7.noarch.rpm"
    sktx_curl_options="-f -s"
    sktx_verbose_flag=1
    sktx_ansi_flag=1
    sktx_default_mode=644
    sktx_default_lang="ko_KR.UTF-8"

    sktx_current_country_code=${LANG//.*/}
    sktx_current_country_code=${sktx_current_country_code//*_/}
    sktx_current_country_code=${sktx_current_country_code,,}

    return $G_RET_VAL
}

bootstrap_parse_config() {
    local _cfg=$1 cfg=
    [ ! -f "$_cfg" ] && return 1
    for cfg in $(_bootstrap_load_config ${_cfg})
    do
        #_left=${cfg//=*/}
        #_right=${cfg//*=/}
        _left=${cfg%%=*}
        _right=${cfg#*=}
        _right=${_right//\[\[:space:\]\]/ }
        _bootstrap_hash_insert "_config" "$_left" "$_right"
    done
}

bootstrap_get_config() {
    local _cfg=$1
    _bootstrap_hash_select "_config" "$_cfg"
}

bootstrap_parse_options() {
    local _options=$* option=
    for option in $_options
    do
        _left=${option//=*/}
        _right=${option//*=/}
        _bootstrap_hash_insert "_options" "$_left" "$_right"
    done
}

bootstrap_get_option() {
    local _option=$1
    _bootstrap_hash_select "_options" "$_option"
}

bootstrap_ansi_echo() {
    local _msg=$1
    local _color=$2

    _bootstrap_hash_insert "_colors" "black" "30"
    _bootstrap_hash_insert "_colors" "red" "31"
    _bootstrap_hash_insert "_colors" "green" "32"
    _bootstrap_hash_insert "_colors" "yellow" "33"
    _bootstrap_hash_insert "_colors" "blue" "34"
    _bootstrap_hash_insert "_colors" "magenta" "35"
    _bootstrap_hash_insert "_colors" "cyan" "36"
    _bootstrap_hash_insert "_colors" "white" "37"

    ! [[ "$_color" =~ ^[0-9]+$ ]] && _color=$(_bootstrap_hash_select "_colors" "$_color")
    [ -z "$_color" ] && _color=$(_bootstrap_hash_select "_colors" "blue")

    if [ -n "${sktx_ansi_flag:-}" ]; then
        echo -en "\\033[1;${_color}m${_msg}\033[0m"
    else
        echo -en "${_msg}"
    fi
}

bootstrap_print() {
    local _msg=$1
    local _color=$2
    if [ -n "${sktx_verbose_flag:-}" ]; then
        echo -n "# "
        bootstrap_ansi_echo "$_msg" "$_color"
        echo
    fi
}

bootstrap_check_package() {
    local _package=$*
    \rpm -q ${_package} &> /dev/null
    G_RET_VAL=$?
    _bootstrap_set_ret_str "o:x"
    return $G_RET_VAL 
}

bootstrap_install_release() {
    bootstrap_print ">>>> Install: sktx-release" "black"
    \rpm -Uvh ${sktx_release_url:-}
    G_RET_VAL=$?
    _bootstrap_set_ret_str "o:x"
    return $G_RET_VAL 
}

bootstrap_check_package_install() {
    local _package=$*
    bootstrap_check_package $_package
    if [ "$G_RET_VAL" != "0" ]; then
        bootstrap_pkg_install $_package
        bootstrap_check_package $_package
        [ "$G_RET_VAL" != "0" ] && return 1
    fi
    return $G_RET_VAL
}

bootstrap_init() {
    local _template=$1
    bootstrap_print ">>>> $sktx_banner Start: $_template" "cyan"
    bootstrap_print ">>>> Version: $sktx_version" "cyan"

    bootstrap_update_common

    return $G_RET_VAL
}

bootstrap_finish() {
    local _template=$1
    bootstrap_print ">>>> $sktx_banner Finish: $_template" "cyan"
}

bootstrap_check_code() {
    if [ "$G_RET_VAL" != "0" ]; then
        bootstrap_print "[$G_RET_STR] bootstrap_check_code[$G_RET_VAL]: FAILED" "red"
        exit $G_RET_VAL
    fi
}

bootstrap_files() {
    local _files_path=$1
    \awk '/^[^#[:space:]].*/ {print $1"|"$2"|"$3"|"$4"|"$5"|"$6}' $_files_path
}

bootstrap_parse_files() {
    local stat=$1
    local stat=${1//\*/ALL}
    local ss=

    stat_path=
    stat_type=
    stat_uid=
    stat_gid=
    stat_mode=
    stat_node=

    ss=(${stat//\|/ })

    stat_path=${ss[0]}
    stat_type=${ss[1]}
    stat_uid=${ss[2]}
    stat_gid=${ss[3]}
    stat_mode=${ss[4]}
    if [ ${ss[5]} == "ALL" ]; then
        stat_node="root"
    else
        stat_node="node/${ss[5]}"
    fi
    #stat_node="${ss[5]/ALL/root}"
}

bootstrap_packages() {
    local _files_path=$1
    \awk '/^[^#[:space:]].*/ {printf $0"|"}' $_files_path
}

bootstrap_parse_packages() {
    local package=$1
    local arr=
    package_name=
    package_version=
    package_summary=

    local OIFS=$IFS
    local IFS=':'
    arr=(${package})
    package_name=${arr[0]}
    package_version=${arr[1]}
    package_summary=${arr[2]}

    IFS=$OIFS
}

bootstrap_remove_cache() {
    local _repodata_root="${sktx_manager_root:-}/repodata"

    bootstrap_print ">>>> Template remove" "black"

    bootstrap_ansi_echo "Clean Repository Data: " "white" && bootstrap_progress 5
    _bootstrap_remove "$_repodata_root" && bootstrap_ansi_echo "[OK]\n" "green" || echo "[OK]"
    bootstrap_ansi_echo "Clean Setup Data: " "white" && bootstrap_progress 5
    _bootstrap_remove "${sktx_deploy_root:-}" && bootstrap_ansi_echo "[OK]\n" "green" || echo "[OK]"

    return $G_RET_VAL
}

bootstrap_remove_entry() {
    local _template=$1
    
    [ -z "$_template" ] && return 1 

    _template_root="${sktx_deploy_root:-}/${_template}"
    bootstrap_print ">>>> Template remove" "black"
    _bootstrap_remove "$_template_root"
    bootstrap_print "[$G_RET_STR] $_template_root" "white"
    return $G_RET_VAL
}

bootstrap_replace_entry() {
    local _template=$1
    local _from_str=$2
    local _to_str=$3
    local _template_root= _files_url= _files_path= _entry_path= _entry_dest= stat=
    
    [ -z "$_template" ] && return 1 

    _template_root="${sktx_deploy_root:-}/${_template}"

    _files_url="${sktx_deploy_url:-}/${_template}/controller/files"
    
    _files_path="${_template_root}/controller/files"

    if [ -f "$_files_path" ]; then
        bootstrap_print ">>>> Template file replace" "black"
        for stat in $(bootstrap_files $_files_path)
        do
            bootstrap_parse_files "$stat"
            _entry_path="${_template_root}/entry"
            if [ "$stat_kind" == "f" ]; then
                _entry_dest="${_entry_path}${stat_path}"
                _bootstrap_replace "$_from_str" "$_to_str" "$_entry_dest"
                bootstrap_print "[$_from_str => $_to_str] $_entry_dest" "white"
            fi
        done
    fi
}

bootstrap_get_bootstrap() {
    local _template=$1
    local _template_root= _files_url= _files_path=
    [ -z "$_template" ] && return 1 

    _template_root="${sktx_deploy_root:-}/${_template}"

    _bootstrap_mkdir ${_template_root}/tasks
    
    _files_url="${sktx_deploy_url:-}/${_template}/tasks/bootstrap"
    
    _files_path="${_template_root}/tasks/bootstrap"

    bootstrap_print ">>>> Download: bootstrap" "black"
    _bootstrap_get "$_files_url" "$_files_path"

    if [ ! -e "$_files_path" ]; then
        _bootstrap_remove "$_template_root"
        G_RET_VAL=1
    fi

    return $G_RET_VAL
}

bootstrap_run_bootstrap() {
    local _template=$1
    local _template_root= _files_path=
    if [ -z "$_template" ]; then
        G_RET_VAL=1
        return $G_RET_VAL
    fi

    if [ -f "$sktx_sysconfig_path" ]; then
        . $sktx_sysconfig_path
        bootstrap_print "It is already initialized as a [$template]" "red"
        G_RET_VAL=1
        return $G_RET_VAL
    fi

    _bootstrap_fputs $sktx_sysconfig_path "template=$_template\n"

    _template_root="${sktx_deploy_root:-}/${_template}"

    _files_path="${_template_root}/tasks/bootstrap"

    [ -f "$_files_path" ] && . $_files_path 

    return $G_RET_VAL
}

bootstrap_get_list() {
    local _template=$1
    local _repodata_root= _files_path= package=

    bootstrap_update_repodata

    _repodata_root="${sktx_manager_root:-}/repodata"

    _files_path="${sktx_manager_root:-}/repodata/primary"

    if [ -f "$_files_path" ]; then
        bootstrap_print ">>>> Templates" "black"
        local OIFS=$IFS
        local IFS='|'
        for package in $(bootstrap_packages $_files_path)
        do
            bootstrap_parse_packages "$package"
            if [[ "$package_name" == **${os}** ]]; then
                package_name=$(bootstrap_ansi_echo "$package_name" "white")
                printf "%-50s%-50s%s\n" $package_name $package_version $package_summary
            fi
        done
        IFS=$OIFS
        G_RET_VAL=0
    else
        G_RET_VAL=1
    fi
    return $G_RET_VAL   
}

bootstrap_get_files() {
    local _template=$1
    local _template_root= _files_url= _files_path= stat= _entry_path= _entry_url= _entry_last=
    local _link_src= _link_dst=

    [ -z "$_template" ] && return 1 

    _template_root="${sktx_deploy_root:-}/${_template}"

    _bootstrap_mkdir ${_template_root}/{tasks,files}
    
    _files_url="${sktx_deploy_url:-}/${_template}/tasks/files"

    _files_path="${_template_root}/tasks/files"

    bootstrap_print ">>>> Download: controller files" "black"
    _bootstrap_get "$_files_url" "$_files_path"

    if [ -f "$_files_path" ]; then
        bootstrap_print ">>>> Download: template files" "black"
        for stat in $(bootstrap_files $_files_path)
        do
            bootstrap_parse_files "$stat"

            _entry_path="${_template_root}/files/$stat_node"
            _entry_url="${sktx_deploy_url:-}/${_template}/files/${stat_node}${stat_path}"
            _entry_last=

            if [ "$stat_type" == "f" ]; then
                _entry_dir=$(dirname ${stat_path})
                _entry_dest="${_entry_path}${stat_path}"
                _entry_path="${_entry_path}${_entry_dir}"
                [ ! -e "$_entry_path" ] && _bootstrap_mkdir $_entry_path
                _bootstrap_get "$_entry_url" "$_entry_dest"
                _entry_last=$_entry_dest
            elif [ "$stat_type" == "d" ]; then
                _entry_path="${_entry_path}${stat_path}"
                [ ! -e "$_entry_path" ] && _bootstrap_mkdir $_entry_path
                _entry_last=$_entry_path
            fi

            if [ "$stat_type" == "f" -o "$stat_type" == "d" ]; then
                [ -n "$stat_uid" -a "$stat_uid" != "-" ] && chown $stat_uid $_entry_last
                [ -n "$stat_gid" -a "$stat_gid" != "-" ] && chown :$stat_gid $_entry_last
                [ -n "$stat_mode" -a "$stat_mode" != "-" ] && chmod $stat_mode $_entry_last
            fi
        done
        G_RET_VAL=0
    else
        _bootstrap_remove "$_template_root"
        G_RET_VAL=1
    fi
    return $G_RET_VAL   
}

bootstrap_install_file() {
    local _template=$1
    local _template_root= _files_url= stat= _install_owner= _install_group= _install_mode= _install_options=
    local _entry_path= _entry_last= _entry_dir= _entry_dest=
    local _link_src= _link_dst=

    [ -z "$_template" ] && return 1 

    _template_root="${sktx_deploy_root:-}/${_template}"

    _files_path="${_template_root}/tasks/files"

    bootstrap_print ">>>> Sync: $_template configurations" "black"

    if [ -f "$_files_path" ]; then
        for stat in $(bootstrap_files $_files_path)
        do
            bootstrap_parse_files "$stat"
            _install_owner=$stat_uid
            _install_group=$stat_gid
            _install_mode=${stat_mode:$sktx_default_mode}
            _install_options=

            _entry_path="${_template_root}/files/$stat_node"
            _entry_last=

            [ -n "$stat_ugid" -a "$stat_ugid" != "-" ] && _install_owner=${stat_ugid//:*/} \
                _install_group=${stat_ugid//*:/}
            [ -n "$stat_mode" -a "$stat_mode" != "-" ] && _install_mode=$stat_mode
            [ -n "$_install_owner" ] && _install_options="-o $_install_owner"
            [ -n "$_install_group" ] && _install_options="${_install_options} -g $_install_group"
            [ -n "$_install_mode" ] && _install_options="${_install_options} -m $_install_mode"

            if [ "$stat_type" == "f" ]; then
                _entry_dir=$(dirname ${stat_path})
                _entry_dest="${_entry_path}${stat_path}"
                _entry_path="${_entry_path}${_entry_dir}"
                ##echo "F: $_entry_dir, $_install_options $_entry_dest $stat_path"
                [ ! -e "$_entry_dir" ] && _bootstrap_mkdir $_entry_dir
                _bootstrap_backup_file "$_template" "$stat_path"
                bootstrap_install "$_install_options" "$_entry_dest" "$stat_path"
                bootstrap_print "[$G_RET_STR] $stat_path" "white"
            elif [ "$stat_type" == "d" ]; then
                ##echo "D: install $_install_options -d $stat_path"
                [ ! -e "$_stat_path" ] && install $_install_options -d $stat_path
            elif [ "$stat_type" == "l" ]; then
                _link_src=${stat_path%%@*}
                _link_dst=${stat_path##*@}
                _bootstrap_link $_link_src $_link_dst
                [ -n "$stat_uid" -a "$stat_uid" != "-" ] && chown -h $stat_uid $_link_dst
                [ -n "$stat_gid" -a "$stat_gid" != "-" ] && chown -h :$stat_gid $_link_dst
            fi
        done
    fi
    
    return $G_RET_VAL
}

bootstrap_sync_file() {
    local _template=$1

    # load template by init
    if [ -z $_template ]; then
        if [ -f $sktx_sysconfig_path ]; then
            . $sktx_sysconfig_path
            _template=$template
        fi
    fi

    bootstrap_get_files $_template
    bootstrap_install_file $_template
    return $G_RET_VAL
}

bootstrap_update_repodata() {
    local _repodata_root="${sktx_manager_root:-}/repodata"
    local _files_url= _files_path=

    _bootstrap_mkdir ${_repodata_root}

    _files_url="${sktx_manager_url}/repodata/primary"

    _files_path="${sktx_manager_root:-}/repodata/primary"

    bootstrap_print ">>>> Update: repository data" "black"
    _bootstrap_get "$_files_url" "$_files_path"

    return $G_RET_VAL
}

bootstrap_update_common() {
    local _common_root="${sktx_manager_root:-}/common/bash"
    local _files_url= _files_path=

    _bootstrap_mkdir ${_common_root}
    
    _files_url="${sktx_manager_url}/common/bash/functions"
    
    _files_path="${sktx_manager_root:-}/common/bash/functions"

    bootstrap_print ">>>> Common Update" "black"
    _bootstrap_get "$_files_url" "$_files_path"

    return $G_RET_VAL
}

bootstrap_pkg_install() {
    local _packages=$*
    bootstrap_print ">>>> Install packages: $_packages" "black"
    \yum install -y install $_packages
    bootstrap_check_package "$_packages"
    G_RET_VAL=$?
    _bootstrap_set_ret_str "o:x"
    return $G_RET_VAL 
}

bootstrap_pkg_remove() {
    local _packages=$*
    bootstrap_print ">>>> Remove packages: $_packages" "black"
    \yum remove -y remove $_packages
    G_RET_VAL=$?
    _bootstrap_set_ret_str "o:x"
    return $G_RET_VAL 
}

bootstrap_pkg_clean() {
    local _options=$*
    bootstrap_print ">>>> Clean packages cache: $_options" "black"
    \yum clean $_options
    G_RET_VAL=$?
    _bootstrap_set_ret_str "o:x"
    return $G_RET_VAL 
}

bootstrap_systemctl() {
    local _flag=$1 service=; shift 1
    bootstrap_print ">>>> Systemctl $_flag: $*" "black"
    for service in $*
    do
        \systemctl $_flag $service
    done
}

bootstrap_daemon() {
    local _flag=$1 service=; shift 1
    bootstrap_print ">>>> Init Service Daemon $_flag: $*" "black"
    for service in $*
    do
        if [ -f "/etc/rc.d/init.d/$service" ]; then
            bootstrap_print "[$_flag] $service" "white"
            \service $service $_flag
        elif [ -f "/etc/xinetd.d/$service" ]; then
            bootstrap_print "[$_flag] $service" "white"
            [ "$_flag" == "start" ] && _flag="on"
            [ "$_flag" == "stop" ] && _flag="off"
            \chkconfig $service $_flag
        fi
    done
}

bootstrap_service() {
    local _flag=$1 service=; shift 1
    bootstrap_print ">>>> Init Service Turn $_flag: $*" "black"
    for service in $*
    do
        if [ -f "/etc/rc.d/init.d/$service" ]; then
            \chkconfig --level 35 $service $_flag
            bootstrap_print "[$_flag] $service" "white"
        elif [ -f "/etc/xinetd.d/$service" ]; then
            \chkconfig $service $_flag
            bootstrap_print "[$_flag] $service" "white"
        fi
    done
}

bootstrap_delete_user() {
    local _users=$* user= ret=
    bootstrap_print ">>>> Delete Users: $_users" "black"
    for user in $_users
    do
        ret=$(\awk -F':' "/$user:/ {print \$1}" /etc/passwd)
        if [ ! -z "$ret" ]; then
            bootstrap_print "[$user] DELETE: OK" "white"
            \userdel -f -r $user
        fi
    done
}

bootstrap_delete_group() {
    local _groups=$* group= ret=
    bootstrap_print ">>>> Delete Groups: $_groups" "black"
    for group in $_groups
    do
        ret=$(\awk -F':' "/$group:/ {print \$1}" /etc/group)
        if [ ! -z "$ret" ]; then
            bootstrap_print "[$group] DELETE: OK" "white"
            \groupdel $group
        fi
    done
}

bootstrap_add_member() {
    local _group=$1; shift 1
    local _users=$* user=
    for user in $_users
    do
        groupmems -g $_group -a $user >& /dev/null
    done
}

bootstrap_install() {
    local _install_options=$1
    local _entry_dest=$2
    local _stat_path=$3
    \install $_install_options $_entry_dest $_stat_path
    G_RET_VAL=$?
    _bootstrap_set_ret_str

    return $G_RET_VAL 
}

bootstrap_progress() {
    local _limit=$1
    local xs=( '/' '-' '|' )
    local xc=${#xs[@]}
    local x=

    for ((i=1; i <= _limit; i++))
    do
        usleep 100000
        x=$((i%xc))
        echo -n "[${xs[$x]}]"
        printf "\b\b\b"
    done
}

bootstrap_set_lang() {
    local _lang=$1
    [ -z "$_lang" ] && _lang=${sktx_default_lang:-"ko_KR.UTF-8"}
    _bootstrap_fputs "/etc/sysconfig/i18n" "LANG=$_lang\n"
    _bootstrap_fputs "/etc/sysconfig/i18n" "SYSFONT=latarcyrheb-sun16\n" "a"
}

_bootstrap_set_ret_str() {
    _str=$1
    [ -z "$_str" ] && _str="o:x"
    local _left=${_str//:*/}
    local _right=${_str//*:/}
    [ "$G_RET_VAL" == "0" ] && G_RET_STR="$_left" || G_RET_STR="$_right"
}

_bootstrap_check_cache() {
    # CACHE: G_RET_VAL=0
    # EXPIRE: G_RET_VAL=1
    local _file=$1

    if [ -z "${sktx_cache_flag:-}" ]; then
        G_RET_VAL=1
        return $G_RET_VAL
    fi

    if [ ! -e "$_file" ]; then
        G_RET_VAL=1
        return $G_RET_VAL
    fi

    local _stat_modify_sec=$(\stat -c %Y $_file)
    local _nsec=$(date +'%s')
    local _sec_diff=$((_nsec - _stat_modify_sec))

    [ "$_sec_diff" -gt "$sktx_cache_expire" ] && G_RET_VAL=1 || G_RET_VAL=0

    return $G_RET_VAL 
}

_bootstrap_get() {
    local _src=$1
    local _dst=$2
    local _str="o:x"
    local _cache_expire=

    _bootstrap_check_cache $_dst
    _cache_expire=$G_RET_VAL

    if [ "$_cache_expire" == "1" ]; then
         _bootstrap_curl $_dst $_src
         _str=$_str
        G_RET_CAC=1
    else
        _str="c:x"
        G_RET_CAC=0
    fi

    _bootstrap_set_ret_str "$_str"
    bootstrap_print "[$G_RET_STR] $_src" "white"
    return $G_RET_VAL 
}

_bootstrap_replace() {
    local _from_str=$1
    local _to_str=$2
    local _file=$3

    _from_str=${_from_str//\//\\/};
    _to_str=${_to_str//\//\\/};
    perl -p -i -e "s/$_from_str/$_to_str/g" "$_file";
}

_bootstrap_curl() {
    local _dst=$1
    local _src=$2
    \curl ${sktx_curl_options:-} -o $_dst $_src
    G_RET_VAL=$?
    return $G_RET_VAL 
}

_bootstrap_fputs() {
    local _dst=$1
    local _str=$2
    local _opt=$3
    [ "$_opt" == "a" ] && printf "$_str" >> $_dst || printf "$_str" > $_dst
    G_RET_VAL=$?
    return $G_RET_VAL 
}

_bootstrap_mkdir() {
    local _dest=$*
    [ ! -e "$_dest" ] && \mkdir -p ${_dest}
    G_RET_VAL=$?
    return $G_RET_VAL 
}

_bootstrap_remove() {
    local _dest=$1
    [ -e "$_dest" ] && \rm -rf "$_dest"
    G_RET_VAL=$?
    return $G_RET_VAL 
}

_bootstrap_move() {
    local _src=$1
    local _dst=$2
    [ -e "$_src" ] && \mv -f "$_src" "$_dst"
    G_RET_VAL=$?
    return $G_RET_VAL 
}

_bootstrap_copy() {
    local _src=$1
    local _dst=$2
    [ -e "$_src" ] && \cp -af "$_src" "$_dst"
    G_RET_VAL=$?
    return $G_RET_VAL 
}

_bootstrap_link() {
    local _src=$1
    local _dst=$2
    [ -e "$_src" ] && \ln -sf "$_src" "$_dst"
    G_RET_VAL=$?
    return $G_RET_VAL 
}

_bootstrap_grep() {
    local _str=$1
    local _dst=$2
    [ -e "$_dst" ] && \grep "$_str" $_dst >& /dev/null
    G_RET_VAL=$?
    return $G_RET_VAL 
}

_bootstrap_diff() {
    \diff $1 $2 >& /dev/null
    G_RET_VAL=$?
    return $G_RET_VAL 
}

_bootstrap_backup_file() {
    local _template=$1 
    local _stat_path=$2
    local _template_root= _repository_path= _entry_path= _entry_dest= _ntime= _install_mode= _install_options=
    local repofile=

    [ -z "$_template" ] && return 1 

    _template_root="${sktx_deploy_root:-}/${_template}"

    _repository_path="${sktx_manager_root:-}/backup"

    [ ! -e "$_repository_path" ] && _bootstrap_mkdir ${_repository_path}
            
    _entry_path="${_template_root}/files"
    _entry_dest="${_entry_path}/${stat_node}${_stat_path}"

    ntime=$(date +'%Y%m%d%H%M%S')

    [ ! -f "$_entry_dest" ] && return 1

    _install_mode=${sktx_default_mode:-}
    [ -n "$_install_mode" ] && _install_options="-m $_install_mode"
    
    _bootstrap_diff $_entry_dest $_stat_path

    if [ "$G_RET_VAL" == "1" ]; then
        repofile=${_stat_path//\//_}
        bootstrap_install "$_install_options" "$_stat_path" "$_repository_path/${repofile}.${ntime}"
        bootstrap_print "[$G_RET_STR] $_repository_path/${repofile}.${ntime}" "yellow"
    fi

    return $G_RET_VAL 
}

_bootstrap_load_config() {
    local _files_path=$1
    local _glue=$2
    local _desp="\n"
    _glue=${_glue:-${_desp}}
    \awk "{
            gsub(/\"/, \"\");
            gsub(/(^[[:space:]]*|[[:space:]]*\$)/, \"\");
            gsub(/[[:space:]]*=[[:space:]]*/, \"=\");
            gsub(/[[:space:]]/, \"[[:space:]]\");
            if(/^[^#[:space:]].*/) {
                printf \$0\"${_glue}\";
            }
    }" $_files_path
}

_bootstrap_hash_insert() {
    local name=$1 key=$2 val=$3
    eval __hash_${name}_${key}=\"$val\"
}

_bootstrap_hash_select() {
    local name=$1 key=$2
    local var=__hash_${name}_${key}
    G_HASH_VAL=${!var}
    echo -n "$G_HASH_VAL"
}

# Read in program's configuration
bootstrap_set_global_config

# Install common command
bootstrap_install_global_dependency

# vi:set ft=sh ts=4 sw=4 et fdm=marker:
