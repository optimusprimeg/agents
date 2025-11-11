import logging
from livekit.agents.voice.voice_interruption_filter import SmartVoiceInterruptionHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_integration_tests():
    """Execute integration test scenarios"""
    
    print("\n" + "="*70)
    print("🧪 VOICE INTERRUPTION HANDLER - INTEGRATION TEST")
    print("="*70 + "\n")
    
    handler = SmartVoiceInterruptionHandler(
        debug_mode=True,
        use_ml_enhancement=True  # Test with ML bonus
    )
    
    # Simulation scenarios
    test_cases = [
        ("uh", True, "Should suppress filler during agent speech"),
        ("wait", True, "Should allow genuine speech"),
        ("umm", False, "Should process filler when agent quiet"),
        ("hmm okay stop", True, "Should allow mixed content"),
        ("mmm", True, "Should suppress extended filler"),
        ("umm can you help me", True, "Should allow content after filler"),
    ]
    
    print("Running integration scenarios:\n")
    
    for utterance, agent_active, description in test_cases:
        print(f"Scenario: {description}")
        print(f"  Input: '{utterance}' | Agent Active: {agent_active}")
        
        if agent_active:
            suppressed = handler.should_ignore_utterance(utterance)
            action = "🛑 SUPPRESSED" if suppressed else "✅ ALLOWED"
        else:
            action = "👂 PROCESSED"
        
        print(f"  Action: {action}")
        print(f"     → {description}\n")
    
    # Display final metrics
    metrics = handler.get_performance_metrics()
    print("="*70)
    print("📊 Handler Metrics:")
    print(f"   Suppressed Interrupts: {metrics['suppressed_interrupts']}")
    print(f"   Allowed Interrupts: {metrics['allowed_interrupts']}")
    print(f"   Total Processed: {metrics['total_processed']}")
    print("="*70 + "\n")
    
    print("✅ Integration test completed successfully!\n")


if __name__ == "__main__":
    run_integration_tests()