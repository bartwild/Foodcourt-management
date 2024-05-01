#!/bin/bash
set -e
set -x

function info() {
	# echo -e "\033[0;32m[INFO] $1\033[0m"
	echo "$1"
}

function error() {
	# echo -e "\033[0;31m[ERROR] $1\033[0m"
	echo "$1"
}

function create_rules() {
	local RG=$1
	local GROUP_NAME=$2
	shift 2
	for RULE in "$@"; do
		RULE_NAME=$(./yq '.name' <<<"$RULE")
		RULE_PRIORITY=$(./yq '.priority' <<<"$RULE")
		RULE_SOURCE_ADDRESS_PREFIXES=$(./yq '.source_address_prefixes' <<<"$RULE")
		RULE_SOURCE_PORT_RANGES=$(./yq '.source_port_ranges' <<<"$RULE")
		RULE_DESTINATION_ADDRESS_PREFIXES=$(./yq '.destination_address_prefixes' <<<"$RULE")
		RULE_DESTINATION_PORT_RANGES=$(./yq '.destination_port_ranges' <<<"$RULE")

		info ">>>>CREATING RULE $RULE_NAME"

		$az network nsg rule create \
			--resource-group "$RG" \
			--nsg-name "$GROUP_NAME" \
			--name "$RULE_NAME" \
			--access allow \
			--protocol Tcp \
			--priority "$RULE_PRIORITY" \
			--source-address-prefix "$RULE_SOURCE_ADDRESS_PREFIXES" \
			--source-port-range "$RULE_SOURCE_PORT_RANGES" \
			--destination-address-prefix "$RULE_DESTINATION_ADDRESS_PREFIXES" \
			--destination-port-range "$RULE_DESTINATION_PORT_RANGES"

	done
}

function create_vm() {
	local VM=$1
	local RG=$2
	local VNET_NAME=$3
	NAME=$(./yq '.name' <<<"$VM")
	IMAGE=$(./yq '.image' <<<"$VM")
	SIZE=$(./yq '.size' <<<"$VM")
	SUBNET=$(./yq '.subnet' <<<"$VM")
	PRIVATE_IP=$(./yq '.private_ip_address' <<<"$VM")
	PUBLIC_IP=$(./yq '.public_ip_address' <<<"$VM")
	if [ -z "$PUBLIC_IP" ]; then
		PUBLIC_IP=""
	fi

	if [ $(./yq '.spot' <<<"$VM") == "true" ]; then
		SPOT_SETTINGS=""
		SPOT_SETTINGS+="--priority "$(./yq '.priority' <<<"$VM")" "
		SPOT_SETTINGS+="--max-price "$(./yq '.max_price' <<<"$VM")" "
		SPOT_SETTINGS+="--eviction-policy "$(./yq '.eviction_policy' <<<"$VM")" "
	fi

	info ">>>CREATING VM $NAME"

	$az vm create \
		--resource-group "$RG" \
		--vnet-name "$VNET_NAME" \
		--name "$NAME" \
		--subnet "$SUBNET" \
		--nsg "" \
		--private-ip-address "$PRIVATE_IP" \
		--public-ip-address "$PUBLIC_IP" \
		--image "$IMAGE" \
		--size "$SIZE" \
		--generate-ssh-keys \
		$SPOT_SETTINGS
}

function deploy_service() {
	local SERVICE=$1
	local CONFIG=$2
	local RG=$3
	local PRELOADING=$4
	NAME=$(./yq '.name' <<<"$SERVICE")
	SCRIPT=$(./yq '.script' <<<"$SERVICE")
	VM=$(./yq '.vm' <<<"$SERVICE")
	PORT=$(./yq '.port' <<<"$SERVICE")
	info ">>DEPLOYING SERVICE $NAME"

	DATABASE_USER=$(./yq e '.services[] | select(.name == "database") | .user' <<<"$CONFIG")
	DATABASE_PASSWORD=$(./yq e '.services[] | select(.name == "database") | .password' <<<"$CONFIG")

	case $NAME in
	database)
		PARAMS=("$PORT" "$DATABASE_USER" "$DATABASE_PASSWORD")
		PRELOADING="0"
		;;
	app)
		DATABASE_PORT=$(./yq e '.services[] | select(.name == "database") | .port' <<<"$CONFIG")
		DATABASE_ADDRESS=$(./yq e ".virtual_machines[] | select(.name == \"$(./yq e '.services[] | select(.name == "database") | .vm' <<<"$CONFIG")\") | .private_ip_address" <<<"$CONFIG")
		PARAMS=("$DATABASE_ADDRESS" "$DATABASE_PORT" "$DATABASE_USER" "$DATABASE_PASSWORD" "$PORT")
		;;
	*)
		echo "INVALID SERVICE: $NAME"
		false
		;;
	esac
	if [ "$PRELOADING" == "1" ]; then
		PARAMS=("${PARAMS[0]}" "${PARAMS[1]}" "${PARAMS[2]}" "${PARAMS[3]}")
	fi
	$az vm run-command invoke \
		--resource-group "$RG" \
		--name "$VM" \
		--command-id RunShellScript \
		--scripts "@$SCRIPT" \
		--parameters "${PARAMS[@]}"
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

