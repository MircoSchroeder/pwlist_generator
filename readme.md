🔐 Advanced Custom Wordlist Generator

A Python-based GUI tool designed for penetration testers and security analysts. It generates targeted, pattern-based password lists for security audits and brute-force simulations.
💡 The Story (Why I built this)

During my studies in cybersecurity and pentesting (working with Kali Linux), I noticed a gap in existing wordlist tools. Most tools generate generic dictionaries or pure brute-force combinations. However, in real-world scenarios (and authorized audits), users often construct passwords using predictable patterns (e.g., CompanyName + Year + Symbol).

I needed a tool that allows for specific pattern definition combined with entropy injection (inserting special characters into words) to simulate realistic user behavior. Since I couldn't find a tool that offered this specific flexibility with a GUI, I built it myself.
✨ Key Features

    🧩 Custom Pattern Logic: Define the exact structure of the passwords (e.g., Word -> Number -> Symbol or Number -> Word).

    💉 Entropy Injection: Automatically inserts special characters or numbers into base words (simulating users who try to make passwords "complex").

    🚀 Memory Efficient: Uses Python's itertools to handle combinations without overloading system memory.

    🖥️ User Friendly: Full Graphical User Interface (GUI) built with tkinter – no command line arguments needed.

    📂 Mass Processing: Load your own base lists for words, numbers, and symbols.

-----------------------------------------

🛠️ Tech Stack & Architecture

This project was developed using an AI-assisted workflow to ensure clean code structure and rapid prototyping. It follows the Separation of Concerns principle:

    main_gui.py: Handles the user interface and event loops (Presentation Layer).

    generator_logic.py: Contains the algorithms for combination generation and file handling (Business Logic).

-----------------------------------------

🚀 Getting Started
Prerequisites:

    Python 3.x installed on your system.

    No external heavy libraries required (uses standard libraries tkinter, itertools).

-----------------------------------------

Installation:

1. Clone the repository:
	git clone https://github.com/MircoSchroeder/pwlist_generator.git

2. Navigate to the folder:
	cd custom-wordlist-generator

3.  Run the application:
	python main_gui.py

-----------------------------------------

📸 Screenshots

(Platzhalter: Hier fügst du später ein Bild deines Tools ein)

-----------------------------------------

⚙️ How it works:

1.    Select Output: Choose where to save the generated .txt file.

2.    Load Lists: Import your base .txt files (e.g., a list of common English words, a list of years, etc.).

3.    Define Rules: Set minimum/maximum length and the order of elements.

4.    Generate: The tool calculates all valid combinations and writes them to the file.

-----------------------------------------

📝 Roadmap / Future Improvements

    [ ] Add a "Dark Mode" for the GUI.

    [ ] Implement a CLI (Command Line Interface) mode for headless servers.

    [ ] Add support for "Leet Speak" transformation (e.g., converting E to 3).
