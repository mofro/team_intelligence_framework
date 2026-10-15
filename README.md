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
├── persona_collaboration_framework_v2.md  # Collaboration patterns and primary voice (synthesis phase)
├── persona_interaction_architecture_v1.md # Addressing system (@persona_name)
├── measurement_framework.md               # Performance measurement principles
├── challenge_synthesis_protocol.md        # Runtime-agnostic two-phase execution contract
└── challenge_phase_prompt.md              # Standalone Phase 1 (challenge) system prompt

/.claude/commands
├── challenge.md                           # /challenge slash command (Phase 1 reference impl)
└── synthesize.md                          # /synthesize slash command (Phase 2 reference impl)
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
├── /writing                        # Writing domain
│   ├── context_configuration.json
│   └── /screenplays/
│       ├── screenwriter_persona_schema.json
│       ├── dialog_coach_persona_schema.json
│       ├── science_advisor_persona_schema.json
│       └── dp_persona_schema.json
│
└── /ai_development                 # AI/LLM development domain
    ├── context_configuration.json
    ├── llm_prompt_specialist_persona_schema.json
    └── /teams/
        └── intelligence_framework_team.json
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

### Plugin: `/tif:catalog`

Install the plugin from a terminal (use the path to a clone of this repo, or `mofro/team_intelligence_framework`), then start a **new** Claude Code session in your project, because plugins load at session start:

```bash
claude plugin marketplace add /path/to/team_intelligence_framework
claude plugin install tif@team-intelligence-framework --scope project
```

<!-- tif:quickstart:start (generated by tif.py --sync; do not edit by hand) -->
```text
/tif:catalog help               Show this help
/tif:catalog list [--domain D]  List personas with role, domain and status
/tif:catalog teams              List teams with member count and status
/tif:catalog info <name>        Show details for one persona or team, by id or alias
/tif:catalog install <name>     Copy a persona or team into .persona/ in the current project
/tif:catalog uninstall <name>   Remove an installed persona, or a team and its unshared members, from .persona/
```
<!-- tif:quickstart:end -->

The `tif` plugin installs personas and teams from the bundled catalog into the current project's `.persona/personas/` and `.persona/teams/`. Files are checked against their sha256 before copying. Installing again updates any file that differs from the catalog and says so. Installing a team also installs its member personas, and warns about stub members, unresolved members and a missing default primary voice. Virtual teams (named in a context configuration but without a team file) cannot be installed. `uninstall` removes a persona's file, or a team's file together with the members no other installed team lists. It does not compare files with the catalog, so an older or changed copy is removed too. It records nothing, so a member you installed on its own is removed with a team that lists it when no other installed team does.

Conductor ignores installed team files for now: they are stored for later use and not yet read by Conductor.

The plugin has been tested through the Claude Code CLI only. **The Claude desktop app has not been tested.**

The bundled copy in `plugin/catalog/` and the command lists above are generated. Regenerate with `python3 scripts/build_persona_index.py` and `python3 plugin/scripts/tif.py --sync`; check with `python3 plugin/scripts/tif.py --check`. Run the plugin tests with `python3 -m unittest discover -s plugin/scripts`.

### Retrieving personas

`index.json` at the repo root lists every persona and team: id, summary, role, domain, `path`, size, `sha256`, `aliases`, and for teams the member ids. It is generated, so don't edit it by hand:

```
python3 scripts/build_persona_index.py          # regenerate
python3 scripts/build_persona_index.py --check  # fail if stale (run in CI)
```

To fetch only what you need, read `index.json` at a git ref, pick personas by `id` (or an alias) and/or a team by `id`, then fetch those entries' `path` files. A team entry's `members` gives the persona ids to fetch with it. Entries with `status: "stub"` are placeholder personas that ask to be fleshed out when first invoked; teams containing them are marked `contains_stubs`. A team that names a member with no persona file is marked `incomplete`, with the missing ids in `unresolved_members`; check this before installing a team.

Recommended consumer behavior beyond this (hash verification, tag pinning, install layout) is in [docs/persona-index-roadmap.md](docs/persona-index-roadmap.md). Specs: `openspec/specs/`; design: `openspec/changes/archive/2026-10-10-persona-index/`.

## Key Features

### Collaborative Intelligence
- **Unified Team Voice**: Single coherent response with multiple expertise areas
- **Seamless Handoffs**: Natural transitions between expertise boundaries
- **Deference Patterns**: Each persona knows when to defer to domain authorities
- **Two-Phase Challenge/Synthesis**: Challenge runs as a hard phase gate before synthesis — see `config/challenge_synthesis_protocol.md`

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
