# Infrastructure — Business Brief v4

**Status:** ACTIVE  
**Last consolidated:** 2026-10-22  
**Production runtime:** Hetzner + Caddy + Docker  
**Operational data:** Supabase  
**Railway:** removed from the critical production path

## 1. Current production topology

```text
Internet
  |
  +--> businessbrief.cz / www.businessbrief.cz
  |      |
  |      v
  |    Caddy on Hetzner
  |      |
  |      v
  |    static public web
  |    /var/www/businessbrief.cz
  |
  +--> bridge.businessbrief.cz
         |
         v
       Caddy on Hetzner
         |
         v
       127.0.0.1:8080
         |
         v
       business-brief-bridge Docker container
         |
         +--> Supabase PostgreSQL
         +--> Supabase Storage

Assembler
  |
  v
https://bridge.businessbrief.cz
  |
  v
Bridge -> Supabase
```

The Hetzner host is `tannenberg-prod-01`, public IPv4 `46.225.32.16`.

Supabase remains the authoritative operational/database/storage layer. Hetzner is the production compute and web runtime. Caddy terminates HTTPS and routes public traffic. Docker runs the Bridge and is the expected packaging boundary for backend runtime components.

## 2. Why Railway was removed

On 2026-10-22 the operator received a Railway security notification concerning the Variables area and the possibility that stored secrets could be compromised. The project therefore treated Railway-hosted secrets as exposed until rotated and moved the critical runtime away from Railway.

This was a security and control decision, not evidence that the Business Brief application itself was compromised.

Immediate consequences:

- rotate secrets that had been stored in Railway Variables;
- do not reuse the old Supabase secret after the incident;
- keep server secrets only in the Hetzner-side `.env` with restrictive permissions;
- remove Railway from the Bridge/Assembler production path;
- preserve old Railway deployment IDs only as historical provenance.

Railway may remain visible in historical documentation, old deployments or provenance. It is no longer the source of runtime truth for the current Bridge/Assembler path.

## 3. Hetzner server

Server:

```text
hostname: tannenberg-prod-01
IPv4:     46.225.32.16
OS:       Ubuntu 26.04.1 LTS
```

Primary operator account:

```text
tannenberg
```

Root login is not the normal operating path. The server uses SSH public-key authentication.

The operator's Mac uses a dedicated private SSH key for this host. Private SSH keys must never be committed to GitHub or copied into project repositories.

## 4. Server filesystem layout

Backend repository:

```text
/opt/business-brief-v4
```

Public web repository:

```text
/opt/business-brief-web-v2
```

Published public web root:

```text
/var/www/businessbrief.cz
```

Caddy configuration:

```text
/etc/caddy/Caddyfile
```

Backend production environment file:

```text
/opt/business-brief-v4/.env
```

The production `.env` must remain outside Git, mode 600, and must never be pasted into documentation.

## 5. Docker

Docker is installed and verified on the Hetzner host.

The Bridge image is built from the `business-brief-v4` repository and runs as:

```text
container: business-brief-bridge
image:     business-brief-bridge:local
bind:      127.0.0.1:8080 -> 8080/tcp
restart:   unless-stopped
```

The loopback bind is intentional. The Bridge is not exposed directly to the Internet; public access goes through Caddy over HTTPS.

The Assembler image is:

```text
business-brief-assembler:local
```

Assembler is explicit CLI execution and remains read-only unless `--persist` is supplied.

## 6. Caddy

Caddy runs as the systemd service `caddy.service`.

Current responsibilities:

### Bridge

```caddy
bridge.businessbrief.cz {
    reverse_proxy 127.0.0.1:8080 {
        header_up X-Forwarded-Proto https
    }
}
```

### Public website

```caddy
businessbrief.cz {
    root * /var/www/businessbrief.cz
    encode zstd gzip
    file_server
}

www.businessbrief.cz {
    redir https://businessbrief.cz{uri} permanent
}
```

Operational rule: always back up `/etc/caddy/Caddyfile`, run `caddy validate`, and only then reload the service.

## 7. DNS

DNS is managed at WEDOS.

Current relevant records:

```text
businessbrief.cz          A      46.225.32.16
bridge.businessbrief.cz   A      46.225.32.16
preview.businessbrief.cz  A      46.225.32.16
www.businessbrief.cz      CNAME  businessbrief.cz
```

The previous Railway/root ALIAS and old wildcard A/AAAA records were removed during the migration.

DNS propagation is external and may lag the WEDOS change. Verify with `dig` before treating a routing failure as an application failure.

## 8. Supabase

Supabase remains authoritative for operational PostgreSQL and Storage.

Server-side environment includes, at minimum, the variables required by the Bridge and Assembler, including:

```text
SUPABASE_URL
SUPABASE_SECRET_KEY
BRIDGE_DATABASE_URL
INGESTOR_BRIDGE_TOKEN
BRIDGE_PRINCIPALS
INGESTOR_BRIDGE_URL
```

No secret values belong in Git, Markdown, screenshots intended for publication, or public issue comments.

After the Railway Variables incident, the Supabase secret used by the new Hetzner runtime was rotated and placed in the Hetzner `.env`.

Database connectivity from Hetzner was tested. The first direct database attempt selected an unreachable IPv6 route; using the reachable Supabase pooler path resolved network reachability. An incorrect database password then produced the expected authentication failure; after correction, the database test returned `(1,)`.

## 9. Bridge authentication

The Bridge uses a dedicated bearer token and principal configuration.

Required behavior:

