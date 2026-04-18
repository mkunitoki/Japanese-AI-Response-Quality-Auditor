-- 1. Find samples where naturalness < 5.0 (candidates for revision)
SELECT id, text, description, naturalness
FROM evaluation_results
WHERE naturalness < 5.0;

-- 2. Find high-quality samples (both politeness and naturalness >= 8.0)
SELECT * FROM evaluation_results
WHERE politeness >= 8.0 AND naturalness >= 8.0;

-- 3. Overall average scores (quick check on model tendencies)
SELECT AVG(politeness) AS avg_politeness, AVG(naturalness) AS avg_naturalness
FROM evaluation_results;

-- 4. Rank samples by average score
SELECT id, description, politeness, naturalness,
       ROUND((politeness + naturalness) / 2.0, 1) AS avg_score
FROM evaluation_results
ORDER BY avg_score DESC;
