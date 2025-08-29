# RUDE.AI: Inner Processing Log and Override Engine

**RUDE.AI** is an emotional situation management agent designed to help users process difficult emotional experiences through structured logging and targeted override sequences. The system provides neutral, clinical analysis of emotional patterns and delivers specific intervention protocols.

## Project Overview

RUDE.AI operates on a simple but powerful workflow:

1. **Situation Input**: Users describe emotional situations in detail (including physical sensations)
2. **Structured Logging**: RUDE.AI creates clinical logs analyzing context, triggers, somatic responses, and psychological patterns
3. **Override Sequences**: If users are "override-ready," RUDE.AI provides specific step-by-step intervention protocols
4. **Pattern Recognition**: The system learns from user patterns to provide increasingly targeted responses

The system maintains a completely neutral, non-supportive tone—focusing on factual analysis rather than emotional validation.

## Current Features

### ✅ Implemented Features

**Core Conversation Flow**
- Complete state-managed conversation handler
- Exact conversation sequence: Situation → Log → Override → Result → Close
- Session management with unique IDs and timestamps
- Neutral, clinical tone throughout all interactions

**Intelligent Log Creation**
- Automatic extraction of emotional contexts, triggers, and somatic responses
- Pattern recognition for 8+ psychological patterns (sunk cost, anticipatory vigilance, emotional pendulum, etc.)
- Structured log format based on training examples
- Natural language processing for physical sensation detection

**Advanced Pattern Analysis**
- Financial anxiety patterns (sunk cost override detection)
- Communication anxiety (message checking compulsions)
- Performance anxiety (anticipatory preparation protocols)
- Emotional pendulum recognition (anger-guilt cycles)
- Boundary violation analysis
- Compliance reflex identification

**Session Management**
- Multi-session support with persistent state
- Conversation history tracking
- Session reset and information retrieval
- Active session monitoring

### 🔧 Placeholder Features

**Override Sequences**
- Basic placeholder override sequences implemented
- Customization based on identified patterns
- Ready for integration with actual override protocols

**Analytics System**
- Framework for trigger pattern reports
- Session data collection for analysis
- Ready for comprehensive pattern tracking

## Project Structure

```
RUDE_AI/
├── README.md                          # This file
├── rudeai/                           # Main package
│   ├── __init__.py                   # Package initialization
│   ├── conversation_handler.py       # Core conversation flow management
│   ├── log_creator.py               # Structured log generation system
│   └── log_format.py                # Log format specification and validation
├── data/                            # Training and user data
│   └── training/
│       └── raw_logs/
│           └── raw_logs.pdf         # Training examples (11 situations)
├── test_conversation.py             # Conversation flow testing
├── test_log_creator.py             # Log creation system testing
└── scripts/                        # Additional processing scripts
    └── data_processing/
        └── log_processor.py         # PDF processing utilities
```

### Key Files Explained

**`rudeai/conversation_handler.py`**
- Main conversation orchestrator
- State machine implementation (INITIAL → CONFIRMING_LOG → ASKING_OVERRIDE_READY → PROVIDING_OVERRIDE → CHECKING_OVERRIDE_RESULT → COMPLETE)
- Session management and user input processing

**`rudeai/log_creator.py`**
- Advanced pattern recognition engine
- Somatic response extraction using regex patterns
- Psychological insight generation based on 11 training examples
- Context and trigger identification

**`rudeai/log_format.py`**
- Structured log format specification
- Validation rules and formatting guidelines
- Component definitions (Context, Trigger, Somatic Response, Insight)

**`data/training/raw_logs/raw_logs.pdf`**
- Contains 11 real emotional situation examples
- Training data for pattern recognition
- Examples of structured log format and insights

## Installation & Setup

### Prerequisites
- Python 3.8+
- Required packages: `PyPDF2`, `re`, `dataclasses`, `datetime`, `typing`

### Setup Instructions

