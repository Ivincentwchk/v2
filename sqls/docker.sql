INSERT INTO accounts_question ("QuestionID", "CourseID_id", "QuestionDescription")
VALUES
    (201, 20, 'Which command is used to list all running Docker containers?'),
    (202, 20, 'Which command is used to list all Docker images on your local machine?'),
    (203, 20, 'Which command is used to download an image from Docker Hub?'),
    (204, 20, 'Which command is used to start a new container from an image?'),
    (205, 20, 'Which command is used to stop a running Docker container?');

INSERT INTO accounts_question ("QuestionID", "CourseID_id", "QuestionDescription")
VALUES
    (211, 21, 'Which command is used to build a Docker image from a Dockerfile?'),
    (212, 21, 'Which command is used to view the logs of a running or stopped container?'),
    (213, 21, 'Which command is used to remove a stopped container?'),
    (214, 21, 'Which command is used to remove an image from your local Docker registry?'),
    (215, 21, 'Which command is used to see real-time resource usage statistics of containers?');

-- pattern of correct option indexes by question:
-- 201→4, 202→2, 203→1, 204→3, 205→1, 211→4, 212→3, 213→4, 214→1, 215→2

INSERT INTO accounts_option ("OptionID", "QuestionID_id", "OptionText", "CorrectOption")
VALUES
    (20101, 201, 'docker ps',        FALSE),
    (20102, 201, 'docker list',      FALSE),
    (20103, 201, 'docker images',    FALSE),
    (20104, 201, 'docker ps',        TRUE);

INSERT INTO accounts_option ("OptionID", "QuestionID_id", "OptionText", "CorrectOption")
VALUES
    (20201, 202, 'docker ps',        FALSE),
    (20202, 202, 'docker images',    TRUE),
    (20203, 202, 'docker list-img',  FALSE),
    (20204, 202, 'docker inspect',   FALSE);

INSERT INTO accounts_option ("OptionID", "QuestionID_id", "OptionText", "CorrectOption")
VALUES
    (20301, 203, 'docker pull <image>', TRUE),
    (20302, 203, 'docker clone <image>',FALSE),
    (20303, 203, 'docker get <image>',  FALSE),
    (20304, 203, 'docker fetch <image>',FALSE);

INSERT INTO accounts_option ("OptionID", "QuestionID_id", "OptionText", "CorrectOption")
VALUES
    (20401, 204, 'docker start <image>', FALSE),
    (20402, 204, 'docker create <image>',FALSE),
    (20403, 204, 'docker run <image>',   TRUE),
    (20404, 204, 'docker boot <image>',  FALSE);

INSERT INTO accounts_option ("OptionID", "QuestionID_id", "OptionText", "CorrectOption")
VALUES
    (20501, 205, 'docker stop <container>', TRUE),
    (20502, 205, 'docker kill <container>', FALSE),
    (20503, 205, 'docker end <container>',  FALSE),
    (20504, 205, 'docker pause <container>',FALSE);

INSERT INTO accounts_option ("OptionID", "QuestionID_id", "OptionText", "CorrectOption")
VALUES
    (21101, 211, 'docker make -f Dockerfile .', FALSE),
    (21102, 211, 'docker compile Dockerfile',   FALSE),
    (21103, 211, 'docker image create .',       FALSE),
    (21104, 211, 'docker build -t <name> .',    TRUE);

INSERT INTO accounts_option ("OptionID", "QuestionID_id", "OptionText", "CorrectOption")
VALUES
    (21201, 212, 'docker status <container>', FALSE),
    (21202, 212, 'docker output <container>', FALSE),
    (21203, 212, 'docker logs <container>',   TRUE),
    (21204, 212, 'docker show <container>',   FALSE);

INSERT INTO accounts_option ("OptionID", "QuestionID_id", "OptionText", "CorrectOption")
VALUES
    (21301, 213, 'docker delete <container>',FALSE),
    (21302, 213, 'docker remove-ctn <id>',   FALSE),
    (21303, 213, 'docker purge <container>', FALSE),
    (21304, 213, 'docker rm <container>',    TRUE);

INSERT INTO accounts_option ("OptionID", "QuestionID_id", "OptionText", "CorrectOption")
VALUES
    (21401, 214, 'docker rmi <image>',    TRUE),
    (21402, 214, 'docker rm <image>',     FALSE),
    (21403, 214, 'docker delete <image>', FALSE),
    (21404, 214, 'docker drop <image>',   FALSE);

INSERT INTO accounts_option ("OptionID", "QuestionID_id", "OptionText", "CorrectOption")
VALUES
    (21501, 215, 'docker monitor', FALSE),
    (21502, 215, 'docker stats',   TRUE),
    (21503, 215, 'docker top',     FALSE),
    (21504, 215, 'docker usage',   FALSE);