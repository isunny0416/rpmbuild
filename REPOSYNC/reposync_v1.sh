#!/bin/sh

LOG6="`pwd`/reposync6.log"
LOG73="`pwd`/reposync73.log"
LOG74="`pwd`/reposync74.log"
BASEDIR6="/data/repo/os/centos/6.9/"
BASEDIR73="/data/repo/os/centos/7.3.1611/"
BASEDIR74="/data/repo/os/centos/7.4.1708/"

## CentOS 6 ##
SDATE=`date "+%Y-%m-%d %H:%M:%S"`
echo "### SYNC START $SDATE" >> $LOG6
#rsync -avzH --stats --numeric-ids --delete --delete-during --delay-updates --ignore-errors --exclude "*i386*" --exclude "*i686*" --exclude "*drpm*" --exclude "*isos*" --exclude "*xen4*" rsync://ftp.riken.jp/centos/6.6/ /home/pkgrepos/centos/6.6/ &>> $LOG

rsync -avzH --stats --numeric-ids --delete --delete-during --delay-updates --ignore-errors --exclude "*i386*" --exclude "*i686*" --exclude "*drpm*" --exclude "*isos*" --exclude "xen4*" --exclude "virt*" --exclude "cloud*" --exclude "storage*" rsync://ftp.riken.jp/centos/6.9/ $BASEDIR6 &>> $LOG6

EDATE=`date "+%Y-%m-%d %H:%M:%S"`
echo "### SYNC DONE $EDATE" >> $LOG6

## CentOS7.3 ##

SDATE=`date "+%Y-%m-%d %H:%M:%S"`
echo "### SYNC START $SDATE" >> $LOG73

rsync -avzH --stats --numeric-ids --delete --delete-during --delay-updates --ignore-errors --exclude "*i386*" --exclude "*i686*" --exclude "*drpm*" --exclude "*isos*" --exclude "xen4*" --exclude "cloud*" --exclude "atomic*" --exclude "paas*" --exclude "storage*" rsync://ftp.riken.jp/centos/7.3.1611/ $BASEDIR73 &>> $LOG73

EDATE=`date "+%Y-%m-%d %H:%M:%S"`
echo "### SYNC DONE $EDATE" >> $LOG73

## CentOS7.4 ##

SDATE=`date "+%Y-%m-%d %H:%M:%S"`
echo "### SYNC START $SDATE" >> $LOG74

rsync -avzH --stats --numeric-ids --delete --delete-during --delay-updates --ignore-errors --exclude "*i386*" --exclude "*i686*" --exclude "*drpm*" --exclude "*isos*" --exclude "xen4*" --exclude "cloud*" --exclude "atomic*" --exclude "paas*" --exclude "storage*" rsync://ftp.riken.jp/centos/7.4.1708/ $BASEDIR74 &>> $LOG74

EDATE=`date "+%Y-%m-%d %H:%M:%S"`
echo "### SYNC DONE $EDATE" >> $LOG74