1. **Clone/Download Project**
   ```bash
   cd /path/to/your/projects
   # Ensure you have the RUDE_AI directory
   ```

2. **Install Dependencies**
   ```bash
   pip install PyPDF2
   # Other dependencies are Python standard library
   ```

3. **Test Installation**
   ```bash
   cd RUDE_AI
   python3 test_conversation.py
   python3 test_log_creator.py
   ```

### Usage Example

```python
from rudeai.conversation_handler import RudeAIConversationHandler

handler = RudeAIConversationHandler()
session_id = handler.start_session()

# User describes emotional situation
situation = "I keep checking my phone for messages and getting anxious..."
response = handler.process_user_input(session_id, situation)
print(response)  # Shows structured log + "Confirm log accuracy?"

# Continue conversation...
```

## System Capabilities

### Pattern Recognition

The system can identify and analyze:

- **Sunk Cost Patterns**: Financial guilt and resource waste anxiety
- **Anticipatory Vigilance**: Checking behaviors and monitoring compulsions  
- **Emotional Pendulum**: Anger-guilt cycles in relationships
- **Performance Anxiety**: Presentation/interview stress responses
- **Compliance Reflex**: Automatic gratitude and obligation responses
- **Boundary Violations**: Uninvited interventions and consent issues
- **Family Dynamics**: Inherited emotional patterns and approval seeking
- **Financial Anxiety**: Transaction precision and monetary stress

### Log Format Example

```
August 28, 2025 Evening

Context: Paid apartment deposit via e-transfer
Trigger: App glitches, manual email verification, uncertainty around security question input
Somatic Response: 
– Mild anxiety
– Obsessive checking  
– Sympathetic reflex pulse
– Mental loop ("maybe I messed up the letter")
Insight: Mental hoarding accumulates micro-anxieties without purge. Precision is not panic. Every cent does not cost your peace.
```

## Current Status

### ✅ Completed Components
- [x] PDF training data processing (11 examples analyzed)
- [x] Structured log format specification
- [x] Advanced log creation system with pattern recognition
- [x] Complete conversation handler with state management
- [x] Neutral tone response system
- [x] Session management and tracking
- [x] Multi-pattern psychological analysis
- [x] Somatic response extraction
- [x] Test suites for all components

### 🔧 Next Steps Planned

1. **Override Sequence Integration**
   - Replace placeholder sequences with actual protocols
   - Pattern-specific override customization
   - Effectiveness tracking and optimization

2. **Data Storage System** 
   - Persistent session storage
   - Log archival and retrieval
   - User pattern history

3. **Analytics & Reporting**
   - Trigger pattern analysis reports
   - Progress tracking over time
   - Pattern frequency analysis

4. **Enhanced Pattern Recognition**
   - Additional psychological patterns
   - Improved trigger extraction accuracy
   - Context-aware response generation

## Dependencies

### Required
- **Python 3.8+**: Core runtime
- **PyPDF2**: PDF processing for training data
- **Standard Library**: `re`, `datetime`, `dataclasses`, `typing`, `enum`, `uuid`, `json`

### Optional
- **Development**: Testing frameworks if extending functionality
- **Deployment**: Web framework if building API interface

## Technical Architecture

### Design Principles
- **State-Driven**: Strict conversation flow management
- **Pattern-Based**: Recognition system trained on real examples  
- **Neutral Tone**: Clinical, non-supportive language throughout
- **Modular**: Separable components for easy enhancement
- **Session-Aware**: Multi-user support with conversation isolation

### Performance Notes
- **Lightweight**: No heavy ML dependencies
- **Fast**: Regex-based pattern matching for real-time response
- **Scalable**: Session-based architecture supports multiple users
- **Extensible**: Plugin-ready design for new patterns and overrides

---

**Status**: Core system functional, ready for override sequence integration and deployment.

**Next Milestone**: Integration of actual override protocols and persistent data storage.