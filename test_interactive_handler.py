import logging
from livekit.agents.voice.voice_interruption_filter import SmartVoiceInterruptionHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("interactive-handler-test")


def main():
    """Run interactive testing session"""
    
    handler = SmartVoiceInterruptionHandler(
        debug_mode=True,
        use_ml_enhancement=True
    )
    agent_active = True
    
    print("\n" + "="*70)
    print("🎤 INTERACTIVE VOICE HANDLER TEST")
    print("="*70)
    print("\n📋 Available Commands:")
    print("  - Type utterance to test filtering")
    print("  - 'toggle' - Switch agent state (active/inactive)")
    print("  - 'metrics' - View performance metrics")
    print("  - 'help' - Display this help")
    print("  - 'quit' / 'exit' - End test session")
    print(f"\n🎤 Agent State: {'ACTIVE' if agent_active else 'INACTIVE'}")
    print("="*70 + "\n")
    
    while True:
        try:
            user_input = input("Utterance: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit']:
                break
            
            if user_input.lower() == 'help':
                print("\n📋 Commands:")
                print("  toggle - Change agent state")
                print("  metrics - Show statistics")
                print("  quit/exit - End session\n")
                continue
            
            if user_input.lower() == 'toggle':
                agent_active = not agent_active
                state = "ACTIVE" if agent_active else "INACTIVE"
                print(f"\n🔄 Agent state: {state}\n")
                continue
            
            if user_input.lower() == 'metrics':
                metrics = handler.get_performance_metrics()
                print(f"\n📊 Performance Metrics:")
                print(f"   Suppressed: {metrics['suppressed_interrupts']}")
                print(f"   Allowed: {metrics['allowed_interrupts']}")
                print(f"   Low Confidence: {metrics['low_confidence_blocks']}")
                print(f"   Total: {metrics['total_processed']}\n")
                continue
            
            # Process utterance
            print(f"\n📝 Analyzing: '{user_input}'")
            print(f"   Agent State: {'ACTIVE' if agent_active else 'INACTIVE'}")
            
            if agent_active:
                suppressed = handler.should_ignore_utterance(user_input)
                if suppressed:
                    print(f"   Action: 🛑 SUPPRESSED (no interruption)\n")
                else:
                    print(f"   Action: ✅ ALLOWED (agent interrupted)\n")
            else:
                print(f"   Action: 👂 PROCESSED (agent inactive)\n")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")
    
    # Session summary
    metrics = handler.get_performance_metrics()
    print("\n" + "="*70)
    print("📊 Session Summary:")
    print(f"   Suppressed: {metrics['suppressed_interrupts']}")
    print(f"   Allowed: {metrics['allowed_interrupts']}")
    print(f"   Total: {metrics['total_processed']}")
    print("="*70)
    print("\n✅ Test session ended")
    print(f"   Time: 2025-11-11 13:11:36 UTC\n")


if __name__ == "__main__":
    main()