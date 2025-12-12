# Persona Framework v2.0: Configuration Overview

Complete reference for configuring and customizing the collaborative AI team management system.

## Framework Architecture

```
persona-framework/
├── config/                     # Core framework configuration
│   ├── persona_collaboration_framework.md      # Collaboration rules and patterns
│   ├── persona_interaction_architecture.md     # Addressing system and schemas  
│   ├── persona_activation_framework.md         # State management and discovery
│   └── measurement_framework.md                # Performance monitoring system
│
├── personas/                   # Individual persona definitions
│   ├── development/           # Development-focused expertise
│   │   ├── developer_coding_persona_schema.json
│   │   ├── blits_developer_persona_schema.json
│   │   ├── lightning_developer_persona_schema.json
│   │   ├── react_specialist_persona_schema.json
│   │   └── security_specialist_persona_schema.json
│   │
│   └── design/               # Design and UX expertise  
│       ├── 10_foot_ui_designer_persona_schema.json
│       ├── ott_ux_persona_schema.json
│       └── design_expert_persona_schema.json
│
├── teams/                     # Pre-configured team definitions
│   ├── react_fullstack_team.json
│   ├── security_review_team.json (example)
│   └── team_definition_examples.json
│
├── journal/                   # Session artifacts and logs
│   └── persona_framework_conversation_log.md
│
├── README.md                  # Framework overview and quick start
├── USER_GUIDE.md             # Complete user documentation
└── Persona_Framework_Implementation_Guide.md  # Platform implementation
```

## Configuration Components

### Core Framework Files

**persona_collaboration_framework.md**
- Primary voice system rules
- Optimistic skepticism protocol  
- Response tagging specifications
- Team collaboration patterns
- Unified response architecture

**persona_interaction_architecture.md**
- GitHub-style addressing system (`@persona_name`)
- Schema format specifications (v1.1+)
- Name resolution hierarchy
- Addressing fallback patterns

**persona_activation_framework.md**
- Framework state management (OFF/MINIMAL/ACTIVE/MONITORING)
- Discovery and suggestion logic
- Team persistence strategies
- Performance impact management

**measurement_framework.md**
- Performance metrics collection
- Usage pattern analysis
- Optimization recommendations
- Impact assessment dashboards

### Persona Schema Format (v1.1+)

**Required Fields:**
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

**Collaboration Extensions:**
```json
{
  "collaboration": {
    "expertise_scope": ["primary_domains"],
    "defers_to": ["other_persona_names"],
    "collaborates_well_with": ["complementary_personas"],
    "approach_style": "consultative|directive|supportive",
    "conflict_style": "defer|argue|compromise|demonstrate",
    "fallback_role": "coordination_responsibility"
  }
}
```

**Behavioral Configuration:**
```json
{
  "behavioral_rules": [
    "Always challenge assumptions before providing solutions",
    "Include code examples when explaining technical concepts",
    "Consider performance implications in all recommendations"
  ],
  "knowledge_base": [
    {
      "type": "documentation|research|internal",
      "url": "reference_url",
      "description": "Resource description",
      "project_relevance": "Why this matters",
      "category": "classification"
    }
  ]
}
```

### Team Definition Format

**Core Team Structure:**
```json
{
  "schema_version": "1.0",
  "metadata": {
    "name": "team_identifier",
    "description": "Team purpose and focus",
    "author": "creator",
    "version": "1.0",
    "example": false
  },
  "team": {
    "team_name": "snake_case_identifier", 
    "display_name": "Human Readable Team Name",
    "description": "Detailed team capabilities",
    "members": ["persona1", "persona2", "persona3"],
    "default_primary": "persona_name"
  }
}
```

**Discovery Configuration:**
```json
{
  "activation": {
    "auto_suggest_contexts": [
      "domain_keywords", "topic_areas", "question_types"
    ],
    "auto_suggest_keywords": [
      "specific", "trigger", "words"
    ],
    "discovery_priority": "high|medium|low"
  }
}
```

## Framework Commands Reference

### State Management
```
"personas on"                   # Activate framework
"personas off"                  # Deactivate completely
"minimal persona mode"          # Essential expertise only
"performance mode active"       # Enhanced monitoring
"framework status"              # Current state overview
```

