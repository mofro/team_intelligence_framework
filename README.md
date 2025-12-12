# Team Intelligence Framework v2.1

A collaborative AI team management system enabling multiple specialized personas to work together seamlessly. Personas are organized by domain, composed into teams, and governed by a two-layer architecture: universal framework principles plus domain/project-specific implementations.

## What This Framework Does

Transform AI assistance from individual expert consultation into **true collaborative team intelligence**:

- **🤝 Collaborative Teams**: Pre-configured expert teams that work together with defined deference patterns
- **🎯 Primary Voice System**: Unified responses incorporating multiple expertise areas
- **📦 Portable Schemas**: Personas and teams defined in self-describing JSON files
- **🔍 Domain-Organized**: Personas grouped by domain with activation triggers
- **⚡ Extensible**: Add new domains and personas following established patterns
- **📊 Transparent**: Behavioral rules and expertise scope defined in each schema

## Two-Layer Architecture

### Layer 1: Universal Framework (`/config/`)
Principles that apply across all domains and projects:

```
/config
├── domain_agnostic_framework.md           # Base operating principles
├── persona_activation_framework.md        # How personas discover and activate
├── persona_collaboration_framework_v1.md  # Collaboration patterns and primary voice
├── persona_interaction_architecture_v1.md # Addressing system (@persona_name)
└── measurement_framework.md               # Performance measurement principles
```

### Layer 2: Domains & Projects (`/personas/`)
Concrete implementations for specific domains:

```
/personas
├── /gaming                         # Gaming domain
│   ├── context_configuration.json  # Domain-level activation triggers
│   ├── /hero_heaven/               # Hero Heaven TTRPG project
│   │   ├── lore_keeper_persona_schema.json
│   │   ├── mythweaver_persona_schema.json
│   │   └── /teams/
│   │       └── hero_heaven_worldbuilding_team.json
│   └── ttrpg_game_architect_persona_schema.json
│
├── /development                    # Development domain  
│   ├── context_configuration.json
│   ├── experienced_developer_persona_schema.json
│   ├── react_specialist_persona_schema.json
│   ├── security_specialist_persona_schema_v1.json
│   ├── 10_foot_ui_designer_persona_schema_v1.1.json
│   ├── ott_ux_persona_schema_v1.1.json
│   ├── blits_developer_persona_schema_v1.json
│   ├── lightning_developer_persona_schema_v1.json
│   ├── cloud_architect_persona.json
│   ├── design_expert_persona_schema_v1.1.json
│   └── /teams/
│       └── react_fullstack_team.json
│
├── /financial                      # Financial domain
│   ├── context_configuration.json
│   ├── investment_advisor_schema.json
│   ├── tax_strategist_schema.json
│   ├── social_security_specialist_schema.json
│   ├── healthcare_expert_schema.json
│   ├── insurance_analyst_schema.json
│   ├── estate_planner_schema.json
│   └── /teams/
│       └── retirement_planning_team.json
│
└── /writing                        # Writing domain
    ├── context_configuration.json
    └── /screenplays/
        ├── screenwriter_persona_schema.json
        ├── dialog_coach_persona_schema.json
        ├── science_advisor_persona_schema.json
        └── dp_persona_schema.json

/PROJECT_MIGRATION_GUIDE.md         # Project-specific contexts and knowledge
```

## How Teams Activate

When you invoke `"activate retirement planning team"`:

1. **Framework loads** team definition from `/personas/financial/teams/retirement_planning_team.json`
2. **Team definition specifies** member personas (Investment Advisor, Tax Strategist, Social Security Specialist, Healthcare Expert, Insurance Analyst, Estate Planner)
3. **Framework loads each persona** schema with their expertise scope, behavioral rules, and deference patterns
4. **Universal rules from `/config/`** govern how they collaborate together
5. **Team activates** with all expertise immediately available

## Persona Schema Format (v1.2)

All personas use consistent structure:

