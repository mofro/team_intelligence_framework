# Expertise Domains Glossary

Reference of expertise domains extracted from persona deference structures. Domains emerge organically from actual persona implementations and will be refined and consolidated as the framework scales.

## Domains vs Specializations: Definitions & Philosophy

**DOMAIN** (Universal Pattern Area)
A broad area of knowledge that transcends specific technologies or frameworks. Domains are framework-agnostic and represent fundamental types of expertise that apply across multiple implementations.

Examples:
- "software_architecture" (applies to any system, language, framework)
- "application_security" (universal security principles)
- "design_strategy" (applies across all platforms)
- "infrastructure_deployment" (cloud or on-prem, any provider)

**SPECIALIZATION** (Framework/Technology-Specific Expertise)
Deep expertise in a specific technology, framework, or tool. Specializations exist within broader domains and represent how that domain is implemented using particular technologies.

Examples:
- "flutter_architecture" (specialization of cross-platform development)
- "lightning_blits_framework" (specialization of TV/OTT UI development)
- "lightning_core_framework" (specialization within Lightning framework)
- "react_framework_decisions" (specialization within frontend framework decisions)

**Why This Matters:**
- **Scaling**: If you hire a React Native expert later, they'd operate in a different specialization but the same broader domains (software_architecture, multi-platform_thinking, etc.)
- **Portability**: A persona's deference to "software_architecture" remains valid whether you use Flutter, React Native, or Xamarin
- **Clarity**: It distinguishes "this person knows Flutter specifically" from "this person understands multi-platform thinking generically"

**When to Create a New Domain vs a New Specialization:**
- New **domain**: When the problem area is fundamentally different from existing domains (e.g., "data_engineering" doesn't fit existing domains)
- New **specialization**: When you're adding a framework variant within an existing domain (e.g., "kotlin_native_architecture" is a specialization of framework implementation)

---

## Financial Domain

### Extracted Domains
| Expertise Domain | Primary Persona | Description | Scope |
|---|---|---|---|
| **tax_optimization** | tax_strategist (Trevor) | Tax-efficient withdrawal sequencing, Roth strategies, tax bracket management, IRMAA threshold coordination | Financial planning across retirement phases |
| **estate_planning** | estate_planner (Edmund) | Trust structures, beneficiary optimization, asset protection, wealth transfer strategy | Legal and financial asset protection |
| **portfolio_management** | investment_advisor (Isabella) | Portfolio allocation, sequence of returns risk, asset location optimization, rebalancing | Investment strategy and risk management |
| **healthcare_planning** | healthcare_expert (Heather) | Medicare planning, COBRA bridges, health insurance marketplace, healthcare cost estimation | Benefits and coverage during retirement |
| **retirement_benefits** | social_security_specialist (Samuel) | Social Security claiming strategies, spousal benefit optimization, break-even analysis | Government benefits optimization |
| **risk_management** | insurance_analyst (Ian) | Life insurance needs analysis, catastrophic risk evaluation, long-term care planning | Catastrophic risk protection |

### Deference Relationships (Financial)
- **investment_advisor** → tax_optimization
- **tax_strategist** → estate_planning
- **healthcare_expert** → tax_optimization
- **social_security_specialist** → tax_optimization
- **insurance_analyst** → estate_planning
- **estate_planner** → tax_optimization

---

## Development Domain

### Extracted Domains & Specializations
| Expertise Domain/Specialization | Primary Persona | Type | Description | Scope |
|---|---|---|---|---|
| **software_architecture** | experienced_developer (Dylan) | Domain | System design, architecture patterns, code quality, refactoring, testing, performance, maintainability, scalability | Universal across all development contexts |
| **flutter_architecture** | flutter_architect (Fiona) | Specialization | Flutter-specific multi-platform architecture, platform constraints, migration strategies, runtime integration | Flutter framework implementation |
| **frontend_framework_decisions** | react_specialist (Riley) | Domain | Component architecture, state management, performance optimization, framework assessment, build tooling | Frontend framework selection and patterns |
| **application_security** | security_specialist (Samantha) | Domain | Authentication, token management, secure storage, API security, secure coding, security testing | Security across all development platforms |
| **infrastructure_deployment** | cloud_architect (Cathy) | Domain | Cloud platforms, deployment strategy, infrastructure architecture, cost optimization, serverless design, monitoring | Infrastructure and deployment patterns |
| **lightning_blits_framework** | blits_developer (Johnny) | Specialization | Blits framework architecture, component patterns, rendering optimization, TV application patterns, performance | Lightning/Blits specific implementation |
| **lightning_core_framework** | lightning_developer (Lucy) | Specialization | Lightning v2 core concepts, node trees, textures, shaders, templates, rendering pipelines | Lightning v2 low-level framework |
| **design_strategy** | ux_ui_strategist (Dave) | Domain | Design direction, interaction systems, information architecture, content strategy, cross-platform consistency | Design principles across platforms |
| **tv_user_experience** | ux_designer (Uma) | Domain | TV/OTT UX design, 10-foot UI patterns, remote navigation, accessibility, usability testing | User experience for TV/OTT contexts |

### Deference Relationships (Development)
- **experienced_developer** → (no defers; top authority on software_architecture)
- **flutter_architect** → software_architecture
- **react_specialist** → software_architecture, design_strategy
- **security_specialist** → software_architecture
- **cloud_architect** → software_architecture, application_security
- **blits_developer** → software_architecture
- **lightning_developer** → lightning_blits_framework
- **ux_ui_strategist** → (no defers; independent authority on design_strategy)
- **ux_designer** → lightning_blits_framework

---

## Gaming Domain

*Pending refactoring*

---

## Writing Domain

*Pending refactoring*

---

## Notes

- Domains and specializations are extracted from actual `expertise_scope` and `defers_to` patterns in persona schemas
- Clear distinction between universal domains and framework-specific specializations prevents coupling to particular technologies
- This glossary will be updated as each domain is refactored
- Once all domains are refactored, consolidation analysis will inform refinement of domain definitions
- Two personas (Dave/ux_ui_strategist and Dylan/experienced_developer) have no defers_to, indicating independent authority in their primary domains
