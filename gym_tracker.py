# gym_tracker.py - ULTIMATE PERSONAL VERSION v2.0
# Hani's Personal Gym Tracker with AI Suggestions, Progress Analytics & Smart Watch Integration
# Birthday Gift with Love from M.S. 💝

import streamlit as st
import pandas as pd
import datetime
import random
import hashlib
from io import BytesIO
import matplotlib.pyplot as plt
import os
import sqlite3
import json
import time
from datetime import date, timedelta

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
            "description": "Lie on bench, lower bar to chest, push up explosively",
            "calories_per_hour": 400
        },
        "Incline Bench Press": {
            "image": "https://img.icons8.com/color/100/000000/weightlift.png",
            "description": "Bench at 45-degree angle, targets upper chest",
            "calories_per_hour": 380
        },
        "Chest Fly": {
            "image": "https://img.icons8.com/color/100/000000/chest-fly.png",
            "description": "Lie on bench, arms extended, bring dumbbells together in arc motion",
            "calories_per_hour": 350
        },
        "Push-ups": {
            "image": "https://img.icons8.com/color/100/000000/pushups.png",
            "description": "Bodyweight exercise, great for chest and core",
            "calories_per_hour": 450
        },
        "Dumbbell Press": {
            "image": "https://img.icons8.com/color/100/000000/dumbbell.png",
            "description": "Similar to bench press but with dumbbells for better range",
            "calories_per_hour": 370
        },
        "Cable Crossovers": {
            "image": "https://img.icons8.com/color/100/000000/cable-crossover.png",
            "description": "Stand between cable machines, cross arms in front of chest",
            "calories_per_hour": 360
        }
    },
    "🦵 Leg Day": {
        "Squat": {
            "image": "https://img.icons8.com/color/100/000000/squat.png",
            "description": "Barbell on shoulders, lower until thighs parallel to floor",
            "calories_per_hour": 500
        },
        "Deadlift": {
            "image": "https://img.icons8.com/color/100/000000/deadlift.png",
            "description": "Lift barbell from floor to hip level, keep back straight",
            "calories_per_hour": 550
        },
        "Leg Press": {
            "image": "https://img.icons8.com/color/100/000000/leg-press.png",
            "description": "Sit on machine, push weight away with legs",
            "calories_per_hour": 420
        },
        "Lunges": {
            "image": "https://img.icons8.com/color/100/000000/lunges.png",
            "description": "Step forward, lower hips until both knees bent at 90 degrees",
            "calories_per_hour": 480
        },
        "Leg Extensions": {
            "image": "https://img.icons8.com/color/100/000000/leg-extension.png",
            "description": "Seated machine exercise targeting quadriceps",
            "calories_per_hour": 320
        },
        "Hamstring Curls": {
            "image": "https://img.icons8.com/color/100/000000/hamstring-curl.png",
            "description": "Lying or seated machine for hamstrings",
            "calories_per_hour": 330
        },
        "Calf Raises": {
            "image": "https://img.icons8.com/color/100/000000/calf-raise.png",
            "description": "Raise heels off ground, target calf muscles",
            "calories_per_hour": 280
        }
    },
    "🏋️ Shoulders": {
        "Shoulder Press": {
            "image": "https://img.icons8.com/color/100/000000/shoulder-press.png",
            "description": "Press weight overhead while seated or standing",
            "calories_per_hour": 380
        },
        "Lateral Raises": {
            "image": "https://img.icons8.com/color/100/000000/lateral-raise.png",
            "description": "Raise dumbbells sideways to shoulder height",
            "calories_per_hour": 300
        },
        "Front Raises": {
            "image": "https://img.icons8.com/color/100/000000/front-raise.png",
            "description": "Raise dumbbells in front to shoulder height",
            "calories_per_hour": 290
        },
        "Shrugs": {
            "image": "https://img.icons8.com/color/100/000000/shrugs.png",
            "description": "Lift shoulders toward ears with weights in hands",
            "calories_per_hour": 270
        },
        "Upright Rows": {
            "image": "https://img.icons8.com/color/100/000000/upright-row.png",
            "description": "Pull barbell vertically to chin level",
            "calories_per_hour": 350
        }
    },
    "💪 Back Day": {
        "Pull-ups": {
            "image": "https://img.icons8.com/color/100/000000/pull-up.png",
            "description": "Hang from bar, pull body up until chin over bar",
            "calories_per_hour": 520
        },
        "Lat Pulldown": {
            "image": "https://img.icons8.com/color/100/000000/lat-pulldown.png",
            "description": "Seated machine, pull bar down to chest",
            "calories_per_hour": 370
        },
        "Bent-over Rows": {
            "image": "https://img.icons8.com/color/100/000000/bent-over-row.png",
            "description": "Bend forward, pull barbell to lower chest",
            "calories_per_hour": 420
        },
        "T-Bar Rows": {
            "image": "https://img.icons8.com/color/100/000000/t-bar-row.png",
            "description": "Machine exercise for middle back thickness",
            "calories_per_hour": 390
        },
        "Seated Rows": {
            "image": "https://img.icons8.com/color/100/000000/seated-row.png",
            "description": "Cable machine exercise for back width",
            "calories_per_hour": 360
        }
    },
    "💪 Arms": {
        "Bicep Curls": {
            "image": "https://img.icons8.com/color/100/000000/bicep-curl.png",
            "description": "Curl dumbbells or barbell toward shoulders",
            "calories_per_hour": 280
        },
        "Tricep Extensions": {
            "image": "https://img.icons8.com/color/100/000000/tricep-extension.png",
            "description": "Extend arms overhead with weight behind head",
            "calories_per_hour": 290
        },
        "Hammer Curls": {
            "image": "https://img.icons8.com/color/100/000000/hammer-curl.png",
            "description": "Curl dumbbells with palms facing each other",
            "calories_per_hour": 270
        },
        "Dips": {
            "image": "https://img.icons8.com/color/100/000000/dips.png",
            "description": "Bodyweight exercise for triceps and chest",
            "calories_per_hour": 450
        },
        "Preacher Curls": {
            "image": "https://img.icons8.com/color/100/000000/preacher-curl.png",
            "description": "Isolated bicep exercise using preacher bench",
            "calories_per_hour": 260
        }
    },
    "🔁 Full Body": {
        "Clean and Press": {
            "image": "https://img.icons8.com/color/100/000000/clean-and-press.png",
            "description": "Olympic lift combining deadlift and overhead press",
            "calories_per_hour": 600
        },
        "Kettlebell Swings": {
            "image": "https://img.icons8.com/color/100/000000/kettlebell-swing.png",
            "description": "Hip-hinge movement swinging kettlebell to chest height",
            "calories_per_hour": 550
        },
        "Burpees": {
            "image": "https://img.icons8.com/color/100/000000/burpee.png",
            "description": "Full body exercise: squat, plank, push-up, jump",
            "calories_per_hour": 650
        }
    },
    "🏃 Cardio": {
        "Running": {
            "image": "https://img.icons8.com/color/100/000000/running.png",
            "description": "Outdoor or treadmill running",
            "calories_per_hour": 700
        },
        "Cycling": {
            "image": "https://img.icons8.com/color/100/000000/cycling.png",
            "description": "Stationary or outdoor cycling",
            "calories_per_hour": 500
        },
        "Swimming": {
            "image": "https://img.icons8.com/color/100/000000/swimming.png",
            "description": "Freestyle swimming laps",
            "calories_per_hour": 550
        },
        "Jump Rope": {
            "image": "https://img.icons8.com/color/100/000000/jump-rope.png",
            "description": "Skipping rope exercise",
            "calories_per_hour": 750
        }
    }
}

