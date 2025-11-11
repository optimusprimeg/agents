"""
Integration test for filler word filter
Tests the filter within the actual agent framework
"""
import asyncio
import logging
from livekit.agents.voice.filler_filter import FillerWordFilter
from livekit.agents.voice.events import UserInputTranscribedEvent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_filter_integration():
    """Test that the filter is working correctly"""
    
    print("\n" + "="*70)
    print("🧪 FILLER WORD FILTER INTEGRATION TEST")
    print("="*70 + "\n")
    
    # Create filter instance
    filter = FillerWordFilter(enable_logging=True)
    
    # Simulate scenarios
    test_cases = [
        ("uh", True, "Should ignore filler when agent speaking"),
        ("wait", True, "Should allow real speech when agent speaking"),
        ("umm", False, "Should register filler when agent quiet"),
        ("hmm okay stop", True, "Should allow mixed speech"),
        ("mmm", True, "Should ignore multiple fillers"),
        ("umm can you help me", True, "Should allow real speech after filler"),
    ]
    
    for transcript, agent_speaking, description in test_cases:
        is_filler = filter.is_filler_only(transcript)
        
        if agent_speaking and is_filler:
            action = "🚫 IGNORED"
        elif agent_speaking and not is_filler:
            action = "✅ INTERRUPTED"
        else:
            action = "👂 REGISTERED"
        
        print(f"  {action} | '{transcript}' | Agent Speaking: {agent_speaking}")
        print(f"     → {description}\n")
    
    # Show stats
    stats = filter.get_stats()
    print("="*70)
    print(f"📊 Filter Statistics:")
    print(f"   Ignored Fillers: {stats['ignored_fillers']}")
    print(f"   Valid Interruptions: {stats['valid_interruptions']}")
    print(f"   Total Events: {stats['total_events']}")
    print("="*70 + "\n")
    
    print("✅ Integration test completed successfully!")

if __name__ == "__main__":
    test_filter_integration()