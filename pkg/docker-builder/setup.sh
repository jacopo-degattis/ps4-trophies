#!/bin/bash

TOKEN="<GITHUB_TOKEN>"
API_URL="https://api.github.com/repos/OpenOrbis/OpenOrbis-PS4-Toolchain/actions/runs?per_page=1&branch=master&status=success"

function check_status_code() {
    if [ $1 -ne 0 ]; then
        echo "Error while fetching /actions/runs"
        exit 1
    fi
}

ARTIFACTS_URL=$(curl -s "$API_URL" | jq -r '.workflow_runs' | jq -cs '.[0][0]' | jq -r '.artifacts_url')

check_status_code $?

response=$(curl -s "$ARTIFACTS_URL")

check_status_code $?

target="toolchain-llvm-18"
latest_llvm_release=$(echo "$response" | jq -r --arg target "$target" \
    '.artifacts[] | select(.name == $target) | @json' | head -n 1)

if [ -z "$latest_llvm_release" ]; then
    echo "Error: no artifact found with name $target"
    exit 1
fi

archive_url=$(echo "$latest_llvm_release" | jq -r '.archive_download_url')
curl -L --progress-bar --output toolchain-llvm-18.zip --header "Authorization: Bearer $TOKEN" "$archive_url"

echo "Done."