# Workout templates
WORKOUT_TEMPLATES = {
    "Beginner Full Body": ["Squat", "Bench Press", "Bent-over Rows", "Shoulder Press"],
    "Push Day": ["Bench Press", "Shoulder Press", "Tricep Extensions", "Push-ups"],
    "Pull Day": ["Pull-ups", "Bent-over Rows", "Bicep Curls", "Shrugs"],
    "Leg Day": ["Squat", "Deadlift", "Leg Press", "Calf Raises"],
    "Chest & Back": ["Bench Press", "Incline Bench Press", "Pull-ups", "Bent-over Rows"]
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
    st.session_state.weight_unit = "kg"
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# Database functions
def init_database():
    """Initialize SQLite database for better data management"""
    conn = sqlite3.connect('gym_tracker.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, name TEXT, email TEXT, age INTEGER, 
                  created_date DATE, is_active BOOLEAN DEFAULT TRUE)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS workouts
                 (id INTEGER PRIMARY KEY, user_id INTEGER, date DATE, duration_minutes INTEGER,
                  workout_type TEXT, exercise TEXT, weight REAL, reps INTEGER, sets INTEGER, 
                  intensity TEXT, calories_burned INTEGER, notes TEXT,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS user_stats
                 (id INTEGER PRIMARY KEY, user_id INTEGER, date DATE, weight REAL, 
                  height INTEGER, bmi REAL, bmi_category TEXT, fitness_goal TEXT,
                  experience_level TEXT, FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS custom_exercises
                 (id INTEGER PRIMARY KEY, user_id INTEGER, exercise_name TEXT, 
                  category TEXT, description TEXT, calories_per_hour INTEGER,
                  created_date DATE, FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    conn.commit()
    conn.close()

def get_or_create_user(name, email="", age=25):
    """Get existing user or create new one"""
    conn = sqlite3.connect('gym_tracker.db')
    c = conn.cursor()
    
    c.execute("SELECT id FROM users WHERE name = ?", (name,))
    result = c.fetchone()
    
    if result:
        user_id = result[0]
    else:
        c.execute('''INSERT INTO users (name, email, age, created_date) 
                     VALUES (?, ?, ?, ?)''', 
                 (name, email, age, datetime.date.today()))
        user_id = c.lastrowid
    
    conn.commit()
    conn.close()
    return user_id

def save_workout(user_id, workout_data):
    """Save workout to database"""
    conn = sqlite3.connect('gym_tracker.db')
    c = conn.cursor()
    
    c.execute('''INSERT INTO workouts 
                 (user_id, date, duration_minutes, workout_type, exercise, weight, 
                  reps, sets, intensity, calories_burned, notes)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (user_id, workout_data['date'], workout_data['duration_minutes'],
               workout_data['workout_type'], workout_data['exercise'],
               workout_data['weight'], workout_data['reps'], workout_data['sets'],
               workout_data['intensity'], workout_data['calories_burned'],
               workout_data['notes']))
    
    conn.commit()
    conn.close()

def get_user_workouts(user_id, limit=100):
    """Get workouts for a user"""
    conn = sqlite3.connect('gym_tracker.db')
    df = pd.read_sql_query('''SELECT * FROM workouts 
                              WHERE user_id = ? 
                              ORDER BY date DESC, id DESC 
                              LIMIT ?''', 
                          conn, params=(user_id, limit))
    conn.close()
    return df

def save_custom_exercise(user_id, exercise_data):
    """Save custom exercise to database"""
    conn = sqlite3.connect('gym_tracker.db')
    c = conn.cursor()
    
    c.execute('''INSERT INTO custom_exercises 
                 (user_id, exercise_name, category, description, calories_per_hour, created_date)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (user_id, exercise_data['name'], exercise_data['category'],
               exercise_data['description'], exercise_data['calories_per_hour'],
               datetime.date.today()))
    
    conn.commit()
    conn.close()

def get_custom_exercises(user_id):
    """Get custom exercises for a user"""
    conn = sqlite3.connect('gym_tracker.db')
    df = pd.read_sql_query('''SELECT * FROM custom_exercises 
                              WHERE user_id = ? 
                              ORDER BY created_date DESC''', 
                          conn, params=(user_id,))
    conn.close()
    return df

# Initialize database
init_database()

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
        # Create a simple text-based QR code alternative
        st.info("🔗 **Quick Mobile Access:**")
        st.code(url, language="text")
        st.write("💡 **Tip:** Copy this URL to your phone's browser!")
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
        return weight * 0.453592
    return weight

def convert_from_kg(weight, unit):
    """Convert weight from kg to selected unit"""
    if unit == "kg":
        return weight
    elif unit == "lb":
        return weight / 0.453592
    return weight

def calculate_calories_burned(age, weight, duration_minutes, intensity, exercise_type=None):
    """Calculate estimated calories burned based on user data and exercise"""
    # Base metabolic rate adjustment
    age_factor = max(0.8, 1 - (age - 25) * 0.005)  # Metabolism decreases with age
    
    # Intensity multipliers
    intensity_multipliers = {
        "Light": 4,
        "Moderate": 6,
        "High": 8
    }
    
    intensity_multiplier = intensity_multipliers.get(intensity, 5)
    
    # Calculate calories based on weight, duration, and intensity
    base_calories = (weight * intensity_multiplier * duration_minutes) / 60
    adjusted_calories = base_calories * age_factor
    
    return int(adjusted_calories)

def calculate_fat_loss_muscle_gain(calories_burned, workout_intensity, user_stats):
    """Calculate estimated fat loss and muscle gain potential"""
    # Fat loss calculation (approx. 7700 calories = 1kg fat)
    fat_loss_kg = calories_burned / 7700
    
    # Muscle gain potential based on intensity and protein intake
    intensity_factors = {"Light": 0.1, "Moderate": 0.3, "High": 0.5}
    muscle_gain_potential = intensity_factors.get(workout_intensity, 0.2) * (fat_loss_kg / 10)
    
    return fat_loss_kg, muscle_gain_potential

def check_new_pr(exercise, weight, reps, user_data):
    """Check if this is a new personal record and return congratulatory message"""
    try:
        if user_data.empty:
            return f"🎉 First time logging {exercise}! Welcome to your fitness journey, babe! 'WOW! Eljamal bema 7amal. Good job 7bb' 💪"
        
        exercise_data = user_data[user_data['exercise'] == exercise]
        
        if not exercise_data.empty:
            # Check for weight PR
            max_weight = exercise_data['weight'].max()
            if weight > max_weight:
                return f"🎉 NEW PERSONAL RECORD! {exercise}: {weight}kg! 'WOW! Eljamal bema 7amal. Good job 7bb' 💪🎊"
            
            # Check for reps PR at this weight
            same_weight_data = exercise_data[exercise_data['weight'] == weight]
            if not same_weight_data.empty:
                max_reps = same_weight_data['reps'].max()
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
    
    # Define milestone thresholds
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
        exercise_data = user_data[user_data['exercise'] == exercise].sort_values('date')
        if len(exercise_data) > 1:
            latest = exercise_data.iloc[-1]
            previous = exercise_data.iloc[-2]
            
            weight_increase = latest['weight'] - previous['weight']
            rep_increase = latest['reps'] - previous['reps']
            
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
    for exercise in user_data['exercise'].unique():
        ex_data = user_data[user_data['exercise'] == exercise].sort_values('date')
        if len(ex_data) > 1:
            improvement = ex_data['weight'].iloc[-1] - ex_data['weight'].iloc[0]
            progress_data.append((exercise, improvement))
    
    if progress_data:
        best_improvement = max(progress_data, key=lambda x: x[1])
        insights.append(f"🏆 **Most Improved**: {best_improvement[0]} (+{best_improvement[1]:.1f}kg)")
    
    # Recent achievements
    recent_workouts = user_data.sort_values('date').tail(5)
    if not recent_workouts.empty:
        max_weight = recent_workouts['weight'].max()
        max_exercise = recent_workouts[recent_workouts['weight'] == max_weight]['exercise'].iloc[0]
        insights.append(f"💪 **Recent PR**: {max_weight}kg on {max_exercise}")
    
    # Total calories burned
    total_calories = user_data['calories_burned'].sum()
    insights.append(f"🔥 **Total Calories Burned**: {total_calories:,}")
    
    # BMI progress if available
    if 'starting_weight' in user_stats and 'current_weight' in user_stats:
        weight_change = user_stats['current_weight'] - user_stats['starting_weight']
        if weight_change > 0:
            insights.append(f"⚖️ **Weight Change**: +{weight_change:.1f}kg muscle gain! Amazing, babe!")
        elif weight_change < 0:
            insights.append(f"⚖️ **Weight Change**: {weight_change:.1f}kg fat loss! Great work, babe!")
    
    # Workout frequency
    workout_days = user_data['date'].nunique()
    total_workouts = len(user_data)
    insights.append(f"📅 **Consistency**: {workout_days} workout days, {total_workouts} total sessions")
    
    return "\n\n".join(insights)

def get_protein_recommendation(workout_type, intensity, calories_burned):
    """Recommend protein shake based on workout and calories burned"""
    if calories_burned > 500 or intensity == "High" or "Leg Day" in workout_type:
        return PROTEIN_SHAKES["Mass Gainer"]
    elif calories_burned > 300:
        return PROTEIN_SHAKES["Post-Workout Basic"]
    elif "Cardio" in workout_type:
        return PROTEIN_SHAKES["Quick Recovery"]
    else:
        return random.choice(list(PROTEIN_SHAKES.values()))

def rest_timer(minutes=2):
    """Display a rest timer between sets"""
    if st.button(f"⏰ Start {minutes}min Rest Timer"):
        with st.empty():
            for seconds in range(minutes * 60, 0, -1):
                mins, secs = divmod(seconds, 60)
                st.metric("Rest Time", f"{mins:02d}:{secs:02d}")
                time.sleep(1)
            st.success("💪 Rest time over! Next set!")

# Simple password protection
def check_password():
    """Simple password check for basic security"""
    if "password_checked" not in st.session_state:
        st.session_state.password_checked = False
    
    if not st.session_state.password_checked:
        password = st.text_input("Enter access code:", type="password")
        if password:
            if password == "Hani2024":  # Simple static password
                st.session_state.password_checked = True
                st.rerun()
            else:
                st.error("Incorrect access code. Please try again.")
        return False
    return True

# Sidebar authentication
with st.sidebar:
    st.title("🎁 Welcome, Hani!")
    st.image("https://img.icons8.com/color/96/000000/dumbbell.png", width=100)
    
    if not check_password():
        st.stop()
    
    # User profile setup
    user_name = st.text_input("Enter your name:", placeholder="Hani", value=st.session_state.get('user_name', ''))
    user_age = st.number_input("Your Age:", min_value=15, max_value=80, value=25)
    
    if user_name:
        st.session_state.authenticated = True
        st.session_state.user_name = user_name
        st.session_state.user_id = get_or_create_user(user_name, age=user_age)
        
        # Weight unit selection
        st.subheader("⚖️ Weight Units")
        weight_unit = st.radio("Select weight unit:", ["kg", "lb"], 
                              index=0 if st.session_state.get('weight_unit', 'kg') == 'kg' else 1)
        if weight_unit != st.session_state.get('weight_unit', 'kg'):
            st.session_state.weight_unit = weight_unit
            st.rerun()
        
        # Quick rest timer
        st.subheader("⏰ Rest Timer")
        rest_timer()
    else:
        st.session_state.authenticated = False
        st.info("Enter your name to start tracking!")

# Main app content
if st.session_state.authenticated:
    # Personal greeting with birthday detection
    greeting, subheader = get_greeting()
    st.title(f"💪 {st.session_state.user_name}'s Smart Gym Tracker")
    st.subheader(greeting)
    st.write(f"**{subheader}**")
    
    # User stats setup (first time only)
    try:
        conn = sqlite3.connect('gym_tracker.db')
        user_stats_df = pd.read_sql_query('''SELECT * FROM user_stats 
                                           WHERE user_id = ? 
                                           ORDER BY date DESC LIMIT 1''', 
                                        conn, params=(st.session_state.user_id,))
        conn.close()
        
        if not user_stats_df.empty:
            st.session_state.user_stats = user_stats_df.iloc[-1].to_dict()
    except:
        st.session_state.user_stats = {}

    if not st.session_state.user_stats:
        # First-time setup
        with st.expander("📊 Setup Your Profile", expanded=True):
            st.subheader("Let's set up your profile, babe!")
            col1, col2 = st.columns(2)
            
            with col1:
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
                    "user_id": st.session_state.user_id,
                    "date": datetime.date.today(),
                    "weight": weight_kg,
                    "height": height,
                    "bmi": bmi,
                    "bmi_category": bmi_category,
                    "fitness_goal": fitness_goal,
                    "experience_level": experience
                }
                
                # Save to database
                conn = sqlite3.connect('gym_tracker.db')
                c = conn.cursor()
                c.execute('''INSERT INTO user_stats 
                           (user_id, date, weight, height, bmi, bmi_category, fitness_goal, experience_level)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                         (user_stats['user_id'], user_stats['date'], user_stats['weight'],
                          user_stats['height'], user_stats['bmi'], user_stats['bmi_category'],
                          user_stats['fitness_goal'], user_stats['experience_level']))
                conn.commit()
                conn.close()
                
                st.session_state.user_stats = user_stats
                st.success("Profile saved successfully, babe! 🎉")
                st.rerun()
    
    # Monthly weight update
    if st.session_state.user_stats:
        with st.expander("⚖️ Update Your Weight"):
            st.write("Update your weight monthly to track your progress, babe!")
            
            current_weight_kg = st.session_state.user_stats.get('weight', 80.0)
            current_weight_display = convert_from_kg(current_weight_kg, st.session_state.weight_unit)
            
            new_weight_display = st.number_input(f"Current Weight ({st.session_state.weight_unit}):", 
                                               min_value=50.0, max_value=150.0, 
                                               value=float(current_weight_display), step=0.5)
            
            new_weight_kg = convert_to_kg(new_weight_display, st.session_state.weight_unit)
            
            if st.button("Update Weight"):
                # Update in database
                conn = sqlite3.connect('gym_tracker.db')
                c = conn.cursor()
                c.execute('''INSERT INTO user_stats 
                           (user_id, date, weight, height, bmi, bmi_category, fitness_goal, experience_level)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                         (st.session_state.user_id, datetime.date.today(), new_weight_kg,
                          st.session_state.user_stats['height'], 
                          calculate_bmi(new_weight_kg, st.session_state.user_stats['height']),
                          get_bmi_category(calculate_bmi(new_weight_kg, st.session_state.user_stats['height'])),
                          st.session_state.user_stats['fitness_goal'],
                          st.session_state.user_stats['experience_level']))
                conn.commit()
                conn.close()
                
                st.session_state.user_stats['weight'] = new_weight_kg
                
                # Check for weight milestones
                milestone_message = check_weight_goal(st.session_state.user_stats, new_weight_kg)
                if milestone_message:
                    st.balloons()
                    st.success(milestone_message)
                else:
                    st.success("Weight updated successfully, babe! 💪")
    
    # QR Code Generation
    with st.expander("📱 Get Mobile QR Code"):
        st.write("Scan this QR code to open the app on your phone anytime, babe!")
        app_url = "https://hani-gym-miladshaan.streamlit.app/"
        qr_image = generate_qr_code(app_url)
        if qr_image:
            st.image(qr_image, caption="Scan for mobile access", width=200)
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📝 Log Workout", "🏋️ Exercise Library", "📈 View Progress", "🧠 Progress Insights", "🥤 Nutrition", "⚙️ Custom Exercises"])
    
    with tab1:
        st.header("Log Your Workout")
        
        with st.form("workout_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                workout_type = st.selectbox("Workout Focus:", list(EXERCISE_DATABASE.keys()))
                
                # Exercise selection with custom option
                exercise_option = st.radio("Exercise Source:", ["Select from Library", "Enter Custom Exercise"])
                
                if exercise_option == "Select from Library":
                    exercises = list(EXERCISE_DATABASE[workout_type].keys())
                    exercise = st.selectbox("Exercise:", exercises)
                    
                    # Show exercise image and description
                    if exercise in EXERCISE_DATABASE[workout_type]:
                        ex_info = EXERCISE_DATABASE[workout_type][exercise]
                        st.image(ex_info["image"], width=80)
                        st.caption(ex_info["description"])
                        base_calories_per_hour = ex_info.get("calories_per_hour", 300)
                else:
                    # Custom exercise input
                    exercise = st.text_input("Custom Exercise Name:", placeholder="e.g., Turkish Get-Up")
                    custom_description = st.text_area("Exercise Description:", placeholder="Describe how to perform this exercise")
                    custom_calories = st.number_input("Estimated Calories per Hour:", min_value=100, max_value=1000, value=350)
                    base_calories_per_hour = custom_calories
                
                intensity = st.select_slider("Workout Intensity:", ["Light", "Moderate", "High"])
                duration_minutes = st.number_input("Workout Duration (minutes):", min_value=5, max_value=180, value=60)
            
            with col2:
                # Weight input with unit conversion
                weight_display = st.number_input(f"Weight ({st.session_state.weight_unit}):", 
                                               min_value=0.0, step=0.5, value=20.0)
                weight_kg = convert_to_kg(weight_display, st.session_state.weight_unit)
                
                reps = st.number_input("Reps:", min_value=1, max_value=50, value=8)
                sets = st.number_input("Sets:", min_value=1, max_value=10, value=3)
                
                # Smart watch calories input with auto-calculation
                col2a, col2b = st.columns(2)
                with col2a:
                    use_smartwatch = st.checkbox("Use Smartwatch Data", value=True)
                with col2b:
                    if use_smartwatch:
                        smartwatch_calories = st.number_input("Calories Burned (from watch):", 
                                                            min_value=50, max_value=2000, value=400)
                    else:
                        # Auto-calculate calories
                        user_age = st.session_state.user_stats.get('age', 25)
                        user_weight = st.session_state.user_stats.get('weight', 80)
                        calculated_calories = calculate_calories_burned(
                            user_age, user_weight, duration_minutes, intensity
                        )
                        smartwatch_calories = st.number_input("Calories Burned (estimated):", 
                                                            min_value=50, max_value=2000, 
                                                            value=int(calculated_calories))
                
                notes = st.text_input("Notes:", placeholder="How did it feel, babe?")
            
            submitted = st.form_submit_button("💾 Save Workout & Get Analysis")
            
            if submitted:
                if exercise.strip() == "":
                    st.error("Please enter an exercise name, babe!")
                else:
                    # Save custom exercise if it's new
                    if exercise_option == "Enter Custom Exercise" and exercise.strip():
                        custom_exercise_data = {
                            'name': exercise,
                            'category': workout_type,
                            'description': custom_description,
                            'calories_per_hour': custom_calories
                        }
                        save_custom_exercise(st.session_state.user_id, custom_exercise_data)
                        st.success(f"✅ Custom exercise '{exercise}' saved to your library!")
                    
                    # Save workout
                    workout_data = {
                        "date": datetime.date.today(),
                        "duration_minutes": duration_minutes,
                        "workout_type": workout_type,
                        "exercise": exercise,
                        "weight": weight_kg,
                        "reps": reps,
                        "sets": sets,
                        "intensity": intensity,
                        "calories_burned": smartwatch_calories,
                        "notes": notes
                    }
                    
                    save_workout(st.session_state.user_id, workout_data)
                    
                    # Get user data for PR check
                    user_data = get_user_workouts(st.session_state.user_id)
                    
                    # Check for new personal records
                    pr_message = check_new_pr(exercise, weight_kg, reps, user_data)
                    if pr_message:
                        st.balloons()
                        st.success(pr_message)
                    else:
                        st.success("Workout saved successfully, babe! 🎉")
                    
                    # Personal encouragement
                    random_message = random.choice(ENCOURAGING_MESSAGES)
                    st.info(f"💌 From your babe: {random_message}")
                    
                    # AI suggestions
                    next_weight_kg, reason = calculate_next_weight(exercise, weight_kg, reps, user_data)
                    next_weight_display = convert_from_kg(next_weight_kg, st.session_state.weight_unit)
                    st.success(f"🧠 **AI Suggestion**: Try {next_weight_display:.1f}{st.session_state.weight_unit} next time! *{reason}*")
                    
                    # Fat loss and muscle gain analysis
                    fat_loss_kg, muscle_gain_potential = calculate_fat_loss_muscle_gain(
                        smartwatch_calories, intensity, st.session_state.user_stats
                    )
                    
                    st.subheader("🏆 Workout Analysis")
                    col_analysis1, col_analysis2, col_analysis3 = st.columns(3)
                    
                    with col_analysis1:
                        st.metric("🔥 Calories Burned", f"{smartwatch_calories}")
                    
                    with col_analysis2:
                        st.metric("💧 Fat Loss Potential", f"{fat_loss_kg:.3f} kg")
                    
                    with col_analysis3:
                        st.metric("💪 Muscle Gain Potential", f"{muscle_gain_potential:.3f} kg")
                    
                    # Progress explanation
                    st.info(f"""
                    **📊 Analysis Breakdown:**
                    - **Fat Loss**: Burning {smartwatch_calories} calories ≈ {fat_loss_kg:.3f}kg fat loss potential
                    - **Muscle Gain**: {intensity} intensity workout supports muscle growth
                    - **Net Effect**: With proper nutrition, you can build muscle while losing fat!
                    """)
                    
                    # Protein recommendation based on actual calories burned
                    protein_shake = get_protein_recommendation(workout_type, intensity, smartwatch_calories)
                    st.info(f"🥤 **Post-Workout Nutrition**: {protein_shake}")
                    
                    st.balloons()

    with tab2:
        st.header("🏋️ Exercise Library")
        st.write("Browse all exercises with instructions and calorie estimates, babe!")
        
        selected_category = st.selectbox("Choose Category:", list(EXERCISE_DATABASE.keys()))
        
        exercises = EXERCISE_DATABASE[selected_category]
        for exercise_name, exercise_info in exercises.items():
            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                st.image(exercise_info["image"], width=80)
            with col2:
                st.subheader(exercise_name)
                st.write(exercise_info["description"])
                st.write(f"🔥 **Calories/Hour**: ~{exercise_info.get('calories_per_hour', 300)}")
            with col3:
                if st.button("Quick Log", key=f"quick_{exercise_name}"):
                    # Pre-fill workout form
                    st.session_state.quick_log_exercise = exercise_name
                    st.session_state.quick_log_category = selected_category
                    st.info(f"Ready to log {exercise_name}! Go to the 'Log Workout' tab.")
            st.write("---")
        
        # Show custom exercises
        custom_exercises = get_custom_exercises(st.session_state.user_id)
        if not custom_exercises.empty:
            st.subheader("Your Custom Exercises")
            for _, custom_ex in custom_exercises.iterrows():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{custom_ex['exercise_name']}** ({custom_ex['category']})")
                    st.write(f"📝 {custom_ex['description']}")
                    st.write(f"🔥 Calories/Hour: ~{custom_ex['calories_per_hour']}")
                with col2:
                    if st.button("Log", key=f"custom_{custom_ex['id']}"):
                        st.session_state.quick_log_exercise = custom_ex['exercise_name']
                        st.session_state.quick_log_category = custom_ex['category']
                        st.info(f"Ready to log {custom_ex['exercise_name']}!")

    with tab3:
        st.header("Your Progress Dashboard")
        
        user_data = get_user_workouts(st.session_state.user_id)
        
        if not user_data.empty:
            # Convert weights for display
            display_df = user_data.copy()
            display_df['Weight_Display'] = display_df['weight'].apply(
                lambda x: convert_from_kg(x, st.session_state.weight_unit)
            )
            display_df['date'] = pd.to_datetime(display_df['date'])
            
            # Progress charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(f"🏋️ Weight Progression ({st.session_state.weight_unit})")
                selected_exercise = st.selectbox("Select Exercise:", user_data['exercise'].unique(), key="progress_exercise")
                
                exercise_data = display_df[display_df['exercise'] == selected_exercise].sort_values('date')
                if not exercise_data.empty:
                    st.line_chart(exercise_data, x='date', y='Weight_Display')
            
            with col2:
                st.subheader("📊 Workout Distribution")
                workout_counts = user_data['workout_type'].value_counts()
                fig, ax = plt.subplots()
                ax.pie(workout_counts.values, labels=workout_counts.index, autopct='%1.1f%%')
                st.pyplot(fig)
            
            # Calories burned over time
            st.subheader("🔥 Calories Burned Over Time")
            calories_by_date = user_data.groupby('date')['calories_burned'].sum().reset_index()
            st.line_chart(calories_by_date, x='date', y='calories_burned')
            
            # Recent workouts table
            st.subheader("📋 Recent Workouts")
            display_columns = ['date', 'exercise', 'Weight_Display', 'reps', 'sets', 'calories_burned']
            display_table = display_df[display_columns].copy()
            display_table = display_table.rename(columns={
                'Weight_Display': f'Weight ({st.session_state.weight_unit})',
                'date': 'Date',
                'exercise': 'Exercise',
                'reps': 'Reps',
                'sets': 'Sets',
                'calories_burned': 'Calories'
            })
            st.dataframe(display_table.sort_values('Date', ascending=False).head(10))
        else:
            st.info("No workouts logged yet. Start by logging your first workout, babe!")

    with tab4:
        st.header("Progress Insights & Analytics")
        
        user_data = get_user_workouts(st.session_state.user_id)
        
        if not user_data.empty:
            # Progress analysis
            insights = analyze_progress(user_data, st.session_state.user_stats)
            st.success(insights)
            
            # Monthly progress
            st.subheader("📅 Monthly Progress")
            user_data['date'] = pd.to_datetime(user_data['date'])
            user_data['Month'] = user_data['date'].dt.to_period('M')
            monthly_progress = user_data.groupby('Month').agg({
                'weight': 'max',
                'exercise': 'count',
                'calories_burned': 'sum'
            }).rename(columns={'exercise': 'Workouts'})
            
            # Convert max weight for display
            monthly_progress['Weight_Display'] = monthly_progress['weight'].apply(
                lambda x: convert_from_kg(x, st.session_state.weight_unit)
            )
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Workouts", len(user_data))
            with col2:
                st.metric("Total Calories", f"{user_data['calories_burned'].sum():,}")
            with col3:
                st.metric("Workout Days", user_data['date'].nunique())
            
            col4, col5 = st.columns(2)
            with col4:
                st.line_chart(monthly_progress['Weight_Display'])
                st.write(f"Max Weight per Month ({st.session_state.weight_unit})")
            with col5:
                st.bar_chart(monthly_progress['Workouts'])
                st.write("Workouts per Month")
                
            # Fitness age calculation
            st.subheader("🧬 Fitness Age Analysis")
            actual_age = st.session_state.user_stats.get('age', 25)
            workout_frequency = user_data['date'].nunique() / 30  # workouts per month
            avg_intensity = user_data['calories_burned'].mean() / 60  # calories per minute
            
            # Simple fitness age calculation
            fitness_age = max(actual_age - (workout_frequency * 0.5 + avg_intensity * 0.1), 18)
            st.metric("Your Fitness Age", f"{fitness_age:.1f} years", 
                     delta=f"{actual_age - fitness_age:.1f} years younger than actual age!")
            
        else:
            st.info("Log more workouts to unlock detailed insights, babe!")

    with tab5:
        st.header("🥤 Nutrition & Recovery")
        
        # Protein shake recommendations based on recent workout
        user_data = get_user_workouts(st.session_state.user_id, limit=1)
        if not user_data.empty:
            last_workout = user_data.iloc[0]
            st.subheader("💪 Personalized Recommendation")
            recommended_shake = get_protein_recommendation(
                last_workout['workout_type'], 
                last_workout['intensity'],
                last_workout['calories_burned']
            )
            st.success(f"**Based on your last workout:** {recommended_shake}")
        
        st.subheader("🥤 Protein Shake Recipes")
        for shake_name, shake_desc in PROTEIN_SHAKES.items():
            with st.expander(f"🥤 {shake_name}"):
                st.write(shake_desc)
        
        st.subheader("📊 Daily Nutrition Targets")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Protein", "150-200g", "Muscle Building")
        with col2:
            st.metric("Carbs", "200-300g", "Energy")
        with col3:
            st.metric("Fat", "50-70g", "Hormone Health")
        
        st.subheader("💡 Nutrition Tips")
        st.write("""
        - **Hydrate well** before, during, and after workouts
        - **Eat protein** within 30 minutes after training for best recovery
        - **Carbs are fuel** - don't skip them on workout days
        - **Healthy fats** support hormone production and joint health
        - **Listen to your body**, babe - rest when needed!
        - **Track your calories** to match your fitness goals
        """)

    with tab6:
        st.header("⚙️ Custom Exercises Manager")
        st.write("Add and manage your own exercises, babe!")
        
        with st.form("custom_exercise_form"):
            st.subheader("Add New Custom Exercise")
            col1, col2 = st.columns(2)
            
            with col1:
                custom_name = st.text_input("Exercise Name:", placeholder="e.g., Turkish Get-Up")
                custom_category = st.selectbox("Category:", list(EXERCISE_DATABASE.keys()))
                custom_calories = st.number_input("Calories per Hour:", min_value=100, max_value=1000, value=350)
            
            with col2:
                custom_description = st.text_area("Description:", 
                                                placeholder="Describe how to perform this exercise...",
                                                height=100)
                custom_image_url = st.text_input("Image URL (optional):", 
                                               placeholder="https://example.com/image.png")
            
            if st.form_submit_button("💾 Save Custom Exercise"):
                if custom_name.strip():
                    exercise_data = {
                        'name': custom_name,
                        'category': custom_category,
                        'description': custom_description,
                        'calories_per_hour': custom_calories
                    }
                    save_custom_exercise(st.session_state.user_id, exercise_data)
                    st.success(f"✅ '{custom_name}' added to your custom exercises!")
                else:
                    st.error("Please enter an exercise name, babe!")
        
        # Display existing custom exercises
        st.subheader("Your Custom Exercises")
        custom_exercises = get_custom_exercises(st.session_state.user_id)
        
        if not custom_exercises.empty:
            for _, exercise in custom_exercises.iterrows():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{exercise['exercise_name']}**")
                    st.write(f"*Category: {exercise['category']}*")
                    st.write(f"📝 {exercise['description']}")
                    st.write(f"🔥 Calories/Hour: {exercise['calories_per_hour']}")
                with col2:
                    if st.button("Use", key=f"use_{exercise['id']}"):
                        st.session_state.quick_log_exercise = exercise['exercise_name']
                        st.session_state.quick_log_category = exercise['category']
                        st.info(f"Ready to log {exercise['exercise_name']}! Go to 'Log Workout' tab.")
                with col3:
                    if st.button("Delete", key=f"del_{exercise['id']}"):
                        # Simple delete function
                        conn = sqlite3.connect('gym_tracker.db')
                        c = conn.cursor()
                        c.execute("DELETE FROM custom_exercises WHERE id = ?", (exercise['id'],))
                        conn.commit()
                        conn.close()
                        st.success("Exercise deleted!")
                        st.rerun()
                st.write("---")
        else:
            st.info("No custom exercises yet. Add your first one above!")

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
        ✅ **Log calories burned** from your smartwatch  
        ✅ **Predict fat loss & muscle gain** based on your workouts
        ✅ **Add custom exercises** not in the database
        ✅ **Get personalized nutrition advice** 
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
    st.markdown("Made with all my love for you, Hani! I will always cheering for you! 💝")

# Quick log functionality
if hasattr(st.session_state, 'quick_log_exercise'):
    st.sidebar.success(f"💪 Ready to log: {st.session_state.quick_log_exercise}")
    if st.sidebar.button("Clear Quick Log"):
        del st.session_state.quick_log_exercise
        del st.session_state.quick_log_category