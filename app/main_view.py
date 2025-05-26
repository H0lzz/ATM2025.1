from usecases.atm import ATM

def main():
    print("Starting ATM System...")
    try:
        atm = ATM()
    except KeyboardInterrupt:
        print("\nATM session terminated by user.")
    except Exception as e:
        print(f"\nError: {e}. ATM shutting down.")
    finally:
        print("Thank you for using our ATM. Goodbye!")

if __name__ == "__main__":
    main()