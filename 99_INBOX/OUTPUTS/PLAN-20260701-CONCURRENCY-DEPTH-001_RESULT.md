# RESULT -- PLAN-20260701-CONCURRENCY-DEPTH-001

- Executor: ollama
- Status: complete
- Dispatched: 2026-07-01 02:17:41

---

# Concurrency & Priority Enforcement

## Concurrency Control: Single-GPU Limitations

In a single-machine setup with n8n and Ollama running on a single GPU, the **maximum concurrent jobs must be strictly limited to 1**. This constraint arises from the GPU's inability to parallelize workloads effectively—most LLM inference and workflow execution tasks are CPU-bound or require exclusive GPU access. Allowing more than one concurrent job risks resource contention, memory overflows, or degraded performance across tasks. The `max-concurrent-jobs=1` rule ensures deterministic execution, prevents GPU utilization bottlenecks, and guarantees that each task completes fully before the next begins.

## Priority Enforcement: Client-Facing Task Preemption

When multiple tasks are queued, **priority enforcement must prioritize client-facing tasks** (e.g., user-initiated workflows) over background or system tasks. This is achieved by implementing a **priority-aware task queue** with the following mechanics:

- **Priority Levels**: Assign numerical priority values (e.g., `1` for client tasks, `2` for system tasks) during task creation.
- **Queue Ordering**: Maintain a priority-ordered queue where tasks are inserted based on their priority. Higher-priority tasks are dequeued and executed first, even if they arrived later.
- **Preemption Logic**: If a high-priority task arrives while a lower-priority task is running, the current task is paused, and the higher-priority task is immediately scheduled. This requires a mechanism to interrupt ongoing work (e.g., via cancellation tokens or signal handling in n8n/Ollama).

This ensures that user-facing workflows are processed with minimal latency, aligning with service-level expectations while maintaining fairness for system tasks.

## Scaling to Multi-Worker Concurrency with Redis

If Redis is later introduced to enable true multi-worker concurrency (e.g., distributing tasks across multiple GPUs or machines), the following changes would be required:

1. **Centralized Task Queue**: Replace the local in-memory queue with Redis-based data structures (e.g., `RPOPLPUSH` for FIFO queues or `ZSET` for priority queues) to coordinate tasks across workers.
2. **Distributed Locking**: Implement Redis-based locking (e.g., `SETNX` or Redlock) to manage GPU access if multiple workers share the same GPU (though this would still require `max-concurrent-jobs=1` per GPU).
3. **Priority Handling in Redis**: Use Redis sorted sets with priority scores to ensure tasks are dequeued in the correct order, even across distributed workers.
4. **Worker Coordination**: Workers would poll Redis for tasks, process them, and update status (e.g., `INCR` for task counters, `HMSET` for task metadata), enabling dynamic scaling and fault tolerance.

These changes would transition the system from a single-GPU, single-worker model to a scalable, distributed task-processing pipeline while preserving priority enforcement and concurrency control.
