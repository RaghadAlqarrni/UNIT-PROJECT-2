import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def delete_migration_files(app_name):
    migrations_path = os.path.join(BASE_DIR, app_name, 'migrations')
    if not os.path.exists(migrations_path):
        return

    for filename in os.listdir(migrations_path):
        file_path = os.path.join(migrations_path, filename)
        if filename != '__init__.py' and filename.endswith('.py'):
            os.remove(file_path)
            print(f"Deleted {file_path}")
        elif filename.endswith('.pyc'):
            os.remove(file_path)

apps = ['app_main', 'accounts', 'app_business', 'wallet']

for app in apps:
    delete_migration_files(app)

db_path = os.path.join(BASE_DIR, 'db.sqlite3')
if os.path.exists(db_path):
    os.remove(db_path)
    print("Deleted db.sqlite3")

print("✅ Done cleaning migrations and database.")
