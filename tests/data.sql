INSERT INTO users (username, password)
VALUES
  ('aqa_test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('aqa_test2', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO macros (user_id, tdee, protein, carbo, fat)
VALUES
    (1, 2264, 127, 269, 75),
    (2, 2000, 100, 200, 70);

INSERT INTO users_data (user_id, age, gender, weight, height, goal, date)
VALUES
    (1, 28, 'Male', 73, 173, 'Lose weight', '10/08/2021'),
    (2, 29, 'Female', 50, 160, 'Gain weight', '11/09/2021');