# SecOpsAgentKit Skill Reference

Quick reference guide for creating and maintaining security operations skills.

## Frontmatter Quick Reference

### Required Fields

```yaml
---
name: skill-name                          # kebab-case, lowercase with hyphens
description: >                            # Multi-line, include "Use when" clause
  What the skill does and specific use cases.
  Use when: (1) First scenario, (2) Second scenario, (3) Third scenario
version: 0.1.0                            # Semantic versioning: MAJOR.MINOR.PATCH
maintainer: github-username               # Your GitHub username or email
category: appsec                          # One of the valid categories
tags: [sast, security, owasp]            # Array of searchable tags
frameworks: [OWASP, CWE, MITRE-ATT&CK]   # Referenced security frameworks
---
```

### Optional Fields

```yaml
dependencies:                             # External requirements
  python: ">=3.9"
  packages: [semgrep, bandit]
  tools: [docker, git]
references:                               # External documentation
  - https://owasp.org/Top10/
  - https://example.com/docs
```

## Valid Categories

- `appsec` - Application Security
- `devsecops` - DevSecOps & CI/CD Security
- `secsdlc` - Secure Software Development Lifecycle
- `threatmodel` - Threat Modeling & Risk Analysis
- `compliance` - Compliance & Security Auditing
- `incident-response` - Security Incident Response

## Common Security Frameworks

- `OWASP` - Open Web Application Security Project
- `CWE` - Common Weakness Enumeration
- `MITRE-ATT&CK` - Adversarial Tactics, Techniques & Common Knowledge
- `NIST` - National Institute of Standards and Technology
- `SOC2` - Service Organization Control 2
- `PCI-DSS` - Payment Card Industry Data Security Standard
- `GDPR` - General Data Protection Regulation
- `ISO27001` - Information Security Management
- `HIPAA` - Health Insurance Portability and Accountability Act

## Semantic Versioning Guide

### Version Format: MAJOR.MINOR.PATCH

**MAJOR** (1.0.0) - Breaking changes:
- Changed frontmatter structure
- Removed bundled resources
- Changed expected inputs/outputs
- Incompatible workflow changes

**MINOR** (0.1.0) - New features (backward-compatible):
- New bundled scripts or references
- Enhanced workflows
- Additional framework coverage
- New optional features

**PATCH** (0.0.1) - Bug fixes and docs:
- Fixed scripts
- Documentation updates
- Typo corrections
- Reference updates

### Version Lifecycle

- Start new skills at: `0.1.0`
- First stable release: `1.0.0`
- Breaking change: `1.0.0` → `2.0.0`
- New feature: `1.0.0` → `1.1.0`
- Bug fix: `1.0.0` → `1.0.1`

## Directory Structure

```
skills/<category>/<skill-name>/
├── SKILL.md                    # Required: Main skill file
├── scripts/                    # Optional: Executable code
│   ├── .gitkeep
│   └── analyzer.py
├── references/                 # Optional: Reference docs
│   ├── owasp_mapping.md
│   └── remediation_guide.md
└── assets/                     # Optional: Templates/configs
    ├── config_template.yaml
    └── report_template.md
```

## Skill Checklist

Before submitting:

- [ ] All required frontmatter fields present
- [ ] Description includes "Use when" clause
- [ ] Version follows semver (0.1.0 for new skills)
- [ ] Category is valid
- [ ] Tags are relevant and searchable
- [ ] Maintainer field updated (not placeholder)
- [ ] All scripts tested and executable
- [ ] No auxiliary files (README.md, CHANGELOG.md)
- [ ] References linked from SKILL.md
- [ ] Security considerations documented
- [ ] No credentials or sensitive data
- [ ] SKILL.md under 500 lines
- [ ] Validation script passes

## Common Patterns

### Security Considerations Section

```markdown
## Security Considerations

- **Sensitive Data Handling**: How to handle secrets, credentials, PII
- **Access Control**: Required permissions and authorization context
- **Audit Logging**: What should be logged for compliance
- **Compliance**: Relevant standards (SOC2, GDPR, PCI-DSS)
- **Safe Defaults**: Secure-by-default configurations
```

### Script Template

```python
#!/usr/bin/env python3
"""Brief description of what this script does."""

import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Description")
    parser.add_argument("input_file", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        # Implementation
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

### Reference Document Template

```markdown
# Reference Title

