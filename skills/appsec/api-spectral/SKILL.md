---
name: api-spectral
description: >
  API specification linting and security validation using Stoplight's Spectral with support for
  OpenAPI, AsyncAPI, and Arazzo specifications. Validates API definitions against security best
  practices, OWASP API Security Top 10, and custom organizational standards. Use when: (1) Validating
  OpenAPI/AsyncAPI specifications for security issues and design flaws, (2) Enforcing API design
  standards and governance policies across API portfolios, (3) Creating custom security rules for
  API specifications in CI/CD pipelines, (4) Detecting authentication, authorization, and data
  exposure issues in API definitions, (5) Ensuring API specifications comply with organizational
  security standards and regulatory requirements.
version: 0.1.0
maintainer: SirAppSec
category: appsec
tags: [api-security, openapi, asyncapi, linting, spectral, api-governance, owasp-api, specification-validation]
frameworks: [OWASP]
dependencies:
  tools: [node, npm]
  optional: [docker, git]
references:
  - https://docs.stoplight.io/docs/spectral/674b27b261c3c-overview
  - https://github.com/stoplightio/spectral
  - https://owasp.org/API-Security/editions/2023/en/0x11-t10/
---

# API Security with Spectral

## Overview

Spectral is a flexible JSON/YAML linter from Stoplight that validates API specifications against
security best practices and organizational standards. With built-in rulesets for OpenAPI v2/v3.x,
AsyncAPI v2.x, and Arazzo v1.0, Spectral identifies security vulnerabilities, design flaws,
and compliance issues during the API design phase. Custom rulesets enforce OWASP API Security
Top 10 patterns, authentication standards, and data protection requirements.

## Quick Start

```bash
# Install via npm
npm install -g @stoplight/spectral-cli

# Or using Docker
docker pull stoplight/spectral

# Lint OpenAPI specification
spectral lint openapi.yaml

# Lint with specific ruleset, output as JSON
spectral lint openapi.yaml --ruleset .spectral.yaml --format json --output results.json
```

## Core Workflow

Progress:
[ ] 1. Install Spectral and select appropriate base rulesets
[ ] 2. Create or configure ruleset with security rules
[ ] 3. Run linting with appropriate severity thresholds
[ ] 4. Review findings and map to OWASP API Security Top 10
[ ] 5. Create custom rules for organization-specific security patterns
[ ] 6. Integrate into CI/CD pipeline with failure thresholds
[ ] 7. Generate reports with remediation guidance

Work through each step systematically. Check off completed items.

### Step 1: Ruleset Configuration

```yaml
# .spectral.yaml - Security-focused ruleset
extends: ["spectral:oas"]

rules:
  operation-security-defined: error       # All ops must have security (OWASP API1)
  info-contact: warn
  info-description: warn

  # HTTPS enforcement (OWASP API8)
  servers-use-https:
    severity: error
    given: $.servers[*].url
    then:
      function: pattern
      functionOptions:
        match: "^https://"
    message: "Server URL must use HTTPS (OWASP API8)"

  # API version required (OWASP API9)
  api-version-required:
    severity: error
    given: $.info
    then:
      field: version
      function: truthy
    message: "API version must be specified (OWASP API9)"

  # Prevent PII in query parameters
  no-pii-in-query:
    severity: error
    given: $.paths[*][*].parameters[?(@.in == 'query')].name
    then:
      function: pattern
      functionOptions:
        notMatch: "(ssn|social.?security|credit.?card|password|secret|token)"
    message: "Query parameters must not contain PII identifiers"
```

**Built-in Rulesets:**
- `spectral:oas` - OpenAPI v2/v3.x security and best practices
- `spectral:asyncapi` - AsyncAPI v2.x validation rules

For advanced ruleset patterns, see `references/ruleset_patterns.md`.

### Step 2: Security-Focused Linting

```bash
# Comprehensive security scan
spectral lint openapi.yaml --ruleset .spectral.yaml --format stylish --verbose

# Focus on critical issues only
spectral lint openapi.yaml --ruleset .spectral.yaml --fail-severity error

# Scan multiple specifications
spectral lint api-specs/*.yaml --ruleset .spectral.yaml

# Generate JSON report for CI/CD
spectral lint openapi.yaml --ruleset .spectral.yaml --format json --output findings.json
```

