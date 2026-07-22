{{/* Common chart labels. */}}
{{- define "bleatbank.labels" -}}
app.kubernetes.io/part-of: techbleat-global-bank
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | quote }}
{{- end }}
