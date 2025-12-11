INSERT INTO accounts_subject ("SubjectID", "SubjectName", "SubjectDescription")
VALUES
    (0, 'Git', 'Version control system used for tracking changes in source code.'),
    (1, 'Docker', 'Platform to develop, ship, and run applications in containers.');

INSERT INTO accounts_course ("CourseID", "SubjectID_id", "CourseTitle", "CourseDescription", "CourseDifficulty")
VALUES
    (10, 0, 'Intro to Git', 'Learn the basics of Git: repositories, commits, branches, and remotes.', 1),
    (11, 0, 'Advanced Git', 'Deep dive into advanced Git workflows, rebasing, and conflict resolution.', 2),

    (20, 1, 'Intro to Docker', 'Introduction to containers, images, and Docker CLI basics.', 1),
    (21, 1, 'Advanced Docker', 'Advanced Docker networking, volumes, and production deployments.', 2);

