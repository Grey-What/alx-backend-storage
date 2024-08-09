-- ranks country of origin of bands, ordered by number of fans
DROP INDEX origin ON metal_bands;
CREATE INDEX origin ON metal_bands(origin); 

SELECT origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
