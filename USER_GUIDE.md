# Team Intelligence Framework - User Guide

Complete guide to using the collaborative AI team management system with pre-configured domain teams and individual personas.

## Getting Started

### Framework Activation

```
"personas on"                    # Activate the framework
"show my teams"                  # List available expert teams  
"list available personas"        # See individual personas
```

### Quick Team Start - By Domain

**Gaming Domain** (Hero Heaven TTRPG):
```
"activate hero heaven worldbuilding team"  # Lore Keeper, Mythweaver, TTRPG Game Architect
```

**Development Domain** (Full Stack):
```
"activate react fullstack team"   # React Specialist, Experienced Developer, Security Specialist, UX Specialist, UI Designer
```

**Financial Domain** (Retirement Planning):
```
"activate retirement planning team"  # Investment Advisor, Tax Strategist, Social Security Specialist, Healthcare Expert, Insurance Analyst, Estate Planner
```

## Working with Teams

### Pre-Configured Teams by Domain

#### **Gaming Domain**

**Hero Heaven Worldbuilding Team** (`/personas/gaming/teams/hero_heaven_worldbuilding_team.json`)
- **Members**: Lore Keeper, Mythweaver, TTRPG Game Architect
- **Expertise**: World documentation, narrative resonance, mechanical design
- **Activation**: `"activate hero heaven worldbuilding team"`
- **Best For**: TTRPG world-building, narrative consistency, system design

#### **Development Domain**

**React Full-Stack Team** (`/personas/development/teams/react_fullstack_team.json`)
- **Members**: React Specialist, Experienced Developer, Security Specialist, UX Strategist, UI Designer
- **Expertise**: Web application development, component architecture, security integration
- **Activation**: `"activate react fullstack team"`
- **Best For**: React projects, web applications, full-stack development

**Individual Development Personas**:
- **@experienced_developer**: Senior architect and code quality lead
- **@react_specialist**: Pragmatic React framework decisions
- **@security_specialist**: Application security and authentication
- **@blits_developer**: Lightning/Blits UI optimization
- **@lightning_developer**: Lightning v2 core framework
- **@ui_designer**: TV interface design and performance
- **@ux_designer**: User experience and usability
- **@ux_ui_strategist**: Cross-platform design strategy
- **@cloud_architect**: Infrastructure and deployment

#### **Financial Domain**

**Retirement Planning Team** (`/personas/financial/teams/retirement_planning_team.json`)
- **Members**: Investment Advisor, Tax Strategist, Social Security Specialist, Healthcare Expert, Insurance Analyst, Estate Planner
- **Expertise**: Comprehensive retirement planning across all financial dimensions
- **Activation**: `"activate retirement planning team"`
- **Best For**: Early retirement strategy, tax optimization, household planning

**Individual Financial Personas**:
- **@investment_advisor**: Portfolio allocation and risk management
- **@tax_strategist**: Tax optimization and withdrawal strategy
- **@social_security_specialist**: Benefit claiming and household optimization
- **@healthcare_expert**: Medicare planning and cost management
- **@insurance_analyst**: Risk assessment and catastrophic coverage
- **@estate_planner**: Asset protection and succession planning

#### **Writing Domain**

**Screenplay Team** (Team definitions TBD)
- **Members**: Screenwriter, Dialog Coach, Science Advisor, Director of Photography
- **Expertise**: Story structure, dialogue authenticity, scientific accuracy, visual storytelling
- **Best For**: Screenplay development, narrative structure, technical authenticity

**Individual Writing Personas**:
- **@screenwriter**: Story structure and narrative vision
- **@dialog_coach**: Character voice and dialogue authenticity
- **@science_advisor**: Scientific accuracy and technical plausibility
- **@director_of_photography**: Visual storytelling and cinematography

### Team Management Commands

**Team Operations:**
```
"who's on my current team?"      # Display active roster
"show my teams"                  # List all available teams
"activate [team name]"           # Switch to pre-configured team
"deactivate team"               # Return to baseline
"clear my team"                 # Remove all personas from roster
```

**Individual Persona Management:**
```
"add @persona_name"             # Add specific expertise
"remove @persona_name"          # Remove from active team
"persona info @experienced_developer"  # Get detailed persona information
```

**Custom Team Building:**
```
"create team api_security with @experienced_developer @security_specialist @cloud_architect"
"save current team as my_api_team"    # Save roster as template
```

## Addressing Personas

### Direct Engagement

Use `@persona_name` to address specific expertise:

```
@security_specialist Review this authentication flow.
@investment_advisor Should we rebalance the portfolio?
@screenwriter How does this plot change affect the narrative arc?
```

### Natural Topic Routing

Ask domain-specific questions and framework suggests relevant personas:

```
"How do I optimize database queries?"  → suggests @experienced_developer
"What's the best Bond strategy?"       → suggests @investment_advisor  
"How should characters react here?"    → suggests @dialog_coach
```

