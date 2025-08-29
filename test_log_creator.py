"""
Test script for RUDE.AI log creation system
"""

import sys
sys.path.append('/Users/tanyaomelchuk/Desktop/RUDE_AI')

from rudeai.log_creator import LogCreator

def test_log_creation():
    """Test the log creation system with sample situations"""
    
    creator = LogCreator()
    
    # Test case 1: Financial anxiety (similar to breakdancing hat example)
    situation_1 = """I bought this expensive course online for $300 but I never used it and now I'm stressed about the money I wasted. Every time I see the email confirmations I get this anxious feeling in my chest and my stomach gets tight. I keep thinking about how stupid I was to spend that money and I feel like I should force myself to use it even though I don't want to anymore."""
    
    print("=== TEST CASE 1: Financial Anxiety ===")
    log_1 = creator.create_structured_log(situation_1, "test_001")
    formatted_1 = creator.format_log_for_confirmation(log_1)
    print(formatted_1)
    print("\n" + "="*60 + "\n")
    
    # Test case 2: Message checking compulsion (similar to checking examples)
    situation_2 = """I sent my boss a message asking about the deadline and now I keep checking my phone to see if he read it or responded. I've looked at it like 10 times in the last hour. My heart starts racing each time I check and I get this nervous energy in my shoulders. I know it's not urgent but I can't stop myself from looking."""
    
    print("=== TEST CASE 2: Message Checking Compulsion ===")
    log_2 = creator.create_structured_log(situation_2, "test_002")
    formatted_2 = creator.format_log_for_confirmation(log_2)
    print(formatted_2)
    print("\n" + "="*60 + "\n")
    
    # Test case 3: Guilt/reconciliation pattern (similar to sister example)
    situation_3 = """I had an argument with my friend yesterday and said some harsh things. Now I feel terrible and keep wanting to text her to apologize even though she was also in the wrong. I have this guilt sitting in my chest and I keep imagining reaching out to fix things. Part of me feels angry still but the guilt is stronger."""
    
    print("=== TEST CASE 3: Guilt/Reconciliation Pattern ===")
    log_3 = creator.create_structured_log(situation_3, "test_003")
    formatted_3 = creator.format_log_for_confirmation(log_3)
    print(formatted_3)
    print("\n" + "="*60 + "\n")
    
    # Test case 4: Performance anxiety (similar to interview example)
    situation_4 = """I have a presentation tomorrow morning and I woke up at 4am with my mind racing about all the things that could go wrong. My stomach is in knots and I went to the bathroom three times already. I keep reviewing my notes over and over but it's not helping with the anxiety. My chest feels tight and my breathing is shallow."""
    
    print("=== TEST CASE 4: Performance Anxiety ===")
    log_4 = creator.create_structured_log(situation_4, "test_004")
    formatted_4 = creator.format_log_for_confirmation(log_4)
    print(formatted_4)
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    test_log_creation()