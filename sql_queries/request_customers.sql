
-- Les clients viennent de combien de villes et d’état différents?
SELECT COUNT(DISTINCT customer_city) AS unique_city_count, 
       COUNT(DISTINCT customer_state) AS unique_state_count
FROM Customers;

-- 4119, 27

-- Dans l’état de Sao Paolo (SP), combien y a t il de ville différentes

SELECT COUNT(DISTINCT customer_city) AS unique_city_count
FROM Customers
WHERE customer_state ="SP" ;

-- 629

-- La table présente-t-elle des valeurs nulles? 

SELECT COUNT(*) 
FROM CUSTOMERS
WHERE customer_id IS NULL OR 
      customer_unique_id IS NULL OR 
      customer_zip_code_prefix IS NULL OR
      customer_city IS NULL OR
      customer_state IS NULL
      ;

-- 0

-- La table présente deux id, (un de jointure, l’autre comme clef primaire). Est ce que l’un de ces ID est en doublon? 

SELECT COUNT(*) FROM(
    SELECT customer_id,COUNT(*) as nb_lignes
    FROM CUSTOMERS
    GROUP BY customer_id
    HAVING nb_lignes > 1 
);

-- 0

SELECT COUNT(*) FROM(
    SELECT customer_unique_id, COUNT(*) as nb_lignes
    FROM CUSTOMERS
    GROUP BY customer_unique_id
    HAVING nb_lignes > 1 
);

-- 2997

-- Quelle est la relation théorique entre customers et orders (one to many ou many to one)?

-- theorie: one to many
-- en vrai one to one


-- A partir de l’analyse précédente, calculez le nombre réel de client par état (state)

SELECT customer_state , COUNT(DISTINCT customer_unique_id) as nb_client
FROM CUSTOMERS
GROUP BY customer_state
ORDER BY nb_client DESC


-- SP|40302
-- RJ|12384
-- MG|11259
-- RS|5277
-- PR|4882
-- SC|3534
-- BA|3277
-- DF|2075
-- ES|1964
-- GO|1952
-- PE|1609
-- CE|1313
-- PA|949
-- MT|876
-- MA|726
-- MS|694
-- PB|519
-- PI|482
-- RN|474
-- AL|401
-- SE|342
-- TO|273
-- RO|240
-- AM|143
-- AC|77
-- AP|67
-- RR|45