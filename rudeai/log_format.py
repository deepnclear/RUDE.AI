"""
RUDE.AI: Inner processing Log and Override Engine
Structured Log Format Specification - Based on analysis of 11 training examples
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

@dataclass
class StructuredLogFormat:
    """
    Structured format for RUDE.AI logs based on training examples
    """
    # Date and time fields (auto-generated)
    date: str             # ISO format date (YYYY-MM-DD)
    time_of_day: str      # morning/afternoon/evening
    
    # Header format: "[Month Day], [Year] [Time]" (e.g., "August 27, 2025 Evening")
    header: str
    
    # Core log components (always present)
    situation: str               # 1-2 sentences describing the situation
    trigger: str                 # What caused the emotional response
    somatic_cognitive_response: str # Physical/bodily reactions and cognitive responses
    insight: str                 # Pattern analysis and deeper understanding
    
    # Metadata
    log_id: str
    timestamp: datetime
    raw_situation: str

class LogStructure:
    """
    Defines the exact structure and formatting rules for RUDE.AI logs
    """
    
    @staticmethod
    def get_header_format(timestamp: datetime) -> str:
        """
        Format: [Month Day], [Year] [Time]
        Examples: 
        - "August 27, 2025 Evening"
        - "May 24, 2024 Afternoon" 
        - "May 27, 2024 Morning"
        """
        month_day_year = timestamp.strftime("%B %d, %Y")
        time_part = LogStructure._format_time_description(timestamp)
        return f"{month_day_year} {time_part}"
    
    @staticmethod  
    def _format_time_description(timestamp: datetime) -> str:
        """Convert timestamp to natural time descriptions used in examples"""
        hour = timestamp.hour
        
        if 5 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 17:
            return "Afternoon" 
        elif 17 <= hour < 21:
            return "Evening"
        else:
            return "Night"
    
    @staticmethod
    def get_time_of_day(timestamp: datetime) -> str:
        """Get simplified time of day for time_of_day field (morning/afternoon/evening)"""
        hour = timestamp.hour
        
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon" 
        else:
            return "evening"  # Combine evening and night into "evening"
    
    @staticmethod
    def get_situation_format() -> str:
        """
        Situation format rules:
        - 1-2 sentences describing the situation
        - Present tense or past tense
        - Focus on activity, location, or circumstance
        
        Examples:
        - "Decision to give away a $70+ breakdancing hat rather than stay in contact with burned community ties"
        - "Paid apartment deposit via e-transfer"
        - "Sent message to father offering communication"
        """
        return "1-2 sentences describing the situation focusing on activity, location, or circumstance"
    
    @staticmethod
    def get_trigger_format() -> str:
        """
        Trigger format rules:
        - Specific cause of emotional activation
        - Can be single line or bullet points with dashes (–)
        - Focus on immediate precipitating event
        
        Examples:
        - "Internal voice of financial guilt and waste"
        - "App glitches, manual email verification, uncertainty around security question input"
        - "– Time scarcity script\n– Body surveillance loop\n– Paternal judgment residue"
        """
        return "Specific precipitating event or pattern that caused emotional activation"
    
    @staticmethod
    def get_somatic_cognitive_response_format() -> str:
        """
        Somatic Cognitive Response format rules:
        - Physical and cognitive reactions
        - Use bullet points with dashes (–) for multiple items
        - Include specific body sensations and mental patterns
        
        Examples:
        - "Mild discomfort while talking about the situation"
        - "– Light anxiety\n– Shoulder and upper chest tension\n– Thought racing upon waking"
        - "Immediate sympathetic spike, explosive chest tension ('micro ball' between breasts)"
        """
        return "Physical sensations and cognitive responses, formatted with bullet points if multiple"
    
    
    
    @staticmethod
    def get_insight_format() -> str:
        """
        Insight format rules:
        - Deep pattern analysis and psychological mechanism explanation
        - Often identifies the core psychological pattern
        - Explains underlying emotional dynamics
        - Can include philosophical/therapeutic insights
        
        Key insight patterns from examples:
        1. "This is [pattern type] in [specific] form"
        2. "The [emotion] is not about [surface issue]—it's [deeper mechanism]"
        3. "Your system [automatic response description]"
        4. "You are no longer [old pattern]. You are [new pattern]"
        
        Examples:
        - "The guilt is not about the hat—it's a proxy for old expectations of self-punishment when things are 'wasted'"
        - "This interaction carries emotional lineage charge—expectation, wound, and historic silence converge"
        - "This is a trauma-coded social reflex: small kindness = total reevaluation"
        """
        return "Deep pattern analysis explaining psychological mechanisms and insights"

class LogComponentPatterns:
    """
    Common patterns found in each log component from training examples
    """
    
    SITUATION_PATTERNS = [
        "Decision to [action] rather than [alternative]",
        "[Activity] while [circumstance]", 
        "Received [communication] from [person]",
        "[Location/Activity] [temporal context]"
    ]
    
    TRIGGER_PATTERNS = [
        "Internal voice of [emotional content]",
        "[Technical/situational difficulty] [emotional response]",
        "Silence after [action]. [Checking behavior]",
        "Sudden [emotion] surge tied to [specific fears]",
        "[Person] [action] triggering [historical pattern]"
    ]
    
    SOMATIC_COGNITIVE_PATTERNS = [
        "Light/mild [emotion] in [body location]",
        "[Intensity] [body part] [sensation type]",
        "[Autonomic response] [specific description]", 
        "Cognitive [pattern]: [specific thoughts]"
    ]
    
    INSIGHT_PATTERNS = [
        "This is [pattern type] in [specific] form",
        "The [emotion] is not about [surface issue]—it's [deeper pattern]",
        "Your system [old automatic response description]",
        "You are no longer [old pattern]. You are [new pattern]",
        "This interaction carries [emotional dynamic description]"
    ]

# Format validation rules
class LogFormatValidation:
    """
    Validation rules to ensure logs match the training example format
    """
    
    @staticmethod
    def validate_log_structure(log: StructuredLogFormat) -> List[str]:
        """Validate that log follows proper format structure"""
        errors = []
        
        # Check header format - should contain date and time
        if not any(month in log.header for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']):
            errors.append("Header must contain month name")
        
        if not any(time in log.header for time in ['Morning', 'Afternoon', 'Evening', 'Night']):
            errors.append("Header must contain time description")
        
        # Check required components
        required_components = ['situation', 'trigger', 'somatic_cognitive_response', 'insight']
        for component in required_components:
            value = getattr(log, component)
            if not value or len(value.strip()) < 10:
                errors.append(f"{component.replace('_', ' ').title()} must be substantive (at least 10 characters)")
        
        return errors
    
    @staticmethod
    def get_neutral_tone_guidelines() -> List[str]:
        """Guidelines for maintaining neutral, clinical tone"""
        return [
            "No supportive language ('I'm sorry', 'that must be hard')",
            "No encouraging phrases ('you can do this', 'stay strong')", 
            "No judgmental language (good/bad, right/wrong)",
            "Use factual, clinical descriptions",
            "Focus on mechanisms and patterns, not emotional validation",
            "End with confirmation statements ('Log confirmed', 'Pattern recognized')"
        ]