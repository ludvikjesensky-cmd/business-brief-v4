# Deep/Memory runner

The separate Runner v1 candidate merged in PR #17 is superseded by D032's
Bridge-authenticated execution tools. The consolidation retains existing runtime
functions and the zero-provider-call INDEXED replay optimization.

Use [DEEP_RUNNER.md](DEEP_RUNNER.md) and
[deep-runner.openapi.json](deep-runner.openapi.json) for the current contract,
Chat adapter, rollout/rollback and acceptance gates.

Do not deploy a separate runner listener, RUNNER_PRINCIPALS, port 8090 or
runner.businessbrief.cz from the earlier candidate. The existing Bridge owns
authentication, publication authorization, secrets and the public HTTP boundary.
The runner Dockerfile is now only a compatibility build alias for the same Bridge
image; the old runtime module exits with the current deployment instructions.
