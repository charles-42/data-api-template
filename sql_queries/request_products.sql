-- Commencez par déterminer combien il y a de commandes 
-- pour chaque quantité de photos dans la description

SELECT  product_photos_qty, COUNT(*)
FROM OrderItem A
LEFT JOIN Products B
USING (product_id)
GROUP BY B.product_photos_qty
ORDER BY product_photos_qty DESC
LIMIT 10
;


-- On voit qu'au-delà de 6 photos le nombre de commandes est marginal. 
-- Modifiez la requete pour replacer toutes les valeurs supérieurs à 7 par le chiffre 7.
SELECT  product_photos_qty_bin, COUNT(*)
FROM (
SELECT  A.order_id, CASE WHEN B.product_photos_qty > 6 THEN 7 ELSE B.product_photos_qty END AS product_photos_qty_bin
FROM OrderItem A
LEFT JOIN Products B
USING (product_id)
)
GROUP BY product_photos_qty_bin
ORDER BY product_photos_qty_bin DESC
;