```json
{
  "schema_version": "1.2",
  "metadata": {
    "name": "Security Specialist - Application Security Expert",
    "description": "Expert in secure coding and authentication systems",
    "author": "Mo",
    "version": "1.0",
    "created_date": "2025-06-23"
  },
  "persona": {
    "persona_name": "security_specialist",
    "display_name": "SecuritySpecialist",
    "custom_name": "Samantha Security",
    "role": "Application security expert",
    "expertise": ["token_security", "authentication", "secure_storage"]
  },
  "collaboration": {
    "expertise_scope": ["authentication_security", "api_security"],
    "defers_to": ["experienced_developer"],
    "approach_style": "analytical",
    "conflict_style": "evidence"
  },
  "behavioral_rules": [
    "Prioritize security while considering user experience impact",
    "Focus on authentication token lifecycle security",
    "Challenge security assumptions with evidence"
  ],
  "reference_context": "development",
  "reference_guide": "See documentation for operational protocols"
}
```

**Key fields**:
- `persona_name`: Snake_case identifier for addressing (@persona_name)
- `expertise_scope`: What this persona can advise on
- `defers_to`: Who has authority over this persona
- `behavioral_rules`: How this persona acts (8-15 imperative statements)
- `reference_context`: Domain this persona belongs to
- `reference_guide`: Pointer to operational documentation

## Team Definition Format

```json
{
  "team": {
    "team_name": "retirement_planning_team",
    "display_name": "Retirement Planning Team",
    "description": "Comprehensive retirement and financial planning",
    "members": [
      "investment_advisor",
      "tax_strategist",
      "social_security_specialist",
      "healthcare_expert",
      "insurance_analyst",
      "estate_planner"
    ],
    "context": "financial"
  },
  "collaboration": {
    "primary_voice": "investment_advisor",
    "decision_pattern": "consensus_with_hierarchy"
  }
}
```

## Quick Start

### Framework Activation
```
"personas on"                      # Activate the framework
"show my teams"                    # See available teams
"activate retirement planning team" # Start with pre-configured team
```

### Team Management
```
"add @security_specialist"         # Add individual expertise
"remove @persona_name"             # Remove from current team
"who's on my current team?"        # Check active roster
```

## Key Features

### Collaborative Intelligence
- **Unified Team Voice**: Single coherent response with multiple expertise areas
- **Seamless Handoffs**: Natural transitions between expertise boundaries
- **Deference Patterns**: Each persona knows when to defer to domain authorities
- **Optimistic Skepticism**: Personas challenge assumptions before solving

### Portable & Discoverable
- **Schema-Driven**: All personas and teams in discoverable JSON files
- **Domain-Organized**: Personas grouped by domain (gaming, development, financial, writing)
- **Composable**: Mix and match personas for custom teams
- **Self-Describing**: Behavioral rules and expertise in each schema

### Extensible
- **Add New Domains**: Create folder in `/personas/` with `context_configuration.json`
- **Add New Personas**: Create schema file following v1.2 structure
- **Add New Teams**: Define team composition in domain's `/teams/` folder
- **Custom Projects**: Use PROJECT_MIGRATION_GUIDE.md to document project-specific context

## Implementation

### Basic Setup
1. Load framework files from `/config/` for universal principles
2. Load domain folder (e.g., `/personas/development/`) for specific contexts
3. Activate team (e.g., `"activate react fullstack team"`)
4. Framework loads personas and applies collaboration patterns

### Custom Team Building
```
"create team api_team with @experienced_developer @security_specialist @cloud_architect"
```

### Performance Control
```
"show performance metrics"         # Monitor framework impact
"minimal persona mode"             # Reduce overhead for simple questions
"personas off"                     # Return to base LLM
```

## Project-Specific Context

Project-specific knowledge, goals, and constraints are documented in `PROJECT_MIGRATION_GUIDE.md`:

- **Gaming**: Hero Heaven TTRPG project context
- **Development**: Technology stack and team structure
- **Financial**: Retirement planning for Maurice and spouse
- **Writing**: Screenplay project context and creative requirements

See that guide for project-specific activation and knowledge repositories.

## Framework Philosophy

**Compartmental & Composable**: Personas are self-contained units that combine into teams.

**Explicit Deference**: Each persona knows what they're good at and when to defer.

**Transparent Behavior**: Operational patterns defined in schemas, not hidden in implementation.

**Extensible Design**: Add new domains and personas without modifying core framework.

---

**Transform your AI assistance from expert consultation to collaborative team intelligence.**
