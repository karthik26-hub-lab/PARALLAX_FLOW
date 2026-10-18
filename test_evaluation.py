import asyncio
from backend.services.evaluation_job_manager import EvaluationJobManager

async def test():
    print("Initiating Demo Evaluation...")
    job = await EvaluationJobManager.create_demo_job()
    print(f"Created Job: {job.job_id}")

    # Wait for completion
    while True:
        await asyncio.sleep(1)
        cur = EvaluationJobManager.get_job(job.job_id)
        print(f"Status: {cur.status}")
        if cur.status in ("COMPLETED", "FAILED"):
            if cur.status == "COMPLETED":
                print("\n================ EVALUATION SUMMARY ================")
                print(f"Total Score: {cur.total_marks_awarded} / {cur.total_max_marks} ({cur.percentage}%)")
                print(f"Grade: {cur.performance_grade}")
                print(f"Questions Evaluated: {cur.total_questions}")
                print("----------------------------------------------------")
                for q in cur.questions:
                    print(f"Q{q['question_no']} ({q['question_id']}): {q['marks_awarded']} / {q['max_marks']} marks")
                    print(f"  Matched Keywords: {q.get('keywords_matched', [])}")
                    print(f"  Steps Evaluated: {len(q.get('steps_evaluation', []))}")
                    for s in q.get('steps_evaluation', []):
                        print(f"    Step {s['step_no']} [{s['subpart']}]: {s['marks_awarded']}/{s['max_marks']} ({s['status']})")
                print("====================================================")
            else:
                print(f"Error: {cur.error_message}")
            break

if __name__ == "__main__":
    asyncio.run(test())
