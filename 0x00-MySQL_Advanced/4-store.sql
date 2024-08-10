-- a trigger that decreases the quantity of an item after adding a new order
-- Quantity in the table can be negative
-- table initialization file - 4-init.sql
DELIMITER //

CREATE TRIGGER quantity_adjust
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
	UPDATE items
	SET quantity = quantity - NEW.number
	WHERE name = NEW.item_name;
END;
//

DELIMITER ;
