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
integrations="$(curl --fail-with-body --silent --show-error --header "$auth_header" "$PORT_API_URL/v1/integration")"
installation_id="$(
  jq -er '
    .integrations
    | map(select(
        (.integrationType // .type // "" | ascii_downcase | contains("github"))
        or (.installationId // "" | ascii_downcase | contains("github"))
      ))
    | first
    | .installationId
  ' <<<"$integrations"
)"

echo "Using GitHub Ocean installation: $installation_id"

upsert_action() {
  local action="$1"
  local identifier
  local payload
  local status
  identifier="$(jq -r '.identifier' <<<"$action")"
  payload="$(jq --arg installation "$installation_id" 'walk(if type == "string" and . == "__INSTALLATION_ID__" then $installation else . end)' <<<"$action")"
  status="$(curl --silent --output /dev/null --write-out '%{http_code}' --header "$auth_header" "$PORT_API_URL/v1/actions/$identifier")"

  if [[ "$status" == "200" ]]; then
    curl --fail-with-body --silent --show-error \
      --request PATCH \
      --header "$auth_header" \
      --header 'Content-Type: application/json' \
      --data "$payload" \
      "$PORT_API_URL/v1/actions/$identifier" >/dev/null
    echo "Updated self-service action: $identifier"
  elif [[ "$status" == "404" ]]; then
    curl --fail-with-body --silent --show-error \
      --request POST \
      --header "$auth_header" \
      --header 'Content-Type: application/json' \
      --data "$payload" \
      "$PORT_API_URL/v1/actions" >/dev/null
    echo "Created self-service action: $identifier"
  else
    echo "Unable to inspect action $identifier (HTTP $status)" >&2
    return 1
  fi
}

while IFS= read -r action; do
  upsert_action "$action"
done < <(jq -c '.[]' port/self-service/actions.json)

echo "Port self-service setup completed successfully."
