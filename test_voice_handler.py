from livekit.agents.voice.voice_interruption_filter import SmartVoiceInterruptionHandler


def execute_test_scenarios():
    """Run comprehensive test scenarios"""
    
    print("\n" + "="*70)
    print("🧪 SMART VOICE INTERRUPTION HANDLER - TEST SUITE")
    print("="*70 + "\n")
    
    handler = SmartVoiceInterruptionHandler(debug_mode=False)
    
    # Test scenarios with expected outcomes
    scenarios = [
        {
            "name": "Conversational filler during agent speech",
            "utterance": "uh",
            "agent_active": True,
            "expected": "SUPPRESS"
        },
        {
            "name": "Genuine interruption attempt",
            "utterance": "wait one second",
            "agent_active": True,
            "expected": "ALLOW"
        },
        {
            "name": "Filler when agent inactive",
            "utterance": "umm",
            "agent_active": False,
            "expected": "PROCESS"
        },
        {
            "name": "Combined filler with real speech",
            "utterance": "umm okay stop",
            "agent_active": True,
            "expected": "ALLOW"
        },
        {
            "name": "Multiple consecutive fillers",
            "utterance": "uh hmm umm",
            "agent_active": True,
            "expected": "SUPPRESS"
        },
        {
            "name": "Genuine content after filler",
            "utterance": "umm can you help me",
            "agent_active": True,
            "expected": "ALLOW"
        }
    ]
    
    passed = 0
    total = len(scenarios)
    
    for i, test in enumerate(scenarios, 1):
        utterance = test["utterance"]
        agent_active = test["agent_active"]
        expected = test["expected"]
        
        # Execute test
        if agent_active:
            should_suppress = handler.should_ignore_utterance(utterance)
            if should_suppress:
                result = "SUPPRESS"
            else:
                result = "ALLOW"
        else:
            result = "PROCESS"
        
        # Verify result
        status = "✅ PASS" if result == expected else "❌ FAIL"
        
        print(f"Test {i}: {test['name']}")
        print(f"  Input: '{utterance}'")
        print(f"  Agent Active: {agent_active}")
        print(f"  Expected: {expected} | Got: {result}")
        print(f"  {status}\n")
        
        if result == expected:
            passed += 1
    
    # Display metrics
    metrics = handler.get_performance_metrics()
    print("="*70)
    print(f"📊 Metrics: {metrics}")
    print(f"Test Results: {passed}/{total} passed")
    print("="*70 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = execute_test_scenarios()
    exit(0 if success else 1)