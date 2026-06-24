import time
import json
from eval.dataset import REAL_PROMPTS, EDGE_CASE_PROMPTS
from compiler.pipeline import CompilerPipeline
from runtime.simulator import execute_schema

def evaluate_dataset(dataset_name: str, prompts: list[str]):
    print(f"--- Evaluating {dataset_name} ({len(prompts)} prompts) ---")
    pipeline = CompilerPipeline(max_retries=2)
    
    success_count = 0
    total_latency = 0
    results = []

    for idx, prompt in enumerate(prompts):
        print(f"\nProcessing [{idx+1}/{len(prompts)}]: '{prompt[:50]}...'")
        start_time = time.time()
        
        try:
            # 1. Compile
            schema = pipeline.compile(prompt)
            compile_latency = time.time() - start_time
            
            # 2. Execute
            exec_result = execute_schema(schema)
            
            if exec_result["status"] == "success":
                success_count += 1
                status = "SUCCESS"
            else:
                status = f"EXECUTION_ERROR: {exec_result['message']}"
                
            results.append({
                "prompt": prompt,
                "status": status,
                "latency_sec": round(compile_latency, 2)
            })
            total_latency += compile_latency
            
        except Exception as e:
            latency = time.time() - start_time
            results.append({
                "prompt": prompt,
                "status": f"COMPILATION_ERROR: {str(e)}",
                "latency_sec": round(latency, 2)
            })
            total_latency += latency
            
    avg_latency = total_latency / len(prompts) if prompts else 0
    success_rate = (success_count / len(prompts)) * 100
    
    print(f"\n=== {dataset_name} Results ===")
    print(f"Success Rate: {success_rate}%")
    print(f"Average Latency: {avg_latency:.2f}s")
    
    return {
        "success_rate": success_rate,
        "average_latency": avg_latency,
        "results": results
    }

def run_all_evals():
    real_results = evaluate_dataset("REAL PROMPTS", REAL_PROMPTS)
    edge_results = evaluate_dataset("EDGE CASES", EDGE_CASE_PROMPTS)
    
    with open("eval_results.json", "w") as f:
        json.dump({"real": real_results, "edge": edge_results}, f, indent=2)
        
    print("\nDetailed results saved to eval_results.json")

if __name__ == "__main__":
    run_all_evals()
