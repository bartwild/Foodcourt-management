#!/bin/bash

set -e
set -x

function info() {
	echo -e "\033[0;32m[INFO] $1\033[0m"
}

function error() {
	echo -e "\033[0;31m[ERROR] $1\033[0m"
}

az=az
: "${DRY_RUN:=0}"
[ "$DRY_RUN" == "1" ] && az='echo az'

if [ $# -lt 1 ]; then
	error "CONFIG_FILE not specified - aborting"
	exit 22 # EINVAL
fi

CONFIG_FILE="$1"
if [ ! -f "$CONFIG_FILE" ]; then
	error "CONFIG_FILE does not exist - aborting"
	exit 2 # ENOENT
fi

CONFIG=$(./yq 'explode(.)' "$CONFIG_FILE")
RESOURCE_GROUP=$(./yq '.resource_group' <<<"$CONFIG")

info ">UNDEPLOYING"

$az group delete --name "$RESOURCE_GROUP" --yes --verbose

info "<UNDEPLOYING DONE"
