"""
Test confidence threshold for background murmur
"""
from livekit.agents.voice.filler_filter import FillerWordFilter

def test_confidence_filtering():
    print("\n" + "="*70)
    print("🧪 CONFIDENCE THRESHOLD TEST")
    print("="*70 + "\n")
    
    filter = FillerWordFilter(
        confidence_threshold=0.5,  # Default threshold
        enable_logging=True
    )
    
    test_cases = [
        # (transcript, confidence, expected_result, description)
        ("hmm yeah", 0.3, True, "Low confidence background murmur"),
        ("hmm yeah", 0.8, True, "High confidence filler"),
        ("wait stop", 0.3, True, "Low confidence real speech (ignored)"),
        ("wait stop", 0.8, False, "High confidence real speech (allowed)"),
        ("uh", 0.2, True, "Very low confidence filler"),
        ("hello there", 0.9, False, "High confidence real speech"),
    ]
    
    print("Testing different confidence levels:\n")
    
    for transcript, confidence, expected_ignore, description in test_cases:
        result = filter.is_filler_only(transcript, confidence)
        
        status = "✅ PASS" if result == expected_ignore else "❌ FAIL"
        action = "IGNORED" if result else "ALLOWED"
        
        print(f"{status} | '{transcript}' @ {confidence:.1f} confidence")
        print(f"     {description}")
        print(f"     Expected: {'IGNORE' if expected_ignore else 'ALLOW'} | Got: {action}\n")
    
    stats = filter.get_stats()
    print("="*70)
    print(f"📊 Statistics:")
    print(f"   Low Confidence Ignored: {stats['low_confidence_ignored']}")
    print(f"   Regular Fillers Ignored: {stats['ignored_fillers']}")
    print(f"   Total Events: {stats['total_events']}")
    print("="*70 + "\n")

if __name__ == "__main__":
    test_confidence_filtering()