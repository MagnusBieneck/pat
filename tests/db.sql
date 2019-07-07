PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
INSERT INTO auth_user VALUES(1,'pbkdf2_sha256$150000$SpymXIjrYjmm$1n9kwWbwPXId0XTk9Z6+iZZfIptLe7QjEheKc8RJtpc=',NULL,0,'tester-standard','Standard','',0,1,'2019-07-01 15:16:23.567559','Tester');
INSERT INTO auth_user VALUES(2,'pbkdf2_sha256$150000$dp8QxMrUw2hv$n7SH4FeKxQOAdD6vKfP6t3L476W1zpJCu5lIK5JJ1M4=',NULL,0,'tester-staff','Staff','',1,1,'2019-07-01 15:16:40.795824','Tester');
INSERT INTO auth_user VALUES(3,'pbkdf2_sha256$150000$UoSvch9xLEA9$9jz4VxLUH4zq6hDh/+RcdoEJl4YXrIUYTP4xY5+sFxU=',NULL,1,'tester-superuser','Superuser','',1,1,'2019-07-01 15:16:56.674990','Tester');
COMMIT;
