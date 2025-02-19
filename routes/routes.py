from flask import render_template, request, redirect, url_for, flash, session
from models.model import Student, TotalStudent,ElectoralCandidates,Admin,Dues
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def register_routes(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def student_signup():
        if request.method == 'POST':
            fullname = request.form['fullname']
            reg_number = request.form['reg_number']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

        # Validate passwords match
            if password != confirm_password:
                flash('Passwords do not match!', 'danger')
                return redirect(url_for('student_signup'))

        # Check if the student is already registered
            existing_student = Student.query.filter((Student.email == email) | (Student.reg_number == reg_number)).first()
            if existing_student:
                flash('User already registered! Please log in.', 'danger')
                return redirect(url_for('student_signup'))

        # Hash the password
            hashed_password = generate_password_hash(password)

            # Store the new student
            new_student = Student(
                fullname=fullname,
                reg_number=reg_number,
                email=email,
                password=hashed_password
            )
            db.session.add(new_student)
            db.session.commit()

            # Store user session
            session['user_id'] = new_student.id
            session['fullname'] = new_student.fullname

            flash('Signup successful!', 'success')
            return redirect(url_for('user_dashboard'))

        return render_template('user_signup.html')

    @app.route('/student_login', methods=['GET', 'POST'])
    def student_login():
        email_or_reg = request.form.get('email').strip()
        password = request.form.get('password').strip()

        if not email_or_reg or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for('user_login'))

        # Check if the user exists (either by email or registration number)
        student = Student.query.filter((Student.email == email_or_reg) | (Student.registration_number == email_or_reg)).first()

        if not student:
            flash("Invalid email or registration number.", "danger")
            return redirect(url_for('user_login'))

        # Check password
        if not check_password_hash(student.password, password):
            flash("Incorrect password.", "danger")
            return redirect(url_for('user_login'))

        # Login successful
        flash("Login successful!", "success")
        return redirect(url_for('user_dashboard'))  # Redirect to student dashboard

    @app.route('/user_dashboard')
    def user_dashboard():
        if 'user_id' not in session:
            flash('Please log in first!', 'danger')
            return redirect(url_for('student_signup'))

        # Fetch logged-in user details
        user = Student.query.get(session['user_id'])

        # Fetch all election candidates
        candidates = ElectoralCandidates.query.all()

        # Placeholder: Check if user has voted (Implement logic if needed)
        has_voted = False  # You can modify this based on actual vote tracking

        return render_template('user_dashboard.html', user=user, candidates=candidates, has_voted=has_voted)

    @app.route('/lecturer_adminsignup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            full_name = request.form['full_name']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            profile_picture = request.files['profile_picture']

            # Validate Password Match
            if password != confirm_password:
                flash('Passwords do not match!', 'danger')
                return redirect(url_for('signup'))

            # Check if email already exists
            existing_user = Admin.query.filter_by(email=email).first()
            if existing_user:
                flash('user already registered!, please login', 'danger')
                return redirect(url_for('signup'))

            # Save Profile Picture
            filename = secure_filename(profile_picture.filename)
            profile_picture_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            profile_picture.save(profile_picture_path)

            # Hash Password
            hashed_password = generate_password_hash(password)

            # Save to Database
            new_admin = Admin(
                full_name=full_name,
                email=email,
                phone=phone,
                profile_picture=profile_picture_path,
                password=hashed_password
            )
            db.session.add(new_admin)
            db.session.commit()

            # Store user in session
            session['user_id'] = new_admin.id
            session['full_name'] = new_admin.full_name

            flash('Signup successful!', 'success')
            return redirect(url_for('lecturer_admindashboard'))

        return render_template('signup.html')

    @app.route('/lecturer_adminlogin', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email_phone = request.form['email_phone']
            password = request.form['password']

            # Check if the user exists (by email or phone)
            user = Admin.query.filter((Admin.email == email_phone) | (Admin.phone == email_phone)).first()

            if not user or not check_password_hash(user.password, password):
                flash('Invalid email/phone or password', 'danger')
                return redirect(url_for('login'))

            # Store user in session
            session['user_id'] = user.id
            session['full_name'] = user.full_name

            flash('Login successful!', 'success')
            return redirect(url_for('lecturer_admindashboard'))

        return render_template('login.html')

    @app.route('/add_students', methods=['GET', 'POST'])
    def add_students():
        # Check if an admin is logged in
        if 'user_id' not in session:
            flash("You must be logged in as an admin to access this page!", "danger")
            return redirect(url_for('login'))  # Redirect to admin login page

        # Verify the logged-in user is an admin
        admin = Admin.query.get(session['user_id'])
        if not admin:
            flash("Unauthorized access!", "danger")
            return redirect(url_for('login'))

        if request.method == 'POST':
            names = request.form.getlist('name[]')
            reg_numbers = request.form.getlist('reg_number[]')

            if not names or not reg_numbers:
                flash("Please fill in all fields!", "danger")
                return redirect(url_for('add_students'))

            for name, reg_number in zip(names, reg_numbers):
                if not name.strip() or not reg_number.strip():
                    flash("Fields cannot be empty!", "danger")
                    return redirect(url_for('add_students'))

                # Check if registration number already exists
                existing_student = TotalStudent.query.filter_by(reg_number=reg_number).first()
                if existing_student:
                    flash(f"Registration number {reg_number} already exists!", "warning")
                    return redirect(url_for('add_students'))

                new_student = TotalStudent(name=name.strip(), reg_number=reg_number.strip())
                db.session.add(new_student)

            db.session.commit()
            flash("Students successfully registered!", "success")
            return redirect(url_for('add_students'))

        return render_template('add_students.html')

    @app.route('/lecturer_admin_adddepartmental dues', methods=['GET', 'POST'])
    def dues():
        # Ensure an admin is logged in
        if 'user_id' not in session:
            flash("You must be logged in as an admin to access this page!", "danger")
            return redirect(url_for('login'))  # Redirect to admin login page

        # Verify the logged-in user is an admin
        admin = Admin.query.get(session['user_id'])
        if not admin:
            flash("Unauthorized access!", "danger")
            return redirect(url_for('login'))

        if request.method == 'POST':
            session_data = request.form.get('session')
            students = Student.query.all()

            for student in students:
                student_name = request.form.get(f'name_{student.id}')
                reg_number = request.form.get(f'reg_number_{student.id}')
                status = request.form.get(f'status_{student.id}')

                if not (student_name and reg_number and status):
                    flash("All fields are required!", "danger")
                    return redirect(url_for('dues'))

                # Check if dues record already exists for this student in the same session
                existing_due = Dues.query.filter_by(student_id=student.id, session=session_data).first()
                if existing_due:
                    existing_due.status = status  # Update status
                else:
                    new_due = Dues(
                        student_id=student.id,
                        student_name=student_name,
                        reg_number=reg_number,
                        session=session_data,
                        status=status
                    )
                    db.session.add(new_due)

            db.session.commit()
            flash("Dues updated successfully!", "success")
            return redirect(url_for('dues'))

        students = Student.query.all()
        return render_template('departmental_dues.html', students=students)

    @app.route('/lecturer_admindashboard')
    def lecturer_admindashboard():
        if 'user_id' not in session:
            flash('Please log in first!', 'danger')
            return redirect(url_for('signup'))

        return render_template('dashboard.html', full_name=session.get('full_name'))

    @app.route('/lecturer_adminadd_contestants', methods=['GET', 'POST'])
    def add_contestants():
        if 'user_id' not in session:
            flash("You must be logged in as an admin to access this page!", "danger")
            return redirect(url_for('login'))

        admin = Admin.query.get(session['user_id'])
        if not admin:
            flash("Unauthorized access!", "danger")
            return redirect(url_for('login'))

        if request.method == 'POST':
            election_period = request.form['election_period']
            position = request.form['position']
            candidate1_name = request.form['candidate1_name']
            candidate1_reg_no = request.form['candidate1_reg_no']
            candidate2_name = request.form['candidate2_name']
            candidate2_reg_no = request.form['candidate2_reg_no']

            candidate1_picture = request.files['candidate1_picture']
            candidate2_picture = request.files['candidate2_picture']

            # Validate all fields are filled
            if not all([election_period, position, candidate1_name, candidate1_reg_no, candidate1_picture, candidate2_name, candidate2_reg_no, candidate2_picture]):
                flash("All fields are required!", "danger")
                return redirect(url_for('add_contestants'))

            # Validate file types
            if not (allowed_file(candidate1_picture.filename) and allowed_file(candidate2_picture.filename)):
                flash("Only PNG, JPG, and JPEG files are allowed!", "danger")
                return redirect(url_for('add_contestants'))

            # Securely save images
            candidate1_filename = secure_filename(candidate1_picture.filename)
            candidate1_path = os.path.join(app.config['UPLOAD_FOLDER'], candidate1_filename)
            candidate1_picture.save(candidate1_path)

            candidate2_filename = secure_filename(candidate2_picture.filename)
            candidate2_path = os.path.join(app.config['UPLOAD_FOLDER'], candidate2_filename)
            candidate2_picture.save(candidate2_path)

            # Save to database
            new_candidate = ElectoralCandidates(
                election_period=election_period,
                position=position,
                candidate1_name=candidate1_name,
                candidate1_reg_no=candidate1_reg_no,
                candidate1_picture=candidate1_filename,  # Store only filename, not path
                candidate2_name=candidate2_name,
                candidate2_reg_no=candidate2_reg_no,
                candidate2_picture=candidate2_filename,  # Store only filename, not path
                created_by=session['user_id']
            )

            db.session.add(new_candidate)
            db.session.commit()

            flash("Electoral candidates added successfully!", "success")
            return redirect(url_for('lecturer_admindashboard'))

        return render_template('contestants.html')


    @app.route('/lecturer_adminelection_process')
    def election_process():
        if 'user_id' not in session:
            flash('You must be logged in to access this page.', 'danger')
            return redirect(url_for('login'))

        # Check if the logged-in user is an admin
        admin = Admin.query.get(session['user_id'])
        if not admin:
            flash('You are not authorized to access this page.', 'danger')
            return redirect(url_for('home'))  # Redirect non-admin users to home or another page

        # Fetch contestants from the database
        contestants = ElectoralCandidates.query.all()

        return render_template('electionprocess.html', contestants=contestants)

    @app.route('/edit_candidate/<int:id>', methods=['GET', 'POST'])
    def edit_candidate(id):
        contestant = ElectoralCandidates.query.get_or_404(id)

        if request.method == 'POST':
            contestant.election_period = request.form['election_period']
            contestant.position = request.form['position']
            contestant.candidate1_name = request.form['candidate1_name']
            contestant.candidate1_reg_no = request.form['candidate1_reg_no']
            contestant.candidate2_name = request.form['candidate2_name']
            contestant.candidate2_reg_no = request.form['candidate2_reg_no']

            db.session.commit()
            flash('Candidate details updated successfully!', 'success')
            return redirect(url_for('election_process'))

        return render_template('edit_candidate.html', contestant=contestant)

    @app.route('/delete_candidate/<int:id>', methods=['POST'])
    def delete_candidate(id):
        contestant = ElectoralCandidates.query.get_or_404(id)
        db.session.delete(contestant)
        db.session.commit()
        flash('Candidate deleted successfully!', 'success')
        return redirect(url_for('election_process'))
    @app.route('/submit_vote', methods=['POST'])
    def submit_vote():
        # Your voting logic here
        return redirect(url_for('user_dashboard'))

    @app.route('/admin_logout')
    def logout():
        session.clear()
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))