For complete OWASP API Security Top 10 rule mappings, see `references/owasp_api_mappings.md`.

### Step 3: CI/CD Pipeline Integration

**GitHub Actions:**
```yaml
name: API Security Linting
on: [push, pull_request]
jobs:
  spectral:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install Spectral
        run: npm install -g @stoplight/spectral-cli
      - name: Lint API Specifications
        run: |
          spectral lint api-specs/*.yaml \
            --ruleset .spectral.yaml \
            --format github-actions \
            --fail-severity error
      - name: Upload Report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: spectral-security-report
          path: spectral-report.json
```

**GitLab CI:**
```yaml
api-security-lint:
  stage: test
  image: node:18
  script:
    - npm install -g @stoplight/spectral-cli
    - spectral lint api-specs/*.yaml --ruleset .spectral.yaml --fail-severity error
```

### Step 4: Results Analysis and Remediation

1. Review all error-level findings (critical security issues)
2. Map findings to OWASP API Security Top 10 categories
3. Prioritize by severity and exploitability
4. Apply fixes to API specifications and re-lint to verify

**Pre-Commit Validation:**
```bash
# .git/hooks/pre-commit
SPECS=$(git diff --cached --name-only | grep -E '\.(yaml|yml|json)$' | grep -E '(openapi|swagger|api)')
if [ -n "$SPECS" ]; then
  for spec in $SPECS; do
    spectral lint "$spec" --ruleset .spectral.yaml --fail-severity error || exit 1
  done
fi
```

## Security Considerations

- **Specification Security**: API specs may contain sensitive internal URLs and auth schemes - control access
- **Rule Integrity**: Store ruleset files in version control with code review requirements
- **Secrets in Specs**: Never include actual credentials in example values - use placeholders only
- **False Positives**: Review findings in context before making security claims
- **Audit Logging**: Log all Spectral scans, findings, and remediation actions for compliance
- **Compliance Mapping**: Document how rules map to PCI-DSS, GDPR, HIPAA requirements
- **Governance Enforcement**: Define exception process for legitimate rule violations

## Bundled Resources

### Scripts (`scripts/`)

- `parse_spectral_results.py` - Parse JSON output and generate security reports with OWASP mapping
- `generate_remediation.py` - Generate remediation guidance from findings
- `compare_spectral_results.py` - Compare two scans to track remediation progress
- `aggregate_api_findings.py` - Aggregate findings across multiple API specifications
- `spectral_ci.sh` - CI/CD integration wrapper with exit code handling

### References (`references/`)

- `owasp_api_mappings.md` - Complete OWASP API Security Top 10 rule mappings
- `custom_rules_guide.md` - Custom rule authoring with examples
- `ruleset_patterns.md` - Reusable ruleset patterns for common security scenarios
- `api_security_checklist.md` - API security validation checklist

### Assets (`assets/`)

- `spectral-owasp.yaml` - Comprehensive OWASP API Security Top 10 ruleset
- `spectral-org-template.yaml` - Organization-wide API security standards template
- `github-actions-template.yml` - Complete GitHub Actions workflow
- `rule-templates/` - Reusable security rule templates

## Integration Points

- **CI/CD**: GitHub Actions, GitLab CI, Jenkins, CircleCI, Azure DevOps
- **IDE Integration**: VS Code extension, JetBrains plugins for real-time validation
- **Issue Tracking**: Jira, GitHub Issues (automated ticket creation for findings)
- **Security Platforms**: Defect Dojo, SIEM platforms (via JSON export)

## Troubleshooting

- **Too many false positives**: Use `overrides` in ruleset to exclude specific paths; start with `--fail-severity error`
- **Custom rules not working**: Verify JSONPath expressions; use `--verbose` to see which rules are applied
- **Performance issues**: Use `--ignore-paths` for large specs; split into modules
- **CI/CD failing**: Requires Node 14+; verify ruleset path relative to spec file

## References

- [Spectral Documentation](https://docs.stoplight.io/docs/spectral/674b27b261c3c-overview)
- [Spectral GitHub Repository](https://github.com/stoplightio/spectral)
- [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
