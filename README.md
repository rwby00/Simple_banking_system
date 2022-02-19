# Simple_banking_system
Everything goes digital these days, and so does money. Today, most people have credit cards, which save us time, energy and nerves. From not having to carry a wallet full of cash to consumer protection, cards make our lives easier in many ways. In this project, I develop a simple banking system with database.

Let's take a look at the anatomy of a credit card:
<img src="https://lh3.googleusercontent.com/ZgkQv6hMeNkbBrSeSsnb2t6GLkawQFKJNaXapTAaFmy-WPWPPtFp5MpnvlzSFzn3R-0zAvOEUriCg6bGeX_stXdG8L0WSeASnwvqFLLFyeQO4JcbfH4yjh2QdHBEdQyZy2k72q4V" alt="Card"/>

This project objectives: 
- Create a simple system to simulate simple function of banking system. 
- Create a database to verify all process and transaction
- Use Luhn Alogrithm to verify credit cards. 

Create a simple menu to navigate, it will have these options below: 
1. Create an account
2. Log into account

If you choose 1, it will create a new bank account to the database (Luhn Algorithm will verify)
If choose 2, it will check for your card in database then navigate to a menu with more options

1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit

Logic: 
- If the user tries to transfer more money than he/she has, output: Not enough money!
- If the user tries to transfer money to the same account, output the following message: You can't transfer money to the same account!
- If the receiver's card number doesn’t pass the Luhn algorithm, you should output: Probably you made a mistake in the card number. Please try again!
- If the receiver's card number doesn’t exist, you should output: Such a card does not exist.
- If there is no error, ask the user how much money they want to transfer and make the transaction.