yq_read_array='./yq e -o=json -I=0'

CONFIG=$(./yq 'explode(.)' "$CONFIG_FILE")

RESOURCE_GROUP=$(./yq '.resource_group' <<<"$CONFIG")
info ">CREATING RESOURCE_GROUP $RESOURCE_GROUP"
LOCATION=$(./yq '.location' <<<"$CONFIG")
$az group create --name "$RESOURCE_GROUP" --location "$LOCATION"

NETWORK_ADDRESS_PREFIX=$(./yq '.network.address_prefix' <<<"$CONFIG")
VNET_NAME=$(./yq '.network.name' <<<"$CONFIG")

info ">>CREATING VIRTUAL NETWORK $VNET_NAME"

$az network vnet create \
	--name "$VNET_NAME" \
	--resource-group "$RESOURCE_GROUP" \
	--address-prefix "$NETWORK_ADDRESS_PREFIX"

readarray -t NETWORK_SECURITY_GROUPS < <($yq_read_array '.network_security_groups[]' <<<"$CONFIG")
info '>>CREATING NETWORK SECURITY GROUPS'

for GROUP in "${NETWORK_SECURITY_GROUPS[@]}"; do
	(
		GROUP_NAME=$(./yq '.name' <<<"$GROUP")
		info ">>>CREATING NETWORK SECURITY GROUP $GROUP_NAME"

		$az network nsg create \
			--resource-group "$RESOURCE_GROUP" \
			--name "$GROUP_NAME"

		readarray -t RULES < <($yq_read_array '.rules[]' <<<"$GROUP")
		create_rules "$RESOURCE_GROUP" "$GROUP_NAME" "${RULES[@]}"
	) &
done
info '>>> WAITING FOR ALL GROUPS TO BE CREATED'
wait
info '>>> ALL GROUPS CREATED'

info ">>CREATING NETWORK SUBNETS"
readarray -t SUBNETS < <($yq_read_array '.subnets[]' <<<"$CONFIG")

for SUBNET in "${SUBNETS[@]}"; do
	NAME=$(./yq '.name' <<<"$SUBNET")
	ADDRESS_PREFIX=$(./yq '.address_prefix' <<<"$SUBNET")
	NSG=$(./yq '.network_security_group' <<<"$SUBNET")

	info ">>>CREATING SUBNET $NAME"

	$az network vnet subnet create \
		--resource-group "$RESOURCE_GROUP" \
		--vnet-name "$VNET_NAME" \
		--name "$NAME" \
		--address-prefix "$ADDRESS_PREFIX" \
		--network-security-group "$NSG"
done

readarray -t PUBLIC_IPS < <($yq_read_array '.public_ips[]' <<<"$CONFIG")
info ">>CREATING PUBLIC IPS"

for IP in "${PUBLIC_IPS[@]}"; do
	NAME=$(./yq '.name' <<<"$IP")
	info ">>>CREATING PUBLIC IP $NAME"

	$az network public-ip create \
		--resource-group "$RESOURCE_GROUP" \
		--name "$NAME"
done

info ">>CREATING VIRTUAL MACHINES"
readarray -t VIRTUAL_MACHINES < <($yq_read_array '.virtual_machines[]' <<<"$CONFIG")

for VM in "${VIRTUAL_MACHINES[@]}"; do
	(
		create_vm "$VM" "$RESOURCE_GROUP" "$VNET_NAME"
	) &
done
info '>>> WAITING FOR ALL VIRTUAL_MACHINES TO BE CREATED'
wait
info '>>> ALL VIRTUAL_MACHINESS CREATED'

info ">>DEPLOYING SERVICES"
readarray -t SERVICES < <($yq_read_array '.services[]' <<<"$CONFIG")

for SERVICE in "${SERVICES[@]}"; do
	deploy_service "$SERVICE" "$CONFIG" "$RESOURCE_GROUP"
done

info ">>OPENING IPS"

for IP in "${PUBLIC_IPS[@]}"; do
	NAME=$(./yq '.name' <<<"$IP")
	info ">>>OPENING IP $NAME"

	$az network public-ip show \
		--resource-group "$RESOURCE_GROUP" \
		--name "$NAME" \
		--query "ipAddress" \
		--output tsv
done
