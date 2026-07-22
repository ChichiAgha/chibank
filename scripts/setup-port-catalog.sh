#!/usr/bin/env bash
set -euo pipefail

: "${PORT_CLIENT_ID:?PORT_CLIENT_ID is required}"
: "${PORT_CLIENT_SECRET:?PORT_CLIENT_SECRET is required}"

PORT_API_URL="${PORT_API_URL:-https://api.port.io}"

access_token="$({
  curl --fail-with-body --silent --show-error \
    --request POST \
    --header 'Content-Type: application/json' \
    --data "$(jq -cn --arg id "$PORT_CLIENT_ID" --arg secret "$PORT_CLIENT_SECRET" '{clientId:$id,clientSecret:$secret}')" \
    "$PORT_API_URL/v1/auth/access_token"
} | jq -er '.accessToken')"

auth_header="Authorization: Bearer $access_token"

upsert_blueprint() {
  local blueprint="$1"
  local identifier
  local status
  identifier="$(jq -r '.identifier' <<<"$blueprint")"
  status="$(curl --silent --output /dev/null --write-out '%{http_code}' --header "$auth_header" "$PORT_API_URL/v1/blueprints/$identifier")"

  if [[ "$status" == "200" ]]; then
    curl --fail-with-body --silent --show-error \
      --request PATCH \
      --header "$auth_header" \
      --header 'Content-Type: application/json' \
      --data "$blueprint" \
      "$PORT_API_URL/v1/blueprints/$identifier" >/dev/null
    echo "Updated blueprint: $identifier"
  elif [[ "$status" == "404" ]]; then
    curl --fail-with-body --silent --show-error \
      --request POST \
      --header "$auth_header" \
      --header 'Content-Type: application/json' \
      --data "$blueprint" \
      "$PORT_API_URL/v1/blueprints" >/dev/null
    echo "Created blueprint: $identifier"
  else
    echo "Unable to inspect blueprint $identifier (HTTP $status)" >&2
    return 1
  fi
}

upsert_entity() {
  local entity="$1"
  local blueprint
  local identifier
  local payload
  blueprint="$(jq -r '.blueprint' <<<"$entity")"
  identifier="$(jq -r '.identifier' <<<"$entity")"
  payload="$(jq 'del(.blueprint)' <<<"$entity")"

  curl --fail-with-body --silent --show-error \
    --request POST \
    --header "$auth_header" \
    --header 'Content-Type: application/json' \
    --data "$payload" \
    "$PORT_API_URL/v1/blueprints/$blueprint/entities?upsert=true" >/dev/null
  echo "Upserted entity: $blueprint/$identifier"
}

while IFS= read -r blueprint; do
  upsert_blueprint "$blueprint"
done < <(jq -c '.[]' port/catalog/blueprints.json)

while IFS= read -r entity; do
  upsert_entity "$entity"
done < <(jq -c '.[]' port/catalog/entities.json)

echo "Port catalog setup completed successfully."
