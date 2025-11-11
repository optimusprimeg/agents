from livekit.agents.voice.voice_interruption_filter import SmartVoiceInterruptionHandler


def test_confidence_filtering():
    """Test confidence-based filtering functionality"""
    
    print("\n" + "="*70)
    print("🧪 CONFIDENCE-BASED FILTERING TEST")
    print("="*70 + "\n")
    
    handler = SmartVoiceInterruptionHandler(
        minimum_confidence=0.5,
        debug_mode=True
    )
    
    test_cases = [
        # (utterance, confidence, expected_suppress, description)
        ("hmm yeah", 0.3, True, "Low confidence background noise"),
        ("hmm yeah", 0.8, True, "High confidence filler"),
        ("wait stop", 0.3, True, "Low confidence genuine speech (suppressed)"),
        ("wait stop", 0.8, False, "High confidence genuine speech (allowed)"),
        ("uh", 0.2, True, "Very low confidence filler"),
        ("hello there", 0.9, False, "High confidence genuine speech"),
    ]
    
    print("Testing confidence thresholds:\n")
    
    for utterance, confidence, expected, description in test_cases:
        result = handler.should_ignore_utterance(utterance, confidence)
        
        status = "✅ PASS" if result == expected else "❌ FAIL"
        action = "SUPPRESSED" if result else "ALLOWED"
        
        print(f"{status} | '{utterance}' @ {confidence:.1f} confidence")
        print(f"     {description}")
        print(f"     Expected: {'SUPPRESS' if expected else 'ALLOW'} | Got: {action}\n")
    
    metrics = handler.get_performance_metrics()
    print("="*70)
    print(f"📊 Metrics:")
    print(f"   Low Confidence Blocks: {metrics['low_confidence_blocks']}")
    print(f"   Suppressed Interrupts: {metrics['suppressed_interrupts']}")
    print(f"   Total Processed: {metrics['total_processed']}")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_confidence_filtering()