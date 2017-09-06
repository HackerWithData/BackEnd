CREATE TRIGGER update_objects_rating AFTER UPDATE ON review_review
  When (NEW.review_status = 'A')
  BEGIN
  UPDATE ratings_rating
  SET
    ratings_rating.count = ratings_rating.count+1,
    ratings_rating.total = ratings_rating.total +(SELECT  rur.rating_score FROM ratings_userrating as rur WHERE NEW.review_id = rur.review_id and rur.rating_type='Q')
  WHERE
   NEW.contractor_id = ratings_rating.contractor_id and ratings_rating.rating_type= 'Q';
END;


CREATE TRIGGER update_objects_rating AFTER UPDATE ON review_review
  When (NEW.review_status = 'A')
  BEGIN
  UPDATE ratings_rating
  SET
    ratings_rating.count = ratings_rating.count+1,
    ratings_rating.total = ratings_rating.total +(SELECT  rur.rating_score FROM ratings_userrating as rur WHERE NEW.review_id = rur.review_id and rur.rating_type='L')
  WHERE
   NEW.contractor_id = ratings_rating.contractor_id and ratings_rating.rating_type= 'L';
END;


CREATE TRIGGER update_objects_rating AFTER UPDATE ON review_review
  When (NEW.review_status = 'A')
  BEGIN
  UPDATE ratings_rating
  SET
    ratings_rating.count = ratings_rating.count+1,
    ratings_rating.total = ratings_rating.total +(SELECT  rur.rating_score FROM ratings_userrating as rur WHERE NEW.review_id = rur.review_id and rur.rating_type='E')
  WHERE
   NEW.contractor_id = ratings_rating.contractor_id and ratings_rating.rating_type= 'E';
END;
--
-- CREATE TRIGGER update_objects_rating AFTER UPDATE ON review_review
--   When (NEW.review_status = 'A')
--   BEGIN
--   UPDATE ratings_rating
--   SET
--     ratings_rating.count = ratings_rating.count+1,
--     ratings_rating.total = ratings_rating.total + A.rating_score
--   FROM
--   (SELECT rur.rating_type, rur.rating_score,New.contractor_id FROM ratings_userrating as rur WHERE NEW.review_id = rur.review_id ) as A
--   WHERE A.rating_type = ratings_rating.rating_type
-- END;