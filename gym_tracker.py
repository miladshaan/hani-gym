# gym_tracker.py - ULTIMATE PERSONAL VERSION
# Hani's Personal Gym Tracker with AI Suggestions & Progress Analytics
# Birthday Gift with Love from Your Babe 💝

import streamlit as st
import pandas as pd
import datetime
import random
import hashlib
from io import BytesIO
import matplotlib.pyplot as plt
import os

# Page configuration
st.set_page_config(
    page_title="Hani's Smart Gym Tracker",
    page_icon="💪🎁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Personal encouraging messages with "babe"
ENCOURAGING_MESSAGES = [
    "I love watching you crush your goals, babe!",
    "I'm so proud of you! Keep going, 7bibi!",
    "You're getting stronger every day, my love!",
    "Your dedication inspires me, habibi!",
    "Happy Birthday, babe! This is just the beginning of your fitness journey!",
    "You've got this, babe! So proud of you!",
    "Every rep brings you closer to your goals - I believe in you, my love!",
    "Looking strong, babe! Can't wait to see your progress!",
    "You're amazing, babe! Keep up the great work!",
    "So proud of my strong man! Love you, babe! 💪"
]

# Comprehensive exercise database with images and descriptions
EXERCISE_DATABASE = {
    "💪 Chest Day": {
        "Bench Press": {
            "image": "https://img.icons8.com/color/100/000000/bench-press.png",
            "description": "Lie on bench, lower bar to chest, push up explosively"
        },
        "Incline Bench Press": {
            "image": "https://img.icons8.com/color/100/000000/weightlift.png",
            "description": "Bench at 45-degree angle, targets upper chest"
        },
        "Chest Fly": {
            "image": "https://img.icons8.com/color/100/000000/chest-fly.png",
            "description": "Lie on bench, arms extended, bring dumbbells together in arc motion"
        },
        "Push-ups": {
            "image": "https://img.icons8.com/color/100/000000/pushups.png",
            "description": "Bodyweight exercise, great for chest and core"
        },
        "Dumbbell Press": {
            "image": "https://img.icons8.com/color/100/000000/dumbbell.png",
            "description": "Similar to bench press but with dumbbells for better range"
        },
        "Cable Crossovers": {
            "image": "https://img.icons8.com/color/100/000000/cable-crossover.png",
            "description": "Stand between cable machines, cross arms in front of chest"
        }
    },
    "🦵 Leg Day": {
        "Squat": {
            "image": "https://img.icons8.com/color/100/000000/squat.png",
            "description": "Barbell on shoulders, lower until thighs parallel to floor"
        },
        "Deadlift": {
            "image": "https://img.icons8.com/color/100/000000/deadlift.png",
            "description": "Lift barbell from floor to hip level, keep back straight"
        },
        "Leg Press": {
            "image": "https://img.icons8.com/color/100/000000/leg-press.png",
            "description": "Sit on machine, push weight away with legs"
        },
        "Lunges": {
            "image": "https://img.icons8.com/color/100/000000/lunges.png",
            "description": "Step forward, lower hips until both knees bent at 90 degrees"
        },
        "Leg Extensions": {
            "image": "https://img.icons8.com/color/100/000000/leg-extension.png",
            "description": "Seated machine exercise targeting quadriceps"
        },
        "Hamstring Curls": {
            "image": "https://img.icons8.com/color/100/000000/hamstring-curl.png",
            "description": "Lying or seated machine for hamstrings"
        },
        "Calf Raises": {
            "image": "https://img.icons8.com/color/100/000000/calf-raise.png",
            "description": "Raise heels off ground, target calf muscles"
        }
    },
    "🏋️ Shoulders": {
        "Shoulder Press": {
            "image": "https://img.icons8.com/color/100/000000/shoulder-press.png",
            "description": "Press weight overhead while seated or standing"
        },
        "Lateral Raises": {
            "image": "https://img.icons8.com/color/100/000000/lateral-raise.png",
            "description": "Raise dumbbells sideways to shoulder height"
        },
        "Front Raises": {
            "image": "https://img.icons8.com/color/100/000000/front-raise.png",
            "description": "Raise dumbbells in front to shoulder height"
        },
        "Shrugs": {
            "image": "https://img.icons8.com/color/100/000000/shrugs.png",
            "description": "Lift shoulders toward ears with weights in hands"
        },
        "Upright Rows": {
            "image": "https://img.icons8.com/color/100/000000/upright-row.png",
            "description": "Pull barbell vertically to chin level"
        }
    },
    "💪 Back Day": {
        "Pull-ups": {
            "image": "https://img.icons8.com/color/100/000000/pull-up.png",
            "description": "Hang from bar, pull body up until chin over bar"
        },
        "Lat Pulldown": {
            "image": "https://img.icons8.com/color/100/000000/lat-pulldown.png",
            "description": "Seated machine, pull bar down to chest"
        },
        "Bent-over Rows": {
            "image": "https://img.icons8.com/color/100/000000/bent-over-row.png",
            "description": "Bend forward, pull barbell to lower chest"
        },
        "T-Bar Rows": {
            "image": "https://img.icons8.com/color/100/000000/t-bar-row.png",
            "description": "Machine exercise for middle back thickness"
        },
        "Seated Rows": {
            "image": "https://img.icons8.com/color/100/000000/seated-row.png",
            "description": "Cable machine exercise for back width"
        }
    },
    "💪 Arms": {
        "Bicep Curls": {
            "image": "https://img.icons8.com/color/100/000000/bicep-curl.png",
            "description": "Curl dumbbells or barbell toward shoulders"
        },
        "Tricep Extensions": {
            "image": "https://img.icons8.com/color/100/000000/tricep-extension.png",
            "description": "Extend arms overhead with weight behind head"
        },
        "Hammer Curls": {
            "image": "https://img.icons8.com/color/100/000000/hammer-curl.png",
            "description": "Curl dumbbells with palms facing each other"
        },
        "Dips": {
            "image": "https://img.icons8.com/color/100/000000/dips.png",
            "description": "Bodyweight exercise for triceps and chest"
        },
        "Preacher Curls": {
            "image": "https://img.icons8.com/color/100/000000/preacher-curl.png",
            "description": "Isolated bicep exercise using preacher bench"
        }
    },
    "🔁 Full Body": {
        "Clean and Press": {
            "image": "https://img.icons8.com/color/100/000000/clean-and-press.png",
            "description": "Olympic lift combining deadlift and overhead press"
        },
        "Kettlebell Swings": {
            "image": "https://img.icons8.com/color/100/000000/kettlebell-swing.png",
            "description": "Hip-hinge movement swinging kettlebell to chest height"
        },
        "Burpees": {
            "image": "https://img.icons8.com/color/100/000000/burpee.png",
            "description": "Full body exercise: squat, plank, push-up, jump"
        }
    }
}

# Protein shake recommendations
PROTEIN_SHAKES = {
    "Post-Workout Basic": "🥤 **Whey Protein** (30g) + Water/Milk - Perfect for muscle recovery",
    "Mass Gainer": "🏋️ **Whey Protein** (30g) + Banana + Oats + Peanut Butter + Milk - For weight gain",
    "Lean Muscle": "💪 **Isolate Protein** (25g) + Almond Milk + Spinach + Berries - Low calorie",
    "Quick Recovery": "⚡ **BCAA Protein** + Water + Honey - Fast absorption, great after intense workouts",
    "Bedtime Recovery": "🌙 **Casein Protein** + Milk - Slow release for overnight muscle repair"
}

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'user_stats' not in st.session_state:
    st.session_state.user_stats = {}
if 'weight_unit' not in st.session_state:
    st.session_state.weight_unit = "kg"  # Default unit

def hash_email(email):
    """Create a simple hash of email for personalized data storage"""
    return hashlib.md5(email.lower().encode()).hexdigest()[:10]

def generate_qr_code(url):
    """Generate QR code for the app URL with fallback"""
    try:
        import qrcode
        from PIL import Image
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buf = BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    except ImportError:
        # Fallback if QR code generation fails
        st.warning("QR code feature temporarily unavailable")
        return None
    except Exception as e:
        st.warning(f"QR code generation issue: {str(e)}")
        return None

def calculate_bmi(weight, height):
    """Calculate BMI"""
    height_m = height / 100
    return weight / (height_m ** 2)

def get_bmi_category(bmi):
    """Get BMI category"""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def is_birthday():
    """Check if today is Hani's birthday (September 29th)"""
    today = datetime.date.today()
    return today.month == 9 and today.day == 29

def get_greeting():
    """Get appropriate greeting based on whether it's his birthday"""
    if is_birthday():
        return "🎂 Happy Birthday, My Love! 🎉", "This is your special birthday gift to track your amazing progress!"
    else:
        return "Welcome back, 7bb! 💪", "Ready to crush your goals today?"

def convert_to_kg(weight, unit):
    """Convert weight to kg based on selected unit"""
    if unit == "kg":
        return weight
    elif unit == "lb":
        return weight * 0.453592  # Convert pounds to kg
    return weight

def convert_from_kg(weight, unit):
    """Convert weight from kg to selected unit"""
    if unit == "kg":
        return weight
    elif unit == "lb":
        return weight / 0.453592  # Convert kg to pounds
    return weight

def check_new_pr(exercise, weight, reps, user_data):
    """Check if this is a new personal record and return congratulatory message"""
    try:
        if user_data.empty:
            return f"🎉 First time logging {exercise}! Welcome to your fitness journey, babe! 'WOW! Eljamal bema 7amal. Good job 7bb' 💪"
        
        exercise_data = user_data[user_data['Exercise'] == exercise]
        
        if not exercise_data.empty:
            # Check for weight PR
            max_weight = exercise_data['Weight'].max()
            if weight > max_weight:
                return f"🎉 NEW PERSONAL RECORD! {exercise}: {weight}kg! 'WOW! Eljamal bema 7amal. Good job 7bb' 💪🎊"
            
            # Check for reps PR at this weight
            same_weight_data = exercise_data[exercise_data['Weight'] == weight]
            if not same_weight_data.empty:
                max_reps = same_weight_data['Reps'].max()
                if reps > max_reps:
                    return f"🎉 REPS PR! {reps} reps at {weight}kg on {exercise}! 'WOW! Eljamal bema 7amal. Good job 7bb' 💪"
        
        return None
        
    except:
        return None

def check_weight_goal(user_stats, new_weight):
    """Check if reached weight goal milestones"""
    if not user_stats or 'starting_weight' not in user_stats:
        return None
    
    starting_weight = user_stats['starting_weight']
    weight_change = new_weight - starting_weight
    
    # Define milestone thresholds (adjust as needed)
    milestones = {
        2.5: "First milestone reached!",
        5: "Amazing progress!",
        10: "Incredible transformation!",
        -2.5: "Great fat loss progress!",
        -5: "Amazing weight loss!",
        -10: "Incredible transformation!"
    }
    
    for milestone, message in milestones.items():
        if abs(weight_change) >= abs(milestone) and (weight_change * milestone) > 0:
            return f"🎯 WEIGHT GOAL ACHIEVED! {message} 'WOW! Eljamal bema 7amal. Good job 7bb' 🏆"
    
    return None

def calculate_next_weight(exercise, current_weight, reps, user_data):
    """AI-powered weight suggestion based on progress"""
    try:
        exercise_data = user_data[user_data['Exercise'] == exercise].sort_values('Date')
        if len(exercise_data) > 1:
            latest = exercise_data.iloc[-1]
            previous = exercise_data.iloc[-2]
            
            weight_increase = latest['Weight'] - previous['Weight']
            rep_increase = latest['Reps'] - previous['Reps']
            
            if reps >= 10:
                suggestion = current_weight + 2.5
                reason = f"Great job, babe! You handled {reps} reps easily. Time to level up! 💪"
            elif reps >= 6:
                suggestion = current_weight + 1.25
                reason = f"Solid performance, babe! You're ready for a small increase."
            else:
                suggestion = current_weight
                reason = f"Focus on mastering this weight, babe. Perfect your form!"
                
            return suggestion, reason
    except:
        pass
    return current_weight + 2.5, "New personal best! Keep pushing forward, babe! 🎯"

def analyze_progress(user_data, user_stats):
    """Analyze workout progress and provide insights"""
    if user_data.empty:
        return "Start logging workouts to see your progress analysis, babe!"
    
    insights = []
    
    # Most improved exercise
    progress_data = []
    for exercise in user_data['Exercise'].unique():
        ex_data = user_data[user_data['Exercise'] == exercise].sort_values('Date')
        if len(ex_data) > 1:
            improvement = ex_data['Weight'].iloc[-1] - ex_data['Weight'].iloc[0]
            progress_data.append((exercise, improvement))
    
    if progress_data:
        best_improvement = max(progress_data, key=lambda x: x[1])
        insights.append(f"🏆 **Most Improved**: {best_improvement[0]} (+{best_improvement[1]:.1f}kg)")
    
    # Recent achievements
    recent_workouts = user_data.sort_values('Date').tail(5)
    if not recent_workouts.empty:
        max_weight = recent_workouts['Weight'].max()
        max_exercise = recent_workouts[recent_workouts['Weight'] == max_weight]['Exercise'].iloc[0]
        insights.append(f"💪 **Recent PR**: {max_weight}kg on {max_exercise}")
    
    # BMI progress if available
    if 'starting_weight' in user_stats and 'current_weight' in user_stats:
        weight_change = user_stats['current_weight'] - user_stats['starting_weight']
        if weight_change > 0:
            insights.append(f"⚖️ **Weight Change**: +{weight_change:.1f}kg muscle gain! Amazing, babe!")
        elif weight_change < 0:
            insights.append(f"⚖️ **Weight Change**: {weight_change:.1f}kg fat loss! Great work, babe!")
    
    # Workout frequency
    workout_days = user_data['Date'].nunique()
    total_workouts = len(user_data)
    insights.append(f"📅 **Consistency**: {workout_days} workout days, {total_workouts} total sessions")
    
    return "\n\n".join(insights)

def get_protein_recommendation(workout_type, intensity):
    """Recommend protein shake based on workout"""
    if intensity == "High" or "Leg Day" in workout_type:
        return PROTEIN_SHAKES["Mass Gainer"]
    elif "Cardio" in workout_type:
        return PROTEIN_SHAKES["Quick Recovery"]
    else:
        return random.choice(list(PROTEIN_SHAKES.values()))

# Simplified authentication for public access
with st.sidebar:
    st.title("🎁 Welcome, Hani!")
    st.image("https://img.icons8.com/color/96/000000/dumbbell.png", width=100)
    
    # Simple name input instead of email authentication
    user_name = st.text_input("Enter your name to begin:", placeholder="Hani")
    
    if user_name:
        st.session_state.authenticated = True
        st.session_state.user_name = user_name
        st.success(f"Welcome, {user_name}!")
        
        # Weight unit selection
        st.subheader("⚖️ Weight Units")
        weight_unit = st.radio("Select weight unit:", ["kg", "lb"], index=0 if st.session_state.get('weight_unit', 'kg') == 'kg' else 1)
        if weight_unit != st.session_state.get('weight_unit', 'kg'):
            st.session_state.weight_unit = weight_unit
            st.rerun()
    else:
        st.session_state.authenticated = False
        st.info("Enter your name to start tracking!")

# Main app content
if st.session_state.authenticated:
    # Personal greeting with birthday detection
    st.title(f"💪 Hani's Smart Gym Tracker")
    
    greeting, subheader = get_greeting()
    st.subheader(greeting)
    st.write(f"**{subheader}**")
    
    # User stats setup (first time only)
    user_stats_file = f"user_stats_{st.session_state.user_name}.csv"
    try:
        user_stats_df = pd.read_csv(user_stats_file)
        if not user_stats_df.empty:
            st.session_state.user_stats = user_stats_df.iloc[-1].to_dict()
    except FileNotFoundError:
        # First-time setup
        with st.expander("📊 Setup Your Profile", expanded=True):
            st.subheader("Let's set up your profile, babe!")
            col1, col2 = st.columns(2)
            
            with col1:
                # Convert weight display based on selected unit
                weight_display = st.number_input(f"Your Current Weight ({st.session_state.weight_unit}):", 
                                               min_value=50.0, max_value=150.0, value=80.0, step=0.5)
                weight_kg = convert_to_kg(weight_display, st.session_state.weight_unit)
                
                height = st.number_input("Your Height (cm):", min_value=150, max_value=200, value=180, step=1)
            
            with col2:
                fitness_goal = st.selectbox("Your Primary Goal:", 
                                          ["Build Muscle", "Lose Fat", "Get Stronger", "Improve Fitness"])
                experience = st.selectbox("Your Experience Level:", 
                                       ["Beginner", "Intermediate", "Advanced"])
            
            if st.button("Save Profile"):
                bmi = calculate_bmi(weight_kg, height)
                bmi_category = get_bmi_category(bmi)
                
                user_stats = {
                    "Date": datetime.date.today(),
                    "starting_weight": weight_kg,
                    "current_weight": weight_kg,
                    "height": height,
                    "bmi": bmi,
                    "bmi_category": bmi_category,
                    "fitness_goal": fitness_goal,
                    "experience": experience
                }
                
                user_stats_df = pd.DataFrame([user_stats])
                user_stats_df.to_csv(user_stats_file, index=False)
                st.session_state.user_stats = user_stats
                st.success("Profile saved successfully, babe! 🎉")
                st.rerun()
    
    # Monthly weight update
    if st.session_state.user_stats:
        with st.expander("⚖️ Update Your Weight"):
            st.write("Update your weight monthly to track your progress, babe!")
            
            # Convert current weight to display unit
            current_weight_kg = st.session_state.user_stats.get('current_weight', 80.0)
            current_weight_display = convert_from_kg(current_weight_kg, st.session_state.weight_unit)
            
            new_weight_display = st.number_input(f"Current Weight ({st.session_state.weight_unit}):", 
                                               min_value=50.0, max_value=150.0, 
                                               value=float(current_weight_display),
                                               step=0.5)
            
            new_weight_kg = convert_to_kg(new_weight_display, st.session_state.weight_unit)
            
            if st.button("Update Weight"):
                st.session_state.user_stats['current_weight'] = new_weight_kg
                # Save updated stats
                updated_stats = st.session_state.user_stats.copy()
                updated_stats['Date'] = datetime.date.today()
                user_stats_df = pd.DataFrame([updated_stats])
                user_stats_df.to_csv(user_stats_file, index=False)
                
                # Check for weight milestones
                milestone_message = check_weight_goal(st.session_state.user_stats, new_weight_kg)
                if milestone_message:
                    st.balloons()
                    st.success(milestone_message)
                else:
                    st.success("Weight updated successfully, babe! 💪")
    
    # QR Code Generation with improved error handling
    with st.expander("📱 Get Mobile QR Code"):
        st.write("Scan this QR code to open the app on your phone anytime, babe!")
        
        # Use the actual Streamlit Cloud URL
        app_url = "https://hani-gym-miladshaan.streamlit.app/"
        
        qr_image = generate_qr_code(app_url)
        if qr_image:
            st.image(qr_image, caption="Scan for mobile access", width=200)
        else:
            st.info("🔗 **Direct App Link:**")
            st.success(app_url)
            st.write("💡 **Tip:** Bookmark this URL on your phone for quick access!")
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Log Workout", "🏋️ Exercise Library", "📈 View Progress", "🧠 Progress Insights", "🥤 Nutrition"])
    
    with tab1:
        st.header("Log Your Workout")
        
        with st.form("workout_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                workout_type = st.selectbox("Workout Focus:", list(EXERCISE_DATABASE.keys()))
                intensity = st.select_slider("Workout Intensity:", ["Light", "Moderate", "High"])
                
                # Exercise selection with images
                exercises = list(EXERCISE_DATABASE[workout_type].keys())
                exercise = st.selectbox("Exercise:", exercises)
                
                # Show exercise image and description
                if exercise in EXERCISE_DATABASE[workout_type]:
                    ex_info = EXERCISE_DATABASE[workout_type][exercise]
                    st.image(ex_info["image"], width=80)
                    st.caption(ex_info["description"])
            
            with col2:
                # Weight input with unit conversion
                weight_display = st.number_input(f"Weight ({st.session_state.weight_unit}):", 
                                               min_value=0.0, step=0.5, value=20.0)
                weight_kg = convert_to_kg(weight_display, st.session_state.weight_unit)
                
                reps = st.number_input("Reps:", min_value=1, max_value=50, value=8)
                sets = st.number_input("Sets:", min_value=1, max_value=10, value=3)
                notes = st.text_input("Notes:", placeholder="How did it feel, babe?")
            
            submitted = st.form_submit_button("💾 Save Workout & Get Suggestions")
            
            if submitted:
                if exercise.strip() == "":
                    st.error("Please select an exercise, babe!")
                else:
                    # Save workout
                    today = datetime.date.today()
                    user_filename = f"gym_progress_{st.session_state.user_name}.csv"
                    
                    new_entry = {
                        "Date": today,
                        "WorkoutType": workout_type,
                        "Exercise": exercise,
                        "Weight": weight_kg,  # Always store in kg
                        "Reps": reps,
                        "Sets": sets,
                        "Intensity": intensity,
                        "Notes": notes
                    }
                    
                    try:
                        user_df = pd.read_csv(user_filename)
                    except FileNotFoundError:
                        user_df = pd.DataFrame(columns=["Date", "WorkoutType", "Exercise", "Weight", "Reps", "Sets", "Intensity", "Notes"])
                    
                    user_df = pd.concat([user_df, pd.DataFrame([new_entry])], ignore_index=True)
                    user_df.to_csv(user_filename, index=False)
                    
                    # Check for new personal records
                    pr_message = check_new_pr(exercise, weight_kg, reps, user_df)
                    if pr_message:
                        st.balloons()
                        st.success(pr_message)
                    else:
                        st.success("Workout saved successfully, babe! 🎉")
                        st.balloons()
                    
                    # Personal encouragement
                    random_message = random.choice(ENCOURAGING_MESSAGES)
                    st.info(f"💌 From your babe: {random_message}")
                    
                    # AI suggestions
                    next_weight_kg, reason = calculate_next_weight(exercise, weight_kg, reps, user_df)
                    next_weight_display = convert_from_kg(next_weight_kg, st.session_state.weight_unit)
                    st.success(f"🧠 **AI Suggestion**: Try {next_weight_display:.1f}{st.session_state.weight_unit} next time! *{reason}*")
                    
                    # Protein recommendation
                    protein_shake = get_protein_recommendation(workout_type, intensity)
                    st.info(f"🥤 **Post-Workout Nutrition**: {protein_shake}")
    
    with tab2:
        st.header("🏋️ Exercise Library")
        st.write("Browse all exercises with instructions, babe!")
        
        selected_category = st.selectbox("Choose Category:", list(EXERCISE_DATABASE.keys()))
        
        exercises = EXERCISE_DATABASE[selected_category]
        for exercise_name, exercise_info in exercises.items():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(exercise_info["image"], width=100)
            with col2:
                st.subheader(exercise_name)
                st.write(exercise_info["description"])
                st.write("---")
    
    with tab3:
        st.header("Your Progress Dashboard")
        
        try:
            user_filename = f"gym_progress_{st.session_state.user_name}.csv"
            progress_df = pd.read_csv(user_filename)
            progress_df['Date'] = pd.to_datetime(progress_df['Date'])
            
            if not progress_df.empty:
                # Convert weights for display
                display_df = progress_df.copy()
                display_df['Weight_Display'] = display_df['Weight'].apply(
                    lambda x: convert_from_kg(x, st.session_state.weight_unit)
                )
                
                # Progress charts
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader(f"Weight Progression ({st.session_state.weight_unit})")
                    selected_exercise = st.selectbox("Select Exercise:", progress_df['Exercise'].unique(), key="progress_exercise")
                    
                    exercise_data = display_df[display_df['Exercise'] == selected_exercise].sort_values('Date')
                    if not exercise_data.empty:
                        st.line_chart(exercise_data, x='Date', y='Weight_Display')
                
                with col2:
                    st.subheader("Workout Distribution")
                    workout_counts = progress_df['WorkoutType'].value_counts()
                    st.bar_chart(workout_counts)
                
                # Recent workouts table
                st.subheader("Workout History")
                display_columns = ['Date', 'Exercise', 'Weight_Display', 'Reps', 'Sets']
                display_table = display_df[display_columns].copy()
                display_table = display_table.rename(columns={'Weight_Display': f'Weight ({st.session_state.weight_unit})'})
                st.dataframe(display_table.sort_values('Date', ascending=False).head(10))
            else:
                st.info("No workouts logged yet. Start by logging your first workout, babe!")
                
        except FileNotFoundError:
            st.info("No workouts logged yet. Start by logging your first workout, babe!")
    
    with tab4:
        st.header("Progress Insights & Analytics")
        
        try:
            user_filename = f"gym_progress_{st.session_state.user_name}.csv"
            user_data = pd.read_csv(user_filename)
            user_data['Date'] = pd.to_datetime(user_data['Date'])
            
            if not user_data.empty:
                # Progress analysis
                insights = analyze_progress(user_data, st.session_state.user_stats)
                st.success(insights)
                
                # Monthly progress
                st.subheader("Monthly Progress")
                user_data['Month'] = user_data['Date'].dt.to_period('M')
                monthly_progress = user_data.groupby('Month').agg({
                    'Weight': 'max',
                    'Exercise': 'count'
                }).rename(columns={'Exercise': 'Workouts'})
                
                # Convert max weight for display
                monthly_progress['Weight_Display'] = monthly_progress['Weight'].apply(
                    lambda x: convert_from_kg(x, st.session_state.weight_unit)
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.line_chart(monthly_progress['Weight_Display'])
                    st.write(f"Max Weight per Month ({st.session_state.weight_unit})")
                with col2:
                    st.bar_chart(monthly_progress['Workouts'])
                    st.write("Workouts per Month")
                    
            else:
                st.info("Log more workouts to unlock detailed insights, babe!")
                
        except FileNotFoundError:
            st.info("Start logging workouts to see your progress insights, babe!")
    
    with tab5:
        st.header("🥤 Nutrition & Recovery")
        st.subheader("Protein Shake Recommendations")
        
        st.write("**Choose based on your workout, babe:**")
        for shake_name, shake_desc in PROTEIN_SHAKES.items():
            with st.expander(f"🥤 {shake_name}"):
                st.write(shake_desc)
        
        st.subheader("💡 Nutrition Tips")
        st.write("""
        - **Hydrate well** before, during, and after workouts
        - **Eat protein** within 30 minutes after training for best recovery
        - **Carbs are fuel** - don't skip them on workout days
        - **Listen to your body**, babe - rest when needed!
        """)

else:
    # Login prompt
    st.title("🎁 Hani's Birthday Fitness Gift")
    st.subheader("💝 A Personal Gym Tracker Made with Love by Your Babe")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("""
        ### Welcome to your personalized fitness journey, babe!
        
        This special birthday gift will help you:
        
        ✅ **Track your progress** with smart analytics
        ✅ **Learn proper form** with exercise images  
        ✅ **Get nutrition advice** for optimal recovery
        ✅ **Receive personal encouragement** from your babe
        ✅ **Access anywhere** via QR code
        ✅ **Celebrate every PR** with special messages
        
        **To begin, enter your name in the sidebar, babe!**
        """)
    
    with col2:
        st.image("https://img.icons8.com/color/200/000000/dumbbell.png")
        st.write("💪 Your strength journey starts today, babe!")

# Footer
st.markdown("---")
if is_birthday():
    st.markdown("🎂 **Happy Birthday, Hani!** Made with all my love for you on your special day! 💝")
else:
    st.markdown("Made with all my love for you, Hani! Your babe is always cheering for you! 💝")