### Team Operations  
```
"show my teams"                 # List available teams
"who's on my current team?"     # Display active roster
"activate [team_name]"          # Switch to pre-configured team
"deactivate team"              # Return to coordinator
"create team [name] with @persona1 @persona2"  # Build custom team
"save current team as [template]"  # Save roster as template
```

### Persona Management
```
"add @persona_name"             # Add to active roster
"remove @persona_name"          # Remove from roster
"list available personas"       # Show all personas
"persona info @name"           # Detailed persona information
"scan for new personas"        # Refresh persona pool
```

### Discovery & Suggestions
```
"suggest personas for this question"  # Context-based recommendations
"enable discovery"                    # Turn on auto-suggestions
"disable discovery"                   # Turn off auto-suggestions
"why this suggestion?"               # Explain discovery logic
```

### Performance Monitoring
```
"show performance metrics"      # Current session impact
"persona impact summary"        # Cost/benefit analysis  
"metrics current"              # Real-time statistics
"metrics summary"              # Historical usage data
"optimize my setup"            # Performance recommendations
```

## Customization Guidelines

### Creating New Personas

**1. Domain Analysis:**
- Identify specific expertise gap
- Define clear scope boundaries
- Determine collaboration patterns
- Plan knowledge base requirements

**2. Schema Development:**
- Use v1.1+ format with collaboration fields
- Define clear expertise scope
- Specify collaboration preferences
- Include relevant knowledge base

**3. Integration Testing:**
- Test collaboration with existing personas
- Verify discovery triggers work correctly
- Validate performance impact
- Confirm behavioral rules function

### Building Custom Teams

**1. Team Composition:**
- Start with coordinator persona
- Add complementary expertise areas
- Balance team size vs complexity
- Consider collaboration dynamics

**2. Discovery Configuration:**
- Define auto-suggestion contexts
- Set appropriate keywords
- Configure discovery priority
- Test suggestion accuracy

**3. Performance Optimization:**
- Monitor team effectiveness
- Adjust size based on usage
- Track collaboration quality
- Optimize based on metrics

### Platform Adaptations

**Claude Projects:**
- Store configurations in project artifacts
- Leverage cross-conversation persistence
- Use document analysis capabilities
- Configure performance artifact storage

**VS Code/Copilot:**
- Integrate with workspace settings
- Configure file context analysis
- Set up development workflow triggers
- Enable extension recommendations

**ChatGPT Custom GPTs:**
- Embed team templates in instructions
- Configure conversation starters
- Set up knowledge base integration
- Enable web browsing for teams

**Google Gemini:**
- Configure multimodal input analysis
- Set up workspace integrations
- Enable real-time information access
- Configure document context analysis

## Advanced Configuration

### Performance Tuning

**Context Management:**
- Monitor token usage patterns
- Optimize persona activation triggers
- Balance collaboration depth vs overhead
- Configure graceful degradation

**Response Quality:**
- Track collaboration effectiveness
- Measure user satisfaction indicators
- Optimize team composition patterns
- Fine-tune discovery algorithms

### Framework Evolution

**Usage Pattern Learning:**
- Track successful persona combinations
- Identify optimization opportunities
- Adapt suggestion algorithms
- Evolve collaboration patterns

**Schema Versioning:**
- Maintain backward compatibility
- Document schema evolution
- Test upgrade paths
- Preserve existing configurations

## Best Practices

### Configuration Management
- Maintain central repository (GitHub) as source of truth
- Use version control for all schema files
- Document customizations and rationale
- Regular sync between platforms and repository

### Performance Optimization
- Start with small teams, scale based on need
- Monitor metrics and optimize regularly  
- Use minimal mode for routine questions
- Leverage discovery rather than pre-loading large teams

### Quality Assurance
- Test persona collaboration patterns
- Validate discovery suggestion accuracy
- Monitor response quality vs performance trade-offs
- Gather user feedback and iterate

---

The Persona Framework v2.0 provides comprehensive configuration capabilities while maintaining simplicity for basic usage. Start with pre-configured teams and gradually customize based on your specific workflow needs.