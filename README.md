Gym Workout Generator

Gym Workout Generator is a full-stack web application that builds personalised weekly gym workout plans and estimates daily calorie needs. The backend is written in Python with Flask handling routing and server connectivity, SQLite stores the exercise library and user data, and the frontend is built with HTML, CSS and JavaScript. Visitors can generate workouts and use the calorie calculator without an account, while creating an account adds the ability to save, edit and delete workout plans and export them as PDFs. The project was built to gain practical experience of full-stack development, authentication, working with databases and applying security best practices.


Features

- Workout generator with two goals (lose weight or gain muscle), 1 to 7 training days per week, two experience levels and three session lengths
- Automatic training split selection (full body, upper/lower, push/pull/legs) based on how many days per week the user trains
- Per-exercise sets, reps or duration and time, plus an estimated total time for every session
- Weight loss plans automatically include cardio, with time estimates shown both with and without it
- Calorie calculator that estimates daily caloric intake from body stats and activity level
- Account system with sign up, login, remember me, logout, change username and full account deletion
- Saved workout library where logged in users can save, view, edit, re-save, delete and download workouts
- In-browser plan editing with live recalculation of session times
- Dark and light themes, plus in-app privacy policy and terms of service pages


How workout generation works

The generator takes four inputs: goal, days per week, experience level and preferred session length. Exercises are read from a SQLite exercise library of 30 exercises, each tagged with a muscle group, experience level and training goal, and filtered to match the user's choices. The beginner option restricts the pool to beginner exercises only, while the experienced option uses the entire library. For weight loss plans, strength work still comes from the muscle building pool and cardio is added separately.

Days per week maps to a standard training split. One day gives a full body session, two days give upper and lower, three days give push, pull and legs, four days repeat upper and lower twice, five days combine upper, lower, push, pull and legs, six days repeat push, pull and legs twice, and seven days cover the whole week. If the days value is ever invalid or missing, the generator falls back to a three-day split instead of crashing.

Each split targets defined muscle groups. Push covers chest, shoulders and triceps, pull covers back and biceps, and legs covers quads, hamstrings, glutes and calves. Short sessions get 4 exercises, medium sessions get 6 and long sessions get 8, spread evenly across the day's muscle groups with at least two exercises per group and no repeated lift within a day. Sets and reps vary by muscle group, for example hamstrings and calves get 2 sets of 8 to 12 reps, arms and back get 3 sets of 8 to 15 reps, and the remaining muscles get 3 sets of 8 to 12 reps.

Timing is estimated at roughly 6 minutes per exercise plus about a minute of rest per set. Sessions are trimmed to fit a cap of around 30, 45 or 60 minutes depending on the chosen length, and built-in failsafes make sure no day is ever generated empty and that a missing database raises a clear error rather than a silent failure. For weight loss goals each day also gets 1 or 2 random cardio exercises of 15 to 30 minutes, and the session totals are reported both with and without cardio.


How the calorie calculator works

The calculator estimates total daily energy expenditure in two steps. First it calculates basal metabolic rate with the Mifflin-St Jeor equation. For men the formula is 10 times weight in kg, plus 6.25 times height in cm, minus 5 times age, plus 5. For women the same formula ends in minus 161 instead of plus 5.

The basal metabolic rate is then multiplied by an activity factor: 1.2 for sedentary, 1.375 for lightly active (exercise 1 to 3 times a week), 1.55 for moderately active (4 to 5 times a week), 1.725 for active (daily exercise or intense exercise 3 to 4 times a week), 1.9 for very active (intense exercise 5 to 6 times a week) and 2.0 for extra active (intense exercise daily or a physical labour job). The result is rounded and displayed as the estimated daily caloric intake in KCAL.

The form enforces sensible input ranges (weight 45 to 140 kg, height 150 to 200 cm and age 19 to 78), and the calculation is sent in the background and returned as JSON so the answer appears instantly without reloading the page.


Outputs

The workout plan page opens with a summary of the chosen goal, days per week, experience level and session length. Below that, day tabs let the user move between training days while rest days are greyed out. Each day shows the muscle focus and a table of exercises with sets, reps or duration and time, followed by an estimated workout time. Weight loss plans also show a second estimate including cardio. Cards at the bottom list rest days and the full weekly schedule, so the user can see which split falls on which day at a glance.

The calorie calculator shows a single figure in KCAL beneath the form. Saved workouts are labelled in plain English, for example a plan might be labelled as Gain Muscle, 6 days per week, medium length, adept, push/pull/legs, along with the date it was saved. Any saved workout can be downloaded as a clean, printable PDF generated with fpdf2. The PDF contains the plan itself only, with day-by-day exercise tables and estimated session times, and no account or preference data.


