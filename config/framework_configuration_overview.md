# Team Intelligence Framework v2.1: Configuration Overview

Complete reference for configuring and customizing the collaborative AI team management system.

## Framework Architecture

```
team_intelligence_framework/
│
├── config/                                       # Universal framework rules (Markdown)
│   ├── domain_agnostic_framework.md              # Domain-agnostic collaboration patterns
│   ├── framework_configuration_overview.md       # This file — structural reference
│   ├── measurement_framework.md                  # Performance monitoring
│   ├── persona_activation_framework.md           # Activation states and phases
│   ├── persona_collaboration_framework_v1.md     # Collaboration patterns and primary voice
│   └── persona_interaction_architecture_v1.md   # Addressing system (@persona_name)
│
├── personas/                                     # Domain-organized schemas (JSON + Markdown)
│   ├── persona_schema_example.json               # Canonical template
│   │
│   ├── ai_development/                           # AI/LLM development domain
│   │   ├── context_configuration.json
│   │   ├── llm_prompt_specialist_persona_schema.json
│   │   └── teams/
│   │       └── intelligence_framework_team.json
│   │
│   ├── development/                              # Software development domain
│   │   ├── context_configuration.json
│   │   ├── developer_coding_persona_schema.json
│   │   ├── react_specialist_persona_schema.json
│   │   ├── security_specialist_persona_schema_v1.json
│   │   ├── blits_developer_persona_schema_v1.json
│   │   ├── lightning_developer_persona_schema_v1.json
│   │   ├── cloud_architect_persona.json
│   │   ├── flutter_architect_persona_schema.json
│   │   ├── 10_foot_ui_designer_persona_schema_v1.1.json
│   │   ├── ott_ux_persona_schema_v1.1.json
│   │   ├── design_expert_persona_schema_v1.1.json
│   │   └── teams/
│   │       ├── react_fullstack_team.json
│   │       ├── flutter_mobile_development_team.json
│   │       └── news_aggregation_team.json
│   │
│   ├── financial/                                # Financial planning domain
│   │   ├── context_configuration.json
│   │   ├── investment_advisor_schema.json
│   │   ├── tax_strategist_schema.json
│   │   ├── healthcare_expert_schema.json
│   │   ├── social_security_specialist_schema.json
│   │   ├── insurance_analyst_schema.json
│   │   ├── estate_planner_schema.json
│   │   └── teams/
│   │       └── retirement_planning_team.json
│   │
│   ├── gaming/                                   # TTRPG and game design domain
│   │   ├── context_configuration.json            # Domain-level defaults
│   │   ├── ttrpg_game_architect_persona_schema.json
│   │   ├── TTRPG_evaluation_framework.md
│   │   └── hero_heaven/                          # Project-level override
│   │       ├── context_configuration_hero_heaven.json
│   │       ├── lore_keeper_persona_schema.json
│   │       ├── mythweaver_persona_schema.json
│   │       └── teams/
│   │           └── hero_heaven_worldbuilding_team.json
│   │
│   ├── writing/                                  # Creative writing domain
│   │   ├── context_configuration.json            # Domain-level defaults
│   │   └── screenplays/                          # Project-level override
│   │       ├── context_configuration_screenplays.json
│   │       ├── screenwriter_persona_schema.json
│   │       ├── dialog_coach_persona_schema.json
│   │       ├── science_advisor_persona_schema.json
│   │       └── dp_persona_schema.json
│   │
│   └── examples/                                 # Reference examples
│       ├── financial_team_collaboration_guide.md
│       ├── more_team_examples.json
│       └── team_definition_examples.json
│
├── README.md
├── ARCHITECTURAL_DECISIONS.md
├── CONFIG_REFERENCE.md
├── EXPERTISE_DOMAINS.md
├── PERSONA_FRAMEWORK_IMPLEMENTATION_GUIDE.md
├── TEAM_DEFINITION_GUIDE.md
├── USER_GUIDE.md
├── TODO.md
└── journal/
    └── persona_framework_conversation_log.md
```

---

## Configuration Components

