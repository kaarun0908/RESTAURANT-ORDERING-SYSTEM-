# Foodies Restaurant Ordering System — V1

## V1 scope
- User registration and login (passwords hashed)
- Browse menu and view item details
- Search/filter/sort the menu UI
- Add items to cart, update quantity, remove items
- Place an order (requires login)
- SQLite database created automatically

## Requirements
- Python 3.10+
- Flask

## Run on Windows
1. Extract this ZIP.
2. Open the `Foodies_V1` folder in VS Code.
3. Open Terminal in that folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again. Or skip activation and run `py -m pip install -r requirements.txt` followed by `py app.py`.

4. Open http://127.0.0.1:5000 in your browser.
5. Register an account, log in, add food to cart, and place an order.

## Git branch workflow
The ZIP contains the integrated V1 application for `main`. To maintain the requested feature branches, initialize Git and make the feature commits in this order:

```bash
git init
git add .
git commit -m "chore: create Foodies V1 baseline"
git branch -M main

git switch -c feature/login
git add app.py templates/auth.html
git commit -m "feat: add registration and login"

git switch main
git switch -c feature/menu
git add app.py templates/index.html static/style.css static/script.js
git commit -m "feat: add menu and Foodies UI"

git switch main
git switch -c feature/cart
git add app.py templates/cart.html
git commit -m "feat: add shopping cart"

git switch main
git switch -c feature/order
git add app.py templates/cart.html
git commit -m "feat: add order checkout"

# Merge feature branches into main
git switch main
git merge feature/login
git merge feature/menu
git merge feature/cart
git merge feature/order
git tag -a V1-Baseline -m "Foodies V1: login, menu, cart and order"
```

**Important:** This branch sequence is a learning/demo workflow. Because this ZIP is already the integrated V1 code, the commits above record the same integrated files on each branch rather than representing a true from-scratch feature-by-feature development history. For a clean feature-branch history, start each feature branch from the initial baseline and implement only that feature before merging.

## Suggested project structure
```
Foodies_V1/
  app.py
  requirements.txt
  foodies.db          # created on first run
  templates/
    base.html
    index.html
    auth.html
    cart.html
  static/
    style.css
    script.js
```

## Version plan
- V1: Login, Registration, Menu, Cart, Order
- V2: Search, cart enhancement, order history, admin dashboard
- V3: Payment, reviews, reports/charts, notifications

Notes: Food menu uses sample data and remote Unsplash images. Payments, admin dashboard, order history, reviews, charts and notifications are intentionally outside V1.