Accounts and data handling

The app uses two separate SQLite databases. The exercise database ships with the repository as read-only content and holds 30 exercises, covering major muscle groups plus 5 cardio machines with fixed durations. The accounts database is created automatically at first launch and holds two tables: users, with an id, username and password hash, and saved workouts, with the user id, preferences, the workout stored as JSON and a timestamp.

Usernames must be 3 to 10 characters, may contain at most one special character and must be unique. Passwords must be 5 to 10 characters and contain at least one number and one special character. Passwords are never stored in plain text. Each account gets a fresh random 16-byte salt, and the password is hashed with PBKDF2-HMAC-SHA256 using 100,000 iterations. Login verification re-derives the hash from the submitted password and compares it with the stored value, and any verification error fails closed rather than open.

Login state is kept in a hardened session cookie, with a remember me option that keeps the session alive across browser restarts. Every saved workout query is scoped to the logged in user's id on the server, so users can only ever reach their own data. Changing a username requires the current password and passes the same validation rules, and deleting an account logs the user out, removes all saved workouts and then deletes the user record for a complete data wipe. Guests can use the generator and calorie calculator freely, and only saving requires an account.


Security

- CSRF protection on every form and background request, implemented with Flask-WTF
- Rate limiting on sensitive endpoints with Flask-Limiter: 5 requests per minute for sign up, login, username changes and account deletion, and 10 per minute for saving and deleting workouts
- Salted password hashing with PBKDF2-HMAC-SHA256 at 100,000 iterations
- Parameterised SQL queries throughout, so user input is never concatenated into database statements
- Session cookies set to HttpOnly and SameSite Lax so they cannot be read by client-side scripts or sent cross-site
- The SECRET_KEY is read from the environment at startup and the app refuses to launch without it
- All workout data is validated on the server before it is stored, and malformed payloads are rejected with a 400 response
- Template output is escaped automatically by Jinja2 to prevent cross-site scripting
- Ownership checks on every saved workout route so users cannot view, edit or delete each other's plans


Requirements

- Python 3.9 or newer and pip
- Windows, macOS or Linux
- The main packages are pinned in requirements.txt: Flask 3.1.3 as the web framework, Flask-WTF 1.3.0 for CSRF protection, Flask-Limiter 4.1.1 for rate limiting and fpdf2 2.8.9 for PDF export, along with support libraries such as Werkzeug, Jinja2, WTForms and itsdangerous


Installation and running

Clone the repository from https://github.com/Vansh6248/Gym-Workout-Generator and open the project folder. Create a virtual environment with python -m venv venv and activate it, using venv\Scripts\activate on Windows or source venv/bin/activate on macOS and Linux. Install the dependencies with pip install -r requirements.txt. Before starting, set the SECRET_KEY environment variable to a strong random value, for example with export SECRET_KEY=your-random-value on macOS and Linux or $env:SECRET_KEY=your-random-value in PowerShell. The app refuses to start without it. Launch the app with python app.py and open http://localhost:5000 in a browser. Running it this way starts Flask's development server with debug mode on, which is only suitable for development; for deployment, use a production server such as Gunicorn or Waitress with debug mode off behind HTTPS. The exercise database is already populated, but running python populate_database.py resets it to the original 30 exercises by dropping and recreating the exercises table.


Project structure

- app.py sets up Flask, defines the routes and applies the security configuration
- auth.py handles sign up, login, password hashing and account management
- workout_generator.py contains the workout generation logic
- calorie_calculator.py calculates basal metabolic rate and daily calorie estimates
- saved_workouts.py stores, validates and labels saved workouts and builds the PDF export
- database.py provides SQLite helper functions
- populate_database.py seeds the exercise database
- exercise_database.db and accounts.db are the two SQLite databases
- templates holds the Jinja2 pages and static/css holds the styling
- requirements.txt pins the Python dependencies


Development notes

The codebase is split into small modules with single responsibilities, so authentication, generation, calculation and storage can each be changed or tested on their own. Input is always validated on the server as well as the browser, and security is layered rather than relying on a single control. Building the project covered the full workflow of designing a database schema, writing the backend logic, connecting it to a frontend and hardening it against common attacks, which is the main reason I chose to build it.

This application provides general fitness estimates only and is not medical advice. Consult a qualified professional before starting a new exercise or nutrition programme.