## Understanding Personas

### Persona Structure

Each persona has:

- **persona_name**: How to address them (@experienced_developer)
- **display_name**: Human-readable identifier
- **custom_name**: Optional nickname
- **expertise_scope**: What domains they advise on
- **behavioral_rules**: How they operate (8-15 principles)
- **defers_to**: Who has authority over them

### Reading Deference Patterns

**Deference indicates hierarchy within teams**:

- `@security_specialist` defers to `@experienced_developer`
  → Developer makes final architectural calls; Security reviews first
  
- `@investment_advisor` leads but consults `@tax_strategist`
  → Portfolio decisions account for tax implications
  
- `@dialog_coach` defers to `@screenwriter`
  → Dialogue serves story structure

When personas disagree, deference patterns guide resolution.

## Framework States

### Active Mode (Default)
```
"personas on"
```
- Full team collaboration available
- Context analysis and suggestions active
- All expertise immediately accessible

### Minimal Mode
```
"minimal persona mode"
```
- Single coordinator persona only
- Reduced context overhead
- Essential functionality maintained

### Off Mode
```
"personas off"
```
- Return to base LLM responses
- Framework completely dormant
- Can reactivate anytime

### Monitoring Mode
```
"monitoring mode"
```
- Detailed performance tracking
- Usage pattern analysis
- Optimization recommendations

## Performance Management

### Monitoring Framework Impact

```
"show performance metrics"

Session Performance
Active Team: Retirement Planning Team (6 personas)
Questions: 12 (all with personas)
Response Length: +65% vs base LLM
Estimated Overhead: ~20% context usage
```

### Optimization Strategies

**Team Size Guidelines**:
- **2-3 personas**: Routine questions, focused expertise
- **4-5 personas**: Complex projects, multiple domains  
- **6+ personas**: Comprehensive analysis, major decisions

**Performance Tips**:
- Use `"minimal mode"` for simple questions
- Remove unused personas from active roster
- Leverage pre-configured teams (more efficient than custom)
- Monitor metrics vs response quality trade-offs

## Platform-Specific Notes

### Claude Projects
- Team persistence across conversations
- Artifact storage for configurations and metrics
- File upload for team analysis

### VS Code/Copilot
- Workspace-aware persona suggestions
- Integration with development workflow
- File context analysis for relevant expertise

### ChatGPT / Google Gemini
- Custom GPT configurations for team templates
- Real-time information access for research
- Multimodal input analysis (images, documents)

## Best Practices

### Effective Team Usage

**Start Small, Scale Up**:
1. Activate basic team for your domain
2. Add expertise as questions become complex
3. Use discovery suggestions rather than pre-loading
4. Monitor performance and optimize

**Leverage Templates**:
- Use pre-configured teams for standard workflows
- Save successful custom combinations
- Build team templates for recurring tasks

**Quality Focus**:
- Challenge framework assumptions (it expects this!)
- Request specific persona input when needed
- Use performance metrics to validate collaboration
- Provide feedback to improve suggestions

### Collaboration Optimization

**Natural Interaction**:
- Let framework suggest personas via context
- Use direct addressing for expertise handoffs
- Trust unified voice system for responses
- Ask follow-up questions for clarity

**When to Use Direct Addressing**:
- Need specific expertise focus: `@security_specialist`
- Want persona opinion: `"What does the screenwriter think?"`
- Handling disagreement between personas
- Requesting detailed explanation from specialist

## Project-Specific Context

Each domain has project-specific knowledge documented in `PROJECT_MIGRATION_GUIDE.md`:

**Gaming**: Hero Heaven TTRPG dual-truth system, mythic integration, exile narrative
**Development**: React/Lightning/Blits technology stack, TV/OTT performance requirements
**Financial**: Retirement planning for Maurice and spouse, age gap considerations, household optimization
**Writing**: Screenplay with astrophysics and neuroscience, ensemble cast, technical authenticity requirements

When starting a project, consult that guide for context and activation recommendations.

## Troubleshooting

### Framework Not Responding
- Check activation: `"personas on"`
- Verify available teams: `"show my teams"`
- List personas: `"list available personas"`

### Personas Not Collaborating
- Reduce team size for clearer responses
- Use direct addressing: `@persona_name specific_question`
- Request perspective: `"Get input from security perspective"`

### Performance Issues
- Switch to minimal mode: `"minimal persona mode"`
- Check overhead: `"show performance metrics"`
- Remove unused personas: `"remove @persona_name"`

### Inconsistent Behavior
- Reinitialize: `"personas off"` then `"personas on"`
- Clear team: `"clear my team"` then rebuild
- Check for schema updates

---

**The Persona Framework transforms individual consultations into collaborative team intelligence. Begin with domain teams and expand as needed.**
