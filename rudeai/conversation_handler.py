"""
RUDE.AI: Inner processing Log and Override Engine
Conversation Handler - Manages the exact conversation flow with strict state management
"""

from enum import Enum
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, List
from datetime import datetime
import json
import uuid

from .log_creator import LogCreator
from .log_format import StructuredLogFormat

class ConversationState(Enum):
    """States in the RUDE.AI conversation flow"""
    INITIAL = "initial"
    CONFIRMING_LOG = "confirming_log"
    ASKING_OVERRIDE_READY = "asking_override_ready"
    PROVIDING_OVERRIDE = "providing_override"
    CHECKING_OVERRIDE_RESULT = "checking_override_result"
    COMPLETE = "complete"

@dataclass
class ConversationSession:
    """Represents a single RUDE.AI conversation session"""
    session_id: str
    state: ConversationState
    current_log: Optional[StructuredLogFormat]
    conversation_history: List[Dict[str, Any]]
    created_at: datetime
    completed_at: Optional[datetime] = None

class RudeAIConversationHandler:
    """
    Handles the complete RUDE.AI conversation flow:
    1. User describes emotional situation
    2. RUDE.AI creates structured log and asks for confirmation
    3. If confirmed, RUDE.AI asks "Are you override-ready?"
    4. If yes, provides override sequence (placeholder for now)
    5. Asks if override worked
    6. Says "Log is closed" and ends conversation
    """
    
    def __init__(self):
        self.log_creator = LogCreator()
        self.sessions: Dict[str, ConversationSession] = {}
        
    def start_session(self, session_id: Optional[str] = None) -> str:
        """Start a new conversation session"""
        if not session_id:
            session_id = str(uuid.uuid4())[:8]
            
        session = ConversationSession(
            session_id=session_id,
            state=ConversationState.INITIAL,
            current_log=None,
            conversation_history=[],
            created_at=datetime.now()
        )
        
        self.sessions[session_id] = session
        return session_id
    
    def process_user_input(self, session_id: str, user_input: str) -> str:
        """Process user input based on current conversation state"""
        if session_id not in self.sessions:
            session_id = self.start_session(session_id)
            
        session = self.sessions[session_id]
        
        # Check if this is a report request
        if self._is_report_request(user_input) and session.state == ConversationState.INITIAL:
            response = self._generate_trigger_report(session_id)
            self._log_interaction(session, user_input, response)
            return response
            
        # Process based on current state
        if session.state == ConversationState.INITIAL:
            response = self._handle_initial_input(session, user_input)
        elif session.state == ConversationState.CONFIRMING_LOG:
            response = self._handle_log_confirmation(session, user_input)
        elif session.state == ConversationState.ASKING_OVERRIDE_READY:
            response = self._handle_override_ready_response(session, user_input)
        elif session.state == ConversationState.PROVIDING_OVERRIDE:
            response = self._handle_override_provision(session, user_input)
        elif session.state == ConversationState.CHECKING_OVERRIDE_RESULT:
            response = self._handle_override_result(session, user_input)
        elif session.state == ConversationState.COMPLETE:
            response = "Log is closed."
        else:
            response = "System error. Provide situation details."
            session.state = ConversationState.INITIAL
        
        self._log_interaction(session, user_input, response)
        return response
    
    def _handle_initial_input(self, session: ConversationSession, user_input: str) -> str:
        """Handle the initial user input describing their emotional situation"""
        
        # Generate log ID
        log_id = f"{session.session_id}_{datetime.now().strftime('%H%M')}"
        
        # Create structured log from user input
        session.current_log = self.log_creator.create_structured_log(user_input, log_id)
        
        # Format log for confirmation
        formatted_log = self.log_creator.format_log_for_confirmation(session.current_log)
        
        # Transition to confirmation state
        session.state = ConversationState.CONFIRMING_LOG
        
        return f"Situation logged. ID: {log_id}\n\n{formatted_log}\n\nConfirm log accuracy?"
    
    def _handle_log_confirmation(self, session: ConversationSession, user_input: str) -> str:
        """Handle user confirmation of the structured log"""
        
        if self._is_affirmative(user_input):
            session.state = ConversationState.ASKING_OVERRIDE_READY
            return "Are you override-ready?"
            
        elif self._is_negative(user_input):
            # Reset to initial state
            session.state = ConversationState.INITIAL
            session.current_log = None
            return "Log discarded. Provide situation details."
            
        else:
            # Ask again for clear confirmation
            return "Confirm log accuracy? Yes or no."
    
    def _handle_override_ready_response(self, session: ConversationSession, user_input: str) -> str:
        """Handle user's response to 'Are you override-ready?'"""
        
        if self._is_affirmative(user_input):
            session.state = ConversationState.PROVIDING_OVERRIDE
            override_sequence = self._generate_override_sequence(session.current_log)
            return f"Override sequence:\n\n{override_sequence}\n\nExecute sequence. Report completion status."
            
        elif self._is_negative(user_input):
            session.state = ConversationState.COMPLETE
            session.completed_at = datetime.now()
            self._save_session(session)
            return "Log is closed."
            
        else:
            return "Are you override-ready? Yes or no."
    
    def _handle_override_provision(self, session: ConversationSession, user_input: str) -> str:
        """Handle the state after providing override sequence"""
        # User should report completion status
        session.state = ConversationState.CHECKING_OVERRIDE_RESULT
        return "Did the override sequence resolve the emotional state?"
    
    def _handle_override_result(self, session: ConversationSession, user_input: str) -> str:
        """Handle user's report on override effectiveness"""
        
        # Record the override result
        if session.current_log:
            # Add override result to log metadata
            session.current_log.raw_situation += f"\n\nOverride Result: {user_input}"
        
        # Complete the session
        session.state = ConversationState.COMPLETE
        session.completed_at = datetime.now()
        self._save_session(session)
        
        return "Log is closed."
    
    def _generate_override_sequence(self, log: StructuredLogFormat) -> str:
        """Generate override sequence based on the structured log"""
        
        # This is a placeholder implementation
        # Will be replaced with actual override sequences when you provide examples
        
        base_sequence = [
            "1. Identify current physical sensations",
            "2. Take 3 measured breaths (4 in, 8 out)", 
            "3. Name the emotion without judgment",
            "4. Locate the trigger source",
            "5. Execute response protocol"
        ]
        
        # Basic customization based on log content
        if 'chest' in log.somatic_cognitive_response.lower():
            base_sequence.append("6. Address chest tension with focused breathing")
            
        if 'checking' in log.trigger.lower():
            base_sequence.append("6. Remove access to checking stimulus")
            
        if 'anxiety' in log.somatic_cognitive_response.lower():
            base_sequence.append("6. Ground through sensory awareness")
        
        return "\n".join(base_sequence)
    
    def _is_affirmative(self, text: str) -> bool:
        """Check if user response is affirmative"""
        affirmative_words = ['yes', 'y', 'yeah', 'yep', 'correct', 'right', 'accurate', 'true', 'ok', 'okay']
        text_lower = text.lower().strip()
        return (text_lower in affirmative_words or 
                any(word in text_lower for word in affirmative_words[:4]))  # Primary yes words
    
    def _is_negative(self, text: str) -> bool:
        """Check if user response is negative"""
        negative_words = ['no', 'n', 'nope', 'wrong', 'incorrect', 'inaccurate', 'false']
        text_lower = text.lower().strip()
        return (text_lower in negative_words or 
                any(word in text_lower for word in negative_words[:4]))  # Primary no words
    
    def _is_report_request(self, text: str) -> bool:
        """Check if user is requesting a trigger pattern report"""
        report_indicators = [
            'report', 'analysis', 'patterns', 'triggers', 'summary', 
            'show me', 'what are my', 'my patterns', 'analytics'
        ]
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in report_indicators)
    
    def _generate_trigger_report(self, session_id: str) -> str:
        """Generate a report of user's trigger patterns"""
        # Placeholder implementation - will be enhanced when analytics system is built
        return "Trigger pattern analysis not yet implemented. Provide situation details."
    
    def _log_interaction(self, session: ConversationSession, user_input: str, response: str):
        """Log the interaction for analysis and debugging"""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'state': session.state.value,
            'user_input': user_input,
            'response': response
        }
        session.conversation_history.append(interaction)
    
    def _save_session(self, session: ConversationSession):
        """Save completed session data"""
        # This will be enhanced when data storage system is built
        # For now, just keep in memory
        pass
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a session"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            return {
                'session_id': session.session_id,
                'state': session.state.value,
                'created_at': session.created_at.isoformat(),
                'completed_at': session.completed_at.isoformat() if session.completed_at else None,
                'current_log_id': session.current_log.log_id if session.current_log else None,
                'interaction_count': len(session.conversation_history)
            }
        return None
    
    def reset_session(self, session_id: str):
        """Reset a session to initial state"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session.state = ConversationState.INITIAL
            session.current_log = None
            session.conversation_history = []
    
    def get_active_sessions(self) -> List[str]:
        """Get list of active (non-complete) session IDs"""
        return [
            session_id for session_id, session in self.sessions.items()
            if session.state != ConversationState.COMPLETE
        ]