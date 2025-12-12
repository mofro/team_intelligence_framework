# Team Intelligence Framework: Implementation Guide v2.1

Detailed instructions for implementing and using the advanced Persona Framework - a collaborative AI team management system.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [File Organization](#file-organization)
3. [Activation and States](#activation-and-states)
4. [Team Management](#team-management)
5. [Adding Personas and Teams](#adding-personas-and-teams)
6. [Performance Management](#performance-management)
7. [Best Practices](#best-practices)

## Architecture Overview

The framework uses a **two-layer architecture**:

### Layer 1: Universal Framework (`/config/`)
Principles governing all domains and projects:

- **Domain Agnostic Framework**: Base operating principles
- **Persona Activation Framework**: Discovery and activation patterns
- **Persona Collaboration Framework**: How personas work together
- **Persona Interaction Architecture**: Addressing system and schema specs
- **Measurement Framework**: Performance measurement principles

These files define what personas *are* and how they *collaborate*, but not specific implementations.

### Layer 2: Domains & Projects (`/personas/`)
Concrete implementations for specific contexts:

- **Domain folders** (gaming, development, financial, writing) contain:
  - `context_configuration.json` - Domain-level activation triggers
  - Individual persona schema files (v1.1 format)
  - `/teams/` subdirectory with team definitions
  
- **Project-specific contexts** documented separately in `PROJECT_MIGRATION_GUIDE.md`

This separation keeps the framework portable while allowing rich customization.

## File Organization

### Framework Structure

```
/config/
├── domain_agnostic_framework.md
├── persona_activation_framework.md
├── persona_collaboration_framework_v1.md
├── persona_interaction_architecture_v1.md
└── measurement_framework.md

/personas/
├── ARCHITECTURAL_DECISIONS.md      # Decisions made during refactoring
├── REFACTORING_REFERENCE.md        # How framework maps to schema
├── CONFIG_REFERENCE.md             # Configuration specifications
├── TEAM_DEFINITION_GUIDE.md        # How to create teams
│
├── /gaming/
│   ├── context_configuration.json
│   ├── /hero_heaven/
│   │   ├── lore_keeper_persona_schema.json
│   │   ├── mythweaver_persona_schema.json
│   │   └── /teams/
│   │       └── hero_heaven_worldbuilding_team.json
│   ├── ttrpg_game_architect_persona_schema.json
│   └── /teams/
│
├── /development/
│   ├── context_configuration.json
│   ├── experienced_developer_persona_schema.json
│   ├── react_specialist_persona_schema.json
│   ├── security_specialist_persona_schema_v1.json
│   ├── [8 other development personas]
│   └── /teams/
│       └── react_fullstack_team.json
│
├── /financial/
│   ├── context_configuration.json
│   ├── investment_advisor_schema.json
│   ├── tax_strategist_schema.json
│   ├── [4 other financial personas]
│   └── /teams/
│       └── retirement_planning_team.json
│
└── /writing/
    ├── context_configuration.json
    ├── /screenplays/
    │   ├── screenwriter_persona_schema.json
    │   ├── dialog_coach_persona_schema.json
    │   ├── science_advisor_persona_schema.json
    │   └── dp_persona_schema.json
    └── /teams/
        └── (ready for team definitions)

PROJECT_MIGRATION_GUIDE.md  # Project-specific contexts and knowledge
```

### File Type Conventions

**Framework Principles** (`/config/*.md`):
- Define universal patterns
- Reference-only; don't modify unless architecture changes
- Dated when updated; track version history

**Domain Configuration** (`/personas/{domain}/context_configuration.json`):
- Domain-level activation triggers and persona groupings
- Created once per domain
- Updated when adding personas to domain

**Persona Schemas** (`/personas/{domain}/*_persona_schema.json`):
- Individual persona definitions
- Schema version 1.1
- Self-contained; portable between projects
- Never embed project-specific context (use PROJECT_MIGRATION_GUIDE instead)

**Team Definitions** (`/personas/{domain}/teams/{team_name}.json`):
- Team composition and collaboration patterns
- Pre-configured teams for common workflows
- Can be domain-specific or cross-domain
- Updated when teams change

**Project Contexts** (`PROJECT_MIGRATION_GUIDE.md`):
- Project-specific goals, constraints, knowledge
- Extracted from personas during refactoring
- Keeps persona schemas clean and portable
- Referenced by personas via `reference_guide` field

## Activation and States

### Framework States

**OFF**
```
"personas off"
```
- Base LLM only; no persona overhead
- Framework completely dormant
- Re-activates with `"personas on"`

**MINIMAL**
```
"minimal persona mode"
```
- Single coordinator persona
- Reduced context overhead
- Essential collaboration available

**ACTIVE** (Default)
```
"personas on"
```
- Full team collaboration
- Context analysis and suggestions
- Performance monitoring available

**MONITORING**
```
"monitoring mode"
```
- Detailed performance tracking
- Usage pattern analysis
- Optimization recommendations

### Activation Flow

1. **User invokes**: `"activate retirement planning team"`
2. **Framework loads**: Team definition from `/personas/financial/teams/retirement_planning_team.json`
3. **Framework loads**: Each persona schema (investment_advisor, tax_strategist, etc.)
4. **Applies**: Universal collaboration rules from `/config/` files
5. **Activates**: Team with all expertise immediately available

## Team Management

### Creating Teams

**Team Definition Structure** (`/personas/{domain}/teams/{team_name}.json`):

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

**Guidelines**:
- Use snake_case for team_name
- Team members must be `persona_name` values (can verify in persona schemas)
- primary_voice persona addresses disagreements
- decision_pattern guides conflict resolution

### Team Activation Commands

```
"show my teams"                 # List all available teams
"activate [team_name]"          # Switch to team
"add @persona_name"             # Add individual to active team
"remove @persona_name"          # Remove from active team
"deactivate team"              # Return to baseline
"create team [name] with [personas]"  # Build custom team
```

## Adding Personas and Teams

### Adding a New Persona to Existing Domain

1. **Create schema file**:
   ```
   /personas/{domain}/{persona_name}_persona_schema.json
   ```
   Use v1.1 format with these required fields:
   - `schema_version: "1.1"`
   - `persona.persona_name` (snake_case)
   - `collaboration.expertise_scope`
   - `collaboration.defers_to`
   - `behavioral_rules` (8-15 imperative statements)
   - `reference_context` (domain name)

2. **Update domain configuration**:
   Edit `/personas/{domain}/context_configuration.json` to include persona in activation_triggers

3. **Add to teams** (optional):
   Update relevant team definitions in `/personas/{domain}/teams/`

### Adding a New Domain

1. **Create domain folder**:
   ```
   /personas/{domain_name}/
   ```

2. **Create domain configuration**:
   ```json
   {
     "domain": "new_domain",
     "display_name": "New Domain",
     "personas": [],
     "activation_triggers": {}
   }
   ```

3. **Add personas**: Create persona schema files in domain folder

4. **Define teams**: Create `/teams/` subdirectory and team definitions

5. **Document context**: Add project-specific info to `PROJECT_MIGRATION_GUIDE.md`

### Schema Template (v1.1)

```json
{
  "schema_version": "1.1",
  "metadata": {
    "name": "Full Name - Description",
    "description": "Detailed description of expertise",
    "author": "Author name",
    "version": "1.0",
    "created_date": "YYYY-MM-DD"
  },
  "persona": {
    "persona_name": "snake_case_name",
    "display_name": "CamelCaseName",
    "custom_name": "Optional nickname",
    "role": "What this persona does",
    "experience": "Background and expertise",
    "expertise": ["area1", "area2"],
    "approach": "How they approach problems",
    "specializations": ["special1", "special2"]
  },
  "collaboration": {
    "expertise_scope": ["domain1", "domain2"],
    "defers_to": ["persona_name_if_exists"],
    "approach_style": "consultative|directive|supportive",
    "conflict_style": "defer|argue|compromise"
  },
  "behavioral_rules": [
    "Imperative rule 1",
    "Imperative rule 2",
    "..."
  ],
  "reference_libraries": [
    {
      "type": "knowledge_type",
      "description": "What this library contains",
      "url": "https://or/internal://",
      "depth": "novice|intermediate|expert"
    }
  ],
  "reference_context": "domain_name",
  "reference_guide": "See documentation for protocols"
}
```

## Performance Management

### Monitoring Impact

```
"show performance metrics"
```

Returns:
- Active team composition
- Response length impact
- Context overhead estimate
- Optimization recommendations

### Optimization Strategies

**Team Size**:
- 2-3 personas: Routine questions
- 4-5 personas: Complex projects
- 6+ personas: Comprehensive analysis

**Mode Selection**:
- Use MINIMAL for simple questions
- Use ACTIVE for complex decisions
- Use MONITORING to identify optimization opportunities

**Regular Tuning**:
- Remove unused personas from rosters
- Consolidate overlapping expertise
- Build templates for recurring workflows

## Best Practices

### Schema Design

**Expertise Scope**:
- Keep to 5-8 core areas (focused domain)
- Avoid generic catch-alls
- Align with deference patterns

**Behavioral Rules**:
- Write as imperative statements ("Do X", "Ask Y")
- Keep to 8-15 rules per persona
- Make them persona-specific, not universal
- Include challenge/skepticism patterns

**Deference**:
- Identify one authority per expertise area
- Keep deference paths short (2-3 levels max)
- Document why deference exists

### Team Composition

**Complementary Expertise**:
- Ensure coverage of needed domains
- Include decision-maker or primary voice
- Balance specialists with generalists
- Consider deference hierarchy

**Collaboration Patterns**:
- Define primary voice (who speaks for team)
- Specify decision pattern (consensus, hierarchy, etc.)
- Document how disagreements resolve

### Extensibility

**Portable Schemas**:
- No project-specific context in persona schemas
- Reference context via `reference_context` field
- Document project details in PROJECT_MIGRATION_GUIDE.md

**Domain Independence**:
- Each domain folder self-contained
- Can move domain to new project unchanged
- Teams within domain portable with personas

**Framework Stability**:
- Don't modify `/config/` files unless architecture changes
- Version schema changes (1.1 → 1.2)
- Track breaking changes in ARCHITECTURAL_DECISIONS.md

## Implementation Checklist

### Setting Up Framework

- [ ] Review `/config/` files for universal patterns
- [ ] Identify domains needed for project
- [ ] Load domain folders or create new ones
- [ ] Test persona activation: `"show my teams"`
- [ ] Activate initial team
- [ ] Monitor performance: `"show performance metrics"`

### Adding New Personas

- [ ] Create schema file (use template above)
- [ ] Verify all required fields present
- [ ] Test activation: `"add @persona_name"`
- [ ] Add to relevant teams
- [ ] Update domain configuration
- [ ] Test team activation

### Creating New Teams

- [ ] Identify team purpose and members
- [ ] Verify members exist (check persona_name values)
- [ ] Define primary voice and decision pattern
- [ ] Create team JSON file
- [ ] Test activation: `"activate [team_name]"`
- [ ] Save as template if recurring

## Troubleshooting

### Persona Not Activating

**Problem**: `"add @persona_name"` fails or doesn't activate

**Solutions**:
1. Verify persona exists: `"list available personas"`
2. Check schema syntax: JSON must be valid
3. Verify `persona_name` matches schema (snake_case)
4. Check domain context loaded

### Team Not Found

**Problem**: `"activate team_name"` fails

**Solutions**:
1. Verify team file exists in correct location
2. Check team JSON syntax
3. Verify member persona_name values exist
4. Confirm domain context loaded

### Performance Issues

**Problem**: Slow responses or high overhead

**Solutions**:
1. Check active team size: `"show performance metrics"`
2. Reduce team: `"remove @less_critical_persona"`
3. Switch to minimal mode: `"minimal persona mode"`
4. Review behavioral rules (overly complex?)

### Unexpected Behavior

**Problem**: Personas not deferring or collaborating as expected

**Solutions**:
1. Review behavioral_rules in schemas
2. Check defers_to relationships
3. Verify team definition primary_voice
4. Consult REFACTORING_REFERENCE.md for schema mapping

## Next Steps

**For Framework Development**:
- See ARCHITECTURAL_DECISIONS.md for decisions made
- See REFACTORING_REFERENCE.md for schema mapping details
- See PROJECT_MIGRATION_GUIDE.md for project-specific extensions

**For Adding Personas**:
- Use schema template above
- Follow v1.1 structure
- Consult existing personas for patterns

**For Custom Implementations**:
- Fork domain folder for your project
- Create project-specific teams
- Document in PROJECT_MIGRATION_GUIDE.md

---

**The framework is designed for extensibility with stable core principles and flexible implementations.**
