"""
Interactive Console Test for Filler Word Detection
Allows manual testing by typing transcripts

Author: optimusprimeg
Date: 2025-11-11 12:35:59 UTC
"""
import logging
from livekit.agents.voice.filler_filter import FillerWordFilter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("interactive-test")


def main():
    filter = FillerWordFilter(enable_logging=True)
    agent_speaking = True
    
    print("\n" + "="*70)
    print("🎤 INTERACTIVE FILLER DETECTION TEST")
    print("="*70)
    print("\n📋 Commands:")
    print("  - Type any text to test filler detection")
    print("  - 'toggle' - Switch agent speaking state")
    print("  - 'stats' - Show statistics")
    print("  - 'help' - Show this help message")
    print("  - 'quit' or 'exit' - Exit the test")
    print("\n🎤 Agent is currently: SPEAKING")
    print("="*70 + "\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit']:
                break
            
            if user_input.lower() == 'help':
                print("\n📋 Available Commands:")
                print("  - toggle: Switch agent between SPEAKING/QUIET")
                print("  - stats: View filtering statistics")
                print("  - quit/exit: Exit the test")
                print("  - Any other text: Test filler detection\n")
                continue
            
            if user_input.lower() == 'toggle':
                agent_speaking = not agent_speaking
                state = "SPEAKING" if agent_speaking else "QUIET"
                print(f"\n🔄 Agent state changed to: {state}\n")
                continue
            
            if user_input.lower() == 'stats':
                stats = filter.get_stats()
                print(f"\n📊 Statistics:")
                print(f"   Ignored Fillers: {stats['ignored_fillers']}")
                print(f"   Valid Interruptions: {stats['valid_interruptions']}")
                print(f"   Low Confidence Ignored: {stats['low_confidence_ignored']}")
                print(f"   Total Events: {stats['total_events']}\n")
                continue
            
            # Process the input
            print(f"\n📝 Processing: '{user_input}'")
            print(f"   Agent State: {'SPEAKING' if agent_speaking else 'QUIET'}")
            
            if agent_speaking:
                if filter.is_filler_only(user_input):
                    print(f"   Result: 🚫 FILLER IGNORED (no interruption)\n")
                else:
                    print(f"   Result: ✅ REAL SPEECH (agent interrupted!)\n")
            else:
                print(f"   Result: 👂 REGISTERED as user speech\n")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")
    
    # Final stats
    stats = filter.get_stats()
    print("\n" + "="*70)
    print("📊 Final Statistics:")
    print(f"   Ignored Fillers: {stats['ignored_fillers']}")
    print(f"   Valid Interruptions: {stats['valid_interruptions']}")
    print(f"   Low Confidence Ignored: {stats['low_confidence_ignored']}")
    print(f"   Total Events: {stats['total_events']}")
    print("="*70)
    print("\n✅ Thank you for testing!")
    print(f"   Session ended: 2025-11-11 12:35:59 UTC\n")


if __name__ == "__main__":
    main()