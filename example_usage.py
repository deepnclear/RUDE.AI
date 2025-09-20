#!/usr/bin/env python3
"""
RUDE.AI Working Example
Demonstrates how to use the log creation and conversation handling features
"""

from rudeai.conversation_handler import RudeAIConversationHandler
from rudeai.log_creator import LogCreator
from rudeai.log_format import StructuredLogFormat

def demo_log_creator():
    """Demonstrate the LogCreator functionality"""
    print("=== RUDE.AI LOG CREATOR DEMO ===\n")
    
    creator = LogCreator()
    
    # Example emotional situations
    situations = [
        "I keep checking my ex's social media even though we broke up 6 months ago. Every time I see their posts I get this burning feeling in my chest and then feel angry at myself for looking.",
        "I have a job interview tomorrow and I've been awake since 3am going over every possible question they might ask. My heart won't stop racing and my stomach feels like it's in knots.",
        "I spent $500 on a course I thought would change my career but I haven't even finished the first module. Every time I see the receipt I feel this wave of guilt and tell myself I'm lazy and wasteful."
    ]
    
    for i, situation in enumerate(situations, 1):
        print(f"--- Example {i} ---")
        print(f"Situation: {situation}\n")
        
        # Create structured log
        log = creator.create_structured_log(situation, f"demo_{i}")
        
        # Format for display
        formatted = creator.format_log_for_confirmation(log)
        print(formatted)
        print("\n" + "="*60 + "\n")

def demo_conversation_handler():
    """Demonstrate the ConversationHandler functionality"""
    print("=== RUDE.AI CONVERSATION HANDLER DEMO ===\n")
    
    handler = RudeAIConversationHandler()
    
    # Start a session
    session_id = handler.start_session()
    print(f"Session started: {session_id}\n")
    
    # Simulate a conversation
    conversation_steps = [
        "I can't stop scrolling through social media late at night. I tell myself I'll just check for 5 minutes but then it's suddenly 2am and I have to wake up at 6. My eyes burn and I feel exhausted but I keep scrolling anyway.",
        "yes",
        "yes", 
        "I did the breathing exercises and put my phone in another room. It helped me fall asleep faster.",
        "yes, the technique worked"
    ]
    
    for step in conversation_steps:
        print(f"USER: {step}")
        response = handler.process_user_input(session_id, step)
        print(f"RUDE.AI: {response}\n")
    
    # Show session info
    session_info = handler.get_session_info(session_id)
    print("Session completed successfully!")
    print(f"Total interactions: {session_info['interaction_count']}")

def demo_standalone_log_creation():
    """Demonstrate creating logs without the conversation flow"""
    print("=== STANDALONE LOG CREATION DEMO ===\n")
    
    creator = LogCreator()
    
    situation = ("I was supposed to submit my project today but I kept procrastinating. "
                "Now it's 11pm and I'm panicking because I only have an hour left. "
                "My chest feels tight and I can't focus on anything.")
    
    log = creator.create_structured_log(situation, "standalone_001")
    
    print("Raw situation:")
    print(f"'{situation}'\n")
    
    print("Generated structured log:")
    print(f"Date: {log.date}")
    print(f"Time of Day: {log.time_of_day}")
    print(f"Header: {log.header}")
    print(f"Situation: {log.situation}")
    print(f"Trigger: {log.trigger}")
    print(f"Somatic Cognitive Response: {log.somatic_cognitive_response}")
    print(f"Pattern: {log.pattern}")
    print(f"Insight: {log.insight}")
    print(f"Log ID: {log.log_id}")

if __name__ == "__main__":
    print("RUDE.AI: Inner processing Log and Override Engine")
    print("Working Examples\n")
    
    demo_log_creator()
    demo_conversation_handler()
    demo_standalone_log_creation()