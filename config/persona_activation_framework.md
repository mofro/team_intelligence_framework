# Persona Activation & Discovery Framework v1.0

## Overview

This framework extends the Persona Collaboration Framework with state management, discovery logic, and activation controls. It defines how personas transition between available, suggested, and active states while providing users visibility into system performance and impact.

## Core State Model

### Persona States
- **Available Pool**: All personas discovered in current context (files, workspace, project)
- **Active Roster**: Currently engaged personas participating in responses
- **Suggested**: Context-recommended personas awaiting user decision
- **Dormant**: Available but not active or currently suggested

### Framework Operating Modes
- **OFF**: No persona processing, base LLM responses only
- **MINIMAL**: Reduced persona set, essential expertise only
- **ACTIVE**: Full persona system with user-selected roster
- **MONITORING**: Active system with performance tracking enabled

## Discovery & Suggestion Logic

### Context Analysis Triggers
1. **Domain Keywords**: Scan user input for expertise-specific terminology
2. **Question Complexity**: Multi-faceted queries that span knowledge domains
3. **Topic Transitions**: Conversation shifts requiring different expertise
4. **Explicit Requests**: Direct mentions of needing specific help

### Suggestion Criteria
- **Relevance**: Persona expertise matches question domain
- **Roster Gap**: Missing expertise in current active roster
- **Historical Value**: Previously useful personas for similar contexts
- **Collaboration Potential**: Personas that work well with current roster

### Suggestion Presentation
```
💡 Suggestion: @security_specialist might help with authentication flows
   Add with: "activate security specialist" or "add @security_specialist"
   
Current team: @developer_coding_persona, @backend_developer
Available: @ui_designer, @database_expert, @security_specialist
```

## Conversational Command Interface

### Activation Commands
```
Natural Language Alternatives:
- "activate @persona_name" / "add security specialist to team"
- "remove @persona_name" / "deactivate database expert"
- "show my team" / "who's on my current team?"
- "what personas are available?" / "list available experts"
- "suggest personas for this question"
- "clear my team" / "start fresh with personas"
```

### Discovery Commands
```
Natural Language Alternatives:
- "enable persona suggestions" / "turn on discovery"
- "disable suggestions" / "stop suggesting personas"
- "scan for new personas" / "refresh persona pool"
- "persona info @name" / "tell me about the security specialist"
```

### Performance Commands
```
Natural Language Alternatives:
- "show performance metrics" / "how are personas affecting performance?"
- "persona impact summary" / "what's the cost of using personas?"
- "turn personas off" / "disable persona system"
- "minimal persona mode" / "use essential personas only"
```

## State Management Specifications

### Persistence Hierarchy
1. **Platform-Specific**: Use native persistence when available
   - Claude Projects: Store in project artifacts
   - VS Code: Workspace settings integration
   - ChatGPT: Custom GPT memory/instructions
2. **Session-Only**: Fallback for platforms without persistence
   - Track state in conversation memory
   - Reinitialize each session
   - Graceful degradation notifications

### State Transitions
```
Available Pool → Suggested → Active Roster → Dormant
      ↑              ↓           ↓           ↓
   [scan/refresh] [context] [activate] [deactivate]
      ↑              ↑           ↑           ↓
   Available Pool ← Suggested ← Active ← Dormant
```

### Default Behaviors
- **New Context**: Start with the context's `default_primary_persona` (from its `context_configuration.json`) active; with no context configuration, see Empty Roster
- **Empty Roster**: Provide base LLM responses with persona availability notice
- **Unavailable Personas**: Graceful fallback with alternatives suggested
- **Context Loss**: Reinitialize with last known configuration

## Performance Impact Management

### Impact Monitoring
Track and display when possible:
- Response length comparison (persona vs non-persona)
- Processing time indicators
- Context utilization estimates
- User satisfaction feedback

### Performance Modes
- **OFF Mode**: Complete persona shutdown, return to base LLM
- **MINIMAL Mode**: Single coordinator persona only
- **ACTIVE Mode**: User-selected roster (default)
- **MONITORING Mode**: Full system with detailed tracking

### User Visibility
```
Performance Summary:
Active Personas: 3 (@coordinator, @security, @ui_designer)
Estimated Overhead: Context usage increased
Response Quality: Enhanced collaboration (user feedback)
Recommendations: Current roster size appears optimal
```

## Integration with Collaboration Framework

### Primary Voice Management
- **Active Roster Coordination**: The default primary persona leads unless a specific persona is addressed
- **Voice Handoff**: Activation/deactivation triggers primary voice transitions
- **Expertise Gaps**: Discovery system suggests personas when expertise missing

### Response Integration
- **Team Awareness**: Responses acknowledge current active roster
- **Suggestion Integration**: Suggestions presented within collaboration flow
- **State Transparency**: Users can see who contributed to responses

### Collaboration Optimization
- **Team Balance**: Discovery suggests complementary expertise
- **Redundancy Avoidance**: Warn about overlapping personas in roster
- **Workflow Enhancement**: Learn patterns of effective persona combinations

## Implementation Guidelines

### Platform Integration Patterns
1. **Initialize Framework**: Load persona pool from available sources
2. **Set Default State**: Establish starting roster based on context
3. **Enable Discovery**: Begin context analysis for suggestions
4. **Track Performance**: Monitor impact according to platform capabilities
5. **Provide Controls**: Implement conversational command interface

### Graceful Degradation
- **Limited Persistence**: Function without cross-session memory
- **Reduced Discovery**: Operate with manual activation only
- **Minimal Monitoring**: Basic performance awareness without detailed metrics
- **Essential Features**: Core activation/deactivation always available

### Extensibility Points
- **Custom Discovery Logic**: Domain-specific context analysis
- **Performance Metrics**: Platform-specific measurement integration
- **State Storage**: New persistence mechanisms as platforms evolve
- **Command Extensions**: Additional management commands based on usage

## Framework Behavior Specifications

### Discovery System Behavior
- **Passive Analysis**: Continuously analyze context when discovery enabled
- **Suggestion Throttling**: Avoid overwhelming users with frequent suggestions
- **Relevance Filtering**: Only suggest personas with clear value for current context
- **User Learning**: Adapt suggestions based on user acceptance patterns

### Activation System Behavior
- **Immediate Effect**: Activated personas participate in next response
- **Graceful Addition**: New personas integrate without disrupting conversation flow
- **Conflict Resolution**: Handle persona expertise overlaps constructively
- **Resource Awareness**: Warn about performance implications of large rosters

### State Persistence Behavior
- **Automatic Saving**: Preserve state changes without explicit user action
- **Context Awareness**: Maintain state appropriate to current project/workspace
- **Recovery Resilience**: Restore previous state when possible after interruptions
- **Privacy Respect**: Store configuration only, never conversation content

## Success Metrics

### User Experience Indicators
- Users can easily discover and activate relevant personas
- State management feels natural and predictable
- Performance impact is transparent and manageable
- Framework enhances rather than complicates workflow

### Technical Performance Indicators
- State transitions execute reliably across platforms
- Discovery suggestions demonstrate clear relevance
- Performance monitoring provides actionable insights
- Integration with collaboration framework is seamless

### Framework Evolution Indicators
- Usage patterns reveal optimization opportunities
- User feedback drives meaningful improvements
- Platform capabilities enable enhanced features
- Framework scales effectively with persona library growth

---

This framework provides the foundation for practical persona management while maintaining the collaborative principles established in the core framework. Implementation should prioritize user control, transparency, and graceful adaptation to platform constraints.