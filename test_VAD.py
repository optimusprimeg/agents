"""
Local test scenarios for filler word detection
Simulates different interruption scenarios
"""
import asyncio
from livekit.agents.voice.events import UserInputTranscribedEvent

# Test scenarios from the assignment
TEST_SCENARIOS = [
    {
        "name": "User filler while agent speaks",
        "transcript": "uh",
        "agent_speaking": True,
        "expected": "IGNORE"
    },
    {
        "name": "User real interruption",
        "transcript": "wait one second",
        "agent_speaking": True,
        "expected": "INTERRUPT"
    },
    {
        "name": "User filler while agent quiet",
        "transcript": "umm",
        "agent_speaking": False,
        "expected": "REGISTER"
    },
    {
        "name": "Mixed filler and command",
        "transcript": "umm okay stop",
        "agent_speaking": True,
        "expected": "INTERRUPT"
    },
    {
        "name": "Multiple fillers",
        "transcript": "uh hmm umm",
        "agent_speaking": True,
        "expected": "IGNORE"
    },
    {
        "name": "Real speech after filler",
        "transcript": "umm can you help me",
        "agent_speaking": True,
        "expected": "INTERRUPT"
    }
]

def run_tests():
    """Run all test scenarios"""
    from examples.voice_agents.filler_word_handler_local import FillerWordFilter
    
    filter = FillerWordFilter()
    
    print("\n" + "="*70)
    print("🧪 FILLER WORD DETECTION TEST SUITE")
    print("="*70 + "\n")
    
    for i, scenario in enumerate(TEST_SCENARIOS, 1):
        transcript = scenario["transcript"]
        agent_speaking = scenario["agent_speaking"]
        expected = scenario["expected"]
        
        # Determine behavior
        is_filler = filter.is_filler_only(transcript)
        has_real = filter.contains_real_speech(transcript)
        
        if agent_speaking:
            if is_filler:
                result = "IGNORE"
            else:
                result = "INTERRUPT"
        else:
            result = "REGISTER"
        
        status = "✅ PASS" if result == expected else "❌ FAIL"
        
        print(f"Test {i}: {scenario['name']}")
        print(f"  Input: '{transcript}'")
        print(f"  Agent Speaking: {agent_speaking}")
        print(f"  Expected: {expected} | Got: {result}")
        print(f"  {status}\n")
    
    stats = filter.get_stats()
    print("="*70)
    print(f"📊 Statistics: {stats}")
    print("="*70)

if __name__ == "__main__":
    run_tests()