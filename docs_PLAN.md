# PM Stage

## Chosen idea
`ratelimit-hint` — a tiny Python library that converts HTTP rate-limit headers into a concrete retry delay.

## Why this idea
- Small enough for a polished one-run MVP.
- Useful across many API clients and SDKs.
- Easy to adopt: zero dependencies, single import, no framework lock-in.
- Solves a recurring annoyance: `Retry-After`, `RateLimit-Reset`, and `X-RateLimit-Reset` are inconsistent across APIs.

## MVP scope
- Parse `Retry-After` as integer seconds or HTTP-date.
- Parse `RateLimit-Reset` and `X-RateLimit-Reset`.
- Return a structured result with delay, source header, and computed retry timestamp.
- Optional `cap` and `floor` controls.
- Unit tests.
- English README.
- GitHub Actions CI.

## Explicit non-goals for v0.1.0
- Async sleep helpers.
- Framework-specific adapters.
- Provider-specific heuristics for every API vendor.
- Automatic HTTP client middleware.

## Release checklist
- [x] Pick stack and package idea.
- [x] Define MVP and non-goals.
- [x] Design public API and README outline.
- [x] Implement package.
- [x] Add tests.
- [x] Add CI workflow.
- [x] Write license.
- [x] Verify repository structure.
- [x] List limitations and runtime assumptions.
- [ ] Tag release on GitHub.
- [ ] Publish to PyPI.
