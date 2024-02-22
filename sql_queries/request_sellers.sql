-- Réunissez sur une même table dont chaque ligne correspond à un order item:
-- le prix du produit: order_item
-- la catégorie du produit en anglais : categorie_name_translation
-- le pays du vendeur: seller
-- le pays de l’acheteur: custumer
-- la date de vente: order

DROP TABLE IF EXISTS LocalSales;
CREATE TABLE IF NOT EXISTS LocalSales AS 

WITH product_name AS (
SELECT a.product_id, b.product_category_name_english 
FROM Products a
LEFT JOIN ProductCategoryName b ON a.product_category_name =b.product_category_name
)

SELECT A.order_id,  B.product_category_name_english, C.order_purchase_timestamp, D.customer_state, E.seller_state
FROM OrderItem A
LEFT JOIN product_name B USING (product_id)
LEFT JOIN Orders C ON A.order_id = C.order_id
LEFT JOIN Customers D ON C.customer_id = D.customer_id
LEFT JOIN Sellers E ON A.seller_id = E.seller_id
;


-- A partir de la table précédente créée deux nouvelles colonnes.
-- Une colonne “local_value” Si le pays du vendeur est le même que le pays de l’acheteur 
-- alors cette nouvelle colonne prendra comme valeur “local” 
-- s’ils sont différents la valeurs sera “inter-étatique”

-- Une colonne “local_indicatrice” qui suit la même règle mais qui prendra 
-- la valeur 1 si l’état du vendeur et de l’acheteur sont les mêmes 
-- ou 0 autrement.

ALTER TABLE LocalSales
ADD COLUMN local_value TEXT;
ALTER TABLE LocalSales
ADD COLUMN local_indicatrice INTEGER;

-- Update the new column based on the comparison
UPDATE LocalSales
SET local_value = CASE WHEN customer_state = seller_state THEN 'local' ELSE 'inter-etatique' END;

UPDATE LocalSales
SET local_indicatrice = CASE WHEN customer_state = seller_state THEN 1 ELSE 0 END;

