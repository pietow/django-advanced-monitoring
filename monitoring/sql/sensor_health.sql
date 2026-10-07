WITH measurements_in_range AS (
    SELECT
        st.code AS station_code,
        s.id AS sensor_id,
        s.name AS sensor_name,
        m.value,
        m.timestamp,
        ROW_NUMBER() OVER (
            PARTITION BY s.id
            ORDER BY m.timestamp DESC
        ) AS row_number
    FROM monitoring_sensor s
    JOIN monitoring_measurement m
        ON m.sensor_id = s.id
    JOIN monitoring_station st
        ON st.id = s.station_id
    WHERE st.code = %s
      AND m.timestamp >= %s
      AND m.timestamp < %s
)
SELECT
    r.station_code,
    r.sensor_id,
    r.sensor_name,
    COUNT(*) AS measurement_count,
    AVG(r.value) AS average_value,
    MAX(r.value) FILTER (
        WHERE r.row_number = 1
    ) AS last_value,
    MAX(r.timestamp) AS last_measurement
FROM measurements_in_range r
GROUP BY
    r.station_code,
    r.sensor_id,
    r.sensor_name
ORDER BY r.sensor_name;
