"""
Test script for RUDE.AI conversation handler
"""

import sys
sys.path.append('/Users/tanyaomelchuk/Desktop/RUDE_AI')

from rudeai.conversation_handler import RudeAIConversationHandler

def test_conversation_flow():
    """Test the complete RUDE.AI conversation flow"""
    
    handler = RudeAIConversationHandler()
    
    print("=== RUDE.AI CONVERSATION FLOW TEST ===\n")
    
    # Start session
    session_id = handler.start_session()
    print(f"Session started: {session_id}\n")
    
    # Step 1: User describes emotional situation
    situation = """I spent $200 on a gym membership but I've only gone twice in three months. Every time I see the charge on my credit card I get this sick feeling in my stomach and my chest gets tight. I keep telling myself I should go more but then I make excuses and feel even worse about wasting the money."""
    
    print("USER:", situation)
    response1 = handler.process_user_input(session_id, situation)
    print("RUDE.AI:", response1)
    print()
    
    # Step 2: User confirms log
    confirmation = "yes"
    print("USER:", confirmation)
    response2 = handler.process_user_input(session_id, confirmation)
    print("RUDE.AI:", response2)
    print()
    
    # Step 3: User says they are override-ready
    ready = "yes"
    print("USER:", ready)
    response3 = handler.process_user_input(session_id, ready)
    print("RUDE.AI:", response3)
    print()
    
    # Step 4: User reports completion
    completion = "I tried the breathing and it helped a bit. The chest tension went away."
    print("USER:", completion)
    response4 = handler.process_user_input(session_id, completion)
    print("RUDE.AI:", response4)
    print()
    
    # Step 5: User reports override result
    result = "Yes, it helped reduce the anxiety"
    print("USER:", result)
    response5 = handler.process_user_input(session_id, result)
    print("RUDE.AI:", response5)
    print()
    
    # Check session info
    session_info = handler.get_session_info(session_id)
    print("=== SESSION INFO ===")
    print(f"Session ID: {session_info['session_id']}")
    print(f"State: {session_info['state']}")
    print(f"Interactions: {session_info['interaction_count']}")
    print()

def test_conversation_variations():
    """Test different conversation paths"""
    
    handler = RudeAIConversationHandler()
    
    print("=== TESTING CONVERSATION VARIATIONS ===\n")
    
    # Test 1: User declines override
    print("--- Test 1: User declines override ---")
    session_id = handler.start_session()
    
    situation = "I'm stressed about a work presentation tomorrow."
    print("USER:", situation)
    response1 = handler.process_user_input(session_id, situation)
    print("RUDE.AI:", response1[:100] + "...")
    
    print("USER: yes")
    response2 = handler.process_user_input(session_id, "yes")
    print("RUDE.AI:", response2)
    
    print("USER: no")
    response3 = handler.process_user_input(session_id, "no")
    print("RUDE.AI:", response3)
    print()
    
    # Test 2: User rejects log
    print("--- Test 2: User rejects log ---")
    session_id2 = handler.start_session()
    
    situation2 = "I'm feeling anxious about money."
    print("USER:", situation2)
    response1 = handler.process_user_input(session_id2, situation2)
    print("RUDE.AI:", response1[:100] + "...")
    
    print("USER: no, that's not accurate")
    response2 = handler.process_user_input(session_id2, "no, that's not accurate")
    print("RUDE.AI:", response2)
    print()

if __name__ == "__main__":
    test_conversation_flow()
    print()
    test_conversation_variations()