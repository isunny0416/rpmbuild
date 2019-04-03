rsync -avzH --stats --no-perms --numeric-ids --delete --delete-during --delay-updates --ignore-errors --exclude *i386* --exclude *i686* --exclude *drpm* --exclude *isos* --exclude xen4* --exclude cloud* --exclude atomic* --exclude centosplus* --exclude dotnet* --exclude paas* --exclude storage* --exclude config* rsync://ftp.kaist.ac.kr/CentOS/7/ /data/repo/os/centos/7/

rsync -avzH --stats --no-perms --numeric-ids --delete --delete-during --delay-updates --ignore-errors --exclude *i386* --exclude *i686* --exclude *drpm* --exclude *isos* rsync://dl.fedoraproject.org/pub/epel/7/x86_64/ /data/repo/os/epel/7/

