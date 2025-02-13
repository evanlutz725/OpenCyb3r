import os
from pathlib import Path
import sys
sys.path.append("modules/")

# Ensure the "Password Analyzer Builder" folder is accessible
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Password Analyzer Builder'))

def show_menu():
    print("\nWelcome to OpenCyb3r")
    print("=====================")
    print("1. Hash Generator")
    print("2. Password Strength Analyzer")
    print("3. TOTP Generator")
    print("4. Exit")

    return input("Choose an option: ")

def hash_generator_tool():
    import hash_generator  # Importing inside function to avoid unnecessary memory usage
    hash_generator.main()

def password_analyzer_tool():
    import pwd_analyzer
    pwd_analyzer.run_main()  # Import inside function to prevent unwanted execution

def totp_tool():
    totp_dir = Path("modules/TOTP")
    
    if not totp_dir.exists():
        print("\nError: TOTP module not found!")
        print("Please ensure the TOTP module is installed in the modules directory.")
        input("Press Enter to return to the menu.")
        return

    while True:
        print("\nTOTP Generator")
        print("==============")
        print("1. First Time Setup")
        print("2. Generate New TOTP Key")
        print("3. Get TOTP Code")
        print("4. Return to Main Menu")

        choice = input("Choose an option: ")

        # Change to the TOTP directory to ensure proper file access
        original_dir = os.getcwd()
        os.chdir(totp_dir)

        try:
            if choice == "1":
                if Path("totp_keys.encrypted").exists():
                    print("\nWarning: Setup file already exists!")
                    confirm = input("Do you want to reset and create a new master password? (y/N): ")
                    if confirm.lower() != 'y':
                        print("Setup cancelled.")
                        continue

                print("\nInitializing TOTP Setup...")
                os.system(f"{sys.executable} setup.py")

            elif choice == "2":
                if not Path("totp_keys.encrypted").exists():
                    print("\nPlease run First Time Setup before generating keys.")
                    continue

                print("\nGenerating new TOTP key...")
                os.system(f"{sys.executable} keygen.py")

            elif choice == "3":
                if not Path("totp_keys.encrypted").exists():
                    print("\nPlease run First Time Setup before generating codes.")
                    continue

                print("\nGenerating TOTP code...")
                os.system(f"{sys.executable} otpapp.py")

            elif choice == "4":
                break

            else:
                print("Invalid choice. Please try again.")

        finally:
            # Always return to the original directory
            os.chdir(original_dir)

        input("\nPress Enter to continue...")

def main():
    while True:
        choice = show_menu()
        if choice == "1":
            hash_generator_tool()
        elif choice == "2":
            password_analyzer_tool()
        elif choice == "3":
            totp_tool()
        elif choice == "4":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
