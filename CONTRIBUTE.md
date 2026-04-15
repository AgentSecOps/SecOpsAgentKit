# Contributing to SecOpsAgentKit

Thank you for contributing security operations skills to the community! This guide will help you create high-quality skills that follow best practices.

## Table of Contents

- [Quick Start](#quick-start)
- [Skill Requirements](#skill-requirements)
- [Skill Structure](#skill-structure)
- [Frontmatter Standards](#frontmatter-standards)
- [Semantic Versioning](#semantic-versioning)
- [Submission Process](#submission-process)
- [Quality Guidelines](#quality-guidelines)
- [Progressive Disclosure](#progressive-disclosure)
- [Workflow Patterns](#workflow-patterns)
- [Feedback Loops](#feedback-loops)
- [Evaluation & Testing](#evaluation--testing)
- [Anti-Patterns](#anti-patterns)

## Quick Start

1. **Use the template**: Copy `skills/_template/` as your starting point
2. **Initialize your skill**: Run `./scripts/init_skill.sh <skill-name> <category>`
3. **Follow the structure**: See [Skill Structure](#skill-structure) below
4. **Test thoroughly**: Validate your skill works in real security scenarios
5. **Submit a PR**: Open a pull request with the `[skill]` tag

## Skill Requirements

All skills MUST include:

### Required Files

- `SKILL.md` - Main skill file with YAML frontmatter and instructions
- Proper directory structure under `skills/<category>/<skill-name>/`

### Required Frontmatter Fields

```yaml
---
name: skill-name
description: >
  Comprehensive description including what the skill does and when to use it.
  Must include: (1) Primary functionality, (2) Specific use cases,
  (3) Security context
version: 0.1.0
maintainer: github-username
category: appsec|devsecops|secsdlc|threatmodel|compliance|incident-response
tags: [relevant, security, tags]
frameworks: [OWASP|CWE|MITRE-ATT&CK|NIST|SOC2]
---
```

## Skill Structure

### Directory Layout

```
skills/
├── _template/                    # Template for new skills (DO NOT MODIFY)
├── appsec/                       # Application Security skills
├── devsecops/                    # DevSecOps skills
├── secsdlc/                      # Secure SDLC skills
├── threatmodel/                  # Threat Modeling skills
├── compliance/                   # Compliance & Audit skills
└── incident-response/            # Incident Response skills

skills/<category>/<skill-name>/
├── SKILL.md                      # Required: Main skill file
├── scripts/                      # Optional: Executable scripts
│   └── tool_script.py
├── references/                   # Optional: Reference documentation
│   └── standards.md
└── assets/                       # Optional: Templates, configs, etc.
    └── template.yaml
```

### What Goes Where

**SKILL.md**: Core procedural knowledge and workflows. Keep concise (<500 lines).

**scripts/**: Executable code for deterministic, repeated operations
- Security scanning scripts
- Analysis tools
- Automation utilities
- **Must be tested before submission**

**references/**: Documentation loaded on-demand
- Security framework mappings (OWASP, CWE, MITRE ATT&CK)
- Tool documentation
- Detailed schemas or standards
- Remediation guides

**assets/**: Files used in output (not loaded into context)
- Configuration templates
- Policy templates
- Boilerplate secure code
- Report templates

## Frontmatter Standards

### Required Fields

#### `name` (string, required)
The skill identifier in kebab-case.
```yaml
name: sast-vulnerability-analyzer
```

#### `description` (string, required)
**This is critical** - it determines when Claude uses your skill. Must include:
- What the skill does
- When to use it (specific triggers)
- Security operations context

```yaml
description: >
  Static application security testing using Semgrep with OWASP and CWE mapping.
  Use when: (1) Analyzing code for security vulnerabilities, (2) Performing SAST
  scans in CI/CD, (3) Providing remediation guidance with security framework
  references, (4) Prioritizing findings by CVSS score and exploitability.
```

#### `version` (semver, required)
Semantic versioning: `MAJOR.MINOR.PATCH`
```yaml
version: 0.1.0
```

#### `maintainer` (string, required)
Your GitHub username or email.
```yaml
maintainer: github-username
```

#### `category` (string, required)
Primary security domain (choose one):
- `appsec` - Application Security
- `devsecops` - DevSecOps & CI/CD Security
- `secsdlc` - Secure Software Development Lifecycle
- `threatmodel` - Threat Modeling & Risk Analysis
- `compliance` - Compliance & Security Auditing
- `incident-response` - Security Incident Response

```yaml
category: appsec
```

#### `tags` (array, required)
Searchable tags for skill discovery:
```yaml
tags: [sast, semgrep, vulnerability-scanning, owasp, cwe]
```

#### `frameworks` (array, required if applicable)
Security frameworks referenced:
```yaml
frameworks: [OWASP, CWE, MITRE-ATT&CK, NIST, SOC2, PCI-DSS, GDPR]
```

### Optional Fields

#### `dependencies` (object, optional)
External tools or packages required:
```yaml
dependencies:
  python: ">=3.9"
  packages: [semgrep, bandit, safety]
  tools: [docker, git]
```

#### `references` (array, optional)
External documentation links:
```yaml
references:
  - https://owasp.org/Top10/
  - https://cwe.mitre.org/
  - https://semgrep.dev/docs/
```

## Semantic Versioning

Follow semantic versioning (`MAJOR.MINOR.PATCH`):

- **MAJOR** (1.0.0): Breaking changes to skill interface or workflow
  - Changed frontmatter structure
  - Removed or renamed bundled resources
  - Changed expected inputs/outputs

- **MINOR** (0.1.0): New features, backward-compatible
  - New bundled scripts or references
  - Enhanced workflows
  - Additional security framework coverage

- **PATCH** (0.0.1): Bug fixes, documentation updates
  - Fixed scripts
  - Corrected documentation
  - Updated references

**Starting version**: All new skills should start at `0.1.0`

**Version 1.0.0**: Only use when skill is battle-tested and stable

## Submission Process

### 1. Create Your Skill

```bash
# Option A: Use initialization script
./scripts/init_skill.sh my-skill-name appsec

# Option B: Manually copy template
cp -r skills/_template skills/appsec/my-skill-name
```

### 2. Implement & Test

- Fill in `SKILL.md` with clear, concise instructions
- Add any required scripts, references, or assets
- **Test all scripts** - they must execute without errors
- Validate against real security scenarios

### 3. Quality Checklist

Before submitting, ensure:

- [ ] Frontmatter has all required fields
- [ ] Description clearly explains when to use the skill
- [ ] Version follows semver (start with 0.1.0)
- [ ] Category matches skill's primary domain
- [ ] Tags are relevant and searchable
- [ ] All scripts are tested and working
- [ ] No README.md or extraneous documentation files
- [ ] References are properly linked from SKILL.md
- [ ] Security considerations are documented
- [ ] No sensitive data or credentials included
- [ ] **README.md has been updated** with your skill entry (see step 3.1 below)
- [ ] **marketplace.json has been updated** with your skill path

#### 3.1. Update README.md

Add your skill to the README.md under the appropriate category section using this format:

```markdown
- **[skill-name](skills/category/skill-name/SKILL.md)** - Brief description using [Tool Name](https://link-to-tool-docs) for what it does
```

**Example:**
```markdown
- **[sast-semgrep](skills/appsec/sast-semgrep/SKILL.md)** - Static application security testing using [Semgrep](https://semgrep.dev/docs/) for vulnerability detection
```

**Format requirements:**
- Skill name links to the SKILL.md file in this repository
- Brief description (one line, ~80-100 characters)
- Tool name is linked inline within the description (not at the end)
- Tool link points to the official tool repository or documentation (first URL in your SKILL.md frontmatter `references`)
- Maintain alphabetical order within the category section
- Ensure the entry matches your skill's `name` and primary `references[0]` from SKILL.md frontmatter

### 4. Submit Pull Request

```bash
git checkout -b skill/my-skill-name
git add skills/appsec/my-skill-name README.md .claude-plugin/marketplace.json
git commit -m "Add my-skill-name skill for [brief description]"
git push origin skill/my-skill-name
```

Open a PR with:
- **Title**: `[skill] Add <skill-name> - <brief description>`
- **Labels**: `skill`, category label (e.g., `appsec`)
- **Description**:
  - What the skill does
  - Security use cases it addresses
  - Testing performed
  - Any dependencies required

### 5. Review Process

Maintainers will review for:
- Code quality and security best practices
- Documentation completeness
- Testing coverage
- Adherence to standards
- Community value

## Quality Guidelines

### Writing Effective Skills

**Concise is Key**: The context window is shared. Only include what Claude doesn't already know.

**Imperative Form**: Use command form in instructions
- ✅ "Run the security scan"
- ❌ "You should run the security scan"

**Progressive Disclosure**: Organize content using progressive disclosure patterns (see [Progressive Disclosure](#progressive-disclosure) below)

**Security-First**:
- Document sensitive data handling
- Specify required permissions
- Include audit logging guidance
- Note compliance requirements

### Security Considerations

All skills must address:

1. **Sensitive Data**: How to handle secrets, credentials, PII
2. **Access Control**: Required permissions and authorization
3. **Audit Logging**: What should be logged for compliance
4. **Compliance**: Relevant standards (SOC2, GDPR, PCI-DSS)
5. **Safe Defaults**: Secure-by-default configurations

## Progressive Disclosure

Progressive disclosure is critical for managing Claude's context window efficiently. The context is shared across system prompts, conversation history, active skills, and user requests.

### The 500-Line Rule

**Keep SKILL.md under 500 lines**. When content exceeds this limit, move detailed information to `references/` and link to it from SKILL.md.

**Challenge every piece of information**: Ask "Does Claude really need this explanation?" Claude is already very smart - only include what Claude doesn't already know.

### Three Progressive Disclosure Patterns

#### Pattern 1: High-Level Guide with References

SKILL.md contains core workflows and common patterns. Detailed content lives in references.

**SKILL.md** (150 lines):
```markdown
## Core Workflow

1. Run initial scan
2. Analyze results
3. Generate report

For detailed configuration options, see [references/advanced-config.md](references/advanced-config.md)
For framework mappings, see [references/owasp-mappings.md](references/owasp-mappings.md)
```

**references/advanced-config.md** (300 lines):
- Entropy detection settings
- Custom rule patterns
- Allowlist configuration
- Performance tuning

#### Pattern 2: Domain-Specific Organization

When a skill covers multiple domains (e.g., multiple languages or frameworks), create separate reference files per domain.

**SKILL.md** (200 lines):
```markdown
## Language Support

Semgrep supports multiple languages. For language-specific patterns:
- [references/python-patterns.md](references/python-patterns.md)
- [references/javascript-patterns.md](references/javascript-patterns.md)
- [references/java-patterns.md](references/java-patterns.md)
```

#### Pattern 3: Conditional Details

Provide basic content inline, with links to advanced topics for expert users.

**SKILL.md** (250 lines):
```markdown
## Basic Scanning

Run a basic scan:
```bash
semgrep --config=auto .
```

**Advanced users**: For custom rulesets and CI/CD integration patterns, see [references/advanced-usage.md](references/advanced-usage.md)
```

### Reference File Organization

**For references >100 lines**: Include a table of contents at the top

```markdown
# Advanced Configuration Guide

## Table of Contents
- [Entropy Detection](#entropy-detection)
- [Custom Rules](#custom-rules)
- [Performance Tuning](#performance-tuning)
```

**Keep references one level deep**: Don't create nested reference structures. All reference files should link directly from SKILL.md.

❌ **Don't do**: SKILL.md → references/index.md → references/sub/details.md
✅ **Do**: SKILL.md → references/details.md

### When to Split Content

**Move to references/** when:
- Content exceeds 100 lines
- Details are framework-specific (detailed OWASP/CWE mappings)
- Information is for advanced users only
- Content is lookup-oriented (rule libraries, configuration options)

**Keep in SKILL.md** when:
- Core workflows everyone needs
- Decision points and conditional logic
- Common patterns (top 3-5 use cases)
- Quick start guidance

## Workflow Patterns

Workflows help Claude execute complex operations systematically. Break operations into clear, sequential steps.

### Workflow Checklist Pattern

Provide checkable checklists that Claude can copy and track progress:

```markdown
## Security Assessment Workflow

Research Progress:
[ ] 1. Identify application entry points
[ ] 2. Map authentication and authorization flows
[ ] 3. Identify data flows and sensitive data handling
[ ] 4. Review security controls
[ ] 5. Document findings with framework references
[ ] 6. Generate report with remediation priorities

Work through each step systematically. Check off completed items.
```

**Benefits**:
- Provides clear progress tracking
- Ensures no steps are skipped
- Works for both code-based and analysis tasks
- User can see what's completed and what's remaining

### Conditional Workflow Pattern

Guide Claude through decision points:

```markdown
## Vulnerability Remediation Workflow

1. Identify vulnerability type
   - If SQL injection → See [references/sqli-remediation.md](references/sqli-remediation.md)
   - If XSS → See [references/xss-remediation.md](references/xss-remediation.md)
   - If authentication flaw → See [references/auth-remediation.md](references/auth-remediation.md)

2. Assess severity (CVSS score)
   - If CVSS >= 7.0 → Priority: Critical
   - If CVSS 4.0-6.9 → Priority: High
   - If CVSS < 4.0 → Priority: Medium

3. Apply remediation pattern
4. Validate fix
5. Document changes
```

### Iterative Workflow Pattern

For operations requiring multiple iterations:

```markdown
## Code Security Review Workflow

For each file in scope:
1. Identify security-sensitive operations
2. Check against secure coding patterns
3. Flag potential vulnerabilities
4. Document finding with CWE reference
5. Suggest remediation

Continue until all files reviewed.
```

## Feedback Loops

Feedback loops dramatically improve output quality by enabling iterative refinement.

### The Validation Loop Pattern

**Run validator → Fix errors → Repeat**

```markdown
## Secure Configuration Validation

1. Generate security configuration
2. Run validation script: `./scripts/validate_config.py config.yaml`
3. Review validation output for errors and warnings
4. Fix identified issues
5. Repeat steps 2-4 until validation passes
6. Apply configuration
```

### Code Validation Example

For skills that generate code:

```markdown
## Secure Code Generation Workflow

1. Generate secure code implementation
2. Run security linters:
   ```bash
   bandit -r . -f json -o bandit-report.json
   semgrep --config=auto . --json
   ```
3. Review findings
4. Fix any security issues identified
5. Repeat steps 2-4 until no issues found
6. Run tests to verify functionality
```

### Configuration Validation Example

For skills that generate configurations:

```markdown
## CI/CD Security Configuration

1. Generate pipeline security configuration
2. Validate with validation script
3. Check for:
   - Secrets not in environment variables
   - Excessive permissions
   - Missing security scanning steps
   - Insecure dependencies
4. Fix issues and re-validate
5. Apply configuration once validation passes
```

**Benefits of feedback loops**:
- Catches errors early
- Improves quality systematically
- Reduces manual review burden
- Provides objective success criteria

## Evaluation & Testing

Create evaluations BEFORE extensive documentation. This evaluation-first approach identifies gaps and ensures skills work as intended.

### Evaluation-First Development Process

1. **Identify skill requirements**: What should the skill accomplish?
2. **Create test scenarios**: 3-5 realistic security scenarios
3. **Establish baseline**: Test current skill (or no skill) performance
4. **Write minimal instructions**: Just enough to pass evaluations
5. **Iterate**: Observe behavior, refine instructions, re-test

### Creating Test Scenarios

**Good test scenarios are**:
- **Realistic**: Based on actual security operations
- **Specific**: Clear inputs and expected outputs
- **Measurable**: Objective success criteria
- **Diverse**: Cover common patterns and edge cases

**Example test scenarios for SAST skill**:

```markdown
## Test Scenario 1: SQL Injection Detection
- Input: Python Flask app with SQL injection vulnerability
- Expected: Identify vulnerability, provide CWE-89 reference, suggest parameterized queries
- Success: Finding includes severity, OWASP reference, and code fix

## Test Scenario 2: XSS in React Component
- Input: React component with dangerouslySetInnerHTML
- Expected: Flag XSS risk (CWE-79), suggest DOMPurify or safer alternatives
- Success: Finding references OWASP A03:2021, provides secure example

## Test Scenario 3: Insecure Deserialization
- Input: Java code using ObjectInputStream with untrusted data
- Expected: Identify CWE-502, explain risks, suggest safer serialization
- Success: References MITRE ATT&CK T1027, provides remediation steps
```

### Testing Across Models

Test skills with multiple Claude models:
- **Haiku**: Fast, cost-effective operations
- **Sonnet**: Balanced performance for most tasks
- **Opus**: Complex analysis requiring deep reasoning

Different models may need different levels of detail. Aim for instructions that work well across all models.

### Iterative Development with Claude

**Claude A (Expert)**: Helps you refine the skill
**Claude B (Agent)**: Uses the skill to perform work

1. Ask Claude A to review and improve skill documentation
2. Test skill with Claude B on real scenarios
3. Observe Claude B's behavior and identify gaps
4. Return to Claude A with observations for improvements
5. Repeat until skill performs reliably

### Manual Testing Checklist

Before submission, test your skill:

- [ ] Runs successfully on 3-5 realistic scenarios
- [ ] All bundled scripts execute without errors
- [ ] References are accessible and load correctly
- [ ] No placeholder text (TODO, FIXME)
- [ ] Workflows complete end-to-end
- [ ] Error conditions handled gracefully
- [ ] Security considerations documented
- [ ] Validation passes: `./scripts/validate_skill.py skills/<category>/<skill-name>`

## Anti-Patterns

Avoid these common mistakes when creating skills:

### Content Anti-Patterns

❌ **Excessive verbosity**: Explaining concepts Claude already knows
```markdown
<!-- DON'T -->
Git is a version control system used by developers to track changes...

<!-- DO -->
Scan git history for exposed secrets using Gitleaks
```

❌ **Time-sensitive information**: Dates that will become outdated
```markdown
<!-- DON'T -->
As of 2024, the OWASP Top 10 includes...

<!-- DO -->
Map findings to current OWASP Top 10 categories
```

❌ **Windows-style paths**: Always use forward slashes
```markdown
<!-- DON'T -->
scripts\validate_config.py

<!-- DO -->
scripts/validate_config.py
```

### Structural Anti-Patterns

❌ **Deeply nested references**: Keep references one level from SKILL.md
```markdown
<!-- DON'T -->
SKILL.md → references/index.md → references/advanced/details.md

<!-- DO -->
SKILL.md → references/advanced-details.md
```

❌ **Auxiliary files**: Don't create extra documentation files
```markdown
<!-- DON'T -->
README.md, CHANGELOG.md, INSTALLATION.md

<!-- DO -->
Only SKILL.md for documentation
```

❌ **Exceeding line limits**: Keep SKILL.md under 500 lines
```markdown
<!-- DON'T -->
SKILL.md with 700 lines of content

<!-- DO -->
SKILL.md (350 lines) + references/advanced-topics.md (350 lines)
```

### Workflow Anti-Patterns

❌ **Offering too many options**: Provide default with escape hatch
```markdown
<!-- DON'T -->
Choose one of these 8 scanning approaches...

<!-- DO -->
Run standard scan with: semgrep --config=auto .
For custom configurations, see references/custom-scans.md
```

❌ **Vague workflows**: Be specific about steps
```markdown
<!-- DON'T -->
1. Analyze the code
2. Fix issues
3. Done

<!-- DO -->
1. Run SAST scan: semgrep --config=auto . --json
2. Review findings with CVSS >= 7.0
3. For each critical finding:
   - Identify root cause
   - Apply remediation pattern from references/
   - Validate fix with re-scan
4. Generate report with remaining findings
```

❌ **Punting to Claude**: Handle deterministic operations in scripts
```markdown
<!-- DON'T -->
"Parse the JSON output and extract CVE IDs"

<!-- DO -->
Run: ./scripts/extract_cves.py scan-results.json
```

### Degrees of Freedom

Match instruction strictness to operation fragility:

**High Freedom** (text instructions): Multiple valid approaches
- "Analyze the codebase for security anti-patterns"
- "Provide recommendations based on OWASP guidelines"

**Medium Freedom** (pseudocode with parameters): Preferred pattern with variation
- "Run semgrep with --config=auto, review findings, prioritize by severity"
- "Generate threat model covering STRIDE categories"

**Low Freedom** (specific scripts): Operations are fragile, consistency critical
- "Run: ./scripts/validate_policy.py policy.json"
- "Execute: docker run --rm -v $(pwd):/src returntocorp/semgrep:latest"

**Use scripts for low-freedom operations** to ensure reliability and consistency.

## Skill Maintenance

### Renaming a Skill

If you need to rename an existing skill, follow these steps to ensure all references are updated:

1. **Rename the directory**:
   ```bash
   mv skills/<category>/<old-name> skills/<category>/<new-name>
   ```

2. **Update SKILL.md frontmatter**:
   - Change the `name` field to match the new directory name
   - Update the `description` if needed to reflect the new name
   - Reorder `tags` if necessary (put most relevant tags first)

3. **Update README.md**:
   - Find the skill entry in the appropriate category section
   - Update the skill name in the markdown link
   - Update the file path: `skills/<category>/<new-name>/SKILL.md`
   - Ensure alphabetical ordering within the category

4. **Update marketplace.json**:
   - Locate the skill path in `.claude-plugin/marketplace.json`
   - Change `./<category>/<old-name>` to `./<category>/<new-name>`
   - Maintain alphabetical ordering within the plugin's skills array

5. **Validate the renamed skill**:
   ```bash
   python3 ./scripts/validate_skill.py skills/<category>/<new-name>
   ```

6. **Test the skill**: Verify that the skill loads correctly and functions as expected

**Example**:
```bash
# Rename sca-grype to container-grype
mv skills/devsecops/sca-grype skills/devsecops/container-grype

# Update SKILL.md frontmatter: name: container-grype
# Update README.md: [container-grype](skills/devsecops/container-grype/SKILL.md)
# Update marketplace.json: "./devsecops/container-grype"

python3 ./scripts/validate_skill.py skills/devsecops/container-grype
```

## Getting Help

- Read the [Claude Code Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)
- Check existing skills in the repository for examples
- Open a discussion for questions
- Review the `_template/` directory

## License

By contributing to this project, you agree that your contributions will be licensed under the same dual-license structure:

### For Documentation Contributions

All **documentation files** (markdown files, including `*.md` files, skill documentation, reference materials) you contribute will be licensed under:
- **[Creative Commons Attribution-ShareAlike 4.0 International (CC-BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)**

This allows others to freely use, share, and adapt your documentation with attribution, under the same license terms.

### For Code Contributions

All **code files** (Python scripts, Bash scripts, YAML configurations, and other executable or configuration code) you contribute will be dual-licensed under:
- **[CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)** AND
- **[Mozilla Public License 2.0 (MPL 2.0)](https://www.mozilla.org/en-US/MPL/2.0/)**

Users of your code can choose which license to use. The MPL 2.0 option allows your code to be combined with proprietary software while keeping the MPL-licensed files themselves open source.

### What This Means

- ✅ You retain copyright to your contributions
- ✅ Your work will be freely available to the security community
- ✅ Others must attribute you when using your contributions
- ✅ Documentation adaptations must remain open (ShareAlike)
- ✅ Code can be used flexibly under either license

### Full License Details

See [LICENSE.md](LICENSE.md) for complete license texts and detailed terms.