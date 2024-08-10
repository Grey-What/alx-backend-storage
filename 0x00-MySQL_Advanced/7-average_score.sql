-- stored prcedure that computes and store the average score for a student
-- table initialization file - 7-init.sql
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
	DECLARE student_average DECIMAL(10,2);

	SELECT AVG(score) INTO student_average
	FROM corrections
	WHERE corrections.user_id = user_id;

	UPDATE users
	SET users.average_score = student_average
	WHERE users.id = user_id;
END;
//

DELIMITER ;
