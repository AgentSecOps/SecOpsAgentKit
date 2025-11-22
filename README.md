# SecOpsAgentKit

An assortment of security operations skills for AI coding agents. A collaborative approach to shift-left security using Claude Code skills.

## Overview

SecOpsAgentKit provides specialized Claude Code skills for security operations, covering:
- **Application Security (AppSec)**: SAST/DAST, vulnerability analysis, secure code review
- **DevSecOps**: CI/CD security, infrastructure as code security, container scanning
- **Secure SDLC**: Threat modeling, security requirements, secure design patterns
- **Compliance**: Security auditing, policy enforcement, compliance frameworks
- **Incident Response**: Security event analysis, forensics, remediation workflows

## Quick Start
```
/plugin marketplace add https://github.com/AgentSecOps/SecOpsAgentKit.git
```


## Available Skills

### Application Security (appsec/)

- **[api-mitmproxy](skills/appsec/api-mitmproxy/SKILL.md)** - Interactive HTTPS proxy for API security testing with [mitmproxy](https://mitmproxy.org/) traffic interception and modification
- **[api-spectral](skills/appsec/api-spectral/SKILL.md)** - API specification linting and security validation using [Spectral](https://docs.stoplight.io/docs/spectral) for OpenAPI and AsyncAPI
- **[dast-ffuf](skills/appsec/dast-ffuf/SKILL.md)** - Fast web fuzzer using [ffuf](https://github.com/ffuf/ffuf) for directory enumeration and parameter fuzzing
- **[dast-nuclei](skills/appsec/dast-nuclei/SKILL.md)** - Fast, template-based vulnerability scanning using ProjectDiscovery's [Nuclei](https://docs.projectdiscovery.io/tools/nuclei/overview)
- **[dast-zap](skills/appsec/dast-zap/SKILL.md)** - Dynamic application security testing using [OWASP ZAP](https://www.zaproxy.org/docs/) (Zed Attack Proxy)
- **[sast-bandit](skills/appsec/sast-bandit/SKILL.md)** - Python security vulnerability detection using [Bandit](https://github.com/PyCQA/bandit) SAST with CWE and OWASP mappings
- **[sast-semgrep](skills/appsec/sast-semgrep/SKILL.md)** - Static application security testing using [Semgrep](https://semgrep.dev/docs/) for vulnerability detection
- **[sca-blackduck](skills/appsec/sca-blackduck/SKILL.md)** - Software Composition Analysis using Synopsys [Black Duck](https://sig-product-docs.synopsys.com/bundle/bd-hub/page/Welcome.html) for dependency vulnerabilities and license compliance

### DevSecOps (devsecops/)

- **[container-grype](skills/devsecops/container-grype/SKILL.md)** - Container vulnerability scanning and dependency risk assessment using [Grype](https://github.com/anchore/grype) with CVSS, EPSS, and CISA KEV prioritization
- **[container-hadolint](skills/devsecops/container-hadolint/SKILL.md)** - Dockerfile security linting and best practice validation using [Hadolint](https://github.com/hadolint/hadolint)
- **[iac-checkov](skills/devsecops/iac-checkov/SKILL.md)** - Infrastructure as Code security scanning using [Checkov](https://www.checkov.io/) with 750+ built-in policies
- **[sca-trivy](skills/devsecops/sca-trivy/SKILL.md)** - Software Composition Analysis and container vulnerability scanning using [Trivy](https://aquasecurity.github.io/trivy/) for CVE detection
- **[secrets-gitleaks](skills/devsecops/secrets-gitleaks/SKILL.md)** - Hardcoded secret detection and prevention in git repositories using [Gitleaks](https://github.com/gitleaks/gitleaks)

### Secure SDLC (secsdlc/)

- **[reviewdog](skills/secsdlc/reviewdog/SKILL.md)** - Automated code review and security linting integration for CI/CD pipelines using [reviewdog](https://github.com/reviewdog/reviewdog)
- **[sast-horusec](skills/secsdlc/sast-horusec/SKILL.md)** - Multi-language static application security testing using [Horusec](https://github.com/ZupIT/horusec) (18+ languages, 20+ tools)
- **[sbom-syft](skills/secsdlc/sbom-syft/SKILL.md)** - Software Bill of Materials (SBOM) generation using [Syft](https://github.com/anchore/syft) for container images and filesystems

### Compliance (compliance/)

- **[policy-opa](skills/compliance/policy-opa/SKILL.md)** - Policy-as-code enforcement and compliance validation using [Open Policy Agent](https://www.openpolicyagent.org/docs/latest/) (OPA)

### Threat Modeling (threatmodel/)

- **[pytm](skills/threatmodel/pytm/SKILL.md)** - Python-based threat modeling using [pytm](https://github.com/izar/pytm) for STRIDE analysis and data flow diagrams

### Incident Response (incident-response/)

- **[detection-sigma](skills/incident-response/detection-sigma/SKILL.md)** - Generic detection rule creation and management using [Sigma](https://github.com/SigmaHQ/sigma) (universal SIEM rule format)
- **[forensics-osquery](skills/incident-response/forensics-osquery/SKILL.md)** - SQL-powered forensic investigation and system interrogation using [osquery](https://osquery.io/) for endpoint analysis
- **[ir-velociraptor](skills/incident-response/ir-velociraptor/SKILL.md)** - Endpoint visibility and digital forensics using [Velociraptor](https://docs.velociraptor.app/) for incident response at scale

### Offensive Security (offsec/)

- **[pentest-metasploit](skills/offsec/pentest-metasploit/SKILL.md)** - Penetration testing framework using [Metasploit](https://docs.metasploit.com/) for exploit development and vulnerability validation
- **[recon-nmap](skills/offsec/recon-nmap/SKILL.md)** - Network reconnaissance and security auditing using [Nmap](https://nmap.org/book/) for port scanning and service detection
- **[network-netcat](skills/offsec/network-netcat/SKILL.md)** - Network utility using [Netcat](https://nmap.org/ncat/guide/index.html) for reading/writing data across TCP/UDP connections and port scanning
- **[analysis-tshark](skills/offsec/analysis-tshark/SKILL.md)** - Network protocol analyzer and packet capture tool using [tshark](https://www.wireshark.org/docs/man-pages/tshark.html) for traffic analysis
- **[webapp-sqlmap](skills/offsec/webapp-sqlmap/SKILL.md)** - Automated SQL injection detection and exploitation using [SQLMap](https://sqlmap.org/) for web application security testing
- **[webapp-nikto](skills/offsec/webapp-nikto/SKILL.md)** - Web server vulnerability scanner using [Nikto](https://cirt.net/Nikto2) for identifying security issues and misconfigurations
- **[crack-hashcat](skills/offsec/crack-hashcat/SKILL.md)** - Advanced password recovery and hash cracking using [Hashcat](https://hashcat.net/wiki/) supporting multiple algorithms


## Security Frameworks

Skills in this repository reference industry-standard security frameworks:

- **OWASP** - Open Web Application Security Project
- **CWE** - Common Weakness Enumeration
- **MITRE ATT&CK** - Adversarial Tactics, Techniques & Common Knowledge
- **NIST** - National Institute of Standards and Technology
- **SOC2** - Service Organization Control 2
- **PCI-DSS** - Payment Card Industry Data Security Standard
- **GDPR** - General Data Protection Regulation

## Contributing

We welcome contributions! Please read [CONTRIBUTE.md](CONTRIBUTE.md) for:
- Skill creation guidelines
- Frontmatter standards
- Quality requirements
- Submission process

### Contributing a New Skill

To kickstart a new skill for this repo:
1. **Initialize**: Create a new skill from the template
   ```bash
   ./scripts/init_skill.sh my-skill-name appsec
   ```

2. **Develop**: Fill in `SKILL.md` and add bundled resources
   - `scripts/` - Executable security tools
   - `references/` - Security framework documentation
   - `assets/` - Templates and configurations

3. **Validate**: Run the validation script
   ```bash
   ./scripts/validate_skill.py skills/appsec/my-skill-name
   ```

4. **Update Documentation**:
   - Add your skill to the README.md (this file) under the appropriate category
   - Update `.claude-plugin/marketplace.json` with your skill path

5. **Submit**: Open a PR with the `[skill]` tag

See [CONTRIBUTE.md](CONTRIBUTE.md) for detailed guidelines including the exact format for README.md entries.

### Skill Standards

All skills follow these requirements:

#### Required Frontmatter

```yaml
---
name: skill-name                 # kebab-case identifier
description: >                   # Comprehensive description with use cases
  What the skill does and when to use it...
version: 0.1.0                   # Semantic versioning
maintainer: github-username      # Your GitHub username
category: appsec                 # Primary security domain
tags: [sast, owasp, security]   # Searchable tags
frameworks: [OWASP, CWE]        # Security frameworks referenced
---
```

#### Quality Standards

- **Concise**: Keep SKILL.md under 500 lines
- **Tested**: All scripts must be tested and working
- **Secure**: Include security considerations and safe defaults
- **Documented**: Clear instructions using imperative form
- **Versioned**: Follow semantic versioning (MAJOR.MINOR.PATCH)
### Tools & Scripts

- `scripts/init_skill.sh` - Initialize a new skill from template
- `scripts/validate_skill.py` - Validate skill structure and frontmatter
- `skills/_template/` - Base template for all new skills

## Resources

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Claude Code Skills Guide](https://docs.claude.com/en/docs/claude-code/skills)
- [OWASP Top 10](https://owasp.org/Top10/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [MITRE ATT&CK](https://attack.mitre.org/)

## License

This project uses dual licensing:

- **Documentation** (skills - markdown files): [Creative Commons Attribution-ShareAlike 4.0 International (CC-BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)
- **Code** (scripts, configurations): Dual-licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) and [Mozilla Public License 2.0 (MPL 2.0)](https://www.mozilla.org/en-US/MPL/2.0/)

This means:
- You can freely use, share, and adapt all content with attribution
- Skills must be shared under the same CC-BY-SA 4.0 license
- Code should be used under MPL 2.0

See [LICENSE.md](LICENSE.md) for full license texts and details.
