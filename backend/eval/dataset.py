# 10 Real Product Prompts
REAL_PROMPTS = [
    "Build a CRM with login, contacts, dashboard, role-based access, and premium plan with payments. Admins can see analytics.",
    "Create a task management app where users can create projects, add tasks, assign them to team members, and set deadlines.",
    "Design an e-commerce platform for selling digital courses. Users can browse courses, buy them, and watch videos. Instructors can upload content.",
    "Build a social network for pet owners. Users can create profiles for their pets, post photos, like posts, and send direct messages.",
    "Create an internal HR portal for employee onboarding. New hires can fill out forms, upload documents, and watch training videos. HR admins can track progress.",
    "Design a restaurant reservation system. Customers can see available tables, book a slot, and get email confirmations. Managers can see daily bookings.",
    "Build a personal finance tracker. Users can link bank accounts, categorize transactions, and view monthly spending charts.",
    "Create a real estate listing platform. Agents can post properties with images and prices. Buyers can search, filter by location, and contact agents.",
    "Design a fitness tracking app where users can log workouts, track calories, and join community challenges.",
    "Build a support ticketing system. Customers can submit issues. Support agents can reply, change status, and escalate tickets."
]

# 10 Edge Cases (Vague, Conflicting, Incomplete)
EDGE_CASE_PROMPTS = [
    "Build an app.", # Extremely vague
    "I want an app where users can buy things but there is no payment system and no user accounts.", # Conflicting
    "A dashboard with charts.", # Incomplete
    "An AI that does everything.", # Vague/Impossible
    "Users can upload photos, but only if they are logged in, but there is no login page.", # Conflicting logic
    "A messaging app without a database.", # Contradictory to standard architecture
    "Make Facebook.", # Underspecified
    "An app for admins only. No users.", # Edge case roles
    "Just give me the database tables for a school.", # Missing UI/API intent
    "An offline-only web app with real-time multiplayer features." # Conflicting
]
