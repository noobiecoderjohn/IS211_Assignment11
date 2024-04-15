from flask import Flask, render_template, request, redirect, url_for
import os
import pickle

app = Flask(__name__)

todo_items = []

# Load saved to-do list if exists
def load_saved_list():
    if os.path.exists('todo_list.pkl'):
        with open('todo_list.pkl', 'rb') as f:
            return pickle.load(f)
    else:
        return []

# Save the current list to a file using pickle
def save_list(todo_list):
    with open('todo_list.pkl', 'wb') as f:
        pickle.dump(todo_list, f)

# Load the to-do list at the start of the application
todo_items = load_saved_list()

# The main controller for displaying the to-do list and the form for adding new items
@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        # This part is for handling the new item submission
        task = request.form.get('task')
        email = request.form.get('email')
        priority = request.form.get('priority')

        # Data validation
        if not (email and '@' in email) or priority not in ['Low', 'Medium', 'High']:
            error = 'Invalid email or priority'
        else:
            todo_items.append((task, email, priority))
            save_list(todo_items)  # Save the updated list
            return redirect(url_for('index'))

    return render_template('index.html', todo_items=todo_items, error=error)

# Controller for clearing the to-do list
@app.route('/clear', methods=['POST'])
def clear():
    todo_items.clear()
    save_list(todo_items)  # Save the empty list
    return redirect(url_for('index'))

# Controller for deleting an individual item
@app.route('/delete/<int:item_index>', methods=['POST'])
def delete(item_index):
    if 0 <= item_index < len(todo_items):
        del todo_items[item_index]
        save_list(todo_items)  # Save the updated list
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