## Table of Contents
- [Section 1](#section-1)
- [Security Standards](#security-standards)

## Section 1
Detailed information...

## Security Standards
### OWASP Mapping
- A01: Broken Access Control
### CWE Mapping
- CWE-79: Cross-site Scripting
```

## Commands

### Initialize New Skill
```bash
./scripts/init_skill.sh <skill-name> <category>
```

### Validate Skill
```bash
./scripts/validate_skill.py skills/<category>/<skill-name>
```

### Test Script
```bash
chmod +x skills/<category>/<skill-name>/scripts/script.py
./skills/<category>/<skill-name>/scripts/script.py --help
```

## Progressive Disclosure Quick Reference

**Goal**: Keep SKILL.md under 500 lines by moving detailed content to `references/`

### When to Split Content

**Keep in SKILL.md**:
- Core workflows (top 3-5 use cases)
- Decision points and conditional logic
- Quick start guidance
- Essential security considerations

**Move to references/**:
- Content exceeding 100 lines
- Framework-specific details (OWASP/CWE mappings)
- Advanced user content only
- Lookup-oriented content (rule libraries)

### Three Patterns

1. **High-Level + References**: Core workflows in SKILL.md, details in references
2. **Domain-Specific**: Separate reference files per domain/language
3. **Conditional Details**: Basic content inline, advanced topics linked

### Key Rules

- ✅ Keep references **one level deep** from SKILL.md
- ✅ Add table of contents for references >100 lines
- ❌ No nested references (SKILL.md → ref → sub-ref)
- ❌ Don't explain what Claude already knows

## Workflow Patterns

### Workflow Checklist Template

```markdown
## Workflow Name

Progress:
[ ] 1. First step description
[ ] 2. Second step description
[ ] 3. Third step description
[ ] 4. Fourth step description

Work through each step systematically. Check off completed items.
```

**Use for**: Complex multi-step operations where progress tracking helps

### Conditional Workflow Template

```markdown
## Workflow Name

1. Analyze situation
   - If condition A → Action A / See reference-a.md
   - If condition B → Action B / See reference-b.md
   - If condition C → Action C / See reference-c.md

2. Apply appropriate pattern
3. Validate results
```

**Use for**: Decision-based workflows with branching logic

### Iterative Workflow Template

```markdown
## Workflow Name

For each item in scope:
1. Perform operation
2. Check result
3. Document finding

Continue until all items processed.
```

**Use for**: Operations repeated across multiple targets

## Degrees of Freedom

Match instruction strictness to operation fragility:

| Level | Type | When to Use | Example |
|-------|------|-------------|---------|
| **High** | Text instructions | Multiple valid approaches | "Analyze codebase for security anti-patterns" |
| **Medium** | Pseudocode + params | Preferred pattern with variation | "Run semgrep --config=auto, prioritize by severity" |
| **Low** | Specific scripts | Fragile operations needing consistency | "Run: ./scripts/validate.py config.json" |

**Tip**: Use scripts for low-freedom operations to ensure reliability

## Anti-Patterns

### Content Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Explain what Claude knows | Only include security-specific knowledge |
| Include dates (e.g., "As of 2024...") | Use timeless language ("current standards") |
| Use Windows paths (scripts\file.py) | Use forward slashes (scripts/file.py) |
| Verbose explanations | Concise, imperative instructions |

### Structural Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Nested references (SKILL → ref → sub-ref) | One level from SKILL.md |
| Create README.md, CHANGELOG.md | Only SKILL.md for docs |
| Exceed 500 lines in SKILL.md | Split to references/ |
| Offer 8+ options | Provide default + escape hatch |

### Workflow Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| "Analyze the code" (vague) | "Run semgrep --config=auto . --json" (specific) |
| "Parse JSON and extract CVEs" | "Run: ./scripts/extract_cves.py results.json" |
| Offer too many scan types | Provide default scan + link to advanced options |

## Testing & Evaluation

### Evaluation-First Process

1. Identify skill requirements
2. Create 3-5 realistic test scenarios
3. Establish baseline performance
4. Write minimal instructions to pass tests
5. Iterate based on observed behavior

### Good Test Scenarios

- **Realistic**: Based on actual security operations
- **Specific**: Clear inputs and expected outputs
- **Measurable**: Objective success criteria
- **Diverse**: Cover common patterns and edge cases

### Testing Checklist

- [ ] Test on 3-5 realistic security scenarios
- [ ] All scripts execute without errors
- [ ] References load correctly
- [ ] No placeholder text (TODO, FIXME)
- [ ] Workflows complete end-to-end
- [ ] Error conditions handled gracefully
- [ ] Validation script passes

### Claude A/B Development

- **Claude A (Expert)**: Review and refine skill documentation
- **Claude B (Agent)**: Use skill to perform actual work
- Iterate: Observe B's behavior → Return to A for improvements

## Resources

- [CONTRIBUTE.md](CONTRIBUTE.md) - Full contribution guidelines
- [Claude Code Skills Docs](https://docs.claude.com/en/docs/claude-code/skills)
- [skills/_template/](skills/_template/) - Template directory
