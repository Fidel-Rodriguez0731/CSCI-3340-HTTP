import requests

def display_menu():
  print("HTTP API EXPLORER")
  print("1. Get a post by ID")
  print("2. Get all posts from a user")
  print("3. Get comments for a post")
  print("4. Create a new post")
  print("5. Update a post")
  print("6. Delete a post")
  print("7. Get a random joke")
  print("8. Exit")

def get_post_by_id():
  """Option 1: Get a post by ID (GET)"""
  user_input = input("Enter a post ID between 1 and 100: ").strip()

  if not user_input.isdigit():
    print("Invalid input. Please enter a valid numeric post ID.")
    return

  post_id = int(user_input)
  if post_id < 1 or post_id > 100:
    print("Error: Post ID must be between 1 and 100.")
    return

  url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"

  try:
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
      data = response.json()
      print(f"\n--- Post #{data.get('id')} ---")
      print(f"Title: {data.get('title')}")
      print(f"Body: {data.get('body')}")
    elif response.status_code == 404:
      print("Post not found.")
    else:
      print(f"Unexpected status code received: {response.status_code}")
  except requests.exceptions.RequestException as e:
    print(f"Connection error occurred: {e}. Program continues.")

def get_posts_by_user():
  """Option 2: Get posts by user (GET + query parameters)"""
  user_input = input("Enter a user ID between 1 and 10: ").strip()

  if not user_input.isdigit():
    print("Invalid input. Please enter a valid numeric user ID.")
    return

  user_id = int(user_input)
  if user_id < 1 or user_id > 10:
    print("Error: User ID must be between 1 and 10.")
    return

  url = "https://jsonplaceholder.typicode.com/posts"
  try:
    response = requests.get(url, params={"userId": user_id}, timeout=10)
    response.raise_for_status()
    posts = response.json()

    print(f"\n--- Posts for User {user_id} ---")
    for post in posts:
      print(f"ID: {post.get('id')} | Title: {post.get('title')}")
  except requests.exceptions.RequestException as e:
    print(f"Connection error occurred: {e}. Program continues.")

def get_comments_for_post():
  """Option 3: Get comments for a post (GET)"""
  user_input = input("Enter a post ID to view comments: ").strip()

  if not user_input.isdigit():
    print("Invalid input. Please enter a valid numeric post ID.")
    return

  post_id = int(user_input)
  url = f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments"

  try:
    response = requests.get(url, timeout=10)
    if response.status_code == 404:
      print("Post or comments not found.")
      return
    response.raise_for_status()

    comments = response.json()
    print(f"\n--- Comments for Post #{post_id} ---")
    for comment in comments:
      print(f"Author: {comment.get('name')} ({comment.get('email')})")
      print(f"Body: {comment.get('body')}\n")
  except requests.exceptions.RequestException as e:
    print(f"Connection error occurred: {e}. Program continues.")


def create_new_post():
  """Option 4: Create a post (POST)"""
  title = input("Enter post title: ").strip()
  body = input("Enter post body: ").strip()
  user_input = input("Enter user ID (1-10): ").strip()

  if not title or not body:
    print("Title and body cannot be empty.")
    return

  if not user_input.isdigit():
    print("Invalid user ID. Must be a number.")
    return

  data = {"title": title, "body": body, "userId": int(user_input)}
  url = "https://jsonplaceholder.typicode.com/posts"

  try:
    response = requests.post(url, json=data, timeout=10)
    if response.status_code == 201:
      res_json = response.json()
      print("POST successful")
      print(f"Returned New Post ID: {res_json.get('id')}")
    else:
      print(f"Failed with status code: {response.status_code}")
  except requests.exceptions.RequestException as e:
    print(f"Connection error occurred: {e}. Program continues.")


def update_post():
  """Option 5: Update a post (PATCH)"""
  user_input = input("Enter post ID to update: ").strip()
  if not user_input.isdigit():
    print("Invalid post ID.")
    return

  post_id = int(user_input)
  new_title = input("Enter the new title: ").strip()
  if not new_title:
    print("Title cannot be empty.")
    return

  url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
  data = {"title": new_title}

  try:
    # Using PATCH to change only the title
    response = requests.patch(url, json=data, timeout=10)
    if response.ok:
      print("Success response; updated data returned:")
      print(response.json())
    else:
      print(f"Failed to update. Status code: {response.status_code}")
  except requests.exceptions.RequestException as e:
    print(f"Connection error occurred: {e}. Program continues.")


def delete_post():
  """Option 6: Delete a post (DELETE)"""
  user_input = input("Enter post ID to delete: ").strip()
  if not user_input.isdigit():
    print("Invalid post ID.")
    return

  post_id = int(user_input)
  confirm = (
      input(f"Are you sure you want to delete post #{post_id}? (Y/N): ")
      .strip()
      .upper()
  )

  if confirm != "Y":
    print("Deletion cancelled.")
    return

  url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
  try:
    response = requests.delete(url, timeout=10)
    if response.ok:
      print(
          "API accepted the DELETE request (Note: JSONPlaceholder simulates"
          " deletion; data is not permanently removed)."
      )
    else:
      print(f"Delete request failed with status code: {response.status_code}")
  except requests.exceptions.RequestException as e:
    print(f"Connection error occurred: {e}. Program continues.")


def get_random_joke():
  """Option 7: Get a random programming joke (JokeAPI)"""
  url = "https://v2.jokeapi.dev/joke/Programming?safe-mode"
  try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    joke_data = response.json()

    print("\n--- Programming Joke ---")
    if joke_data.get("type") == "single":
      print(joke_data.get("joke"))
    elif joke_data.get("type") == "twopart":
      print(f"Setup: {joke_data.get('setup')}")
      print(f"Delivery: {joke_data.get('delivery')}")
    else:
      print("Received unexpected joke format.")
  except requests.exceptions.RequestException as e:
    print(
        f"Could not fetch a joke due to a network or connection error: {e}."
        " Please try again later."
    )

def main():
  while True:
    display_menu()
    choice = input("Select an option (1-8): ").strip()

    if choice == "1":
      get_post_by_id()
    elif choice == "2":
      get_posts_by_user()
    elif choice == "3":
      get_comments_for_post()
    elif choice == "4":
      create_new_post()
    elif choice == "5":
      update_post()
    elif choice == "6":
      delete_post()
    elif choice == "7":
      get_random_joke()
    elif choice == "8":
      print("Exiting HTTP API Explorer. Goodbye!")
      break
    else:
      print("Invalid menu selection. Please choose a number between 1 and 8.")


if __name__ == "__main__":
  main()