### Layer 1: Universal Framework Files (`/config/`)

These Markdown files define how the framework works everywhere — across all domains and projects. They are loaded once; domain configs reference them, not the other way around.

**`domain_agnostic_framework.md`**
- Base collaboration principles applicable to any professional domain
- Domain adaptation examples (software, business, creative, research, healthcare)
- Framework implementation schema with domain-appropriate coordinator selection

**`persona_collaboration_framework_v1.md`**
- Primary voice system rules (who leads, how expertise shifts)
- Optimistic skepticism protocol (challenge before solve)
- Response tagging specification
- Unified response architecture

**`persona_interaction_architecture_v1.md`**
- GitHub-style `@persona_name` addressing system
- Name resolution hierarchy (custom name → persona name → display name)
- Schema portability and fallback patterns

**`persona_activation_framework.md`**
- Framework state management (Available Pool → Active Roster)
- Discovery and suggestion logic
- Activation phases (context detection → persona activation → reference binding → communication → checkout)

**`measurement_framework.md`**
- Performance metrics collection
- Usage pattern analysis
- Optimization recommendations

---

### Layer 2: Domain Configuration (`/personas/[domain]/`)

Each domain has a `context_configuration.json` that applies universal rules in domain-specific ways, plus persona schemas and team definitions.

**Two-level layering within domains:**
- **Domain level**: `personas/[domain]/context_configuration.json` — defaults for the whole domain
- **Project level**: `personas/[domain]/[project]/context_configuration_[project].json` — overrides for a specific project (e.g., `hero_heaven`, `screenplays`)

---

## Schema Formats

### Persona Schema (v1.2)

**Required fields:**
```json
{
  "schema_version": "1.2",
  "metadata": {
    "name": "Persona display name",
    "description": "Brief role description",
    "author": "creator_identifier",
    "version": "1.0",
    "created_date": "YYYY-MM-DD"
  },
  "persona": {
    "persona_name": "snake_case_identifier",
    "display_name": "CamelCaseDisplay",
    "custom_name": "Human Friendly Name",
    "role": "Specific expertise role",
    "expertise": ["domain1", "domain2", "domain3"],
    "approach": "Methodology description"
  }
}
```

**Collaboration fields:**
```json
{
  "collaboration": {
    "expertise_scope": ["primary_expertise_areas"],
    "defers_to": ["expertise_domain_not_persona_name"],
    "collaborates_well_with": ["complementary_expertise_areas"],
    "approach_style": "consultative|directive|supportive",
    "conflict_style": "defer|argue|compromise|demonstrate",
    "fallback_role": "coordination_responsibility"
  }
}
```

> **Note**: `defers_to` references expertise domains, not persona names. This keeps deference rules portable across teams with different membership.

**Behavioral configuration:**
```json
{
  "behavioral_rules": [
    "Challenge assumptions before providing solutions",
    "Include examples when explaining technical concepts",
    "Consider second-order implications in all recommendations"
  ],
  "reference_context": "domain_name",
  "reference_guide": "See PERSONA_ENGAGEMENT_GUIDE.md — [Section Name]"
}
```

> **Note**: No `knowledge_base` arrays in persona schemas. External references live in `reference_guide` (a pointer to documentation) and `reference_context` (the domain). Embedding knowledge base URLs in schemas caused maintenance drift and has been removed.

---

### context_configuration.json Schema

```json
{
  "schema_version": "1.0",
  "context_name": "domain_name",
  "description": "What this domain covers",
  "created_date": "YYYY-MM-DD",

  "reference_libraries": [
    "PERSONA_ENGAGEMENT_GUIDE.md",
    "ARCHITECTURAL_DECISIONS.md",
    "domain_specific_guide.md"
  ],

  "context_behavioral_protocols": {
    "primary_voice_system": "Who leads and how routing works in this domain",
    "optimistic_skepticism": "How challenge-before-solve applies in this domain",
    "domain_specific_rule": "Any additional behavioral guidance"
  },

  "activation_triggers": {
    "persona_name": {
      "keywords": ["keyword1", "keyword2"],
      "auto_suggest": true,
      "engagement_guide_section": "Section name in PERSONA_ENGAGEMENT_GUIDE.md"
    }
  },

  "always_on_personas": ["persona_name"],

  "available_personas": ["persona_name_1", "persona_name_2"],

  "available_teams": ["team_name_1"],

  "default_primary_persona": "persona_name",

  "collaboration_patterns": {
    "persona1": {
      "persona2": "How these two collaborate. Trigger: what activates it"
    }
  }
}
```

