
delimiter $$
CREATE PROCEDURE check_user_info(IN user_name VARCHAR(50), OUT user_password VARCHAR(20))
BEGIN
	SELECT user_table.password INTO user_password FROM user_table WHERE user_table.user_name = user_name;
END $$
delimiter ;

delimiter $$
CREATE PROCEDURE register(IN user_name VARCHAR(50), IN user_password VARCHAR(20), OUT succeed INT)
proc: BEGIN
	DECLARE num INT;
	SELECT COUNT(*) INTO num FROM user_table WHERE user_table.user_name = user_name;
	IF num > 0 THEN
			SET succeed = 0;
			LEAVE proc;
	END IF;
	SET succeed = 1;
	INSERT INTO user_table 
	(user_table.user_name, user_table.password, user_table.likes) 
	VALUES 
	(user_name, user_password, 0);
END $$
delimiter ;

delimiter $$
CREATE PROCEDURE update_star(IN answer_id INT)
BEGIN
	DECLARE star INT;
	SELECT answer_table.likes INTO star FROM answer_table WHERE answer_table.a_id = answer_id;
	SET star = star + 1;
	UPDATE answer_table SET answer_table.likes = star WHERE answer_table.a_id = answer_id;
END $$
delimiter ;

delimiter $$
CREATE PROCEDURE delete_answer(IN answer_id INT)
BEGIN
	DELETE FROM answer_table WHERE answer_table.a_id = answer_id;
END $$
delimiter ;


delimiter $$
CREATE PROCEDURE get_questions()
BEGIN
	DROP TABLE IF EXISTS temporary_question_table;
	CREATE TEMPORARY TABLE temporary_question_table
	SELECT question_table.q_id, question_table.title, question_table.content, user_table.user_name
	FROM question_table, user_table
	WHERE question_table.user_id = user_table.user_id;
END $$
delimiter ;
