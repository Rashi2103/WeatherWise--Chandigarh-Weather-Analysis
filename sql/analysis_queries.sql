-- 1. Annual temperature and rainfall summary
SELECT year,
       ROUND(AVG(temperature_max_c), 1) AS avg_daily_max_c,
       ROUND(AVG(temperature_min_c), 1) AS avg_daily_min_c,
       ROUND(SUM(precipitation_mm), 1) AS total_rainfall_mm,
       SUM(heavy_rain_day) AS heavy_rain_days
FROM daily_weather
GROUP BY year
ORDER BY year;

-- 2. Monthly rainfall pattern across all available years
SELECT month, month_name,
       ROUND(AVG(precipitation_mm), 1) AS avg_daily_rainfall_mm,
       ROUND(SUM(precipitation_mm), 1) AS rainfall_sum_mm
FROM daily_weather
GROUP BY month, month_name
ORDER BY month;

-- 3. Days that cross the project's exploratory thresholds
SELECT date, temperature_max_c, precipitation_mm,
       CASE WHEN temperature_max_c >= 40 THEN 'Hot-day flag' ELSE '' END AS heat_flag,
       CASE WHEN precipitation_mm >= 50 THEN 'Heavy-rain flag' ELSE '' END AS rain_flag
FROM daily_weather
WHERE temperature_max_c >= 40 OR precipitation_mm >= 50
ORDER BY date DESC;

-- 4. Data quality check: should return zero rows after cleaning
SELECT date, COUNT(*) AS record_count
FROM daily_weather
GROUP BY date
HAVING COUNT(*) > 1;
