#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# TODO implement forge in this project
# echo "--------------------------- forged in Mount Etna ==> $SCRIPT_DIR ---------------------------"
# source $SCRIPT_DIR/forge/main.sh
# echo "--------------------------- forged in Mount Etna ==> $SCRIPT_DIR ---------------------------"

emergency() {
    set +x

    if [ "$1" == "STAGE" ];
    then
        ENV_ENDPOINT="https://localhost/emergency/"
    else
        ENV_ENDPOINT="http://localhost:8081/emergency/"
    fi

    curl -i -X POST -F "photo_fileupload_field=@/some_path/images/image_test_01.jpg" \
         -F "data_field=2024-10-04T12:37:45.983520-03:00" \
         -F "str_field=Test cUrl 01" \
         -F "str_empty_field=" \
         -F "int_field=0" \
         -F "bool_field=false" \
         -F "geom={\"type\": \"Point\", \"coordinates\": [-46.625290, -23.533773]}" \
         $ENV_ENDPOINT
}

post_json() {
	URL="$1"
	FILENAME="$2"
	DEBUG=${DEBUG:-0}
	if [[ "${DEBUG}" == "1" ]]; then
		echo "${URL} :: ${FILENAME}"
	fi
	curl -X POST $URL -H "Content-Type: application/json" -H "Accept: application/json" -d $FILENAME
}

health_check() {
	curl -i -H "Content-Type: application/json" -H "Accept: application/json" -X GET "http://localhost:8000/health_check"
}

auth() {
    set +x

    if [ "$1" == "NO_AUTH" ];
    then
        AUTH_HEADER=""
    elif [ "$1" == "INVALID_AUTH" ];
    then
        AUTH_HEADER="Authorization: INVALID $API_AUTHORIZATION_TOKEN WRONG"
    elif [ "$1" == "IGNORE_AUTH" ];
    then
        AUTH_HEADER="Authorization: IGNORED $API_AUTHORIZATION_TOKEN"
    elif [ "$1" == "ERR_AUTH" ];
    then
        AUTH_HEADER="Authorization: Api-Key MY_CUSTOM_FAKE_TOKEN"
    else
        AUTH_HEADER="Authorization: Api-Key $API_AUTHORIZATION_TOKEN"
    fi
    URL="$BASE_ENDPOINT/emergency/protected_test_custom_auth/"
    echo "$URL -- $AUTH_HEADER"

    curl -i -X GET $URL -H "$AUTH_HEADER"
}

# BASE_ENDPOINT="https://localhost"
BASE_ENDPOINT="http://eth0.kuna-mashiro.msr-c012.jeffersoncampos.eti.br"
URL_PORT="8080"
URL_PATH="api"
case $1 in
    "emergency") emergency $2;;
	"health_check")
		clear
		health_check
		echo ""
		date
		;;
    "inventory")
		URL_PORT="8082"
		URL_PATH="inventory/deduct"
		post_json "${BASE_ENDPOINT}:${URL_PORT}/${URL_PATH}" "tests/fixtures/inventory/deduct.json";;
	"order")
		URL_PORT="8083"
		URL_PATH="orders"
		post_json "${BASE_ENDPOINT}:${URL_PORT}/${URL_PATH}" "tests/fixtures/order/orders.json"
		;;
	"payment")
		URL_PORT="8081"
		URL_PATH="payments/process"
		post_json "${BASE_ENDPOINT}:${URL_PORT}/${URL_PATH}" "tests/fixtures/payment/process.json"
		;;
    "auth") auth $3;;
    *)
		echo "TODO implement forge in this project. $1 *NOT* found!!"
		# erupt $@
		;;
esac
