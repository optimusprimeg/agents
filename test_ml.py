"""
Compare Rule-Based vs ML Detection
Shows what ML catches that rules miss
"""
from livekit.agents.voice.voice_interruption_filter import SmartVoiceInterruptionHandler
from livekit.agents.voice.ml_utterance_classifier import MLUtteranceClassifier

print("\n" + "="*70)
print("🤖 ML vs RULE-BASED COMPARISON")
print("="*70 + "\n")

# Create both handlers
rule_only = SmartVoiceInterruptionHandler(
    debug_mode=False,
    use_ml_enhancement=False  # Rules only
)

ml_enhanced = SmartVoiceInterruptionHandler(
    debug_mode=False,
    use_ml_enhancement=True  # Rules + ML
)

# Test cases where ML helps
test_cases = [
    ("uh", "Exact match - both should catch"),
    ("uhhhhhh", "Stretched filler - ML should catch"),
    ("like you know", "Discourse marker - ML should catch"),
    ("wait stop", "Real speech - both should allow"),
    ("gonna tell you", "Informal - ML might catch"),
    ("sooooo cool", "Vowel stretch - ML might catch"),
    ("can you help", "Real speech - both should allow"),
]

print("Test Results:\n")
print(f"{'Utterance':<20} {'Rules Only':<15} {'ML Enhanced':<15} {'Description'}")
print("-" * 70)

for utterance, description in test_cases:
    rule_result = rule_only.should_ignore_utterance(utterance)
    ml_result = ml_enhanced.should_ignore_utterance(utterance)
    
    rule_text = "🛑 SUPPRESS" if rule_result else "✅ ALLOW"
    ml_text = "🛑 SUPPRESS" if ml_result else "✅ ALLOW"
    
    # Highlight differences
    if rule_result != ml_result:
        indicator = " ⭐ ML DIFFERENCE!"
    else:
        indicator = ""
    
    print(f"{utterance:<20} {rule_text:<15} {ml_text:<15} {description}{indicator}")

print("\n" + "="*70)

# Show ML feature analysis for one example
print("\n🔬 ML Feature Analysis for 'uhhhhhh':\n")
classifier = MLUtteranceClassifier()
prob = classifier.calculate_filler_probability("uhhhhhh")
print(f"   Filler Probability: {prob:.2f}")
print(f"   Prediction: {'FILLER' if prob >= 0.65 else 'GENUINE'}")
print("\n" + "="*70 + "\n")