- the configured principal must contain `id`, `token`, `scopes`, and `publications`;
- the principal token must match `INGESTOR_BRIDGE_TOKEN`;
- the accepted token is not duplicated or concatenated;
- token values are never logged or committed.

The observed failure mode `CONFIGURATION_MISSING` was traced to an empty/mismatched principal token. After correction, the container remained `Up` and the authenticated readiness check passed.

Public health test:

```sh
curl -i \
  -H "Authorization: Bearer $TOKEN" \
  https://bridge.businessbrief.cz/ready
```

Accepted result:

```text
HTTP/2 200
{"contract_version":"ingestor-access-v1",...,"status":"READY"}
```

## 10. Assembler runtime and Q020 acceptance

The Assembler was built and executed on Hetzner against the accepted WSJ 2026-10-14 manifest.

Accepted source:

```text
source_id:
603e8242-ffe8-4e1d-a5de-9adb3da4d188

manifest_id:
wsj-2026-10-14-selection-r1

manifest_sha256:
f78c5339c3f4e406f78645a3c6e3fe3b8f53d89a3919ab6adad4c7e8f29a1d77
```

Read-only acceptance result:

```text
page_items:            27
article_records:       21
VERIFIED:              16
VERIFIED_WITH_NOTES:    5
NEEDS_REVIEW:           0
BLOCKED:                0
persistence.requested: false
eligible_count:        21
persisted_count:        0
```

The first `--persist` run created immutable Article Records and returned receipts with disposition `CREATED`.

The same `--persist` command was then replayed. The same records returned disposition `REPLAYED`, confirming idempotent same-key/same-bytes persistence rather than duplicate creation.

This closes the real-source Q020 acceptance for the accepted WSJ manifest on the Hetzner runtime.

## 11. Public website

The first public landing page lives in a separate private repository:

```text
ludvikjesensky-cmd/business-brief-web-v2
```

Initial GitHub commit:

```text
d53f60cec1b0180a2ef1af5bf3d97463c760006b
```

The site is deliberately simple:

- static HTML/CSS;
- no framework;
- no JavaScript requirement;
- no database;
- no secrets.

The Hetzner server has a read-only GitHub deploy key dedicated to this repository. The repository is cloned into `/opt/business-brief-web-v2`; only `public/` is published to `/var/www/businessbrief.cz`.

Both checks passed after deployment:

```text
https://businessbrief.cz/               -> 200
https://bridge.businessbrief.cz/ready   -> 200 with authorized token
```

## 12. GitHub deployment model

Backend and web are separate repositories.

Backend:

```text
ludvikjesensky-cmd/business-brief-v4
```

Public web:

```text
ludvikjesensky-cmd/business-brief-web-v2
```

The web repository uses a dedicated read-only deploy key on `tannenberg-prod-01`. Write access is intentionally disabled.

Current deployment is manual and explicit. A future automated GitHub-to-Hetzner deployment may be added, but no such automation should be assumed today.

## 13. Runtime source of truth

For current production questions use this order:

1. Hetzner process/service state:
   - `docker ps`
   - `docker logs`
   - `systemctl status caddy`
2. Public endpoint behavior:
   - `businessbrief.cz`
   - `bridge.businessbrief.cz/ready`
3. Supabase operational state and immutable artifacts.
4. GitHub repository state and exact commit identity.
5. Historical Railway deployments only when investigating provenance or old behavior.

Do not use an old Railway deployment as evidence of current production health.

## 14. Recovery and redeploy runbook

### Bridge

From `/opt/business-brief-v4`:

1. pull/checkout the intended reviewed commit;
2. rebuild the Bridge image;
3. verify the production `.env` exists and is mode 600;
4. recreate `business-brief-bridge` bound only to `127.0.0.1:8080`;
5. verify `docker ps`;
6. verify authenticated local `/ready`;
7. verify authenticated public `https://bridge.businessbrief.cz/ready`.

### Public web

From `/opt/business-brief-web-v2`:

1. `git pull` the intended `main` commit;
2. copy `public/.` into `/var/www/businessbrief.cz/`;
3. keep directories 755 and files 644;
4. validate Caddy if configuration changed;
5. reload Caddy only after successful validation;
6. verify `curl -I https://businessbrief.cz/`.

### Caddy

Before every configuration change:

```sh
sudo cp -a /etc/caddy/Caddyfile /etc/caddy/Caddyfile.backup-$(date -u +%Y%m%dT%H%M%SZ)
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
sudo systemctl status caddy --no-pager
```

Do not reload after a failed validation.

## 15. Railway historical boundary

The following statements are now historical only:

- Railway as the production compute/workspace layer;
- Bridge runtime health inferred from a Railway deployment;
- Railway Variables as the production secret store;
- Railway endpoint as `INGESTOR_BRIDGE_URL`.

The current Assembler configuration is:

```text
INGESTOR_BRIDGE_URL=https://bridge.businessbrief.cz
```

Old Railway pins/deployment IDs remain valuable provenance and must not be deleted from history, but they do not describe current production.

## 16. Security rules

- Never commit `.env`.
- Never commit private SSH keys.
- Never grant write access to a deploy key that only needs pull access.
- Bind internal HTTP services to loopback when Caddy is the public gateway.
- Rotate any secret that was present in a platform reported as potentially exposed.
- Do not reveal bearer tokens, Supabase secret keys or database passwords in logs or documentation.
- Treat GitHub repository access, SSH host access and Supabase credentials as separate trust boundaries.
