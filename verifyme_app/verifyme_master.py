import os

while True:
    print("\n=== Verify Me Master Menu ===")
    print("1. Professions")
    print("2. Cars")
    print("3. Stands")
    print("4. Houses")
    print("5. Companies")
    print("6. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        os.system("python3 verifyme_terminal.py")
    elif choice == "2":
        os.system("python3 verifyme_cars.py")
    elif choice == "3":
        os.system("python3 verifyme_stands.py")
    elif choice == "4":
        os.system("python3 verifyme_houses.py")
    elif choice == "5":
        os.system("python3 verifyme_companies.py")
    elif choice == "6":
        break
    else:
        print("Invalid choice, try again.")
