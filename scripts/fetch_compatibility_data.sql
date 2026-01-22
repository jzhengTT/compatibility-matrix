WITH recent_pipelines AS (
    SELECT cicd_pipeline_id,
           github_pipeline_id,
           pipeline_start_ts,
           pipeline_end_ts,
           git_commit_hash,
           name
    FROM   sw_test.cicd_pipeline
    WHERE  
      name = 'On nightly'
      AND project = 'tt-shield'
      AND git_branch_name = 'main'
    ORDER BY pipeline_end_ts DESC
    LIMIT 1
),
filtered_jobs AS (
    SELECT *
    FROM   sw_test.cicd_job
    WHERE (name ILIKE 'run-release%' OR name ILIKE 'run-evals%')
),
shield_runs AS (
    SELECT *
    FROM   sw_test.benchmark_run
    WHERE  git_repo_name = 'tt-shield'
)
SELECT
    p.github_pipeline_id,
    p.pipeline_end_ts,
    r.ml_model_name,
    LOWER(r.device_info->>'device_name') AS device_name,
    r.input_sequence_length AS isl,
    r.output_sequence_length AS osl,
    r.batch_size,
    r.precision,
    r.benchmark_run_id,
    m.step_name,
    m.name AS metric_name,
    m.value AS metric_value
FROM         recent_pipelines            p
JOIN         filtered_jobs               j  ON j.cicd_pipeline_id = p.cicd_pipeline_id
LEFT JOIN    shield_runs                 r  ON r.github_job_id    = j.github_job_id
LEFT JOIN    sw_test.benchmark_measurement m ON m.benchmark_run_id = r.benchmark_run_id
ORDER BY p.pipeline_end_ts DESC, r.ml_model_name, m.step_name