import os
import sys
# Ensure Python can locate the src folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import run_research_agent

# 1. Setup our Evaluation Dataset (Gold Standards)
EVAL_DATASET = [
    {"topic": "The impacts of high-interest rates on housing markets", "expected_keywords": ["housing", "interest", "rates"]},
    {"topic": "The current timeline of renewable energy adoption in 2026", "expected_keywords": ["energy", "renewable", "solar" or "wind"]},
]

def run_evaluation_suite():
    print("🔬 Starting Automated AI Agent Evaluation Suite...\n")
    total_tests = len(EVAL_DATASET)
    passed_tests = 0

    for idx, test in enumerate(EVAL_DATASET, 1):
        print(f"Running Test {idx}/{total_tests} for topic: '{test['topic']}'...")
        try:
            # Execute the agent live
            report = run_research_agent(test["topic"])
            
            # Metric 1: Assert Pydantic structural validation
            has_title = len(report.title) > 0
            has_summary = len(report.summary) > 0
            valid_score = 0.0 <= report.confidence_score <= 1.0
            
            # Metric 2: Context keyword alignment validation
            contains_keywords = any(kw in report.summary.lower() or kw in report.title.lower() for kw in test["expected_keywords"])
            
            if has_title and has_summary and valid_score and contains_keywords:
                print(f"✅ Test {idx} PASSED (Accuracy Score: {report.confidence_score})")
                passed_tests += 1
            else:
                print(f"❌ Test {idx} FAILED (Failed validation metrics checks)")
                
        except Exception as e:
            print(f"❌ Test {idx} CRASHED: {e}")

    # Final Dashboard output calculation
    success_rate = (passed_tests / total_tests) * 100
    print("\n==========================================")
    print("📊 EVALUATION RESULTS ENGINE DASHBOARD")
    print(f"Total Test Cases Processed: {total_tests}")
    print(f"Successful Alignments: {passed_tests}")
    print(f"Total Production System Accuracy: {success_rate:.1f}%")
    print("==========================================\n")

if __name__ == "__main__":
    run_evaluation_suite()
