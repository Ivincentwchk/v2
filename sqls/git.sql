INSERT INTO accounts_question ("QuestionID", "CourseID_id", "QuestionDescription")
VALUES
    (101, 10, 'Which command is used to initialize a new Git repository in the current directory?'),
    (102, 10, 'How do you stage changes for the next commit in Git?'),
    (103, 10, 'Which command is used to view the commit history?'),
    (104, 10, 'Which command is used to record staged changes to the repository?'),
    (105, 10, 'What is the primary branch in a Git repository traditionally called?');

INSERT INTO accounts_question ("QuestionID", "CourseID_id", "QuestionDescription")
VALUES
    (111, 11, 'How do you create a new branch and switch to it in one command?'),
    (112, 11, 'Which command is used to download changes from a remote repository and integrate them into your current local branch?'),
    (113, 11, 'Which command is used to upload local branch commits to the remote repository?'),
    (114, 11, 'What does the ''staging area'' (or index) in Git represent?'),
    (115, 11, 'Which command would you use to discard unstaged changes in your working directory and revert a file to its last committed state?');

INSERT INTO accounts_option ("OptionID", "QuestionID_id", "OptionText", "CorrectOption")
VALUES
    (10101, 101, 'git start',  FALSE),
    (10102, 101, 'git new',    FALSE),
    (10103, 101, 'git init',   TRUE),
    (10104, 101, 'git create', FALSE);

INSERT INTO accounts_option ("OptionID", "QuestionID_id", "OptionText", "CorrectOption")
VALUES
    (10201, 102, 'git save <file>',  FALSE),
    (10202, 102, 'git add <file>',   TRUE),
    (10203, 102, 'git track <file>', FALSE),
    (10204, 102, 'git stage <file>', FALSE);

INSERT INTO accounts_option ("OptionID", "QuestionID_id", "OptionText", "CorrectOption")
VALUES
    (10301, 103, 'git status',  FALSE),
    (10302, 103, 'git diff',    FALSE),
    (10303, 103, 'git log',     TRUE),
    (10304, 103, 'git history', FALSE);

INSERT INTO accounts_option ("OptionID", "QuestionID_id", "OptionText", "CorrectOption")
VALUES
    (10401, 104, 'git push',                    FALSE),
    (10402, 104, 'git commit -m ''message''',   TRUE),
    (10403, 104, 'git save -m ''message''',     FALSE),
    (10404, 104, 'git update',                  FALSE);

INSERT INTO accounts_option ("OptionID", "QuestionID_id", "OptionText", "CorrectOption")
VALUES
    (10501, 105, 'dev',     FALSE),
    (10502, 105, 'main',    FALSE),
    (10503, 105, 'master',  TRUE),
    (10504, 105, 'staging', FALSE);

INSERT INTO accounts_option ("OptionID", "QuestionID_id", "OptionText", "CorrectOption")
VALUES
    (11101, 111, 'git branch -c <branch-name>',    FALSE),
    (11102, 111, 'git checkout -b <branch-name>',  TRUE),
    (11103, 111, 'git switch -n <branch-name>',    FALSE),
    (11104, 111, 'git new-branch <branch-name>',   FALSE);

INSERT INTO accounts_option ("OptionID", "QuestionID_id", "OptionText", "CorrectOption")
VALUES
    (11201, 112, 'git pull',  TRUE),
    (11202, 112, 'git fetch', FALSE),
    (11203, 112, 'git clone', FALSE),
    (11204, 112, 'git sync',  FALSE);

INSERT INTO accounts_option ("OptionID", "QuestionID_id", "OptionText", "CorrectOption")
VALUES
    (11301, 113, 'git get',     FALSE),
    (11302, 113, 'git send',    FALSE),
    (11303, 113, 'git upload',  FALSE),
    (11304, 113, 'git push',    TRUE);

INSERT INTO accounts_option ("OptionID", "QuestionID_id", "OptionText", "CorrectOption")
VALUES
    (11401, 114, 'The directory where the final compiled code is placed.', FALSE),
    (11402, 114, 'A place to store files that should never be committed.', FALSE),
    (11403, 114, 'A temporary space to prepare and group changes before committing them.', TRUE),
    (11404, 114, 'The working directory where files are currently being edited.', FALSE);

INSERT INTO accounts_option ("OptionID", "QuestionID_id", "OptionText", "CorrectOption")
VALUES
    (11501, 115, 'git reset --hard',       FALSE),
    (11502, 115, 'git checkout -- <file>', TRUE),
    (11503, 115, 'git revert <file>',      FALSE),
    (11504, 115, 'git clean -f',           FALSE);