---

### Team Schema

```json
{
  "schema_version": "1.0",
  "metadata": {
    "name": "Team Name",
    "description": "Team purpose and focus",
    "context": "domain_name",
    "created_date": "YYYY-MM-DD"
  },

  "team": {
    "team_name": "snake_case_identifier",
    "display_name": "Human Readable Team Name",
    "members": ["persona1", "persona2", "persona3"],
    "default_primary": "persona1"
  },

  "activation": {
    "auto_suggest_contexts": ["context_keyword1", "context_keyword2"],
    "auto_suggest_keywords": ["specific_trigger_word"],
    "discovery_priority": "high|medium|low"
  },

  "team_dynamics": {
    "primary_workflow": "How the team collaborates",
    "collaboration_patterns": [
      {
        "members": ["persona1", "persona2"],
        "focus": "What they focus on together"
      }
    ],
    "decision_hierarchy": [
      "persona1: what they decide",
      "persona2: what they decide"
    ]
  },

  "use_cases": [
    "Scenario 1 where this team activates",
    "Scenario 2"
  ]
}
```

**Location**: `/personas/[domain]/teams/[team_name].json`  
Teams live inside their domain folder, not at the repo root.

---

## Framework Commands Reference

### Team Operations
```
"show my teams"                    # List available teams for active domain
"activate [team_name]"             # Switch to pre-configured team
"deactivate team"                  # Return to coordinator only
"create team [name] with @p1 @p2"  # Build custom team
"who's on my current team?"        # Display active roster
```

### Persona Management
```
"add @persona_name"                # Add to active roster
"remove @persona_name"             # Remove from roster
"list available personas"          # Show all personas for active domain
"persona info @name"               # Detailed persona information
```

### Domain Switching
```
"switch to financial context"      # Load financial domain config
"switch to gaming context"         # Load gaming domain config
"switch to development context"    # Load development domain config
```

### Framework State
```
"personas on"                      # Activate framework
"personas off"                     # Deactivate completely
"minimal persona mode"             # Essential expertise only
"framework status"                 # Current state overview
```

---

## Adding New Domains and Personas

### New Domain

1. Create `/personas/[domain]/` folder
2. Create `context_configuration.json` using the schema above
3. Add persona schemas following v1.2 format
4. Create `/personas/[domain]/teams/` and add at least one team definition

### New Persona

1. Create `[persona_name]_schema.json` in the appropriate domain folder using v1.2 format
2. Add `persona_name` to `available_personas` in the domain's `context_configuration.json`
3. Add activation triggers to `activation_triggers` in context config
4. Add collaboration patterns to `collaboration_patterns` where relevant

### New Project Context (within a domain)

1. Create `/personas/[domain]/[project]/` subfolder
2. Create `context_configuration_[project].json` — overrides domain defaults for this project
3. Add project-specific persona schemas to the project subfolder
4. Add team definitions to a `teams/` subfolder within the project

---

## Best Practices

- **Teams live inside domains**: `/personas/[domain]/teams/` — never at the repo root
- **No embedded knowledge bases**: Use `reference_guide` pointers in persona schemas
- **Deference by expertise, not by name**: `defers_to` field uses expertise domain strings
- **Layer configs correctly**: Domain config provides defaults; project config overrides only what differs
- **Version control schemas**: Increment persona schema version when behavioral rules change significantly
- **Start small**: Build teams of 3–4 personas; scale based on actual need

---

**The two-layer architecture (universal `/config/` + domain `/personas/[domain]/`) is the single most important structural decision in this framework. See ARCHITECTURAL_DECISIONS.md for the full rationale.**
